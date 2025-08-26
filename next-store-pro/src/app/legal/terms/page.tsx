import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Terms of Service',
  description: 'Read our terms of service.',
};

// IMPORTANT: This is placeholder content and not real legal advice.
// You should consult with a legal professional to create your own terms of service.

export default function TermsPage() {
  return (
    <main className="container py-12 md:py-16">
      <div className="prose prose-lg mx-auto max-w-4xl">
        <h1>Terms of Service</h1>
        <p className="lead">Last updated: August 25, 2025</p>

        <h2>1. Introduction</h2>
        <p>
          Welcome to Next Store Pro ("we," "our," "us"). These Terms of Service govern your use of our website and the purchase of digital products offered on it. By accessing our website or purchasing our products, you agree to be bound by these Terms.
        </p>

        <h2>2. Digital Products</h2>
        <p>
          All products sold on this website are digital and are delivered electronically. Upon purchase, you will receive a license to use the product, not ownership of the product itself. Licenses are typically for personal or single-commercial use unless otherwise specified.
        </p>

        <h2>3. Payments and Refunds</h2>
        <p>
          All payments are processed through our third-party payment partners (e.g., Gumroad, Stripe). Due to the digital nature of our products, we generally do not offer refunds. Please review the product descriptions carefully before purchasing. Exceptions may be made on a case-by-case basis at our sole discretion.
        </p>

        <h2>4. Intellectual Property</h2>
        <p>
          All content on this website, including products, text, graphics, and logos, is our property or the property of our content suppliers and is protected by international copyright laws.
        </p>

        <h2>5. Limitation of Liability</h2>
        <p>
          Our products are provided "as is" without any warranty. In no event shall we be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on our website.
        </p>

        <h2>6. Changes to These Terms</h2>
        <p>
          We reserve the right to modify these Terms of Service at any time. We will notify you of any changes by posting the new Terms on this page. Your continued use of the site after any such changes constitutes your acceptance of the new Terms.
        </p>

        <h2>7. Contact Us</h2>
        <p>
          If you have any questions about these Terms, please contact us through our support page.
        </p>
      </div>
    </main>
  );
}
