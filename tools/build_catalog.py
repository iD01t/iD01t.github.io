#!/usr/bin/env python3
"""
Build catalog.json from Google Play CSV export
Converts iD01t Productions catalog CSV to JSON for web consumption
"""

import csv
import json
import pathlib
import sys
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / 'data' / 'catalog.csv'
JSON_PATH = ROOT / 'data' / 'catalog.json'

def normalize(s):
    """Normalize string field"""
    return (s or '').strip()

def parse_price(s):
    """Extract price from string"""
    if not s:
        return ""
    s = str(s).strip().replace('$', '').replace(',', '')
    try:
        return f"{float(s):.2f}"
    except ValueError:
        return ""

def build_cover_url(book_id):
    """Build HD cover URL from book ID"""
    if not book_id:
        return ""
    # Google Books API uses zoom parameter for resolution
    # zoom=1 (small), zoom=2 (medium), zoom=3 (large)
    return f"https://books.google.com/books/content?id={book_id}&printsec=frontcover&img=1&zoom=3"

def build_buy_url(book_id, book_format):
    """Build Google Play purchase URL"""
    if not book_id:
        return ""
    
    if book_format == 'Audiobook':
        return f"https://play.google.com/store/audiobooks/details?id={book_id}"
    else:
        return f"https://play.google.com/store/books/details?id={book_id}"

def parse_date(date_str):
    """Parse and normalize date"""
    if not date_str:
        return ""
    
    date_str = normalize(date_str)
    
    # Try common formats
    for fmt in ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y/%m/%d', '%b %d, %Y']:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue
    
    # If just year
    if date_str.isdigit() and len(date_str) == 4:
        return f"{date_str}-01-01"
    
    return date_str

def main():
    """Main build function"""
    if not CSV_PATH.exists():
        print(f"❌ Error: CSV file not found at {CSV_PATH}")
        print(f"   Please place your Google Play export CSV at: data/catalog.csv")
        sys.exit(1)
    
    print(f"📖 Reading catalog from: {CSV_PATH}")
    
    catalog = []
    skipped = 0
    
    with CSV_PATH.open('r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        
        # Detect column names (CSV exports may vary)
        fieldnames = reader.fieldnames
        print(f"   Detected columns: {', '.join(fieldnames[:5])}...")
        
        for row_num, row in enumerate(reader, start=2):
            # Extract fields with fallbacks for different CSV formats
            book_id = normalize(
                row.get('Identifier') or 
                row.get('ID') or 
                row.get('id') or
                row.get('Book ID')
            )
            
            title = normalize(
                row.get('Title') or 
                row.get('title') or
                row.get('Book Title')
            )
            
            book_format = normalize(
                row.get('Format') or 
                row.get('Book Format') or
                row.get('format') or
                row.get('Type')
            )
            
            # Skip invalid rows
            if not book_id or not title:
                skipped += 1
                continue
            
            # Normalize format
            if 'audio' in book_format.lower():
                book_format = 'Audiobook'
            elif 'ebook' in book_format.lower() or 'book' in book_format.lower():
                book_format = 'eBook'
            
            # Only include eBooks and Audiobooks
            if book_format not in ('eBook', 'Audiobook'):
                skipped += 1
                continue
            
            # Build catalog entry
            entry = {
                'id': book_id,
                'title': title,
                'subtitle': normalize(row.get('Subtitle') or row.get('subtitle') or ''),
                'format': book_format,
                'contributors': normalize(
                    row.get('Primary Creator(s) / Contributors') or
                    row.get('Contributor [Role], Semicolon-Separated') or
                    row.get('Author') or
                    row.get('Narrator') or
                    row.get('Contributors') or
                    ''
                ),
                'publisher': normalize(
                    row.get('Publisher / Label') or
                    row.get('Publisher') or
                    'iD01t Productions'
                ),
                'language': normalize(
                    row.get('Language') or
                    row.get('language') or
                    'English'
                ),
                'date': parse_date(
                    row.get('Release / Publish Date') or
                    row.get('On Sale Date') or
                    row.get('Published Date') or
                    row.get('Date') or
                    ''
                ),
                'cover_hd': normalize(
                    row.get('HD Cover Image URL') or
                    row.get('Cover URL') or
                    build_cover_url(book_id)
                ),
                'buy': normalize(
                    row.get('Google Play Buy Link') or
                    row.get('Buy Link') or
                    row.get('URL') or
                    build_buy_url(book_id, book_format)
                ),
                'price': parse_price(
                    row.get('Price (if present)') or
                    row.get('Price') or
                    row.get('List Price') or
                    ''
                )
            }
            
            catalog.append(entry)
    
    if not catalog:
        print(f"❌ Error: No valid entries found in CSV")
        sys.exit(1)
    
    # Sort by date (newest first), then title
    catalog.sort(key=lambda x: (x['date'] or '0000-00-00', x['title']), reverse=True)
    
    # Write JSON
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    with JSON_PATH.open('w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Successfully processed {len(catalog)} items")
    if skipped:
        print(f"   ⚠️  Skipped {skipped} invalid/unsupported rows")
    print(f"📝 Wrote catalog to: {JSON_PATH}")
    
    # Print statistics
    formats = {}
    languages = {}
    for item in catalog:
        formats[item['format']] = formats.get(item['format'], 0) + 1
        lang = item['language'] or 'Unknown'
        languages[lang] = languages.get(lang, 0) + 1
    
    print(f"\n📊 Catalog Statistics:")
    print(f"   Formats:")
    for fmt, count in sorted(formats.items()):
        print(f"     • {fmt}: {count}")
    print(f"   Languages:")
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"     • {lang}: {count}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
