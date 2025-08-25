import { getProducts } from '@/lib/data';
import { ProductCard } from '@/components/product-card';
import { Button } from '@/components/ui/button';
import Link from 'next/link';
import type { Metadata } from 'next';
import { generateOrganizationJsonLd } from '@/lib/seo';
import { BookOpen, ShoppingBag } from 'lucide-react';

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

      {/* Hero Section */}
      <section className="relative border-b">
        {/* Subtle background gradient */}
        <div className="absolute inset-0 bg-background [mask-image:radial-gradient(ellipse_at_center,black_0%,transparent_70%)]"></div>

        <div className="container relative grid items-center gap-6 pt-12 pb-16 text-center md:py-20">
          <div className="mx-auto flex max-w-[980px] flex-col items-center gap-4">
            <div className="inline-flex items-center rounded-lg bg-muted px-3 py-1 text-sm font-medium">
              🚀 Now Live: The All-New Creator Store
            </div>
            <h1 className="text-4xl font-extrabold leading-tight tracking-tighter md:text-5xl lg:text-6xl lg:leading-[1.1]">
              Your Revenue Engine, Shipped Today.
            </h1>
            <p className="max-w-[700px] text-lg text-muted-foreground sm:text-xl">
              Professional, fast, and automated solutions. High-quality digital products to elevate your brand and workflow.
            </p>
          </div>
          <div className="mx-auto flex gap-4">
            <Link href="/catalog">
              <Button size="lg">
                <ShoppingBag className="mr-2 h-5 w-5" />
                View Catalog
              </Button>
            </Link>
            <Link href="/docs">
              <Button size="lg" variant="outline">
                <BookOpen className="mr-2 h-5 w-5" />
                Read Docs
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section id="featured-products" className="container py-12 md:py-16">
        <div className="flex flex-col items-center gap-2 text-center">
          <h2 className="text-3xl font-bold leading-tight tracking-tighter">
            Featured Products
          </h2>
          <p className="text-muted-foreground max-w-[700px]">
            Explore a selection of our best-selling products, trusted by thousands of creators worldwide.
          </p>
        </div>
        <div className="mt-10 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {featuredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>
    </>
  );
}
