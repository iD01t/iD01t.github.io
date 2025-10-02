import json
import os
import re
import requests

def to_url_safe(s):
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s).strip('-')
    return s

def download_images_and_update_catalog(catalog_path):
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    images_dir = 'assets/images'
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for book_type in ['ebooks', 'audiobooks']:
        for book in catalog[book_type]:
            image_url = book.get('image')
            if image_url and image_url.startswith('http'):
                try:
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()

                    # Generate a clean filename
                    filename_base = to_url_safe(book['title'])
                    if not filename_base:
                        # Fallback for titles with only special characters
                        filename_base = f"item-{book.get('id', 'unknown')}"

                    # Determine the file extension
                    content_type = response.headers.get('content-type')
                    if content_type and 'jpeg' in content_type:
                        ext = '.jpg'
                    elif content_type and 'png' in content_type:
                        ext = '.png'
                    elif content_type and 'webp' in content_type:
                        ext = '.webp'
                    else:
                        # Fallback extension
                        ext = '.jpg'

                    filename = f"{filename_base}-cover{ext}"
                    filepath = os.path.join(images_dir, filename)

                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    print(f"Downloaded: {filename}")

                    # Update the image path in the catalog
                    book['image'] = f"/{filepath}"

                except requests.exceptions.RequestException as e:
                    print(f"Error downloading {image_url}: {e}")
                    # Keep the original URL if download fails
                    pass

    with open(catalog_path, 'w') as f:
        json.dump(catalog, f, indent=2)

if __name__ == '__main__':
    download_images_and_update_catalog('assets/catalog.json')
    print("Image download and catalog update process complete.")