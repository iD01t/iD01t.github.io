/*! iD01t Productions — audiobooks.client.js (bullet‑proof Google Books client) */
(function (window, document) {
  'use strict';

  // ---- Configuration -------------------------------------------------------
  // 1) Preferred: set window.AUDIOBOOKS_CONFIG = { API_KEY: '...', AUTHOR: '...', PUBLISHER: '...' } before this script
  // 2) Or add: <meta name="google-books-api-key" content="YOUR_KEY">
  // 3) Fallback uses the inline constant below.
  const META_KEY = (document.querySelector('meta[name="google-books-api-key"]') || {}).content;
  const CFG = Object.assign({
    API_KEY: META_KEY || (window.AUDIOBOOKS_CONFIG && window.AUDIOBOOKS_CONFIG.API_KEY) || "AIzaSyBpG4uswyDjQXfZbIOfW7hwg2Il0RaUYYs",
    AUTHOR: (window.AUDIOBOOKS_CONFIG && window.AUDIOBOOKS_CONFIG.AUTHOR) || "Guillaume Lessard",
    PUBLISHER: (window.AUDIOBOOKS_CONFIG && window.AUDIOBOOKS_CONFIG.PUBLISHER) || "iD01t Productions",
    PAGE_SIZE: 40,
    MAX_PAGES: 5,
    RETRIES: 3,
    TIMEOUT: 9000
  }, window.AUDIOBOOKS_CONFIG || {});

  // ---- DOM -----------------------------------------------------------------
  const $ = id => document.getElementById(id);
  const q = $('q'), language = $('language'), from = $('from'), to = $('to'), sort = $('sort');
  const resetBtn = $('reset'), grid = $('grid'), empty = $('empty'), count = $('count'), tally = $('tally');

  // ---- Utils ---------------------------------------------------------------
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  function escapeHtml(s){ return String(s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;','\'':'&#39;'}[c])); }
  async function fetchWithTimeout(url, opts={}, timeout=CFG.TIMEOUT){
    const ctrl = new AbortController();
    const id = setTimeout(()=>ctrl.abort(), timeout);
    try { return await fetch(url, Object.assign({ cache:'no-store' }, opts, { signal: ctrl.signal })); }
    finally { clearTimeout(id); }
  }

  // ---- Local landing page resolver ----------------------------------------
  async function resolveLocalLanding(a){
    async function exists(url){
      try {
        let r = await fetchWithTimeout(url, {method:'HEAD'}, 3500);
        if (r.ok) return true;
        r = await fetchWithTimeout(url, {method:'GET'}, 4500);
        return r.ok;
      } catch(_) { return false; }
    }
    const safe = s => (s||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/&/g,' and ').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
    const t = safe(a.title);
    const auth = safe((a.authors||'').split(',')[0]||'');
    const combos = [
      `/audiobooks/${t}.html`,
      `/audiobooks/${t}/index.html`,
      `/audiobooks/${auth}-${t}.html`,
      `/audiobooks/${auth}/${t}.html`
    ];
    const MAP = window.AUDIOBOOK_MAP || {};
    if (MAP[a.id] && await exists(MAP[a.id])) return MAP[a.id];
    for (const p of combos) if (await exists(p)) return p;
    return null;
  }

  // ---- Audiobook detection + normalization --------------------------------
  function isAudiobook(v){
    const hay = ((v.title||'')+' '+(v.subtitle||'')+' '+(v.categories||[]).join(' ')+' '+(v.description||'')+' '+(v.searchInfo?.textSnippet||'')).toLowerCase();
    const hints = ['audiobook','audio book','spoken word','narrated','unabridged','abridged','read by','narrator'];
    return hints.some(h => hay.includes(h));
  }
  function normalize(item){
    const v = item.volumeInfo || {}, links = v.imageLinks || {};
    return {
      id: item.id,
      title: v.title || 'Untitled',
      authors: (v.authors || []).join(', '),
      year: (v.publishedDate||'').slice(0,4) || '',
      language: v.language || '',
      categories: v.categories || [],
      image: (links.thumbnail || links.smallThumbnail || '/assets/img/brand/ebooks.png').replace(/^http:/,'https:'),
      infoLink: (v.infoLink || v.canonicalVolumeLink || '#').replace(/^http:/,'https:'),
      audio: isAudiobook(v)
    };
  }

  // ---- UI helpers ----------------------------------------------------------
  function populateLanguages(items){
    const langs = Array.from(new Set(items.map(x=>x.language).filter(Boolean))).sort();
    language.innerHTML = '<option value="">All languages</option>' + langs.map(l=>`<option value="${l}">${l}</option>`).join('');
  }
  function card(a){
    const chips = [a.language, ...(a.categories||[]).slice(0,1), a.audio ? 'Audiobook' : 'Book'].filter(Boolean);
    const href = a.localUrl || a.infoLink || '#';
    return `
      <article class="rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden bg-white dark:bg-slate-900 flex flex-col">
        <img src="${escapeHtml(a.image)}" alt="${escapeHtml(a.title)} cover" class="w-full aspect-[3/4] object-cover">
        <div class="p-4 flex-1 flex flex-col">
          <h3 class="font-semibold leading-snug">${escapeHtml(a.title)}</h3>
          <p class="text-xs text-slate-500 mt-1">${escapeHtml(a.authors||'')}</p>
          <div class="mt-2 flex flex-wrap gap-2">${chips.map(c=>`<span class="text-xs rounded-full border border-slate-300 dark:border-slate-700 px-2 py-0.5">${escapeHtml(c)}</span>`).join('')}</div>
          <div class="mt-auto pt-4 flex items-center justify-between gap-2">
            <span class="text-sm text-slate-500">${escapeHtml(a.year)}</span>
            <div class="flex items-center gap-2">
              <a href="${href}" class="rounded-full bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 text-sm">Details</a>
              <a href="${escapeHtml(a.infoLink)}" target="_blank" rel="noopener nofollow" class="text-sm underline">Google Books</a>
            </div>
          </div>
        </div>
      </article>`;
  }
  function applyFilters(items){
    const text = (q && q.value || '').toLowerCase();
    const lang = language && language.value;
    const f = parseInt(from && from.value || '') || 0;
    const t = parseInt(to && to.value || '') || 0;
    const s = (sort && sort.value) || 'date_desc';
    let list = items.filter(x=>{
      if (text){
        const hay = `${x.title} ${x.authors} ${(x.categories||[]).join(' ')}`.toLowerCase();
        if (!hay.includes(text)) return false;
      }
      if (lang && x.language !== lang) return false;
      const yr = parseInt(x.year||'')||0;
      if (f && yr < f) return false;
      if (t && yr > t) return false;
      return x.audio;
    });
    if (s==='date_asc') list.sort((a,b)=>(parseInt(a.year)||0)-(parseInt(b.year)||0));
    else if (s==='title_asc') list.sort((a,b)=>a.title.localeCompare(b.title));
    else if (s==='title_desc') list.sort((a,b)=>b.title.localeCompare(a.title));
    else list.sort((a,b)=>(parseInt(b.year)||0)-(parseInt(a.year)||0));
    return list;
  }
  function emitSchema(items){
    try{
      const ld = {'@context':'https://schema.org','@type':'ItemList','name':'Audiobooks',
        itemListElement: items.slice(0,60).map((a,i)=>({'@type':'ListItem',position:i+1,item:{'@type':'Audiobook',name:a.title,inLanguage:a.language,datePublished:a.year||undefined,image:a.image,url:a.localUrl||a.infoLink}}))
      };
      let el = document.getElementById('ld-audiobooks');
      if (!el){ el = document.createElement('script'); el.id='ld-audiobooks'; el.type='application/ld+json'; document.head.appendChild(el); }
      el.textContent = JSON.stringify(ld);
    }catch(e){}
  }
  function render(list, all){
    if (!grid) return;
    const loading = document.getElementById('loading');
    loading && loading.remove();
    if (!list.length){
      grid.innerHTML = '';
      empty && empty.classList.remove('hidden');
      count && (count.textContent = '0 audiobooks');
      tally && (tally.textContent = `${all.length} titles • ${all.filter(x=>x.audio).length} audiobooks`);
      return;
    }
    empty && empty.classList.add('hidden');
    grid.innerHTML = list.map(card).join('');
    count && (count.textContent = `${list.length} audiobook${list.length!==1?'s':''}`);
    tally && (tally.textContent = `${all.length} titles • ${all.filter(x=>x.audio).length} audiobooks`);
    emitSchema(list);
  }
  function bind(all){
    const again = () => render(applyFilters(all), all);
    [q, language, from, to, sort].forEach(el => { if (!el) return; el.addEventListener('input', again); el.addEventListener('change', again); });
    if (resetBtn){ resetBtn.addEventListener('click', ()=>{ if(q) q.value=''; if(language) language.value=''; if(from) from.value=''; if(to) to.value=''; if(sort) sort.value='date_desc'; again(); }); }
  }

  // ---- Google Books fetch with retries ------------------------------------
  async function fetchAllFromBooksAPI(){
    const base = `inauthor:"${CFG.AUTHOR}" OR inpublisher:"${CFG.PUBLISHER}"`;
    const items = [];
    for (let page=0; page<CFG.MAX_PAGES; page++){
      const start = page * CFG.PAGE_SIZE;
      const params = new URLSearchParams({ q: base, maxResults: CFG.PAGE_SIZE, startIndex: String(start), projection: 'full', printType: 'books', key: CFG.API_KEY });
      const url = `https://www.googleapis.com/books/v1/volumes?${params.toString()}`;
      let ok = false, data = null;
      for (let attempt=0; attempt<CFG.RETRIES && !ok; attempt++){
        try {
          const res = await fetchWithTimeout(url, {}, CFG.TIMEOUT);
          if (!res.ok) throw new Error('HTTP '+res.status);
          data = await res.json(); ok = true;
        } catch(e){
          await sleep(200*(attempt+1));
        }
      }
      if (!ok) throw new Error('Books API unavailable');
      const pageItems = (data && data.items) ? data.items : [];
      items.push(...pageItems);
      if (pageItems.length < CFG.PAGE_SIZE) break;
    }
    return items;
  }

  // ---- Fallback loaders ----------------------------------------------------
  async function loadWindowFallback(){
    try{
      if (window.AUDIOBOOK_FALLBACK && Array.isArray(window.AUDIOBOOK_FALLBACK.items)){
        const fb = window.AUDIOBOOK_FALLBACK.items;
        return fb.map(a => ({
          id: a.id || a.title,
          title: a.title,
          authors: (a.authors || a.narrators || []).join(', '),
          year: a.year,
          language: a.language,
          categories: [a.genre].filter(Boolean),
          image: a.cover || '/assets/img/brand/ebooks.png',
          infoLink: a.googleBooks || a.googlePlay || a.url || '#',
          audio: true,
          localUrl: a.url || null
        }));
      }
    }catch(e){}
    return null;
  }
  async function loadJsonFallback(){
    try{
      const res = await fetchWithTimeout('/assets/data/audiobooks.json', {}, 8000);
      if (!res.ok) return null;
      const data = await res.json();
      const arr = Array.isArray(data) ? data : (data.items || []);
      return arr.map(a => ({
        id: a.id || a.title,
        title: a.title,
        authors: (a.authors || a.narrators || []).join(', '),
        year: a.year,
        language: a.language,
        categories: [a.genre].filter(Boolean),
        image: a.cover || '/assets/img/brand/ebooks.png',
        infoLink: a.googleBooks || a.googlePlay || a.url || '#',
        audio: true,
        localUrl: a.url || null
      }));
    }catch(e){ return null; }
  }

  // ---- Init ----------------------------------------------------------------
  async function init(){
    if (grid) grid.innerHTML = '<div class="p-4 text-slate-500">Loading audiobooks…</div>';
    try{
      const raw = await fetchAllFromBooksAPI();
      let all = raw.map(normalize).filter(x => x.audio);
      for (let i=0;i<all.length;i+=6){
        await Promise.all(all.slice(i,i+6).map(async a => { a.localUrl = await resolveLocalLanding(a); }));
      }
      populateLanguages(all);
      bind(all);
      render(applyFilters(all), all);
      return;
    }catch(apiErr){
      // continue to fallbacks
    }
    let fb = await loadWindowFallback();
    if (!fb) fb = await loadJsonFallback();
    if (fb && fb.length){
      populateLanguages(fb); bind(fb); render(applyFilters(fb), fb);
    } else {
      if (grid) grid.innerHTML = '<div class="p-4 text-slate-500">Could not load audiobooks. Please try again later.</div>';
      empty && empty.classList.remove('hidden');
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})(window, document);
