#!/usr/bin/env python3
"""
Update catalog.csv to include audiobooks
"""

import json
import csv
from pathlib import Path

BASE_DIR = Path("/home/user/iD01t.github.io")

# Load JSON catalog
with open(BASE_DIR / "data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

ebooks = catalog["ebooks"]
audiobooks = catalog["audiobooks"]

print(f"Loaded {len(ebooks)} eBooks and {len(audiobooks)} audiobooks")

# Combine all items
all_items = ebooks + audiobooks

# Backup old CSV
csv_file = BASE_DIR / "data/catalog.csv"
backup_file = BASE_DIR / "data/catalog.csv.backup"

with open(csv_file, 'r', encoding='utf-8') as f:
    with open(backup_file, 'w', encoding='utf-8') as b:
        b.write(f.read())

print(f"✓ Backed up old CSV to: {backup_file}")

# Write new CSV with audiobooks
with open(csv_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)

    # Write header
    writer.writerow([
        'Identifier',
        'Title',
        'Subtitle',
        'Format',
        'Primary Creator(s) / Contributors',
        'Publisher / Label',
        'Language',
        'Release / Publish Date',
        'HD Cover Image URL',
        'Google Play Buy Link',
        'Price (if present)'
    ])

    # Write all items
    for item in all_items:
        writer.writerow([
            item.get('id', ''),
            item.get('title', ''),
            item.get('subtitle', ''),
            item.get('format', ''),
            item.get('contributors', ''),
            item.get('publisher', ''),
            item.get('language', ''),
            item.get('date', ''),
            item.get('cover_hd', ''),
            item.get('buy', ''),
            item.get('price', '')
        ])

print(f"✓ Wrote {len(all_items)} items to CSV")
print(f"  - eBooks: {len(ebooks)}")
print(f"  - Audiobooks: {len(audiobooks)}")
print(f"\n✅ CSV update complete!")
