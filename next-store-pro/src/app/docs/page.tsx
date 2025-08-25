import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Documentation',
  description: 'Learn how to use our products and get the most out of them.',
};

export default function DocsPage() {
  return (
    <main className="container py-12 md:py-16">
      <div className="mx-auto max-w-4xl">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">Documentation</h1>
          <p className="mt-4 text-lg text-muted-foreground">
            Your journey to mastery starts here. Find guides and tutorials for all of our products.
          </p>
        </div>

        <div className="mt-12 text-center">
          <p className="text-muted-foreground">
            Our comprehensive documentation is currently being written and will be available here soon.
          </p>
          <p className="mt-2 text-muted-foreground">
            In the meantime, if you have any questions, please visit our{' '}
            <a href="/support" className="text-primary underline">Support Page</a>.
          </p>
        </div>
      </div>
    </main>
  );
}
