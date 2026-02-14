import { useRef, useEffect, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { 
  BookOpen, 
  Film, 
  Music, 
  Layers,
  Sparkles,
  ArrowRight,
  Cpu,
  Binary,
  ExternalLink
} from 'lucide-react';

interface TransmediaItem {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  image: string;
  type: 'fiction' | 'visual' | 'software';
  tags: string[];
  link?: string;
}

const transmediaItems: TransmediaItem[] = [
  {
    id: '1',
    title: 'SYNTAX_ERROR: The Jess Damaged Archives',
    subtitle: 'Cyberpunk eBook Trilogy',
    description: 'The definitive literary entry point into the ROOT_ACCESS universe. Documents the tactical and psychological collapse of digital sovereignty within the Echo Protocol framework.',
    image: 'https://images.unsplash.com/photo-1535879218367-8466d910aaa4?w=600&h=400&fit=crop',
    type: 'fiction',
    tags: ['NeoShanghai Setting', 'Jessica Chen / "Damaged" Protagonist', 'Sound Architect Character', 'High-Stakes Storytelling'],
    link: 'https://id01t.itch.io/syntax-error'
  },
  {
    id: '2',
    title: 'SYSTEM_OVERRIDE',
    subtitle: 'Visual Project',
    description: 'Morphic AI cinematic project demonstrating visual-to-rhythm synchronization. The Future Is Not a Choice. It Is a Command.',
    image: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=600&h=400&fit=crop',
    type: 'visual',
    tags: ['AI-Native Production', 'Cybernetic Study', 'Binary Heart', 'Visual Glitch Synchronization'],
    link: 'https://www.youtube.com/watch?v=dpn-XW0yen0'
  },
  {
    id: '3',
    title: 'ROOT_ACCESS // ZERO DAY',
    subtitle: 'Music Album',
    description: 'The complete cyberpunk electronic journey. Nine tracks of industrial dubstep and technical glitch designed to bypass standard auditory firewalls.',
    image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop',
    type: 'software',
    tags: ['Industrial Dubstep', 'System Override', 'Cyberpunk Electronic', 'Bass Music'],
    link: 'https://open.spotify.com/album/0tUOIdVIe63qCu4bUHOk0F'
  },
];

const typeIcons = {
  fiction: BookOpen,
  visual: Film,
  software: Cpu,
};

const typeColors = {
  fiction: 'from-pink-500 to-rose-500',
  visual: 'from-purple-500 to-indigo-500',
  software: 'from-cyan-500 to-blue-500',
};

function TransmediaCard({ item }: { item: TransmediaItem }) {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const Icon = typeIcons[item.type];

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
      {/* Image */}
      <div className="relative h-56 overflow-hidden">
        <img
          src={item.image}
          alt={item.title}
          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background via-background/30 to-transparent" />
        
        {/* Type Badge */}
        <div className="absolute top-4 left-4">
          <Badge className={`bg-gradient-to-r ${typeColors[item.type]} text-white`}>
            <Icon className="w-3 h-3 mr-1" />
            {item.type.charAt(0).toUpperCase() + item.type.slice(1)}
          </Badge>
        </div>
      </div>

      <CardContent className="p-6">
        <p className="text-sm text-muted-foreground mb-1">{item.subtitle}</p>
        <h3 className="text-xl font-bold mb-3 group-hover:text-primary transition-colors">
          {item.title}
        </h3>
        <p className="text-muted-foreground text-sm mb-4 line-clamp-3">
          {item.description}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {item.tags.slice(0, 3).map((tag) => (
            <Badge key={tag} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>

        {/* Link */}
        {item.link && (
          <Button variant="ghost" size="sm" className="group/btn p-0 h-auto" asChild>
            <a href={item.link} target="_blank" rel="noopener noreferrer">
              Explore
              <ArrowRight className="w-4 h-4 ml-1 group-hover/btn:translate-x-1 transition-transform" />
            </a>
          </Button>
        )}
      </CardContent>
    </Card>
  );
}

export function Transmedia() {
  return (
    <section id="universe" className="relative py-24 overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/5 rounded-full blur-3xl" />
      </div>

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <Badge variant="outline" className="mb-4 px-4 py-1 border-primary/50">
            <Layers className="w-3 h-3 mr-1" />
            Transmedia Architecture
          </Badge>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4">
            The <span className="text-gradient">ROOT_ACCESS</span> Universe
          </h2>
          <p className="text-muted-foreground max-w-3xl mx-auto mb-6">
            The transmedia architecture is constitutive rather than promotional: 
            the ROOT_ACCESS album cannot be fully understood without reference to 
            the SYNTAX_ERROR fiction and SYSTEM_OVERRIDE visuals with which it is 
            explicitly associated.
          </p>
          
          {/* Link to Fan Experience */}
          <Button size="lg" className="group" asChild>
            <a href="https://itechmobile.site" target="_blank" rel="noopener noreferrer">
              <Sparkles className="w-5 h-5 mr-2" />
              DJ iD01t Complete Fan Experience
              <ExternalLink className="w-4 h-4 ml-2" />
            </a>
          </Button>
        </div>

        {/* Connection Diagram */}
        <div className="flex flex-col lg:flex-row items-center justify-center gap-8 mb-16">
          {[
            { icon: BookOpen, label: 'Fiction', color: 'text-pink-500', bg: 'from-pink-500/20 to-rose-500/20' },
            { icon: Film, label: 'Visuals', color: 'text-purple-500', bg: 'from-purple-500/20 to-indigo-500/20' },
            { icon: Music, label: 'Music', color: 'text-cyan-500', bg: 'from-cyan-500/20 to-blue-500/20' },
          ].map((item, index) => (
            <div key={item.label} className="flex items-center gap-4">
              <div className={`flex flex-col items-center p-6 rounded-2xl bg-gradient-to-br ${item.bg} border border-border/50`}>
                <div className={`w-16 h-16 rounded-xl bg-background/80 flex items-center justify-center mb-3`}>
                  <item.icon className={`w-8 h-8 ${item.color}`} />
                </div>
                <span className="font-semibold">{item.label}</span>
              </div>
              {index < 2 && (
                <div className="hidden lg:flex items-center">
                  <Binary className="w-6 h-6 text-muted-foreground" />
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Transmedia Cards */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-12">
          {transmediaItems.map((item) => (
            <TransmediaCard key={item.id} item={item} />
          ))}
        </div>

        {/* Quote */}
        <div className="text-center max-w-2xl mx-auto">
          <blockquote className="relative">
            <Sparkles className="absolute -top-4 -left-4 w-8 h-8 text-primary/30" />
            <p className="text-lg italic text-muted-foreground mb-4">
              "The Future Is Not a Choice. It Is a Command."
            </p>
            <footer className="text-sm text-muted-foreground">
              — SYSTEM_OVERRIDE Manifesto
            </footer>
          </blockquote>
        </div>
      </div>
    </section>
  );
}
