(() => {
  const SIZE = "w600-h900";
  const FALLBACK = "/assets/img/placeholder_light_gray_block.png";
  const s = document.currentScript;
  const explicitId = s?.dataset?.bookId?.trim();
  let id = explicitId;
  if (!id) {
    const file = (location.pathname.split("/").pop() || "").replace(/\.html$/i,"");
    if (file && !/index|ebooks|audiobooks|404/i.test(file)) id = file;
  }
  if (!id) return;
  const coverURL = `https://books.google.com/books/publisher/content/images/frontcover/${encodeURIComponent(id)}?fife=${SIZE}`;
  const SELECTORS = ["img#cover",".book-cover img","img[data-role='cover']",".hero img"];
  let img = null;
  for (const sel of SELECTORS) { img = document.querySelector(sel); if (img) break; }
  if (!img) {
    const c = document.createElement("div");
    c.innerHTML = '<div style="max-width:1200px;margin:0 auto;padding:1rem"><img id="cover" width="600" height="900" style="display:block;width:100%;height:auto;aspect-ratio:2/3;object-fit:cover;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.2)"></div>';
    (document.querySelector("main") || document.body).prepend(c.firstChild);
    img = document.getElementById("cover");
  }
  const setSrc = (el, url) => {
    el.src = url; el.width = 600; el.height = 900; el.loading = "eager"; el.referrerPolicy="no-referrer";
    el.addEventListener("error", () => { el.src = FALLBACK; }, { once:true });
  };
  setSrc(img, coverURL);
  const upsertMeta = (name, content, attr="property") => {
    let m = document.querySelector(`meta[${attr}="${name}"]`);
    if (!m) { m = document.createElement("meta"); m.setAttribute(attr, name); document.head.appendChild(m); }
    m.setAttribute("content", content);
  };
  upsertMeta("og:image", coverURL); upsertMeta("twitter:image", coverURL, "name");
})();