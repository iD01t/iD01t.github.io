#!/usr/bin/env python3
"""
Upgrade Audiobook Individual Landing Pages to Professional Standard
This script applies the same professional header/footer design from the ebooks.html
and individual eBook pages to all audiobook landing pages.
"""

import os
import re
from pathlib import Path

def create_professional_audiobook_template(title, author, description, image_path, buy_link, language="EN"):
    """Create professional audiobook page template matching ebooks structure"""
    
    # Clean up for URL and meta tags
    slug = re.sub(r'[^\w\s-]', '', title.lower()).replace(' ', '-').replace('--', '-').strip('-')
    meta_description = re.sub(r'<[^>]+>', '', description)[:160] + ('...' if len(description) > 160 else '')
    
    # Ensure proper image path
    if not image_path.startswith('/'):
        image_path = f"/assets/harvested/ebooks/{image_path}" if not image_path.startswith('/assets') else image_path
    
    template = f'''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} (Audiobook) · iD01t Productions</title>
    <meta name="description" content="{meta_description}">
    
    <!-- Tailwind (CDN) -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Early theme init to avoid FOUC -->
    <script>(function(){{try{{var s=localStorage.getItem('theme');var d=window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches; if(s==='dark'||(!s&&d)){{document.documentElement.classList.add('dark');}}}}catch(e){{}}}})();</script>
    
    <script>
      /* Extend Tailwind with brand palette */
      tailwind.config = {{
        theme: {{
          extend: {{
            colors: {{
              brand: {{
                50:  '#f5faff',
                100: '#e0f2ff',
                200: '#bae0ff',
                300: '#8dceff',
                400: '#5abaff',
                500: '#2aa7ff',
                600: '#008ef6',
                700: '#0070d7',
                800: '#0057b5',
                900: '#003f92'
              }}
            }},
            keyframes: {{
              bounceSubtle: {{
                '0%,100%': {{ transform: 'translateY(0)' }},
                '50%': {{ transform: 'translateY(-4px)' }}
              }},
              pulseGlow: {{
                '0%,100%': {{ opacity: 0.2 }},
                '50%': {{ opacity: 0.4 }}
              }},
              float: {{
                '0%,100%': {{ transform: 'translateY(0)' }},
                '50%': {{ transform: 'translateY(-6px)' }}
              }}
            }},
            animation: {{
              'bounce-subtle': 'bounceSubtle 1.4s ease-in-out infinite',
              'pulse-glow': 'pulseGlow 2.4s ease-in-out infinite',
              float: 'float 6s ease-in-out infinite'
            }}
          }}
        }}
      }};
    </script>

    <!-- Custom utility classes -->
    <style>
      :root {{
        --ring-color: theme('colors.brand.500');
      }}
      /* underline utility */
      .link-underline {{
        position: relative;
        transition: color 0.2s;
      }}
      .link-underline::after {{
        content: '';
        position: absolute;
        left: 0;
        bottom: -1px;
        width: 100%;
        height: 1px;
        background: currentColor;
        transform: scaleX(0);
        transform-origin: right;
        transition: transform 0.2s ease-out;
      }}
      .link-underline:hover::after,
      .link-underline:focus-visible::after {{
        transform: scaleX(1);
        transform-origin: left;
      }}
      /* focus ring */
      .focus-ring:focus-visible {{
        outline: 2px solid var(--ring-color);
        outline-offset: 2px;
      }}
      /* gradient text */
      .gradient-text {{
        background: linear-gradient(to right, #2aa7ff, #0070d7);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        color: transparent; /* fallback to ensure visibility */
      }}
      /* card hover lift */
      .card-hover {{
        transition: transform 0.4s ease, box-shadow 0.4s ease;
      }}
      .card-hover:hover {{
        transform: translateY(-6px);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15);
      }}
      /* glass effect */
      .glass-effect {{
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(12px) saturate(150%);
      }}
      @media (prefers-color-scheme: dark) {{
        .glass-effect {{
          background: rgba(30, 41, 59, 0.55);
        }}
      }}
      /* intersection animations */
      .intersection-animate {{
        opacity: 0;
        transform: translateY(20px);
        transition: all 0.6s cubic-bezier(0.22, 1, 0.36, 1);
      }}
      .intersection-animate.visible {{
        opacity: 1;
        transform: translateY(0);
      }}
    </style>

    <!-- Favicons -->
    <link rel="icon" href="/favicon.ico" />
    <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
    <link rel="manifest" href="/site.webmanifest" />

    <link rel="canonical" href="https://id01t.store/audiobooks/{slug}.html">
    <meta property="og:type" content="audiobook">
    <meta property="og:title" content="{title} (Audiobook)">
    <meta property="og:description" content="{meta_description}">
    <meta property="og:url" content="https://id01t.store/audiobooks/{slug}.html">
    <meta property="og:image" content="{image_path}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title} (Audiobook)">
    <meta name="twitter:description" content="{meta_description}">
    <meta name="twitter:image" content="{image_path}">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Audiobook",
      "name": "{title}",
      "author": {{
        "@type": "Person",
        "name": "{author}"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "iD01t Productions",
        "url": "https://id01t.store"
      }},
      "description": "{meta_description}",
      "image": "{image_path}",
      "url": "https://id01t.store/audiobooks/{slug}.html",
      "inLanguage": "{language.lower()}",
      "bookFormat": "AudiobookFormat"
    }}
    </script>
</head>
<body class="bg-white text-slate-800 dark:bg-slate-950 dark:text-slate-100">

<!-- Header (Professional Design) -->
<header class="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 backdrop-blur border-b border-slate-200 dark:border-slate-800">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div class="flex items-center justify-between h-16">
      <!-- Logo -->
      <a href="/" class="flex items-center gap-2 focus-ring" aria-label="iD01t Productions home">
        <img src="/assets/img/brand/logo.svg" alt="iD01t Productions logo" class="h-8 w-8" />
        <span class="font-semibold text-lg hidden sm:inline">iD01t Productions</span>
      </a>

      <!-- Desktop nav -->
      <nav class="hidden md:flex items-center gap-6" aria-label="Primary navigation">
        <a href="/store.html" class="link-underline focus-ring rounded px-2 py-1">Store</a>
        <a href="/ebooks.html" class="link-underline focus-ring rounded px-2 py-1">eBooks</a>
        <a href="/audiobooks.html" class="link-underline focus-ring rounded px-2 py-1 text-blue-600 dark:text-blue-400">Audiobooks</a>
        <a href="/apps.html" class="link-underline focus-ring rounded px-2 py-1">Apps</a>
        <a href="/games.html" class="link-underline focus-ring rounded px-2 py-1">Games</a>
        <a href="/music.html" class="link-underline focus-ring rounded px-2 py-1">Music</a>
        <a href="/blog.html" class="link-underline focus-ring rounded px-2 py-1">Blog</a>
        <a href="/about.html" class="link-underline focus-ring rounded px-2 py-1">About</a>
        <a href="/contact.html" class="link-underline focus-ring rounded px-2 py-1">Contact</a>
      </nav>

      <!-- Actions -->
      <div class="flex items-center gap-3">
        <button id="themeToggle" class="focus-ring rounded-full border border-slate-300 dark:border-slate-700 px-3 py-1 text-sm hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" aria-label="Toggle theme">
          <span class="theme-text">Theme</span>
        </button>
        <a href="/#newsletter" class="inline-flex items-center rounded-full bg-brand-600 hover:bg-brand-700 text-white text-sm px-4 py-2 transition-all duration-300 hover:scale-105 animate-pulse-glow focus-ring">
          Newsletter
        </a>
        <button id="mobileMenuBtn" class="md:hidden focus-ring inline-flex items-center justify-center p-2 rounded-lg border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors" aria-label="Open navigation menu" aria-expanded="false">
          <svg id="menuIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-5 w-5 transition-transform" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 6h18M3 12h18M3 18h18" />
          </svg>
          <svg id="closeIcon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="h-5 w-5 hidden transition-transform" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M6 6l12 12M6 18L18 6" />
          </svg>
        </button>
      </div>
    </div>
  </div>

  <!-- Mobile menu -->
  <div id="mobileMenu" class="md:hidden hidden border-t border-slate-200 dark:border-slate-800 glass-effect" role="dialog" aria-modal="true" aria-labelledby="mobile-menu-title">
    <div class="px-4 py-3 flex flex-col gap-2">
      <h2 id="mobile-menu-title" class="sr-only">Navigation Menu</h2>
      <a href="/store.html" class="py-2 px-2 rounded focus-ring">Store</a>
      <a href="/ebooks.html" class="py-2 px-2 rounded focus-ring">eBooks</a>
      <a href="/audiobooks.html" class="py-2 px-2 rounded focus-ring text-blue-600 dark:text-blue-400">Audiobooks</a>
      <a href="/apps.html" class="py-2 px-2 rounded focus-ring">Apps</a>
      <a href="/games.html" class="py-2 px-2 rounded focus-ring">Games</a>
      <a href="/music.html" class="py-2 px-2 rounded focus-ring">Music</a>
      <a href="/blog.html" class="py-2 px-2 rounded focus-ring">Blog</a>
      <a href="/about.html" class="py-2 px-2 rounded focus-ring">About</a>
      <a href="/contact.html" class="py-2 px-2 rounded focus-ring">Contact</a>
    </div>
  </div>
</header>

<!-- Main Content -->
<section class="relative overflow-hidden">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-12 pb-10">
    <nav class="text-sm text-slate-500 mb-4">
      <a class="link-underline" href="/">Home</a> › 
      <a class="link-underline" href="/audiobooks.html">Audiobooks</a> › 
      <span>{title}</span>
    </nav>
    
    <div class="grid md:grid-cols-2 gap-8 items-start">
      <img src="{image_path}" 
           alt="{title} audiobook cover" 
           class="w-full aspect-[3/4] object-cover rounded-2xl ring-1 ring-slate-200 dark:ring-slate-800" 
           loading="eager"
           onerror="this.onerror=null;this.src='/assets/img/placeholders/card-portrait-384x576.webp'">
      
      <div>
        <div class="flex items-center gap-2 mb-3">
          <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 text-sm font-medium">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.369 4.369 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z"/>
            </svg>
            Audiobook
          </span>
        </div>
        
        <h1 class="text-3xl font-bold tracking-tight mb-3">{title}</h1>
        
        <p class="text-slate-600 dark:text-slate-300 mb-4">
          <span class="font-medium">Narrated by:</span> {author}
        </p>
        
        <div class="prose prose-slate dark:prose-invert max-w-none mb-6">
          <p>{description}</p>
        </div>
        
        <div class="flex items-center gap-3 mb-4">
          <a href="{buy_link}" 
             target="_blank" 
             rel="noopener" 
             class="inline-flex items-center gap-2 rounded-full bg-brand-600 hover:bg-brand-700 text-white px-6 py-3 font-medium transition-all duration-300 hover:scale-105 focus-ring">
            <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z"/>
            </svg>
            Listen Now
          </a>
          <a href="/audiobooks.html" 
             class="inline-flex items-center rounded-full border border-slate-300 dark:border-slate-700 px-6 py-3 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors focus-ring">
            All Audiobooks
          </a>
        </div>
        
        <ul class="text-sm text-slate-500 space-y-1">
          <li><span class="font-medium">Language:</span> {language}</li>
          <li><span class="font-medium">Format:</span> Digital Audiobook</li>
          <li><span class="font-medium">Publisher:</span> iD01t Productions</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- Professional Footer -->
<footer class="mt-24 bg-slate-900 text-slate-300 py-16">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid md:grid-cols-4 gap-12">
    <div class="space-y-4">
      <a href="/" class="flex items-center gap-2 focus-ring" aria-label="iD01t Productions home">
        <img src="/assets/img/brand/logo.svg" alt="iD01t Productions logo" class="h-8 w-8" />
        <span class="font-semibold text-lg text-white">iD01t Productions</span>
      </a>
      <p class="text-sm">Professional digital tools and creative content for developers, creators, and innovators worldwide.</p>
    </div>

    <div>
      <h3 class="font-semibold text-white mb-4">Products</h3>
      <ul class="space-y-2 text-sm">
        <li><a href="/apps.html" class="hover:text-white transition-colors focus-ring rounded">Windows Apps</a></li>
        <li><a href="/ebooks.html" class="hover:text-white transition-colors focus-ring rounded">Technical eBooks</a></li>
        <li><a href="/audiobooks.html" class="hover:text-white transition-colors focus-ring rounded">Audiobooks</a></li>
        <li><a href="/games.html" class="hover:text-white transition-colors focus-ring rounded">Online Games</a></li>
        <li><a href="/music.html" class="hover:text-white transition-colors focus-ring rounded">Original Music</a></li>
      </ul>
    </div>

    <div>
      <h3 class="font-semibold text-white mb-4">Resources</h3>
      <ul class="space-y-2 text-sm">
        <li><a href="/blog.html" class="hover:text-white transition-colors focus-ring rounded">Blog & Guides</a></li>
        <li><a href="/store.html" class="hover:text-white transition-colors focus-ring rounded">Store</a></li>
        <li><a href="/about.html" class="hover:text-white transition-colors focus-ring rounded">About Us</a></li>
        <li><a href="/contact.html" class="hover:text-white transition-colors focus-ring rounded">Contact</a></li>
        <li><a href="/#newsletter" class="hover:text-white transition-colors focus-ring rounded">Newsletter</a></li>
      </ul>
    </div>

    <div>
      <h3 class="font-semibold text-white mb-4">Legal</h3>
      <ul class="space-y-2 text-sm">
        <li><a href="/legal/terms.html" class="hover:text-white transition-colors focus-ring rounded">Terms of Service</a></li>
        <li><a href="/legal/privacy.html" class="hover:text-white transition-colors focus-ring rounded">Privacy Policy</a></li>
        <li><a href="/legal/refunds.html" class="hover:text-white transition-colors focus-ring rounded">Refund Policy</a></li>
      </ul>
    </div>
  </div>

  <!-- Bottom -->
  <div class="pt-8 border-t border-slate-800 mt-12 px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4 text-sm">
    <p class="text-slate-400">© <span id="year"></span> iD01t Productions. All rights reserved.</p>
    <div class="flex items-center gap-6">
      <span class="flex items-center gap-2">
        <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        <span class="text-slate-400">All systems operational</span>
      </span>
      <a href="/legal/terms.html" class="hover:text-white transition-colors focus-ring rounded">Terms</a>
      <a href="/legal/privacy.html" class="hover:text-white transition-colors focus-ring rounded">Privacy</a>
    </div>
  </div>
</footer>

<!-- JavaScript -->
<script>
  // Theme functionality
  function initTheme() {{
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = savedTheme === 'dark' || (!savedTheme && prefersDark);
    
    if (isDark) {{
      document.documentElement.classList.add('dark');
    }} else {{
      document.documentElement.classList.remove('dark');
    }}
    
    return isDark;
  }}
  
  // Initialize theme on page load
  const currentTheme = initTheme();
  
  // Theme toggle functionality
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {{
    const themeText = themeToggle.querySelector('.theme-text');
    
    function updateThemeText() {{
      const isDark = document.documentElement.classList.contains('dark');
      themeText.textContent = isDark ? 'Light' : 'Dark';
    }}
    
    updateThemeText();
    
    themeToggle.addEventListener('click', function() {{
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('theme', isDark ? 'dark' : 'light');
      updateThemeText();
    }});
  }}
  
  // Mobile menu functionality
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const mobileMenu = document.getElementById('mobileMenu');
  const menuIcon = document.getElementById('menuIcon');
  const closeIcon = document.getElementById('closeIcon');
  
  if (mobileMenuBtn && mobileMenu) {{
    mobileMenuBtn.addEventListener('click', function() {{
      const isOpen = !mobileMenu.classList.contains('hidden');
      
      mobileMenu.classList.toggle('hidden');
      menuIcon.classList.toggle('hidden', !isOpen);
      closeIcon.classList.toggle('hidden', isOpen);
      mobileMenuBtn.setAttribute('aria-expanded', String(!isOpen));
    }});
  }}
  
  // Set current year
  document.getElementById('year').textContent = new Date().getFullYear();
</script>

</body>
</html>'''
    
    return template

def extract_audiobook_info(html_content, filename):
    """Extract audiobook information from existing HTML content"""
    
    # Extract title
    title_match = re.search(r'<title>(.*?) ·', html_content)
    title = title_match.group(1) if title_match else filename.replace('.html', '').replace('-', ' ').title()
    
    # Extract author (often listed as "Unknown" in audiobook pages)
    author_match = re.search(r'"author": \{"@type": "Person", "name": "(.*?)"\}', html_content)
    author = author_match.group(1) if author_match else "Guillaume Lessard"
    
    # Extract description from JSON-LD
    desc_match = re.search(r'"description": "(.*?)"', html_content, re.DOTALL)
    if desc_match:
        description = desc_match.group(1).replace('&lt;', '<').replace('&gt;', '>').replace('\\n', ' ')
        # Clean up HTML entities and truncate for better display
        description = re.sub(r'<[^>]+>', '', description)
        description = description.replace('&amp;', '&').strip()
    else:
        description = f"Professional audiobook narrated by {author}. Discover insights, techniques, and strategies that will transform your approach to this topic."
    
    # Extract image path
    image_match = re.search(r'"image": "(.*?)"', html_content)
    image_path = image_match.group(1) if image_match else "/assets/img/placeholders/card-portrait-384x576.webp"
    
    # Extract buy link
    buy_match = re.search(r'href="(https://play\.google\.com/store/books/details\?id=[^"]*)"', html_content)
    buy_link = buy_match.group(1) if buy_match else "https://play.google.com/store/books"
    
    # Extract language
    lang_match = re.search(r'"inLanguage": "([^"]*)"', html_content)
    language = lang_match.group(1).upper() if lang_match else "EN"
    
    return {
        'title': title,
        'author': author,
        'description': description,
        'image_path': image_path,
        'buy_link': buy_link,
        'language': language
    }

def upgrade_audiobook_page(file_path):
    """Upgrade a single audiobook page to professional standard"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        filename = os.path.basename(file_path)
        print(f"Processing: {filename}")
        
        # Extract information from existing content
        info = extract_audiobook_info(content, filename)
        
        # Generate new professional template
        new_content = create_professional_audiobook_template(
            title=info['title'],
            author=info['author'],
            description=info['description'],
            image_path=info['image_path'],
            buy_link=info['buy_link'],
            language=info['language']
        )
        
        # Write upgraded content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"✅ Upgraded: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function to upgrade all audiobook pages"""
    
    # Get repository root directory
    repo_root = Path(__file__).parent.parent
    audiobooks_dir = repo_root / "audiobooks"
    
    if not audiobooks_dir.exists():
        print(f"❌ Audiobooks directory not found: {audiobooks_dir}")
        return
    
    # Find all HTML files in audiobooks directory
    html_files = list(audiobooks_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in audiobooks directory")
        return
    
    print(f"🎧 Found {len(html_files)} audiobook pages to upgrade")
    print("🚀 Starting professional upgrade process...")
    print("-" * 60)
    
    success_count = 0
    total_count = len(html_files)
    
    for html_file in html_files:
        if upgrade_audiobook_page(html_file):
            success_count += 1
    
    print("-" * 60)
    print(f"✅ Upgrade complete: {success_count}/{total_count} files processed successfully")
    
    if success_count == total_count:
        print("🎉 All audiobook pages upgraded to professional standard!")
        print("📱 Pages now feature:")
        print("   • Professional header/footer design")
        print("   • Modern Tailwind CSS styling")
        print("   • Enhanced SEO and metadata")
        print("   • Responsive mobile design")
        print("   • Audio-specific branding")
        print("   • Structured data for search engines")
    else:
        print(f"⚠️  {total_count - success_count} files had issues and may need manual review")

if __name__ == "__main__":
    main()