import type { Product } from './schema';
import type { WithContext, Organization, Product as SchemaProduct } from 'schema-dts';

/**
 * Generates JSON-LD structured data for the organization.
 * This should be included in the root layout.
 */
export function generateOrganizationJsonLd(): WithContext<Organization> {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Next Store Pro',
    url: siteUrl,
    logo: `${siteUrl}/logo.png`, // A default logo path
  };
}

/**
 * Generates JSON-LD structured data for a single product.
 * This should be included on individual product pages.
 * @param product The product data.
 */
export function generateProductJsonLd(product: Product): WithContext<SchemaProduct> {
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';
  return {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.title,
    description: product.description,
    image: product.media.map((url) => `${siteUrl}${url}`),
    sku: product.sku,
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'USD', // This could be made dynamic in a real app
      availability: 'https://schema.org/InStock',
      url: `${siteUrl}/products/${product.slug}`,
    },
    brand: {
      '@type': 'Brand',
      name: 'Next Store Pro',
    },
  };
}
