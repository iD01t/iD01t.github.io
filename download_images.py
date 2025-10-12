import json
import os
import re
import requests

def to_url_safe(s):
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s).strip('-')
    return s

def download_images_and_update_catalog(catalog_path):
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    hd_dir = 'assets/harvested/ebooks/hd'
    sd_dir = 'assets/harvested/ebooks/sd'
    os.makedirs(hd_dir, exist_ok=True)
    os.makedirs(sd_dir, exist_ok=True)

    for book_type in ['ebooks', 'audiobooks']:
        if book_type in catalog:
            for book in catalog[book_type]:
                # Process HD image
                if book.get('image_hd') and book['image_hd'].startswith('http'):
                    book['image_hd'] = download_image(book['image_hd'], book['title'], hd_dir, "-hd")

                # Process SD image
                if book.get('image_sd') and book['image_sd'].startswith('http'):
                    book['image_sd'] = download_image(book['image_sd'], book['title'], sd_dir, "-sd")

    with open(catalog_path, 'w') as f:
        json.dump(catalog, f, indent=2)

def download_image(url, title, target_dir, suffix=""):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        filename_base = to_url_safe(title)
        if not filename_base:
            filename_base = f"item-{url.split('id=')[1].split('&')[0]}"

        content_type = response.headers.get('content-type')
        ext = '.jpg'
        if content_type:
            if 'jpeg' in content_type:
                ext = '.jpg'
            elif 'png' in content_type:
                ext = '.png'
            elif 'webp' in content_type:
                ext = '.webp'

        filename = f"{filename_base}{suffix}{ext}"
        filepath = os.path.join(target_dir, filename)

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"Downloaded: {filename}")
        return f"/{filepath}"

    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return url

if __name__ == '__main__':
    download_images_and_update_catalog('catalog.json')
    print("Image download and catalog update process complete.")
