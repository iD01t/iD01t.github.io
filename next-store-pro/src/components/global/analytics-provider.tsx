'use client';

import Script from 'next/script';
import { usePathname, useSearchParams } from 'next/navigation';
import { useEffect, useState } from 'react';

// In a real app, this would be integrated with your cookie consent solution.
// For now, we'll use a simple state that defaults to false and is set by the banner.
export function useCookieConsent() {
  const [hasConsent, setHasConsent] = useState(false);
  // This would be replaced by reading a cookie, e.g., `Cookie.get('cookie_consent') === 'true'`
  useEffect(() => {
    // For the demo, we can simulate consent being given after a delay.
    // In a real app, the CookieBanner component would set this state.
    // const consent = localStorage.getItem('cookie_consent') === 'true';
    // setHasConsent(consent);
  }, []);

  return { hasConsent, setHasConsent };
}


export const AnalyticsProvider = () => {
  const gaId = process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID;
  const plausibleDomain = process.env.NEXT_PUBLIC_PLAUSIBLE_DOMAIN;
  const metaPixelId = process.env.NEXT_PUBLIC_META_PIXEL_ID;
  const tiktokPixelId = process.env.NEXT_PUBLIC_TIKTOK_PIXEL_ID;

  const pathname = usePathname();
  const searchParams = useSearchParams();

  // This is a placeholder. The CookieBanner will eventually control this state.
  const hasConsent = true;

  useEffect(() => {
    if (gaId && hasConsent) {
      const url = pathname + searchParams.toString();
      window.gtag('config', gaId, {
        page_path: url,
      });
    }
  }, [pathname, searchParams, gaId, hasConsent]);

  if (!hasConsent) {
    return null;
  }

  return (
    <>
      {/* Google Analytics 4 */}
      {gaId && (
        <>
          <Script
            strategy="afterInteractive"
            src={`https://www.googletagmanager.com/gtag/js?id=${gaId}`}
          />
          <Script
            id="google-analytics"
            strategy="afterInteractive"
            dangerouslySetInnerHTML={{
              __html: `
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
                gtag('config', '${gaId}', {
                  page_path: window.location.pathname,
                });
              `,
            }}
          />
        </>
      )}

      {/* Plausible Analytics */}
      {plausibleDomain && (
        <Script
          strategy="afterInteractive"
          src="https://plausible.io/js/script.js"
          data-domain={plausibleDomain}
        />
      )}

      {/* Meta (Facebook) Pixel */}
      {metaPixelId && (
        <Script
          id="meta-pixel"
          strategy="afterInteractive"
          dangerouslySetInnerHTML={{
            __html: `
              !function(f,b,e,v,n,t,s)
              {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
              n.callMethod.apply(n,arguments):n.queue.push(arguments)};
              if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
              n.queue=[];t=b.createElement(e);t.async=!0;
              t.src=v;s=b.getElementsByTagName(e)[0];
              s.parentNode.insertBefore(t,s)}(window, document,'script',
              'https://connect.facebook.net/en_US/fbevents.js');
              fbq('init', '${metaPixelId}');
              fbq('track', 'PageView');
            `,
          }}
        />
      )}
    </>
  );
};

declare global {
  interface Window {
    gtag: (
      command: 'config' | 'event',
      targetId: string,
      config?: Record<string, unknown>
    ) => void;
    fbq: (...args: any[]) => void;
  }
}
