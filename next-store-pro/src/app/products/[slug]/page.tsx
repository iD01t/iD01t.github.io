import { getProducts, getProductBySlug } from '@/lib/data';
import { notFound } from 'next/navigation';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { CheckCircle2 } from 'lucide-react';
import type { Metadata } from 'next';
import { generateProductJsonLd } from '@/lib/seo';

type ProductPageProps = {
  params: {
    slug: string;
  };
};

export async function generateMetadata({ params }: ProductPageProps): Promise<Metadata> {
  const product = await getProductBySlug(params.slug);

  if (!product) {
    return {
      title: 'Product Not Found',
    };
  }

  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';

  return {
    title: product.title,
    description: product.subtitle || product.description.substring(0, 150),
    openGraph: {
      title: product.title,
      description: product.subtitle || product.description.substring(0, 150),
      type: 'website',
      url: `${siteUrl}/products/${product.slug}`,
      images: product.media.map(url => ({
        url: `${siteUrl}${url}`,
        width: 1200,
        height: 630,
        alt: product.title,
      })),
    },
  };
}

export async function generateStaticParams() {
  const products = await getProducts();
  return products.map((product) => ({
    slug: product.slug,
  }));
}

export default async function ProductPage({ params }: ProductPageProps) {
  const product = await getProductBySlug(params.slug);

  if (!product) {
    notFound();
  }

  // A simple list of features, can be expanded in the product data
  const features = product.description.split('\n').filter(f => f.trim().length > 0);

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateProductJsonLd(product)) }}
      />
      <main className="container py-10 md:py-16">
        <div className="grid gap-12 md:grid-cols-2 lg:gap-16">
          {/* Image Gallery */}
          <div className="flex flex-col gap-4">
            <div className="relative aspect-[4/3] w-full overflow-hidden rounded-lg border shadow-sm">
              <Image
<div>
            <div className="relative aspect-[4/3] w-full overflow-hidden rounded-lg border">
              <Image
                src={product.media[0] || '/images/placeholder.webp'}
                alt={product.title}
                fill
                className="object-cover"
                alt={product.title}
                fill
                className="object-cover"
                priority
              />
            </div>
            {/* Thumbnail gallery would go here */}
          </div>

          {/* Product Details */}
          <div className="flex flex-col gap-6">
            <div className="flex flex-col gap-2">
              <p className="font-semibold uppercase tracking-wide text-primary">
                {product.category}
              </p>
              <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">{product.title}</h1>
              {product.subtitle && <p className="text-xl text-muted-foreground">{product.subtitle}</p>}
            </div>

            {product.badges && (
              <div className="flex flex-wrap gap-2">
                {product.badges.map((badge) => (
                  <Badge key={badge}>{badge}</Badge>
                ))}
              </div>
            )}

            <Separator />

            {/* Features Section */}
            <div className="space-y-4">
               <h2 className="text-2xl font-semibold">What's Included</h2>
               <ul className="space-y-2">
                {features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-3">
                    <CheckCircle2 className="h-5 w-5 flex-shrink-0 text-green-500" />
                    <span className="text-muted-foreground">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>

            <Separator />

            {/* Buy Box */}
            <div className="rounded-lg border bg-card p-6 shadow-sm">
              <div className="flex items-center justify-between">
                <p className="text-2xl font-bold">
                  ${product.price}
                  {product.compareAtPrice && (
                    <span className="ml-2 text-base text-muted-foreground line-through">
                      ${product.compareAtPrice}
                    </span>
                  )}
                </p>
                <Badge variant="secondary">{product.platform}</Badge>
              </div>
              <a href={product.buyUrl} target="_blank" rel="noopener noreferrer" className="mt-6 block">
                <Button size="lg" className="w-full font-semibold">Buy Now</Button>
              </a>
              <p className="mt-2 text-center text-xs text-muted-foreground">
                Secure purchase via {product.platform}
              </p>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
