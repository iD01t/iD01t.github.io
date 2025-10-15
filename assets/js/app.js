/* Tiny helper library for id01t.github.io — zero dependencies. */
const SITE = {
  base: location.origin,
  pages: { ebooks: '/ebooks.html', audiobooks: '/audiobooks.html', book: '/book.html' },
  dataUrl: '/data/catalog.json', // built by tools/build_catalog.py
  // Infer page mode
  mode() {
    const p = location.pathname.toLowerCase();
    if (p.endsWith('/ebooks.html')) return 'ebooks';
    if (p.endsWith('/audiobooks.html')) return 'audiobooks';
    if (p.endsWith('/book.html')) return 'book';
    return 'other';
  }
};

// Simple fetch with session cache
async function getCatalog() {
  const cacheKey = 'catalog.v1';
  const cached = sessionStorage.getItem(cacheKey);
  if (cached) {
    try { return JSON.parse(cached); } catch {}
  }
  const res = await fetch(SITE.dataUrl, { credentials: 'omit', cache: 'no-store' });
  if (!res.ok) throw new Error('Failed to load catalog.json');
  const json = await res.json();
  sessionStorage.setItem(cacheKey, JSON.stringify(json));
  return json;
}

function $(sel, root=document){ return root.querySelector(sel); }
function $all(sel, root=document){ return [...root.querySelectorAll(sel)]; }
function esc(s=''){ return (s+'').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function fmtPrice(p){ return (!p || isNaN(+p)) ? '' : `$${(+p).toFixed(2)}`; }
function param(name){ return new URLSearchParams(location.search).get(name); }
function setParams(obj){
  const url = new URL(location.href);
  for (const [k,v] of Object.entries(obj)) {
    if (v === null || v === undefined || v === '') url.searchParams.delete(k);
    else url.searchParams.set(k,v);
  }
  history.replaceState({}, '', url);
}

function injectJSONLD(obj){
  const s = document.createElement('script');
  s.type = 'application/ld+json';
  s.textContent = JSON.stringify(obj);
  document.head.appendChild(s);
}

// Build search index (very light): lowercase fields joined
function makeIndex(item){
  return [
    item.title, item.subtitle || '', item.contributors || '',
    item.publisher || '', item.language || '', item.format || ''
  ].join(' ').toLowerCase();
}

// Render list page (ebooks/audiobooks)
async function bootstrapList(){
  const MODE = SITE.mode(); if (!['ebooks','audiobooks'].includes(MODE)) return;
  const isAudio = MODE === 'audiobooks';

  const data = (await getCatalog()).filter(x => (isAudio ? x.format === 'Audiobook' : x.format === 'eBook'));
  const index = data.map(d => ({ id:d.id, hay: makeIndex(d) }));
  const $grid = $('#grid'); const $count = $('#count');
  const $q = $('#q'); const $lang = $('#lang'); const $sort = $('#sort');
  const $min = $('#min'); const $max = $('#max');

  // Build language filter options
  const langs = [...new Set(data.map(d => (d.language||'').trim()).filter(Boolean))].sort();
  $lang.innerHTML = `<option value="">All languages</option>` + langs.map(l => `<option>${esc(l)}</option>`).join('');

  // URL params→controls
  const params = new URLSearchParams(location.search);
  $q.value   = params.get('search') || '';
  $lang.value= params.get('lang') || '';
  $sort.value= params.get('sort') || 'relevance';
  $min.value = params.get('min') || '';
  $max.value = params.get('max') || '';

  function apply(){
    const q = $q.value.trim().toLowerCase();
    const lang = $lang.value.trim();
    const min = parseFloat($min.value) || null;
    const max = parseFloat($max.value) || null;
    const sort = $sort.value;

    setParams({ search:q || null, lang:lang || null, sort, min: $min.value || null, max: $max.value || null });

    let ids = data.map(d=>d.id);
    if (q) {
      const terms = q.split(/\s+/);
      ids = index.filter(row => terms.every(t => row.hay.includes(t))).map(r => r.id);
    }
    // Filter language/price
    let rows = data.filter(d => ids.includes(d.id))
      .filter(d => !lang || (d.language||'')===lang)
      .filter(d => (min==null || (+d.price||1e9) >= min))
      .filter(d => (max==null || (+d.price||0) <= max));

    // Sort
    if (sort === 'title-asc') rows.sort((a,b)=>a.title.localeCompare(b.title));
    if (sort === 'date-desc') rows.sort((a,b)=>(b.date||'').localeCompare(a.date||''));
    if (sort === 'price-asc') rows.sort((a,b)=>(+a.price||1e9)-(+b.price||1e9));

    $count.textContent = `${rows.length} ${isAudio?'audiobooks':'ebooks'}`;
    renderCards(rows, $grid, isAudio);
    injectItemListJSONLD(rows.slice(0, 30), isAudio);
  }

  // Debounce typing
  let t; const deb = (fn)=>{ clearTimeout(t); t=setTimeout(fn, 120); };
  [$q,$lang,$sort,$min,$max].forEach(el => el.addEventListener('input', ()=>deb(apply)));
  apply();

  // Structured data: WebSite + SearchAction (sitewide)
  injectJSONLD({
    "@context":"https://schema.org",
    "@type":"WebSite",
    "url": SITE.base + '/',
    "name":"iD01t Productions",
    "potentialAction":{
      "@type":"SearchAction",
      "target": SITE.base + (isAudio?"/audiobooks.html":"/ebooks.html") + "?search={search_term_string}",
      "query-input":"required name=search_term_string"
    }
  });
}

function renderCards(rows, $grid, isAudio){
  if (!rows.length) {
    $grid.innerHTML = `<div class="empty">No results yet. Try fewer filters.</div>`;
    return;
  }
  $grid.innerHTML = rows.map(d => {
    const title = esc(d.title + (d.subtitle?`: ${d.subtitle}`:'')); 
    const price = fmtPrice(d.price);
    const lang  = esc(d.language||''); 
    const label = isAudio?'Audiobook':'eBook';
    const buy = esc(d.buy);
    const detail = `${SITE.pages.book}?id=${encodeURIComponent(d.id)}`;
    const img = esc(d.cover_hd);
    const srcset = `${img}&zoom=1 320w, ${img}&zoom=2 640w, ${img}&zoom=3 960w`;
    return `
    <article class="card" itemscope itemtype="${isAudio?'https://schema.org/Audiobook':'https://schema.org/Book'}">
      <a class="card-media" href="${detail}" aria-label="${title}">
        <img loading="lazy" decoding="async" src="${img}" srcset="${srcset}" sizes="(max-width:600px) 50vw, 220px"
             alt="${title} cover artwork" itemprop="image">
      </a>
      <div class="card-body">
        <h3 class="card-title" itemprop="name"><a href="${detail}">${title}</a></h3>
        <p class="card-sub" itemprop="author">${esc(d.contributors || '—')}</p>
        <div class="row">
          <span class="badge" title="Language">${lang||'—'}</span>
          <span class="badge" title="Format">${label}</span>
          ${price ? `<span class="badge" title="Price">${price}</span>`:''}
        </div>
        <div class="row" style="margin-top:10px">
          <a class="btn primary" href="${buy}" rel="noopener nofollow sponsored" target="_blank">Buy on Google Play</a>
          <a class="btn" href="${detail}" aria-label="Details for ${title}">Details</a>
        </div>
      </div>
    </article>`;
  }).join('');
}

function injectItemListJSONLD(items, isAudio){
  const elts = items.map((d,i)=>({
    "@type":"ListItem","position":i+1,
    "url": SITE.base + SITE.pages.book + "?id=" + encodeURIComponent(d.id),
    "name": d.title
  }));
  injectJSONLD({
    "@context":"https://schema.org",
    "@type":"ItemList",
    "itemListElement": elts
  });
}

// Detail page
async function bootstrapDetail(){
  if (SITE.mode() !== 'book') return;
  const id = param('id'); if (!id){ $('#detail').innerHTML = `<p class="empty">Missing id</p>`; return; }
  const data = await getCatalog();
  const d = data.find(x => x.id === id);
  if (!d){ $('#detail').innerHTML = `<p class="empty">Not found.</p>`; return; }
  const isAudio = d.format === 'Audiobook';

  document.title = `${d.title}${d.subtitle?`: ${d.subtitle}`:''} · ${isAudio?'Audiobook':'eBook'} · iD01t Productions`;
  const meta = (name,content)=>{ let m=$(`meta[name="${name}"]`); if(!m){m=document.createElement('meta');m.setAttribute('name',name);document.head.appendChild(m);} m.setAttribute('content',content); };
  const og = (p,c)=>{ let m=$(`meta[property="${p}"]`); if(!m){m=document.createElement('meta');m.setAttribute('property',p);document.head.appendChild(m);} m.setAttribute('content',c); };

  // OpenGraph/Twitter
  og('og:type','product');
  og('og:title', `${d.title}${d.subtitle?`: ${d.subtitle}`:''}`);
  og('og:url', location.href);
  og('og:image', d.cover_hd);
  meta('twitter:card','summary_large_image');

  // Render
  $('#detail').innerHTML = `
    <div class="detail" itemscope itemtype="${isAudio?'https://schema.org/Audiobook':'https://schema.org/Book'}">
      <div class="card">
        <div class="card-media"><img src="${esc(d.cover_hd)}" alt="${esc(d.title)} cover" itemprop="image" loading="eager" decoding="async"></div>
      </div>
      <div>
        <h1 class="h1" itemprop="name">${esc(d.title)}${d.subtitle?`: ${esc(d.subtitle)}`:''}</h1>
        <p class="muted" itemprop="author">${esc(d.contributors || '')}</p>
        <p class="tag">Publisher: <span itemprop="publisher">${esc(d.publisher||'')}</span></p>
        <p class="tag">Language: <span itemprop="inLanguage">${esc(d.language||'')}</span></p>
        ${d.date?`<p class="tag">Published: <time itemprop="datePublished" datetime="${esc(d.date)}">${esc(d.date)}</time></p>`:''}
        ${d.price?`<p class="tag" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
            <span itemprop="priceCurrency" content="USD"></span>Price: <span itemprop="price">${fmtPrice(d.price)}</span>
          </p>`:''}
        <div class="row" style="margin:16px 0;">
          <a class="btn primary" href="${esc(d.buy)}" target="_blank" rel="noopener nofollow sponsored">Buy on Google Play</a>
          <a class="btn" href="${history.length>1 ? 'javascript:history.back()' : (d.format==='Audiobook'?SITE.pages.audiobooks:SITE.pages.ebooks)}">Back to catalog</a>
        </div>
      </div>
    </div>`;

  // JSON‑LD entity
  injectJSONLD({
    "@context":"https://schema.org",
    "@type": isAudio ? "Audiobook" : "Book",
    "name": d.title + (d.subtitle?`: ${d.subtitle}`:''),
    "inLanguage": d.language || "en",
    "image": d.cover_hd,
    "author": d.contributors || undefined,
    "publisher": d.publisher || undefined,
    "datePublished": d.date || undefined,
    "workExample": {
      "@type": "CreativeWork",
      "url": d.buy
    },
    "offers": d.price ? {
      "@type":"Offer","priceCurrency":"USD","price": String(d.price),"url": d.buy,"availability":"https://schema.org/InStock"
    } : undefined
  });
}

// PWA
function setupSW(){
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js').catch(()=>{});
  }
}

document.addEventListener('DOMContentLoaded', ()=>{
  setupSW();
  bootstrapList();
  bootstrapDetail();
});
