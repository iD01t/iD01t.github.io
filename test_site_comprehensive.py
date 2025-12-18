#!/usr/bin/env python3
"""
Comprehensive website testing script
Tests all pages that depend on catalog.json
"""

import json
import os
import re
from pathlib import Path

def test_catalog_json():
    """Test catalog.json validity and structure"""
    print("=" * 60)
    print("TEST 1: Catalog JSON Validation")
    print("=" * 60)

    catalog_path = "data/catalog.json"

    # Check file exists
    if not os.path.exists(catalog_path):
        print(f"❌ FAIL: {catalog_path} does not exist")
        return False

    # Check file size (should be ~158KB, not 236KB)
    file_size = os.path.getsize(catalog_path)
    print(f"   File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")

    if file_size > 200000:  # > 200KB indicates corruption
        print(f"   ⚠️  WARNING: File size too large (expected ~158KB)")
        return False

    # Validate JSON structure
    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ FAIL: Invalid JSON - {e}")
        return False

    # Check structure
    if not isinstance(data, dict):
        print(f"❌ FAIL: Root should be object, got {type(data)}")
        return False

    if 'ebooks' not in data or 'audiobooks' not in data:
        print(f"❌ FAIL: Missing 'ebooks' or 'audiobooks' keys")
        print(f"   Found keys: {list(data.keys())}")
        return False

    ebook_count = len(data['ebooks'])
    audiobook_count = len(data['audiobooks'])
    total = ebook_count + audiobook_count

    print(f"   ✓ Valid JSON structure")
    print(f"   ✓ eBooks: {ebook_count}")
    print(f"   ✓ Audiobooks: {audiobook_count}")
    print(f"   ✓ Total items: {total}")

    # Verify first item structure
    if ebook_count > 0:
        first_ebook = data['ebooks'][0]
        required_fields = ['id', 'title', 'format', 'buy']
        missing = [f for f in required_fields if f not in first_ebook]
        if missing:
            print(f"   ⚠️  Missing fields in eBook items: {missing}")
        else:
            print(f"   ✓ eBook items have required fields")

    if audiobook_count > 0:
        first_audiobook = data['audiobooks'][0]
        if 'format' in first_audiobook and first_audiobook['format'] == 'Audiobook':
            print(f"   ✓ Audiobook format correctly set")
        else:
            print(f"   ⚠️  Audiobook format field incorrect")

    print("✅ PASS: Catalog JSON is valid\n")
    return True


def test_page_catalog_references():
    """Test that all pages correctly reference /data/catalog.json"""
    print("=" * 60)
    print("TEST 2: Page Catalog References")
    print("=" * 60)

    pages_to_check = {
        'ebooks.html': ['/data/catalog.json'],
        'audiobooks.html': ['/data/catalog.json'],
        'search.html': ['/data/catalog.json'],
        'ebook.html': ['/data/catalog.json'],
    }

    all_pass = True

    for page, expected_paths in pages_to_check.items():
        if not os.path.exists(page):
            print(f"   ⚠️  {page} not found")
            continue

        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all catalog.json references
        catalog_refs = re.findall(r'["\']([^"\']*catalog\.json[^"\']*)["\']', content)

        print(f"\n   {page}:")

        # Check for wrong paths
        wrong_paths = [ref for ref in catalog_refs if '/assets/catalog.json' in ref]
        if wrong_paths:
            print(f"      ❌ Found old path: {wrong_paths}")
            all_pass = False

        # Check for correct paths
        correct_paths = [ref for ref in catalog_refs if '/data/catalog.json' in ref]
        if correct_paths:
            print(f"      ✓ Uses correct path: /data/catalog.json ({len(correct_paths)} references)")
        else:
            print(f"      ❌ No references to /data/catalog.json found")
            all_pass = False

    if all_pass:
        print("\n✅ PASS: All pages use correct catalog path\n")
    else:
        print("\n❌ FAIL: Some pages have incorrect paths\n")

    return all_pass


def test_catalog_loading_code():
    """Test that pages correctly handle the new catalog structure"""
    print("=" * 60)
    print("TEST 3: Catalog Loading Code Structure")
    print("=" * 60)

    pages_to_check = {
        'ebooks.html': 'data.ebooks',
        'audiobooks.html': 'data.audiobooks',
        'search.html': 'data.ebooks',  # search.html accesses both
        'ebook.html': 'data.ebooks',
    }

    all_pass = True

    for page, expected_access in pages_to_check.items():
        if not os.path.exists(page):
            continue

        with open(page, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"\n   {page}:")

        # Check if it accesses data.ebooks or data.audiobooks
        if 'data.ebooks' in content or 'data["ebooks"]' in content or "data['ebooks']" in content:
            print(f"      ✓ Accesses data.ebooks")
        elif 'ebooks.html' in page or 'ebook.html' in page:
            print(f"      ❌ Does not access data.ebooks")
            all_pass = False

        if 'data.audiobooks' in content or 'data["audiobooks"]' in content or "data['audiobooks']" in content:
            print(f"      ✓ Accesses data.audiobooks")
        elif 'audiobooks.html' in page:
            print(f"      ❌ Does not access data.audiobooks")
            all_pass = False

    if all_pass:
        print("\n✅ PASS: All pages correctly access new catalog structure\n")
    else:
        print("\n❌ FAIL: Some pages don't use new structure\n")

    return all_pass


def test_html_structure():
    """Basic HTML structure validation"""
    print("=" * 60)
    print("TEST 4: HTML Structure Validation")
    print("=" * 60)

    html_files = list(Path('.').glob('*.html'))
    issues_found = []

    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for basic structure
        has_doctype = '<!DOCTYPE html>' in content
        has_html = '<html' in content
        has_head = '<head' in content
        has_body = '<body' in content
        has_title = '<title>' in content

        if not all([has_doctype, has_html, has_head, has_body, has_title]):
            issues_found.append(f"{html_file.name}: Missing basic HTML elements")

    if issues_found:
        print("   ❌ Issues found:")
        for issue in issues_found:
            print(f"      - {issue}")
        print()
        return False
    else:
        print(f"   ✓ All {len(html_files)} HTML files have valid structure")
        print("✅ PASS: HTML structure validation\n")
        return True


def main():
    """Run all tests"""
    print("\n🔍 COMPREHENSIVE WEBSITE TEST SUITE")
    print("Testing catalog.json and page functionality\n")

    results = []

    # Run all tests
    results.append(("Catalog JSON Validation", test_catalog_json()))
    results.append(("Page Catalog References", test_page_catalog_references()))
    results.append(("Catalog Loading Code", test_catalog_loading_code()))
    results.append(("HTML Structure", test_html_structure()))

    # Print summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")

    print(f"\n   Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Site is ready for deployment.")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED. Please review and fix issues above.")
        return 1


if __name__ == "__main__":
    exit(main())
