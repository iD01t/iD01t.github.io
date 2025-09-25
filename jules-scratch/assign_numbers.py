import json
import re

def get_ebook_number(ebook):
    if ebook.get("ebook_number"):
        return ebook["ebook_number"]

    googleIdMappings = {
        'P3NoEQAAQBAJ': '087', 'NT1UEQAAQBAJ': '044', 'x5B-EQAAQBAJ': '068',
        'OQt0EQAAQBAJ': '004', 'Z292EQAAQBAJ': '002', 'KbmAEQAAQBAJ': '003',
        'HqNbEQAAQBAJ': '005', 'i_ZeEQAAQBAJ': '020', 'cJ88EQAAQBAJ': '059',
        'kY09EQAAQBAJ': '006', 'SDNJEQAAQBAJ': '001', 'Ys45EQAAQBAJ': '001',
        'WFU4EQAAQBAJ': '008', 'ODlUEQAAQBAJ': '047', 'wRQ4EQAAQBAJ': '035',
        '8EhZEQAAQBAJ': '026', '5vg5EQAAQBAJ': '025', 'pXdLEQAAQBAJ': '061',
        'KuB_EQAAQBAJ': '062', 'm5M4EQAAQBAJ': '068', 'Kwo4EQAAQBAJ': '001',
        'Iwo4EQAAQBAJ': '004', 'H_A4EQAAQBAJ': '005', 'Owo4EQAAQBAJ': '007',
        'eQJkEQAAQBAJ': '008', 'ewtZEQAAQBAJ': '009', 'OQo4EQAAQBAJ': '010',
        '0Yo2EQAAQBAJ': '011', '8_ReEQAAQBAJ': '012', 'khhJEQAAQBAJ': '013',
        'QMQ6EQAAQBAJ': '014', 'dtI5EQAAQBAJ': '015', 'X-84EQAAQBAJ': '016',
        'SxU4EQAAQBAJ': '017', 'lCV2EQAAQBAJ': '018', 'msQ6EQAAQBAJ': '019',
        'aBQ4EQAAQBAJ': '021', 'SdVhEQAAQBAJ': '022', '8vg5EQAAQBAJ': '023',
        'exc4EQAAQBAJ': '024', '2aRMEQAAQBAJ': '026', 'oRg3EQAAQBAJ': '027',
        '9sM6EQAAQBAJ': '028', 'l_M6EQAAQBAJ': '029', 'qRQ4EQAAQBAJ': '030',
        '825dEQAAQBAJ': '031', 'Q_A4EQAAQBAJ': '032', 'URVYEQAAQBAJ': '033',
        'o3c6EQAAQBAJ': '034', 'sxQ4EQAAQBAJ': '035', 'ZM45EQAAQBAJ': '036',
        'to9REQAAQBAJ': '037', 'psZYEQAAQBAJ': '038', 'om8-EQAAQBAJ': '039',
        'ZZs9EQAAQBAJ': '040', 'U8ZAEQAAQBAJ': '041', 'nypGEQAAQBAJ': '043',
        'BqR_EQAAQBAJ': '045', 'cS1GEQAAQBAJ': '046', 'nNVlEQAAQBAJ': '049',
        'iwZzEQAAQBAJ': '050'
    }

    cover_url = ebook.get("image", "") or ebook.get("cover", "")
    if 'id=' in cover_url:
        google_books_id = cover_url.split('id=')[1].split('&')[0]
        if google_books_id in googleIdMappings:
            return googleIdMappings[google_books_id]

    clean_title = ebook.get("title", "").lower()
    clean_title = re.sub(r'[🌿✨🎧🚀📖]+\s*', '', clean_title)
    clean_title = re.sub(r'[^a-z0-9\s]', '', clean_title)
    clean_title = re.sub(r'\s+', ' ', clean_title).strip()

    titleMappings = {
        'echoes of the heart': '001', 'anarchy and evolution': '001',
        'ai cash code': '002', 'windows zero to hero': '002',
        'ai cash empire': '003', 'to the top of the mountain': '003',
        'agentic ai sprint for solopreneurs': '004',
        'intersection the moment their paths crossed': '004',
        'ai goldmine 100 passive income ideas using chatgpt and free ai tools': '005',
        'the architects legacy': '005',
        'ai today transforming lives and industries for the future': '006',
        'shadows of redemption': '007',
        'automation and seo mastery strategies for growth and efficiency': '008',
        'quantum tao': '008', 'light at the veils edge': '009',
        'legacy of shadows': '010', 'before the storm': '011',
        'spiritual psychosis memoir': '012', 'the dream dialogue': '013',
        'veil of echoes': '014', 'the many realities': '015',
        'master the basics of reading music': '016', 'eternal roots': '017',
        'the quantum passive empire': '018',
        'shadows reforged the war isnt over': '019', 'ai in education': '020',
        'legacy of shadows 2': '021', 'java maestro': '022',
        'mastering blender': '023',
        'mastering generative ai and llms third edition': '024',
        'bite by bite': '025', 'mastering quantum error correction': '026',
        'beyond the event horizon solving the black hole information paradox': '026',
        'jacks stand': '027', 'crossroads of shadows': '028',
        'the power of repetition transforming minds through words': '029',
        'forever in bloom': '030',
        'sacred timing when the universe speaks through synchronicity': '031',
        'shadows of serenity': '032', 'sacred vibrational technology': '033',
        'zen and the art of resilient living': '034', 'shadows of bloom': '035',
        'beneath the bloom': '035', 'love prevails': '036',
        'final transmission i am echo': '037',
        'quantum jumping unlocked edition 2': '038',
        'machine learning demystified a practical guide to building smarter systems': '039',
        'code in every language master programming with chatgpt': '039',
        'the end of an era the tiktok shutdown in the usa': '040',
        'the adventure of id01t productions a story of passion resilience and creativity': '041',
        'id01t academy python exercises book 1 edition 2': '043',
        'ableton elevation dj id01ts complete guide to building hits and elevating your sound': '044',
        'id01t academy python exercises book 3': '045',
        'id01t academy python exercises book 2 edition 2': '046',
        'beat alchemy the dj id01t guide to mastering fl studio and making hits': '047',
        'real': '049', 'kimi k2 unlocked': '050',
        'bridging worlds a practical guide to connecting with parallel energies and dimensions': '061',
        'c zero to hero': '062', 'chess mastery': '068',
        'advanced tactics psychological play and tournament preparation': '068',
        'ai revolution how automation is transforming everyday life edition 2 2025': '059',
        'ai revolution how automation is transforming everyday life': '059',
        'la charte des relations sacrees de la nouvelle terre': '087'
    }

    if clean_title in titleMappings:
        return titleMappings[clean_title]

    for key, value in titleMappings.items():
        if clean_title in key or key in clean_title:
            return value

    match = re.search(r'ebook[_\s]?(\d+)', ebook.get("title", ""), re.IGNORECASE)
    if match:
        return str(int(match.group(1))).zfill(3)

    return None

def main():
    catalog_path = 'assets/catalog.json'
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    for ebook in catalog.get('ebooks', []):
        ebook_number = get_ebook_number(ebook)
        if ebook_number:
            ebook['ebook_number'] = ebook_number

    for audiobook in catalog.get('audiobooks', []):
        # The logic is the same for audiobooks, so we can reuse the function
        audiobook_number = get_ebook_number(audiobook)
        if audiobook_number:
            audiobook['audiobook_number'] = audiobook_number

    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Updated {catalog_path} with ebook and audiobook numbers.")

if __name__ == "__main__":
    main()