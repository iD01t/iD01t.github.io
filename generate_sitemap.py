#!/usr/bin/env python3
"""
Sitemap Generator for iD01t Productions
Version: 2.0.0
Generates sitemap.xml from all HTML files in the project
"""

import os
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

# Configuration
BASE_URL = "https://id01t.github.io"
SITE_ROOT = Path(__file__).parent
OUTPUT_FILE = SITE_ROOT / "sitemap.xml"

# Priority rules
PRIORITY_RULES = {
    'index.html': 1.0,
    'store.html': 0.9,
    'apps.html': 0.9,
    'games.html': 0.9,
    'ebooks.html': 0.9,
    'audiobooks.html': 0.9,
    'music.html': 0.9,
    'blog.html': 0.8,
    'about.html': 0.8,
    'contact.html': 0.8,
    'nini.html': 0.7,
}

# Directories to exclude
EXCLUDE_DIRS = {'includes', 'node_modules', '.git', '__pycache__', 'assets', 'css', 'js'}

# Files to exclude
EXCLUDE_FILES = {'404.html', 'third.html', 'thankyou.html', 'help.html', 'htmlhelp.html', 'html2.html'}

# Change frequency rules
CHANGEFREQ_RULES = {
    'index.html': 'weekly',
    'blog.html': 'weekly',
    'store.html': 'daily',
}

def get_priority(file_path):
    """Determine priority based on file path"""
    filename = file_path.name

    # Check specific file rules
    if filename in PRIORITY_RULES:
        return PRIORITY_RULES[filename]

    # Category pages
    if 'blog' in str(file_path):
        return 0.7
    if 'ebooks' in str(file_path) or 'audiobooks' in str(file_path):
        return 0.6
    if 'legal' in str(file_path):
        return 0.5
    if 'landing_pages' in str(file_path):
        return 0.6

    # Default
    return 0.5

def get_changefreq(file_path):
    """Determine change frequency based on file path"""
    filename = file_path.name

    # Check specific file rules
    if filename in CHANGEFREQ_RULES:
        return CHANGEFREQ_RULES[filename]

    # Category-based rules
    if 'blog' in str(file_path):
        return 'weekly'
    if 'legal' in str(file_path):
        return 'yearly'
    if 'ebooks' in str(file_path) or 'audiobooks' in str(file_path):
        return 'monthly'

    # Default
    return 'monthly'

def should_exclude(file_path):
    """Check if file should be excluded from sitemap"""
    # Check if in excluded directory
    for part in file_path.parts:
        if part in EXCLUDE_DIRS:
            return True

    # Check if excluded file
    if file_path.name in EXCLUDE_FILES:
        return True

    # Exclude old versions
    if '_old' in file_path.name or 'old_' in file_path.name:
        return True

    return False

def get_url_from_path(file_path, site_root):
    """Convert file path to URL"""
    rel_path = file_path.relative_to(site_root)
    url_path = str(rel_path).replace('\\', '/')

    # Handle index.html specially
    if url_path == 'index.html':
        return f"{BASE_URL}/"

    return f"{BASE_URL}/{url_path}"

def get_last_modified(file_path):
    """Get last modified date in ISO format"""
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')

def generate_sitemap():
    """Generate sitemap.xml from all HTML files"""
    print(f"Generating sitemap for: {SITE_ROOT}")
    print(f"Base URL: {BASE_URL}")

    # Create XML root
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation',
               'http://www.sitemaps.org/schemas/sitemap/0.9 '
               'http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')

    # Find all HTML files
    html_files = []
    for html_file in SITE_ROOT.rglob('*.html'):
        if not should_exclude(html_file):
            html_files.append(html_file)

    # Sort files (homepage first, then alphabetically)
    html_files.sort(key=lambda x: (x.name != 'index.html', str(x)))

    print(f"Found {len(html_files)} HTML files to include")

    # Add URLs to sitemap
    for html_file in html_files:
        url_elem = ET.SubElement(urlset, 'url')

        # loc
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = get_url_from_path(html_file, SITE_ROOT)

        # lastmod
        lastmod = ET.SubElement(url_elem, 'lastmod')
        lastmod.text = get_last_modified(html_file)

        # changefreq
        changefreq = ET.SubElement(url_elem, 'changefreq')
        changefreq.text = get_changefreq(html_file)

        # priority
        priority = ET.SubElement(url_elem, 'priority')
        priority.text = str(get_priority(html_file))

    # Create tree and write to file
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space='  ', level=0)  # Pretty print (Python 3.9+)

    # Write with XML declaration
    with open(OUTPUT_FILE, 'wb') as f:
        tree.write(f, encoding='utf-8', xml_declaration=True)

    print(f"\nSitemap generated successfully: {OUTPUT_FILE}")
    print(f"Total URLs: {len(html_files)}")

    # Show sample URLs
    print("\nSample URLs (first 10):")
    root = tree.getroot()
    for i, url in enumerate(root.findall('url')[:10]):
        loc = url.find('loc').text
        priority = url.find('priority').text
        print(f"  {i+1}. {loc} (priority: {priority})")

    return len(html_files)

if __name__ == '__main__':
    try:
        count = generate_sitemap()
        print(f"\n✅ Success! Generated sitemap with {count} URLs")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
