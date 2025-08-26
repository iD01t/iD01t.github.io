import Link from 'next/link';
import { cn } from '@/lib/utils';

export const Header = () => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 max-w-screen-2xl items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            {/* You can replace this with a logo component */}
            <span className="font-bold sm:inline-block">
              Next Store Pro
            </span>
          </Link>
          <nav className="hidden items-center gap-6 text-sm md:flex">
            <Link
              href="/catalog"
              className="text-foreground/60 transition-colors hover:text-foreground/80"
            >
              Catalog
            </Link>
            <Link
              href="/blog"
              className="text-foreground/60 transition-colors hover:text-foreground/80"
            >
              Blog
            </Link>
            <Link
              href="/docs"
              className="text-foreground/60 transition-colors hover:text-foreground/80"
            >
              Docs
            </Link>
             <Link
              href="/support"
              className="text-foreground/60 transition-colors hover:text-foreground/80"
            >
              Support
            </Link>
          </nav>
        </div>
        {/* Mobile Nav will go here */}
        <div className="flex flex-1 items-center justify-end space-x-2">
          {/* Right-side content, e.g., Theme Toggle, Cart */}
        </div>
      </div>
    </header>
  );
};
