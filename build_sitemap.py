#!/usr/bin/env python3
"""
Build sitemap.xml from catalog.json
Generates sitemap with all pages and book detail URLs
"""

import json
import pathlib
import datetime
import urllib.parse
import sys

def build_sitemap():
    """Generate sitemap.xml from catalog"""
    # Paths
    root = pathlib.Path(__file__).resolve().parents[1]
    catalog_path = root / 'data' / 'catalog.json'
    sitemap_path = root / 'sitemap.xml'
    
    base_url = 'https://id01t.github.io'
    
    if not catalog_path.exists():
        print(f"❌ Catalog file not found: {catalog_path}", file=sys.stderr)
        print("   Run build_catalog.py first to generate the catalog.")
        sys.exit(1)
    
    print(f"📖 Reading catalog from: {catalog_path}")
    
    try:
        with catalog_path.open('r', encoding='utf-8') as f:
            catalog = json.load(f)
        
        # Build URL list with priorities
        urls = [
            (f"{base_url}/", '1.0'),
            (f"{base_url}/ebooks.html", '0.9'),
            (f"{base_url}/audiobooks.html", '0.9'),
        ]
        
        # Add all book detail pages
        for item in catalog:
            book_id = urllib.parse.quote(item['id'])
            urls.append((f"{base_url}/book.html?id={book_id}", '0.8'))
        
        # Get current date for lastmod
        today = datetime.date.today().isoformat()
        
        # Build XML
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        ]
        
        for loc, priority in urls:
            lines.extend([
                '  <url>',
                f'    <loc>{loc}</loc>',
                f'    <lastmod>{today}</lastmod>',
                f'    <priority>{priority}</priority>',
                '  </url>'
            ])
        
        lines.append('</urlset>')
        
        # Write sitemap
        with sitemap_path.open('w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Successfully wrote {len(urls)} URLs to: {sitemap_path}")
        print(f"   🌐 Base URL: {base_url}")
        print(f"   📚 Book pages: {len(catalog)}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error building sitemap: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(build_sitemap())
