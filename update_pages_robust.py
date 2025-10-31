import json
import os
import re
import unicodedata

def to_url_safe(s):
    """
    Converts a string to a URL-safe format. This function is critical for matching
    catalog titles to filenames.
    """
    # Normalize Unicode characters to their base form (e.g., 'é' -> 'e')
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    # Remove any characters that are not alphanumeric, spaces, or hyphens
    s = re.sub(r'[^\w\s-]', '', s)
    # Replace one or more spaces or hyphens with a single hyphen
    s = re.sub(r'[\s-]+', '-', s)
    # Remove leading/trailing hyphens
    s = s.strip('-')
    return s

def update_landing_pages(catalog_path):
    """
    Updates all landing pages by matching them to the catalog entries
    using a normalized, URL-safe key.
    """
    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Cannot read or parse catalog file at {catalog_path}. {e}")
        return

    # Create a lookup table from the catalog with normalized titles as keys
    catalog_lookup = {}
    for book_type in ['ebooks', 'audiobooks']:
        for book in catalog.get(book_type, []):
            title = book.get('title', '').strip()
            if title:
                safe_key = to_url_safe(title)
                if safe_key:
                    catalog_lookup[safe_key] = {
                        'image': book.get('image', ''),
                        'link': book.get('link', ''),
                        'type': book_type
                    }

    # Iterate through the directories and update files
    for book_type in ['ebooks', 'audiobooks']:
        print(f"\nProcessing directory: {book_type}/")
        if not os.path.isdir(book_type):
            print(f"Directory not found: {book_type}/")
            continue

        for filename in os.listdir(book_type):
            if filename.endswith('.html'):
                file_path = os.path.join(book_type, filename)
                # Create a safe key from the filename to match with the catalog
                file_key = to_url_safe(os.path.splitext(filename)[0])

                if file_key in catalog_lookup:
                    book_data = catalog_lookup[file_key]
                    new_image_url = book_data.get('image')
                    new_buy_url = book_data.get('link')

                    if not new_image_url or not new_buy_url:
                        print(f"Skipping {file_path}: Missing image or buy URL in catalog.")
                        continue

                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Use more specific regex to avoid accidental replacements
                        # Regex for the main cover image
                        content, img_subs = re.subn(
                            r'(<img[^>]+id="coverImage"[^>]+src=")[^"]+(")',
                            r'\g<1>' + new_image_url + r'\2',
                            content,
                            count=1
                        )
                        # Regex for Open Graph image
                        content, og_subs = re.subn(
                            r'(<meta property="og:image" content=")[^"]+(")',
                            r'\g<1>' + new_image_url + r'\2',
                            content,
                            count=1
                        )
                        # Regex for the main call-to-action link
                        content, link_subs = re.subn(
                            r'(<a[^>]+id="buyLink"[^>]+href=")[^"]+(")',
                            r'\g<1>' + new_buy_url + r'\2',
                            content,
                            count=1
                        )

                        if img_subs > 0 or og_subs > 0 or link_subs > 0:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            print(f"  -> Updated: {file_path} (Images: {img_subs + og_subs}, Links: {link_subs})")
                        else:
                            print(f"  -> No update patterns found in {file_path}.")

                    except Exception as e:
                        print(f"  -> Error processing file {file_path}: {e}")
                else:
                    print(f"  -> No catalog match for file: {file_path}")

if __name__ == '__main__':
    update_landing_pages('assets/catalog.json')
    print("\nLanding page update process complete.")