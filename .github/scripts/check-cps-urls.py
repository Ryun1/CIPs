#!/usr/bin/env python3
"""URL liveness checker for CPS README.md files.

Extracts every URL referenced in a CPS document (header fields + markdown body)
and verifies each one resolves to a live resource. Used by .github/workflows/cps-validation.yaml.
"""

import sys
import re
import time
import yaml
import socket
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Set, Tuple

USER_AGENT = (
    "Mozilla/5.0 (compatible; cardano-foundation-CIPs-CPS-Validator/1.0; "
    "+https://github.com/cardano-foundation/CIPs)"
)
TIMEOUT_SECONDS = 10
MAX_WORKERS = 8
RETRY_BACKOFF_SECONDS = 2
TRANSIENT_STATUSES = {500, 502, 503, 504}
AUTH_OK_STATUSES = {401, 403}  # Resource exists, just requires auth


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """Parse YAML frontmatter, returning (frontmatter_dict, body_text)."""
    if not content.startswith('---'):
        return {}, content
    lines = content.split('\n')
    if lines[0] != '---':
        return {}, content
    end_idx = next((i for i in range(1, len(lines)) if lines[i] == '---'), None)
    if end_idx is None:
        return {}, content

    # Quote standalone '?' values so YAML doesn't choke
    processed = []
    for line in lines[1:end_idx]:
        if re.match(r'^[A-Za-z][A-Za-z ]*:\s+\?+\s*$', line):
            line = re.sub(r':\s+(\?+)\s*$', r': "\1"', line)
        processed.append(line)

    try:
        fm = yaml.safe_load('\n'.join(processed)) or {}
    except (yaml.YAMLError, ValueError):
        fm = {}
    body = '\n'.join(lines[end_idx + 1:])
    return fm, body


def _strip_code_and_comments(text: str) -> str:
    """Remove fenced code blocks and HTML comments so URLs inside aren't checked."""
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'~~~.*?~~~', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`\n]+`', '', text)
    return text


URL_RE = re.compile(r'https?://[^\s<>\)\]\}"\'`]+', re.IGNORECASE)


def _clean_trailing(url: str) -> str:
    """Strip trailing punctuation that's likely sentence-level, not URL-level."""
    while url and url[-1] in '.,;:!?':
        url = url[:-1]
    return url


def extract_urls_from_header(frontmatter: Dict) -> Set[str]:
    """Pull URLs from labeled-list fields like Discussions / Proposed Solutions."""
    urls: Set[str] = set()
    for field in ('Discussions', 'Proposed Solutions'):
        entries = frontmatter.get(field) or []
        if not isinstance(entries, list):
            continue
        for entry in entries:
            url = None
            if isinstance(entry, dict) and len(entry) == 1:
                url = next(iter(entry.values()))
            elif isinstance(entry, str):
                m = re.match(r'^[^:]+:\s+(.+)$', entry)
                if m:
                    url = m.group(1).strip()
            if url:
                m2 = URL_RE.search(str(url))
                if m2:
                    urls.add(_clean_trailing(m2.group(0)))
    return urls


def extract_urls_from_body(body: str) -> Set[str]:
    """Pull URLs from markdown body: [label](url), <url>, and bare URLs."""
    text = _strip_code_and_comments(body)
    urls: Set[str] = set()
    for m in URL_RE.finditer(text):
        urls.add(_clean_trailing(m.group(0)))
    return urls


def find_line_numbers(content: str, url: str) -> List[int]:
    """Return 1-indexed line numbers where `url` appears in `content`."""
    return [i + 1 for i, line in enumerate(content.split('\n')) if url in line]


def _request(url: str, method: str) -> Tuple[int, str]:
    """One HTTP request. Returns (status_code, reason)."""
    req = urllib.request.Request(url, method=method, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        return resp.status, resp.reason or ''


def check_url(url: str) -> Tuple[str, str, str]:
    """Check a single URL. Returns (url, classification, detail).

    classification is one of 'alive', 'dead', 'transient'.
    """
    def _attempt(method: str):
        try:
            status, reason = _request(url, method)
            return ('http', status, reason)
        except urllib.error.HTTPError as e:
            return ('http', e.code, e.reason or '')
        except (urllib.error.URLError, socket.timeout, ConnectionError, TimeoutError) as e:
            return ('net', None, str(e))

    # HEAD first, fall back to GET on 405/501 or some networks that reject HEAD
    kind, status, detail = _attempt('HEAD')
    if kind == 'http' and status in (405, 501):
        kind, status, detail = _attempt('GET')

    # Retry once on transient
    needs_retry = kind == 'net' or (kind == 'http' and status in TRANSIENT_STATUSES)
    if needs_retry:
        time.sleep(RETRY_BACKOFF_SECONDS)
        kind, status, detail = _attempt('GET')

    if kind == 'net':
        return (url, 'transient', f'network error: {detail}')
    if 200 <= status < 400 or status in AUTH_OK_STATUSES:
        return (url, 'alive', f'HTTP {status}')
    if status in TRANSIENT_STATUSES:
        return (url, 'transient', f'HTTP {status} {detail}')
    return (url, 'dead', f'HTTP {status} {detail}')


def check_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Check all URLs in one CPS file. Returns (is_valid, messages).

    is_valid = True if no URLs classified as 'dead'. Transient results print warnings
    but do not fail.
    """
    content = file_path.read_text(encoding='utf-8')
    frontmatter, body = parse_frontmatter(content)
    urls = extract_urls_from_header(frontmatter) | extract_urls_from_body(body)

    if not urls:
        return True, [f"  (no URLs to check)"]

    messages: List[str] = []
    dead_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        future_to_url = {ex.submit(check_url, u): u for u in urls}
        for future in as_completed(future_to_url):
            url, classification, detail = future.result()
            if classification == 'dead':
                dead_count += 1
                lines = find_line_numbers(content, url)
                line_hint = f" (line {', '.join(map(str, lines))})" if lines else ""
                messages.append(f"  DEAD: {url} -- {detail}{line_hint}")
            elif classification == 'transient':
                lines = find_line_numbers(content, url)
                line_hint = f" (line {', '.join(map(str, lines))})" if lines else ""
                messages.append(f"  WARN: {url} -- {detail}{line_hint} [transient, not failing]")

    return (dead_count == 0), messages


def main():
    if len(sys.argv) < 2:
        print("Usage: check-cps-urls.py <file1> [file2] ...", file=sys.stderr)
        sys.exit(1)

    all_alive = True
    for raw in sys.argv[1:]:
        file_path = Path(raw)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            all_alive = False
            continue
        ok, messages = check_file(file_path)
        print(f"\nURL check for {file_path}:", file=sys.stderr)
        for m in messages:
            print(m, file=sys.stderr)
        if not ok:
            all_alive = False

    if not all_alive:
        print("\nURL check failed: one or more dead links detected.", file=sys.stderr)
        sys.exit(1)
    print("\nAll URLs reachable (transient errors ignored).", file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
