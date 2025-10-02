import json
import os
import re
import unicodedata

def to_url_safe(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    s = s.strip('-')
    return s

def get_title_from_html(html_content):
    match = re.search(r'<title>(.*?)<\/title>', html_content)
    if match:
        title = match.group(1).split('·')[0].strip()
        return title
    return None

def build_safe_tree(catalog_path):
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    new_dir = 'landing_pages_new'
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    for book_type in ['ebooks', 'audiobooks']:
        book_type_dir = os.path.join(new_dir, book_type)
        if not os.path.exists(book_type_dir):
            os.makedirs(book_type_dir)

        for book in catalog.get(book_type, []):
            title = book.get('title', '').strip()
            if not title:
                continue

            safe_filename_base = to_url_safe(title)
            if not safe_filename_base:
                continue

            new_filepath = os.path.join(book_type_dir, f"{safe_filename_base}.html")

            # Find the original file by iterating and matching title
            original_filepath = None
            if os.path.exists(book_type):
                for existing_file in os.listdir(book_type):
                    if existing_file.endswith('.html'):
                        try:
                            with open(os.path.join(book_type, existing_file), 'r', encoding='utf-8') as f:
                                content = f.read()
                            html_title = get_title_from_html(content)
                            if html_title and to_url_safe(html_title) == safe_filename_base:
                                original_filepath = os.path.join(book_type, existing_file)
                                break
                        except Exception:
                            continue

            if original_filepath:
                with open(original_filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_image_url = book.get('image', '')
                new_buy_url = book.get('link', '')

                content = re.sub(r'(<img[^>]+src=")[^"]+(")', r'\g<1>' + new_image_url + r'\2', content)
                content = re.sub(r'(<meta property="og:image" content=")[^"]+(")', r'\g<1>' + new_image_url + r'\2', content)
                content = re.sub(r'(<a[^>]+href=")[^"]+("[^>]*class="[^"]*buy-button[^"]*")', r'\g<1>' + new_buy_url + r'\2', content)

                with open(new_filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Created updated landing page: {new_filepath}")
            else:
                print(f"Could not find original landing page for: {title}")

if __name__ == '__main__':
    build_safe_tree('assets/catalog.json')
    print("\nSafe landing page tree build process complete.")