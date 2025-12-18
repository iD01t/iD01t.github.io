#!/usr/bin/env python3
"""
Fix Landing Page Google Books Links
Replace incorrect GGKEY IDs with correct Google Books IDs from catalog.json
"""

import json
import re
from pathlib import Path
from urllib.parse import unquote

# Base directory
BASE_DIR = Path("/home/user/iD01t.github.io")

# Load catalog data
with open(BASE_DIR / "data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Create lookup maps by title (normalized)
def normalize_title(title):
    """Normalize title for matching"""
    return title.lower().strip()

catalog_by_title = {}
for item in catalog:
    key = normalize_title(item['title'])
    catalog_by_title[key] = item

# Also create lookup by filename (slug)
def title_to_slug(title):
    """Convert title to URL slug"""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars
    slug = re.sub(r'[-\s]+', '-', slug)    # Replace spaces/hyphens with single hyphen
    return slug.strip('-')

catalog_by_slug = {}
for item in catalog:
    slug = title_to_slug(item['title'])
    catalog_by_slug[slug] = item

def extract_filename_slug(filepath):
    """Extract slug from filepath"""
    return filepath.stem  # filename without extension

def fix_landing_page(filepath):
    """Fix Google Books links in a landing page"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Extract filename slug
        slug = extract_filename_slug(filepath)

        # Try to find matching book in catalog
        book = catalog_by_slug.get(slug)

        if not book:
            # Try alternate lookup by extracting title from HTML
            title_match = re.search(r'<title>([^—|]+)', content)
            if title_match:
                page_title = normalize_title(title_match.group(1).strip())
                book = catalog_by_title.get(page_title)

        if not book:
            print(f"  ⚠️  No matching book found for: {filepath.name}")
            return False

        # Get correct ID and URL
        correct_id = book['id']
        correct_url = book['buy']

        # Find current GGKEY ID
        ggkey_match = re.search(r'GGKEY:[A-Z0-9]+', content)
        if not ggkey_match:
            print(f"  ℹ️  No GGKEY found in: {filepath.name}")
            return False

        old_ggkey = ggkey_match.group(0)
        old_url = f"https://play.google.com/store/books/details?id={old_ggkey}"

        # Replace all occurrences of the old URL with correct URL
        content = content.replace(old_url, correct_url)

        # Verify changes were made
        if content == original_content:
            print(f"  ℹ️  No changes needed for: {filepath.name}")
            return False

        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  ✓ Fixed {filepath.name}")
        print(f"    {old_ggkey} → {correct_id}")
        return True

    except Exception as e:
        print(f"  ✗ Error fixing {filepath}: {e}")
        return False

def main():
    """Fix all landing pages"""
    print("=" * 70)
    print("Fixing Landing Page Google Books Links")
    print("=" * 70)

    landing_pages = []

    # Collect all landing pages
    ebook_dir = BASE_DIR / "landing_pages_new/ebooks"
    audiobook_dir = BASE_DIR / "landing_pages_new/audiobooks"

    if ebook_dir.exists():
        landing_pages.extend(ebook_dir.glob("*.html"))
    if audiobook_dir.exists():
        landing_pages.extend(audiobook_dir.glob("*.html"))

    print(f"\nFound {len(landing_pages)} landing pages to check\n")

    fixed_count = 0
    for filepath in sorted(landing_pages):
        if fix_landing_page(filepath):
            fixed_count += 1

    print("\n" + "=" * 70)
    print(f"✅ Fixed {fixed_count} landing pages")
    print("=" * 70)

if __name__ == "__main__":
    main()
