#!/usr/bin/env python3
"""
Live site verification - tests actual production deployment
"""

import requests
import json
import sys

SITE_URL = "https://id01t.store"

def test_catalog():
    """Test catalog.json loads and is valid"""
    print("=" * 60)
    print("TEST 1: Live Catalog JSON")
    print("=" * 60)

    try:
        response = requests.get(f"{SITE_URL}/data/catalog.json", timeout=10)
        print(f"   HTTP Status: {response.status_code}")

        if response.status_code != 200:
            print(f"   ❌ FAIL: Got status {response.status_code}")
            return False

        data = response.json()

        if not isinstance(data, dict):
            print(f"   ❌ FAIL: Expected object, got {type(data)}")
            return False

        if 'ebooks' not in data or 'audiobooks' not in data:
            print(f"   ❌ FAIL: Missing ebooks or audiobooks keys")
            return False

        ebook_count = len(data['ebooks'])
        audiobook_count = len(data['audiobooks'])

        print(f"   ✅ Valid JSON structure")
        print(f"   ✅ {ebook_count} eBooks")
        print(f"   ✅ {audiobook_count} audiobooks")
        print(f"   ✅ Total: {ebook_count + audiobook_count} items")
        print("✅ PASS\n")
        return True

    except Exception as e:
        print(f"   ❌ FAIL: {e}\n")
        return False


def test_pages():
    """Test all main pages load successfully"""
    print("=" * 60)
    print("TEST 2: Live Pages Loading")
    print("=" * 60)

    pages = [
        'index.html',
        'ebooks.html',
        'audiobooks.html',
        'search.html',
    ]

    all_pass = True

    for page in pages:
        try:
            response = requests.get(f"{SITE_URL}/{page}", timeout=10)
            status = response.status_code

            if status == 200:
                # Check if page has content
                if len(response.text) > 1000:
                    print(f"   ✅ {page}: OK ({len(response.text):,} bytes)")
                else:
                    print(f"   ⚠️  {page}: OK but small ({len(response.text)} bytes)")
            else:
                print(f"   ❌ {page}: HTTP {status}")
                all_pass = False

        except Exception as e:
            print(f"   ❌ {page}: {e}")
            all_pass = False

    if all_pass:
        print("✅ PASS\n")
    else:
        print("❌ FAIL\n")

    return all_pass


def test_catalog_in_pages():
    """Test pages actually load catalog data"""
    print("=" * 60)
    print("TEST 3: Pages Use Catalog")
    print("=" * 60)

    pages = {
        'ebooks.html': '/data/catalog.json',
        'audiobooks.html': '/data/catalog.json',
        'search.html': '/data/catalog.json',
    }

    all_pass = True

    for page, expected_path in pages.items():
        try:
            response = requests.get(f"{SITE_URL}/{page}", timeout=10)
            content = response.text

            if expected_path in content:
                print(f"   ✅ {page}: References {expected_path}")
            else:
                print(f"   ❌ {page}: Does not reference {expected_path}")
                all_pass = False

        except Exception as e:
            print(f"   ❌ {page}: {e}")
            all_pass = False

    if all_pass:
        print("✅ PASS\n")
    else:
        print("❌ FAIL\n")

    return all_pass


def main():
    print("\n🌐 LIVE SITE VERIFICATION")
    print(f"Testing: {SITE_URL}\n")

    results = []
    results.append(("Catalog JSON", test_catalog()))
    results.append(("Pages Loading", test_pages()))
    results.append(("Pages Use Catalog", test_catalog_in_pages()))

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")

    print(f"\n   Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Website is working perfectly.")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED.")
        return 1


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        exit(1)
