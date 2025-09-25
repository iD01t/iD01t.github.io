import json
import os
import re

def slugify(text):
    """
    A simple function to convert a string into a URL-friendly slug.
    """
    text = text.lower()
    # Remove special characters but keep letters, numbers, and spaces
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces and repeated hyphens with a single hyphen
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def create_image_maps(ebook_dir, audiobook_dir):
    """
    Scans the image directories and creates mappings for easy lookup.
    Returns two dictionaries: one for ebooks and one for audiobooks.
    The keys are slugs and the values are the full image paths.
    """
    ebook_map = {slugify(os.path.splitext(f)[0].split('_cover')[0]): f for f in os.listdir(ebook_dir) if f.endswith('.jpg')}
    audiobook_map = {slugify(os.path.splitext(f)[0].split('_cover')[0]): f for f in os.listdir(audiobook_dir) if f.endswith('.jpg')}
    return ebook_map, audiobook_map

def find_image_path(item, primary_map, fallback_map, primary_prefix, fallback_prefix):
    """
    Tries to find a matching image for an item in the provided maps.
    """
    if 'title' in item and item['title']:
        slug = slugify(item['title'])
        # Search in the primary map first
        if slug in primary_map:
            return f"{primary_prefix}{primary_map[slug]}"
        # If not found, search in the fallback map
        if slug in fallback_map:
            return f"{fallback_prefix}{fallback_map[slug]}"

    # As a last resort, check the URL for a book ID
    if 'url' in item and item['url']:
        match = re.search(r'id=([a-zA-Z0-9_-]+)', item['url'])
        if match:
            book_id = match.group(1)
            # Search all files for the ID
            for slug, filename in fallback_map.items():
                 if book_id in filename:
                     return f"{fallback_prefix}{filename}"

    return None

def main():
    catalog_path = 'assets/catalog.json'
    ebook_images_dir = 'assets/harvested/ebooks/'
    audiobook_images_dir = 'assets/harvested/audiobooks/'
    placeholder_path = '/assets/placeholder-cover.svg'

    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading catalog file: {e}")
        return

    ebook_map, audiobook_map = create_image_maps(ebook_images_dir, audiobook_images_dir)

    updated_ebooks = 0
    updated_audiobooks = 0
    not_found_ebooks = []
    not_found_audiobooks = []

    # Update ebooks
    for ebook in catalog.get('ebooks', []):
        current_image = ebook.get('image', '')
        if not current_image or placeholder_path in current_image or not os.path.exists(current_image.lstrip('/')):
            new_path = find_image_path(ebook, ebook_map, {}, ebook_images_dir, '')
            if new_path:
                ebook['image'] = new_path
                updated_ebooks += 1
            else:
                ebook['image'] = placeholder_path
                not_found_ebooks.append(ebook['title'])

    # Update audiobooks
    for audiobook in catalog.get('audiobooks', []):
        current_image = audiobook.get('image', '')
        if not current_image or placeholder_path in current_image or not os.path.exists(current_image.lstrip('/')):
            # Prioritize audiobook-specific images, but fall back to ebook images
            new_path = find_image_path(audiobook, audiobook_map, ebook_map, audiobook_images_dir, ebook_images_dir)
            if new_path:
                audiobook['image'] = new_path
                updated_audiobooks += 1
            else:
                audiobook['image'] = placeholder_path
                not_found_audiobooks.append(audiobook['title'])

    # Write the updated data back to the file
    try:
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print("Catalog update complete.")
        print(f"Ebooks updated: {updated_ebooks}")
        print(f"Audiobooks updated: {updated_audiobooks}")
        if not_found_ebooks:
            print("\nEbooks not found:")
            for title in not_found_ebooks:
                print(f"- {title}")
        if not_found_audiobooks:
            print("\nAudiobooks not found:")
            for title in not_found_audiobooks:
                print(f"- {title}")

    except IOError as e:
        print(f"Error writing to catalog file: {e}")

if __name__ == "__main__":
    main()