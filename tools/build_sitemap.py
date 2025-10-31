#!/usr/bin/env python3
"""
Build sitemap.xml from catalog.json
Generates SEO-optimized sitemap for all catalog pages
"""

import json
import pathlib
import sys
from datetime import date
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / 'data' / 'catalog.json'
SITEMAP_PATH = ROOT / 'sitemap.xml'
BASE_URL = 'https://id01t.github.io'

def build_sitemap():
    """Generate sitemap.xml"""
    
    if not CATALOG_PATH.exists():
        print(f"❌ Error: catalog.json not found at {CATALOG_PATH}")
        print(f"   Run tools/build_catalog.py first")
        sys.exit(1)
    
    print(f"📖 Reading catalog from: {CATALOG_PATH}")
    
    with CATALOG_PATH.open('r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    if not catalog:
        print(f"❌ Error: Empty catalog")
        sys.exit(1)
    
    print(f"   Found {len(catalog)} items")
    
    today = date.today().isoformat()
    
    # Build URL list with priorities
    urls = [
        (f"{BASE_URL}/", '1.0', 'daily'),
        (f"{BASE_URL}/ebooks.html", '0.9', 'daily'),
        (f"{BASE_URL}/audiobooks.html", '0.9', 'daily'),
    ]
    
    # Add individual book pages
    for item in catalog:
        book_url = f"{BASE_URL}/book.html?id={quote(item['id'])}"
        # Higher priority for newer books
        priority = '0.8' if item.get('date', '') > '2024-01-01' else '0.7'
        urls.append((book_url, priority, 'weekly'))
    
    # Build XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    
    for loc, priority, changefreq in urls:
        xml_lines.extend([
            '  <url>',
            f'    <loc>{loc}</loc>',
            f'    <lastmod>{today}</lastmod>',
            f'    <changefreq>{changefreq}</changefreq>',
            f'    <priority>{priority}</priority>',
            '  </url>',
        ])
    
    xml_lines.append('</urlset>')
    
    # Write sitemap
    sitemap_content = '\n'.join(xml_lines)
    SITEMAP_PATH.write_text(sitemap_content, encoding='utf-8')
    
    print(f"✅ Successfully generated sitemap with {len(urls)} URLs")
    print(f"📝 Wrote sitemap to: {SITEMAP_PATH}")
    print(f"\n📊 Sitemap Statistics:")
    print(f"   • Main pages: 3")
    print(f"   • eBook pages: {sum(1 for x in catalog if x['format'] == 'eBook')}")
    print(f"   • Audiobook pages: {sum(1 for x in catalog if x['format'] == 'Audiobook')}")
    print(f"   • Total URLs: {len(urls)}")

if __name__ == '__main__':
    try:
        build_sitemap()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
