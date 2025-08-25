import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Blog',
  description: 'Insights, tutorials, and announcements from the Next Store Pro team.',
};

// In a real application, this data would come from a CMS or local markdown files.
const mockPosts = [
  {
    slug: 'how-we-built-our-store-with-nextjs',
    title: 'How We Built Our Store with Next.js and Achieved a 98 Lighthouse Score',
    date: 'August 20, 2025',
    description: 'A deep dive into the tech stack and performance optimizations behind our new store.',
  },
  {
    slug: '5-mistakes-to-avoid-when-selling-digital-products',
    title: '5 Mistakes to Avoid When Selling Digital Products',
    date: 'August 15, 2025',
    description: 'Learn from our experience and avoid common pitfalls that can hurt your sales and brand.',
  },
  {
    slug: 'introducing-the-pro-notion-template-pack',
    title: 'Introducing the Pro Notion Template Pack v2.0',
    date: 'August 10, 2025',
    description: 'An inside look at our best-selling product and the new features in our latest update.',
  },
];

export default function BlogPage() {
  return (
    <main className="container py-12 md:py-16">
      <div className="mx-auto max-w-4xl">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">Our Blog</h1>
          <p className="mt-4 text-lg text-muted-foreground">
            Insights, tutorials, and announcements from our team.
          </p>
        </div>

        <div className="mt-12 space-y-10">
          {mockPosts.map((post) => (
            <article key={post.slug}>
              <Link href={`/blog/${post.slug}`} className="group">
                <p className="text-sm text-muted-foreground">{post.date}</p>
                <h2 className="mt-1 text-2xl font-semibold group-hover:text-primary">
                  {post.title}
                </h2>
                <p className="mt-2 text-muted-foreground">{post.description}</p>
                <p className="mt-4 font-semibold text-primary">Read more →</p>
              </Link>
            </article>
          ))}
        </div>
      </div>
    </main>
  );
}
