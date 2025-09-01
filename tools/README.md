# Image Fixing Tools

## Overview
Tools to fix broken image references and ensure all images are local or base64 encoded.

## fix_images.py

### Purpose
Automatically scans all HTML files in the repository and fixes broken image references by:
1. Downloading external images (especially Imgur)
2. Converting them to WebP format
3. Storing them locally in `/assets/images/`
4. Updating HTML files to use local paths
5. Maintaining a manifest in `/assets/images.json`

### Installation
```bash
pip install -r requirements.txt
```

### Usage

#### Dry Run (see what would be changed)
```bash
python tools/fix_images.py --dry-run
```

#### Fix All Images
```bash
python tools/fix_images.py
```

#### Fix Images in Specific Directory
```bash
python tools/fix_images.py --repo-path /path/to/repo
```

### Features
- **Smart Image Processing**: Converts to WebP with optimal quality
- **Automatic Resizing**: Limits images to 800x1200 for performance
- **Fallback Handling**: Uses placeholder for failed downloads
- **Manifest Management**: Maintains JSON mapping of titles to local paths
- **HTML Updates**: Automatically updates img tags with lazy loading

### Output
- Local WebP images in `/assets/images/`
- Updated HTML files with local image paths
- Enhanced `images.json` manifest
- Console progress reporting

## Requirements
- Python 3.7+
- BeautifulSoup4 (HTML parsing)
- Pillow (image processing)
- Requests (HTTP downloads)

## Notes
- Always run with `--dry-run` first to see what will be changed
- The tool respects existing local images and base64 data
- External images are only processed if they're not from trusted domains
- All processed images get proper alt text, lazy loading, and async decoding
