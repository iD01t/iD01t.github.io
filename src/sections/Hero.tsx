import { useEffect, useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  ArrowRight, 
  Sparkles, 
  Zap, 
  Code, 
  Music,
  Gamepad2,
  BookOpen
} from 'lucide-react';

// Glitching number component
function GlitchNumber({ baseValue, suffix = '' }: { baseValue: number; suffix?: string }) {
  const [displayValue, setDisplayValue] = useState(baseValue);
  const [isGlitching, setIsGlitching] = useState(false);

  useEffect(() => {
    const glitchInterval = setInterval(() => {
      setIsGlitching(true);
      
      // Generate random glitch numbers
      let glitchCount = 0;
      const maxGlitches = 5;
      const glitchTimer = setInterval(() => {
        setDisplayValue(Math.floor(Math.random() * baseValue * 2) + Math.floor(Math.random() * 100));
        glitchCount++;
        
        if (glitchCount >= maxGlitches) {
          clearInterval(glitchTimer);
          setDisplayValue(baseValue);
          setIsGlitching(false);
        }
      }, 50);
    }, 5000 + Math.random() * 5000); // Random interval between 5-10 seconds

    return () => clearInterval(glitchInterval);
  }, [baseValue]);

  return (
    <span className={`font-mono transition-all duration-100 ${isGlitching ? 'text-cyber-pink animate-pulse' : ''}`}>
      {displayValue.toLocaleString()}{suffix}
    </span>
  );
}

export function Hero() {
  const [typedText, setTypedText] = useState('');
  const fullText = 'Digital Tools for Creators';
  const [isVisible, setIsVisible] = useState(false);
  const heroRef = useRef<HTMLElement>(null);

  useEffect(() => {
    setIsVisible(true);
    
    let index = 0;
    const timer = setInterval(() => {
      if (index <= fullText.length) {
        setTypedText(fullText.slice(0, index));
        index++;
      } else {
        clearInterval(timer);
      }
    }, 50);

    return () => clearInterval(timer);
  }, []);

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const features = [
    { icon: Code, label: 'Windows Apps', color: 'text-cyber-cyan' },
    { icon: BookOpen, label: 'Technical eBooks', color: 'text-cyber-purple' },
    { icon: Gamepad2, label: 'Interactive Games', color: 'text-cyber-pink' },
    { icon: Music, label: 'Original Music', color: 'text-cyber-green' },
  ];

  return (
    <section
      ref={heroRef}
      id="home"
      className="relative min-h-screen flex items-center justify-center pt-16 overflow-hidden"
    >
      {/* Background Effects */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Gradient Orbs */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse-glow" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '1s' }} />
        
        {/* Grid Pattern */}
        <div className="absolute inset-0 grid-pattern opacity-50" />
        
        {/* Scanline Effect */}
        <div className="absolute inset-0 pointer-events-none">
          <div 
            className="absolute w-full h-px bg-gradient-to-r from-transparent via-primary/30 to-transparent"
            style={{
              animation: 'scanline 8s linear infinite',
            }}
          />
        </div>
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          {/* AI Badge */}
          <div 
            className={`inline-flex items-center gap-2 mb-6 transition-all duration-700 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            <Badge 
              variant="outline" 
              className="px-4 py-2 text-sm font-medium border-primary/50 bg-primary/10 backdrop-blur-sm"
            >
              <Sparkles className="w-4 h-4 mr-2 text-primary" />
              AI-Native Production
            </Badge>
          </div>

          {/* Main Title */}
          <h1 
            className={`text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-bold mb-6 transition-all duration-700 delay-100 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            <span className="block font-mono text-primary">&gt; {typedText}</span>
            <span className="inline-block w-3 h-12 bg-primary ml-2 animate-pulse" />
          </h1>

          {/* Subtitle */}
          <p 
            className={`text-lg sm:text-xl md:text-2xl text-muted-foreground max-w-3xl mx-auto mb-8 transition-all duration-700 delay-200 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            Professional Windows utilities, 167+ technical eBooks, 103+ audiobooks, 
            indie games, and DJ iD01t cyberpunk electronic music. Built for creators who demand{' '}
            <span className="text-primary font-semibold">quality</span>,{' '}
            <span className="text-accent font-semibold">speed</span>, and{' '}
            <span className="text-cyber-green font-semibold">reliability</span>.
          </p>

          {/* Feature Tags */}
          <div 
            className={`flex flex-wrap justify-center gap-3 mb-10 transition-all duration-700 delay-300 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            {features.map((feature, index) => (
              <div
                key={feature.label}
                className="flex items-center gap-2 px-4 py-2 rounded-full bg-card border border-border/50 hover:border-primary/50 transition-all hover:scale-105"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <feature.icon className={`w-4 h-4 ${feature.color}`} />
                <span className="text-sm font-medium">{feature.label}</span>
              </div>
            ))}
          </div>

          {/* CTA Buttons */}
          <div 
            className={`flex flex-col sm:flex-row items-center justify-center gap-4 transition-all duration-700 delay-400 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            <Button
              size="lg"
              onClick={() => scrollToSection('#products')}
              className="group bg-gradient-to-r from-primary to-accent hover:opacity-90 text-primary-foreground px-8 py-6 text-lg font-semibold shadow-glow hover:shadow-glow-purple transition-all"
            >
              <Zap className="w-5 h-5 mr-2" />
              Explore Store
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => scrollToSection('#music')}
              className="group px-8 py-6 text-lg font-semibold border-2 hover:bg-primary/10 transition-all"
            >
              <Music className="w-5 h-5 mr-2" />
              Listen to Music
            </Button>
          </div>

          {/* Stats Preview with Glitching Numbers */}
          <div 
            className={`mt-16 grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto transition-all duration-700 delay-500 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            {[
              { value: 2473, label: 'Active Users', suffix: '' },
              { value: 36, label: 'GitHub Repos', suffix: '' },
              { value: 111, label: 'Music Tracks', suffix: '' },
              { value: 15, label: 'Products', suffix: '+' },
            ].map((stat) => (
              <div 
                key={stat.label} 
                className="text-center p-4 rounded-xl bg-card/50 border border-border/50 backdrop-blur-sm hover:border-primary/30 transition-all"
              >
                <div className="text-2xl sm:text-3xl font-bold text-gradient mb-1">
                  <GlitchNumber baseValue={stat.value} suffix={stat.suffix} />
                </div>
                <div className="text-xs sm:text-sm text-muted-foreground">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Gradient */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-background to-transparent" />
    </section>
  );
}
