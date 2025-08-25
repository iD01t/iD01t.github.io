/**
 * Represents a normalized product structure from any platform.
 */
export type Product = {
  /** A unique identifier for the product, typically from its source platform. */
  id: string;

  /** A URL-friendly version of the title. */
  slug: string;

  /** The main title of the product. */
  title: string;

  /** A short, secondary title or tagline. */
  subtitle?: string;

  /** A detailed description of the product, can include markdown. */
  description: string;

  /** The current selling price of the product. */
  price: number;

  /** An optional higher price to show a discount, e.g., $100 vs $80. */
  compareAtPrice?: number;

  /** The source platform, e.g., 'Gumroad', 'Ko-fi', 'Stripe'. */
  platform: 'Gumroad' | 'Ko-fi' | 'Itch.io' | 'Google Books' | 'Stripe' | 'Manual';

  /** The direct URL to purchase or access the product. */
  buyUrl: string;

  /** An array of URLs for product images, videos, or other media. The first is the primary thumbnail. */
  media: string[];

  /** A list of tags for filtering and organization. */
  tags: string[];

  /** The primary category the product belongs to. */
  category: string;

  /** Stock Keeping Unit, if applicable. */
  sku?: string;

  /** The date the product was released or last significantly updated, in ISO 8601 format. */
  releaseDate: string;

  /** The version number of the product, if applicable. */
  version?: string;

  /** A list of badges to highlight product status, e.g., 'New', 'Updated', 'Best Seller'. */
  badges?: string[];
};
