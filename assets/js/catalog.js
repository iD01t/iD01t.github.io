async function loadCatalog() {
  try {
    const response = await fetch('/data/catalog.json');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to load catalog:', error);
    return { ebooks: [], audiobooks: [] };
  }
}

function createBookCard(item, format) {
  return `
    <article class="bg-white dark:bg-slate-800 rounded-2xl shadow-lg overflow-hidden card-hover" role="listitem">
      <!-- Cover Image with fallback -->
      <a href="/book.html?id=${encodeURIComponent(item.id)}" class="block aspect-[2/3] overflow-hidden bg-slate-200 dark:bg-slate-700">
        <img
          feature/catalog-system
          src="${item.cover_hd || '/assets/img/placeholders/card-portrait-384x576.webp'}"
          alt="${item.title} cover"
          class="w-full h-full object-cover"
          loading="lazy"
          onerror="this.src='/assets/img/placeholders/card-portrait-384x576.webp'"

          src="${item.cover_hd || '/assets/img/placeholder-cover.jpg'}"
          alt="${item.title} cover"
          class="w-full h-full object-cover"
          loading="lazy"
          onerror="this.src='/assets/img/placeholder-cover.jpg'"
       main
        />
      </a>

      <!-- Content -->
      <div class="p-4 space-y-3">
        <!-- Title -->
        <h3 class="font-bold text-lg line-clamp-2">
          <a href="/book.html?id=${encodeURIComponent(item.id)}" class="hover:text-brand-600 dark:hover:text-brand-400">
            ${item.title}
          </a>
        </h3>

        <!-- Subtitle if exists -->
        ${item.subtitle ? `<p class="text-sm text-slate-600 dark:text-slate-400 line-clamp-1">${item.subtitle}</p>` : ''}

        <!-- Contributors -->
        <p class="text-sm text-slate-600 dark:text-slate-400">
          By ${item.contributors}
        </p>

        <!-- Categories -->
        ${item.categories && item.categories.length > 0 ? `
          <div class="flex flex-wrap gap-1">
            ${item.categories.slice(0, 3).map(cat =>
              `<span class="px-2 py-1 bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 text-xs rounded-full">${cat}</span>`
            ).join('')}
          </div>
        ` : ''}

        <!-- Description -->
        ${item.description ? `
          <p class="text-sm text-slate-600 dark:text-slate-400 line-clamp-2">
            ${item.description}
          </p>
        ` : ''}

        <!-- Price and Buy Button -->
        <div class="flex items-center justify-between pt-2 border-t border-slate-200 dark:border-slate-700">
          <span class="text-lg font-bold text-brand-600 dark:text-brand-400">
            ${item.price ? `$${item.price}` : 'View Details'}
          </span>
          <a
            href="${item.buy}"
            target="_blank"
            rel="noopener noreferrer nofollow"
            class="px-4 py-2 bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-2"
          >
            Buy Now
          </a>
        </div>
      </div>
    </article>
  `;
}

function filterAndSortCatalog(items, filters) {
  let filtered = [...items];

  // Search filter (title, contributors, description)
  if (filters.search) {
    const search = filters.search.toLowerCase();
    filtered = filtered.filter(item =>
      item.title.toLowerCase().includes(search) ||
      item.contributors.toLowerCase().includes(search) ||
      (item.description && item.description.toLowerCase().includes(search))
    );
  }

  // Language filter
  if (filters.language) {
    filtered = filtered.filter(item => item.language === filters.language);
  }

  // Brand/Author filter
  if (filters.brand) {
    filtered = filtered.filter(item =>
      item.contributors.toLowerCase().includes(filters.brand.toLowerCase())
    );
  }

  // Price range filter
  if (filters.minPrice) {
    filtered = filtered.filter(item =>
      parseFloat(item.price || 0) >= parseFloat(filters.minPrice)
    );
  }
  if (filters.maxPrice) {
    filtered = filtered.filter(item =>
      parseFloat(item.price || 0) <= parseFloat(filters.maxPrice)
    );
  }

  // Sorting
  switch (filters.sort) {
    case 'date-desc':
      filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
      break;
    case 'title-asc':
      filtered.sort((a, b) => a.title.localeCompare(b.title));
      break;
    case 'price-asc':
      filtered.sort((a, b) => parseFloat(a.price || 0) - parseFloat(b.price || 0));
      break;
  }

  return filtered;
}

function populateFilters(items) {
  // Get unique languages
  const languages = [...new Set(items.map(item => item.language))];
  const langFilter = document.getElementById('langFilter');
  languages.forEach(lang => {
    const option = document.createElement('option');
    option.value = lang;
    option.textContent = lang === 'en' ? 'English' : lang === 'fr' ? 'French' : lang;
    langFilter.appendChild(option);
  });

  // Get unique contributors
  const contributors = [...new Set(items.map(item => item.contributors))];
  const brandFilter = document.getElementById('brandFilter');
  contributors.forEach(contributor => {
    const option = document.createElement('option');
    option.value = contributor;
    option.textContent = contributor;
    brandFilter.appendChild(option);
  });
}
