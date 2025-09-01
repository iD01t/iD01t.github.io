#!/usr/bin/env python3
"""
Image fixer tool for iD01t Productions website.
Scans HTML files and fixes broken image references.
"""

import os
import re
import json
import argparse
import requests
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from PIL import Image
import io

def download_image(url, timeout=10):
    """Download image from URL with error handling."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"  ❌ Failed to download {url}: {e}")
        return None

def convert_to_webp(image_data, output_path, quality=85):
    """Convert image data to WebP format."""
    try:
        image = Image.open(io.BytesIO(image_data))
        # Convert RGBA to RGB if necessary
        if image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (15, 21, 48))
            background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize if too large
        max_size = (800, 1200)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        image.save(output_path, 'WEBP', quality=quality, optimize=True)
        return True
    except Exception as e:
        print(f"  ❌ Failed to convert to WebP: {e}")
        return False

def slugify(text):
    """Convert text to URL-friendly slug."""
    return re.sub(r'[^\w\-]', '-', text.lower()).strip('-')

def fix_images_in_html(html_file, images_dir, images_manifest, dry_run=False):
    """Fix images in a single HTML file."""
    print(f"📄 Processing: {html_file}")
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        modified = False
        
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if not src:
                continue
                
            # Skip if already local or base64
            if src.startswith(('data:', '/assets/', './assets/')):
                continue
                
            # Check if it's an external image that needs fixing
            if src.startswith('http') and not any(domain in src.lower() for domain in ['id01t.store', 'id01t.github.io']):
                print(f"  🔗 Found external image: {src}")
                
                if dry_run:
                    print(f"    [DRY RUN] Would download and convert: {src}")
                    continue
                
                # Generate filename from alt text or URL
                alt_text = img.get('alt', '')
                filename = slugify(alt_text) if alt_text else slugify(os.path.basename(urlparse(src).path))
                if not filename:
                    filename = 'image'
                
                webp_path = f"/assets/images/{filename}.webp"
                local_path = Path(images_dir) / f"{filename}.webp"
                
                # Download and convert
                print(f"    📥 Downloading: {src}")
                image_data = download_image(src)
                if image_data:
                    print(f"    🎨 Converting to WebP: {local_path}")
                    if convert_to_webp(image_data, local_path):
                        # Update HTML
                        img['src'] = webp_path
                        img['loading'] = 'lazy'
                        img['decoding'] = 'async'
                        img['referrerPolicy'] = 'no-referrer'
                        
                        # Update manifest
                        if alt_text:
                            images_manifest[alt_text] = webp_path
                        
                        modified = True
                        print(f"    ✅ Fixed: {src} → {webp_path}")
                    else:
                        print(f"    ❌ Failed to convert: {src}")
                else:
                    print(f"    ❌ Failed to download: {src}")
        
        if modified:
            # Write updated HTML
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"  💾 Updated: {html_file}")
        
        return modified
        
    except Exception as e:
        print(f"  ❌ Error processing {html_file}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Fix broken images in HTML files')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--repo-path', default='.', help='Path to repository root')
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    html_files = list(repo_path.rglob('*.html'))
    images_dir = repo_path / 'assets' / 'images'
    manifest_path = repo_path / 'assets' / 'images.json'
    
    print(f"🔍 Found {len(html_files)} HTML files")
    print(f"📁 Images directory: {images_dir}")
    print(f"📋 Manifest: {manifest_path}")
    
    # Ensure images directory exists
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # Load existing manifest
    images_manifest = {}
    if manifest_path.exists():
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                images_manifest = json.load(f)
            print(f"📋 Loaded existing manifest with {len(images_manifest)} entries")
        except Exception as e:
            print(f"⚠️  Could not load manifest: {e}")
    
    # Process HTML files
    fixed_count = 0
    for html_file in html_files:
        if fix_images_in_html(html_file, images_dir, images_manifest, args.dry_run):
            fixed_count += 1
    
    # Save updated manifest
    if not args.dry_run and images_manifest:
        try:
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(images_manifest, f, indent=2, ensure_ascii=False)
            print(f"💾 Updated manifest with {len(images_manifest)} entries")
        except Exception as e:
            print(f"❌ Failed to save manifest: {e}")
    
    # Summary
    if args.dry_run:
        print(f"\n🔍 DRY RUN COMPLETE")
        print(f"   Would process: {len(html_files)} files")
        print(f"   Would fix: {fixed_count} files")
    else:
        print(f"\n✅ COMPLETE")
        print(f"   Processed: {len(html_files)} files")
        print(f"   Fixed: {fixed_count} files")
        print(f"   Manifest entries: {len(images_manifest)}")

if __name__ == '__main__':
    main()
