'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

const COOKIE_CONSENT_KEY = 'cookie_consent_status';

export const CookieBanner = () => {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    // The banner is only shown if consent has not been explicitly given or denied.
    const consentStatus = localStorage.getItem(COOKIE_CONSENT_KEY);
    if (!consentStatus) {
      setShowBanner(true);
    }
  }, []);

  const handleAccept = () => {
    // In a real app, you might distinguish between 'accepted' and 'denied'.
    localStorage.setItem(COOKIE_CONSENT_KEY, 'accepted');
    setShowBanner(false);
    // Reload the page to apply analytics scripts if they were blocked.
    // A more sophisticated approach might use a state management solution.
    window.location.reload();
  };

  if (!showBanner) {
    return null;
  }

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 w-full">
      <div className="container">
        <div className="mb-4 rounded-md border border-border bg-background/95 p-4 shadow-lg backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
            <p className="text-sm text-foreground">
              We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies. See our{' '}
              <Link href="/legal/privacy" className="underline hover:text-primary">
                Privacy Policy
              </Link>
              .
            </p>
            <Button onClick={handleAccept} size="sm">
              Accept
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
