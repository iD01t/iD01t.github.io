/*! iD01t Productions — ebooks.client.js (HD Product Images) */
(function (window, document) {
  'use strict';

  // ---- Configuration -------------------------------------------------------
  const CFG = Object.assign({
    FALLBACK_URL: '/assets/data/ebooks.json',
    RETRIES: 3,
    TIMEOUT: 8000,
    CURRENCY: 'CAD'
  }, window.EBOOKS_CONFIG || {});

  // ---- HD Cover Generator --------------------------------------------------
  function generateHDEbookCover(title, author, tags = [], price = '', color = null) {
    const colors = [
      '#1e40af', '#7c2d12', '#059669', '#dc2626', '#ea580c',
      '#0891b2', '#be185d', '#4338ca', '#65a30d', '#ca8a04',
      '#7c3aed', '#e11d48', '#0f766e', '#b91c1c', '#c2410c'
    ];
    const bgColor = color || colors[Math.abs(hashString(title + author)) % colors.length];
    
    const canvas = document.createElement('canvas');
    canvas.width = 400;
    canvas.height = 600;
    const ctx = canvas.getContext('2d');
    
    // Background with professional gradient
    const gradient = ctx.createLinearGradient(0, 0, 400, 600);
    gradient.addColorStop(0, bgColor);
    gradient.addColorStop(0.7, darkenColor(bgColor, 0.2));
    gradient.addColorStop(1, darkenColor(bgColor, 0.4));
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 400, 600);
    
    // Geometric pattern overlay
    ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
    for (let i = 0; i < 10; i++) {
      for (let j = 0; j < 15; j++) {
        if ((i + j) % 3 === 0) {
          ctx.fillRect(i * 40, j * 40, 20, 20);
        }
      }
    }
    
    // Main title
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 28px Arial, sans-serif';
    ctx.textAlign = 'center';
    ctx.shadowColor = 'rgba(0,0,0,0.3)';
    ctx.shadowBlur = 4;
    ctx.shadowOffsetY = 2;
    
    // Smart text wrapping for title
    const maxWidth = 350;
    const words = title.split(' ');
    let lines = [];
    let currentLine = words[0] || '';
    
    for (let i = 1; i < words.length; i++) {
      const testLine = currentLine + ' ' + words[i];
      const metrics = ctx.measureText(testLine);
      if (metrics.width > maxWidth && currentLine.length > 0) {
        lines.push(currentLine);
        currentLine = words[i];
      } else {
        currentLine = testLine;
      }
    }
    if (currentLine) lines.push(currentLine);
    
    // Position title in upper third
    const titleStartY = 150 - (lines.length * 15);
    lines.forEach((line, index) => {
      ctx.fillText(line, 200, titleStartY + (index * 35));
    });
    
    // Reset shadow
    ctx.shadowColor = 'transparent';
    ctx.shadowBlur = 0;
    ctx.shadowOffsetY = 0;
    
    // Author name
    ctx.font = 'normal 16px Arial, sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillText('by ' + author, 200, titleStartY + (lines.length * 35) + 30);
    
    // Primary tag/genre
    if (tags && tags.length > 0) {
      const primaryTag = tags[0].toUpperCase();
      ctx.font = 'bold 12px Arial, sans-serif';
      ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
      ctx.fillRect(50, 380, 300, 25);
      ctx.fillStyle = '#ffffff';
      ctx.fillText(primaryTag, 200, 397);
    }
    
    // Price badge (if provided)
    if (price) {
      ctx.font = 'bold 18px Arial, sans-serif';
      ctx.fillStyle = '#fbbf24';
      ctx.fillRect(280, 50, 100, 40);
      ctx.fillStyle = '#000000';
      ctx.fillText(price, 330, 75);
    }
    
    // eBook indicator
    ctx.font = 'bold 14px Arial, sans-serif';
    ctx.fillStyle = '#10b981';
    ctx.fillText('📚 eBOOK', 200, 480);
    
    // Professional border
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
    ctx.lineWidth = 2;
    ctx.strokeRect(10, 10, 380, 580);
    
    return canvas.toDataURL('image/png', 0.9);
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

  // ---- DOM Elements --------------------------------------------------------
  const $ = id => document.getElementById(id);
  const searchInput = $('ebook-search');
  const categoryFilter = $('category-filter');
  const priceFilter = $('price-filter');
  const sortSelect = $('sort-ebooks');
  const resetBtn = $('reset-filters');
  const ebooksGrid = $('ebooks-grid');
  const ebooksCount = $('ebooks-count');
  const loadingEl = $('ebooks-loading');
  const emptyEl = $('ebooks-empty');

  // ---- Utilities -----------------------------------------------------------
  function escapeHtml(s) { 
    return String(s || '').replace(/[&<>"']/g, c => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', '\'': '&#39;'
    }[c])); 
  }

  async function fetchWithTimeout(url, opts = {}, timeout = CFG.TIMEOUT) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);
    
    try {
      return await fetch(url, Object.assign({ cache: 'no-store' }, opts, { 
        signal: controller.signal 
      }));
    } finally {
      clearTimeout(timeoutId);
    }
  }

  async function testImageUrl(url) {
    try {
      const response = await fetchWithTimeout(url, { method: 'HEAD' }, 3000);
      return response.ok;
    } catch (e) {
      return false;
    }
  }

  async function getOptimalImage(ebook) {
    const { title, author, tags = [], price_cad, price_usd, image } = ebook;
    
    // Try original image first
    if (image && await testImageUrl(image)) {
      return image;
    }
    
    // Generate price string for cover
    const priceStr = price_cad ? `$${price_cad}` : price_usd ? `$${price_usd}` : '';
    
    // Generate HD cover as fallback
    return generateHDEbookCover(title, author, tags, priceStr);
  }

  // ---- UI Components -------------------------------------------------------
  function createEbookCard(ebook) {
    const { 
      id, title, author, description, tags = [], price_cad, price_usd, 
      pages, date, format, features = [], url, preview_url, image
    } = ebook;
    
    const priceDisplay = price_cad ? 
      `$${price_cad} CAD` : 
      price_usd ? `$${price_usd} USD` : 'Free';
    
    const tagChips = tags.slice(0, 3).map(tag => 
      `<span class="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full text-xs font-medium">${escapeHtml(tag)}</span>`
    ).join('');
    
    const featuresText = features.length > 0 ? 
      `<div class="mt-2 text-xs text-gray-600 dark:text-gray-400">
         <strong>Includes:</strong> ${features.slice(0, 2).join(', ')}
       </div>` : '';
    
    return `
      <article class="group bg-white dark:bg-gray-800 rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-200 dark:border-gray-700">
        <div class="relative overflow-hidden">
          <img 
            src="${escapeHtml(image)}" 
            alt="${escapeHtml(title)} cover"
            class="w-full aspect-[3/4] object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
            onerror="this.src='${generateHDEbookCover(title, author, tags, priceDisplay)}'"
          >
          <div class="absolute top-3 right-3 bg-green-600 text-white px-2 py-1 rounded-lg text-xs font-bold">
            📚 HD
          </div>
          <div class="absolute bottom-3 left-3 bg-black bg-opacity-70 text-white px-2 py-1 rounded text-xs">
            ${pages} pages
          </div>
        </div>
        
        <div class="p-4">
          <div class="mb-3">
            <h3 class="font-bold text-lg leading-tight mb-1 line-clamp-2">${escapeHtml(title)}</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400">by ${escapeHtml(author)}</p>
          </div>
          
          <p class="text-sm text-gray-700 dark:text-gray-300 mb-3 line-clamp-2">${escapeHtml(description)}</p>
          
          <div class="flex flex-wrap gap-1 mb-3">
            ${tagChips}
          </div>
          
          ${featuresText}
          
          <div class="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-600">
            <div class="text-lg font-bold text-green-600 dark:text-green-400">
              ${priceDisplay}
            </div>
            <div class="flex gap-2">
              ${preview_url ? `<a href="${escapeHtml(preview_url)}" class="px-3 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-800 dark:text-gray-200 rounded-lg text-sm transition-colors">Preview</a>` : ''}
              <a href="${escapeHtml(url)}" target="_blank" rel="noopener nofollow" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors">
                Buy Now
              </a>
            </div>
          </div>
          
          <div class="mt-2 text-xs text-gray-500 dark:text-gray-400 flex justify-between">
            <span>${format || 'Digital'}</span>
            <span>${date}</span>
          </div>
        </div>
      </article>`;
  }

  function populateFilters(ebooks) {
    // Categories
    if (categoryFilter) {
      const categories = [...new Set(ebooks.flatMap(e => e.tags || []))].sort();
      categoryFilter.innerHTML = '<option value="">All Categories</option>' + 
        categories.map(cat => `<option value="${escapeHtml(cat)}">${escapeHtml(cat)}</option>`).join('');
    }
  }

  // ---- Filtering and Sorting -----------------------------------------------
  function filterEbooks(ebooks) {
    const searchTerm = (searchInput?.value || '').toLowerCase();
    const category = categoryFilter?.value || '';
    const priceRange = priceFilter?.value || '';
    const sortBy = sortSelect?.value || 'date_desc';
    
    let filtered = ebooks.filter(ebook => {
      // Text search
      if (searchTerm) {
        const searchableText = `${ebook.title} ${ebook.author} ${ebook.description} ${(ebook.tags || []).join(' ')}`.toLowerCase();
        if (!searchableText.includes(searchTerm)) return false;
      }
      
      // Category filter
      if (category && !(ebook.tags || []).includes(category)) return false;
      
      // Price filter
      if (priceRange) {
        const price = ebook.price_cad || ebook.price_usd || 0;
        switch (priceRange) {
          case 'free': if (price > 0) return false; break;
          case 'under-15': if (price >= 15) return false; break;
          case '15-25': if (price < 15 || price > 25) return false; break;
          case 'over-25': if (price <= 25) return false; break;
        }
      }
      
      return true;
    });
    
    // Sort
    switch (sortBy) {
      case 'title_asc': filtered.sort((a, b) => a.title.localeCompare(b.title)); break;
      case 'title_desc': filtered.sort((a, b) => b.title.localeCompare(a.title)); break;
      case 'price_asc': filtered.sort((a, b) => (a.price_cad || a.price_usd || 0) - (b.price_cad || b.price_usd || 0)); break;
      case 'price_desc': filtered.sort((a, b) => (b.price_cad || b.price_usd || 0) - (a.price_cad || a.price_usd || 0)); break;
      case 'date_asc': filtered.sort((a, b) => new Date(a.date) - new Date(b.date)); break;
      default: filtered.sort((a, b) => new Date(b.date) - new Date(a.date)); break;
    }
    
    return filtered;
  }

  // ---- Rendering -----------------------------------------------------------
  async function renderEbooks(ebooks) {
    if (!ebooksGrid) return;
    
    if (loadingEl) loadingEl.style.display = 'none';
    
    if (!ebooks.length) {
      ebooksGrid.innerHTML = '';
      if (emptyEl) emptyEl.classList.remove('hidden');
      if (ebooksCount) ebooksCount.textContent = '0 ebooks found';
      return;
    }
    
    if (emptyEl) emptyEl.classList.add('hidden');
    
    // Process images in parallel but render immediately with loading placeholders
    ebooksGrid.innerHTML = ebooks.map(ebook => createEbookCard(ebook)).join('');
    
    // Update images asynchronously
    setTimeout(async () => {
      const imageUpdates = ebooks.map(async (ebook, index) => {
        try {
          const optimalImage = await getOptimalImage(ebook);
          const imgElement = ebooksGrid.querySelector(`article:nth-child(${index + 1}) img`);
          if (imgElement && optimalImage !== ebook.image) {
            imgElement.src = optimalImage;
          }
        } catch (e) {
          console.warn('Failed to optimize image for:', ebook.title, e);
        }
      });
      
      await Promise.allSettled(imageUpdates);
    }, 100);
    
    if (ebooksCount) {
      ebooksCount.textContent = `${ebooks.length} ebook${ebooks.length !== 1 ? 's' : ''} found`;
    }
  }

  // ---- Event Binding -------------------------------------------------------
  function bindEvents(allEbooks) {
    const updateDisplay = () => {
      const filtered = filterEbooks(allEbooks);
      renderEbooks(filtered);
    };
    
    // Search and filter inputs
    [searchInput, categoryFilter, priceFilter, sortSelect].forEach(el => {
      if (el) {
        el.addEventListener('input', updateDisplay);
        el.addEventListener('change', updateDisplay);
      }
    });
    
    // Reset button
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        if (searchInput) searchInput.value = '';
        if (categoryFilter) categoryFilter.value = '';
        if (priceFilter) priceFilter.value = '';
        if (sortSelect) sortSelect.value = 'date_desc';
        updateDisplay();
      });
    }
  }

  // ---- Data Loading --------------------------------------------------------
  async function loadEbooksData() {
    if (loadingEl) loadingEl.style.display = 'block';
    
    try {
      const response = await fetchWithTimeout(CFG.FALLBACK_URL);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      const ebooks = Array.isArray(data) ? data : (data.items || []);
      
      // Ensure all ebooks have working images
      const processedEbooks = await Promise.all(ebooks.map(async ebook => ({
        ...ebook,
        image: ebook.image || generateHDEbookCover(
          ebook.title, 
          ebook.author, 
          ebook.tags, 
          ebook.price_cad ? `$${ebook.price_cad}` : ''
        )
      })));
      
      return processedEbooks;
      
    } catch (error) {
      console.error('Failed to load ebooks:', error);
      
      // Return demo data if loading fails
      return [
        {
          id: 'demo-1',
          title: 'AI-Powered Development Guide',
          author: 'Guillaume Lessard',
          description: 'Master modern development with artificial intelligence tools and techniques.',
          tags: ['ai', 'programming', 'development'],
          price_cad: 24.99,
          pages: 180,
          date: '2025-01-15',
          format: 'PDF + Code',
          features: ['Code Examples', 'Video Tutorials'],
          url: '#demo',
          image: generateHDEbookCover('AI-Powered Development Guide', 'Guillaume Lessard', ['ai', 'programming'], '$24.99')
        },
        {
          id: 'demo-2', 
          title: 'Creative Automation Strategies',
          author: 'Guillaume Lessard',
          description: 'Streamline your creative workflow with smart automation techniques.',
          tags: ['automation', 'creativity', 'productivity'],
          price_cad: 19.99,
          pages: 145,
          date: '2024-12-10',
          format: 'EPUB + Templates',
          features: ['Template Library', 'Workflow Diagrams'],
          url: '#demo',
          image: generateHDEbookCover('Creative Automation Strategies', 'Guillaume Lessard', ['automation', 'creativity'], '$19.99')
        }
      ];
    }
  }

  // ---- Schema.org Structured Data ------------------------------------------
  function generateEbooksSchema(ebooks) {
    try {
      const schema = {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        name: 'HD eBooks Collection',
        description: 'Professional eBooks with high-quality covers and content',
        itemListElement: ebooks.slice(0, 50).map((ebook, index) => ({
          '@type': 'ListItem',
          position: index + 1,
          item: {
            '@type': 'Book',
            name: ebook.title,
            author: {
              '@type': 'Person',
              name: ebook.author
            },
            description: ebook.description,
            image: ebook.image,
            offers: {
              '@type': 'Offer',
              price: ebook.price_cad || ebook.price_usd || 0,
              priceCurrency: ebook.price_cad ? 'CAD' : 'USD',
              availability: 'https://schema.org/InStock'
            },
            numberOfPages: ebook.pages,
            datePublished: ebook.date,
            bookFormat: 'EBook'
          }
        }))
      };
      
      let scriptEl = document.getElementById('ebooks-schema');
      if (!scriptEl) {
        scriptEl = document.createElement('script');
        scriptEl.id = 'ebooks-schema';
        scriptEl.type = 'application/ld+json';
        document.head.appendChild(scriptEl);
      }
      scriptEl.textContent = JSON.stringify(schema);
    } catch (e) {
      console.warn('Failed to generate schema:', e);
    }
  }

  // ---- Initialization ------------------------------------------------------
  async function init() {
    try {
      console.log('Loading HD eBooks collection...');
      
      const ebooks = await loadEbooksData();
      console.log(`Loaded ${ebooks.length} eBooks with HD covers`);
      
      populateFilters(ebooks);
      bindEvents(ebooks);
      await renderEbooks(ebooks);
      generateEbooksSchema(ebooks);
      
      console.log('HD eBooks client initialized successfully');
    } catch (error) {
      console.error('eBooks initialization failed:', error);
      
      if (ebooksGrid) {
        ebooksGrid.innerHTML = `
          <div class="col-span-full text-center py-16">
            <div class="text-6xl mb-4">📚</div>
            <h2 class="text-2xl font-semibold text-gray-700 dark:text-gray-300 mb-2">Failed to load eBooks</h2>
            <p class="text-gray-500 dark:text-gray-400">Please refresh the page to try again</p>
          </div>`;
      }
    }
  }

  // ---- Public API ----------------------------------------------------------
  window.EBooksClient = {
    init,
    generateHDEbookCover,
    loadEbooksData,
    filterEbooks,
    renderEbooks
  };

  // Auto-initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 0);
  }

})(window, document);