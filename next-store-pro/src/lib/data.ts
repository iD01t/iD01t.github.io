import fs from 'fs/promises';
import path from 'path';
// import { cache } from 'react'; // Removed for compatibility with Node.js scripts
import type { Product } from './schema';

const PRODUCTS_FILE = path.join(process.cwd(), 'data/products.json');

/**
 * Fetches all products from the local JSON file.
 * NOTE: React.cache was removed to allow this function to be used in Node.js scripts
 * without the full Next.js/React environment.
 */
export const getProducts = async (): Promise<Product[]> => {
  try {
    const data = await fs.readFile(PRODUCTS_FILE, 'utf-8');
    const products = JSON.parse(data) as Product[];
    return products;
  } catch (error) {
    console.error('Failed to read or parse products.json:', error);
    return [];
  }
};

/**
 * Fetches a single product by its URL-friendly slug.
 */
export const getProductBySlug = async (slug: string): Promise<Product | null> => {
  try {
* NOTE: React.cache was removed to allow this function to be used in Node.js scripts
 * without the full Next.js/React environment.
 */
// Import memoize function from lodash
// import memoize from 'lodash/memoize';

export const getProducts = async (): Promise<Product[]> => {
  try {
    const data = await fs.readFile(PRODUCTS_FILE, 'utf-8');
    const products = JSON.parse(data) as Product[];
    return products;
  } catch (error) {
    console.error('Failed to read or parse products.json:', error);
    return [];
  }
};

// Memoize the getProducts function to cache the result
// const memoizedGetProducts = memoize(getProducts);

/**
 * Fetches a single product by its URL-friendly slug.
 */
export const getProductBySlug = async (slug: string): Promise<Product | null> => {
  try {
    // Use memoized function to get products
    const products = await getProducts(); // TODO: Replace with memoizedGetProducts() once implemented
    return products.find((p) => p.slug === slug) || null;
  } catch (error) {
    console.error(`Failed to get product by slug "${slug}":`, error);
    return null;
  }
};
    return products.find((p) => p.slug === slug) || null;
  } catch (error) {
// Import the sanitize-log package for log sanitization
// sanitizeLog function removes or encodes potentially harmful characters
import { sanitizeLog } from 'sanitize-log';

try {
  const products = await getProducts();
  return products.find((p) => p.slug === slug) || null;
} catch (error) {
  console.error(`Failed to get product by slug "${sanitizeLog(slug)}":`, error);
  return null;
}
    return null;
  }
};
