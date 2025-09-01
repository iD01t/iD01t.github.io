#!/usr/bin/env python3
"""
Ebook updater tool for iD01t Productions website.
Updates all ebook HTML files to use shared assets and consistent structure.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def clean_html_content(html_content):
    """Clean HTML content by removing HTML entities and fixing formatting."""
    # Remove HTML entities
    html_content = html_content.replace('&lt;', '<')
    html_content = html_content.replace('&gt;', '>')
    html_content = html_content.replace('&amp;', '&')
    html_content = html_content.replace('&#39;', "'")
    
    # Fix common formatting issues
    html_content = html_content.replace('<p><p>', '<p>')
    html_content = html_content.replace('</p></p>', '</p>')
    
    return html_content

def extract_book_info(html_content):
    """Extract book information from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract title
    title_elem = soup.find('title')
    title = title_elem.get_text().replace(' · iD01t Productions', '').strip() if title_elem else 'Unknown Title'
    
    # Extract description
    desc_elem = soup.find('meta', {'name': 'description'})
    description = desc_elem.get('content', '') if desc_elem else ''
    description = clean_html_content(description)
    
    # Extract author (try to find it in the content)
    author = 'Guillaume Lessard'  # Default author
    
    # Extract image path
    img_elem = soup.find('img')
    image_path = img_elem.get('src', '') if img_elem else ''
    
    # Extract buy link
    buy_link = ''
    buy_elem = soup.find('a', href=re.compile(r'play\.google\.com|books\.apple\.com'))
    if buy_elem:
        buy_link = buy_elem.get('href', '')
    
    return {
        'title': title,
        'description': description,
        'author': author,
        'image_path': image_path,
        'buy_link': buy_link
    }

def create_ebook_template(book_info):
    """Create a standardized ebook HTML template."""
    title = book_info['title']
    description = book_info['description']
    author = book_info['author']
    image_path = book_info['image_path']
    buy_link = book_info['buy_link']
    
    # Clean up description for meta tags
    meta_description = description[:160] + '...' if len(description) > 160 else description
    meta_description = re.sub(r'<[^>]+>', '', meta_description)  # Remove HTML tags
    
    template = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · iD01t Productions</title>
<meta name="description" content="{meta_description}">
<link rel="canonical" href="/ebooks/{title.lower().replace(' ', '-').replace('·', '').replace(':', '').replace('(', '').replace(')', '').replace('&', 'and')}.html">
<meta property="og:type" content="website">
<meta property="og:title" content="{title} · iD01t Productions">
<meta property="og:description" content="{meta_description}">
<meta property="og:image" content="{image_path}">
<meta property="og:url" content="/ebooks/{title.lower().replace(' ', '-').replace('·', '').replace(':', '').replace('(', '').replace(')', '').replace('&', 'and')}.html">
<link rel="stylesheet" href="/assets/site.css">
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CHX65WY0WZ"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', 'G-CHX65WY0WZ');
</script>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GT-M39S87SN');</script>
<!-- End Google Tag Manager -->
<script type="application/ld+json">
{{"@context": "http://schema.org", "@type": "Book", "name": "{title}", "author": {{"@type": "Person", "name": "{author}"}}, "image": "{image_path}", "description": "{meta_description}", "url": "/ebooks/{title.lower().replace(' ', '-').replace('·', '').replace(':', '').replace('(', '').replace(')', '').replace('&', 'and')}.html"}}
</script>
</head>
<body data-active="eBooks">
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GT-M39S87SN"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

<div class="container">
  <article>
    <div style="display:grid;grid-template-columns:240px 1fr;gap:20px;align-items:start">
      <div><img src="{image_path}" alt="{title} cover" style="width:100%;border-radius:10px;"></div>
      <div>
        <h1>{title}</h1>
        <div class="meta">By {author}</div>
        <div style="margin-top:12px">
          {description}
        </div>'''
    
    if buy_link:
        template += f'''
        <div style="margin:12px 0">
          <a href="{buy_link}" target="_blank" rel="noopener" class="btn">Buy Now</a>
        </div>'''
    
    template += '''
      </div>
    </div>
  </article>
</div>

<script src="/assets/site.js" defer></script>
</body></html>'''
    
    return template

def update_ebook_file(ebook_path, dry_run=False):
    """Update a single ebook file with the new template."""
    print(f"📚 Processing: {ebook_path}")
    
    try:
        with open(ebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract book information
        book_info = extract_book_info(content)
        
        # Create new template
        new_content = create_ebook_template(book_info)
        
        if dry_run:
            print(f"    [DRY RUN] Would update: {book_info['title']}")
            return False
        
        # Write updated content
        with open(ebook_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"    ✅ Updated: {book_info['title']}")
        return True
        
    except Exception as e:
        print(f"    ❌ Error processing {ebook_path}: {e}")
        return False

def main():
    """Main function to update all ebooks."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update all ebooks with shared structure')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--repo-path', default='.', help='Path to repository root')
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    ebooks_dir = repo_path / 'ebooks'
    
    if not ebooks_dir.exists():
        print(f"❌ Ebooks directory not found: {ebooks_dir}")
        return
    
    html_files = list(ebooks_dir.glob('*.html'))
    print(f"🔍 Found {len(html_files)} ebook files")
    
    updated_count = 0
    for html_file in html_files:
        if update_ebook_file(html_file, args.dry_run):
            updated_count += 1
    
    if args.dry_run:
        print(f"\n🔍 DRY RUN COMPLETE")
        print(f"   Would update: {len(html_files)} ebooks")
    else:
        print(f"\n✅ COMPLETE")
        print(f"   Updated: {updated_count} ebooks")
        print(f"   Total: {len(html_files)} ebooks")

if __name__ == '__main__':
    main()
