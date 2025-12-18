#!/usr/bin/env python3
"""
Fix page includes - Replace JavaScript fetch() calls with actual include content
This fixes display issues on ebooks.html, audiobooks.html, and landing pages
"""

import os
import re
from pathlib import Path

# Base directory
BASE_DIR = Path("/home/user/iD01t.github.io")

# Read include files
with open(BASE_DIR / "includes/header.html", "r", encoding="utf-8") as f:
    HEADER_CONTENT = f.read()

with open(BASE_DIR / "includes/footer.html", "r", encoding="utf-8") as f:
    FOOTER_CONTENT = f.read()

with open(BASE_DIR / "includes/consent-banner.html", "r", encoding="utf-8") as f:
    CONSENT_CONTENT = f.read()

def fix_page(file_path):
    """Fix a single page by replacing fetch() calls with actual include content"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        original_content = content

        # Pattern 1: Header loading via fetch (at beginning of body)
        header_pattern = r'(<!-- Shared Header -->.*?<script>.*?fetch\(\'/includes/header\.html\'\).*?</script>)'
        if re.search(header_pattern, content, re.DOTALL):
            content = re.sub(
                header_pattern,
                f'<!-- Shared Header (from includes/header.html) -->\n{HEADER_CONTENT}',
                content,
                flags=re.DOTALL
            )
            print(f"  ✓ Replaced header fetch in {file_path.name}")

        # Pattern 2: Footer loading via fetch
        footer_pattern = r'(<!-- Shared Footer -->.*?<script>.*?fetch\(\'/includes/footer\.html\'\).*?</script>)'
        if re.search(footer_pattern, content, re.DOTALL):
            content = re.sub(
                footer_pattern,
                f'<!-- Shared Footer (from includes/footer.html) -->\n{FOOTER_CONTENT}',
                content,
                flags=re.DOTALL
            )
            print(f"  ✓ Replaced footer fetch in {file_path.name}")

        # Pattern 3: Consent banner loading via fetch
        consent_pattern = r'(<!-- Consent Banner -->.*?<script>.*?fetch\(\'/includes/consent-banner\.html\'\).*?</script>)'
        if re.search(consent_pattern, content, re.DOTALL):
            content = re.sub(
                consent_pattern,
                f'<!-- Consent Banner (from includes/consent-banner.html) -->\n{CONSENT_CONTENT}',
                content,
                flags=re.DOTALL
            )
            print(f"  ✓ Replaced consent banner fetch in {file_path.name}")

        # Only write if content changed
        if content != original_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"  ✗ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix all pages with fetch() includes"""
    print("=" * 60)
    print("Fixing Page Includes - Replacing fetch() with static content")
    print("=" * 60)

    files_to_fix = []

    # Main catalog pages
    files_to_fix.extend([
        BASE_DIR / "ebooks.html",
        BASE_DIR / "audiobooks.html"
    ])

    # Landing pages
    landing_pages_dir = BASE_DIR / "landing_pages_new"
    if landing_pages_dir.exists():
        files_to_fix.extend(landing_pages_dir.rglob("*.html"))

    fixed_count = 0
    for file_path in files_to_fix:
        if file_path.exists():
            print(f"\nProcessing: {file_path.relative_to(BASE_DIR)}")
            if fix_page(file_path):
                fixed_count += 1

    print("\n" + "=" * 60)
    print(f"✅ Fixed {fixed_count} pages")
    print("=" * 60)

if __name__ == "__main__":
    main()
