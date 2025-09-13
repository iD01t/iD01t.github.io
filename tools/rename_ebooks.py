import os

def rename_ebooks():
    ebooks_dir = 'ebooks'
    for filename in os.listdir(ebooks_dir):
        if filename.endswith(".html"):
            os.rename(os.path.join(ebooks_dir, filename), os.path.join(ebooks_dir, f"_{filename}"))

def rename_ebooks_back():
    ebooks_dir = 'ebooks'
    for filename in os.listdir(ebooks_dir):
        if filename.startswith("_") and filename.endswith(".html"):
            os.rename(os.path.join(ebooks_dir, filename), os.path.join(ebooks_dir, filename[1:]))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'back':
        rename_ebooks_back()
    else:
        rename_ebooks()
