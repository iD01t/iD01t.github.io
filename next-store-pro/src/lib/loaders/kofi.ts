import type { Product } from '@/lib/schema';

export async function getKofiProducts(): Promise<Product[]> {
  console.log('Fetching products from Ko-fi (mock)...');
  // In a real application, this might involve scraping or using a private API.
  return [
    {
      id: 'kofi-prod-1',
      slug: 'pixel-art-icon-set',
      title: 'Pixel Art Icon Set',
      subtitle: '8-bit style icons for your projects.',
      description: 'A collection of 100+ pixel art icons, perfect for games, websites, and apps. Includes source files.',
      price: 15,
      platform: 'Ko-fi',
      buyUrl: 'https://ko-fi.com/s/fakesampleid',
      media: ['/images/mock/product-2.webp'],
      tags: ['pixel art', 'icons', 'assets'],
      category: 'Apps',
      releaseDate: '2024-07-20T10:00:00Z',
      badges: ['New'],
    },
  ];
}
