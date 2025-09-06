js = r"""/*! iD01t Productions — audiobooks.js (bullet-proof client) */
/* Place <script src="/assets/data/audiobooks.js"></script> near the end of <body> on audiobooks.html */

(function (window, document) {
  'use strict';

  // Configuration
  const CONFIG = {
    API_KEY: "AIzaSyBpG4uswyDjQXfZbIOfW7hwg2Il0RaUYYs", // <-- your Google Books API key
    AUTHOR: "Guillaume Lessard",
    PUBLISHER: "iD01t Productions",
    PAGE_SIZE: 40,
    MAX_PAGES: 5, // maxResults * MAX_PAGES will cap number of fetched items
    RETRIES: 3,
    TIMEOUT: 9000
  };

  // DOM helpers — these IDs must exist in audiobooks.html
  const ids = ['q','language','from','to','sort','reset','grid','empty','count','tally'];
  const $ = id => document.getElementById(id);
  const [q, language, from, to, sort, resetBtn, grid, empty, count, tally] = ids.map(id => $(id));

  // Safe text escaping
  const escapeHtml = str => String(str||'').replace(/[&<>"']/g, s => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]));

  // Minimal timeout-aware fetch
  function fetchWithTimeout(url, opts={}, timeout=CONFIG.TIMEOUT){
    const controller = new AbortController();
    const signal = controller.signal;
    const id = setTimeout(()=>controller.abort(), timeout);
    return fetch(url, Object.assign({}, opts, {signal, cache:'no-store'}))
      .finally(()=>clearTimeout(id));
  }

  // Exponential backoff wrapper
  async function fetchJsonWithRetries(url, opts={}, retries=CONFIG.RETRIES){
    let attempt = 0;
    let lastErr = null;
    while (attempt <= retries){
      try{
        const res = await fetchWithTimeout(url, opts);
        if (!res.ok) throw new Error('HTTP '+res.status);
        return await res.json();
      }catch(err){
        lastErr = err;
        attempt++;
        await new Promise(r => setTimeout(r, 200 * attempt));
      }
    }
    throw lastErr;
  }

  // Detect audiobook hints in volumeInfo (title, subtitle, categories, snippet)
  function isAudiobook(volumeInfo){
    if (!volumeInfo) return false;
    const hay = ((volumeInfo.title||'') + ' ' + (volumeInfo.subtitle||'') + ' ' + (volumeInfo.categories||[]).join(' ') + ' ' + (volumeInfo.description||'') + ' ' + (volumeInfo.searchInfo?.textSnippet||'')).toLowerCase();
    const hints = ['audiobook','audio book','spoken word','narrated','unabridged','abridged','read by','narrator'];
    return hints.some(h => hay.includes(h));
  }

  // Normalize Google Books item to our UI-friendly shape
  function normalize(item){
    const v = item.volumeInfo || {};
    const links = v.imageLinks || {};
    return {
      id: item.id,
      title: v.title || 'Untitled',
      subtitle: v.subtitle || '',
      authors: (v.authors || []).join(', '),
      year: (v.publishedDate||'').slice(0,4) || '',
      language: v.language || '',
      categories: v.categories || [],
      image: (links.thumbnail || links.smallThumbnail || '/assets/img/brand/ebooks.png').replace(/^http:/,'https:'),
      infoLink: (v.infoLink || v.canonicalVolumeLink || '#').replace(/^http:/,'https:'),
      audio: isAudiobook(v)
    };
  }

  // Try to detect a local landing page under /audiobooks/ for a title.
  async function resolveLocalLanding(a){
    // quick HEAD with small timeout
    async function exists(url){
      try{
        let res = await fetchWithTimeout(url, {method:'HEAD'}, 3500);
        if (res.ok) return true;
        // Fall back to GET if HEAD not allowed.
        res = await fetchWithTimeout(url, {method:'GET'}, 4500);
        return res.ok;
      }catch(e){ return false; }
    }
    const safe = s => (s||'').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/&/g,' and ').replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
    const titleSlug = safe(a.title);
    const authorSlug = safe((a.authors||'').split(',')[0]||'');
    const combos = [
      `/audiobooks/${titleSlug}.html`,
      `/audiobooks/${titleSlug}/index.html`,
      `/audiobooks/${authorSlug}-${titleSlug}.html`,
      `/audiobooks/${authorSlug}/${titleSlug}.html`
    ];
    const MAP = window.AUDIOBOOK_MAP || {};
    if (MAP[a.id]) {
      const m = MAP[a.id];
      if (await exists(m)) return m;
    }
    for (const p of combos){
      if (await exists(p)) return p;
    }
    return null;
  }

  // Render a single card
  function card(a){
    const chips = [a.language, ...(a.categories||[]).slice(0,1), a.audio ? 'Audiobook' : 'Book'].filter(Boolean);
    const href = a.localUrl || a.infoLink || '#';
    return `
      <article class="rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden bg-white dark:bg-slate-900 flex flex-col card">
        <img src="${escapeHtml(a.image)}" alt="${escapeHtml(a.title)} cover" class="w-full aspect-[3/4] object-cover">
        <div class="p-4 flex-1 flex flex-col">
          <h3 class="font-semibold leading-snug">${escapeHtml(a.title)}</h3>
          <p class="text-xs text-slate-500 mt-1">${escapeHtml(a.authors)}</p>
          <div class="mt-2 flex flex-wrap gap-2">${chips.map(c=>`<span class="text-xs rounded-full border border-slate-300 dark:border-slate-700 px-2 py-0.5">${escapeHtml(c)}</span>`).join('')}</div>
          <div class="mt-auto pt-4 flex items-center justify-between gap-2">
            <span class="text-sm text-slate-500">${escapeHtml(a.year)}</span>
            <div class="flex items-center gap-2">
              <a href="${href}" class="rounded-full bg-brand-600 hover:bg-brand-700 text-white px-4 py-2 text-sm">Details</a>
              <a href="${escapeHtml(a.infoLink)}" target="_blank" rel="noopener nofollow" class="text-sm underline">Google Books</a>
            </div>
          </div>
        </div>
      </article>
    `;
  }

  // Emit JSON-LD ItemList for the first items (improves rich results)
  function emitSchema(items){
    try{
      const ld = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'name': 'Audiobooks',
        'itemListElement': items.slice(0,60).map((a,i)=>({ '@type':'ListItem','position': i+1, 'item': {'@type':'Audiobook','name': a.title, 'inLanguage': a.language, 'datePublished': a.year || undefined, 'image': a.image, 'url': a.localUrl || a.infoLink }}))
      };
      let el = document.getElementById('ld-audiobooks');
      if (!el){
        el = document.createElement('script');
        el.id = 'ld-audiobooks';
        el.type = 'application/ld+json';
        document.head.appendChild(el);
      }
      el.textContent = JSON.stringify(ld);
    }catch(e){ /* no-op on schema fail */ }
  }

  // Apply active filters and sorting
  function applyFilters(items){
    const text = (q && q.value || '').trim().toLowerCase();
    const langVal = language ? language.value : '';
    const f = parseInt(from ? from.value : '') || 0;
    const t = parseInt(to ? to.value : '') || 0;
    let list = items.filter(x => {
      if (!x) return false;
      if (text){
        const hay = `${x.title} ${x.authors} ${(x.categories||[]).join(' ')}`.toLowerCase();
        if (!hay.includes(text)) return false;
      }
      if (langVal && x.language !== langVal) return false;
      if (f && (parseInt(x.year) || 0) < f) return false;
      if (t && (parseInt(x.year) || 0) > t) return false;
      return x.audio; // ensure audiobooks only
    });
    const sortVal = sort ? sort.value : 'date_desc';
    if (sortVal === 'date_asc') list.sort((a,b) => (a.year||0)-(b.year||0));
    else if (sortVal === 'title_asc') list.sort((a,b)=>a.title.localeCompare(b.title));
    else if (sortVal === 'title_desc') list.sort((a,b)=>b.title.localeCompare(a.title));
    else list.sort((a,b)=>(parseInt(b.year)||0)-(parseInt(a.year)||0));
    return list;
  }

  // Render list to grid
  function render(list, all){
    if (!grid) return;
    if (!list || !list.length){
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
    emitSchema(list, all);
  }

  // Bind UI controls
  function bindControls(all){
    const onChange = ()=>render(applyFilters(all), all);
    [q, language, from, to, sort].forEach(elm=>{ if(elm) elm.addEventListener('input', onChange); elm && elm.addEventListener('change', onChange); });
    if (resetBtn) resetBtn.addEventListener('click', ()=>{ if(q) q.value=''; if(language) language.value=''; if(from) from.value=''; if(to) to.value=''; if(sort) sort.value='date_desc'; render(applyFilters(all), all); });
  }

  // Fetch pages from Google Books
  async function fetchAllFromBooksAPI(){
    const items = [];
    const qBase = `inauthor:"${CONFIG.AUTHOR}" OR inpublisher:"${CONFIG.PUBLISHER}"`;
    for (let page=0; page < CONFIG.MAX_PAGES; page++){
      const start = page * CONFIG.PAGE_SIZE;
      const params = new URLSearchParams({ q: qBase, maxResults: CONFIG.PAGE_SIZE, startIndex: String(start), projection: 'full', printType: 'books' });
      if (CONFIG.API_KEY) params.set('key', CONFIG.API_KEY);
      const url = `https://www.googleapis.com/books/v1/volumes?${params.toString()}`;
      try{
        const data = await fetchJsonWithRetries(url, {}, CONFIG.RETRIES);
        if (!data || !data.items || !data.items.length) break;
        items.push(...data.items);
        if (data.items.length < CONFIG.PAGE_SIZE) break;
      }catch(err){
        // Re-throw to allow caller to fallback to JSON
        throw err;
      }
    }
    return items;
  }

  // Main init: try API, then fallback to AUDIOBOOK_FALLBACK or JSON file
  async function init(){
    // show loading skeleton
    if (grid) grid.innerHTML = '<div class="p-8 text-slate-500">Loading audiobooks…</div>';
    let raw = null;
    try{
      raw = await fetchAllFromBooksAPI();
      raw = raw || [];
      let all = raw.map(normalize);
      // Resolve local landing pages in small batches for performance
      for (let i=0;i<all.length;i+=6){
        await Promise.all(all.slice(i,i+6).map(async a=>{ a.localUrl = await resolveLocalLanding(a); }));
      }
      bindControls(all);
      render(applyFilters(all), all);
      return;
    }catch(apiErr){
      // Try window fallback injected by audiobooks.js dataset
    }

    try{
      if (window.AUDIOBOOK_FALLBACK && Array.isArray(window.AUDIOBOOK_FALLBACK.items)){
        const fb = window.AUDIOBOOK_FALLBACK.items;
        const all = fb.map(a=>({ id: a.id||a.title, title: a.title, authors: (a.authors||a.narrators||[]).join(', '), year: a.year, language: a.language, categories: [a.genre].filter(Boolean), infoLink: a.googleBooks||a.googlePlay||a.url||'#', image: a.cover, audio: true, localUrl: a.url }));
        bindControls(all); render(applyFilters(all), all); return;
      }
    }catch(e){ /* continue to next fallback */ }

    try{
      const res = await fetchWithTimeout('/assets/data/audiobooks.json',{},7000);
      if (res.ok){
        const fb = await res.json();
        const arr = Array.isArray(fb) ? fb : (fb.items || []);
        const all = arr.map(a=>({ id: a.id||a.title, title: a.title, authors: (a.authors||a.narrators||[]).join(', '), year: a.year, language: a.language, categories: [a.genre].filter(Boolean), infoLink: a.googleBooks||a.googlePlay||a.url||'#', image: a.cover, audio: true, localUrl: a.url }));
        bindControls(all); render(applyFilters(all), all); return;
      }
    }catch(e){ /* final fallback below */ }

    // Final fallback: show a friendly error and allow manual refresh
    if (grid) grid.innerHTML = '<div class="p-8 text-slate-500">Could not load audiobooks. Please refresh or try again later.</div>';
    empty && empty.classList.remove('hidden');
  }

  // Start
  document.addEventListener('DOMContentLoaded', function(){
    // Preconnect to Google APIs to reduce latency
    try{ const l=document.createElement('link'); l.rel='preconnect'; l.href='https://www.googleapis.com'; document.head.appendChild(l);}catch(e){}
    init().catch(e=>{ console.error('Audiobooks init error', e); });
  });

})(window, document);
"""
