import type { Product } from '@/lib/schema';

export async function getManualProducts(): Promise<Product[]> {
  console.log('Fetching manual products (mock)...');
  // These are products managed directly in the codebase.
  return [
    {
      id: 'manual-prod-1',
      slug: 'premium-consulting-session',
      title: 'Premium Consulting Session',
      subtitle: '1-on-1 strategy call.',
      description: 'A 60-minute one-on-one consulting session to discuss your project, strategy, or code. We will dive deep into your challenges and unlock new growth opportunities.',
      price: 499,
      platform: 'Manual',
      // This could link to a Stripe Checkout session, Calendly, etc.
      buyUrl: '/contact?service=consulting',
      media: ['/images/mock/product-5.webp'],
      tags: ['consulting', 'strategy', '1-on-1'],
      category: 'Services',
      releaseDate: '2024-01-01T10:00:00Z',
    },
  ];
}
