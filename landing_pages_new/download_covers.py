#!/usr/bin/env python3
import json, os, sys, time, pathlib, urllib.request, urllib.error

OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else "covers_out"
os.makedirs(OUT_DIR, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
HEADERS = {"User-Agent": UA, "Referer": "https://books.google.com"}

def fetch(url, outpath, retries=5, backoff=1.5):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp, open(outpath, "wb") as f:
                f.write(resp.read())
            return True
        except Exception as e:
            time.sleep(backoff ** i)
    return False

manifest = json.loads((pathlib.Path(__file__).parent / "covers_manifest.json").read_text(encoding="utf-8"))

for it in manifest:
    title = it["title"]
    volid = it["id"]
    slug  = it["slug"]
    out = os.path.join(OUT_DIR, f"{slug}_{volid}.jpg")

    ok = False
    for url in it["image_urls"]:
        if fetch(url, out):
            print(f"OK  - {title} -> {out}")
            ok = True
            break
        else:
            print(f"TRY - {title} failed: {url}", file=sys.stderr)
    if not ok:
        print(f"ERR - {title} (all image URLs failed). Preview: {it['books_frontcover_preview']}", file=sys.stderr)
