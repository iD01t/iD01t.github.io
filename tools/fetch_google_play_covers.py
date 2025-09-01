#!/usr/bin/env python3
"""
Enhanced Google Play Cover Fetcher for iD01t Productions website.
Fetches real cover images from Google Play Books with multiple fallback methods.
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, quote
import random

def get_random_user_agent():
    """Get a random user agent to avoid detection."""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    return random.choice(user_agents)

def extract_google_play_id(url):
    """Extract Google Play Book ID from URL with multiple fallback methods."""
    if not url or 'play.google.com' not in url:
        return None
    
    # Method 1: Extract from query parameter
    if 'id=' in url:
        try:
            query = parse_qs(urlparse(url).query)
            book_id = query.get('id', [None])[0]
            if book_id:
                return book_id
        except:
            pass
    
    # Method 2: Extract from path
    try:
        path = urlparse(url).path
        if '/books/details/' in path:
            book_id = path.split('/books/details/')[-1]
            if book_id and len(book_id) > 5:
                return book_id
    except:
        pass
    
    # Method 3: Extract from URL using regex
    try:
        match = re.search(r'id=([A-Z0-9:_]+)', url)
        if match:
            return match.group(1)
    except:
        pass
    
    return None

def try_alternative_google_play_urls(book_id):
    """Try different Google Play URL formats."""
    if not book_id:
        return []
    
    # Try different URL formats
    urls = [
        f"https://play.google.com/store/books/details?id={book_id}",
        f"https://play.google.com/store/books/details?id={quote(book_id)}",
        f"https://play.google.com/store/books/details?id={book_id}&hl=en",
        f"https://play.google.com/store/books/details?id={book_id}&hl=fr",
        f"https://play.google.com/store/books/details?id={book_id}&hl=es",
        f"https://play.google.com/store/books/details?id={book_id}&hl=de",
        f"https://play.google.com/store/books/details?id={book_id}&hl=it",
        f"https://play.google.com/store/books/details?id={book_id}&hl=pt",
        f"https://play.google.com/store/books/details?id={book_id}&hl=ru",
        f"https://play.google.com/store/books/details?id={book_id}&hl=ja",
        f"https://play.google.com/store/books/details?id={book_id}&hl=ko",
        f"https://play.google.com/store/books/details?id={book_id}&hl=zh"
    ]
    
    return urls

def fetch_google_play_cover_robust(book_id):
    """Fetch cover image from Google Play Books with multiple fallback methods."""
    if not book_id:
        return None
    
    urls_to_try = try_alternative_google_play_urls(book_id)
    
    for url in urls_to_try:
        try:
            print(f"        🔍 Trying: {url}")
            
            # Set headers to mimic a browser request
            headers = {
                'User-Agent': get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
            
            # Add a small delay to be respectful
            time.sleep(0.5)
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Method 1: Look for cover images in various locations
                cover_img = None
                
                # Try different selectors for cover images
                selectors = [
                    'img[alt*="cover" i]',
                    'img[alt*="Cover" i]',
                    'img[class*="cover" i]',
                    'img[class*="Cover" i]',
                    'img[src*="cover" i]',
                    'img[src*="Cover" i]',
                    'img[data-src*="cover" i]',
                    'img[data-src*="Cover" i]',
                    'img[style*="cover" i]',
                    'img[style*="Cover" i]'
                ]
                
                for selector in selectors:
                    cover_img = soup.select_one(selector)
                    if cover_img:
                        break
                
                # Method 2: Look for any image that might be a cover
                if not cover_img:
                    images = soup.find_all('img')
                    for img in images:
                        src = img.get('src', '')
                        alt = img.get('alt', '')
                        if src and ('cover' in alt.lower() or 'book' in alt.lower() or 'title' in alt.lower()):
                            cover_img = img
                            break
                
                # Method 3: Look for the first reasonable image
                if not cover_img:
                    images = soup.find_all('img')
                    for img in images:
                        src = img.get('src', '')
                        if src and src.startswith('http') and ('googleusercontent.com' in src or 'play.google.com' in src):
                            cover_img = img
                            break
                
                if cover_img and cover_img.get('src'):
                    src = cover_img['src']
                    
                    # Convert to HTTPS if needed
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = 'https://play.google.com' + src
                    
                    # Ensure it's a valid image URL
                    if src.startswith('http') and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
                        print(f"        ✅ Found cover: {src}")
                        return src
                    elif 'googleusercontent.com' in src or 'play.google.com' in src:
                        print(f"        ✅ Found cover: {src}")
                        return src
            
            elif response.status_code == 404:
                print(f"        ❌ 404 Not Found")
                continue
            else:
                print(f"        ⚠️  Status: {response.status_code}")
                continue
                
        except requests.exceptions.Timeout:
            print(f"        ⏰ Timeout")
            continue
        except requests.exceptions.ConnectionError:
            print(f"        🔌 Connection Error")
            continue
        except Exception as e:
            print(f"        ❌ Error: {str(e)[:50]}")
            continue
    
    return None

def find_google_play_links_in_html(html_content):
    """Find Google Play links in HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=re.compile(r'play\.google\.com'))
    
    google_play_links = []
    for link in links:
        href = link.get('href')
        if href and 'play.google.com' in href:
            google_play_links.append(href)
    
    return google_play_links

def update_html_file_with_google_play_cover(html_file_path):
    """Update a single HTML file to use Google Play cover image."""
    print(f"    📄 Processing: {html_file_path.name}")
    
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find Google Play links
        google_play_links = find_google_play_links_in_html(content)
        
        if not google_play_links:
            print(f"        ⚠️  No Google Play links found")
            return False
        
        # Use the first Google Play link found
        google_play_link = google_play_links[0]
        book_id = extract_google_play_id(google_play_link)
        
        if not book_id:
            print(f"        ⚠️  Could not extract Google Play ID from: {google_play_link}")
            return False
        
        print(f"        🔍 Found Google Play ID: {book_id}")
        
        # Fetch the cover image with robust method
        cover_url = fetch_google_play_cover_robust(book_id)
        
        if not cover_url:
            print(f"        ❌ Failed to fetch cover image after trying all methods")
            return False
        
        print(f"        ✅ Successfully fetched cover: {cover_url}")
        
        # Update the HTML content
        soup = BeautifulSoup(content, 'html.parser')
        
        # Update the main image
        img = soup.find('img')
        if img:
            old_src = img.get('src', '')
            img['src'] = cover_url
            print(f"        🔄 Updated image from {old_src} to {cover_url}")
        
        # Update Open Graph image
        og_img = soup.find('meta', {'property': 'og:image'})
        if og_img:
            old_og = og_img.get('content', '')
            og_img['content'] = cover_url
            print(f"        🔄 Updated og:image from {old_og} to {cover_url}")
        
        # Update schema markup
        schema_script = soup.find('script', {'type': 'application/ld+json'})
        if schema_script:
            try:
                schema_data = json.loads(schema_script.string)
                if 'image' in schema_data:
                    old_schema = schema_data['image']
                    schema_data['image'] = cover_url
                    schema_script.string = json.dumps(schema_data, ensure_ascii=False)
                    print(f"        🔄 Updated schema image from {old_schema} to {cover_url}")
            except Exception as e:
                print(f"        ⚠️  Could not update schema markup: {e}")
        
        # Save the updated HTML
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"        💾 Saved updated HTML file")
        return True
        
    except Exception as e:
        print(f"        ❌ Error processing {html_file_path.name}: {e}")
        return False

def update_all_html_files_with_google_play_covers(ebooks_dir, audiobooks_dir):
    """Update all HTML files to use Google Play cover images."""
    print("🌐 Updating HTML files with Google Play cover images...")
    
    updated_count = 0
    total_files = 0
    
    # Process ebooks directory
    print("📚 Processing ebooks directory...")
    for html_file in Path(ebooks_dir).glob('*.html'):
        total_files += 1
        if update_html_file_with_google_play_cover(html_file):
            updated_count += 1
        
        # Add a small delay between files to be respectful
        time.sleep(1)
    
    # Process audiobooks directory
    print("🎧 Processing audiobooks directory...")
    for html_file in Path(audiobooks_dir).glob('*.html'):
        total_files += 1
        if update_html_file_with_google_play_cover(html_file):
            updated_count += 1
        
        # Add a small delay between files to be respectful
        time.sleep(1)
    
    print(f"📊 Update Summary:")
    print(f"   Total files processed: {total_files}")
    print(f"   Successfully updated: {updated_count}")
    print(f"   Failed updates: {total_files - updated_count}")
    
    return updated_count

def test_single_book_id(book_id):
    """Test a single book ID to see if it works."""
    print(f"🧪 Testing book ID: {book_id}")
    cover_url = fetch_google_play_cover_robust(book_id)
    if cover_url:
        print(f"✅ Success: {cover_url}")
    else:
        print(f"❌ Failed to fetch cover")
    return cover_url

def main():
    """Main function to update all ebooks with Google Play cover images."""
    import argparse
    parser = argparse.ArgumentParser(description='Update ebooks with Google Play cover images')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--test-id', type=str, help='Test a specific book ID')
    parser.add_argument('--repo-path', default='.', help='Path to repository root')
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    ebooks_dir = repo_path / 'ebooks'
    audiobooks_dir = repo_path / 'audiobooks'
    
    if not ebooks_dir.exists():
        print(f"❌ Ebooks directory not found: {ebooks_dir}")
        return
    
    if not audiobooks_dir.exists():
        print(f"❌ Audiobooks directory not found: {audiobooks_dir}")
        return
    
    print("🚀 Enhanced Google Play Cover Fetcher for iD01t Productions")
    print("=" * 70)
    
    # Test mode
    if args.test_id:
        test_single_book_id(args.test_id)
        return
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
        
        # Count files and show what would be updated
        ebook_files = list(ebooks_dir.glob('*.html'))
        audiobook_files = list(audiobooks_dir.glob('*.html'))
        
        print(f"📚 Ebooks directory: {len(ebook_files)} HTML files")
        print(f"🎧 Audiobooks directory: {len(audiobook_files)} HTML files")
        print(f"📊 Total: {len(ebook_files) + len(audiobook_files)} files")
        
        # Show a few examples of what would be processed
        print("\n🔍 Sample files that would be processed:")
        for i, file_path in enumerate(ebook_files[:3]):
            print(f"    📄 {file_path.name}")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                google_play_links = find_google_play_links_in_html(content)
                if google_play_links:
                    print(f"        ✅ Has Google Play link: {google_play_links[0]}")
                    book_id = extract_google_play_id(google_play_links[0])
                    if book_id:
                        print(f"        🔍 Book ID: {book_id}")
                else:
                    print(f"        ⚠️  No Google Play link found")
            except:
                print(f"        ❌ Could not read file")
        
        if len(ebook_files) > 3:
            print(f"    ... and {len(ebook_files) - 3} more ebook files")
        
        print(f"\n🔍 DRY RUN COMPLETE")
        print(f"   Would process: {len(ebook_files) + len(audiobook_files)} HTML files")
        print(f"   Would attempt to fetch Google Play covers for each file")
        print(f"   Run without --dry-run to actually update the files")
        print(f"   Use --test-id <BOOK_ID> to test a specific book ID")
        
    else:
        print("🔄 Starting update process...")
        print("⚠️  This will take some time due to rate limiting...")
        print()
        
        # Update HTML files
        updated_count = update_all_html_files_with_google_play_covers(ebooks_dir, audiobooks_dir)
        print()
        
        print("✅ UPDATE COMPLETE")
        print(f"   All ebooks now use real Google Play cover images!")
        print(f"   Updated {updated_count} files successfully")

if __name__ == '__main__':
    main()
