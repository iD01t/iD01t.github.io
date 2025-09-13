import os

def lazy_load_iframes_in_ebooks():
    with open('tools/ebook_list.txt', 'r') as f:
        filenames = f.read().splitlines()

    for filepath in filenames:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            content = content.replace('<iframe', '<iframe loading="lazy"')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")

if __name__ == '__main__':
    lazy_load_iframes_in_ebooks()
