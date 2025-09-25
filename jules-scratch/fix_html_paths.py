import os
import re

def fix_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # This regex is the Python equivalent of the sed command
    pattern = r'(src|data-src)=["\']\/assets\/harvested\/(ebooks|audiobooks)\/(https?:\/\/[^"\']+)["\']'

    # Use a lambda to construct the replacement string
    replacement = lambda m: f'{m.group(1)}="{m.group(3)}"'

    new_content, count = re.subn(pattern, replacement, content)

    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {count} path(s) in {filepath}")

def main():
    for directory in ['audiobooks', 'ebooks']:
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".html"):
                    filepath = os.path.join(root, filename)
                    fix_html_file(filepath)

if __name__ == "__main__":
    main()