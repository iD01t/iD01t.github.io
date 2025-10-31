import json
import os
import re
import requests
import uuid

def to_url_safe(s):
    if not s:
        return ""
    s = s.lower()
    s = re.sub(r'[^a-z0-9\\s-]', '', s)
    s = re.sub(r'[\\s-]+', '-', s).strip('-')
    return s

def download_image(url, filename_base, target_dir, suffix=""):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

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

def download_images_and_update_catalog(catalog_path):
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    hd_dir = 'assets/harvested/ebooks/hd'
    sd_dir = 'assets/harvested/ebooks/sd'
    os.makedirs(hd_dir, exist_ok=True)
    os.makedirs(sd_dir, exist_ok=True)

    book_lists = [k for k in catalog.keys() if isinstance(catalog.get(k), list)]

    for book_type in book_lists:
        for book in catalog[book_type]:
            title = book.get('title')
            image_url = book.get('image')

            print(f"Processing book: {title}")

            if not image_url or not image_url.startswith('http'):
                print(f"  Skipping book with no valid image URL.")
                continue

            volume_id = book.get('volume_id')
            if volume_id:
                filename_base = to_url_safe(volume_id)
            elif title:
                filename_base = to_url_safe(title)
            else:
                filename_base = str(uuid.uuid4())
                print(f"Warning: Book with no volume_id or title found. Using UUID for filename.")

            # Download for HD
            hd_path = download_image(image_url, filename_base, hd_dir, "-hd")
            book['image_hd'] = hd_path

            # Download for SD
            sd_path = download_image(image_url, filename_base, sd_dir, "-sd")
            book['image_sd'] = sd_path


    with open(catalog_path, 'w') as f:
        json.dump(catalog, f, indent=2)

if __name__ == '__main__':
    download_images_and_update_catalog('catalog.json')
    print("Image download and catalog update process complete.")
