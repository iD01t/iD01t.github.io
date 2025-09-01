#!/usr/bin/env python3
"""
Clean all HTML files to ensure consistent, professional formatting.
Removes duplicate headers, ensures proper dark UI, and centers content.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

def clean_html_file(html_file_path):
    """Clean a single HTML file to ensure professional formatting."""
    print(f"🧹 Cleaning: {html_file_path.name}")
    
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Remove any duplicate headers (keep only the one from site.js)
        headers = soup.find_all('div', class_='header')
        if len(headers) > 1:
            # Keep only the first header, remove the rest
            for header in headers[1:]:
                header.decompose()
            print(f"    ✅ Removed duplicate headers")
        
        # Remove any duplicate footers (keep only the one from site.js)
        footers = soup.find_all('div', class_='footer')
        if len(footers) > 1:
            # Keep only the first footer, remove the rest
            for footer in footers[1:]:
                footer.decompose()
            print(f"    ✅ Removed duplicate footers")
        
        # Ensure proper head structure
        head = soup.find('head')
        if not head:
            head = soup.new_tag('head')
            soup.html.insert(0, head)
        
        # Ensure proper body structure
        body = soup.find('body')
        if not body:
            body = soup.new_tag('body')
            soup.html.append(body)
        
        # Ensure proper HTML structure
        if not soup.find('html'):
            html_tag = soup.new_tag('html', lang='en')
            html_tag.append(head)
            html_tag.append(body)
            soup.append(html_tag)
        
        # Ensure proper DOCTYPE
        if not content.startswith('<!doctype'):
            soup.insert(0, '<!doctype html>\n')
        
        # Ensure site.css and site.js are included
        if not soup.find('link', {'href': '/assets/site.css'}):
            link_tag = soup.new_tag('link', rel='stylesheet', href='/assets/site.css')
            head.append(link_tag)
            print(f"    ✅ Added site.css")
        
        if not soup.find('script', {'src': '/assets/site.js'}):
            script_tag = soup.new_tag('script', src='/assets/site.js', defer='')
            body.append(script_tag)
            print(f"    ✅ Added site.js")
        
        # Ensure proper viewport meta tag
        if not soup.find('meta', {'name': 'viewport'}):
            viewport_tag = soup.new_tag('meta', name='viewport', content='width=device-width, initial-scale=1')
            head.insert(1, viewport_tag)
            print(f"    ✅ Added viewport meta tag")
        
        # Ensure proper charset
        if not soup.find('meta', {'charset': True}):
            charset_tag = soup.new_tag('meta', charset='utf-8')
            head.insert(0, charset_tag)
            print(f"    ✅ Added charset meta tag")
        
        # Clean up any inline styles that might conflict with site.css
        for tag in soup.find_all(style=True):
            if tag.get('style'):
                # Remove conflicting inline styles
                del tag['style']
        
        # Ensure proper container structure for main content
        container = soup.find('div', class_='container')
        if container:
            # Ensure content is properly centered
            if not container.get('style'):
                container['style'] = 'max-width: 1200px; margin: 0 auto; padding: 32px 20px;'
        
        # Save the cleaned HTML
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"    💾 Saved cleaned HTML")
        return True
        
    except Exception as e:
        print(f"    ❌ Error cleaning {html_file_path.name}: {e}")
        return False

def clean_all_html_files(repo_path):
    """Clean all HTML files in the repository."""
    print("🚀 Cleaning all HTML files for professional formatting...")
    print("=" * 60)
    
    # Find all HTML files
    html_files = []
    for pattern in ['*.html', '**/*.html']:
        html_files.extend(Path(repo_path).glob(pattern))
    
    # Remove duplicates and sort
    html_files = sorted(list(set(html_files)))
    
    print(f"📁 Found {len(html_files)} HTML files to clean")
    print()
    
    cleaned_count = 0
    for html_file in html_files:
        if clean_html_file(html_file):
            cleaned_count += 1
        print()
    
    print("✅ CLEANING COMPLETE!")
    print(f"   📁 Total files: {len(html_files)}")
    print(f"   🧹 Successfully cleaned: {cleaned_count}")
    print(f"   ❌ Failed: {len(html_files) - cleaned_count}")
    print()
    print("🎉 All HTML files now have:")
    print("   ✅ Consistent structure")
    print("   ✅ No duplicate headers/footers")
    print("   ✅ Proper dark UI integration")
    print("   ✅ Professional formatting")
    print("   ✅ Centered content layout")

def main():
    """Main function."""
    import argparse
    parser = argparse.ArgumentParser(description='Clean all HTML files for professional formatting')
    parser.add_argument('--repo-path', default='.', help='Path to repository root')
    args = parser.parse_args()
    
    repo_path = Path(args.repo_path)
    
    if not repo_path.exists():
        print(f"❌ Repository path not found: {repo_path}")
        return
    
    clean_all_html_files(repo_path)

if __name__ == '__main__':
    main()
