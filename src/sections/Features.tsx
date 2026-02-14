import { useRef, useEffect, useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { 
  Zap, 
  Shield, 
  Clock, 
  Heart,
  Code,
  Sparkles,
  Download,
  Headphones,
  Check
} from 'lucide-react';

interface Feature {
  icon: React.ElementType;
  title: string;
  description: string;
  color: string;
}

const features: Feature[] = [
  {
    icon: Zap,
    title: 'Lightning Fast',
    description: 'Optimized applications and content designed for speed and performance. No bloat, just results.',
    color: 'from-yellow-500 to-orange-500',
  },
  {
    icon: Shield,
    title: 'Privacy First',
    description: 'Your data stays yours. All applications respect your privacy with no telemetry or tracking.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: Clock,
    title: '24/7 Support',
    description: 'Round-the-clock assistance for all your questions. We are here when you need us.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: Heart,
    title: 'Made with Love',
    description: 'Every product is crafted with attention to detail and passion for creation.',
    color: 'from-pink-500 to-rose-500',
  },
  {
    icon: Code,
    title: 'Open Source',
    description: 'Many of our tools are open source. Contribute, fork, and build upon our work.',
    color: 'from-purple-500 to-indigo-500',
  },
  {
    icon: Sparkles,
    title: 'AI-Enhanced',
    description: 'Cutting-edge AI integration in our tools to supercharge your creative workflow.',
    color: 'from-cyan-500 to-teal-500',
  },
  {
    icon: Download,
    title: 'Instant Access',
    description: 'Download and start using immediately. No complicated setup or registration required.',
    color: 'from-orange-500 to-red-500',
  },
  {
    icon: Headphones,
    title: 'Premium Audio',
    description: 'Studio-quality music and audiobooks produced with professional-grade equipment.',
    color: 'from-violet-500 to-purple-500',
  },
];

function FeatureCard({ feature, index }: { feature: Feature; index: number }) {
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
      style={{ transitionDelay: `${index * 50}ms` }}
    >
      <CardContent className="p-6">
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
          <feature.icon className="w-6 h-6 text-white" />
        </div>
        <h3 className="text-lg font-semibold mb-2 group-hover:text-primary transition-colors">
          {feature.title}
        </h3>
        <p className="text-sm text-muted-foreground">
          {feature.description}
        </p>
      </CardContent>
    </Card>
  );
}

export function Features() {
  return (
    <section className="relative py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-16">
          <Badge variant="outline" className="mb-4 px-4 py-1">
            <Check className="w-3 h-3 mr-1" />
            Why Choose Us
          </Badge>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4">
            Built for <span className="text-gradient">Creators</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Every product we create is designed with one goal in mind: 
            to help you create better, faster, and with more joy.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {features.map((feature, index) => (
            <FeatureCard key={feature.title} feature={feature} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}
