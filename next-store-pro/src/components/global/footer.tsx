import Link from 'next/link';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t">
      <div className="container flex flex-col items-center justify-between gap-4 py-10 md:h-24 md:flex-row md:py-0">
        <div className="flex flex-col items-center gap-4 px-8 md:flex-row md:gap-2 md:px-0">
          <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
            &copy; {currentYear} Next Store Pro. All rights reserved.
          </p>
        </div>
        <div className="flex items-center gap-4">
          <nav className="flex gap-4">
            <Link
              href="/legal/terms"
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              Terms
            </Link>
            <Link
              href="/legal/privacy"
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              Privacy
            </Link>
             <Link
              href="/support"
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              Support
            </Link>
          </nav>
          {/* Placeholder for social media icons */}
        </div>
      </div>
    </footer>
  );
};
