import fs from 'fs';
import path from 'path';
import type { Product } from '@/lib/schema';

// Using aliases configured in tsconfig.json for cleaner imports
import { getGumroadProducts } from '@/lib/loaders/gumroad';
import { getKofiProducts } from '@/lib/loaders/kofi';
import { getItchioProducts } from '@/lib/loaders/itchio';
import { getGoogleBooksProducts } from '@/lib/loaders/google-books';
import { getManualProducts } from '@/lib/loaders/manual';

const CWD = process.cwd();
const DATA_DIR = path.join(CWD, 'data');
const PRODUCTS_FILE = path.join(DATA_DIR, 'products.json');

async function syncProducts() {
  console.log('Starting product sync...');

  // Ensure data directory exists
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }

  // Await all loaders in parallel
  const allProductsPromises: Promise<Product[]>[] = [
    getGumroadProducts(),
    getKofiProducts(),
    getItchioProducts(),
    getGoogleBooksProducts(),
    getManualProducts(),
  ];

  const allProducts = await Promise.all(allProductsPromises);
  const products = allProducts.flat();

  // Sort products by release date, newest first
  products.sort((a, b) => new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime());

  console.log(`Found a total of ${products.length} products.`);

  // Write to the products.json file
  fs.writeFileSync(PRODUCTS_FILE, JSON.stringify(products, null, 2));

  console.log(`✅ Successfully synced products to ${PRODUCTS_FILE}`);
}

syncProducts().catch((error) => {
  console.error('❌ Error syncing products:');
  console.error(error);
  process.exit(1);
});
