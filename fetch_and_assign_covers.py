#!/usr/bin/env python3
"""
fetch_and_assign_covers.py

Batch-download HD cover images for ebooks and audiobooks from Google Books
using a links file (JSON or CSV) with columns:
  - title
  - authors (optional)
  - type ("ebook" or "audiobook")
  - google_volume_id
  - cover_zoom5, cover_zoom3, cover_zoom2  (direct content URLs)
  - info_page (optional, human page)
  - api_url (optional)

Images are saved to:
  assets/covers/ebooks/{safe_id}.jpg
  assets/covers/audiobooks/{safe_id}.jpg

Optionally updates a product catalog JSON by setting the `image` field to
the saved file path. Matching is by:
  1) google_volume_id field if present in catalog items, else
  2) case-insensitive title match, with a few normalization heuristics.

Usage examples:

# Basic: download all covers to assets/covers/* using the links JSON
python3 fetch_and_assign_covers.py \
  --links data/google_books_links.json \
  --out-dir assets/covers

# Update an ebooks catalog after downloading
python3 fetch_and_assign_covers.py \
  --links data/google_books_links.json \
  --out-dir assets/covers \
  --update-catalog data/ebooks_json_fixed.json \
  --catalog-type ebooks \
  --image-key image

# Force re-downloads and write a JSON/CSV report
python3 fetch_and_assign_covers.py \
  --links data/google_books_links.json \
  --out-dir assets/covers \
  --force \
  --report-json data/covers_report.json \
  --report-csv  data/covers_report.csv
"""
import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# We only import requests at runtime (to keep this file importable in restricted envs)
try:
    import requests
except Exception as e:
    requests = None

def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"

def safe_join(*parts: str) -> str:
    return os.path.normpath(os.path.join(*parts))

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def normalize_title(title: str) -> str:
    t = (title or "").strip().lower()
    # Remove common separators for subtitles
    t = re.split(r"[:\-–—|•]\s*", t)[0].strip()
    # Collapse whitespace
    t = re.sub(r"\s+", " ", t)
    return t

@dataclass
class LinkRow:
    title: str
    authors: str
    itype: str
    volume_id: str
    cover_urls: List[str]

def parse_links(path: str) -> List[LinkRow]:
    rows: List[LinkRow] = []
    if path.lower().endswith(".json"):
        data = json.load(open(path, "r", encoding="utf-8"))
        for obj in data:
            title = str(obj.get("title", "")).strip()
            authors = str(obj.get("authors", "")).strip()
            itype = str(obj.get("type", "")).strip().lower()
            vid = str(obj.get("google_volume_id", "")).strip()
            covers = [obj.get("cover_zoom5", ""), obj.get("cover_zoom3", ""), obj.get("cover_zoom2", "")]
            covers = [c for c in covers if isinstance(c, str) and c.strip()]
            rows.append(LinkRow(title, authors, itype, vid, covers))
    else:
        # CSV
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for obj in reader:
                title = str(obj.get("title", "")).strip()
                authors = str(obj.get("authors", "")).strip()
                itype = str(obj.get("type", "")).strip().lower()
                vid = str(obj.get("google_volume_id", "")).strip()
                covers = [obj.get("cover_zoom5", ""), obj.get("cover_zoom3", ""), obj.get("cover_zoom2", "")]
                covers = [c for c in covers if isinstance(c, str) and c.strip()]
                rows.append(LinkRow(title, authors, itype, vid, covers))
    return rows

def pick_filename(row: LinkRow) -> str:
    base = row.volume_id if row.volume_id else slugify(row.title or "untitled")
    return f"{base}.jpg"

def download_first_ok(urls: List[str], timeout: int = 12, max_retries: int = 2) -> Optional[bytes]:
    if requests is None:
        raise RuntimeError("requests is not available in this environment. Install it to run downloads.")
    headers = {"User-Agent": "iD01t-CoverFetcher/1.0"}
    for url in urls:
        for attempt in range(max_retries + 1):
            try:
                resp = requests.get(url, headers=headers, timeout=timeout, stream=True)
                if resp.status_code == 200:
                    content_type = resp.headers.get("Content-Type", "")
                    if "image" in content_type:
                        data = resp.content
                        # Minimum sanity check: at least 10KB
                        if len(data) >= 10_000:
                            return data
                # brief backoff
                time.sleep(0.5 * (attempt + 1))
            except Exception:
                time.sleep(0.5 * (attempt + 1))
                continue
    return None

def load_catalog(path: str) -> List[dict]:
    return json.load(open(path, "r", encoding="utf-8"))

def save_catalog(path: str, items: List[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def index_catalog(items: List[dict], volume_id_key: str = "google_volume_id") -> Tuple[Dict[str, int], Dict[str, int]]:
    by_vol: Dict[str, int] = {}
    by_title: Dict[str, int] = {}
    for idx, it in enumerate(items):
        vid = str(it.get(volume_id_key, "")).strip().lower()
        if vid:
            by_vol[vid] = idx
        t = normalize_title(str(it.get("title", "")))
        if t:
            by_title[t] = idx
    return by_vol, by_title

def assign_image(item: dict, image_path: str, image_key: str) -> None:
    item[image_key] = image_path

def main():
    ap = argparse.ArgumentParser(description="Download HD covers and assign to catalogs.")
    ap.add_argument("--links", required=True, help="Path to google_books_links.json or .csv")
    ap.add_argument("--out-dir", required=True, help="Base output dir for covers (e.g., assets/covers)")
    ap.add_argument("--force", action="store_true", help="Re-download even if file exists")
    ap.add_argument("--report-json", default="", help="Write a JSON report here")
    ap.add_argument("--report-csv", default="", help="Write a CSV report here")

    ap.add_argument("--update-catalog", default="", help="Optional: path to a catalog JSON to update")
    ap.add_argument("--catalog-type", choices=["ebooks","audiobooks"], default="ebooks", help="Catalog type (affects subdir and matching heuristics)")
    ap.add_argument("--image-key", default="image", help="Field name to write the image path to in the catalog")
    ap.add_argument("--volume-id-key", default="google_volume_id", help="Catalog field name for the Google volume id, if present")

    args = ap.parse_args()

    links = parse_links(args.links)
    out_base = args.out_dir

    # Prepare catalogs if any
    catalog_items: Optional[List[dict]] = None
    by_vol: Dict[str, int] = {}
    by_title: Dict[str, int] = {}
    if args.update_catalog:
        catalog_items = load_catalog(args.update_catalog)
        by_vol, by_title = index_catalog(catalog_items, volume_id_key=args.volume_id_key)

    report: List[Dict[str, str]] = []
    total = 0
    ok = 0

    for row in links:
        total += 1
        sub = "audiobooks" if row.itype == "audiobook" else "ebooks"
        out_dir = safe_join(out_base, sub)
        ensure_dir(out_dir)
        fname = pick_filename(row)
        out_path = safe_join(out_dir, fname)

        status = "skipped"
        reason = ""

        if not args.force and os.path.exists(out_path):
            status = "exists"
        else:
            data = download_first_ok(row.cover_urls) if row.cover_urls else None
            if data:
                with open(out_path, "wb") as f:
                    f.write(data)
                status = "downloaded"
                ok += 1
            else:
                status = "failed"
                reason = "no_cover_downloaded"

        # Assign to catalog if provided
        assigned = ""
        catalog_idx = None
        if catalog_items is not None:
            # Prefer volume id match
            vid_key = (row.volume_id or "").strip().lower()
            if vid_key and vid_key in by_vol:
                catalog_idx = by_vol[vid_key]
            else:
                # Title fallback
                tnorm = normalize_title(row.title)
                if tnorm and tnorm in by_title:
                    catalog_idx = by_title[tnorm]

            if catalog_idx is not None:
                rel_path = f"assets/covers/{sub}/{fname}"
                assign_image(catalog_items[catalog_idx], rel_path, args.image_key)
                assigned = rel_path

        report.append({
            "title": row.title,
            "authors": row.authors,
            "type": row.itype,
            "google_volume_id": row.volume_id,
            "file": out_path,
            "status": status,
            "assigned_image": assigned,
            "reason": reason,
        })

    # Save report
    if args.report_json:
        with open(args.report_json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    if args.report_csv:
        import csv
        with open(args.report_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(report[0].keys()) if report else
                               ["title","authors","type","google_volume_id","file","status","assigned_image","reason"])
            w.writeheader()
            for r in report:
                w.writerow(r)

    # Save catalog if updated
    if catalog_items is not None:
        save_catalog(args.update_catalog, catalog_items)

    print(f"Done. {ok}/{total} covers downloaded.")
    if args.update_catalog:
        print(f"Catalog updated: {args.update_catalog}")

if __name__ == "__main__":
    import re
    main()
