import { useEffect, useRef, useState } from 'react';
import { 
  Github, 
  Music, 
  Package, 
  Star, 
  Heart,
  Zap,
  BookOpen,
  Headphones
} from 'lucide-react';

// Glitching number component
function GlitchStat({ value, suffix = '' }: { value: number; suffix?: string }) {
  const [displayValue, setDisplayValue] = useState(value);
  const [isGlitching, setIsGlitching] = useState(false);

  useEffect(() => {
    const glitchInterval = setInterval(() => {
      setIsGlitching(true);
      
      let glitchCount = 0;
      const maxGlitches = 8;
      const glitchTimer = setInterval(() => {
        // Generate random numbers around the base value
        const variance = Math.floor(Math.random() * value * 0.5);
        const sign = Math.random() > 0.5 ? 1 : -1;
        setDisplayValue(Math.max(0, value + sign * variance));
        glitchCount++;
        
        if (glitchCount >= maxGlitches) {
          clearInterval(glitchTimer);
          setDisplayValue(value);
          setIsGlitching(false);
        }
      }, 60);
    }, 4000 + Math.random() * 6000); // Random interval between 4-10 seconds

    return () => clearInterval(glitchInterval);
  }, [value]);

  return (
    <span className={`font-mono transition-all duration-75 ${isGlitching ? 'text-cyber-pink' : ''}`}>
      {displayValue.toLocaleString()}{suffix}
    </span>
  );
}

interface StatItemProps {
  icon: React.ElementType;
  value: number;
  label: string;
  suffix?: string;
  color: string;
  delay: number;
  glitch?: boolean;
}

function StatItem({ icon: Icon, value, label, suffix = '', color, delay, glitch = false }: StatItemProps) {
  const [count, setCount] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.3 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (!isVisible) return;

    const timer = setTimeout(() => {
      const duration = 2000;
      const steps = 60;
      const increment = value / steps;
      let current = 0;

      const interval = setInterval(() => {
        current += increment;
        if (current >= value) {
          setCount(value);
          clearInterval(interval);
        } else {
          setCount(Math.floor(current));
        }
      }, duration / steps);

      return () => clearInterval(interval);
    }, delay);

    return () => clearTimeout(timer);
  }, [isVisible, value, delay]);

  return (
    <div
      ref={ref}
      className={`relative group p-6 rounded-2xl bg-card/50 border border-border/50 backdrop-blur-sm hover:border-primary/30 transition-all duration-500 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      }`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      <div className={`absolute -inset-px rounded-2xl bg-gradient-to-r ${color} opacity-0 group-hover:opacity-20 transition-opacity blur-sm`} />
      <div className="relative flex items-center gap-4">
        <div className={`p-3 rounded-xl bg-gradient-to-br ${color} bg-opacity-10`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="text-3xl sm:text-4xl font-bold">
            {glitch ? (
              <GlitchStat value={value} suffix={suffix} />
            ) : (
              <>{count.toLocaleString()}{suffix}</>
            )}
          </div>
          <div className="text-sm text-muted-foreground">{label}</div>
        </div>
      </div>
    </div>
  );
}

export function Stats() {
  const stats = [
    { icon: BookOpen, value: 167, suffix: '+', label: 'eBooks Available', color: 'from-blue-500 to-cyan-500', glitch: true },
    { icon: Headphones, value: 103, suffix: '+', label: 'Audiobooks', color: 'from-purple-500 to-pink-500', glitch: true },
    { icon: Github, value: 36, label: 'GitHub Repositories', color: 'from-indigo-500 to-purple-500' },
    { icon: Music, value: 111, label: 'Music Tracks', color: 'from-green-500 to-emerald-500' },
    { icon: Package, value: 15, suffix: '+', label: 'Digital Products', color: 'from-orange-500 to-yellow-500' },
    { icon: Star, value: 99, suffix: '%', label: 'Satisfaction Rate', color: 'from-red-500 to-pink-500' },
    { icon: Heart, value: 24, suffix: '/7', label: 'Support Available', color: 'from-rose-500 to-red-500' },
    { icon: Zap, value: 9, label: 'Albums Released', color: 'from-teal-500 to-cyan-500' },
  ];

  return (
    <section className="relative py-20 overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            Trusted by <span className="text-gradient">Creators Worldwide</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Join creators who rely on iD01t Productions for their digital tools and creative content.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, index) => (
            <StatItem
              key={stat.label}
              {...stat}
              delay={index * 100}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
