from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BAD = re.compile(r'/assets/[^"\']*https?://', re.IGNORECASE)

def scan(dirp: Path):
    hits = []
    for f in dirp.rglob("*.html"):
        t = f.read_text(encoding="utf-8", errors="ignore")
        if BAD.search(t):
            hits.append(f)
    return hits

if __name__ == "__main__":
    aud = ROOT / "audiobooks"
    hits = scan(aud)
    print(f"Hybrid paths in audiobooks: {len(hits)}")
    for h in hits[:100]:
        print(" -", h)