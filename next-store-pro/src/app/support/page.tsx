import type { Metadata } from 'next';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

export const metadata: Metadata = {
  title: 'Support',
  description: 'Get help and find answers to frequently asked questions.',
};

const faqs = [
  {
    question: 'How are digital products delivered?',
    answer:
      'All products are delivered instantly via email. You will receive a secure link to download your purchased files. Please check your spam folder if you do not see the email within a few minutes.',
  },
  {
    question: 'What is your refund policy?',
    answer:
      'Due to the nature of digital products, all sales are final and we generally do not offer refunds. If you have an issue with your purchase, please contact us and we will do our best to resolve it.',
  },
  {
    question: 'Can I use these products for commercial projects?',
    answer:
      'Yes, all of our products come with a license for unlimited personal and commercial use. You may not, however, resell or redistribute the products themselves.',
  },
  {
    question: 'I lost my download link. Can you resend it?',
    answer:
      'Absolutely. Please contact us with your order number or the email address you used to make the purchase, and we will resend your download link.',
  },
];

export default function SupportPage() {
  return (
    <main className="container py-12 md:py-16">
      <div className="mx-auto max-w-4xl">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl">Support Center</h1>
          <p className="mt-4 text-lg text-muted-foreground">
            We're here to help. If you can't find the answer you're looking for, please don't hesitate to reach out.
          </p>
        </div>

        <div className="mt-12">
          <h2 className="text-2xl font-semibold text-center">Frequently Asked Questions</h2>
          <Accordion type="single" collapsible className="mt-8 w-full">
            {faqs.map((faq, i) => (
              <AccordionItem key={i} value={`item-${i}`}>
                <AccordionTrigger>{faq.question}</AccordionTrigger>
                <AccordionContent>{faq.answer}</AccordionContent>
              </AccordionItem>
            ))}
          </Accordion>
        </div>

        <div className="mt-16 text-center">
           <h2 className="text-2xl font-semibold">Contact Us</h2>
           <p className="mt-4 text-muted-foreground">
            For any other questions, please email us at:
           </p>
           <a href="mailto:support@nextstorepro.com" className="mt-2 inline-block text-lg font-medium text-primary">
            support@nextstorepro.com
           </a>
        </div>
      </div>
    </main>
  );
}
