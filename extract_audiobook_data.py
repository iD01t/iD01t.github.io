#!/usr/bin/env python3
"""
Extract Audiobook Data from HTML Pages
Creates audiobook catalog entries based on existing eBook catalog
"""

import json
import re
from pathlib import Path

BASE_DIR = Path("/home/user/iD01t.github.io")

# Load eBook catalog
with open(BASE_DIR / "data/catalog.json", "r", encoding="utf-8") as f:
    ebook_catalog = json.load(f)

# Create lookup by title (normalized)
def normalize_title(title):
    """Normalize title for matching"""
    # Remove emojis and special chars, lowercase
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'\s+', ' ', title)
    return title.lower().strip()

ebook_by_title = {}
for item in ebook_catalog:
    key = normalize_title(item['title'])
    ebook_by_title[key] = item

print(f"Loaded {len(ebook_catalog)} eBooks from catalog")

# Get all audiobook HTML files
audiobook_dir = BASE_DIR / "audiobooks"
audiobook_files = sorted(audiobook_dir.glob("*.html"))

print(f"Found {len(audiobook_files)} audiobook HTML files")

audiobooks = []
matched = 0
unmatched = []

for filepath in audiobook_files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract title from <title> tag using regex
        title_match = re.search(r'<title>([^<]+)</title>', content)
        if not title_match:
            continue

        # Title format is usually "Book Title · iD01t Productions"
        full_title = title_match.group(1).strip()
        title = full_title.split('·')[0].strip() if '·' in full_title else full_title

        # Try to match with eBook catalog
        normalized = normalize_title(title)
        ebook_match = ebook_by_title.get(normalized)

        if ebook_match:
            # Create audiobook entry based on eBook data
            audiobook = {
                "id": ebook_match["id"],  # Same Google Books ID (they publish both formats)
                "title": ebook_match["title"],  # Use canonical title from eBook
                "subtitle": ebook_match.get("subtitle", ""),
                "format": "Audiobook",
                "contributors": ebook_match["contributors"],
                "publisher": ebook_match["publisher"],
                "language": ebook_match["language"],
                "date": ebook_match["date"],
                "cover_hd": ebook_match["cover_hd"],
                "buy": ebook_match["buy"],  # Google Play has both eBook and audiobook on same page
                "price": ebook_match.get("price", "9.99")
            }
            audiobooks.append(audiobook)
            matched += 1
        else:
            unmatched.append({
                "file": filepath.name,
                "title": title,
                "normalized": normalized
            })

    except Exception as e:
        print(f"  ✗ Error processing {filepath.name}: {e}")

print(f"\n📊 Results:")
print(f"  ✓ Matched: {matched} audiobooks")
print(f"  ⚠ Unmatched: {len(unmatched)} audiobooks")

if unmatched:
    print(f"\n⚠️  Unmatched audiobooks (first 10):")
    for item in unmatched[:10]:
        print(f"  - {item['title']} ({item['file']})")

# Save audiobook catalog
output = {
    "audiobooks": audiobooks,
    "stats": {
        "total": len(audiobooks),
        "matched": matched,
        "unmatched": len(unmatched)
    }
}

output_file = BASE_DIR / "audiobooks_extracted.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(audiobooks)} audiobook entries to: {output_file}")
print(f"\nSample audiobook entries:")
for ab in audiobooks[:3]:
    print(f"  - {ab['title']} (ID: {ab['id']})")
