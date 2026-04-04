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


# Required fields for CIP headers
CIP_REQUIRED_FIELDS = {
    'CIP', 'Title', 'Category', 'Status', 'Authors', 
    'Implementors', 'Discussions', 'Created', 'License'
}

# Required sections (H2 headers)
CIP_REQUIRED_SECTIONS = {
    'Abstract',
    'Motivation: why is this CIP necessary?',
    'Specification',
    'Rationale: how does this CIP achieve its goals?',
    'Path to Active',
    'Copyright'
}

# Required subsections for Path to Active (H3 headers)
PATH_TO_ACTIVE_SUBSECTIONS = {
    'Acceptance Criteria',
    'Implementation Plan'
}

# Optional fields (allowed but not required)
CIP_OPTIONAL_FIELDS = {
    'Solution-To'
}

# Optional H2 sections (allowed but not required)
CIP_OPTIONAL_SECTIONS = {
    'Versioning',
    'References',
    'Appendix',
    'Appendices',
    'Acknowledgments',
    'Acknowledgements'
}

# Load CIP header schema
SCHEMA_PATH = Path(__file__).parent.parent / 'schemas' / 'cip-header.schema.json'
try:
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        CIP_HEADER_SCHEMA = json.load(f)
except FileNotFoundError:
    CIP_HEADER_SCHEMA = None
    print(f"Warning: Schema file not found at {SCHEMA_PATH}. Schema validation will be skipped.", file=sys.stderr)
except json.JSONDecodeError as e:
    CIP_HEADER_SCHEMA = None
    print(f"Warning: Invalid JSON schema file: {e}. Schema validation will be skipped.", file=sys.stderr)


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], Optional[str]]:
    """Parse YAML frontmatter from markdown content.
    
    Returns:
        Tuple of (frontmatter_dict, remaining_content) or (None, content) if no frontmatter
    """
    # Check for frontmatter delimiters - must start with ---
    if not content.startswith('---'):
        return None, content
    
    # Find the closing delimiter (--- on its own line)
    # Split on '\n---\n' or '\n---' at end of content
    lines = content.split('\n')
    if lines[0] != '---':
        return None, content
    
    # Find the closing ---
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i] == '---':
            end_idx = i
            break
    
    if end_idx is None:
        return None, content
    
    # Extract frontmatter (lines between the two --- markers)
    frontmatter_lines = lines[1:end_idx]
    frontmatter_text = '\n'.join(frontmatter_lines)
    
    # Extract remaining content (everything after the closing ---)
    remaining_lines = lines[end_idx + 1:]
    remaining_content = '\n'.join(remaining_lines)
    
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if frontmatter is None:
            return None, content
        return frontmatter, remaining_content
    except yaml.YAMLError as e:
        return None, content


def extract_h2_headers(content: str) -> List[str]:
    """Extract all H2 headers (##) from markdown content."""
    h2_pattern = r'^##\s+(.+)$'
    headers = []
    for line in content.split('\n'):
        match = re.match(h2_pattern, line)
        if match:
            headers.append(match.group(1).strip())
    return headers


def extract_h3_headers_under_section(content: str, section_name: str) -> List[str]:
    """Extract H3 headers (###) that appear under a specific H2 section."""
    lines = content.split('\n')
    h3_headers = []
    in_section = False
    
    for line in lines:
        # Check if we're entering the target section
        h2_match = re.match(r'^##\s+(.+)$', line)
        if h2_match:
            current_section = h2_match.group(1).strip()
            in_section = (current_section == section_name)
            continue
        
        # If we're in the target section, collect H3 headers
        if in_section:
            h3_match = re.match(r'^###\s+(.+)$', line)
            if h3_match:
                h3_headers.append(h3_match.group(1).strip())
            # Stop if we hit another H2 section
            elif line.startswith('## '):
                break
    
    return h3_headers


def extract_h1_headers(content: str) -> List[str]:
    """Extract all H1 headers (#) from markdown content."""
    h1_pattern = r'^#\s+(.+)$'
    headers = []
    for line in content.split('\n'):
        match = re.match(h1_pattern, line)
        if match:
            headers.append(match.group(1).strip())
    return headers


def validate_line_endings(file_path: Path) -> List[str]:
    """Validate that file uses UNIX line endings (LF, not CRLF).
    
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    try:
        # Read file in binary mode to check line endings
        with open(file_path, 'rb') as f:
            content_bytes = f.read()
        
        # Check for CRLF (\r\n) - Windows line endings
        if b'\r\n' in content_bytes:
            errors.append("File uses Windows line endings (CRLF). Use UNIX line endings (LF) instead.")
        
        # Check for standalone \r without \n (old Mac line endings)
        # Replace CRLF first, then check for remaining CR
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


def validate_header(frontmatter: Dict) -> List[str]:
    """Validate the YAML frontmatter header for CIPs.
    
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    # Use JSON Schema validation for CIP headers if schema is available
    if CIP_HEADER_SCHEMA is not None:
        try:
            # Convert date objects to strings for schema validation
            # JSON Schema expects dates as strings, but PyYAML may parse them as date objects
            frontmatter_for_schema = {}
            for key, value in frontmatter.items():
                if key == 'Created' and hasattr(value, 'isoformat'):
                    # Handle date objects from PyYAML (datetime.date or datetime.datetime)
                    frontmatter_for_schema[key] = value.isoformat()
                else:
                    frontmatter_for_schema[key] = value
            
            jsonschema.validate(instance=frontmatter_for_schema, schema=CIP_HEADER_SCHEMA)
        except jsonschema.ValidationError as e:
            # Format JSON Schema validation errors in a user-friendly way
            error_path = '.'.join(str(p) for p in e.path) if e.path else 'root'
            errors.append(f"Header validation error at '{error_path}': {e.message}")
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")
    else:
        # Fallback to manual validation if schema is not available
        errors.extend(_validate_header_manual(frontmatter))
    
    return errors


def _validate_header_manual(frontmatter: Dict) -> List[str]:
    """Manual validation fallback (used when schema is unavailable).
    
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    # Check for required fields
    missing_fields = CIP_REQUIRED_FIELDS - set(frontmatter.keys())
    if missing_fields:
        errors.append(f"Missing required header fields: {', '.join(sorted(missing_fields))}")
    
    # Check for extra fields (strict validation, but allow optional fields)
    allowed_fields = CIP_REQUIRED_FIELDS.copy()
    allowed_fields.update(CIP_OPTIONAL_FIELDS)
    
    extra_fields = set(frontmatter.keys()) - allowed_fields
    if extra_fields:
        errors.append(f"Unexpected header fields: {', '.join(sorted(extra_fields))}")
    
    # Validate field formats
    if 'Authors' in frontmatter:
        if not isinstance(frontmatter['Authors'], list):
            errors.append("'Authors' field must be a list")
        elif len(frontmatter['Authors']) == 0:
            errors.append("'Authors' field must contain at least one author")
    
    if 'Discussions' in frontmatter:
        if not isinstance(frontmatter['Discussions'], list):
            errors.append("'Discussions' field must be a list")
    
    if 'Created' in frontmatter:
        created = frontmatter['Created']
        # PyYAML may parse dates as date objects, so convert to string for validation
        # Handle both string and date object types
        if created is None:
            errors.append("'Created' field must be in YYYY-MM-DD format")
        else:
            # Convert to string (handles date objects from PyYAML)
            created_str = str(created)
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', created_str):
                errors.append(f"'Created' field must be in YYYY-MM-DD format, got: {created_str}")
    
    if 'Implementors' in frontmatter:
        # Implementors can be a list or "N/A"
        if not isinstance(frontmatter['Implementors'], (list, str)):
            errors.append("'Implementors' field must be a list or 'N/A'")
    
    if 'Solution-To' in frontmatter:
        # Solution-To should be a list of CPS references
        if not isinstance(frontmatter['Solution-To'], list):
            errors.append("'Solution-To' field must be a list")
    
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
        # Map back to original case from required_sections for error message
        missing_sections = {orig for orig in CIP_REQUIRED_SECTIONS 
                          if orig.lower() in missing_sections_lower}
        errors.append(f"Missing required sections: {', '.join(sorted(missing_sections))}")
    
    # Check Path to Active subsections (case-insensitive check)
    path_to_active_found = any(h.lower() == 'path to active' for h in found_sections)
    if path_to_active_found:
        h3_headers = extract_h3_headers_under_section(content, 'Path to Active')
        # Normalize headers to lowercase for case-insensitive comparison
        found_subsections_lower = {h.lower() for h in h3_headers}
        required_subsections_lower = {h.lower() for h in PATH_TO_ACTIVE_SUBSECTIONS}
        missing_subsections_lower = required_subsections_lower - found_subsections_lower
        if missing_subsections_lower:
            # Map back to original case for error message
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
    # Normalize path separators and check for CIP- pattern
    # Handles both absolute (/CIP-123/) and relative (CIP-123/) paths
    # Also handles Windows paths (CIP-123\README.md)
    normalized_path = path_str.replace('\\', '/')
    
    # Check for CIP- pattern (with or without leading slash)
    return bool(re.search(r'(^|/)CIP-', normalized_path, re.IGNORECASE))


def validate_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Validate a single CIP README.md file.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check if this is a CIP file
    if not is_cip_file(file_path):
        return False, [f"File path does not indicate a CIP document: {file_path}"]
    
    # Validate line endings (must check raw file bytes)
    line_ending_errors = validate_line_endings(file_path)
    errors.extend(line_ending_errors)
    
    # Read file content
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Error reading file: {e}"]
    
    # Parse frontmatter
    frontmatter, remaining_content = parse_frontmatter(content)
    if frontmatter is None:
        errors.append("Missing or invalid YAML frontmatter (must start with '---' and end with '---')")
        return False, errors
    
    # Validate header
    header_errors = validate_header(frontmatter)
    errors.extend(header_errors)
    
    # Validate no H1 headings
    h1_errors = validate_no_h1_headings(remaining_content)
    errors.extend(h1_errors)
    
    # Validate sections
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

