#!/usr/bin/env python3
"""
Validation script for CIP README.md files.
Validates YAML headers and required sections.
"""

import sys
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema library is required. Install it with: pip install jsonschema", file=sys.stderr)
    sys.exit(1)


# Required fields for CIP headers (in required order)
CIP_REQUIRED_FIELDS_ORDER = [
    'CIP', 'Title', 'Category', 'Status', 'Authors',
    'Implementors', 'Discussions', 'Created', 'License'
]
CIP_REQUIRED_FIELDS = set(CIP_REQUIRED_FIELDS_ORDER)

# Optional fields (allowed but not required)
CIP_OPTIONAL_FIELDS = {'Solution-To'}

# Required sections (H2 headers) in required order
CIP_REQUIRED_SECTIONS_ORDER = [
    'Abstract',
    'Motivation: why is this CIP necessary?',
    'Specification',
    'Rationale: how does this CIP achieve its goals?',
    'Path to Active',
    'Copyright',
]
CIP_REQUIRED_SECTIONS = set(CIP_REQUIRED_SECTIONS_ORDER)

# Optional H2 sections (allowed but not required)
# These should appear after the required sections, before Copyright
CIP_OPTIONAL_SECTIONS = {
    'Versioning',
    'References',
    'Appendix',
    'Appendices',
    'Acknowledgments',
    'Acknowledgements',
}

# Required H3 subsections under "Path to Active"
PATH_TO_ACTIVE_SUBSECTIONS = {
    'Acceptance Criteria',
    'Implementation Plan',
}

# Load CIP header schema
SCHEMA_PATH = Path(__file__).parent.parent / 'schemas' / 'cip-header.schema.json'
with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
    CIP_HEADER_SCHEMA = json.load(f)


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], Optional[str], Optional[List[str]]]:
    """Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter_dict, remaining_content, raw_lines) or (None, content, None) if no frontmatter
    """
    # Check for frontmatter delimiters - must start with ---
    if not content.startswith('---'):
        return None, content, None

    # Find the closing delimiter (--- on its own line)
    lines = content.split('\n')
    if lines[0] != '---':
        return None, content, None

    # Find the closing ---
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i] == '---':
            end_idx = i
            break

    if end_idx is None:
        return None, content, None

    # Extract frontmatter (lines between the two --- markers)
    frontmatter_lines = lines[1:end_idx]

    # Preprocess: quote standalone '?' values (YAML interprets '?' as explicit key indicator)
    processed_lines = []
    for line in frontmatter_lines:
        # Match lines like "CIP: ?" or "Category: ?" and quote the ?
        if re.match(r'^[A-Za-z][A-Za-z -]*:\s+\?+\s*$', line):
            line = re.sub(r':\s+(\?+)\s*$', r': "\1"', line)
        processed_lines.append(line)

    frontmatter_text = '\n'.join(processed_lines)

    # Extract remaining content (everything after the closing ---)
    remaining_lines = lines[end_idx + 1:]
    remaining_content = '\n'.join(remaining_lines)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if frontmatter is None:
            return None, content, None
        return frontmatter, remaining_content, frontmatter_lines
    except yaml.YAMLError:
        return None, content, None
    except ValueError:
        # Catches invalid date values that YAML tries to parse (e.g., month 13)
        return None, content, None


def extract_h2_headers(content: str) -> List[str]:
    """Extract all H2 headers (##) from markdown content."""
    h2_pattern = r'^##\s+(.+)$'
    headers = []
    for line in content.split('\n'):
        match = re.match(h2_pattern, line)
        if match:
            headers.append(match.group(1).strip())
    return headers


def extract_h1_headers(content: str) -> List[str]:
    """Extract all H1 headers (#) from markdown content."""
    h1_pattern = r'^#\s+(.+)$'
    headers = []
    for line in content.split('\n'):
        match = re.match(h1_pattern, line)
        if match:
            headers.append(match.group(1).strip())
    return headers


def extract_h3_headers_under_section(content: str, section_name: str) -> List[str]:
    """Extract H3 headers (###) that appear under a specific H2 section."""
    lines = content.split('\n')
    h3_headers = []
    in_section = False

    for line in lines:
        h2_match = re.match(r'^##\s+(.+)$', line)
        if h2_match:
            current_section = h2_match.group(1).strip()
            in_section = (current_section == section_name)
            continue

        if in_section:
            h3_match = re.match(r'^###\s+(.+)$', line)
            if h3_match:
                h3_headers.append(h3_match.group(1).strip())
            elif line.startswith('## '):
                break

    return h3_headers


def validate_line_endings(file_path: Path) -> List[str]:
    """Validate that file uses UNIX line endings (LF, not CRLF).

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    try:
        with open(file_path, 'rb') as f:
            content_bytes = f.read()

        if b'\r\n' in content_bytes:
            errors.append("File uses Windows line endings (CRLF). Use UNIX line endings (LF) instead.")

        # Check for standalone \r without \n (old Mac line endings)
        content_without_crlf = content_bytes.replace(b'\r\n', b'')
        if b'\r' in content_without_crlf:
            errors.append("File uses old Mac line endings (CR). Use UNIX line endings (LF) instead.")
    except Exception as e:
        errors.append(f"Error checking line endings: {e}")

    return errors


def validate_no_h1_headings(content: str) -> List[str]:
    """Validate that no H1 headings are present in the document.

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    h1_headers = extract_h1_headers(content)
    if h1_headers:
        errors.append(f"H1 headings are not allowed. Found: {', '.join(h1_headers)}")

    return errors


def _validate_field_order(frontmatter: Dict) -> List[str]:
    """Validate that header fields appear in the correct order.

    Optional fields (e.g., Solution-To) may appear at any position and are
    ignored for the order check; only the required-field order is enforced.

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    actual_fields = list(frontmatter.keys())

    # Filter to only known required fields (ignore optional/extra fields for order check)
    actual_required = [f for f in actual_fields if f in CIP_REQUIRED_FIELDS]

    # Build expected order based on which required fields are present
    expected_order = [f for f in CIP_REQUIRED_FIELDS_ORDER if f in actual_required]

    if actual_required != expected_order:
        errors.append(
            f"Header fields are not in the correct order. "
            f"Expected: {', '.join(expected_order)}. "
            f"Got: {', '.join(actual_required)}"
        )

    return errors


def _validate_label_entries(entries: list, field_name: str, label_prefixes: List[str]) -> List[str]:
    """Validate semantic rules for labeled 'Label: URL' entries.

    When a label matches one of the given prefixes followed by -NNNN (e.g., CIP-0030):
    - URL must be a GitHub CIPs repository link (PR or merged document)
    - Pull request URLs require '?' suffix on the number (candidate)
    - Merged URLs must NOT have '?' suffix

    Other labels are allowed with any valid URL.

    Args:
        entries: List of label-URL entries (strings 'Label: URL' or dicts {Label: URL})
        field_name: Name of the field for error messages
        label_prefixes: List of label prefixes to validate (e.g., ['CIP'], ['CIP', 'CPS'])

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    if not isinstance(entries, list):
        return errors

    prefix_group = '|'.join(label_prefixes)
    label_pattern = re.compile(rf'^({prefix_group})-\d+(\?)?$')
    pr_pattern = re.compile(r'https://github\.com/cardano-foundation/CIPs/pull/\d+')
    merged_pattern = re.compile(
        rf'https://github\.com/cardano-foundation/CIPs/(tree|blob)/[^/]+/({prefix_group})-\d+'
    )
    github_cips_pattern = re.compile(
        rf'^https://github\.com/cardano-foundation/CIPs/(pull/\d+|tree/[^/]+/({prefix_group})-\d+|blob/[^/]+/({prefix_group})-\d+)'
    )

    for i, entry in enumerate(entries):
        if isinstance(entry, dict) and len(entry) == 1:
            label, url = next(iter(entry.items()))
        elif isinstance(entry, str):
            match = re.match(r'^([^:]+):\s+(.+)$', entry)
            if not match:
                continue
            label, url = match.groups()
        else:
            continue

        label = label.strip()
        url = url.strip()

        label_match = label_pattern.match(label)
        if not label_match:
            continue  # Non-matching labels are allowed with any URL

        ref_id = label_match.group(0).rstrip('?')
        has_question_mark = label_match.group(2) == '?'

        if not github_cips_pattern.match(url):
            errors.append(
                f"'{field_name}' entry {i+1}: label '{label}' requires a GitHub CIPs repository URL "
                f"(pull request or merged document). Got: {url}"
            )
            continue

        is_pr = pr_pattern.search(url) is not None
        is_merged = merged_pattern.search(url) is not None

        if is_pr and not has_question_mark:
            errors.append(
                f"'{field_name}' entry {i+1}: Pull request URL requires '?' suffix on the reference "
                f"(use '{ref_id}?' instead of '{ref_id}' to indicate candidate status)"
            )
        elif is_merged and has_question_mark:
            errors.append(
                f"'{field_name}' entry {i+1}: Merged document should not have '?' suffix "
                f"(use '{ref_id}' instead of '{ref_id}?' since this document is merged)"
            )

    return errors


def validate_header(frontmatter: Dict) -> List[str]:
    """Validate the YAML frontmatter header for CIPs.

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    # Validate field order
    errors.extend(_validate_field_order(frontmatter))

    # Normalize and run JSON Schema validation
    try:
        frontmatter_for_schema = {}
        for key, value in frontmatter.items():
            if key == 'Created' and hasattr(value, 'isoformat'):
                # Handle date objects from PyYAML (datetime.date or datetime.datetime)
                frontmatter_for_schema[key] = value.isoformat()
            elif key == 'Discussions' and isinstance(value, list):
                # Convert dictionary entries to string format "Label: URL"
                normalized_list = []
                for item in value:
                    if isinstance(item, dict):
                        if len(item) == 1:
                            label, url = next(iter(item.items()))
                            normalized_list.append(f"{label}: {url}")
                        else:
                            normalized_list.append(": ".join(f"{k}: {v}" for k, v in item.items()))
                    elif isinstance(item, str):
                        normalized_list.append(item)
                    else:
                        normalized_list.append(str(item))
                frontmatter_for_schema[key] = normalized_list
            else:
                frontmatter_for_schema[key] = value

        jsonschema.validate(instance=frontmatter_for_schema, schema=CIP_HEADER_SCHEMA)
    except jsonschema.ValidationError as e:
        error_path = '.'.join(str(p) for p in e.path) if e.path else 'root'
        errors.append(f"Header validation error at '{error_path}': {e.message}")
    except jsonschema.SchemaError as e:
        errors.append(f"Schema error: {e.message}")

    # Validate CIP/CPS label semantic rules on Discussions
    if 'Discussions' in frontmatter:
        errors.extend(_validate_label_entries(frontmatter['Discussions'], 'Discussions', ['CIP', 'CPS']))

    return errors


def validate_sections(content: str) -> List[str]:
    """Validate required sections exist at H2 level for CIPs.

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    h2_headers = extract_h2_headers(content)
    found_sections = set(h2_headers)

    # Normalize headers to lowercase for case-insensitive comparison
    found_sections_lower = {h.lower() for h in found_sections}
    required_sections_lower = {h.lower() for h in CIP_REQUIRED_SECTIONS}
    optional_sections_lower = {h.lower() for h in CIP_OPTIONAL_SECTIONS}

    # Check for missing required sections (case-insensitive)
    missing_sections_lower = required_sections_lower - found_sections_lower
    if missing_sections_lower:
        missing_sections = {orig for orig in CIP_REQUIRED_SECTIONS
                            if orig.lower() in missing_sections_lower}
        errors.append(f"Missing required sections: {', '.join(sorted(missing_sections))}")

    # Check for unknown sections (not in required or optional)
    allowed_sections_lower = required_sections_lower | optional_sections_lower
    for header in h2_headers:
        if header.lower() not in allowed_sections_lower:
            errors.append(f"Unknown section: '{header}'. Only required and optional sections are allowed.")

    # Build a mapping from lowercase to expected capitalization
    expected_capitalization = {}
    for section in CIP_REQUIRED_SECTIONS:
        expected_capitalization[section.lower()] = section
    for section in CIP_OPTIONAL_SECTIONS:
        expected_capitalization[section.lower()] = section

    # Check for incorrect capitalization
    for header in h2_headers:
        header_lower = header.lower()
        if header_lower in expected_capitalization:
            expected = expected_capitalization[header_lower]
            if header != expected:
                errors.append(f"Section '{header}' has incorrect capitalization. Expected: '{expected}'")

    # Map found headers to their canonical names (for order comparison)
    canonical_headers = []
    for header in h2_headers:
        header_lower = header.lower()
        if header_lower in expected_capitalization:
            canonical_headers.append(expected_capitalization[header_lower])
        else:
            canonical_headers.append(header)

    # Extract just the required sections in the order they appear
    found_required_order = [h for h in canonical_headers if h in CIP_REQUIRED_SECTIONS]

    expected_required_order = [s for s in CIP_REQUIRED_SECTIONS_ORDER if s in found_required_order]

    if found_required_order != expected_required_order:
        errors.append(
            f"Sections are not in the correct order. "
            f"Expected: {', '.join(expected_required_order)}. "
            f"Got: {', '.join(found_required_order)}"
        )

    # Check that optional sections appear only between the last non-Copyright
    # required section ("Path to Active") and "Copyright".
    optional_sections_normalized = {s.lower() for s in CIP_OPTIONAL_SECTIONS}
    required_before_optional = [s for s in CIP_REQUIRED_SECTIONS_ORDER if s != 'Copyright']

    for i, header in enumerate(canonical_headers):
        header_lower = header.lower()
        if header_lower in optional_sections_normalized:
            for j in range(i + 1, len(canonical_headers)):
                following_header = canonical_headers[j]
                if following_header in required_before_optional:
                    errors.append(
                        f"Optional section '{header}' appears before required section '{following_header}'. "
                        f"Optional sections must appear after 'Path to Active' and before 'Copyright'."
                    )
                    break

    # CIP-specific: validate Path to Active H3 subsections
    path_to_active_found = any(h.lower() == 'path to active' for h in found_sections)
    if path_to_active_found:
        # Find the actual header text used (may have wrong capitalization)
        actual_header = next((h for h in h2_headers if h.lower() == 'path to active'), 'Path to Active')
        h3_headers = extract_h3_headers_under_section(content, actual_header)
        found_subsections_lower = {h.lower() for h in h3_headers}
        required_subsections_lower = {h.lower() for h in PATH_TO_ACTIVE_SUBSECTIONS}
        missing_subsections_lower = required_subsections_lower - found_subsections_lower
        if missing_subsections_lower:
            missing_subsections = {orig for orig in PATH_TO_ACTIVE_SUBSECTIONS
                                   if orig.lower() in missing_subsections_lower}
            errors.append(
                f"'Path to Active' section missing required subsections: "
                f"{', '.join(sorted(missing_subsections))}"
            )

    return errors


def is_cip_file(file_path: Path) -> bool:
    """Check if file path indicates a CIP document."""
    path_str = str(file_path)
    normalized_path = path_str.replace('\\', '/')
    return bool(re.search(r'(^|/)CIP-', normalized_path, re.IGNORECASE))


def validate_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Validate a single CIP README.md file.

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    if not is_cip_file(file_path):
        return False, [f"File path does not indicate a CIP document: {file_path}"]

    # Validate line endings (must check raw file bytes)
    line_ending_errors = validate_line_endings(file_path)
    errors.extend(line_ending_errors)

    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Error reading file: {e}"]

    frontmatter, remaining_content, raw_lines = parse_frontmatter(content)
    if frontmatter is None:
        errors.append("Missing or invalid YAML frontmatter (must start with '---' and end with '---')")
        return False, errors

    # Check for leading zeros in CIP field (YAML loses this information)
    if raw_lines:
        for line in raw_lines:
            if re.match(r'^CIP:\s+0\d+', line):
                errors.append("CIP number must not have leading zeros")
                break

    header_errors = validate_header(frontmatter)
    errors.extend(header_errors)

    h1_errors = validate_no_h1_headings(remaining_content)
    errors.extend(h1_errors)

    section_errors = validate_sections(remaining_content)
    errors.extend(section_errors)

    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    """Main entry point for the validation script."""
    if len(sys.argv) < 2:
        print("Usage: validate-cip.py <file1> [file2] ...", file=sys.stderr)
        sys.exit(1)

    files_to_validate = [Path(f) for f in sys.argv[1:]]
    all_valid = True
    all_errors = []

    for file_path in files_to_validate:
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            all_valid = False
            continue

        is_valid, errors = validate_file(file_path)

        if not is_valid:
            all_valid = False
            print(f"\nValidation failed for {file_path}:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            all_errors.append((file_path, errors))

    if not all_valid:
        print(f"\nValidation failed for {len(all_errors)} file(s)", file=sys.stderr)
        sys.exit(1)

    print(f"\nAll {len(files_to_validate)} file(s) passed validation", file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
