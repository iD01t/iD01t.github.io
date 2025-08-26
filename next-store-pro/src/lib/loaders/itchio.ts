import type { Product } from '@/lib/schema';

export async function getItchioProducts(): Promise<Product[]> {
  console.log('Fetching products from Itch.io (mock)...');
  // In a real application, you might use the Itch.io API.
  return [
    {
      id: 'itchio-prod-1',
      slug: 'indie-game-soundtrack',
      title: 'Indie Game Soundtrack Vol. 1',
      subtitle: 'Royalty-free music for your games.',
      description: 'A collection of 10 original tracks, perfect for platformers, RPGs, and puzzle games. Looped and ready to use.',
      price: 25,
      platform: 'Itch.io',
      buyUrl: 'https://fake-developer.itch.io/indie-game-soundtrack',
      media: ['/images/mock/product-3.webp'],
      tags: ['music', 'soundtrack', 'gamedev'],
      category: 'Music',
      releaseDate: '2024-06-01T10:00:00Z',
    },
  ];
}
