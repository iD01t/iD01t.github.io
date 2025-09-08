// scripts/build-sitemap.js
const fs = require("fs");
const path = require("path");

const SITE = "https://id01t.store";
const PAGES = [
  "/", "/store.html", "/apps.html", "/ebooks.html", "/audiobooks.html",
  "/games.html", "/music.html", "/blog.html", "/about.html", "/contact.html",
  "/blog/html2exe-pro-launch.html", "/blog/kitties-mayhem-beta.html",
  // Add programmatically discovered ebook pages below:
  // ...we will scan /ebooks directory.
];

function iso(d) { return d.toISOString().split("T")[0]; }

function collectEbookPages(rootDir) {
  const dir = path.join(rootDir, "ebooks");
  const out = [];
  if (!fs.existsSync(dir)) return out;
  const created_ebooks = [
    "veo3-json-guide.html",
    "diy-digital-skills.html",
    "chess-mastery.html"
  ]
  for (const f of fs.readdirSync(dir)) {
    if (f.endsWith(".html") && f !== "index.html" && f !== "ebooks.html" && created_ebooks.includes(f)) {
      out.push(`/ebooks/${f}`);
    }
  }
  return out;
}

(function main() {
  const root = process.cwd();
  const lastmod = iso(new Date());
  const urls = new Set(PAGES);

  for (const e of collectEbookPages(root)) urls.add(e);

  const body = [...urls].sort().map(u => (
    `  <url><loc>${SITE}${u}</loc><lastmod>${lastmod}</lastmod></url>`
  )).join("\n");

  const xml =
`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${body}
</urlset>
`;

  fs.writeFileSync(path.join(root, "sitemap.xml"), xml, "utf8");
  console.log("sitemap.xml written");
})();
