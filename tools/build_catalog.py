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

def infer_language(title):
    # Simple heuristic to infer language from title
    if any(word in title.lower() for word in ['le', 'la', 'des', 'et', 'pour', 'que', 'qui', 'dans']):
        return 'fr'
    if any(word in title.lower() for word in ['der', 'die', 'das', 'und', 'für']):
        return 'de'
    if any(word in title.lower() for word in ['el', 'la', 'los', 'y', 'para', 'que', 'en']):
        return 'es'
    return 'en'

def assign_categories(title):
    categories = []
    title_lower = title.lower()
    if any(keyword in title_lower for keyword in ['python', 'java', 'c#', 'c++', 'javascript', 'html', 'css', 'code', 'programming']):
        categories.append('Programming')
    if any(keyword in title_lower for keyword in ['ai', 'machine learning', 'gpt']):
        categories.append('AI')
    if 'chess' in title_lower:
        categories.append('Games')
    if 'seo' in title_lower:
        categories.append('Marketing')
    if any(keyword in title_lower for keyword in ['dj', 'music', 'traktor', 'ableton', 'fl studio']):
        categories.append('Music')
    if 'quantum' in title_lower:
        categories.append('Science')
    if any(keyword in title_lower for keyword in ['sacred', 'god', 'jesus', 'spirituality', 'zen']):
        categories.append('Spirituality')
    if not categories:
        categories.append('General')
    return categories

def generate_description(title, categories):
    category_map = {
        "Programming": f"A comprehensive technical guide to mastering the concepts in '{title}'.",
        "AI": f"An in-depth exploration of the world of Artificial Intelligence and its applications, as discussed in '{title}'.",
        "Games": f"A strategic guide to mastering the game of chess, focusing on the techniques in '{title}'.",
        "Music": f"A creative guide for music producers and DJs, covering the methods in '{title}'.",
        "Science": f"A scientific exploration of the principles and theories presented in '{title}'.",
        "Spirituality": f"A journey into spiritual concepts and practices, as revealed in '{title}'.",
        "Marketing": f"A guide to modern marketing techniques, with a focus on the strategies in '{title}'.",
        "General": f"An insightful book that explores the topics presented in '{title}'."
    }
    # Return the first description that matches a category, or the general one.
    for cat in categories:
        if cat in category_map:
            return category_map[cat]
    return category_map["General"]

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
    
    catalog = {"ebooks": [], "audiobooks": []}
    
    try:
        with csv_path.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Extract and normalize fields
                title = normalize(row.get("Title") or row.get("title"))

                # Skip if title is 'nan' or empty
                if title.lower() == 'nan' or not title:
                    continue

                categories = assign_categories(title)
                description = generate_description(title, categories)
                language = infer_language(title)

                item = {
                    "id": normalize(
                        row.get("Identifier") or 
                        row.get("ID") or 
                        row.get("id") or 
                        row.get("Google Play Store Link ID")
                    ),
                    "title": title,
                    "subtitle": normalize(row.get("Subtitle") or row.get("subtitle") or ""),
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
                    "language": language,
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
                    ),
                    "description": description,
                    "categories": categories
                }
                
                # Validate required fields
                if not item["id"] or not item["title"]:
                    continue
                
                # Validate and sort format
                format_type = normalize(
                    row.get("Format") or
                    row.get("Book Format") or
                    row.get("format")
                )
                if format_type == "eBook":
                    item["pages"] = 250
                    catalog["ebooks"].append(item)
                elif format_type == "Audiobook":
                    item["duration"] = "5h 30m"
                    catalog["audiobooks"].append(item)
        
        # Write JSON output
        json_path.parent.mkdir(parents=True, exist_ok=True)
        
        with json_path.open('w', encoding='utf-8') as f:
            json.dump(catalog, f, ensure_ascii=False, indent=2)
        
        item_count = len(catalog["ebooks"]) + len(catalog["audiobooks"])
        print(f"✅ Successfully wrote {item_count} items to: {json_path}")
        
        # Statistics
        print(f"   📚 eBooks: {len(catalog['ebooks'])}")
        print(f"   🎧 Audiobooks: {len(catalog['audiobooks'])}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing CSV: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(build_catalog())
