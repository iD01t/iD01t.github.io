#!/usr/bin/env python3
import json, os, re, sys, time
from pathlib import Path
from urllib.parse import urlencode
import requests

ROOT = Path('.')
CATALOG = ROOT / 'assets' / 'catalog.json'
HD_DIR = ROOT / 'assets' / 'harvested' / 'ebooks'
SUMMARY = ROOT / 'assets' / 'harvested' / 'ebooks' / 'download_summary.json'

GOOGLE_API = 'https://www.googleapis.com/books/v1/volumes'
HEADERS = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'}

def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r'\s+', '-', s)
    s = re.sub(r'[^a-z0-9\-]', '', s)
    s = re.sub(r'-{2,}', '-', s).strip('-')
    return s


def extract_book_id_from_url(url: str) -> str:
    if not url:
        return ''
    match = re.search(r'[?&]id=([^&]+)', url)
    if match:
        # Exclude GGKEY patterns as they are not volume IDs
        if 'GGKEY' in match.group(1):
            return ''
        return match.group(1)
    return ''


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def best_cover_from_volume(volume: dict) -> str:
    links = (volume.get('volumeInfo') or {}).get('imageLinks') or {}
    # Prefer largest available
    for key in ['extraLarge','large','medium','thumbnail','small','smallThumbnail']:
        if links.get(key):
            return links[key]
    return ''


def fetch_volume_by_id(book_id: str) -> dict:
    url = f'{GOOGLE_API}/{book_id}?country=US'
    r = requests.get(url, timeout=12, headers=HEADERS)
    if r.ok:
        return r.json()
    return {}


def search_volume(title: str, author: str='Guillaume Lessard') -> dict:
    q = {'q': f'intitle:{title} inauthor:{author}', 'country': 'US'}
    r = requests.get(GOOGLE_API, params=q, timeout=12, headers=HEADERS)
    if not r.ok:
        return {}
    data = r.json()
    items = data.get('items') or []
    return items[0] if items else {}


def download_image(url: str, dest: Path) -> bool:
    try:
        r = requests.get(url, timeout=20, headers=HEADERS)
        if not r.ok:
            return False
        dest.write_bytes(r.content)
        return True
    except Exception:
        return False


def normalize_buy_link(volume: dict) -> str:
    # Prefer canonical Google Play Books/Books URL
    info = volume.get('volumeInfo') or {}
    # Try canonicalVolumeLink first
    link = info.get('canonicalVolumeLink') or info.get('infoLink') or ''
    return link


def get_long_description(volume: dict) -> str:
    info = volume.get('volumeInfo') or {}
    return info.get('description') or ''


def build_local_image_name(title: str, book_id: str) -> str:
    base = slugify(title) or book_id.lower()
    return f'{base}_{book_id}_cover.jpg'


def main():
    ensure_dir(HD_DIR)
    catalog = json.loads(CATALOG.read_text(encoding='utf-8'))
    ebooks = catalog.get('ebooks') or []

    # Map possible IDs from summary
    id_map = {}
    if SUMMARY.exists():
        try:
            summ = json.loads(SUMMARY.read_text(encoding='utf-8'))
            for b in summ.get('books', []):
                id_map[b.get('title','').strip().lower()] = b.get('book_id','')
        except Exception:
            pass

    updated = 0
    for book in ebooks:
        title = (book.get('title') or '').strip()
        if not title:
            continue

        book_id = extract_book_id_from_url(book.get('url', ''))

        if not book_id:
            key = title.lower()
            book_id = id_map.get(key, '')

        volume = fetch_volume_by_id(book_id) if book_id else {}
        if not volume:
            volume = search_volume(title)

        if not volume:
            continue

        # Cover
        cover_url = best_cover_from_volume(volume)
        if cover_url:
            # bump resolution if param present
            cover_url = re.sub(r'zoom=\d', 'zoom=6', cover_url)
            # switch to https if missing
            if cover_url.startswith('http://'):
                cover_url = 'https://' + cover_url[len('http://'):]
            local_name = build_local_image_name(title, (volume.get('id') or 'id'))
            local_path = HD_DIR / local_name
            if download_image(cover_url, local_path):
                book['image'] = f'/assets/harvested/ebooks/{local_name}'

        # Description
        desc = get_long_description(volume)
        if desc:
            book['description'] = desc
            # also provide a short version for grids
            plain = re.sub(r'<[^>]*>', '', desc)
            short = (plain.strip())[:180]
            book['short'] = short

        # Buy link
        buy = normalize_buy_link(volume)
        if buy:
            book['url'] = buy

        updated += 1
        time.sleep(0.5)

    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Updated {updated} ebooks with HD image/description/buy link')

if __name__ == '__main__':
    main()