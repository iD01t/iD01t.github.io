import type { Product } from '@/lib/schema';

export async function getGumroadProducts(): Promise<Product[]> {
  console.log('Fetching products from Gumroad (mock)...');
  // In a real application, you would fetch this from the Gumroad API
  // using an API key from process.env.GUMROAD_API_KEY.
  return [
    {
      id: 'gumroad-prod-1',
      slug: 'pro-notion-template-pack',
      title: 'Pro Notion Template Pack',
      subtitle: 'Organize your life and work.',
      description: 'A comprehensive pack of Notion templates for productivity, project management, and personal growth.',
      price: 49,
      compareAtPrice: 79,
      platform: 'Gumroad',
      buyUrl: 'https://fake-store.gumroad.com/l/pro-notion',
      media: ['/images/mock/product-1.webp'],
      tags: ['notion', 'productivity', 'templates'],
      category: 'eBooks',
      releaseDate: '2024-08-15T10:00:00Z',
      version: '2.0',
      badges: ['Best Seller', 'Updated'],
    },
  ];
}
