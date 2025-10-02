import json
import io

MAN = json.load(open("landing_manifest.json", encoding="utf-8"))
SLUG_TO_REAL = { e["slug"]: e["original_path"] for e in MAN["entries"] }

def open_by_slug(slug: str, mode="r", **kw):
    real = SLUG_TO_REAL.get(slug)
    if not real:
        raise FileNotFoundError(f"Slug not found: {slug}")
    return open(real, mode, **kw)