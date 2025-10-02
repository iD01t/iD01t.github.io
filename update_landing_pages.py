import json
import os
import re
import unicodedata

def to_url_safe(s):
    # Normalize the string to decompose combined characters (like é -> e + ´)
    s = unicodedata.normalize('NFKD', s)
    # Encode to ASCII bytes, ignoring characters that can't be represented
    s = s.encode('ascii', 'ignore').decode('ascii')
    # Convert to lowercase
    s = s.lower()
    # Remove any characters that are not alphanumeric, spaces, or hyphens
    s = re.sub(r'[^\w\s-]', '', s)
    # Replace one or more spaces/hyphens with a single hyphen
    s = re.sub(r'[\s-]+', '-', s)
    # Remove leading/trailing hyphens
    s = s.strip('-')
    return s

def update_landing_pages(catalog_path):
    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing catalog file at {catalog_path}: {e}")
        return

    # Process eBooks and Audiobooks
    for book_type in ['ebooks', 'audiobooks']:
        print(f"\nProcessing {book_type}...")
        for book in catalog.get(book_type, []):
            title = book.get('title', '').strip()
            if not title:
                print("Skipping entry with no title.")
                continue

            # Generate the expected filename from the title
            filename_base = to_url_safe(title)
            if not filename_base:
                print(f"Could not generate a valid filename for title: {title}")
                continue

            # Construct the path
            page_path = os.path.join(book_type, f"{filename_base}.html")

            print(f"Attempting to update: {page_path}")

            if os.path.exists(page_path):
                try:
                    with open(page_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_image_url = book.get('image', '')
                    new_buy_url = book.get('link', '')

                    if not new_image_url or not new_buy_url:
                        print(f"Skipping update for {page_path} due to missing image or buy URL.")
                        continue

                    # Regex to find the main cover image
                    content, img_subs = re.subn(
                        r'(<img[^>]+src=")[^"]+("[^>]*alt="[^"]*cover[^"]*"[^>]*>)',
                        r'\g<1>' + new_image_url + r'\2',
                        content,
                        count=1
                    )

                    # Regex to find Open Graph image meta tag
                    content, og_img_subs = re.subn(
                        r'(<meta property="og:image" content=")[^"]+(")',
                        r'\g<1>' + new_image_url + r'\2',
                        content
                    )

                    # Regex to find the primary "Buy" or "Listen" button link
                    content, link_subs = re.subn(
                        r'(<a[^>]+href=")[^"]+("[^>]*class="[^"]*(?:buy|get|purchase|listen)-button[^"]*"[^>]*>)',
                        r'\g<1>' + new_buy_url + r'\2',
                        content
                    )

                    if img_subs > 0 or og_img_subs > 0 or link_subs > 0:
                        with open(page_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"  -> Successfully updated: {page_path} (Images: {img_subs+og_img_subs}, Links: {link_subs})")
                    else:
                        print(f"  -> No matching patterns found to update in {page_path}.")

                except Exception as e:
                    print(f"  -> Error processing file {page_path}: {e}")
            else:
                print(f"  -> Landing page not found for '{title}' (expected at {page_path})")

if __name__ == '__main__':
    update_landing_pages('assets/catalog.json')
    print("\nLanding page update process complete.")