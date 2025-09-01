// iD01t Productions Catalog Integration
// This file integrates with the catalog system in /assets/site.js

document.addEventListener('DOMContentLoaded', async () => {
    const catalogGrid = document.querySelector('.grid');
    
    if (!catalogGrid) {
        console.log('No catalog grid found - this page may not use the catalog system');
        return;
    }

    // Check if this page has a catalog type specified
    const catalogType = document.body.dataset.catalog;
    
    if (!catalogType) {
        console.log('No catalog type specified - using default catalog');
        return;
    }

    try {
        // Use the existing catalog system from site.js
        const catalogRes = await fetch('/assets/catalog.json', {cache: 'no-store'});
        
        if (!catalogRes.ok) {
            throw new Error(`Failed to fetch catalog: ${catalogRes.status}`);
        }
        
        const catalogData = await catalogRes.json();
        const items = catalogData[catalogType] || [];
        
        if (items.length === 0) {
            catalogGrid.innerHTML = '<p>No items found in this category.</p>';
            return;
        }

        // Render the catalog items using the same format as site.js
        catalogGrid.innerHTML = items.map(item => `
            <article class="card">
                <img alt="${item.title}" data-key="${item.title}" src="${item.image || ''}">
                <div class="badge">${catalogType.slice(0, -1)}</div>
                <h3 class="title"><a href="${item.link}">${item.title}</a></h3>
                <div class="meta">${item.author || 'Unknown'} • ${item.lang || 'EN'}</div>
                <a class="btn" href="${item.link}">Open</a>
            </article>
        `).join('');

        // Trigger image resolution from site.js
        if (window.resolveImages) {
            window.resolveImages();
        }

    } catch (error) {
        console.error('Failed to load catalog:', error);
        catalogGrid.innerHTML = '<p>There was an error loading the catalog. Please check the console for details.</p>';
    }
});
