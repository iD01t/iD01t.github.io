import { useState, useEffect } from 'react';
import { useTheme } from '@/components/theme-provider';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from '@/components/ui/sheet';
import { 
  Sun, 
  Moon, 
  Menu, 
  ChevronDown,
  Code2,
  BookOpen,
  Gamepad2,
  Music,
  ShoppingBag,
  Headphones,
  Home,
  Heart,
  Sparkles,
  ExternalLink
} from 'lucide-react';

const navItems = [
  { name: 'Home', href: '#home', icon: Home },
  { name: 'Products', href: '#products', icon: ShoppingBag },
  { name: 'Store', href: '#store', icon: Heart },
  { name: 'Music', href: '#music', icon: Music },
  { name: 'Universe', href: '#universe', icon: Sparkles },
];

const productDropdown = [
  { name: 'eBooks', href: '#products', icon: BookOpen },
  { name: 'Apps', href: '#store', icon: Code2 },
  { name: 'Games', href: '#products', icon: Gamepad2 },
  { name: 'Audiobooks', href: '#products', icon: Headphones },
];

const externalLinks = [
  { name: 'itch.io Store', href: 'https://id01t.itch.io', icon: Heart },
  { name: 'Fan Experience', href: 'https://itechmobile.site', icon: Sparkles },
];

export function Navigation() {
  const { theme, setTheme } = useTheme();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (href: string) => {
    if (href.startsWith('#')) {
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
    setMobileOpen(false);
  };

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-background/80 backdrop-blur-xl border-b border-border/50'
          : 'bg-transparent'
      }`}
    >
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <a 
            href="#home" 
            onClick={(e) => { e.preventDefault(); scrollToSection('#home'); }}
            className="flex items-center gap-2 group"
          >
            <div className="relative w-10 h-10 flex items-center justify-center">
              <div className="absolute inset-0 bg-gradient-to-br from-cyber-cyan via-cyber-purple to-cyber-pink rounded-lg opacity-80 group-hover:opacity-100 transition-opacity" />
              <span className="relative text-white font-bold text-lg font-mono">iD</span>
            </div>
            <span className="font-bold text-lg hidden sm:block group-hover:text-primary transition-colors">
              iD01t Productions
            </span>
          </a>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center gap-1">
            {navItems.map((item) => {
              if (item.name === 'Products') {
                return (
                  <DropdownMenu key={item.name}>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="gap-1">
                        <item.icon className="w-4 h-4" />
                        {item.name}
                        <ChevronDown className="w-3 h-3" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="start" className="w-48">
                      {productDropdown.map((subItem) => (
                        <DropdownMenuItem
                          key={subItem.name}
                          onClick={() => scrollToSection(subItem.href)}
                          className="cursor-pointer"
                        >
                          <subItem.icon className="w-4 h-4 mr-2" />
                          {subItem.name}
                        </DropdownMenuItem>
                      ))}
                    </DropdownMenuContent>
                  </DropdownMenu>
                );
              }
              return (
                <Button
                  key={item.name}
                  variant="ghost"
                  onClick={() => scrollToSection(item.href)}
                  className="gap-1"
                >
                  <item.icon className="w-4 h-4" />
                  {item.name}
                </Button>
              );
            })}
            
            {/* External Links Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="gap-1">
                  <ExternalLink className="w-4 h-4" />
                  More
                  <ChevronDown className="w-3 h-3" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" className="w-48">
                {externalLinks.map((link) => (
                  <DropdownMenuItem key={link.name} asChild>
                    <a 
                      href={link.href} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="cursor-pointer"
                    >
                      <link.icon className="w-4 h-4 mr-2" />
                      {link.name}
                    </a>
                  </DropdownMenuItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>
          </div>

          {/* Right Side */}
          <div className="flex items-center gap-2">
            {/* Theme Toggle */}
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="relative"
            >
              <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
              <span className="sr-only">Toggle theme</span>
            </Button>

            {/* Contact Button */}
            <Button 
              className="hidden sm:flex bg-gradient-to-r from-primary to-accent hover:opacity-90 text-primary-foreground"
              onClick={() => scrollToSection('#newsletter')}
            >
              Contact
            </Button>

            {/* Mobile Menu */}
            <Sheet open={mobileOpen} onOpenChange={setMobileOpen}>
              <SheetTrigger asChild className="lg:hidden">
                <Button variant="ghost" size="icon">
                  <Menu className="h-5 w-5" />
                </Button>
              </SheetTrigger>
              <SheetContent side="right" className="w-72">
                <div className="flex flex-col gap-4 mt-8">
                  {navItems.map((item) => (
                    <Button
                      key={item.name}
                      variant="ghost"
                      onClick={() => scrollToSection(item.href)}
                      className="justify-start gap-2"
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                    </Button>
                  ))}
                  <div className="border-t border-border my-2" />
                  <p className="text-sm text-muted-foreground px-4">Products</p>
                  {productDropdown.map((item) => (
                    <Button
                      key={item.name}
                      variant="ghost"
                      onClick={() => scrollToSection(item.href)}
                      className="justify-start gap-2 pl-8"
                    >
                      <item.icon className="w-4 h-4" />
                      {item.name}
                    </Button>
                  ))}
                  <div className="border-t border-border my-2" />
                  <p className="text-sm text-muted-foreground px-4">External Links</p>
                  {externalLinks.map((item) => (
                    <Button
                      key={item.name}
                      variant="ghost"
                      className="justify-start gap-2 pl-8"
                      asChild
                    >
                      <a href={item.href} target="_blank" rel="noopener noreferrer">
                        <item.icon className="w-4 h-4" />
                        {item.name}
                      </a>
                    </Button>
                  ))}
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </nav>
    </header>
  );
}
