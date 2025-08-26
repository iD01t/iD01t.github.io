import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { cn } from '@/lib/utils';
import { Header } from '@/components/global/header';
import { Footer } from '@/components/global/footer';
import { AnalyticsProvider } from '@/components/global/analytics-provider';
import { CookieBanner } from '@/components/global/cookie-banner';

const inter = Inter({ subsets: ['latin'], variable: '--font-sans' });

export const metadata: Metadata = {
  title: {
    default: 'Next Store Pro',
    template: '%s | Next Store Pro',
  },
  description: 'The official store for high-quality digital products.',
  // More specific metadata will be handled by the SEO component on each page
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full" suppressHydrationWarning>
      <body
        className={cn(
          'relative h-full bg-background font-sans antialiased',
          inter.className
        )}
      >
        <AnalyticsProvider />
        <main className="relative flex flex-col min-h-screen">
          <Header />
          <div className="flex-grow flex-1">{children}</div>
          <Footer />
        </main>
        <CookieBanner />
      </body>
    </html>
  );
}
