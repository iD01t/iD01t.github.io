import { useState, useEffect } from 'react';
import { ThemeProvider } from '@/components/theme-provider';
import { Navigation } from '@/sections/Navigation';
import { Hero } from '@/sections/Hero';
import { Stats } from '@/sections/Stats';
import { Products } from '@/sections/Products';
import { ItchStore } from '@/sections/ItchStore';
import { MusicShowcase } from '@/sections/MusicShowcase';
import { Transmedia } from '@/sections/Transmedia';
import { Features } from '@/sections/Features';
import { Newsletter } from '@/sections/Newsletter';
import { Footer } from '@/sections/Footer';
import { ParticleBackground } from '@/components/ParticleBackground';

function App() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return null;
  }

  return (
    <ThemeProvider defaultTheme="dark" storageKey="id01t-theme">
      <div className="relative min-h-screen bg-background text-foreground overflow-x-hidden">
        <ParticleBackground />
        <Navigation />
        <main>
          <Hero />
          <Stats />
          <Products />
          <ItchStore />
          <MusicShowcase />
          <Transmedia />
          <Features />
          <Newsletter />
        </main>
        <Footer />
      </div>
    </ThemeProvider>
  );
}

export default App;
