// —— Replace your fetcher + init/bind with this ——

// Build an API query from UI state (audiobooks bias + user text)
function buildQuery(text) {
  const core = `(${[
    `inauthor:"${CONFIG.AUTHOR}"`,
    `inpublisher:"${CONFIG.PUBLISHER}"`
  ].join(' OR ')})`;
  const audioHints = '(audiobook OR "audio book" OR "spoken word" OR narrated OR unabridged OR abridged)';
  const user = (text || '').trim();
  return user ? `${core} ${audioHints} ${user}` : `${core} ${audioHints}`;
}

// Exponential backoff fetch
async function safeFetch(url, tries = 3) {
  let attempt = 0, lastErr;
  while (attempt < tries) {
    try {
      const res = await fetch(url, { cache: 'no-store' });
      if (res.ok) return res.json();
      // Retry on 429/5xx
      if (res.status === 429 || (res.status >= 500 && res.status < 600)) {
        throw new Error(`retryable:${res.status}`);
      }
      throw new Error(`Books API ${res.status}`);
    } catch (e) {
      lastErr = e;
      await new Promise(r => setTimeout(r, 250 * Math.pow(2, attempt))); // 250ms, 500ms, 1s
      attempt++;
    }
  }
  throw lastErr;
}

// Paged fetcher with langRestrict + newest ordering
async function fetchAllAudiobooksFromAPI({ text = '', lang = '' } = {}) {
  const q = buildQuery(text);
  let startIndex = 0, items = [];
  while (startIndex < CONFIG.MAX_TOTAL) {
    const p = new URLSearchParams({
      q,
      maxResults: CONFIG.PAGE_SIZE,
      startIndex,
      printType: 'books',
      orderBy: 'newest',
    });
    if (lang) p.set('langRestrict', lang);
    if (CONFIG.API_KEY) p.set('key', CONFIG.API_KEY);

    const url = `https://www.googleapis.com/books/v1/volumes?${p}`;
    const data = await safeFetch(url);
    const page = (data.items || []).filter(x => isAudioBook(x.volumeInfo || {}));
    items.push(...page);
    if (!data.items || data.items.length < CONFIG.PAGE_SIZE) break;
    startIndex += CONFIG.PAGE_SIZE;
  }
  return items;
}

// Bind: re-fetch on search or language changes (year/sort still client-side)
function bindDynamicFetch() {
  const refetch = async () => {
    try {
      const raw = await fetchAllAudiobooksFromAPI({ text: q.value, lang: language.value });
      const all = raw.map(normalize);
      populateLanguages(all);
      render(applyFilters(all), all);
    } catch (err) {
      console.warn('API failed, fallback → /assets/data/audiobooks.json', err);
      try {
        const r = await fetch('/assets/data/audiobooks.json', { cache: 'no-store' });
        const fb = await r.json();
        const all = (Array.isArray(fb) ? fb : (fb.items || [])).map(a => ({
          id: a.id || a.title,
          title: a.title,
          authors: (a.authors || a.narrators || []).join(', '),
          year: a.year,
          language: a.language,
          categories: [a.genre].filter(Boolean),
          snippet: a.description || '',
          infoLink: (a.googleBooks || a.googlePlay || a.url || '#'),
          image: a.cover
        }));
        populateLanguages(all);
        render(applyFilters(all), all);
      } catch (e2) {
        grid.innerHTML = '<div class="muted">Could not load audiobooks from API or fallback JSON.</div>';
        empty.hidden = false;
      }
    }
  };

  const debounce = (fn, ms) => { let t; return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); }; };
  const debounced = debounce(refetch, 200);

  ['input','change'].forEach(evt => [q, language].forEach(el => el.addEventListener(evt, debounced)));
  // Year/sort stay client-side
  ['input','change'].forEach(evt => [from, to, sort].forEach(el => el.addEventListener(evt, () => {
    const cards = document._abCache || [];
    render(applyFilters(cards), cards);
  })));
  clearBtn.addEventListener('click', () => { q.value=''; language.value=''; from.value=''; to.value=''; sort.value='date_desc'; debounced(); });

  // First load
  refetch();
}

// Init
async function init() {
  try {
    // First fetch uses current UI state (empty q/lang)
    const raw = await fetchAllAudiobooksFromAPI({ text: q.value, lang: language.value });
    if (!raw.length) throw new Error('No API items');
    const all = raw.map(normalize);
    document._abCache = all; // cache for client-side filters
    populateLanguages(all);
    render(applyFilters(all), all);
    bindDynamicFetch();
  } catch (err) {
    console.warn('API failed at init → fallback JSON', err);
    try {
      const r = await fetch('/assets/data/audiobooks.json', { cache: 'no-store' });
      const fb = await r.json();
      const all = (Array.isArray(fb) ? fb : (fb.items || [])).map(a => ({
        id: a.id || a.title, title: a.title, authors: (a.authors || a.narrators || []).join(', '),
        year: a.year, language: a.language, categories: [a.genre].filter(Boolean),
        snippet: a.description || '',
        infoLink: (a.googleBooks || a.googlePlay || a.url || '#'), image: a.cover
      }));
      document._abCache = all;
      populateLanguages(all);
      render(applyFilters(all), all);
      bindDynamicFetch();
    } catch (e2) {
      grid.innerHTML = '<div class="muted">Could not load audiobooks from API or fallback JSON.</div>';
      empty.hidden = false;
    }
  }
}
init();
