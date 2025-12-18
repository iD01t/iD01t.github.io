#!/usr/bin/env python3
"""
Comprehensive Website Display Verification
Checks all pages for common display issues
"""

import json
import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/home/user/iD01t.github.io")

issues = defaultdict(list)
warnings = defaultdict(list)
passed = []

def check_file(filepath):
    """Check a single HTML file for display issues"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        filename = filepath.name

        # Check 1: Has <!DOCTYPE html>
        if not content.strip().startswith('<!DOCTYPE html>') and not content.strip().startswith('<!DOCTYPE HTML>'):
            issues[filename].append("Missing DOCTYPE declaration")

        # Check 2: Has <html> tag
        if not re.search(r'<html[^>]*>', content, re.IGNORECASE):
            issues[filename].append("Missing <html> tag")

        # Check 3: Has <head> section
        if not re.search(r'<head[^>]*>', content, re.IGNORECASE):
            issues[filename].append("Missing <head> section")

        # Check 4: Has <body> tag
        if not re.search(r'<body[^>]*>', content, re.IGNORECASE):
            issues[filename].append("Missing <body> tag")

        # Check 5: Has <title> tag
        if not re.search(r'<title[^>]*>.*?</title>', content, re.IGNORECASE):
            warnings[filename].append("Missing <title> tag")

        # Check 6: Check for fetch() calls to wrong paths
        bad_fetch = re.findall(r'fetch\([\'"]([^\'"]+catalog\.json)[\'"]', content)
        for url in bad_fetch:
            if '/assets/catalog.json' in url:
                issues[filename].append(f"Using old catalog path: {url}")
            elif '/data/catalog.json' not in url and 'catalog.json' in url:
                warnings[filename].append(f"Unusual catalog path: {url}")

        # Check 7: Check for broken include references
        if 'fetch(\'/includes/header.html\')' in content:
            issues[filename].append("Using fetch() for header (should be inline)")
        if 'fetch(\'/includes/footer.html\')' in content:
            issues[filename].append("Using fetch() for footer (should be inline)")

        # Check 8: Has navigation
        if not re.search(r'<nav[^>]*>', content, re.IGNORECASE):
            warnings[filename].append("No <nav> element found")

        # Check 9: Check for very small files (likely broken)
        file_size = len(content)
        if file_size < 500:
            issues[filename].append(f"File very small ({file_size} bytes) - possibly broken")

        # Check 10: Has Tailwind CSS
        if 'tailwindcss.com' not in content and filename not in ['404.html']:
            warnings[filename].append("No Tailwind CSS reference found")

        # Check 11: Check for unclosed tags (basic check)
        open_divs = len(re.findall(r'<div[^>]*>', content))
        close_divs = len(re.findall(r'</div>', content))
        if abs(open_divs - close_divs) > 2:  # Allow small variance
            warnings[filename].append(f"Possible unclosed <div> tags (open: {open_divs}, close: {close_divs})")

        # If no issues, mark as passed
        if filename not in issues and filename not in warnings:
            passed.append(filename)

    except Exception as e:
        issues[filename].append(f"Error reading file: {e}")

# Check all main HTML files
html_files = list(BASE_DIR.glob("*.html"))
print(f"Checking {len(html_files)} HTML files...\n")

for filepath in html_files:
    check_file(filepath)

# Check catalog structure
print("=" * 70)
print("CATALOG VERIFICATION")
print("=" * 70)

try:
    with open(BASE_DIR / "data/catalog.json", "r") as f:
        catalog = json.load(f)

    print(f"✓ /data/catalog.json is valid JSON")
    print(f"  - Structure: {list(catalog.keys())}")
    print(f"  - eBooks: {len(catalog.get('ebooks', []))}")
    print(f"  - Audiobooks: {len(catalog.get('audiobooks', []))}")

    # Check if old catalog exists
    old_catalog = BASE_DIR / "assets/catalog.json"
    if old_catalog.exists():
        with open(old_catalog, "r") as f:
            old_cat = json.load(f)
        if old_cat == catalog:
            print(f"✓ /assets/catalog.json is synchronized")
        else:
            print(f"⚠ /assets/catalog.json is out of sync")

except Exception as e:
    print(f"✗ Error with catalog.json: {e}")

print()

# Print results
print("=" * 70)
print("CRITICAL ISSUES (Must Fix)")
print("=" * 70)

if issues:
    for filename, issue_list in sorted(issues.items()):
        print(f"\n❌ {filename}")
        for issue in issue_list:
            print(f"   - {issue}")
else:
    print("✓ No critical issues found!")

print()
print("=" * 70)
print("WARNINGS (Should Review)")
print("=" * 70)

if warnings:
    for filename, warning_list in sorted(warnings.items()):
        print(f"\n⚠️  {filename}")
        for warning in warning_list:
            print(f"   - {warning}")
else:
    print("✓ No warnings!")

print()
print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Total files checked: {len(html_files)}")
print(f"✓ Passed: {len(passed)}")
print(f"⚠ With warnings: {len(warnings)}")
print(f"❌ With issues: {len(issues)}")
print()

if len(issues) == 0:
    print("🎉 All pages verified - no critical display issues!")
else:
    print(f"⚠️  {len(issues)} files need fixes")
