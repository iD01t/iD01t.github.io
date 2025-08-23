document.addEventListener('DOMContentLoaded', async () => {
    const seriesGrid = document.getElementById('series-grid');
    const seriesTitleElement = document.getElementById('series-title');
    const params = new URLSearchParams(window.location.search);
    const seriesSlug = params.get('name');

    if (!seriesGrid || !seriesTitleElement) {
        console.error('Series grid or title element not found.');
        return;
    }

    if (!seriesSlug) {
        seriesTitleElement.textContent = 'No Series Specified';
        seriesGrid.innerHTML = '<p>Please select a series from the catalog.</p>';
        return;
    }

    try {
        const catalog = await getFullCatalog();
        const seriesBooks = catalog.filter(book => book.seriesSlug === seriesSlug);

        if (seriesBooks.length === 0) {
            seriesTitleElement.textContent = 'Series Not Found';
            seriesGrid.innerHTML = '<p>Could not find any books for this series.</p>';
            return;
        }

        // Use the full series title from the first book found
        const seriesName = seriesBooks[0].seriesName;
        seriesTitleElement.textContent = `Series: ${seriesName}`;

        // Clear the grid
        seriesGrid.innerHTML = '';

        seriesBooks.forEach(book => {
            const productCard = document.createElement('div');
            productCard.className = 'product-card';

            const productLink = document.createElement('a');
            productLink.href = `product.html?id=${book.id}`;

            const coverImage = document.createElement('img');
            coverImage.src = book.coverUrl || 'https://via.placeholder.com/128x192.png?text=No+Cover';
            coverImage.alt = `Cover of ${book.title}`;

            const title = document.createElement('h3');
            title.textContent = book.title;

            productLink.appendChild(coverImage);
            productLink.appendChild(title);
            productCard.appendChild(productLink);

            seriesGrid.appendChild(productCard);
        });

    } catch (error) {
        console.error('Failed to load series:', error);
        seriesTitleElement.textContent = 'Error';
        seriesGrid.innerHTML = '<p>There was an error loading the series details.</p>';
    }
});
