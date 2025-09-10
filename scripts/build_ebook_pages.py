import json, os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "ebooks.json"
TPL  = ROOT / "templates" / "ebook.html.j2"
OUT  = ROOT / "ebooks"

def main():
    books = json.loads(DATA.read_text(encoding="utf-8"))
    env = Environment(
        loader=FileSystemLoader(str(TPL.parent)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    tpl = env.get_template(TPL.name)
    OUT.mkdir(parents=True, exist_ok=True)
    site_origin = os.environ.get("SITE_ORIGIN", "https://id01t.store")
    for e in books:
        html = tpl.render(e=e, site_origin=site_origin)
        (OUT / f"{e['slug']}.html").write_text(html, encoding="utf-8")
    print(f"Generated {len(books)} pages in {OUT}")

if __name__ == "__main__":
    main()
