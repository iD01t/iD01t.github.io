import json
import os
import re

def to_slug(name):
    """Converts a string to a slug."""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')

def find_best_image(book, harvested_ebooks_path, harvested_audiobooks_path, assets_images_path):
    """Finds the best available image for a book, prioritizing local HD files."""

    title_slug = to_slug(book.get('title', ''))

    # --- Priority 1: Harvested HD (zoom5) images by ebook_number ---
    ebook_number = book.get('ebook_number') or book.get('audiobook_number')
    if ebook_number:
        # Construct expected HD filename format
        clean_title_slug = book.get('title', '').replace(':', '').replace('’', '').replace(',', '')
        clean_title_slug = re.sub(r'[^a-zA-Z0-9\s]', '', clean_title_slug).replace(' ', '_')

        # Look for zoom5 first, then thumbnail in ebooks
        zoom5_filename_ebook = f"ebook_{str(ebook_number).zfill(3)}_{clean_title_slug}_zoom5.jpg"
        if os.path.exists(os.path.join(harvested_ebooks_path, zoom5_filename_ebook)):
            return f"/assets/harvested/ebooks/{zoom5_filename_ebook}"

        thumbnail_filename_ebook = f"ebook_{str(ebook_number).zfill(3)}_{clean_title_slug}_thumbnail.jpg"
        if os.path.exists(os.path.join(harvested_ebooks_path, thumbnail_filename_ebook)):
            return f"/assets/harvested/ebooks/{thumbnail_filename_ebook}"

        # Look for zoom5 first, then thumbnail in audiobooks
        zoom5_filename_audio = f"audiobook_{str(ebook_number).zfill(3)}_{clean_title_slug}_zoom5.jpg"
        if os.path.exists(os.path.join(harvested_audiobooks_path, zoom5_filename_audio)):
            return f"/assets/harvested/audiobooks/{zoom5_filename_audio}"

        thumbnail_filename_audio = f"audiobook_{str(ebook_number).zfill(3)}_{clean_title_slug}_thumbnail.jpg"
        if os.path.exists(os.path.join(harvested_audiobooks_path, thumbnail_filename_audio)):
            return f"/assets/harvested/audiobooks/{thumbnail_filename_audio}"

    # --- Priority 2: Harvested images by Google Books ID ---
    google_id = None
    for key in ['url', 'link', 'image']:
        if book.get(key) and 'id=' in book[key]:
            try:
                google_id = re.search(r'id=([a-zA-Z0-9_-]+)', book[key]).group(1)
                break
            except AttributeError:
                continue

    if google_id:
        google_filename = f"{title_slug}_{google_id}_cover.jpg"
        if os.path.exists(os.path.join(harvested_ebooks_path, google_filename)):
            return f"/assets/harvested/ebooks/{google_filename}"

    # --- Priority 3: Harvested images by title slug (for audiobooks and fallbacks) ---
    audiobook_cover_path = os.path.join(harvested_audiobooks_path, f"{title_slug}_cover.jpg")
    if os.path.exists(audiobook_cover_path):
        return f"/assets/harvested/audiobooks/{title_slug}_cover.jpg"

    # --- Priority 4: General assets/images by title slug ---
    asset_image_path = os.path.join(assets_images_path, f"{title_slug}-cover.webp")
    if os.path.exists(asset_image_path):
        return f"/assets/images/{title_slug}-cover.webp"

    # --- Priority 5: Check if existing image path is a valid local file ---
    existing_image = book.get('image', '')
    if existing_image and not existing_image.startswith('http'):
        # Normalize path to be relative from root
        if existing_image.startswith('/'):
            local_path = existing_image.lstrip('/')
        else:
            local_path = existing_image

        if os.path.exists(local_path):
            return f"/{local_path}" # Return as root-relative path

    # --- Fallback to a placeholder if no image is found ---
    return "/assets/placeholder-cover.svg"


def main():
    """
    Cleans and standardizes the catalog JSON file.
    """
    catalog_path = 'assets/catalog.json'
    output_path = 'assets/catalog_cleaned.json'

    harvested_ebooks_path = 'assets/harvested/ebooks'
    harvested_audiobooks_path = 'assets/harvested/audiobooks'
    assets_images_path = 'assets/images'

    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    except FileNotFoundError:
        print(f"Error: Catalog file not found at {catalog_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {catalog_path}")
        return

    print("Cleaning and standardizing ebook entries...")
    for book in catalog.get('ebooks', []):
        book['image'] = find_best_image(book, harvested_ebooks_path, harvested_audiobooks_path, assets_images_path)
        # Simple link validation/correction
        if not book.get('link') and book.get('url'):
            book['link'] = book['url']
        if not book.get('link'):
             book['link'] = '#' # Placeholder link

    print("Cleaning and standardizing audiobook entries...")
    for book in catalog.get('audiobooks', []):
        best_image = find_best_image(book, harvested_ebooks_path, harvested_audiobooks_path, assets_images_path)
        book['image'] = best_image
        if not book.get('link') and book.get('url'):
            book['link'] = book['url']
        if not book.get('link'):
             book['link'] = '#'

    # We can skip series for now as it doesn't have the same problem.

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"Successfully cleaned catalog saved to {output_path}")
    except IOError as e:
        print(f"Error writing to output file {output_path}: {e}")

if __name__ == '__main__':
    main()