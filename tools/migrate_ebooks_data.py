import json
import re

def slugify(text):
    """
    Convert a string to a URL-friendly slug.
    """
    if text is None:
        return ""
    # Remove unsupported characters from the title
    text = re.sub(r'[^\w\s-]', '', str(text).lower())
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'--+', '-', text)
    text = re.sub(r'^-+', '', text)
    text = re.sub(r'-+$', '', text)
    return text

def main():
    """
    Main function to migrate the ebook data.
    """
    with open("assets/catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)

    new_ebooks = []
    for ebook in catalog.get("ebooks", []):
        title = ebook.get("title", "Untitled")
        # Clean the title by removing the author and publisher
        title = re.sub(r'\s+by Guillaume Lessard.*$', '', title, flags=re.IGNORECASE)

        new_ebook = {
            "slug": slugify(title),
            "title": title,
            "subtitle": ebook.get("description", ""),
            "cover": ebook.get("image", ""),
            "price": ebook.get("price_cad", ""),
            "currency": "CAD" if ebook.get("price_cad") else "",
            "authors": ["Guillaume Lessard"],
            "description": ebook.get("description", ""),
            "language": ebook.get("lang", "en"),
            "isbn": "",
            "pages": ebook.get("pages", 0),
            "categories": ebook.get("tags", []),
            "buyLinks": {
                "GoogleBooks": ebook.get("url", "")
            },
            "tags": ebook.get("tags", []),
            "published": ebook.get("date", ""),
            "updated": ebook.get("date", "")
        }
        new_ebooks.append(new_ebook)

    with open("data/ebooks.json", "w", encoding="utf-8") as f:
        json.dump(new_ebooks, f, indent=2, ensure_ascii=False)

    print(f"Successfully migrated {len(new_ebooks)} ebooks.")

if __name__ == "__main__":
    main()
