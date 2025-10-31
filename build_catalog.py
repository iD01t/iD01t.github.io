#!/usr/bin/env python3
"""
Build catalog JSON from CSV export
Converts data/catalog.csv → data/catalog.json
"""

import csv
import json
import pathlib
import sys

def normalize(s):
    """Normalize string value"""
    return (s or '').strip()

def build_catalog():
    """Read CSV and generate JSON catalog"""
    # Paths
    root = pathlib.Path(__file__).resolve().parents[1]
    csv_path = root / 'data' / 'catalog.csv'
    json_path = root / 'data' / 'catalog.json'
    
    if not csv_path.exists():
        print(f"❌ CSV file not found: {csv_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"📖 Reading catalog from: {csv_path}")
    
    catalog = []
    
    try:
        with csv_path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Extract and normalize fields
                # Support multiple possible column names from different exports
                item = {
                    "id": normalize(
                        row.get("Identifier") or 
                        row.get("ID") or 
                        row.get("id") or 
                        row.get("Google Play Store Link ID")
                    ),
                    "title": normalize(row.get("Title") or row.get("title")),
                    "subtitle": normalize(row.get("Subtitle") or row.get("subtitle") or ""),
                    "format": normalize(
                        row.get("Format") or 
                        row.get("Book Format") or 
                        row.get("format")
                    ),
                    "contributors": normalize(
                        row.get("Primary Creator(s) / Contributors") or
                        row.get("Contributor [Role], Semicolon-Separated") or
                        row.get("Contributors") or
                        row.get("Author")
                    ),
                    "publisher": normalize(
                        row.get("Publisher / Label") or 
                        row.get("Publisher") or 
                        row.get("publisher")
                    ),
                    "language": normalize(
                        row.get("Language") or 
                        row.get("language")
                    ),
                    "date": normalize(
                        row.get("Release / Publish Date") or 
                        row.get("On Sale Date") or
                        row.get("Date") or
                        row.get("date")
                    ),
                    "cover_hd": normalize(
                        row.get("HD Cover Image URL") or
                        row.get("Cover Image URL") or
                        row.get("cover")
                    ),
                    "buy": normalize(
                        row.get("Google Play Buy Link") or
                        row.get("Play Store Link (Do Not Modify)") or
                        row.get("Buy Link") or
                        row.get("URL")
                    ),
                    "price": normalize(
                        row.get("Price (if present)") or 
                        row.get("Price") or 
                        row.get("price") or
                        ""
                    )
                }
                
                # Validate required fields
                if not item["id"] or not item["title"]:
                    continue
                
                # Validate format
                if item["format"] not in ("eBook", "Audiobook"):
                    continue
                
                catalog.append(item)
        
        # Write JSON output
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with json_path.open('w', encoding='utf-8') as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Successfully wrote {len(catalog)} items to: {json_path}")
        
        # Statistics
        ebooks = sum(1 for item in catalog if item["format"] == "eBook")
        audiobooks = sum(1 for item in catalog if item["format"] == "Audiobook")
        print(f"   📚 eBooks: {ebooks}")
        print(f"   🎧 Audiobooks: {audiobooks}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing CSV: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(build_catalog())
