// A simple API client for the Google Books API.
// Note: This runs in the browser and does not use an API key.
// It is subject to standard unauthenticated API rate limits.

const API_BASE_URL = 'https://www.googleapis.com/books/v1';

// The queries to perform to find the books for the store.
const SEARCH_QUERIES = [
  'inauthor:"Guillaume Lessard"',
  'intitle:"iD01t"',
  'inpublisher:"iD01t Productions"',
];

/**
 * A simple slugify function.
 * @param {string} text The text to slugify.
 * @returns {string} The slugified text.
 */
const slugify = (text) =>
  text
    .toLowerCase()
    .replace(/[^a-z0-9 -]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-');

/**
 * Processes a raw Google Books volume into a more usable format.
 * @param {object} volume The raw volume object from the API.
 * @returns {object} A processed book object.
 */
const processBookVolume = (volume) => {
  if (!volume.volumeInfo) return null;

  const vi = volume.volumeInfo;
  const id = volume.id;
  const isbn13 = vi.industryIdentifiers?.find(i => i.type === 'ISBN_13')?.identifier;
  const isbn10 = vi.industryIdentifiers?.find(i => i.type === 'ISBN_10')?.identifier;

  // Auto-detect series from title, e.g., "My Book (My Series, Book 1)"
  const seriesMatch = vi.title.match(/\(([^,]+), Book \d+\)/);
  const seriesName = seriesMatch ? seriesMatch[1].trim() : null;

  return {
    id: id,
    slug: slugify(vi.title),
    title: vi.title,
    subtitle: vi.subtitle,
    authors: vi.authors || [],
    description: vi.description,
    publishedDate: vi.publishedDate,
    pageCount: vi.pageCount,
    categories: vi.categories || [],
    coverUrl: vi.imageLinks?.thumbnail?.replace('http://', 'https://'),
    googleBooksViewUrl: vi.infoLink,
    googleBooksBuyUrl: volume.saleInfo?.buyLink,
    isbn10,
    isbn13,
    seriesName: seriesName,
    seriesSlug: seriesName ? slugify(seriesName) : null,
  };
};

/**
 * Fetches all books for the store by running all search queries.
 * De-duplicates results based on book ID.
 * @returns {Promise<Array<object>>} A promise that resolves to the catalog of books.
 */
async function getFullCatalog() {
  // Use a simple cache to avoid re-fetching on the same session.
  if (window.ID01T_STORE_CATALOG) {
    return window.ID01T_STORE_CATALOG;
  }

  const allBooks = new Map();

  for (const q of SEARCH_QUERIES) {
    try {
      // Note: In a real app, we'd handle pagination. For this simple case, we'll get the first 40.
      const response = await fetch(`${API_BASE_URL}/volumes?q=${q}&maxResults=40`);
      if (!response.ok) throw new Error(`API request failed for query: ${q}`);
      const data = await response.json();

      if (data.items) {
        data.items.forEach(item => {
          const processed = processBookVolume(item);
          if (processed && !allBooks.has(processed.id)) {
            allBooks.set(processed.id, processed);
          }
        });
      }
    } catch (error) {
      console.error(error);
    }
  }

  const catalog = Array.from(allBooks.values());
  window.ID01T_STORE_CATALOG = catalog; // Cache the result
  return catalog;
}

/**
 * Fetches the details for a single book by its volume ID.
 * @param {string} volumeId The Google Books volume ID.
 * @returns {Promise<object|null>} A promise that resolves to the book details.
 */
async function getBookById(volumeId) {
    try {
        const response = await fetch(`${API_BASE_URL}/volumes/${volumeId}`);
        if (!response.ok) throw new Error(`API request failed for volume ID: ${volumeId}`);
        const data = await response.json();
        return processBookVolume(data);
    } catch (error) {
        console.error(error);
        return null;
    }
}
