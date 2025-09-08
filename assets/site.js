(function(){
  const $ = (s,r=document)=>r.querySelector(s), $$=(s,r=document)=>r.querySelectorAll(s);

  // Theme
  const saved = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  if(saved==="light") document.documentElement.classList.add("light");
  if(!saved && !prefersDark) document.documentElement.classList.add("light");
  function toggleTheme(){
    document.documentElement.classList.toggle("light");
    localStorage.setItem("theme", document.documentElement.classList.contains("light")?"light":"dark");
  }

  // Header + footer inject
  function header(active){
    const links = [
      ["Home","/index.html"],
      ["Store","/store.html"],
      ["Apps","/apps.html"],
      ["eBooks","/ebooks.html"],
      ["Audiobooks","/audiobooks.html"],
      ["Games","/games.html"],
      ["Music","/music.html"],
      ["Blog","/blog.html"],
      ["About","/about.html"],
      ["Contact","/contact.html"]
    ];
    return `
      <div class="header">
        <nav class="nav">
          <a href="/"><strong>iD01t Productions</strong></a>
          ${links.map(([t,href])=>`<a href="${href}" ${active===t?'style="text-decoration:underline"':''}>${t}</a>`).join("")}
          <div class="right"><button class="toggle" id="themeToggle">Theme</button></div>
        </nav>
      </div>`;
  }
  if(!document.querySelector(".header")){
    document.body.insertAdjacentHTML("afterbegin", header(document.body.dataset.active||""));
    $("#themeToggle").addEventListener("click", toggleTheme);
  }
  if(!document.querySelector(".footer")){
    document.body.insertAdjacentHTML("beforeend", `<div class="footer">© iD01t Productions — Built for speed & SEO</div>`);
  }

  // Image resolver: replace blocked Imgur or empty images with local/base64 from manifest
  async function resolveImages(){
    let manifest={};
    try{
      const r = await fetch("/assets/images.json", {cache:"no-store"});
      if(r.ok) manifest = await r.json();
    }catch(e){}
    const placeholder = "/assets/placeholder-cover.svg";
    for (const img of $$("img")){
      const src = img.getAttribute("src")||"";
      if(!src || /imgur\.com/i.test(src) || src.startsWith("http") && !/^(https?:)?\/\/(id01t\.store|id01t\.github\.io)/i.test(src)){
        const key = img.getAttribute("data-key") || img.getAttribute("alt") || src;
        const mapped = manifest[key] || manifest[key?.toLowerCase?.()] || manifest[(key||"").replace(/\s+/g,"-").toLowerCase()];
        img.loading = "lazy";
        img.decoding = "async";
        img.referrerPolicy = "no-referrer";
        img.src = mapped || placeholder;
      }else{
        img.loading = "lazy";
        img.decoding = "async";
      }
    }
  }
  resolveImages();

  // Catalog renderer (optional): render cards from JSON into .grid
  async function renderGrid(kind){
    const grid = document.querySelector(".grid"); if(!grid) return;
    const catRes = await fetch("/assets/catalog.json", {cache:"no-store"}).catch(()=>null);
    if(!catRes || !catRes.ok) return;
    const data = await catRes.json();
    const items = data[kind]||[];
    grid.innerHTML = items.map(it => `
      <article class="card">
        <img alt="${it.title}" data-key="${it.title}" src="${it.image||''}">
        <div class="badge">${kind.slice(0,-1)}</div>
        <h3 class="title"><a href="${it.link}">${it.title}</a></h3>
        <div class="meta">${it.author||'Unknown'} • ${it.lang||'EN'}</div>
        <a class="btn" href="${it.link}">Open</a>
      </article>`).join("");
    resolveImages();
  }
  const kind = document.body.dataset.catalog;
  if(kind) renderGrid(kind);

  // Link checker: warn in console if any nav link 404s
  window.addEventListener('load', ()=>{
    [...$$('.nav a')].forEach(async a=>{
      if(a.getAttribute('href').startsWith('/')){
        try{
          const r = await fetch(a.href, {method:'HEAD'});
          if(!r.ok) console.warn('Broken link:', a.href, r.status);
        }catch(e){ console.warn('Broken link:', a.href, e); }
      }
    });
  });
})();

// Minimal in-page product registry example; replace with your real dataset
window.PRODUCTS = window.PRODUCTS || {
  "html2exe-pro": {
    title: "HTML2exe Pro",
    subtitle: "Turn HTML into Windows .exe",
    image: "/assets/apps/html2exe-pro/cover-1200.jpg",
    bullets: [
      "Local, offline builds",
      "No telemetry, no accounts",
      "Includes templates and CI tips"
    ],
    price: "19.00 CAD",
    buy: "https://your-checkout-link"
  }
};

function openProductModal(slug) {
  const p = window.PRODUCTS[slug];
  if (!p) return;
  document.getElementById("pm-title").textContent = p.title;
  document.getElementById("pm-sub").textContent = p.subtitle || "";
  document.getElementById("pm-image").src = p.image || "";
  const ul = document.getElementById("pm-bullets");
  ul.innerHTML = "";
  (p.bullets || []).forEach(b => {
    const li = document.createElement("li");
    li.textContent = b;
    ul.appendChild(li);
  });
  const buy = document.getElementById("pm-buy");
  buy.textContent = `Buy • ${p.price || "View"}`;
  buy.href = p.buy || "#";
  document.getElementById("product-modal").style.display = "block";
  document.getElementById("product-modal").setAttribute("aria-hidden","false");
}

function closeProductModal() {
  const m = document.getElementById("product-modal");
  m.style.display = "none";
  m.setAttribute("aria-hidden","true");
}
