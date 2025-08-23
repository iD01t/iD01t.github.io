document.addEventListener('DOMContentLoaded', () => {
    const loadComponent = async (url, placeholderId) => {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Failed to load component: ${url}`);
            }
            const text = await response.text();
            const placeholder = document.getElementById(placeholderId);
            if (placeholder) {
                placeholder.outerHTML = text;
            }
        } catch (error) {
            console.error(error);
        }
    };

    // Load header and footer on every page that includes this script
    loadComponent('_header.html', 'header-placeholder');
    loadComponent('_footer.html', 'footer-placeholder');
});
