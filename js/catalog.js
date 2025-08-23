document.addEventListener('DOMContentLoaded', async () => {
    const catalogGrid = document.getElementById('catalog-grid');

    if (!catalogGrid) {
        console.error('Catalog grid element not found.');
        return;
    }

    try {
        const catalog = await getFullCatalog();

        if (catalog.length === 0) {
            catalogGrid.innerHTML = '<p>No books found. This may be due to API rate limiting. Please try again later.</p>';
            return;
        }

        // Clear the "Loading..." message
        catalogGrid.innerHTML = '';

        catalog.forEach(book => {
            const productCard = document.createElement('div');
            productCard.className = 'product-card';

            // Link the entire card to the product page
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

            catalogGrid.appendChild(productCard);
        });

    } catch (error) {
        console.error('Failed to load catalog:', error);
        catalogGrid.innerHTML = '<p>There was an error loading the catalog. Please check the console for details.</p>';
    }
});
