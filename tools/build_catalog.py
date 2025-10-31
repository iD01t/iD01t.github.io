#!/usr/bin/env python3
"""
CSV to JSON converter for iD01t Productions catalog
Converts Google Play Books export CSV to flat JSON array
"""

import csv
import json
import sys
from pathlib import Path

def build_catalog():
    """Convert CSV to JSON format expected by the JavaScript app"""
    
    csv_path = Path('data/catalog.csv')
    json_path = Path('data/catalog.json')
    
    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        return False
    
    books = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Skip empty rows
                if not row.get('Title', '').strip():
                    continue

                # Determine format
                format_type = row.get('Format', 'eBook').strip()
                if format_type not in ['eBook', 'Audiobook']:
                    format_type = 'eBook'

                book = {
                    "id": row.get('Identifier', row.get('ID', '')).strip(),
                    "title": row.get('Title', '').strip(),
                    "subtitle": row.get('Subtitle', '').strip(),
                    "format": format_type,
                    "contributors": row.get('Primary Creator(s) / Contributors', row.get('Author', '')).strip(),
                    "publisher": row.get('Publisher / Label', row.get('Publisher', '')).strip(),
                    "language": row.get('Language', 'en').strip(),
                    "date": row.get('Release / Publish Date', row.get('Date', '')).strip(),
                    "cover_hd": row.get('HD Cover Image URL', '').strip(),
                    "buy": row.get('Google Play Buy Link', '').strip(),
                    "price": row.get('Price (if present)', row.get('Price', '')).strip()
                }

                # Only include books with valid IDs
                if book['id']:
                    books.append(book)
        
        # Write as flat array (not nested by format)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(books, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully converted {len(books)} books to {json_path}")
        return True

    except Exception as e:
        print(f"❌ Error processing CSV: {e}")
        return False

if __name__ == '__main__':
    success = build_catalog()
    sys.exit(0 if success else 1)
