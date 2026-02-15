import { useEffect, useRef, useState } from 'react';
import { ExternalLink, Sparkles, ShoppingBag } from 'lucide-react';

export default function Hero() {
  const titleRef = useRef<HTMLHeadingElement>(null);
  const [decodedTitle, setDecodedTitle] = useState('');
  const [isDecoding, setIsDecoding] = useState(true);

  // Decode animation
  useEffect(() => {
    const originalText = 'JESS DAMAGED';
    const chars = '01_01_01_';
    let iteration = 0;
    const maxIterations = 15;

    const interval = setInterval(() => {
      setDecodedTitle(
        originalText
          .split('')
          .map((char, index) => {
            if (char === ' ') return ' ';
            if (index < iteration / 2) return originalText[index];
            return chars[Math.floor(Math.random() * chars.length)];
          })
          .join('')
      );

      iteration += 1;

      if (iteration >= maxIterations) {
        setDecodedTitle(originalText);
        setIsDecoding(false);
        clearInterval(interval);
      }
    }, 80);

    return () => clearInterval(interval);
  }, []);

  return (
    <section className="relative w-full min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0">
        <img
          src="/jess-alley.png"
          alt="Neo-Kyoto"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black" />
        <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-transparent to-black/80" />
      </div>

      {/* Scanline Effect */}
      <div 
        className="absolute inset-0 pointer-events-none opacity-[0.03]"
        style={{
          backgroundImage: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.3) 2px, rgba(0,0,0,0.3) 4px)',
        }}
      />

      {/* Content */}
      <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center py-20">
        {/* Brand */}
        <div className="mb-8">
          <span className="text-xs font-mono text-slate-400 tracking-[0.3em]">
            THE ARCHIVES
          </span>
        </div>

        {/* Main Title with Decode Effect */}
        <h1
          ref={titleRef}
          className="text-5xl sm:text-6xl md:text-8xl lg:text-9xl font-black text-white mb-6 tracking-tight"
          style={{
            textShadow: '0 0 60px rgba(0, 212, 255, 0.4)',
          }}
        >
          {decodedTitle || 'JESS DAMAGED'}
          {isDecoding && (
            <span className="inline-block w-1 h-[0.8em] bg-cyan-400 ml-2 animate-pulse" />
          )}
        </h1>

        {/* Tagline */}
        <p className="text-xl md:text-2xl text-cyan-400 font-mono mb-6">
          The System Cannot Fail, But It Can Bleed
        </p>

        {/* Hook */}
        <p className="text-lg md:text-xl text-slate-300 max-w-2xl mx-auto mb-10">
          A cyberpunk trilogy exploring the boundaries between human consciousness and artificial intelligence. 
          3 books. 1 resistance. Zero compromise.
        </p>

        {/* Primary CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8">
          <a
            href="#books"
            className="group relative px-8 py-4 bg-cyan-400 text-black font-bold rounded-full overflow-hidden transition-all hover:scale-105 hover:shadow-lg hover:shadow-cyan-400/30"
          >
            <span className="relative z-10 flex items-center gap-2">
              READ BOOK I: SYNTAX_ERROR
            </span>
          </a>

          <a
            href="#trinity"
            className="px-8 py-4 border border-white/30 text-white font-medium rounded-full hover:border-cyan-400 hover:text-cyan-400 transition-all"
          >
            MEET THE TRINITY
          </a>
        </div>

        {/* Special Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="https://id01t.itch.io"
            target="_blank"
            rel="noopener noreferrer"
            className="group px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-full font-medium transition-all hover:scale-105 flex items-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            DJ iD01t Complete Fan Experience
            <ExternalLink className="w-4 h-4" />
          </a>
          <a
            href="https://id01t.store"
            target="_blank"
            rel="noopener noreferrer"
            className="group px-6 py-3 bg-gradient-to-r from-emerald-600 to-cyan-600 text-white rounded-full font-medium transition-all hover:scale-105 flex items-center gap-2"
          >
            <ShoppingBag className="w-4 h-4" />
            HUB
            <ExternalLink className="w-4 h-4" />
          </a>
        </div>

        {/* Quick Stats */}
        <div className="flex items-center justify-center gap-8 mt-16 text-sm font-mono text-slate-500">
          <div className="text-center">
            <div className="text-2xl font-bold text-white">3</div>
            <div>Books</div>
          </div>
          <div className="w-px h-8 bg-white/20" />
          <div className="text-center">
            <div className="text-2xl font-bold text-white">1,196</div>
            <div>Pages</div>
          </div>
          <div className="w-px h-8 bg-white/20" />
          <div className="text-center">
            <div className="text-2xl font-bold text-white">9</div>
            <div>Albums</div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 text-white/40 animate-bounce">
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      </div>
    </section>
  );
}
