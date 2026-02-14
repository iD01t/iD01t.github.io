import { useRef, useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { 
  ShoppingBag, 
  ExternalLink,
  Search,
  Code2,
  Gamepad2,
  Music,
  BookOpen,
  Heart,
  Download,
  Sparkles
} from 'lucide-react';

interface ItchProduct {
  id: string;
  name: string;
  description: string;
  image: string;
  price: string;
  originalPrice?: string;
  category: 'app' | 'game' | 'tool' | 'ebook' | 'audio';
  url: string;
  featured?: boolean;
  tags: string[];
}

// Products from id01t.itch.io with real images
const itchProducts: ItchProduct[] = [
  {
    id: '1',
    name: 'HTML2Win Pro',
    description: 'Turn web code into native Windows apps. No Electron bloat. 3 clicks to executable.',
    image: 'https://img.itch.zone/aW1nLzE1NjM5MzYucG5n/original/6q8rXq.png',
    price: '$7.49',
    originalPrice: '$14.99',
    category: 'tool',
    url: 'https://id01t.itch.io/html2win',
    featured: true,
    tags: ['Windows', 'HTML', 'Converter', 'Native'],
  },
  {
    id: '2',
    name: 'NEURO_GLITCH',
    description: '36+ pro effects including Datamosh, Pixel Sort, VHS Tracking. Audio-reactive visuals.',
    image: 'https://img.itch.zone/aW1nLzQyNDkxNTUucG5n/original/LnXrNg.png',
    price: '$2.49',
    originalPrice: '$4.99',
    category: 'app',
    url: 'https://id01t.itch.io/neuro-glitch',
    featured: true,
    tags: ['Visual Effects', 'Glitch', 'Creative', 'Commercial'],
  },
  {
    id: '3',
    name: 'Sonic Bits Pro Ultimate',
    description: 'Generate professional 8-bit, Sci-Fi, and Retro sound effects in seconds.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$2.49',
    originalPrice: '$4.99',
    category: 'audio',
    url: 'https://id01t.itch.io/sonic-bits-pro-ultimate',
    tags: ['SFX', 'Audio', 'Game Dev', '8-bit'],
  },
  {
    id: '4',
    name: 'HeartBeat Companion',
    description: 'Private offline self-care app with love notes, mood tracking, and card creation.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$1.50',
    originalPrice: '$2.99',
    category: 'app',
    url: 'https://id01t.itch.io/heartbeat-companion',
    tags: ['Self-Care', 'PWA', 'Offline', 'Wellness'],
  },
  {
    id: '5',
    name: 'Systems Architect Vault',
    description: 'Master low-level programming & OS architecture. 8 books included.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$12.49',
    originalPrice: '$24.99',
    category: 'ebook',
    url: 'https://id01t.itch.io/the-zero-to-hero-engineering-series',
    tags: ['Systems', 'Programming', 'Education', 'Bundle'],
  },
  {
    id: '6',
    name: 'Python Engineering Archive',
    description: 'Complete 7-volume technical series. Python mastery from basics to expert.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$7.49',
    originalPrice: '$14.99',
    category: 'ebook',
    url: 'https://id01t.itch.io/the-python-engineering-automation-archive',
    tags: ['Python', 'Programming', 'Education', 'Bundle'],
  },
  {
    id: '7',
    name: 'Jam Butler Pro',
    description: 'One-click tool to zip, lint, generate assets, and upload game jam builds to itch.io.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: 'Free',
    category: 'tool',
    url: 'https://id01t.itch.io/jam-butler-pro',
    tags: ['Game Jam', 'Automation', 'Butler', 'Dev Tool'],
  },
  {
    id: '8',
    name: 'HTML2Linux Pro',
    description: 'Build native Linux apps from HTML. No dependencies. Pure native performance.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$9.99',
    originalPrice: '$19.99',
    category: 'tool',
    url: 'https://id01t.itch.io/html2linux-pro',
    tags: ['Linux', 'HTML', 'Converter', 'Native'],
  },
  {
    id: '9',
    name: 'CryptoPulse Monitor',
    description: 'Desktop crypto alerts that actually work. Stop refreshing CoinGecko every 10 minutes.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$4.99',
    originalPrice: '$9.99',
    category: 'app',
    url: 'https://id01t.itch.io/cryptopulse-monitor',
    tags: ['Crypto', 'Finance', 'Alerts', 'Desktop'],
  },
  {
    id: '10',
    name: 'ROOT_ACCESS: The Jess Damaged Archives',
    description: 'Cyberpunk eBook prequel finale. Jess Damaged fuses with AI for global system reboot.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$1.99',
    originalPrice: '$3.99',
    category: 'ebook',
    url: 'https://id01t.itch.io/root-access-ebook',
    featured: true,
    tags: ['Cyberpunk', 'Fiction', 'ROOT_ACCESS', 'Lore'],
  },
  {
    id: '11',
    name: 'SYNTAX_ERROR: Jess Damaged Archives',
    description: 'Cyberpunk eBook story based on DJ iD01t ROOT_ACCESS LP universe.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$1.99',
    originalPrice: '$3.99',
    category: 'ebook',
    url: 'https://id01t.itch.io/syntax-error',
    tags: ['Cyberpunk', 'Fiction', 'Story', 'Lore'],
  },
  {
    id: '12',
    name: 'BRUTE_FORCE: Jess Damaged Archives',
    description: 'High-octane cyberpunk thriller. Human-AI hybrid leads digital revolution.',
    image: 'https://img.itch.zone/aW1nLzQyNTA5MjYucG5n/original/6q8rXq.png',
    price: '$1.99',
    originalPrice: '$3.99',
    category: 'ebook',
    url: 'https://id01t.itch.io/brute-force',
    tags: ['Cyberpunk', 'Thriller', 'AI', 'Fiction'],
  },
];

const categories = [
  { id: 'all', name: 'All', icon: ShoppingBag },
  { id: 'app', name: 'Apps', icon: Code2 },
  { id: 'tool', name: 'Tools', icon: Download },
  { id: 'ebook', name: 'eBooks', icon: BookOpen },
  { id: 'audio', name: 'Audio', icon: Music },
  { id: 'game', name: 'Games', icon: Gamepad2 },
];

function ProductCard({ product }: { product: ItchProduct }) {
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
      
      {product.originalPrice && (
        <div className="absolute top-3 right-3 z-10">
          <Badge variant="destructive" className="text-xs">
            -50%
          </Badge>
        </div>
      )}
      
      <a href={product.url} target="_blank" rel="noopener noreferrer">
        <div className="relative h-48 overflow-hidden bg-muted">
          <img
            src={product.image}
            alt={product.name}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent" />
        </div>
      </a>

      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="font-semibold text-lg line-clamp-1 group-hover:text-primary transition-colors">
            {product.name}
          </h3>
        </div>

        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {product.description}
        </p>

        <div className="flex flex-wrap gap-1 mb-3">
          {product.tags.slice(0, 3).map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>

        <div className="flex items-center justify-between pt-2">
          <div className="flex items-center gap-2">
            <span className="font-bold text-primary">{product.price}</span>
            {product.originalPrice && (
              <span className="text-sm text-muted-foreground line-through">
                {product.originalPrice}
              </span>
            )}
          </div>
          
          <Button size="sm" variant="ghost" className="gap-1" asChild>
            <a href={product.url} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="w-3 h-3" />
              View
            </a>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

export function ItchStore() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const filteredProducts = itchProducts.filter((product) => {
    const matchesSearch = 
      product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      product.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <section id="store" className="relative py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 px-4 py-1">
            <Heart className="w-3 h-3 mr-1" />
            iD01t on itch.io
          </Badge>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4">
            Digital <span className="text-gradient">Store</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Browse our collection of professional tools, creative apps, eBooks, and audio assets. 
            Built by indie creators, for indie creators.
          </p>
        </div>

        {/* iD01t Customer Manifesto */}
        <div className="max-w-2xl mx-auto mb-12 p-6 rounded-2xl bg-gradient-to-br from-primary/10 to-accent/10 border border-primary/20">
          <h3 className="font-semibold mb-4 flex items-center gap-2">
            <Heart className="w-5 h-5 text-primary" />
            iD01t Customer Manifesto
          </h3>
          <div className="space-y-2 text-sm text-muted-foreground">
            <p>We do not buy products. We buy accelerators.</p>
            <p>We ship. Even tired. Even messy. Still shipping.</p>
            <p>We pay for tools that turn idea into build into upload.</p>
            <p>We want small utilities that save hours and rescue jams.</p>
            <p>We like glitch aesthetics, but we demand function.</p>
            <p>Love is the key, because love is what makes you finish.</p>
          </div>
        </div>

        {/* Search and Filter */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search products..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          
          <div className="flex gap-2 overflow-x-auto pb-2 sm:pb-0">
            {categories.map((cat) => (
              <Button
                key={cat.id}
                variant={selectedCategory === cat.id ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedCategory(cat.id)}
                className="flex items-center gap-1 whitespace-nowrap"
              >
                <cat.icon className="w-3 h-3" />
                {cat.name}
              </Button>
            ))}
          </div>
        </div>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {filteredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">No products found matching your criteria.</p>
          </div>
        )}

        {/* CTA */}
        <div className="text-center">
          <Button size="lg" variant="outline" className="group" asChild>
            <a 
              href="https://id01t.itch.io"
              target="_blank"
              rel="noopener noreferrer"
            >
              <ShoppingBag className="w-5 h-5 mr-2" />
              Visit itch.io Store
              <ExternalLink className="w-4 h-4 ml-2" />
            </a>
          </Button>
        </div>
      </div>
    </section>
  );
}
