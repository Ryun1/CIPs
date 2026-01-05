#!/usr/bin/env python3
"""
Validation script for CIP and CPS README.md files.
Validates YAML frontmatter headers and required sections.
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional


# Required fields for CIP and CPS headers
CIP_REQUIRED_FIELDS = {
    'CIP', 'Title', 'Category', 'Status', 'Authors', 
    'Implementors', 'Discussions', 'Created', 'License'
}

CPS_REQUIRED_FIELDS = {
    'CPS', 'Title', 'Category', 'Status', 'Authors', 
    'Proposed Solutions', 'Discussions', 'Created', 'License'
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

CPS_REQUIRED_SECTIONS = {
    'Abstract',
    'Problem',
    'Use cases',
    'Goals',
    'Open Questions',
    'Copyright'
}

# Required subsections for Path to Active (H3 headers)
PATH_TO_ACTIVE_SUBSECTIONS = {
    'Acceptance Criteria',
    'Implementation Plan'
}


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


def validate_header(frontmatter: Dict, doc_type: str) -> List[str]:
    """Validate the YAML frontmatter header.
    
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    if doc_type == 'CIP':
        required_fields = CIP_REQUIRED_FIELDS
    elif doc_type == 'CPS':
        required_fields = CPS_REQUIRED_FIELDS
    else:
        return [f"Unknown document type: {doc_type}"]
    
    # Check for required fields
    missing_fields = required_fields - set(frontmatter.keys())
    if missing_fields:
        errors.append(f"Missing required header fields: {', '.join(sorted(missing_fields))}")
    
    # Check for extra fields (strict validation)
    extra_fields = set(frontmatter.keys()) - required_fields
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
    
    if doc_type == 'CIP' and 'Implementors' in frontmatter:
        # Implementors can be a list or "N/A"
        if not isinstance(frontmatter['Implementors'], (list, str)):
            errors.append("'Implementors' field must be a list or 'N/A'")
    
    if doc_type == 'CPS' and 'Proposed Solutions' in frontmatter:
        if not isinstance(frontmatter['Proposed Solutions'], list):
            errors.append("'Proposed Solutions' field must be a list")
    
    return errors


def validate_sections(content: str, doc_type: str) -> List[str]:
    """Validate required sections exist at H2 level.
    
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    if doc_type == 'CIP':
        required_sections = CIP_REQUIRED_SECTIONS
    elif doc_type == 'CPS':
        required_sections = CPS_REQUIRED_SECTIONS
    else:
        return [f"Unknown document type: {doc_type}"]
    
    h2_headers = extract_h2_headers(content)
    found_sections = set(h2_headers)
    
    # Check for missing sections
    missing_sections = required_sections - found_sections
    if missing_sections:
        errors.append(f"Missing required sections: {', '.join(sorted(missing_sections))}")
    
    # For CIP, check Path to Active subsections
    if doc_type == 'CIP' and 'Path to Active' in found_sections:
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


def determine_doc_type(file_path: Path) -> Optional[str]:
    """Determine document type (CIP or CPS) from file path."""
    path_str = str(file_path)
    # Normalize path separators and check for CIP- or CPS- patterns
    # Handles both absolute (/CIP-123/) and relative (CIP-123/) paths
    # Also handles Windows paths (CIP-123\README.md)
    normalized_path = path_str.replace('\\', '/')
    
    # Check for CIP- pattern (with or without leading slash)
    if re.search(r'(^|/)CIP-', normalized_path, re.IGNORECASE):
        return 'CIP'
    # Check for CPS- pattern (with or without leading slash)
    elif re.search(r'(^|/)CPS-', normalized_path, re.IGNORECASE):
        return 'CPS'
    return None


def validate_file(file_path: Path) -> Tuple[bool, List[str]]:
    """Validate a single README.md file.
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Determine document type
    doc_type = determine_doc_type(file_path)
    if not doc_type:
        return False, [f"Could not determine document type from path: {file_path}"]
    
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
    header_errors = validate_header(frontmatter, doc_type)
    errors.extend(header_errors)
    
    # Validate sections
    section_errors = validate_sections(remaining_content, doc_type)
    errors.extend(section_errors)
    
    is_valid = len(errors) == 0
    return is_valid, errors


def main():
    """Main entry point for the validation script."""
    if len(sys.argv) < 2:
        print("Usage: validate-cip-cps.py <file1> [file2] ...", file=sys.stderr)
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
            print(f"\n❌ Validation failed for {file_path}:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            all_errors.append((file_path, errors))
        else:
            print(f"✅ {file_path} is valid", file=sys.stderr)
    
    if not all_valid:
        print(f"\n❌ Validation failed for {len(all_errors)} file(s)", file=sys.stderr)
        sys.exit(1)
    
    print(f"\n✅ All {len(files_to_validate)} file(s) passed validation", file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()

