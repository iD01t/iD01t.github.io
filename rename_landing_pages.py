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

def find_file_ignore_case(directory, filename):
    for f in os.listdir(directory):
        if f.lower() == filename.lower():
            return os.path.join(directory, f)
    return None

def rename_landing_pages(catalog_path):
    with open(catalog_path, 'r') as f:
        catalog = json.load(f)

    for book_type in ['ebooks', 'audiobooks']:
        if not os.path.exists(book_type):
            continue

        for book in catalog.get(book_type, []):
            title = book.get('title', '').strip()
            if not title:
                continue

            standard_filename_base = to_url_safe(title)
            if not standard_filename_base:
                continue

            standard_filename = f"{standard_filename_base}.html"

            # Find a matching file, even with encoding differences
            for existing_file in os.listdir(book_type):
                # Heuristic: if the url-safe version of the existing file matches the standard, we have a candidate
                if to_url_safe(os.path.splitext(existing_file)[0]) == standard_filename_base:
                    old_path = os.path.join(book_type, existing_file)
                    new_path = os.path.join(book_type, standard_filename)
                    if old_path != new_path:
                        try:
                            os.rename(old_path, new_path)
                            print(f"Renamed: {old_path} -> {new_path}")
                        except OSError as e:
                            print(f"Error renaming {old_path} to {new_path}: {e}")
                    break

if __name__ == '__main__':
    rename_landing_pages('assets/catalog.json')
    print("\nLanding page renaming process complete.")