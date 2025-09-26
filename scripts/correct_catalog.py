import json
import re
import os

def slugify(text):
    """
    Generate a slug from a given text.
    """
    # Lowercase the text
    text = text.lower()
    # Replace special characters with spaces
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces and repeated dashes with a single dash
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text

def correct_catalog(input_path, output_path):
    """
    Corrects image paths and URLs in the catalog file.
    """
    with open(input_path, 'r') as f:
        catalog = json.load(f)

    # --- Correct eBooks ---
    if 'ebooks' in catalog:
        for ebook in catalog['ebooks']:
            title = ebook.get('title', 'N/A')

            # Correct image path
            if 'image' in ebook:
                image_path = ebook['image']
                # Standardize to /assets/images/ and .webp
                filename = os.path.basename(image_path)
                # Create a slug from the title for a standardized filename
                slug = slugify(title)
                new_image_path = f"/assets/images/{slug}-cover.webp"
                ebook['image'] = new_image_path

            # Correct 'link' and 'url' if they are invalid
            is_link_valid = ebook.get('link') and re.match(r'^https?://', ebook['link'])
            is_url_valid = ebook.get('url') and re.match(r'^https?://', ebook['url'])

            if not is_link_valid or not is_url_valid:
                print(f"[WARNING] eBook '{title}': Invalid or missing URL. Marking as unavailable.")
                ebook['link'] = "#"
                ebook['url'] = "#"
                ebook['status'] = "unavailable"
            else:
                 # Ensure status is 'available' if links are valid
                ebook['status'] = 'available'


    # --- Correct Audiobooks ---
    if 'audiobooks' in catalog:
        for audiobook in catalog.get('audiobooks', []):
            title = audiobook.get('title', 'N/A')

            # Correct image path
            if 'image' in audiobook:
                image_path = audiobook['image']
                filename = os.path.basename(image_path)
                slug = slugify(title)
                new_image_path = f"/assets/images/{slug}-cover.webp"
                audiobook['image'] = new_image_path

            # Correct 'link' URL
            is_link_valid = audiobook.get('link') and re.match(r'^https?://', audiobook['link'])

            if not is_link_valid:
                print(f"[WARNING] Audiobook '{title}': Invalid or missing 'link'. Marking as unavailable.")
                audiobook['link'] = "#"
                audiobook['status'] = "unavailable"
            else:
                audiobook['status'] = "available"

    # Write the corrected catalog to a new file
    with open(output_path, 'w') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"\nCorrection complete. Corrected catalog saved to {output_path}")

if __name__ == "__main__":
    correct_catalog('assets/catalog.json', 'assets/catalog_corrected.json')