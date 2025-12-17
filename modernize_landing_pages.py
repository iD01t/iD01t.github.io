#!/usr/bin/env python3
"""
Modernize Landing Pages Script
Bulletproofs all landing pages with SEO, accessibility, performance, and security
"""

import os
import re
from pathlib import Path
from html.parser import HTMLParser
import json

class LandingPageParser(HTMLParser):
    """Extract product data from existing landing pages"""
    def __init__(self):
        super().__init__()
        self.data = {
            'title': '',
            'description': '',
            'cover_image': '',
            'buy_url': '',
            'price': '',
            'language': 'EN',
            'product_type': 'ebook'
        }
        self.current_tag = None
        self.in_title = False
        self.in_description = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Extract title
        if tag == 'title':
            self.in_title = True

        # Extract meta description
        if tag == 'meta' and attrs_dict.get('name') == 'description':
            self.data['description'] = attrs_dict.get('content', '')[:160]

        # Extract cover image
        if tag == 'img' and 'cover' in attrs_dict.get('alt', '').lower():
            self.data['cover_image'] = attrs_dict.get('src', '')

        # Extract buy URL
        if tag == 'a' and 'play.google.com' in attrs_dict.get('href', ''):
            self.data['buy_url'] = attrs_dict.get('href', '')

    def handle_data(self, data):
        if self.in_title:
            # Extract product title from page title
            title_parts = data.split('·')
            if len(title_parts) > 0:
                self.data['title'] = title_parts[0].strip()

        # Look for price
        if data.strip().startswith('$'):
            self.data['price'] = data.strip()

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False


def create_landing_page_html(product_data, product_type):
    """Generate modern landing page HTML"""

    title = product_data.get('title', 'Product')
    description = product_data.get('description', '')[:160]
    cover_image = product_data.get('cover_image', '/assets/img/placeholders/card-portrait-384x576.webp')
    buy_url = product_data.get('buy_url', '#')
    price = product_data.get('price', '$4.99')
    language = product_data.get('language', 'EN')

    # Determine product type label
    product_label = 'Audiobook' if product_type == 'audiobook' else 'eBook'
    product_path = 'audiobooks' if product_type == 'audiobook' else 'ebooks'
    canonical_base = f'https://id01t.github.io/landing_pages_new/{product_path}/'

    # Create slug from title
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    canonical_url = canonical_base + slug + '.html'

    html = f'''<!DOCTYPE html>
<html class="scroll-smooth" lang="en">
<head>
  <!-- Essential Meta Tags -->
  <meta charset="utf-8"/>
  <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>

  <!-- SEO Meta Tags -->
  <title>{title} — {product_label} | iD01t Productions</title>
  <meta name="description" content="{description}"/>
  <meta name="keywords" content="{product_label.lower()}, {title.lower()}, programming, technology, books, digital products"/>
  <meta name="author" content="Guillaume Lessard"/>
  <meta name="robots" content="index,follow,max-image-preview:large"/>
  <meta name="theme-color" content="#2aa7ff"/>

  <!-- Canonical URL -->
  <link rel="canonical" href="{canonical_url}"/>

  <!-- Hreflang Tags -->
  <link rel="alternate" hreflang="en" href="{canonical_url}"/>
  <link rel="alternate" hreflang="x-default" href="{canonical_url}"/>

  <!-- Open Graph Tags -->
  <meta property="og:type" content="product"/>
  <meta property="og:site_name" content="iD01t Productions"/>
  <meta property="og:title" content="{title}"/>
  <meta property="og:description" content="{description}"/>
  <meta property="og:url" content="{canonical_url}"/>
  <meta property="og:image" content="{cover_image}"/>
  <meta property="og:image:width" content="600"/>
  <meta property="og:image:height" content="900"/>
  <meta property="og:locale" content="en_US"/>

  <!-- Twitter Card Tags -->
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:site" content="@id01t"/>
  <meta name="twitter:creator" content="@id01t"/>
  <meta name="twitter:title" content="{title}"/>
  <meta name="twitter:description" content="{description}"/>
  <meta name="twitter:image" content="{cover_image}"/>

  <!-- Preconnect to External Domains -->
  <link rel="preconnect" href="https://books.google.com" crossorigin="anonymous"/>
  <link rel="dns-prefetch" href="https://books.google.com"/>
  <link rel="preconnect" href="https://play.google.com" crossorigin="anonymous"/>
  <link rel="dns-prefetch" href="https://play.google.com"/>
  <link rel="preconnect" href="https://cdn.tailwindcss.com" crossorigin="anonymous"/>
  <link rel="dns-prefetch" href="https://cdn.tailwindcss.com"/>

  <!-- Favicons -->
  <link rel="icon" href="/favicon.ico"/>
  <link rel="apple-touch-icon" href="/apple-touch-icon.png"/>

  <!-- Structured Data - Product Schema -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "{'AudioBook' if product_type == 'audiobook' else 'Book'}",
    "name": "{title}",
    "description": "{description}",
    "image": "{cover_image}",
    "url": "{canonical_url}",
    "author": {{
      "@type": "Person",
      "name": "Guillaume Lessard"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "iD01t Productions",
      "url": "https://id01t.github.io/"
    }},
    "inLanguage": "{language.lower()}",
    "bookFormat": "{'AudiobookFormat' if product_type == 'audiobook' else 'EBook'}",
    "offers": {{
      "@type": "Offer",
      "price": "{price.replace('$', '')}",
      "priceCurrency": "USD",
      "availability": "https://schema.org/InStock",
      "url": "{buy_url}",
      "seller": {{
        "@type": "Organization",
        "name": "Google Play Books"
      }}
    }}
  }}
  </script>

  <!-- Structured Data - Breadcrumb -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://id01t.github.io/"
      }},
      {{
        "@type": "ListItem",
        "position": 2,
        "name": "{product_label}s",
        "item": "https://id01t.github.io/{product_path}.html"
      }},
      {{
        "@type": "ListItem",
        "position": 3,
        "name": "{title}",
        "item": "{canonical_url}"
      }}
    ]
  }}
  </script>

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com" crossorigin="anonymous"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#f5faff', 100: '#e0f2ff', 200: '#bae0ff', 300: '#8dceff', 400: '#5abaff',
              500: '#2aa7ff', 600: '#008ef6', 700: '#0070d7', 800: '#0057b5', 900: '#003f92'
            }}
          }}
        }}
      }}
    }}
  </script>

  <!-- Site Styles -->
  <link rel="stylesheet" href="/site.css"/>

  <style>
    /* Product page specific styles */
    .product-hero {{
      background: linear-gradient(135deg, #f5faff 0%, #e0f2ff 100%);
    }}

    @media (prefers-color-scheme: dark) {{
      .product-hero {{
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      }}
    }}
  </style>
</head>

<body class="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-sans antialiased">

  <!-- Skip to main content link -->
  <a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-brand-600 focus:text-white focus:rounded-lg">Skip to main content</a>

  <!-- Shared Header -->
  <script>
    fetch('/includes/header.html')
      .then(response => response.text())
      .then(html => {{
        const headerContainer = document.createElement('div');
        headerContainer.innerHTML = html;
        document.body.insertBefore(headerContainer.firstElementChild, document.body.firstChild);
      }})
      .catch(error => console.error('Error loading header:', error));
  </script>

  <!-- Main Content -->
  <main id="main" role="main">

    <!-- Breadcrumb -->
    <section class="bg-slate-50 dark:bg-slate-800/50 py-4">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav aria-label="Breadcrumb">
          <ol class="flex items-center gap-2 text-sm">
            <li><a href="/" class="text-slate-600 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 transition-colors">Home</a></li>
            <li><span class="text-slate-400">/</span></li>
            <li><a href="/{product_path}.html" class="text-slate-600 dark:text-slate-400 hover:text-brand-600 dark:hover:text-brand-400 transition-colors">{product_label}s</a></li>
            <li><span class="text-slate-400">/</span></li>
            <li aria-current="page" class="text-slate-900 dark:text-white font-medium">{title}</li>
          </ol>
        </nav>
      </div>
    </section>

    <!-- Product Hero -->
    <section class="product-hero py-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-2 gap-12 items-start">

          <!-- Product Image -->
          <div class="relative">
            <img
              src="{cover_image}"
              alt="{title} cover"
              class="w-full max-w-md mx-auto aspect-[2/3] object-cover rounded-2xl shadow-2xl"
              loading="eager"
              onerror="this.src='/assets/img/placeholders/card-portrait-384x576.webp'"
              width="600"
              height="900"
            />
            {'<div class="absolute top-4 right-4 bg-brand-600 text-white px-3 py-1.5 rounded-full text-sm font-medium flex items-center gap-2"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/></svg>Audiobook</div>' if product_type == 'audiobook' else ''}
          </div>

          <!-- Product Info -->
          <div class="space-y-6">
            <div>
              <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 mb-4">
                {product_label}
              </span>
              <h1 class="text-4xl md:text-5xl font-bold tracking-tight mb-4">{title}</h1>
              <p class="text-lg text-slate-600 dark:text-slate-300 leading-relaxed">{description}</p>
            </div>

            <!-- Author -->
            <div class="flex items-center gap-3 py-4 border-y border-slate-200 dark:border-slate-700">
              <svg class="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
              </svg>
              <div>
                <p class="text-sm text-slate-500 dark:text-slate-400">By</p>
                <p class="font-medium">Guillaume Lessard</p>
              </div>
            </div>

            <!-- Features -->
            <div class="grid grid-cols-2 gap-4">
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-brand-600 dark:text-brand-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                </svg>
                <div>
                  <p class="font-medium text-sm">Instant Access</p>
                  <p class="text-xs text-slate-500">{'Stream or download' if product_type == 'audiobook' else 'Download immediately'}</p>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-brand-600 dark:text-brand-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                </svg>
                <div>
                  <p class="font-medium text-sm">Lifetime Access</p>
                  <p class="text-xs text-slate-500">Read anytime, anywhere</p>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-brand-600 dark:text-brand-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                </svg>
                <div>
                  <p class="font-medium text-sm">{'HD Audio Quality' if product_type == 'audiobook' else 'Multiple Formats'}</p>
                  <p class="text-xs text-slate-500">{'Professional narration' if product_type == 'audiobook' else 'PDF, EPUB, and more'}</p>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-brand-600 dark:text-brand-400 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M5 13l4 4L19 7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                </svg>
                <div>
                  <p class="font-medium text-sm">Language: {language}</p>
                  <p class="text-xs text-slate-500">{'English' if language == 'EN' else 'French'}</p>
                </div>
              </div>
            </div>

            <!-- Price and CTA -->
            <div class="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-lg border border-slate-200 dark:border-slate-700">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <p class="text-sm text-slate-500 dark:text-slate-400">Price</p>
                  <p class="text-3xl font-bold text-brand-600 dark:text-brand-400">{price}</p>
                </div>
                <span class="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-sm font-medium rounded-full">
                  In Stock
                </span>
              </div>
              <a
                href="{buy_url}"
                target="_blank"
                rel="noopener noreferrer nofollow"
                class="block w-full px-6 py-4 bg-brand-600 hover:bg-brand-700 text-white text-center text-lg font-semibold rounded-xl transition-all hover:scale-105 focus-ring shadow-lg"
              >
                {'Listen Now on Google Play' if product_type == 'audiobook' else 'Buy Now on Google Play'}
              </a>
              <p class="text-xs text-center text-slate-500 dark:text-slate-400 mt-3">
                Secure checkout via Google Play Books
              </p>
            </div>

            <!-- Back Link -->
            <div class="pt-4">
              <a href="/{product_path}.html" class="inline-flex items-center gap-2 text-brand-600 dark:text-brand-400 hover:text-brand-700 dark:hover:text-brand-300 transition-colors">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                  <path d="M10 19l-7-7m0 0l7-7m-7 7h18" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
                </svg>
                Browse all {product_label}s
              </a>
            </div>
          </div>

        </div>
      </div>
    </section>

  </main>

  <!-- Shared Footer -->
  <script>
    fetch('/includes/footer.html')
      .then(response => response.text())
      .then(html => {{
        document.body.insertAdjacentHTML('beforeend', html);
      }})
      .catch(error => console.error('Error loading footer:', error));
  </script>

  <!-- Consent Banner -->
  <script>
    fetch('/includes/consent-banner.html')
      .then(response => response.text())
      .then(html => {{
        document.body.insertAdjacentHTML('beforeend', html);
      }})
      .catch(error => console.error('Error loading consent banner:', error));
  </script>

</body>
</html>
'''
    return html


def process_landing_page(file_path):
    """Process a single landing page file"""
    print(f"Processing: {file_path}")

    # Determine product type from path
    product_type = 'audiobook' if '/audiobooks/' in str(file_path) else 'ebook'

    # Read existing file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse product data
    parser = LandingPageParser()
    parser.feed(content)
    product_data = parser.data
    product_data['product_type'] = product_type

    # If we didn't extract data, try to get from filename and basic parsing
    if not product_data['title']:
        # Extract from filename
        filename = Path(file_path).stem
        product_data['title'] = filename.replace('-', ' ').title()

    # Generate new HTML
    new_html = create_landing_page_html(product_data, product_type)

    # Write updated file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"✓ Updated: {file_path}")
    return True


def main():
    """Main processing function"""
    landing_pages_dir = Path('/home/user/iD01t.github.io/landing_pages_new')

    # Find all HTML files
    html_files = list(landing_pages_dir.glob('**/*.html'))

    print(f"\nFound {len(html_files)} landing pages to modernize\n")
    print("="*60)

    success_count = 0
    for html_file in html_files:
        try:
            if process_landing_page(html_file):
                success_count += 1
        except Exception as e:
            print(f"✗ Error processing {html_file}: {e}")

    print("="*60)
    print(f"\nCompleted: {success_count}/{len(html_files)} landing pages modernized\n")


if __name__ == '__main__':
    main()
