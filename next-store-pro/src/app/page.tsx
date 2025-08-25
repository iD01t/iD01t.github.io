import { getProducts } from '@/lib/data';
import { ProductCard } from '@/components/product-card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import type { Metadata } from 'next';
import { generateOrganizationJsonLd } from '@/lib/seo';

export const metadata: Metadata = {
  title: 'Next Store Pro | High-Quality Digital Products',
  description: 'The official store for professional-grade templates, apps, and courses designed to boost your productivity and revenue.',
  openGraph: {
    title: 'Next Store Pro | High-Quality Digital Products',
    description: 'The official store for professional-grade templates, apps, and courses designed to boost your productivity and revenue.',
    type: 'website',
    url: process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000',
    images: [
      {
        url: `${process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000'}/og-image.png`,
        width: 1200,
        height: 630,
        alt: 'Next Store Pro',
      },
    ],
  },
};

export default async function HomePage() {
  const products = await getProducts();
  const featuredProducts = products.slice(0, 3);

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateOrganizationJsonLd()) }}
      />
      <section className="container grid items-center gap-6 pt-6 pb-8 text-center md:py-10">
        <div className="mx-auto flex max-w-[980px] flex-col items-center gap-2">
          <h1 className="text-3xl font-extrabold leading-tight tracking-tighter md:text-5xl lg:text-6xl lg:leading-[1.1]">
            Your Revenue Engine, Shipped Today.
          </h1>
          <p className="max-w-[700px] text-lg text-muted-foreground sm:text-xl">
            Professional, fast, and automated solutions. High-quality digital products to elevate your brand and workflow.
          </p>
        </div>
        <div className="mx-auto flex gap-4">
          <Link href="/catalog">
            <Button>View Catalog</Button>
          </Link>
          <Link href="/docs">
             <Button variant="outline">Read Docs</Button>
          </Link>
        </div>
      </section>

      <section id="featured-products" className="container py-8 md:py-12">
        <h2 className="mb-8 text-center text-2xl font-bold leading-tight tracking-tighter">
          Featured Products
        </h2>
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {featuredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>
    </>
  );
}
