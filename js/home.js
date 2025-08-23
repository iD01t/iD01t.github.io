document.addEventListener('DOMContentLoaded', async () => {
    const newReleasesGrid = document.getElementById('new-releases-grid');
    const bestSellersGrid = document.getElementById('best-sellers-grid');

    if (!newReleasesGrid || !bestSellersGrid) {
        console.error('Homepage grid elements not found.');
        return;
    }

    try {
        const catalog = await getFullCatalog();

        if (catalog.length === 0) {
            newReleasesGrid.innerHTML = '<p>Could not load products.</p>';
            bestSellersGrid.innerHTML = '';
            return;
        }

        // --- Populate New Releases (e.g., first 4 books) ---
        const newReleases = catalog.slice(0, 4);
        newReleasesGrid.innerHTML = ''; // Clear loading message
        newReleases.forEach(book => {
            newReleasesGrid.appendChild(createProductCard(book));
        });

        // --- Populate Best Sellers (e.g., next 4 books, just for demo) ---
        const bestSellers = catalog.slice(4, 8);
        bestSellersGrid.innerHTML = ''; // Clear loading message
        bestSellers.forEach(book => {
            bestSellersGrid.appendChild(createProductCard(book));
        });

    } catch (error) {
        console.error('Failed to load homepage content:', error);
        newReleasesGrid.innerHTML = '<p>Error loading content.</p>';
        bestSellersGrid.innerHTML = '';
    }
});

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
