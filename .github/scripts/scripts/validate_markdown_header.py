import re
import sys
import os
import json

REQUIRED_FIELDS_CPS = ["CPS", "Title", "Status", "Category", "Authors", "Proposed Solutions", "Discussions", "Created", "License"]
REQUIRED_FIELDS_CIP = ["CIP", "Title", "Category", "Status", "Authors", "Implementors", "Discussions", "Created", "License"]

HEADER_PATTERN = re.compile(r"---(.*?)---", re.DOTALL)

def validate_header(content):
    match = HEADER_PATTERN.search(content)
    if not match:
        return False, "No valid header found"
    
    header_text = match.group(1).strip()
    lines = [line.strip() for line in header_text.split("\n") if line.strip()]
    fields = [line.split(":")[0] for line in lines if ":" in line]
    
    if fields == REQUIRED_FIELDS_CPS or fields == REQUIRED_FIELDS_CIP:
        return True, "Valid header"
    return False, "Header fields are missing or out of order"

def main():
    failed_files = []
    files = json.loads(os.getenv("FILES", "[]"))
    
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            valid, message = validate_header(content)
            if not valid:
                failed_files.append((file, message))
    
    if failed_files:
        print("Markdown header validation failed for the following files:")
        for file, message in failed_files:
            print(f"- {file}: {message}")
        sys.exit(1)
    else:
        print("All markdown files have valid headers.")

if __name__ == "__main__":
    main()
