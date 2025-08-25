import type { Product } from '@/lib/schema';

export async function getGoogleBooksProducts(): Promise<Product[]> {
  console.log('Fetching products from Google Books (mock)...');
  // In a real application, you would use the Google Books API.
  return [
    {
      id: 'google-books-1',
      slug: 'the-art-of-conversion-copywriting',
      title: 'The Art of Conversion Copywriting',
      subtitle: 'Turn words into revenue.',
      description: 'A deep dive into the psychology and strategy behind high-converting copy. Learn frameworks used by top growth marketers.',
      price: 9.99,
      platform: 'Google Books',
      buyUrl: 'https://play.google.com/store/books/details?id=fakeid',
      media: ['/images/mock/product-4.webp'],
      tags: ['copywriting', 'marketing', 'business'],
      category: 'eBooks',
      releaseDate: '2024-05-10T10:00:00Z',
    },
  ];
}
