import { getProducts, getProductBySlug } from '@/lib/data';
import { notFound } from 'next/navigation';
import Image from 'next/image';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
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
    description: product.description,
    openGraph: {
      title: product.title,
      description: product.description,
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

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(generateProductJsonLd(product)) }}
      />
      <main className="container py-8 md:py-12">
        <div className="grid gap-8 md:grid-cols-2">
          <div>
            <div className="relative aspect-[4/3] w-full overflow-hidden rounded-lg border">
              <Image
                src={product.media[0]}
                alt={product.title}
                fill
                className="object-cover"
                priority // Prioritize loading the main product image
              />
            </div>
            {/* TODO: Add a thumbnail gallery for multiple images */}
          </div>

          <div className="flex flex-col gap-4">
            <div>
              <p className="text-sm font-medium text-muted-foreground">{product.category}</p>
              <h1 className="text-3xl font-bold tracking-tight lg:text-4xl">{product.title}</h1>
              {product.subtitle && <p className="mt-1 text-lg text-muted-foreground">{product.subtitle}</p>}
            </div>

            {product.badges && (
              <div className="flex flex-wrap gap-2">
                {product.badges.map((badge) => (
                  <Badge key={badge} variant="outline">{badge}</Badge>
                ))}
              </div>
            )}

            <p className="text-3xl font-semibold">
              ${product.price}
              {product.compareAtPrice && (
                <span className="ml-2 text-xl text-muted-foreground line-through">
                  ${product.compareAtPrice}
                </span>
              )}
            </p>

            <div
              className="prose max-w-full text-muted-foreground"
              dangerouslySetInnerHTML={{ __html: product.description.replace(/\n/g, '<br />') }}
            />

            <div className="mt-4">
              <a href={product.buyUrl} target="_blank" rel="noopener noreferrer">
                <Button size="lg" className="w-full">Buy Now on {product.platform}</Button>
              </a>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
