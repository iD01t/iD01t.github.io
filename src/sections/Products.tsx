import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  BookOpen, 
  Code, 
  Gamepad2, 
  Headphones,
  ExternalLink,
  Download,
  ArrowRight,
  Check,
  Sparkles,
  Music
} from 'lucide-react';

interface Product {
  id: string;
  name: string;
  description: string;
  image: string;
  price: string;
  count?: string;
  tags: string[];
  featured?: boolean;
  link?: string;
}

const products: Record<string, Product[]> = {
  ebooks: [
    {
      id: '1',
      name: 'AI 2.0 Creator System',
      description: 'Master AI-powered content creation with this comprehensive guide to modern creative workflows.',
      image: 'https://raw.githubusercontent.com/iD01t/iD01t.github.io/main/assets/img/brand/og-home.jpg',
      price: '$29.99',
      count: '167+ eBooks',
      tags: ['AI', 'Automation', 'Creative'],
      featured: true,
      link: 'https://github.com/iD01t/AI-2.0-CREATOR-SYSTEM'
    },
    {
      id: '2',
      name: 'Python Engineering Archive',
      description: 'Complete technical series covering Python software engineering from basics to mastery.',
      image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
      price: '$49.99',
      count: '7 Volumes',
      tags: ['Python', 'Programming', 'Engineering'],
      link: 'https://id01t.itch.io/the-python-engineering-automation-archive'
    },
    {
      id: '3',
      name: 'Systems Architect Vault',
      description: 'Master low-level programming and OS architecture with this comprehensive vault.',
      image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
      price: '$24.99',
      count: '8 Books',
      tags: ['Systems', 'Architecture', 'Low-level'],
      link: 'https://id01t.itch.io/the-zero-to-hero-engineering-series'
    },
    {
      id: '4',
      name: 'Ableton Elevation Guide',
      description: 'DJ iD01T\'s Complete Guide to Building Hits and Elevating Your Sound.',
      image: 'https://i.scdn.co/image/ab67616d00001e0296348b3fd9471f607a16a67c',
      price: '$9.99',
      tags: ['Music Production', 'Ableton', 'Audio'],
    },
    {
      id: '5',
      name: 'Agentic AI Sprint',
      description: 'For Solopreneurs - Launch Autonomous Money-Making Systems in 7 Days.',
      image: 'https://avatars.githubusercontent.com/u/140584560?v=4',
      price: '$9.99',
      tags: ['AI', 'Business', 'Automation'],
    },
    {
      id: '6',
      name: 'Advanced Tactics & Tournament Prep',
      description: 'Psychological Play and Tournament Preparation for competitive gaming.',
      image: 'https://img.itch.zone/aW1nLzI1MjY2NzAxLmpwZw==/315x250%23cb/7Xb3vz.jpg',
      price: '$9.99',
      tags: ['Gaming', 'Strategy', 'Psychology'],
    },
  ],
  apps: [
    {
      id: '7',
      name: 'HTML2Win Pro',
      description: 'Convert HTML apps to Windows executables with one click. No dependencies required.',
      image: 'https://img.itch.zone/aW1nLzE1NjM5MzYucG5n/original/6q8rXq.png',
      price: '$7.49',
      count: '50% OFF',
      tags: ['HTML', 'Windows', 'Converter'],
      featured: true,
      link: 'https://id01t.itch.io/html2win'
    },
    {
      id: '8',
      name: 'NEURO_GLITCH',
      description: '36+ pro effects including Datamosh, Pixel Sort, VHS Tracking. Audio-reactive.',
      image: 'https://img.itch.zone/aW1nLzQyNDkxNTUucG5n/original/LnXrNg.png',
      price: '$2.49',
      count: '50% OFF',
      tags: ['Visual Effects', 'Glitch', 'Creative'],
      featured: true,
      link: 'https://id01t.itch.io/neuro-glitch'
    },
    {
      id: '9',
      name: 'Sonic Bits Pro Ultimate',
      description: 'Generate professional 8-bit, Sci-Fi, and Retro sound effects in seconds.',
      image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
      price: '$2.49',
      count: '50% OFF',
      tags: ['Audio', 'SFX', 'Game Dev'],
      link: 'https://id01t.itch.io/sonic-bits-pro-ultimate'
    },
    {
      id: '10',
      name: 'HeartBeat Companion',
      description: 'Private offline self-care app with love notes, mood tracking, and card creation.',
      image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
      price: '$1.50',
      count: '50% OFF',
      tags: ['Self-Care', 'PWA', 'Wellness'],
      link: 'https://id01t.itch.io/heartbeat-companion'
    },
    {
      id: '11',
      name: 'Jam Butler Pro',
      description: 'One-click tool to zip, lint, generate assets, and upload game jam builds.',
      image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
      price: 'Free',
      tags: ['Game Jam', 'Automation', 'Dev Tool'],
      link: 'https://id01t.itch.io/jam-butler-pro'
    },
    {
      id: '12',
      name: 'CryptoPulse Monitor',
      description: 'Desktop crypto alerts that actually work. Stop refreshing CoinGecko.',
      image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
      price: '$4.99',
      count: '50% OFF',
      tags: ['Crypto', 'Finance', 'Alerts'],
      link: 'https://id01t.itch.io/cryptopulse-monitor'
    },
  ],
  games: [
    {
      id: '13',
      name: "Nini's Adventures",
      description: 'Heartwarming tales and interactive stories for all ages. Coming soon!',
      image: 'https://img.itch.zone/aW1nLzI1MjY2NzAxLmpwZw==/315x250%23cb/7Xb3vz.jpg',
      price: 'TBA',
      tags: ['Adventure', 'Story', 'Family'],
      featured: true,
      link: 'https://id01t.store/nini.html'
    },
    {
      id: '14',
      name: 'Neuro Glitch Game',
      description: 'Immersive cyberpunk puzzle experience with stunning visuals.',
      image: 'https://img.itch.zone/aW1nLzQyNDkxNTUucG5n/original/LnXrNg.png',
      price: '$2.49',
      tags: ['Puzzle', 'Cyberpunk', 'Indie'],
      link: 'https://id01t.itch.io/neuro-glitch'
    },
  ],
  audiobooks: [
    {
      id: '15',
      name: 'ROOT_ACCESS: Jess Damaged Archives',
      description: 'Cyberpunk audiobook trilogy exploring digital sovereignty and identity.',
      image: 'https://img.itch.zone/aW1nLzI1MzU0NzA3LnBuZw==/original/yrN5%2Bp.png',
      price: '$1.99',
      count: '103+ Audiobooks',
      tags: ['Cyberpunk', 'Fiction', 'Trilogy'],
      featured: true,
      link: 'https://id01t.itch.io/root-access-ebook'
    },
    {
      id: '16',
      name: 'SYNTAX_ERROR Archives',
      description: 'Cyberpunk eBook story based on DJ iD01t ROOT_ACCESS LP universe.',
      image: 'https://img.itch.zone/aW1hZ2UvNDI1NTYxOC8yNTM1Mjg5NS5qcGc=/original/PhKraW.jpg',
      price: '$1.99',
      tags: ['Cyberpunk', 'Fiction', 'Story'],
      link: 'https://id01t.itch.io/syntax-error'
    },
    {
      id: '17',
      name: 'BRUTE_FORCE Archives',
      description: 'High-octane cyberpunk thriller. Human-AI hybrid leads digital revolution.',
      image: 'https://img.itch.zone/aW1nLzI1MzU0NzgwLnBuZw==/original/qQOYG%2B.png',
      price: '$1.99',
      tags: ['Cyberpunk', 'Thriller', 'AI'],
      link: 'https://id01t.itch.io/brute-force'
    },
    {
      id: '18',
      name: 'AI Innovation Series',
      description: 'Learn AI automation and creative workflows through immersive audio.',
      image: 'https://avatars.githubusercontent.com/u/140584560?v=4',
      price: '$19.99',
      tags: ['AI', 'Education', 'Business'],
    },
    {
      id: '19',
      name: 'Developer Mindset',
      description: 'Master the psychological aspects of software development and creativity.',
      image: 'https://raw.githubusercontent.com/iD01t/iD01t.github.io/main/assets/img/brand/og-home.jpg',
      price: '$12.99',
      tags: ['Mindset', 'Productivity', 'Career'],
    },
    {
      id: '20',
      name: 'Ableton Elevation Audio',
      description: 'Complete audio guide to building hits and elevating your sound.',
      image: 'https://i.scdn.co/image/ab67616d00001e0296348b3fd9471f607a16a67c',
      price: '$9.99',
      tags: ['Music', 'Production', 'Audio'],
    },
  ],
};

function ProductCard({ product }: { product: Product }) {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.2 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <Card
      ref={ref}
      className={`group relative overflow-hidden bg-card/50 border-border/50 hover:border-primary/50 transition-all duration-500 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      }`}
    >
      {product.featured && (
        <div className="absolute top-3 left-3 z-10">
          <Badge className="bg-gradient-to-r from-primary to-accent text-primary-foreground">
            <Sparkles className="w-3 h-3 mr-1" />
            Featured
          </Badge>
        </div>
      )}
      
      {product.count?.includes('OFF') && (
        <div className="absolute top-3 right-3 z-10">
          <Badge variant="destructive" className="text-xs">
            {product.count}
          </Badge>
        </div>
      )}
      
      <div className="relative h-48 overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent" />
      </div>

      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-semibold text-lg line-clamp-1">{product.name}</h3>
          <span className="text-primary font-bold whitespace-nowrap">{product.price}</span>
        </div>
        {product.count && !product.count.includes('OFF') && (
          <Badge variant="secondary" className="text-xs w-fit">
            {product.count}
          </Badge>
        )}
      </CardHeader>

      <CardContent className="space-y-3">
        <p className="text-sm text-muted-foreground line-clamp-2">
          {product.description}
        </p>

        <div className="flex flex-wrap gap-1">
          {product.tags.map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>

        {product.link && (
          <div className="pt-2">
            <Button size="sm" variant="ghost" className="gap-1 p-0 h-auto" asChild>
              <a href={product.link} target="_blank" rel="noopener noreferrer">
                Learn More
                <ExternalLink className="w-3 h-3" />
              </a>
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export function Products() {
  const [activeTab, setActiveTab] = useState('ebooks');

  return (
    <section id="products" className="relative py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 px-4 py-1">
            <Check className="w-3 h-3 mr-1" />
            Professional Grade
          </Badge>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4">
            Explore Our <span className="text-gradient">Digital Products</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Discover our curated collection of professional digital tools and creative content. 
            167+ eBooks, 103+ audiobooks, Windows apps, and games crafted with attention to quality.
          </p>
        </div>

        {/* Products Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid grid-cols-2 sm:grid-cols-4 w-full max-w-2xl mx-auto mb-8">
            <TabsTrigger value="ebooks" className="gap-2">
              <BookOpen className="w-4 h-4" />
              <span className="hidden sm:inline">eBooks</span>
            </TabsTrigger>
            <TabsTrigger value="apps" className="gap-2">
              <Code className="w-4 h-4" />
              <span className="hidden sm:inline">Apps</span>
            </TabsTrigger>
            <TabsTrigger value="games" className="gap-2">
              <Gamepad2 className="w-4 h-4" />
              <span className="hidden sm:inline">Games</span>
            </TabsTrigger>
            <TabsTrigger value="audiobooks" className="gap-2">
              <Headphones className="w-4 h-4" />
              <span className="hidden sm:inline">Audiobooks</span>
            </TabsTrigger>
          </TabsList>

          {Object.entries(products).map(([key, items]) => (
            <TabsContent key={key} value={key} className="mt-0">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {items.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            </TabsContent>
          ))}
        </Tabs>

        {/* CTA */}
        <div className="text-center mt-12 flex flex-col sm:flex-row justify-center gap-4">
          <Button size="lg" className="group" asChild>
            <a href="https://id01t.store/store.html" target="_blank" rel="noopener noreferrer">
              <Download className="w-4 h-4 mr-2" />
              Visit Full Store
              <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
            </a>
          </Button>
          <Button size="lg" variant="outline" className="group" asChild>
            <a href="https://id01t.itch.io" target="_blank" rel="noopener noreferrer">
              <Music className="w-4 h-4 mr-2" />
              Browse itch.io
              <ExternalLink className="w-4 h-4 ml-2" />
            </a>
          </Button>
        </div>
      </div>
    </section>
  );
}
