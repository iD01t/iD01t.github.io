import json
import os
import re

def get_title_from_html(html_content):
    """Extracts the book title from the HTML content."""
    # Try to get the title from the <title> tag first
    match = re.search(r'<title>(.*?)<\/title>', html_content)
    if match:
        # Clean up the title
        title = match.group(1).split('·')[0].strip()
        return title
    return None

def update_landing_pages(catalog_path):
    """
    Updates all landing pages by reading the title from each HTML file
    and looking up the corresponding data in the catalog.
    """
    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: Cannot read or parse catalog file at {catalog_path}. {e}")
        return

    # Create a lookup table from the catalog with a clean title as the key
    catalog_lookup = {}
    for book_type in ['ebooks', 'audiobooks']:
        for book in catalog.get(book_type, []):
            title = book.get('title', '').strip()
            if title:
                # A simplified key for matching
                clean_key = re.sub(r'[^a-zA-Z0-9]', '', title).lower()
                catalog_lookup[clean_key] = {
                    'image': book.get('image', ''),
                    'link': book.get('link', '')
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
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    html_title = get_title_from_html(content)
                    if not html_title:
                        print(f"  -> Could not extract title from {file_path}. Skipping.")
                        continue

                    # Create a clean key from the HTML title to find in the lookup
                    lookup_key = re.sub(r'[^a-zA-Z0-9]', '', html_title).lower()

                    if lookup_key in catalog_lookup:
                        book_data = catalog_lookup[lookup_key]
                        new_image_url = book_data.get('image')
                        new_buy_url = book_data.get('link')

                        if not new_image_url or not new_buy_url:
                            print(f"Skipping {file_path}: Missing image or buy URL in catalog.")
                            continue

                        # Update the image and link
                        content, subs = re.subn(r'(<img[^>]+src=")[^"]+(")', r'\g<1>' + new_image_url + r'\2', content)
                        content, subs2 = re.subn(r'(<meta property="og:image" content=")[^"]+(")', r'\g<1>' + new_image_url + r'\2', content)
                        content, subs3 = re.subn(r'(<a[^>]+href=")[^"]+("[^>]*class="[^"]*buy-button[^"]*")', r'\g<1>' + new_buy_url + r'\2', content)

                        if subs > 0 or subs2 > 0 or subs3 > 0:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            print(f"  -> Updated: {file_path}")
                        else:
                            print(f"  -> No patterns to update in {file_path}")

                    else:
                        print(f"  -> No catalog match for title '{html_title}' in {file_path}")

                except Exception as e:
                    print(f"  -> Error processing file {file_path}: {e}")

if __name__ == '__main__':
    update_landing_pages('assets/catalog.json')
    print("\nLanding page update process complete.")