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
    const products = await getProducts();
    return products.find((p) => p.slug === slug) || null;
  } catch (error) {
    console.error(`Failed to get product by slug "${slug}":`, error);
    return null;
  }
};
