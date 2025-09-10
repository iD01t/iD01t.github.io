import json, os, sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

def find_catalog():
    # 1) Explicit override
    p = os.environ.get("EBOOKS_JSON")
    if p:
        p = Path(p)
        if p.is_file():
            return p
        else:
            print(f"[build] EBOOKS_JSON set but file not found: {p}", file=sys.stderr)
    # 2) Common fallbacks
    root = Path(__file__).resolve().parents[1]
    candidates = [
        root / "data" / "ebooks.json",
        root / "docs" / "data" / "ebooks.json",
        root / "site" / "data" / "ebooks.json",
        root / "content" / "data" / "ebooks.json",
        root / "assets" / "ebooks.json",
    ]
    for c in candidates:
        if c.is_file():
            return c
    raise FileNotFoundError("ebooks.json not found. Set EBOOKS_JSON or place it under data/, docs/data/, site/data/, content/data/, or assets/.")

def main():
    root = Path(__file__).resolve().parents[1]
    data_path = find_catalog()
    print(f"[build] Using catalog: {data_path}")

    books = json.loads(data_path.read_text(encoding="utf-8"))

    # Template resolution with fallbacks
    tpl_dir_candidates = [
        root / "templates",
        root / "scripts" / "templates",
    ]
    tpl_dir = next((p for p in tpl_dir_candidates if p.is_dir()), None)
    if not tpl_dir:
        raise FileNotFoundError("Template directory not found under templates/ or scripts/templates/")

    tpl_name = "ebook.html.j2"
    env = Environment(
        loader=FileSystemLoader(str(tpl_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    tpl = env.get_template(tpl_name)

    out_dir = root / "ebooks"
    out_dir.mkdir(parents=True, exist_ok=True)

    site_origin = os.environ.get("SITE_ORIGIN", "https://id01t.store")

    count = 0
    for e in books:
        slug = e.get("slug")
        if not slug:
            print(f"[build] Skipping entry without slug: {e}", file=sys.stderr)
            continue
        html = tpl.render(e=e, site_origin=site_origin)
        (out_dir / f"{slug}.html").write_text(html, encoding="utf-8")
        count += 1

    print(f"[build] Generated {count} pages in {out_dir}")

if __name__ == "__main__":
    main()
