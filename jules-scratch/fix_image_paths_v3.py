import json
import os
import re
from unicodedata import normalize

def slugify(text):
    """
    Convert a string to a slug. This version is more robust and handles non-ASCII characters.
    """
    if not text:
        return ""
    # Normalize the text to decompose combined characters
    text = normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Convert to lowercase
    text = text.lower()
    # Remove all characters that are not alphanumeric, spaces, or hyphens
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Replace spaces and repeated hyphens with a single hyphen
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def create_image_maps(ebook_dir, audiobook_dir):
    """
    Create mappings from a slugified version of the filename to the original filename.
    """
    ebook_map = {slugify(os.path.splitext(f)[0].replace('_cover', '')): f for f in os.listdir(ebook_dir) if f.endswith(('.jpg', '.webp'))}
    audiobook_map = {slugify(os.path.splitext(f)[0].replace('_cover', '')): f for f in os.listdir(audiobook_dir) if f.endswith(('.jpg', '.webp'))}
    return ebook_map, audiobook_map

def find_image_path(item, primary_map, fallback_map, primary_prefix, fallback_prefix):
    """
    Find the image path for a given item using a slug of its title.
    """
    if 'title' in item and item['title']:
        slug = slugify(item['title'])

        # Try to find a direct match in the primary map
        if slug in primary_map:
            return os.path.join(primary_prefix, primary_map[slug])

        # Try to find a direct match in the fallback map
        if slug in fallback_map:
            return os.path.join(fallback_prefix, fallback_map[slug])

        # If no direct match, try a partial match
        for map_slug, filename in primary_map.items():
            if slug in map_slug or map_slug in slug:
                return os.path.join(primary_prefix, filename)

        for map_slug, filename in fallback_map.items():
            if slug in map_slug or map_slug in slug:
                return os.path.join(fallback_prefix, filename)

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

    # Process Ebooks
    for ebook in catalog.get('ebooks', []):
        current_image = ebook.get('image', '')
        if not current_image or placeholder_path in current_image or not os.path.exists(current_image.lstrip('/')):
            new_path = find_image_path(ebook, ebook_map, {}, ebook_images_dir, '')
            if new_path:
                ebook['image'] = new_path.replace('\\', '/')
                updated_ebooks += 1
            else:
                ebook['image'] = placeholder_path
                not_found_ebooks.append(ebook.get('title', 'Unknown Title'))

    # Process Audiobooks
    for audiobook in catalog.get('audiobooks', []):
        current_image = audiobook.get('image', '')
        if not current_image or placeholder_path in current_image or not os.path.exists(current_image.lstrip('/')):
            new_path = find_image_path(audiobook, audiobook_map, ebook_map, audiobook_images_dir, ebook_images_dir)
            if new_path:
                audiobook['image'] = new_path.replace('\\', '/')
                updated_audiobooks += 1
            else:
                audiobook['image'] = placeholder_path
                not_found_audiobooks.append(audiobook.get('title', 'Unknown Title'))

    try:
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print("Catalog update complete.")
        print(f"Ebooks updated: {updated_ebooks}")
        print(f"Audiobooks updated: {updated_audiobooks}")
        if not_found_ebooks:
            print(f"\nEbooks not found ({len(not_found_ebooks)}):")
            for title in not_found_ebooks:
                print(f"- {title}")
        if not_found_audiobooks:
            print(f"\nAudiobooks not found ({len(not_found_audiobooks)}):")
            for title in not_found_audiobooks:
                print(f"- {title}")
    except IOError as e:
        print(f"Error writing to catalog file: {e}")

if __name__ == "__main__":
    main()