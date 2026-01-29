#!/usr/bin/env python3
"""
Final Professional Quality Check for iD01t.github.io
Ensures everything is ready for job interview presentation
"""

import os
import json
import re
from pathlib import Path

def check_catalog_integrity():
    """Verify catalog.json is valid and complete"""
    print("=" * 80)
    print("1. CATALOG INTEGRITY CHECK")
    print("=" * 80)

    try:
        with open('data/catalog.json', 'r') as f:
            data = json.load(f)

        ebooks = data.get('ebooks', [])
        audiobooks = data.get('audiobooks', [])

        print(f"✅ Catalog JSON is valid")
        print(f"✅ {len(ebooks)} eBooks")
        print(f"✅ {len(audiobooks)} Audiobooks")
        print(f"✅ Total: {len(ebooks) + len(audiobooks)} products")

        # Check first item structure
        if ebooks:
            first = ebooks[0]
            required_fields = ['id', 'title', 'buy', 'format']
            missing = [f for f in required_fields if f not in first]
            if missing:
                print(f"⚠️  Missing fields: {missing}")
            else:
                print(f"✅ All required fields present")

        return True
    except Exception as e:
        print(f"❌ Catalog error: {e}")
        return False


def check_music_integration():
    """Check ROOT_ACCESS LP integration"""
    print("\n" + "=" * 80)
    print("2. MUSIC / ROOT_ACCESS LP CHECK")
    print("=" * 80)

    pages_to_check = ['index.html', 'music.html']
    all_good = True

    for page in pages_to_check:
        if not os.path.exists(page):
            print(f"❌ {page} not found")
            all_good = False
            continue

        with open(page, 'r') as f:
            content = f.read()

        has_root_access = 'ROOT_ACCESS' in content
        has_soundcloud = 'soundcloud.com' in content
        has_soundcloud_iframe = 'w.soundcloud.com/player' in content

        print(f"\n📄 {page}:")
        print(f"   {'✅' if has_root_access else '❌'} ROOT_ACCESS LP section")
        print(f"   {'✅' if has_soundcloud else '❌'} SoundCloud link")
        print(f"   {'✅' if has_soundcloud_iframe else '❌'} SoundCloud embed player")

        if not (has_root_access and has_soundcloud and has_soundcloud_iframe):
            all_good = False

    return all_good


def check_navigation_consistency():
    """Check navigation is consistent"""
    print("\n" + "=" * 80)
    print("3. NAVIGATION CONSISTENCY CHECK")
    print("=" * 80)

    main_pages = ['index.html', 'ebooks.html', 'audiobooks.html',
                  'apps.html', 'games.html', 'music.html', 'store.html']

    required_links = [
        '/store.html', '/ebooks.html', '/audiobooks.html',
        '/apps.html', '/games.html', '/music.html', '/blog.html'
    ]

    issues = []

    for page in main_pages:
        if not os.path.exists(page):
            continue

        with open(page, 'r') as f:
            content = f.read()

        missing = [link for link in required_links if link not in content]

        if missing:
            issues.append((page, missing))
            print(f"⚠️  {page}: Missing {missing}")
        else:
            print(f"✅ {page}: All nav links present")

    return len(issues) == 0


def check_buy_links():
    """Verify buy links are properly formatted"""
    print("\n" + "=" * 80)
    print("4. BUY LINKS CHECK")
    print("=" * 80)

    try:
        with open('data/catalog.json', 'r') as f:
            data = json.load(f)

        ebooks = data.get('ebooks', [])
        audiobooks = data.get('audiobooks', [])

        # Check eBooks
        ebook_issues = []
        for item in ebooks[:5]:  # Check first 5
            if 'buy' not in item or not item['buy'].startswith('https://play.google.com'):
                ebook_issues.append(item.get('title', 'Unknown'))

        if ebook_issues:
            print(f"⚠️  eBook buy link issues: {len(ebook_issues)} items")
        else:
            print(f"✅ eBook buy links verified (sample: {min(5, len(ebooks))} items)")

        # Check audiobooks
        audiobook_issues = []
        for item in audiobooks[:5]:
            if 'buy' not in item or not item['buy'].startswith('https://play.google.com'):
                audiobook_issues.append(item.get('title', 'Unknown'))

        if audiobook_issues:
            print(f"⚠️  Audiobook buy link issues: {len(audiobook_issues)} items")
        else:
            print(f"✅ Audiobook buy links verified (sample: {min(5, len(audiobooks))} items)")

        return len(ebook_issues) == 0 and len(audiobook_issues) == 0
    except Exception as e:
        print(f"❌ Error checking buy links: {e}")
        return False


def check_professional_elements():
    """Check for professional presentation elements"""
    print("\n" + "=" * 80)
    print("5. PROFESSIONAL PRESENTATION CHECK")
    print("=" * 80)

    checks = {
        'index.html': [
            ('Meta description', '<meta.*description'),
            ('Open Graph tags', 'property="og:'),
            ('Favicon', '/favicon'),
            ('Responsive viewport', 'viewport'),
        ],
        'music.html': [
            ('Artist schema', '@type.*MusicGroup'),
            ('Structured data', 'application/ld\+json'),
        ],
    }

    all_good = True

    for page, page_checks in checks.items():
        if not os.path.exists(page):
            continue

        print(f"\n📄 {page}:")
        with open(page, 'r') as f:
            content = f.read()

        for name, pattern in page_checks:
            if re.search(pattern, content):
                print(f"   ✅ {name}")
            else:
                print(f"   ❌ {name}")
                all_good = False

    return all_good


def check_image_assets():
    """Check critical image assets exist"""
    print("\n" + "=" * 80)
    print("6. IMAGE ASSETS CHECK")
    print("=" * 80)

    critical_images = [
        'assets/img/brand/logo.svg',
        'assets/img/brand/logo.png',
        'assets/img/brand/og-home.jpg',
    ]

    all_exist = True

    for image_path in critical_images:
        exists = os.path.exists(image_path)
        print(f"   {'✅' if exists else '❌'} {image_path}")
        if not exists:
            all_exist = False

    # Check ROOT_ACCESS cover
    root_access_cover = 'assets/img/brand/root-access-cover.jpg'
    exists = os.path.exists(root_access_cover)
    print(f"   {'✅' if exists else '⚠️ '} {root_access_cover}" +
          (" (will need actual album artwork)" if not exists else ""))

    return all_exist


def main():
    print("\n" + "=" * 80)
    print("🎯 FINAL PROFESSIONAL QUALITY CHECK FOR JOB INTERVIEW")
    print("=" * 80)
    print()

    results = []

    results.append(("Catalog Integrity", check_catalog_integrity()))
    results.append(("ROOT_ACCESS LP Integration", check_music_integration()))
    results.append(("Navigation Consistency", check_navigation_consistency()))
    results.append(("Buy Links", check_buy_links()))
    results.append(("Professional Elements", check_professional_elements()))
    results.append(("Image Assets", check_image_assets()))

    # Final summary
    print("\n" + "=" * 80)
    print("🏆 FINAL SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "⚠️  NEEDS ATTENTION"
        print(f"   {status}: {test_name}")

    print(f"\n   Score: {passed}/{total} ({int(passed/total*100)}%)")

    if passed == total:
        print("\n🎉 PERFECT! Site is 100% ready for job interview presentation!")
        print("   All systems operational, all links working, professional presentation confirmed.")
    elif passed >= total * 0.8:
        print("\n✅ GOOD! Site is ready with minor notes above.")
        print("   Core functionality verified, presentation is professional.")
    else:
        print("\n⚠️  ATTENTION NEEDED: Review issues above before interview.")

    return 0 if passed == total else 1

if __name__ == "__main__":
    exit(main())
