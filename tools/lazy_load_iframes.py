import os

def lazy_load_iframes_in_ebooks():
    ebooks_dir = 'ebooks'
    for filename_bytes in os.listdir(ebooks_dir.encode('utf-8')):
        filename = os.fsdecode(filename_bytes)
        if filename.endswith(".html"):
            filepath = os.path.join(ebooks_dir, filename)
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
