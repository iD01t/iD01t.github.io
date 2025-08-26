import { getProducts } from '@/lib/data';
import { ProductCard } from '@/components/product-card';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Catalog',
  description: 'Browse our full catalog of high-quality digital products.',
};

export default async function CatalogPage() {
  const products = await getProducts();

  return (
    <main className="container py-8 md:py-12">
      <div className="mb-8 text-center">
        <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl">
          Product Catalog
        </h1>
        <p className="mt-2 text-lg text-muted-foreground">
          Explore all of our available digital products, templates, and courses.
        </p>
      </div>
      {products.length > 0 ? (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      ) : (
        <p className="text-center text-muted-foreground">
          No products found. Please run the sync script or add products to your platforms.
        </p>
      )}
    </main>
  );
}
