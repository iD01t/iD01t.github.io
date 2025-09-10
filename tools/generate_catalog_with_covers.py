#!/usr/bin/env python3
"""
Generate comprehensive catalog.json with real book covers for iD01t Productions website.
This script creates a catalog with real cover images from multiple sources.
"""

import os
import re
import json
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
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

def search_google_books_api(title, author="Guillaume Lessard"):
    """Search Google Books API for book covers."""
    try:
        # Clean the title for search
        search_query = f"{title} {author}".replace(':', '').replace('-', ' ').replace('_', ' ')
        search_query = re.sub(r'\s+', ' ', search_query).strip()
        
        # Google Books API endpoint (free, no key required)
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {'q': search_query}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                book = data['items'][0]
                if 'volumeInfo' in book and 'imageLinks' in book['volumeInfo']:
                    cover_url = book['volumeInfo']['imageLinks'].get('thumbnail', '')
                    if cover_url:
                        # Convert to high resolution
                        cover_url = cover_url.replace('zoom=1', 'zoom=3')
                        return cover_url
        
        return None
        
    except Exception as e:
        print(f"        ⚠️  Google Books API error: {str(e)[:50]}")
        return None

def search_open_library(title, author="Guillaume Lessard"):
    """Search Open Library for book covers."""
    try:
        # Clean the title for search
        search_query = f"{title} {author}".replace(':', '').replace('-', ' ').replace('_', ' ')
        search_query = re.sub(r'\s+', ' ', search_query).strip()
        
        # Open Library search endpoint
        url = "https://openlibrary.org/search.json"
        params = {'q': search_query}
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'docs' in data and len(data['docs']) > 0:
                book = data['docs'][0]
                if 'cover_i' in book:
                    cover_id = book['cover_i']
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
                    return cover_url
        
        return None
        
    except Exception as e:
        print(f"        ⚠️  Open Library error: {str(e)[:50]}")
        return None

def find_book_cover(title, author="Guillaume Lessard"):
    """Find book cover using multiple sources."""
    print(f"        🔍 Finding cover for: '{title}' by {author}")
    
    # Try Google Books API first (most reliable)
    cover_url = search_google_books_api(title, author)
    if cover_url:
        print(f"        ✅ Found via Google Books API: {cover_url}")
        return cover_url
    
    # Try Open Library as fallback
    cover_url = search_open_library(title, author)
    if cover_url:
        print(f"        ✅ Found via Open Library: {cover_url}")
        return cover_url
    
    print(f"        ❌ No cover found for: {title}")
    return None

def extract_book_info_from_html(html_file_path):
    """Extract book information from HTML file."""
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract title
        title = None
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text()
            title = title_text.replace(' · iD01t Productions', '').replace(' • iD01t Productions', '').strip()
        
        if not title:
            h1_tag = soup.find('h1')
            if h1_tag:
                title = h1_tag.get_text().strip()
        
        # Extract description
        description = ""
        meta_desc = soup.find('meta', {'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
        
        # Extract buy link
        buy_link = ""
        buy_elem = soup.find('a', href=re.compile(r'play\.google\.com|books\.apple\.com|amazon\.com'))
        if buy_elem:
            buy_link = buy_elem.get('href', '')
        
        # Extract existing image
        image = ""
        img = soup.find('img')
        if img:
            image = img.get('src', '')
        
        return {
            'title': title,
            'description': description,
            'author': 'Guillaume Lessard',
            'image': image,
            'link': buy_link or f"/ebooks/{html_file_path.stem}.html",
            'lang': 'EN'
        }
        
    except Exception as e:
        print(f"        ❌ Error extracting info from {html_file_path.name}: {e}")
        return None

def generate_comprehensive_catalog(ebooks_dir, audiobooks_dir, output_file):
    """Generate comprehensive catalog with real covers."""
    print("🚀 Generating comprehensive catalog with real book covers...")
    print("=" * 70)
    
    catalog = {
        'ebooks': [],
        'audiobooks': [],
        'series': []
    }
    
    # Process ebooks
    print("📚 Processing ebooks...")
    ebook_files = list(ebooks_dir.glob('*.html'))
    
    for i, html_file in enumerate(ebook_files, 1):
        print(f"    📖 [{i}/{len(ebook_files)}] Processing: {html_file.name}")
        
        book_info = extract_book_info_from_html(html_file)
        if not book_info or not book_info['title']:
            continue
        
        # Try to find a real cover
        real_cover = find_book_cover(book_info['title'], book_info['author'])
        if real_cover:
            book_info['image'] = real_cover
            print(f"        🎨 Updated with real cover")
        else:
            print(f"        ⚠️  Using existing image: {book_info['image']}")
        
        catalog['ebooks'].append(book_info)
        
        # Add delay to be respectful
        time.sleep(1)
    
    
    # Add some series (you can customize this)
    catalog['series'] = [
        {
            'title': 'Python Academy Series',
            'description': 'Complete Python learning series from beginner to advanced',
            'author': 'Guillaume Lessard',
            'image': '/assets/images/python-academy-series.webp',
            'link': '/series.html',
            'lang': 'EN'
        },
        {
            'title': 'Chess Mastery Collection',
            'description': 'Comprehensive chess strategy and tactics series',
            'author': 'Guillaume Lessard',
            'image': '/assets/images/chess-mastery-series.webp',
            'link': '/series.html',
            'lang': 'EN'
        }
    ]
    
    # Save the catalog
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ CATALOG GENERATED SUCCESSFULLY!")
        print(f"   📁 Output file: {output_file}")
        print(f"   📚 Ebooks: {len(catalog['ebooks'])}")
        print(f"   🎧 Audiobooks: {len(catalog['audiobooks'])}")
        print(f"   📚 Series: {len(catalog['series'])}")
        print(f"   🎨 Real covers found: {sum(1 for book in catalog['ebooks'] + catalog['audiobooks'] if book['image'] and not book['image'].startswith('/assets/'))}")
        
        return catalog
        
    except Exception as e:
        print(f"❌ Failed to save catalog: {e}")
        return None

def main():
    """Main function."""
    import argparse
    parser = argparse.ArgumentParser(description='Generate comprehensive catalog with real book covers')
    parser.add_argument('--output', default='assets/catalog.json', help='Output catalog file path')
    parser.add_argument('--repo-path', default='.', help='Path to repository root')
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    ebooks_dir = repo_path / 'ebooks'
    audiobooks_dir = repo_path / 'audiobooks'
    output_file = repo_path / args.output
    
    if not ebooks_dir.exists():
        print(f"❌ Ebooks directory not found: {ebooks_dir}")
        return
    
    if not audiobooks_dir.exists():
        print(f"❌ Audiobooks directory not found: {audiobooks_dir}")
        return
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Generate catalog
    catalog = generate_comprehensive_catalog(ebooks_dir, audiobooks_dir, output_file)
    
    if catalog:
        print(f"\n🎉 Catalog generation complete!")
        print(f"   The catalog is now ready to use with your website.")
        print(f"   All pages using data-catalog attributes will automatically display these items.")

if __name__ == '__main__':
    main()
