import json
import os
import requests
import re

def slugify(text):
    """
    Convert a string to a URL-friendly slug.
    """
    if text is None:
        return ""
    # Remove unsupported characters from the title
    text = re.sub(r'[^\w\s-]', '', str(text).lower())
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'--+', '-', text)
    text = re.sub(r'^-+', '', text)
    text = re.sub(r'-+$', '', text)
    return text

def download_image(url, path):
    """
    Download an image from a URL and save it to a path.
    """
    try:
        # Try to get a higher resolution image
        url = url.replace('zoom=1', 'zoom=3').replace('zoom=5', 'zoom=3')
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    """
    Main function to download ebook covers.
    """
    if not os.path.exists("assets/images"):
        os.makedirs("assets/images")

    with open("data/ebooks.json", "r+", encoding="utf-8") as f:
        ebooks = json.load(f)

        for ebook in ebooks:
            cover_url = ebook.get("cover")
            if cover_url and cover_url.startswith("http"):
                slug = ebook.get("slug")
                if not slug:
                    slug = slugify(ebook.get("title"))
                image_filename = f"{slug}.webp"
                image_path = f"assets/images/{image_filename}"

                if download_image(cover_url, image_path):
                    ebook["cover"] = f"/{image_path}"

        f.seek(0)
        json.dump(ebooks, f, indent=2, ensure_ascii=False)
        f.truncate()

    print(f"Successfully downloaded and updated covers for {len(ebooks)} ebooks.")

if __name__ == "__main__":
    main()
