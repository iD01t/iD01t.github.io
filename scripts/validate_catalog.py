import json
import re

def validate_url(url):
    """Validate the URL format."""
    # A simple regex to check if the URL is valid.
    # This is a basic check and does not guarantee the URL is reachable.
    return re.match(r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', url)

def validate_catalog(catalog_path):
    """
    Validates the catalog file for correct image paths and URLs.
    """
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    issues_found = False

    print("--- Validating eBooks ---")
    for ebook in catalog.get('ebooks', []):
        title = ebook.get('title', 'N/A')

        # Validate image path
        image_path = ebook.get('image', '')
        if not image_path.startswith('/assets/images/'):
            print(f"[ERROR] eBook '{title}': Invalid image path start: {image_path}")
            issues_found = True
        if not image_path.endswith('.webp'):
            print(f"[ERROR] eBook '{title}': Invalid image extension: {image_path}")
            issues_found = True

        # Validate 'link' URL
        link_url = ebook.get('link', '')
        if not validate_url(link_url):
            print(f"[ERROR] eBook '{title}': Invalid 'link' URL: {link_url}")
            issues_found = True

        # Validate 'url' URL
        page_url = ebook.get('url', '')
        if not validate_url(page_url):
            print(f"[ERROR] eBook '{title}': Invalid 'url': {page_url}")
            issues_found = True

    print("\n--- Validating Audiobooks ---")
    for audiobook in catalog.get('audiobooks', []):
        title = audiobook.get('title', 'N/A')

        # Validate image path
        image_path = audiobook.get('image', '')
        if not image_path.startswith('/assets/images/'):
            print(f"[ERROR] Audiobook '{title}': Invalid image path start: {image_path}")
            issues_found = True
        if not image_path.endswith('.webp'):
            print(f"[ERROR] Audiobook '{title}': Invalid image extension: {image_path}")
            issues_found = True

        # Validate 'link' URL
        link_url = audiobook.get('link', '')
        if not validate_url(link_url):
            print(f"[ERROR] Audiobook '{title}': Invalid 'link' URL: {link_url}")
            issues_found = True

    if not issues_found:
        print("\nValidation complete. No issues found.")
    else:
        print("\nValidation complete. Issues found.")

if __name__ == "__main__":
    validate_catalog('assets/catalog.json')