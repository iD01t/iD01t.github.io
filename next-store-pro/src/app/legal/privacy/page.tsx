import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Privacy Policy',
  description: 'Read our privacy policy.',
};

// IMPORTANT: This is placeholder content and not real legal advice.
// You should consult with a legal professional to create your own privacy policy,
// especially to comply with regulations like GDPR, CCPA, and PIPEDA.

export default function PrivacyPage() {
  return (
    <main className="container py-12 md:py-16">
      <div className="prose prose-lg mx-auto max-w-4xl">
        <h1>Privacy Policy</h1>
        <p className="lead">Last updated: August 25, 2025</p>

        <h2>1. Introduction</h2>
        <p>
          We respect your privacy and are committed to protecting it. This Privacy Policy explains how we collect, use, and safeguard your information when you visit our website.
        </p>

        <h2>2. Information We Collect</h2>
        <p>
          We may collect information about you in a variety of ways. The information we may collect on the Site includes:
        </p>
        <ul>
          <li>
            <strong>Personal Data:</strong> Personally identifiable information, such as your name and email address, that you voluntarily give to us when you purchase a product or sign up for our newsletter.
          </li>
          <li>
            <strong>Derivative Data:</strong> Information our servers automatically collect when you access the Site, such as your IP address, your browser type, and your operating system. Our analytics providers (e.g., Google Analytics) also collect this type of data.
          </li>
        </ul>

        <h2>3. Use of Your Information</h2>
        <p>
          Having accurate information about you permits us to provide you with a smooth, efficient, and customized experience. Specifically, we may use information collected about you via the Site to:
        </p>
        <ul>
          <li>Fulfill and manage purchases, orders, payments, and other transactions related to the Site.</li>
          <li>Email you regarding your account or order.</li>
          <li>Send you a newsletter, with your consent.</li>
          <li>Monitor and analyze usage and trends to improve your experience with the Site.</li>
        </ul>

        <h2>4. Tracking Technologies</h2>
        <p>
          We may use cookies, web beacons, tracking pixels, and other tracking technologies on the Site to help customize the Site and improve your experience. When you access the Site, your personal information is not collected through the use of tracking technology. Most browsers are set to accept cookies by default. You can remove or reject cookies, but be aware that such action could affect the availability and functionality of the Site.
        </p>

        <h2>5. Security of Your Information</h2>
        <p>
          We use administrative, technical, and physical security measures to help protect your personal information. While we have taken reasonable steps to secure the personal information you provide to us, please be aware that despite our efforts, no security measures are perfect or impenetrable, and no method of data transmission can be guaranteed against any interception or other type of misuse.
        </p>

        <h2>6. Contact Us</h2>
        <p>
          If you have questions or comments about this Privacy Policy, please contact us through our support page.
        </p>
      </div>
    </main>
  );
}
