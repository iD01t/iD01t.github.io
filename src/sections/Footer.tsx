import { Badge } from '@/components/ui/badge';
import { 
  Code2, 
  BookOpen, 
  Gamepad2, 
  Music, 
  Headphones,
  Heart,
  ExternalLink,
  Github,
  Twitter,
  Youtube,
  Mail,
  Sparkles
} from 'lucide-react';

const footerLinks = {
  products: [
    { name: 'eBooks (167+)', href: 'https://id01t.store/ebooks.html', icon: BookOpen, external: true },
    { name: 'Audiobooks (103+)', href: 'https://id01t.store/audiobooks.html', icon: Headphones, external: true },
    { name: 'Windows Apps', href: '#store', icon: Code2 },
    { name: 'Online Games', href: 'https://id01t.store/games.html', icon: Gamepad2, external: true },
    { name: 'Original Music', href: '#music', icon: Music },
  ],
  resources: [
    { name: 'Blog', href: 'https://id01t.store/blog.html', icon: BookOpen, external: true },
    { name: "Nini's Adventures", href: 'https://id01t.store/nini.html', icon: Gamepad2, external: true },
    { name: 'itch.io Store', href: 'https://id01t.itch.io', icon: Heart, external: true },
    { name: 'Fan Experience', href: 'https://itechmobile.site', icon: Sparkles, external: true },
  ],
  legal: [
    { name: 'Terms of Service', href: 'https://id01t.store/legal/terms.html', external: true },
    { name: 'Privacy Policy', href: 'https://id01t.store/legal/privacy.html', external: true },
    { name: 'Refund Policy', href: 'https://id01t.store/legal/refunds.html', external: true },
  ],
  social: [
    { name: 'GitHub', href: 'https://github.com/iD01t', icon: Github },
    { name: 'Twitter', href: 'https://twitter.com/djid01t', icon: Twitter },
    { name: 'YouTube', href: 'https://www.youtube.com/@djid01t', icon: Youtube },
    { name: 'Email', href: 'mailto:contact@id01t.ca', icon: Mail },
  ],
};

export function Footer() {
  const scrollToSection = (href: string) => {
    if (href.startsWith('#')) {
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <footer className="relative border-t border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8 lg:gap-12">
          {/* Brand */}
          <div className="lg:col-span-2">
            <a href="#home" className="flex items-center gap-2 mb-4">
              <div className="relative w-10 h-10 flex items-center justify-center">
                <div className="absolute inset-0 bg-gradient-to-br from-cyber-cyan via-cyber-purple to-cyber-pink rounded-lg" />
                <span className="relative text-white font-bold text-lg font-mono">iD</span>
              </div>
              <span className="font-bold text-lg">iD01t Productions</span>
            </a>
            <p className="text-muted-foreground text-sm mb-4 max-w-sm">
              Professional digital tools, 167+ eBooks, 103+ audiobooks, indie games, 
              and DJ iD01t cyberpunk electronic music. Built with passion in Canada.
            </p>
            
            {/* Status Badge */}
            <Badge variant="outline" className="mb-4">
              <span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse" />
              All systems operational
            </Badge>

            {/* Social Links */}
            <div className="flex gap-2">
              {footerLinks.social.map((item) => (
                <a
                  key={item.name}
                  href={item.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="w-10 h-10 rounded-lg bg-muted flex items-center justify-center hover:bg-primary/10 hover:text-primary transition-colors"
                  title={item.name}
                >
                  <item.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Products */}
          <div>
            <h3 className="font-semibold mb-4">Products</h3>
            <ul className="space-y-2">
              {footerLinks.products.map((item) => (
                <li key={item.name}>
                  {item.external ? (
                    <a
                      href={item.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-muted-foreground hover:text-primary transition-colors flex items-center gap-2"
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  ) : (
                    <a
                      href={item.href}
                      onClick={(e) => {
                        e.preventDefault();
                        scrollToSection(item.href);
                      }}
                      className="text-sm text-muted-foreground hover:text-primary transition-colors flex items-center gap-2"
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                    </a>
                  )}
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              {footerLinks.resources.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-muted-foreground hover:text-primary transition-colors flex items-center gap-2"
                  >
                    <item.icon className="w-4 h-4" />
                    {item.name}
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="font-semibold mb-4">Legal</h3>
            <ul className="space-y-2">
              {footerLinks.legal.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-muted-foreground hover:text-primary transition-colors"
                  >
                    {item.name}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-border/50 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} iD01t Productions. All rights reserved.
          </p>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <span>Made with <Heart className="w-4 h-4 text-red-500 fill-red-500 inline" /> in Canada</span>
            <span>|</span>
            <a href="https://itechmobile.site" target="_blank" rel="noopener noreferrer" className="hover:text-primary transition-colors flex items-center gap-1">
              <Sparkles className="w-4 h-4" />
              Fan Experience
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
