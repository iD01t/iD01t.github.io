import json

def resolve_catalog_conflicts(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    ours_lines = []
    theirs_lines = []
    in_conflict = False
    is_ours = False

    for line in lines:
        if line.startswith('<<<<<<<'):
            in_conflict = True
            is_ours = True
        elif line.startswith('======='):
            is_ours = False
        elif line.startswith('>>>>>>>'):
            in_conflict = False
        elif in_conflict:
            if is_ours:
                ours_lines.append(line)
            else:
                theirs_lines.append(line)
        else:
            ours_lines.append(line)
            theirs_lines.append(line)

    try:
        ours_json = json.loads("".join(ours_lines))
    except json.JSONDecodeError:
        print("Error decoding 'ours' JSON")
        return

    try:
        theirs_json = json.loads("".join(theirs_lines))
    except json.JSONDecodeError:
        print("Error decoding 'theirs' JSON")
        return

    # Merge the data
    merged_catalog = theirs_json

    # Create a map of volume_id to image paths from our changes
    ours_ebook_images = {book['volume_id']: {'image_hd': book.get('image_hd'), 'image_sd': book.get('image_sd')} for book in ours_json.get('ebooks', []) if 'volume_id' in book}
    ours_audiobook_images = {book['volume_id']: {'image_hd': book.get('image_hd'), 'image_sd': book.get('image_sd')} for book in ours_json.get('audiobooks', []) if 'volume_id' in book}

    # Update the merged catalog with our image paths
    for book in merged_catalog.get('ebooks', []):
        if 'volume_id' in book and book['volume_id'] in ours_ebook_images:
            book['image_hd'] = ours_ebook_images[book['volume_id']]['image_hd']
            book['image_sd'] = ours_ebook_images[book['volume_id']]['image_sd']

    for book in merged_catalog.get('audiobooks', []):
        if 'volume_id' in book and book['volume_id'] in ours_audiobook_images:
            book['image_hd'] = ours_audiobook_images[book['volume_id']]['image_hd']
            book['image_sd'] = ours_audiobook_images[book['volume_id']]['image_sd']

    with open(filepath, 'w') as f:
        json.dump(merged_catalog, f, indent=2)

if __name__ == '__main__':
    resolve_catalog_conflicts('catalog.json')
    print("Merge conflicts in catalog.json have been resolved.")
