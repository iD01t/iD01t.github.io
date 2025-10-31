import json
import os
import re
from resolver import open_by_slug, SLUG_TO_REAL
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

def update_landing_pages_with_resolver(catalog_path):
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
                        'type': book_type,
                        'slug': f"{safe_key}.html"
                    }

    # Iterate through the slugs in the resolver and update files
    for slug in SLUG_TO_REAL.keys():
        file_key = os.path.splitext(slug)[0]
        if file_key in catalog_lookup:
            book_data = catalog_lookup[file_key]
            new_image_url = book_data.get('image')
            new_buy_url = book_data.get('link')

            if not new_image_url or not new_buy_url:
                print(f"Skipping {slug}: Missing image or buy URL in catalog.")
                continue

            try:
                with open_by_slug(slug, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Regex for the main cover image
                content, img_subs = re.subn(
                    r'(<img[^>]+src=")[^"]+("[^>]*alt="[^"]*cover[^"]*"[^>]*>)',
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
                    r'(<a[^>]+href=")[^"]+("[^>]*class="[^"]*(?:buy|get|purchase|listen)-button[^"]*"[^>]*>)',
                    r'\g<1>' + new_buy_url + r'\2',
                    content
                )

                if img_subs > 0 or og_subs > 0 or link_subs > 0:
                    with open_by_slug(slug, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  -> Updated: {slug} (Images: {img_subs + og_subs}, Links: {link_subs})")
                else:
                    print(f"  -> No update patterns found in {slug}.")

            except Exception as e:
                print(f"  -> Error processing file with slug {slug}: {e}")
        else:
            print(f"  -> No catalog match for slug: {slug}")

if __name__ == '__main__':
    update_landing_pages_with_resolver('assets/catalog.json')
    print("\nLanding page update process complete.")