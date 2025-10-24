/**
 * Catalog application for iD01t Productions
 * Handles ebooks/audiobooks catalog display, search, filtering, and SEO
 */

const SITE = {
  base: location.origin,
  pages: {
    ebooks: '/ebooks.html',
    audiobooks: '/audiobooks.html',
    book: '/book.html'
  },
  dataUrl: '/data/catalog.json',
  
  // Determine current page mode
  mode() {
    const p = location.pathname.toLowerCase();
    if (p.endsWith('/ebooks.html')) return 'ebooks';
    if (p.endsWith('/audiobooks.html')) return 'audiobooks';
    if (p.endsWith('/book.html')) return 'book';
    return 'other';
  }
};

// Fetch catalog with session storage caching
async function getCatalog() {
  const cacheKey = 'catalog.v1';
  const cached = sessionStorage.getItem(cacheKey);
  
  if (cached) {
    try {
      return JSON.parse(cached);
    } catch (e) {
      console.warn('Cache parse error:', e);
    }
  }
  
  try {
    const res = await fetch(SITE.dataUrl, { 
      credentials: 'omit', 
      cache: 'no-store' 
    });
    
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    
    const json = await res.json();
    sessionStorage.setItem(cacheKey, JSON.stringify(json));
    return json;
  } catch (error) {
    console.error('Failed to load catalog:', error);
    throw error;
  }
}

// Helper functions
function $(sel, root = document) {
  return root.querySelector(sel);
}

function $all(sel, root = document) {
  return [...root.querySelectorAll(sel)];
}

function esc(s = '') {
  return (s + '').replace(/[&<>"']/g, c => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[c]));
}

function fmtPrice(p) {
  if (!p || isNaN(+p)) return '';
  return `$${(+p).toFixed(2)}`;
}

function param(name) {
  return new URLSearchParams(location.search).get(name);
}

function setParams(obj) {
  const url = new URL(location.href);
  for (const [k, v] of Object.entries(obj)) {
    if (v === null || v === undefined || v === '') {
      url.searchParams.delete(k);
    } else {
      url.searchParams.set(k, v);
    }
  }
  history.replaceState({}, '', url);
}

// Inject JSON-LD structured data
function injectJSONLD(obj) {
  const script = document.createElement('script');
  script.type = 'application/ld+json';
  script.textContent = JSON.stringify(obj);
  document.head.appendChild(script);
}

function injectLandingEnhancer() {
    const script = document.createElement('script');
    script.src = '/assets/js/landing-enhancer.js';
    script.defer = true;
    document.body.appendChild(script);
}

// Build search index for fast filtering
function makeIndex(item) {
  return [
    item.title || '',
    item.subtitle || '',
    item.contributors || '',
    item.publisher || '',
    item.language || '',
    item.format || ''
  ].join(' ').toLowerCase();
}

// Bootstrap list pages (ebooks/audiobooks)
async function bootstrapList() {
  const MODE = SITE.mode();
  if (!['ebooks', 'audiobooks'].includes(MODE)) return;
  
  const isAudio = MODE === 'audiobooks';
  
  try {
    // Load and filter data
    const allData = await getCatalog();
    const data = allData.filter(x =>
      isAudio ? x.format === 'Audiobook' : x.format === 'eBook'
    );
    
    // Build search index
    const index = data.map(d => ({
      id: d.id,
      hay: makeIndex(d)
    }));
    
    // Get DOM elements
    const $grid = $('#catalogGrid');
    const $count = $('#resultCount');
    const $q = $('#searchInput');
    const $lang = $('#langFilter');
    const $brand = $('#brandFilter');
    const $sort = $('#sortFilter');
    const $min = $('#minPrice');
    const $max = $('#maxPrice');
    
    if (!$grid || !$count) {
      console.error('Required DOM elements not found');
      return;
    }
    
    // Build filter options
    const langs = [...new Set(
      data.map(d => (d.language || '').trim()).filter(Boolean)
    )].sort();
    
    const brands = [...new Set(
      data.map(d => {
        const pub = (d.publisher || '').trim();
        const contrib = (d.contributors || '').toLowerCase();
        if (pub.includes('iD01t')) return 'iD01t Productions';
        if (contrib.includes('guillaume lessard')) return 'Guillaume Lessard';
        if (contrib.includes("el'nox rah") || contrib.includes('elnox')) return "El'Nox Rah";
        if (contrib.includes('dj id01t')) return 'DJ iD01t';
        return pub || 'Other';
      }).filter(Boolean)
    )].sort();
    
    if ($lang) {
      $lang.innerHTML = `<option value="">All languages</option>` + 
        langs.map(l => `<option value="${esc(l)}">${esc(l)}</option>`).join('');
    }
    
    if ($brand) {
      $brand.innerHTML = `<option value="">All brands</option>` + 
        brands.map(b => `<option value="${esc(b)}">${esc(b)}</option>`).join('');
    }
    
    // Load URL parameters into controls
    const params = new URLSearchParams(location.search);
    if ($q) $q.value = params.get('search') || '';
    if ($lang) $lang.value = params.get('lang') || '';
    if ($brand) $brand.value = params.get('brand') || '';
    if ($sort) $sort.value = params.get('sort') || 'relevance';
    if ($min) $min.value = params.get('min') || '';
    if ($max) $max.value = params.get('max') || '';
    
    // Apply filters and render
    function apply() {
      const q = ($q?.value || '').trim().toLowerCase();
      const lang = ($lang?.value || '').trim();
      const brand = ($brand?.value || '').trim();
      const min = parseFloat($min?.value) || null;
      const max = parseFloat($max?.value) || null;
      const sort = $sort?.value || 'relevance';
      
      // Update URL
      setParams({
        search: q || null,
        lang: lang || null,
        brand: brand || null,
        sort,
        min: $min?.value || null,
        max: $max?.value || null
      });
      
      // Filter by search query
      let ids = data.map(d => d.id);
      if (q) {
        const terms = q.split(/\s+/).filter(Boolean);
        ids = index
          .filter(row => terms.every(t => row.hay.includes(t)))
          .map(r => r.id);
      }
      
      // Filter by other criteria
      let rows = data
        .filter(d => ids.includes(d.id))
        .filter(d => !lang || (d.language || '') === lang)
        .filter(d => {
          if (!brand) return true;
          const pub = (d.publisher || '').trim();
          const contrib = (d.contributors || '').toLowerCase();
          if (brand === 'iD01t Productions' && pub.includes('iD01t')) return true;
          if (brand === 'Guillaume Lessard' && contrib.includes('guillaume lessard')) return true;
          if (brand === "El'Nox Rah" && (contrib.includes("el'nox rah") || contrib.includes('elnox'))) return true;
          if (brand === 'DJ iD01t' && contrib.includes('dj id01t')) return true;
          if (brand === 'Other' && !pub.includes('iD01t')) return true;
          return pub === brand;
        })
        .filter(d => min === null || (+d.price || 1e9) >= min)
        .filter(d => max === null || (+d.price || 0) <= max);
      
      // Sort results
      if (sort === 'title-asc') {
        rows.sort((a, b) => a.title.localeCompare(b.title));
      } else if (sort === 'date-desc') {
        rows.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
      } else if (sort === 'price-asc') {
        rows.sort((a, b) => (+a.price || 1e9) - (+b.price || 1e9));
      }
      
      // Update count
      const label = isAudio ? 'audiobooks' : 'ebooks';
      $count.textContent = `${rows.length} ${label}`;
      
      // Render cards
      renderCards(rows, $grid, isAudio);
      
      // Inject structured data
      injectItemListJSONLD(rows.slice(0, 30), isAudio);
    }
    
    // Debounced input handling
    let debounceTimer;
    const debounce = (fn) => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(fn, 150);
    };
    
    const controls = [$q, $lang, $brand, $sort, $min, $max].filter(Boolean);
    controls.forEach(el => {
      el.addEventListener('input', () => debounce(apply));
    });
    
    // Initial render
    apply();
    
    // Inject WebSite structured data with SearchAction
    injectJSONLD({
      "@context": "https://schema.org",
      "@type": "WebSite",
      "url": SITE.base + '/',
      "name": "iD01t Productions",
      "potentialAction": {
        "@type": "SearchAction",
        "target": SITE.base + 
          (isAudio ? "/audiobooks.html" : "/ebooks.html") + 
          "?search={search_term_string}",
        "query-input": "required name=search_term_string"
      }
    });
    
  } catch (error) {
    console.error('Bootstrap error:', error);
    const $grid = $('#catalogGrid');
    if ($grid) {
      $grid.innerHTML = `
        <div class="col-span-full empty-state">
          <p class="text-lg font-medium">Failed to load catalog</p>
          <p class="mt-2">Please try refreshing the page.</p>
        </div>
      `;
    }
  }
}

// Render catalog cards
function renderCards(rows, $grid, isAudio) {
  if (!rows.length) {
    $grid.innerHTML = `
      <div class="col-span-full empty-state">
        <svg class="w-16 h-16 mx-auto mb-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        <p class="text-lg font-medium">No results found</p>
        <p class="mt-2">Try adjusting your filters or search query.</p>
      </div>
    `;
    return;
  }
  
  const label = isAudio ? 'Audiobook' : 'eBook';
  const schemaType = isAudio ? 'https://schema.org/Audiobook' : 'https://schema.org/Book';
  
  $grid.innerHTML = rows.map(d => {
    const title = esc(d.title + (d.subtitle ? `: ${d.subtitle}` : ''));
    const price = fmtPrice(d.price);
    const lang = esc(d.language || '');
    const detail = `${SITE.pages.book}?id=${encodeURIComponent(d.id)}`;
    const img = esc(d.cover_hd);
    const srcset = `${img}&zoom=1 320w, ${img}&zoom=2 640w, ${img}&zoom=3 960w`;
    
    return `
      <article class="catalog-card card-hover intersection-animate" itemscope itemtype="${schemaType}">
        <a href="${detail}" class="catalog-card-media block" aria-label="${title}">
          <img 
            loading="lazy" 
            decoding="async" 
            src="${img}" 
            srcset="${srcset}" 
            sizes="(max-width: 640px) 50vw, (max-width: 1024px) 33vw, 280px"
            alt="${title} cover" 
            itemprop="image"
          />
        </a>
        <div class="p-4 flex flex-col flex-grow">
          <h3 class="font-semibold text-lg mb-1 line-clamp-2" itemprop="name">
            <a href="${detail}" class="hover:text-brand-600 dark:hover:text-brand-400 transition-colors">
              ${title}
            </a>
          </h3>
          <p class="text-sm text-slate-600 dark:text-slate-400 mb-3 line-clamp-2" itemprop="author">
            ${esc(d.contributors || '—')}
          </p>
          <div class="flex flex-wrap gap-2 mb-3">
            ${lang ? `<span class="catalog-badge">${lang}</span>` : ''}
            <span class="catalog-badge format">${label}</span>
            ${price ? `<span class="catalog-badge">${price}</span>` : ''}
          </div>
          <div class="mt-auto flex gap-2">
            <a 
              href="${esc(d.buy)}" 
              class="flex-1 inline-flex items-center justify-center px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg transition-colors focus-ring"
              rel="noopener nofollow sponsored" 
              target="_blank"
            >
              Buy on Google Play
            </a>
            <a 
              href="${detail}" 
              class="px-4 py-2 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-sm font-medium rounded-lg transition-colors focus-ring"
              aria-label="View details for ${title}"
            >
              Details
            </a>
          </div>
        </div>
      </article>
    `;
  }).join('');
  
  // Trigger intersection observer
  requestAnimationFrame(() => {
    $all('.intersection-animate', $grid).forEach((el, i) => {
      setTimeout(() => el.classList.add('visible'), i * 30);
    });
  });
}

// Inject ItemList structured data
function injectItemListJSONLD(items, isAudio) {
  const elements = items.map((d, i) => ({
    "@type": "ListItem",
    "position": i + 1,
    "url": SITE.base + SITE.pages.book + "?id=" + encodeURIComponent(d.id),
    "name": d.title
  }));
  
  injectJSONLD({
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": elements
  });
}

// Bootstrap detail page
async function bootstrapDetail() {
  if (SITE.mode() !== 'book') return;
  
  const id = param('id');
  if (!id) {
    $('#detailContainer').innerHTML = `
      <div class="empty-state">
        <p class="text-lg font-medium">Missing book identifier</p>
      </div>
    `;
    return;
  }
  
  try {
    const data = await getCatalog();
    const item = data.find(x => x.id === id);
    
    if (!item) {
      $('#detailContainer').innerHTML = `
        <div class="empty-state">
          <p class="text-lg font-medium">Book not found</p>
          <p class="mt-2">The requested item could not be found.</p>
          <a href="${item?.format === 'Audiobook' ? SITE.pages.audiobooks : SITE.pages.ebooks}"
             class="mt-4 inline-block px-6 py-3 bg-brand-600 hover:bg-brand-700 text-white rounded-lg transition-colors">
            Browse catalog
          </a>
        </div>
      `;
      return;
    }
    
    injectLandingEnhancer();
    const isAudio = item.format === 'Audiobook';
    
    // Update page metadata
    const fullTitle = `${item.title}${item.subtitle ? `: ${item.subtitle}` : ''}`;
    document.title = `${fullTitle} · ${isAudio ? 'Audiobook' : 'eBook'} · iD01t Productions`;
    
    const setMeta = (name, content) => {
      let meta = $(`meta[name="${name}"]`);
      if (!meta) {
        meta = document.createElement('meta');
        meta.setAttribute('name', name);
        document.head.appendChild(meta);
      }
      meta.setAttribute('content', content);
    };
    
    const setOG = (prop, content) => {
      let meta = $(`meta[property="${prop}"]`);
      if (!meta) {
        meta = document.createElement('meta');
        meta.setAttribute('property', prop);
        document.head.appendChild(meta);
      }
      meta.setAttribute('content', content);
    };
    
    // Set Open Graph and Twitter Card metadata
    setOG('og:type', 'product');
    setOG('og:title', fullTitle);
    setOG('og:url', location.href);
    setOG('og:image', item.cover_hd);
    setMeta('twitter:card', 'summary_large_image');
    setMeta('twitter:title', fullTitle);
    setMeta('twitter:image', item.cover_hd);
    
    // Render detail page
    const schemaType = isAudio ? 'https://schema.org/Audiobook' : 'https://schema.org/Book';
    const backUrl = history.length > 1 ? 
      'javascript:history.back()' : 
      (isAudio ? SITE.pages.audiobooks : SITE.pages.ebooks);
    
    $('#detailContainer').innerHTML = `
      <div class="grid md:grid-cols-[400px_1fr] gap-8 lg:gap-12" itemscope itemtype="${schemaType}">
        <div class="catalog-card">
          <div class="catalog-card-media aspect-[2/3]">
            <img 
              src="${esc(item.cover_hd)}" 
              alt="${esc(fullTitle)} cover" 
              itemprop="image" 
              loading="eager" 
              decoding="async"
              class="w-full h-full object-cover"
            />
          </div>
        </div>
        <div class="space-y-6">
          <div>
            <h1 class="text-4xl md:text-5xl font-bold gradient-text mb-3" itemprop="name">
              ${esc(fullTitle)}
            </h1>
            <p class="text-xl text-slate-600 dark:text-slate-400" itemprop="author">
              ${esc(item.contributors || '')}
            </p>
          </div>
          
          <div class="grid sm:grid-cols-2 gap-4 text-sm">
            ${item.publisher ? `
              <div>
                <span class="text-slate-500 dark:text-slate-400">Publisher</span>
                <p class="font-medium" itemprop="publisher">${esc(item.publisher)}</p>
              </div>
            ` : ''}
            ${item.language ? `
              <div>
                <span class="text-slate-500 dark:text-slate-400">Language</span>
                <p class="font-medium" itemprop="inLanguage">${esc(item.language)}</p>
              </div>
            ` : ''}
            ${item.date ? `
              <div>
                <span class="text-slate-500 dark:text-slate-400">Published</span>
                <time class="block font-medium" itemprop="datePublished" datetime="${esc(item.date)}">
                  ${esc(item.date)}
                </time>
              </div>
            ` : ''}
            ${item.price ? `
              <div itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                <span class="text-slate-500 dark:text-slate-400">Price</span>
                <p class="font-medium">
                  <span itemprop="priceCurrency" content="USD"></span>
                  <span itemprop="price">${fmtPrice(item.price)}</span>
                </p>
                <link itemprop="availability" href="https://schema.org/InStock" />
              </div>
            ` : ''}
          </div>
          
          <div class="flex flex-wrap gap-3">
            <a 
              href="${esc(item.buy)}" 
              class="inline-flex items-center px-6 py-3 bg-brand-600 hover:bg-brand-700 text-white font-medium rounded-lg transition-colors focus-ring"
              target="_blank" 
              rel="noopener nofollow sponsored"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
              Buy on Google Play
            </a>
            <a 
              href="${backUrl}" 
              class="inline-flex items-center px-6 py-3 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 font-medium rounded-lg transition-colors focus-ring"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"></path>
              </svg>
              Back to catalog
            </a>
          </div>
        </div>
      </div>
    `;
    
    // Inject Book/Audiobook structured data
    injectJSONLD({
      "@context": "https://schema.org",
      "@type": isAudio ? "Audiobook" : "Book",
      "name": fullTitle,
      "inLanguage": item.language || "en",
      "image": item.cover_hd,
      "author": item.contributors || undefined,
      "publisher": item.publisher || undefined,
      "datePublished": item.date || undefined,
      "workExample": {
        "@type": "CreativeWork",
        "url": item.buy
      },
      "offers": item.price ? {
        "@type": "Offer",
        "priceCurrency": "USD",
        "price": String(item.price),
        "url": item.buy,
        "availability": "https://schema.org/InStock"
      } : undefined
    });
    
  } catch (error) {
    console.error('Detail page error:', error);
    $('#detailContainer').innerHTML = `
      <div class="empty-state">
        <p class="text-lg font-medium">Error loading book details</p>
        <p class="mt-2">Please try refreshing the page.</p>
      </div>
    `;
  }
}

// PWA Service Worker registration
function setupServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker
      .register('/service-worker.js')
      .then(reg => console.log('SW registered:', reg.scope))
      .catch(err => console.warn('SW registration failed:', err));
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  setupServiceWorker();
  bootstrapList();
  bootstrapDetail();
});
