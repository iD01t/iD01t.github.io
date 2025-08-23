document.addEventListener('DOMContentLoaded', async () => {
    const productDetailsContainer = document.getElementById('product-details');
    const params = new URLSearchParams(window.location.search);
    const volumeId = params.get('id');

    if (!productDetailsContainer) {
        console.error('Product details container not found.');
        return;
    }

    if (!volumeId) {
        productDetailsContainer.innerHTML = '<p>No product ID specified. Please select a product from the <a href="catalog.html">catalog</a>.</p>';
        return;
    }

    try {
        const book = await getBookById(volumeId);

        if (!book) {
            throw new Error('Book could not be found.');
        }

        // Update page title
        document.title = `${book.title} - iD01t Store`;

        // Sanitize description (simple version)
        const descriptionHtml = book.description ? book.description.replace(/—/g, ',') : '<p>No description available.</p>';

        productDetailsContainer.innerHTML = `
            <div class="product-page-layout">
                <div class="product-cover">
                    <img src="${book.coverUrl || 'https://via.placeholder.com/256x384.png?text=No+Cover'}" alt="Cover of ${book.title}">
                </div>
                <div class="product-info">
                    <h2>${book.title}</h2>
                    ${book.subtitle ? `<h3>${book.subtitle}</h3>` : ''}
                    <p><strong>By:</strong> ${book.authors.join(', ')}</p>
                    <p><strong>Published:</strong> ${book.publishedDate || 'N/A'}</p>
                    <p><strong>Pages:</strong> ${book.pageCount || 'N/A'}</p>

                    <div class="purchase-options">
                        <!--
                            Note: The PayPal "Buy Now" button is not implemented here.
                            This is because the client-side Google Books API does not provide reliable pricing data.
                            The original plan was to merge pricing from a local overrides.json file during a build step,
                            which is not possible in this static HTML5-only version of the site.
                        -->
                        ${book.googleBooksBuyUrl ? `<a href="${book.googleBooksBuyUrl}" class="button-buy" target="_blank" rel="noopener noreferrer">Buy on Google Books</a>` : ''}
                        <a href="${book.googleBooksViewUrl}" class="button-view" target="_blank" rel="noopener noreferrer">View on Google Books</a>
                        <a href="https://ko-fi.com/id01t/shop" class="button-kofi" target="_blank" rel="noopener noreferrer">Buy on Ko-fi</a>
                        <a href="https://id01t.gumroad.com/" class="button-gumroad" target="_blank" rel="noopener noreferrer">Buy on Gumroad</a>
                        <a href="https://www.paypal.com/donate?business=itechinfomtl@gmail.com" class="button-donate" target="_blank" rel="noopener noreferrer">Donate with PayPal</a>
                    </div>

                    <div class="description">
                        <h4>Description</h4>
                        ${descriptionHtml}
                    </div>
                </div>
            </div>
        `;

    } catch (error) {
        console.error('Failed to load product details:', error);
        productDetailsContainer.innerHTML = '<p>There was an error loading the product details. It may not exist or there was a network issue.</p>';
    }
});
