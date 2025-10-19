import csv
import json
import re

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

def create_catalog_json():
    ebooks = []
    audiobooks = []

    try:
        with open('data/catalog.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip rows with no ID
                if not row.get("Identifier"):
                    continue

                title = row.get("Title", "No Title Provided")

                # Skip if title is 'nan' or empty
                if title.lower() == 'nan' or not title:
                    continue

                categories = assign_categories(title)
                description = generate_description(title, categories)
                language = infer_language(title)

                # If language in CSV is not 'en', use that instead.
                csv_lang = row.get("Language")
                if csv_lang and csv_lang.lower() != 'en':
                    language = csv_lang.lower()

                item = {
                    "id": row["Identifier"],
                    "title": title,
                    "subtitle": row.get("Subtitle", ""),
                    "contributors": row.get("Primary Creator(s) / Contributors", "Unknown Author"),
                    "publisher": row.get("Publisher / Label", "iD01t Productions"),
                    "language": language,
                    "date": row.get("Release / Publish Date", "2024-01-01"),
                    "cover_hd": row.get("HD Cover Image URL", ""),
                    "buy": row.get("Google Play Buy Link", ""),
                    "price": row.get("Price (if present)", "9.99"),
                    "description": description,
                    "categories": categories
                }

                if row.get("Format") == "eBook":
                    item["pages"] = 250  # Placeholder, as pages are not in the CSV
                    ebooks.append(item)
                elif row.get("Format") == "Audiobook":
                    item["duration"] = "5h 30m"  # Placeholder
                    audiobooks.append(item)

    except FileNotFoundError:
        print("Error: 'data/catalog.csv' not found.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    with open('data/catalog.json', 'w', encoding='utf-8') as f:
        json.dump({"ebooks": ebooks, "audiobooks": audiobooks}, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    create_catalog_json()
    print("catalog.json created successfully.")
