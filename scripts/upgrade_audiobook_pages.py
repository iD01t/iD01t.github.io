# scripts/upgrade_audiobook_pages.py
import sys, argparse
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

PREFERRED_AUDIOBOOK_BASE = "/assets/covers/audiobooks/"
PREFERRED_EBOOK_BASE     = "/assets/covers/ebooks/"

def is_abs_url(s: str) -> bool:
    if not s: return False
    p = urlparse(s)
    return p.scheme in ("http", "https") and bool(p.netloc)

def dehybridize(s: str) -> str:
    if not s: return s
    i = s.find("http://")
    j = s.find("https://")
    k = min([x for x in (i, j) if x != -1], default=-1)
    return s[k:] if k > 0 else s

def to_preferred_local(s: str, is_audiobook=True) -> str:
    base = PREFERRED_AUDIOBOOK_BASE if is_audiobook else PREFERRED_EBOOK_BASE
    if s.startswith("/"):      # already an absolute local path (non-hybrid)
        return dehybridize(s)  # leaves normal locals intact; strips hybrids if any
    name = s.split("/")[-1]    # filename or last segment
    return base + name

def fix_src_val(val: str, is_audiobook=True) -> str:
    if not val: return val
    if is_abs_url(val):         # absolute → keep
        return val
    dh = dehybridize(val)       # strip local prefix before http(s)
    if is_abs_url(dh):
        return dh
    return to_preferred_local(dh, is_audiobook=is_audiobook)

def fix_html_file(path: Path, is_audiobook=True) -> bool:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    changed = False

    for m in soup.find_all("meta", attrs={"property": "og:image"}):
        old = m.get("content")
        new = fix_src_val(old, is_audiobook=is_audiobook)
        if new and new != old:
            m["content"] = new; changed = True

    for m in soup.find_all("meta", attrs={"name": "twitter:image"}):
        old = m.get("content")
        new = fix_src_val(old, is_audiobook=is_audiobook)
        if new and new != old:
            m["content"] = new; changed = True

    for img in soup.find_all("img"):
        old = img.get("src")
        new = fix_src_val(old, is_audiobook=is_audiobook)
        if new and new != old:
            img["src"] = new; changed = True

    if changed:
        path.write_text(str(soup), encoding="utf-8")
    return changed

def iter_targets(root: Path, include_patterns):
    # If specific files were passed, yield those; otherwise recurse.
    if include_patterns:
        for pat in include_patterns:
            for p in root.glob(pat):
                if p.is_file() and p.suffix == ".html":
                    yield p
        return
    for p in root.rglob("*.html"):
        if "audiobooks" in p.parts:  # scope: audiobooks/ only
            yield p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="Files or directories (default: audiobooks)")
    ap.add_argument("--batch-size", type=int, default=20, help="files per run (to avoid env rollback)")
    ap.add_argument("--include", nargs="*", help="Glob patterns relative to each dir, e.g. '*.html'")
    args = ap.parse_args()

    targets = []
    paths = [Path(p) for p in (args.paths or ["audiobooks"])]
    for base in paths:
        if base.is_dir():
            targets.extend(iter_targets(base, args.include))
        elif base.is_file():
            targets.append(base)

    # Deterministic order for stable batching
    targets = sorted(set(targets))

    fixed_total = 0
    for i in range(0, len(targets), args.batch_size):
        batch = targets[i : i + args.batch_size]
        batch_fixed = 0
        for f in batch:
            try:
                if fix_html_file(f, is_audiobook=True):
                    batch_fixed += 1
            except FileNotFoundError:
                # Unicode/shell quoting hiccups won't crash the whole run
                continue
        print(f"[upgrade] batch {i//args.batch_size+1}: {batch_fixed}/{len(batch)} changed")
        fixed_total += batch_fixed

    print(f"[upgrade] total fixed: {fixed_total}, scanned: {len(targets)}")

if __name__ == "__main__":
    main()