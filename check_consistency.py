#!/usr/bin/env python3
"""
Check and report header/footer consistency across all HTML pages
"""

import os
import re
from pathlib import Path

def check_page_structure(filepath):
    """Check if a page has proper header and footer structure"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = {
        'has_nav': '<nav' in content and 'iD01t Productions' in content,
        'has_footer': '<footer' in content,
        'has_mobile_menu': 'mobileMenu' in content,
        'has_theme_toggle': 'themeToggle' in content,
        'has_contact_button': 'Contact</a>' in content and 'contact.html' in content,
        'has_logo': '/assets/img/brand/logo.svg' in content,
        'nav_links': {
            'store': '/store.html' in content,
            'ebooks': '/ebooks.html' in content,
            'audiobooks': '/audiobooks.html' in content,
            'apps': '/apps.html' in content,
            'games': '/games.html' in content,
            'music': '/music.html' in content,
            'blog': '/blog.html' in content,
            'nini': '/nini.html' in content,
        }
    }

    return results

def main():
    print("=" * 80)
    print("HEADER/FOOTER CONSISTENCY CHECK")
    print("=" * 80)
    print()

    # Get all main HTML files (excluding subdirectories)
    html_files = [f for f in Path('.').glob('*.html') if f.is_file()]

    print(f"Found {len(html_files)} HTML files in root directory\n")

    issues = []

    for html_file in sorted(html_files):
        results = check_page_structure(html_file)

        print(f"📄 {html_file.name}")

        # Check critical elements
        if not results['has_nav']:
            print(f"   ❌ Missing navigation with iD01t Productions branding")
            issues.append((html_file.name, "Missing navigation"))
        else:
            print(f"   ✅ Has navigation")

        if not results['has_footer']:
            print(f"   ❌ Missing footer")
            issues.append((html_file.name, "Missing footer"))
        else:
            print(f"   ✅ Has footer")

        if not results['has_logo']:
            print(f"   ⚠️  Missing logo.svg reference")

        if not results['has_theme_toggle']:
            print(f"   ⚠️  Missing theme toggle")

        # Check navigation completeness
        missing_links = [link for link, exists in results['nav_links'].items() if not exists]
        if missing_links:
            print(f"   ⚠️  Missing nav links: {', '.join(missing_links)}")

        print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    if issues:
        print(f"\n❌ Found {len(issues)} issues:\n")
        for filename, issue in issues:
            print(f"   - {filename}: {issue}")
    else:
        print("\n✅ All pages have consistent navigation and footer structure!")

    return 0 if not issues else 1

if __name__ == "__main__":
    exit(main())
