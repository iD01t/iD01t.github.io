/* iD01t Productions - Production JavaScript - Zero Dependencies */

const SITE = {
  base: location.origin,
  pages: {
    ebooks: '/ebooks.html',
    audiobooks: '/audiobooks.html',
    book: '/book.html'
  },
  dataUrl: '/data/catalog.json',
  
  mode() {
    const p = location.pathname.toLowerCase();
    if (p.endsWith('/ebooks.html')) return 'ebooks';
    if (p.endsWith('/audiobooks.html')) return 'audiobooks';
    if (p.endsWith('/book.html')) return 'book';
    return 'other';
  }
};

// ============================================================================
// Utilities
// ============================================================================

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

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// ============================================================================
// Data Loading with Fallback
// ============================================================================

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
    
    if (!Array.isArray(json) || json.length === 0) {
      throw new Error('Invalid catalog data');
    }
    
    sessionStorage.setItem(cacheKey, JSON.stringify(json));
    return json;
  } catch (error) {
    console.error('Catalog load failed:', error);
    
    // Fallback to minimal demo data
    return getFallbackData();
  }
}

function getFallbackData() {
  return [
    {
      id: 'DEMO_EBOOK_1',
      title: 'Python Zero to Hero',
      subtitle: 'Complete Programming Guide',
      format: 'eBook',
      contributors: 'Guillaume Lessard',
      publisher: 'iD01t Productions',
      language: 'English',
      date: '2024-08-15',
      cover_hd: 'https://via.placeholder.com/400x600/8b5cf6/ffffff?text=Python+Zero+to+Hero',
      buy: 'https://play.google.com/store/books',
      price: '9.99'
    },
    {
      id: 'DEMO_AUDIO_1',
      title: 'HTML2Win Pro Guide',
      subtitle: 'Narrated Technical Manual',
      format: 'Audiobook',
      contributors: 'El\'Nox Rah',
      publisher: 'iD01t Productions',
      language: 'English',
      date: '2024-09-01',
      cover_hd: 'https://via.placeholder.com/400x600/ec4899/ffffff?text=HTML2Win+Audio',
      buy: 'https://play.google.com/store/audiobooks',
      price: '14.99'
    }
  ];
}

// ============================================================================
// Schema.org JSON-LD Injection
// ============================================================================

function injectJSONLD(obj) {
  const s = document.createElement('script');
  s.type = 'application/ld+json';
  s.textContent = JSON.stringify(obj, null, 0);
  document.head.appendChild(s);
}

function injectWebSiteSchema(isAudio) {
  injectJSONLD({
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    'url': SITE.base + '/',
    'name': 'iD01t Productions',
    'description': 'Professional eBooks and Audiobooks by Guillaume Lessard / El\'Nox Rah / DJ iD01t',
    'publisher': {
      '@type': 'Organization',
      'name': 'iD01t Productions',
      'url': SITE.base
    },
    'potentialAction': {
      '@type': 'SearchAction',
      'target': SITE.base + (isAudio ? '/audiobooks.html' : '/ebooks.html') + '?search={search_term_string}',
      'query-input': 'required name=search_term_string'
    }
  });
}

function injectItemListSchema(items, isAudio) {
  const elements = items.slice(0, 50).map((d, i) => ({
    '@type': 'ListItem',
    'position': i + 1,
    'url': `${SITE.base}${SITE.pages.book}?id=${encodeURIComponent(d.id)}`,
    'name': d.title + (d.subtitle ? `: ${d.subtitle}` : '')
  }));
  
  injectJSONLD({
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    'itemListElement': elements
  });
}

function injectBookSchema(book, isAudio) {
  const schema = {
    '@context': 'https://schema.org',
    '@type': isAudio ? 'Audiobook' : 'Book',
    'name': book.title + (book.subtitle ? `: ${book.subtitle}` : ''),
    'inLanguage': book.language || 'en',
    'image': book.cover_hd,
    'author': {
      '@type': 'Person',
      'name': book.contributors || 'iD01t Productions'
    },
    'publisher': {
      '@type': 'Organization',
      'name': book.publisher || 'iD01t Productions'
    }
  };
  
  if (book.date) {
    schema.datePublished = book.date;
  }
  
  if (book.price && !isNaN(+book.price)) {
    schema.offers = {
      '@type': 'Offer',
      'priceCurrency': 'USD',
      'price': String(book.price),
      'url': book.buy,
      'availability': 'https://schema.org/InStock',
      'seller': {
        '@type': 'Organization',
        'name': 'Google Play'
      }
    };
  }
  
  if (book.buy) {
    schema.workExample = {
      '@type': 'CreativeWork',
      'url': book.buy
    };
  }
  
  injectJSONLD(schema);
}

// ============================================================================
// Search & Filter Engine
// ============================================================================

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

function filterAndSort(data, filters, sortBy) {
  const { query, lang, brand, minPrice, maxPrice } = filters;
  
  // Build search index
  const index = data.map(d => ({ id: d.id, hay: makeIndex(d) }));
  
  // Filter by search query
  let ids = data.map(d => d.id);
  if (query) {
    const terms = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    ids = index.filter(row => 
      terms.every(t => row.hay.includes(t))
    ).map(r => r.id);
  }
  
  // Apply filters
  let results = data.filter(d => ids.includes(d.id));
  
  if (lang) {
    results = results.filter(d => (d.language || '').toLowerCase() === lang.toLowerCase());
  }
  
  if (brand) {
    results = results.filter(d => 
      (d.contributors || '').toLowerCase().includes(brand.toLowerCase())
    );
  }
  
  if (minPrice !== null && !isNaN(minPrice)) {
    results = results.filter(d => (+d.price || Infinity) >= minPrice);
  }
  
  if (maxPrice !== null && !isNaN(maxPrice)) {
    results = results.filter(d => (+d.price || 0) <= maxPrice);
  }
  
  // Sort
  switch (sortBy) {
    case 'title-asc':
      results.sort((a, b) => (a.title || '').localeCompare(b.title || ''));
      break;
    case 'title-desc':
      results.sort((a, b) => (b.title || '').localeCompare(a.title || ''));
      break;
    case 'date-desc':
      results.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
      break;
    case 'date-asc':
      results.sort((a, b) => (a.date || '').localeCompare(b.date || ''));
      break;
    case 'price-asc':
      results.sort((a, b) => (+a.price || Infinity) - (+b.price || Infinity));
      break;
    case 'price-desc':
      results.sort((a, b) => (+b.price || 0) - (+a.price || 0));
      break;
    default:
      // relevance - keep filtered order
      break;
  }
  
  return results;
}

// ============================================================================
// Rendering
// ============================================================================

function renderCards(items, $grid, isAudio) {
  if (!items.length) {
    $grid.innerHTML = '<div class="empty">📭 No results found. Try adjusting your filters.</div>';
    return;
  }
  
  const html = items.map(d => {
    const title = esc(d.title + (d.subtitle ? `: ${d.subtitle}` : ''));
    const price = fmtPrice(d.price);
    const lang = esc(d.language || 'Unknown');
    const label = d.format || (isAudio ? 'Audiobook' : 'eBook');
    const detailUrl = `${SITE.pages.book}?id=${encodeURIComponent(d.id)}`;
    
    // Handle cover image with fallback
    const coverBase = d.cover_hd || '';
    const srcset = coverBase ? 
      `${coverBase}&zoom=1 320w, ${coverBase}&zoom=2 640w, ${coverBase}&zoom=3 960w` : '';
    
    return `
      <article class="card" itemscope itemtype="https://schema.org/${isAudio ? 'Audiobook' : 'Book'}">
        <a class="card-media" href="${detailUrl}" aria-label="${title}">
          ${coverBase ? `
            <img 
              loading="lazy" 
              decoding="async" 
              src="${esc(coverBase)}&zoom=1" 
              srcset="${srcset}" 
              sizes="(max-width: 600px) 100vw, (max-width: 900px) 50vw, 220px"
              alt="${title} cover"
              itemprop="image"
            >
          ` : `
            <div style="display:flex;align-items:center;justify-content:center;height:100%;font-size:3rem;">📚</div>
          `}
        </a>
        <div class="card-body">
          <h3 class="card-title" itemprop="name">
            <a href="${detailUrl}">${title}</a>
          </h3>
          <p class="card-sub" itemprop="author">${esc(d.contributors || '—')}</p>
          <div class="row">
            <span class="badge" title="Language">${lang}</span>
            <span class="badge" title="Format">${esc(label)}</span>
            ${price ? `<span class="badge" title="Price">${price}</span>` : ''}
          </div>
          <div class="row" style="margin-top: 12px; flex: 1; align-items: flex-end;">
            <a 
              class="btn primary" 
              href="${esc(d.buy)}" 
              rel="noopener nofollow sponsored" 
              target="_blank"
              aria-label="Buy ${title} on Google Play"
            >
              Buy on Google Play
            </a>
            <a class="btn" href="${detailUrl}" aria-label="View details for ${title}">
              Details
            </a>
          </div>
        </div>
      </article>
    `;
  }).join('');
  
  $grid.innerHTML = html;
}

// ============================================================================
// List Page (ebooks.html / audiobooks.html)
// ============================================================================

async function bootstrapList() {
  const MODE = SITE.mode();
  if (!['ebooks', 'audiobooks'].includes(MODE)) return;
  
  const isAudio = MODE === 'audiobooks';
  
  try {
    const allData = await getCatalog();
    const data = allData.filter(x => 
      isAudio ? x.format === 'Audiobook' : x.format === 'eBook'
    );
    
    const $grid = $('#grid');
    const $count = $('#count');
    const $q = $('#q');
    const $lang = $('#lang');
    const $brand = $('#brand');
    const $sort = $('#sort');
    const $min = $('#min');
    const $max = $('#max');
    
    if (!$grid || !$count) return;
    
    // Build filter options
    const langs = [...new Set(data.map(d => (d.language || '').trim()).filter(Boolean))].sort();
    const brands = [...new Set(data.map(d => {
      const c = (d.contributors || '').trim();
      if (c.includes('Guillaume Lessard')) return 'Guillaume Lessard';
      if (c.includes('El\'Nox Rah')) return 'El\'Nox Rah';
      if (c.includes('DJ iD01t')) return 'DJ iD01t';
      return c;
    }).filter(Boolean))].sort();
    
    if ($lang) {
      $lang.innerHTML = '<option value="">All Languages</option>' + 
        langs.map(l => `<option value="${esc(l)}">${esc(l)}</option>`).join('');
    }
    
    if ($brand) {
      $brand.innerHTML = '<option value="">All Creators</option>' + 
        brands.map(b => `<option value="${esc(b)}">${esc(b)}</option>`).join('');
    }
    
    // Load URL params
    const params = new URLSearchParams(location.search);
    if ($q) $q.value = params.get('search') || '';
    if ($lang) $lang.value = params.get('lang') || '';
    if ($brand) $brand.value = params.get('brand') || '';
    if ($sort) $sort.value = params.get('sort') || 'relevance';
    if ($min) $min.value = params.get('min') || '';
    if ($max) $max.value = params.get('max') || '';
    
    function apply() {
      const filters = {
        query: $q ? $q.value.trim() : '',
        lang: $lang ? $lang.value : '',
        brand: $brand ? $brand.value : '',
        minPrice: $min && $min.value ? parseFloat($min.value) : null,
        maxPrice: $max && $max.value ? parseFloat($max.value) : null
      };
      
      const sortBy = $sort ? $sort.value : 'relevance';
      
      setParams({
        search: filters.query || null,
        lang: filters.lang || null,
        brand: filters.brand || null,
        min: $min && $min.value || null,
        max: $max && $max.value || null,
        sort: sortBy
      });
      
      const results = filterAndSort(data, filters, sortBy);
      
      if ($count) {
        $count.textContent = `${results.length} ${isAudio ? 'audiobook' : 'ebook'}${results.length !== 1 ? 's' : ''}`;
      }
      
      renderCards(results, $grid, isAudio);
      injectItemListSchema(results, isAudio);
    }
    
    // Event listeners
    const debouncedApply = debounce(apply, 200);
    
    if ($q) $q.addEventListener('input', debouncedApply);
    if ($lang) $lang.addEventListener('change', apply);
    if ($brand) $brand.addEventListener('change', apply);
    if ($sort) $sort.addEventListener('change', apply);
    if ($min) $min.addEventListener('input', debouncedApply);
    if ($max) $max.addEventListener('input', debouncedApply);
    
    // Initial render
    apply();
    
    // Inject WebSite schema
    injectWebSiteSchema(isAudio);
    
  } catch (error) {
    console.error('Bootstrap list failed:', error);
    const $grid = $('#grid');
    if ($grid) {
      $grid.innerHTML = '<div class="empty">⚠️ Failed to load catalog. Please refresh the page.</div>';
    }
  }
}

// ============================================================================
// Detail Page (book.html)
// ============================================================================

async function bootstrapDetail() {
  if (SITE.mode() !== 'book') return;
  
  const id = param('id');
  const $detail = $('#detail');
  
  if (!$detail) return;
  
  if (!id) {
    $detail.innerHTML = '<div class="empty">⚠️ Missing book ID parameter</div>';
    return;
  }
  
  try {
    const data = await getCatalog();
    const book = data.find(x => x.id === id);
    
    if (!book) {
      $detail.innerHTML = '<div class="empty">📭 Book not found</div>';
      return;
    }
    
    const isAudio = book.format === 'Audiobook';
    
    // Update page metadata
    const fullTitle = book.title + (book.subtitle ? `: ${book.subtitle}` : '');
    document.title = `${fullTitle} · ${isAudio ? 'Audiobook' : 'eBook'} · iD01t Productions`;
    
    // Update meta tags
    const setMeta = (name, content) => {
      let m = $(`meta[name="${name}"]`);
      if (!m) {
        m = document.createElement('meta');
        m.setAttribute('name', name);
        document.head.appendChild(m);
      }
      m.setAttribute('content', content);
    };
    
    const setOG = (prop, content) => {
      let m = $(`meta[property="${prop}"]`);
      if (!m) {
        m = document.createElement('meta');
        m.setAttribute('property', prop);
        document.head.appendChild(m);
      }
      m.setAttribute('content', content);
    };
    
    setOG('og:type', 'product');
    setOG('og:title', fullTitle);
    setOG('og:url', location.href);
    if (book.cover_hd) setOG('og:image', book.cover_hd);
    setMeta('twitter:card', 'summary_large_image');
    
    // Update canonical
    let canonical = $('link[rel="canonical"]');
    if (!canonical) {
      canonical = document.createElement('link');
      canonical.setAttribute('rel', 'canonical');
      document.head.appendChild(canonical);
    }
    canonical.setAttribute('href', location.href);
    
    // Render detail page
    const backUrl = history.length > 1 ? 'javascript:history.back()' : 
      (isAudio ? SITE.pages.audiobooks : SITE.pages.ebooks);
    
    $detail.innerHTML = `
      <div class="detail" itemscope itemtype="https://schema.org/${isAudio ? 'Audiobook' : 'Book'}">
        <div class="card">
          <div class="card-media">
            ${book.cover_hd ? `
              <img 
                src="${esc(book.cover_hd)}&zoom=3" 
                alt="${esc(fullTitle)} cover" 
                itemprop="image"
                loading="eager"
                decoding="async"
              >
            ` : `
              <div style="display:flex;align-items:center;justify-content:center;height:100%;font-size:5rem;">📚</div>
            `}
          </div>
        </div>
        <div>
          <h1 class="h1" itemprop="name">${esc(fullTitle)}</h1>
          ${book.contributors ? `<p class="muted" itemprop="author">${esc(book.contributors)}</p>` : ''}
          
          <div style="margin: 20px 0; display: flex; flex-direction: column; gap: 8px;">
            ${book.publisher ? `<p class="tag">Publisher: <span itemprop="publisher">${esc(book.publisher)}</span></p>` : ''}
            ${book.language ? `<p class="tag">Language: <span itemprop="inLanguage">${esc(book.language)}</span></p>` : ''}
            ${book.format ? `<p class="tag">Format: <span>${esc(book.format)}</span></p>` : ''}
            ${book.date ? `<p class="tag">Published: <time itemprop="datePublished" datetime="${esc(book.date)}">${esc(book.date)}</time></p>` : ''}
            ${book.price ? `
              <p class="tag" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                <span itemprop="priceCurrency" content="USD"></span>
                Price: <span itemprop="price" content="${esc(book.price)}">${fmtPrice(book.price)}</span>
              </p>
            ` : ''}
          </div>
          
          <div class="row" style="margin: 24px 0;">
            <a 
              class="btn primary" 
              href="${esc(book.buy)}" 
              target="_blank" 
              rel="noopener nofollow sponsored"
              aria-label="Buy ${esc(fullTitle)} on Google Play"
            >
              Buy on Google Play
            </a>
            <a class="btn" href="${backUrl}">
              ← Back to Catalog
            </a>
          </div>
        </div>
      </div>
    `;
    
    // Inject book schema
    injectBookSchema(book, isAudio);
    
  } catch (error) {
    console.error('Bootstrap detail failed:', error);
    $detail.innerHTML = '<div class="empty">⚠️ Failed to load book details. Please try again.</div>';
  }
}

// ============================================================================
// PWA Service Worker Registration
// ============================================================================

function setupServiceWorker() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service-worker.js')
      .then(reg => console.log('SW registered:', reg.scope))
      .catch(err => console.log('SW registration failed:', err));
  }
}

// ============================================================================
// Initialize
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
  setupServiceWorker();
  bootstrapList();
  bootstrapDetail();
});
