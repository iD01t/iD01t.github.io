/*! iD01t Productions — audiobooks.client.js (HD Images Fixed) */
(function (window, document) {
  'use strict';

  // ---- Configuration -------------------------------------------------------
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

  // ---- HD Image Generator --------------------------------------------------
  function generateHDCover(title, author, genre = 'Audiobook', color = null) {
    const colors = [
      '#1e3a8a', '#7c3aed', '#059669', '#dc2626', '#ea580c',
      '#0891b2', '#be185d', '#4338ca', '#65a30d', '#ca8a04'
    ];
    const bgColor = color || colors[Math.abs(hashString(title)) % colors.length];
    const textColor = '#ffffff';
    
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 600;
    const ctx = canvas.getContext('2d');
    
    // Background gradient
    const gradient = ctx.createLinearGradient(0, 0, 400, 600);
    gradient.addColorStop(0, bgColor);
    gradient.addColorStop(1, darkenColor(bgColor, 0.3));
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 400, 600);
    
    // Add subtle pattern overlay
    ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
    for (let i = 0; i < 20; i++) {
      ctx.fillRect(i * 40, 0, 20, 600);
    }
    
    // Title text
    ctx.fillStyle = textColor;
    ctx.font = 'bold 32px Arial, sans-serif';
    ctx.textAlign = 'center';
    
    const maxWidth = 360;
    const words = title.split(' ');
    let lines = [];
    let currentLine = words[0];
    
    for (let i = 1; i < words.length; i++) {
      const testLine = currentLine + ' ' + words[i];
      const metrics = ctx.measureText(testLine);
      if (metrics.width > maxWidth) {
        lines.push(currentLine);
        currentLine = words[i];
      } else {
        currentLine = testLine;
      }
    }
    lines.push(currentLine);
    
    const startY = 200 - (lines.length * 20);
    lines.forEach((line, index) => {
      ctx.fillText(line, 200, startY + (index * 40));
    });
    
    // Author text
    ctx.font = 'normal 18px Arial, sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillText(author, 200, 350);
    
    // Genre badge
    ctx.font = 'bold 14px Arial, sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.fillRect(50, 420, 300, 30);
    ctx.fillStyle = textColor;
    ctx.fillText(genre.toUpperCase(), 200, 440);
    
    // Audio indicator
    ctx.font = 'bold 16px Arial, sans-serif';
    ctx.fillStyle = '#fbbf24';
    ctx.fillText('🎧 AUDIOBOOK', 200, 480);
    
    return canvas.toDataURL('image/png');
  }

  function hashString(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }

  function darkenColor(color, amount) {
    const hex = color.replace('#', '');
    const r = Math.max(0, parseInt(hex.substr(0, 2), 16) * (1 - amount));
    const g = Math.max(0, parseInt(hex.substr(2, 2), 16) * (1 - amount));
    const b = Math.max(0, parseInt(hex.substr(4, 2), 16) * (1 - amount));
    return `rgb(${Math.floor(r)}, ${Math.floor(g)}, ${Math.floor(b)})`;
  }

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
    try { 
      return await fetch(url, Object.assign({ cache:'no-store' }, opts, { signal: ctrl.signal })); 
    } finally { 
      clearTimeout(id); 
    }
  }

  function normalizeCover(src) {
    if (!src) return src;
    let s = String(src).trim();
    s = s.replace(/^\/assets\/harvested\/(?:ebooks|audiobooks)\/(https?:\/\/.*)$/i, '$1');
    if (/^https?:\/\//i.test(s)) {
      const hasExt = /\.[a-z]{3,4}(\?.*)?$/i.test(s);
      const isImgurRaw = /^https?:\/\/i\.imgur\.com\/[^.\/\s?]+(?:\?.*)?$/i.test(s);
      if (isImgurRaw && !hasExt) s += '.png';
      return s;
    }
    if (/^\/.+\.(png|jpe?g|webp|avif|gif)(\?.*)?$/i.test(s)) return s;
    return s;
  }

  // ---- Image handling with HD fallbacks -----------------------------------
  async function getWorkingImage(imageUrl, title, author, genre) {
    const normalizedUrl = normalizeCover(imageUrl);
    if (!normalizedUrl) {
      return generateHDCover(title, author, genre);
    }

    imageUrl = normalizedUrl;

    try {
      // Test if the image URL works
      const response = await fetch(imageUrl, { method: 'HEAD', timeout: 3000 });
      if (response.ok) {
        return imageUrl;
      }
    } catch (e) {
      // Image failed, continue to fallback
    }

    // Try alternative Google Books image URLs
    if (imageUrl.includes('books.google')) {
      const alternatives = [
        imageUrl.replace('&edge=curl', '').replace('zoom=1', 'zoom=2'),
        imageUrl.replace('thumbnail', 'small').replace('zoom=1', 'zoom=3'),
        imageUrl.replace('zoom=1', 'zoom=5')
      ];
      
      for (const alt of alternatives) {
        try {
          const response = await fetch(alt, { method: 'HEAD', timeout: 2000 });
          if (response.ok) return alt;
        } catch (e) {
          continue;
        }
      }
    }

    // Generate HD placeholder as final fallback
    return generateHDCover(title, author, genre);
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

  async function normalize(item){
    const v = item.volumeInfo || {}, links = v.imageLinks || {};
    const title = v.title || 'Untitled';
    const authors = (v.authors || []).join(', ');
    const genre = (v.categories || ['Audiobook'])[0];
    
    // Get working HD image
    const originalImage = links.thumbnail || links.smallThumbnail || links.medium || links.large;
    const workingImage = await getWorkingImage(originalImage, title, authors, genre);
    
    return {
      id: item.id,
      title: title,
      authors: authors,
      year: (v.publishedDate||'').slice(0,4) || '',
      language: v.language || '',
      categories: v.categories || [],
      image: workingImage,
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
      <article class="rounded-2xl border border-slate-200 dark:border-slate-800 overflow-hidden bg-white dark:bg-slate-900 flex flex-col shadow-lg hover:shadow-xl transition-shadow">
        <div class="relative overflow-hidden">
          <img 
            src="${escapeHtml(a.image)}" 
            alt="${escapeHtml(a.title)} cover" 
            class="w-full aspect-[3/4] object-cover hover:scale-105 transition-transform duration-300"
            loading="lazy"
            onerror="this.src='${generateHDCover(a.title, a.authors, (a.categories||['Audiobook'])[0])}'"
          >
          <div class="absolute top-2 right-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded text-xs">
            🎧 HD
          </div>
        </div>
        <div class="p-4 flex-1 flex flex-col">
          <h3 class="font-semibold leading-snug line-clamp-2">${escapeHtml(a.title)}</h3>
          <p class="text-xs text-slate-500 mt-1">${escapeHtml(a.authors||'')}</p>
          <div class="mt-2 flex flex-wrap gap-2">
            ${chips.map(c=>`<span class="text-xs rounded-full border border-slate-300 dark:border-slate-700 px-2 py-0.5">${escapeHtml(c)}</span>`).join('')}
          </div>
          <div class="mt-auto pt-4 flex items-center justify-between gap-2">
            <span class="text-sm text-slate-500">${escapeHtml(a.year)}</span>
            <div class="flex items-center gap-2">
              <a href="${href}" class="rounded-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 text-sm transition-colors">
                Details
              </a>
              <a href="${escapeHtml(a.infoLink)}" target="_blank" rel="noopener nofollow" class="text-sm underline hover:text-blue-600">
                Google Books
              </a>
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
      const ld = {
        '@context':'https://schema.org',
        '@type':'ItemList',
        'name':'HD Audiobooks Collection',
        itemListElement: items.slice(0,60).map((a,i)=>({
          '@type':'ListItem',
          position:i+1,
          item:{
            '@type':'Audiobook',
            name:a.title,
            author: a.authors,
            inLanguage:a.language,
            datePublished:a.year||undefined,
            image:a.image,
            url:a.localUrl||a.infoLink
          }
        }))
      };
      
      let el = document.getElementById('ld-audiobooks');
      if (!el){ 
        el = document.createElement('script'); 
        el.id='ld-audiobooks'; 
        el.type='application/ld+json'; 
        document.head.appendChild(el); 
      }
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
    [q, language, from, to, sort].forEach(el => { 
      if (!el) return; 
      el.addEventListener('input', again); 
      el.addEventListener('change', again); 
    });
    
    if (resetBtn){ 
      resetBtn.addEventListener('click', ()=>{ 
        if(q) q.value=''; 
        if(language) language.value=''; 
        if(from) from.value=''; 
        if(to) to.value=''; 
        if(sort) sort.value='date_desc'; 
        again(); 
      }); 
    }
  }

  // ---- Google Books fetch with retries ------------------------------------
  async function fetchAllFromBooksAPI(){
    const base = `inauthor:"${CFG.AUTHOR}" OR inpublisher:"${CFG.PUBLISHER}"`;
    const items = [];
    
    for (let page=0; page<CFG.MAX_PAGES; page++){
      const start = page * CFG.PAGE_SIZE;
      const params = new URLSearchParams({ 
        q: base, 
        maxResults: CFG.PAGE_SIZE, 
        startIndex: String(start), 
        projection: 'full', 
        printType: 'books', 
        key: CFG.API_KEY 
      });
      const url = `https://www.googleapis.com/books/v1/volumes?${params.toString()}`;
      
      let ok = false, data = null;
      for (let attempt=0; attempt<CFG.RETRIES && !ok; attempt++){
        try {
          const res = await fetchWithTimeout(url, {}, CFG.TIMEOUT);
          if (!res.ok) throw new Error('HTTP '+res.status);
          data = await res.json(); 
          ok = true;
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

  // ---- Enhanced fallback loaders ------------------------------------------
  async function loadWindowFallback(){
    try{
      if (window.AUDIOBOOK_FALLBACK && Array.isArray(window.AUDIOBOOK_FALLBACK.items)){
        const fb = window.AUDIOBOOK_FALLBACK.items;
        const processed = await Promise.all(fb.map(async a => {
          const workingImage = await getWorkingImage(a.cover, a.title, (a.authors || []).join(', '), a.genre);
          return {
            id: a.id || a.title,
            title: a.title,
            authors: (a.authors || a.narrators || []).join(', '),
            year: String(a.year || ''),
            language: a.language,
            categories: [a.genre].filter(Boolean),
            image: workingImage,
            infoLink: a.googleBooks || a.googlePlay || a.url || '#',
            audio: true,
            localUrl: a.url || null
          };
        }));
        return processed;
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
      
      const processed = await Promise.all(arr.map(async a => {
        const workingImage = await getWorkingImage(a.cover, a.title, (a.authors || []).join(', '), a.genre);
        return {
          id: a.id || a.title,
          title: a.title,
          authors: (a.authors || a.narrators || []).join(', '),
          year: String(a.year || ''),
          language: a.language,
          categories: [a.genre].filter(Boolean),
          image: workingImage,
          infoLink: a.googleBooks || a.googlePlay || a.url || '#',
          audio: true,
          localUrl: a.url || null
        };
      }));
      return processed;
    }catch(e){ 
      return null; 
    }
  }

  // ---- Init ----------------------------------------------------------------
  async function init(){
    if (grid) grid.innerHTML = '<div id="loading" class="p-8 text-center"><div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div><p class="mt-2 text-slate-500">Loading HD audiobooks…</p></div>';
    
    try{
      console.log('Fetching from Google Books API...');
      const raw = await fetchAllFromBooksAPI();
      console.log(`Found ${raw.length} items from API`);
      
      // Process items in batches for better performance
      const batchSize = 5;
      const all = [];
      
      for (let i = 0; i < raw.length; i += batchSize) {
        const batch = raw.slice(i, i + batchSize);
        const processed = await Promise.all(batch.map(normalize));
        all.push(...processed.filter(x => x.audio));
        
        // Show progress
        if (grid && i % 10 === 0) {
          const progress = Math.round((i / raw.length) * 100);
          grid.innerHTML = `<div class="p-8 text-center"><div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div><p class="mt-2 text-slate-500">Processing images... ${progress}%</p></div>`;
        }
      }
      
      // Resolve local landing pages in batches
      for (let i=0;i<all.length;i+=6){
        await Promise.all(all.slice(i,i+6).map(async a => { 
          a.localUrl = await resolveLocalLanding(a); 
        }));
      }
      
      console.log(`Processed ${all.length} audiobooks with HD images`);
      populateLanguages(all);
      bind(all);
      render(applyFilters(all), all);
      return;
      
    }catch(apiErr){
      console.log('API failed, trying fallbacks...', apiErr);
    }
    
    // Try fallbacks with HD image processing
    let fb = await loadWindowFallback();
    if (!fb) fb = await loadJsonFallback();
    
    if (fb && fb.length){
      console.log(`Loaded ${fb.length} audiobooks from fallback with HD images`);
      populateLanguages(fb); 
      bind(fb); 
      render(applyFilters(fb), fb);
    } else {
      if (grid) grid.innerHTML = '<div class="p-8 text-center text-slate-500">Could not load audiobooks. Please try again later.</div>';
      empty && empty.classList.remove('hidden');
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})(window, document);