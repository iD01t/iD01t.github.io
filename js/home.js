document.addEventListener('DOMContentLoaded', async () => {
    const featuredProductSection = document.getElementById('featured-product-section');
    const newReleasesGrid = document.getElementById('new-releases-grid');
    const bestSellersGrid = document.getElementById('best-sellers-grid');

    if (!newReleasesGrid || !bestSellersGrid || !featuredProductSection) {
        console.error('Homepage grid elements not found.');
        return;
    }

    try {
        const catalog = await getFullCatalog();

        if (catalog.length === 0) {
            newReleasesGrid.innerHTML = '<p>Could not load products.</p>';
            bestSellersGrid.innerHTML = '';
            featuredProductSection.innerHTML = '';
            return;
        }

        // --- Populate Featured Product (the very first book) ---
        const featuredProduct = catalog[0];
        featuredProductSection.innerHTML = ''; // Clear loading message
        featuredProductSection.appendChild(createFeaturedProductCard(featuredProduct));

        // --- Populate New Releases (e.g., first 4 books, skipping the featured one) ---
        const newReleases = catalog.slice(1, 5);
        newReleasesGrid.innerHTML = ''; // Clear loading message
        newReleases.forEach(book => {
            newReleasesGrid.appendChild(createProductCard(book));
        });

        // --- Populate Best Sellers (e.g., next 4 books, just for demo) ---
        const bestSellers = catalog.slice(5, 9);
        bestSellersGrid.innerHTML = ''; // Clear loading message
        bestSellers.forEach(book => {
            bestSellersGrid.appendChild(createProductCard(book));
        });

    } catch (error) {
        console.error('Failed to load homepage content:', error);
        newReleasesGrid.innerHTML = '<p>Error loading content.</p>';
        bestSellersGrid.innerHTML = '';
        featuredProductSection.innerHTML = '<p>Error loading content.</p>';
    }
});

/**
 * Helper function to create a featured product card element.
 * This can have a different, more prominent layout.
 * @param {object} book The book object from the API.
 * @returns {HTMLElement} The featured product card element.
 */
function createFeaturedProductCard(book) {
    const card = document.createElement('div');
    card.className = 'featured-product-card'; // Use a different class for styling

    const productLink = document.createElement('a');
    productLink.href = `product.html?id=${book.id}`;

    const coverImage = document.createElement('img');
    coverImage.src = book.coverUrl?.replace('&zoom=1', '&zoom=2') || 'https://via.placeholder.com/256x384.png?text=No+Cover';
    coverImage.alt = `Cover of ${book.title}`;

    const infoDiv = document.createElement('div');
    infoDiv.className = 'featured-product-info';

    const title = document.createElement('h3');
    title.textContent = book.title;

    const authors = document.createElement('p');
    authors.textContent = `By ${book.authors.join(', ')}`;

    const description = document.createElement('p');
    description.textContent = book.description ? (book.description.substring(0, 200) + '...') : 'No description available.';

    infoDiv.appendChild(title);
    infoDiv.appendChild(authors);
    infoDiv.appendChild(description);

    productLink.appendChild(coverImage);
    productLink.appendChild(infoDiv);
    card.appendChild(productLink);

    return card;
}


/**
 * Helper function to create a product card element.
 * @param {object} book The book object from the API.
 * @returns {HTMLElement} The product card element.
 */
function createProductCard(book) {
    const productCard = document.createElement('div');
    productCard.className = 'product-card';

    const productLink = document.createElement('a');
    productLink.href = `product.html?id=${book.id}`;

    const coverImage = document.createElement('img');
    coverImage.src = book.coverUrl || 'https://via.placeholder.com/128x192.png?text=No+Cover';
    coverImage.alt = `Cover of ${book.title}`;

    const title = document.createElement('h3');
    title.textContent = book.title;

    const authors = document.createElement('p');
    authors.textContent = book.authors.join(', ');

    productLink.appendChild(coverImage);
    productLink.appendChild(title);
    productCard.appendChild(productLink);
    productCard.appendChild(authors);

    return productCard;
}
