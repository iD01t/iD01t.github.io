import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import redirects from '../redirects.json';

type Redirect = {
  source: string;
  destination: string;
  permanent: boolean;
};

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  for (const redirect of redirects as Redirect[]) {
    const sourcePath = redirect.source.replace(/:[a-zA-Z0-9_]+/g, '(.+)');
    const regex = new RegExp(`^${sourcePath}$`);
    const match = pathname.match(regex);

    if (match) {
      let destination = redirect.destination;

      const slugKeys = redirect.source.match(/:[a-zA-Z0-9_]+/g) || [];
      if (slugKeys.length > 0 && match.length > 1) {
        slugKeys.forEach((key, index) => {
          destination = destination.replace(key, match[index + 1]);
        });
      }

      const url = new URL(destination, request.url);
      return NextResponse.redirect(url, redirect.permanent ? 308 : 307);
    }
  }

  return NextResponse.next();
}

// Match all paths except for API routes and static assets
export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
