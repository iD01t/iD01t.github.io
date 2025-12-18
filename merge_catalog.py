#!/usr/bin/env python3
"""
Merge eBooks and Audiobooks into unified catalog.json
"""

import json
from pathlib import Path

BASE_DIR = Path("/home/user/iD01t.github.io")

# Load current eBook catalog (array format)
with open(BASE_DIR / "data/catalog.json", "r", encoding="utf-8") as f:
    ebooks = json.load(f)

print(f"Loaded {len(ebooks)} eBooks")

# Load extracted audiobooks
with open(BASE_DIR / "audiobooks_extracted.json", "r", encoding="utf-8") as f:
    audiobook_data = json.load(f)
    audiobooks = audiobook_data["audiobooks"]

print(f"Loaded {len(audiobooks)} audiobooks")

# Create new unified catalog structure
unified_catalog = {
    "ebooks": ebooks,
    "audiobooks": audiobooks
}

# Backup old catalog
backup_file = BASE_DIR / "data/catalog.json.backup"
with open(backup_file, 'w', encoding='utf-8') as f:
    json.dump(ebooks, f, indent=2, ensure_ascii=False)

print(f"✓ Backed up old catalog to: {backup_file}")

# Write new unified catalog
catalog_file = BASE_DIR / "data/catalog.json"
with open(catalog_file, 'w', encoding='utf-8') as f:
    json.dump(unified_catalog, f, indent=2, ensure_ascii=False)

print(f"✓ Wrote unified catalog to: {catalog_file}")
print(f"\n📊 New catalog structure:")
print(f"  - eBooks: {len(ebooks)}")
print(f"  - Audiobooks: {len(audiobooks)}")
print(f"  - Total: {len(ebooks) + len(audiobooks)}")

# Verify the structure
with open(catalog_file, 'r', encoding='utf-8') as f:
    verify = json.load(f)

assert "ebooks" in verify, "Missing 'ebooks' key"
assert "audiobooks" in verify, "Missing 'audiobooks' key"
assert len(verify["ebooks"]) == len(ebooks), "eBooks count mismatch"
assert len(verify["audiobooks"]) == len(audiobooks), "Audiobooks count mismatch"

print(f"\n✅ Verification passed!")
print(f"\nSample entries:")
print(f"  eBook: {verify['ebooks'][0]['title'][:50]}...")
print(f"  Audiobook: {verify['audiobooks'][0]['title'][:50]}...")
