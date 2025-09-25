#!/usr/bin/env python3
import json, re, os, sys
from pathlib import Path

ROOT = Path('.')
AUDIOBOOKS_DIR = ROOT / 'audiobooks'
CATALOG = ROOT / 'assets' / 'catalog.json'
INDEX = ROOT / 'index.html'
HARV_DIR = ROOT / 'assets' / 'harvested' / 'audiobooks'

# Utilities
slug_re = re.compile(r'[^a-z0-9\-]')

def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r'\s+', '-', s)
    s = slug_re.sub('', s)
    s = re.sub(r'-{2,}', '-', s).strip('-')
    return s


def extract_shell(html: str):
    # Extract header and footer blocks from index.html
    header_match = re.search(r"(<header[\s\S]*?</header>)", html, re.IGNORECASE)
    footer_match = re.search(r"(<footer[\s\S]*?</footer>)", html, re.IGNORECASE)
    head_open = html.split('<body', 1)[0]
    # Build minimal head with Tailwind + custom.css present in index
    head_match = re.search(r"<head>[\s\S]*?</head>", html, re.IGNORECASE)
    head_html = head_match.group(0) if head_match else ''
    return head_html, (header_match.group(1) if header_match else ''), (footer_match.group(1) if footer_match else '')


def build_page(item: dict, head_html: str, header_html: str, footer_html: str) -> str:
    title = item.get('title','').strip()
    desc = (item.get('description') or '').strip()
    img = item.get('image', '/assets/placeholder-cover.svg')
    price = item.get('price_cad')
    pages = item.get('pages') or ''
    date = item.get('date') or ''
    url = item.get('link') or item.get('url') or '#'
    lang = item.get('lang') or 'en'

    # Normalize head to include canonical + OG for the book
    canonical = f"https://id01t.store/audiobooks/{slugify(title)}.html"

    # Replace title/description/og in head
    head = head_html
    head = re.sub(r"<title>[\s\S]*?</title>", f"<title>{title} · iD01t Productions</title>", head, flags=re.IGNORECASE)
    # ensure canonical exists
    if 'rel="canonical"' in head:
        head = re.sub(r"<link[^>]*rel=\"canonical\"[^>]*>", f"<link rel=\"canonical\" href=\"{canonical}\">", head)
    else:
        head = head.replace('</head>', f"  <link rel=\"canonical\" href=\"{canonical}\">\n</head>")
    # meta description
    if re.search(r"<meta name=\"description\"", head, re.IGNORECASE):
        head = re.sub(r"<meta name=\"description\"[^>]*>", f"<meta name=\"description\" content=\"{desc[:160]}\">", head, flags=re.IGNORECASE)
    else:
        head = head.replace('</head>', f"  <meta name=\"description\" content=\"{desc[:160]}\">\n</head>")
    # OG tags
    def upsert_og(prop, val):
        nonlocal head
        if not val:
            return
        pattern = re.compile(rf"<meta[^>]*property=\"og:{re.escape(prop)}\"[^>]*>", re.IGNORECASE)
        tag = f"<meta property=\"og:{prop}\" content=\"{val}\">"
        if pattern.search(head):
            head = pattern.sub(tag, head)
        else:
            head = head.replace('</head>', f"  {tag}\n</head>")
    upsert_og('type', 'book')
    upsert_og('title', title)
    upsert_og('description', desc[:200])
    upsert_og('url', canonical)
    upsert_og('image', img)

    body_main = f"""
  <section class=\"relative overflow-hidden\">\n    <div class=\"mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-12 pb-10\">\n      <nav class=\"text-sm text-slate-500 mb-4\"><a class=\"link-underline\" href=\"/\">Home</a> › <a class=\"link-underline\" href=\"/audiobooks.html\">Audiobooks</a> › <span>{title}</span></nav>\n      <div class=\"grid md:grid-cols-2 gap-8 items-start\">\n        <img src=\"{img}\" alt=\"{title} cover\" class=\"w-full aspect-[3/4] object-cover rounded-2xl ring-1 ring-slate-200 dark:ring-slate-800\" loading=\"eager\">\n        <div>\n          <h1 class=\"text-3xl font-bold tracking-tight\">{title}</h1>\n          <p class=\"mt-3 text-slate-600 dark:text-slate-300\">{desc}</p>\n          <div class=\"mt-5 flex items-center gap-3\">\n            {(f'<span class=\\"font-semibold\\">${price:.2f} CAD</span>' if isinstance(price,(int,float)) else '')}\n            <a href=\"{url}\" target=\"_blank\" rel=\"noopener\" class=\"inline-flex items-center rounded-full bg-brand-600 hover:bg-brand-700 text-white px-5 py-2\">Listen Now</a>\n            <a href=\"/audiobooks.html\" class=\"inline-flex items-center rounded-full border border-slate-300 dark:border-slate-700 px-5 py-2\">All Audiobooks</a>\n          </div>\n          <ul class=\"mt-4 text-sm text-slate-500 space-y-1\">\n            {(f'<li>Language: {lang}</li>' if lang else '')}\n            {(f'<li>Published: {date}</li>' if date else '')}\n          </ul>\n        </div>\n      </div>\n    </div>\n  </section>\n"""

    # Assemble full doc around header/footer
    doc = [
        '<!DOCTYPE html>',
        '<html lang="en" class="scroll-smooth">',
        head,
        '<body class="bg-white text-slate-800 dark:bg-slate-950 dark:text-slate-100">',
        header_html,
        body_main,
        footer_html,
        '</body></html>'
    ]
    return "\n".join(doc)


import argparse

def main():
    parser = argparse.ArgumentParser(description="Rebuild audiobook pages from catalog.")
    parser.add_argument("--start", type=int, default=0, help="Start index of audiobooks to process.")
    parser.add_argument("--end", type=int, default=None, help="End index of audiobooks to process.")
    args = parser.parse_args()

    if not INDEX.exists():
        print("index.html not found", file=sys.stderr)
        sys.exit(1)
    head_html, header_html, footer_html = extract_shell(INDEX.read_text(encoding='utf-8'))
    data = json.loads(CATALOG.read_text(encoding='utf-8'))
    audiobooks = data.get('audiobooks', [])

    if args.end is None:
        args.end = len(audiobooks)

    audiobooks_to_process = audiobooks[args.start:args.end]

    AUDIOBOOKS_DIR.mkdir(parents=True, exist_ok=True)

    written = 0
    for item in audiobooks_to_process:
        title = item.get('title') or ''
        if not title:
            continue
        slug = slugify(title)
        out_path = AUDIOBOOKS_DIR / f"{slug}.html"
        html = build_page(item, head_html, header_html, footer_html)
        out_path.write_text(html, encoding='utf-8')
        written += 1
    print(f"Wrote {written} audiobook pages to {AUDIOBOOKS_DIR} (from index {args.start} to {args.end})")

if __name__ == '__main__':
    main()