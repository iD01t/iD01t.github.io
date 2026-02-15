import { useState, useEffect } from 'react';
import './index.css';
import { siteConfig } from './config';

// Components
import PasswordGate from './components/PasswordGate';

// Sections
import Hero from './sections/Hero';
import Books from './sections/Books';
import Trinity from './sections/Trinity';
import Albums from './sections/Albums';
import FeaturedRelease from './sections/FeaturedRelease';
import Platforms from './sections/Platforms';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hasAttempted, setHasAttempted] = useState(false);

  // Check for saved authentication
  useEffect(() => {
    const saved = sessionStorage.getItem('jda_auth');
    if (saved === 'true') {
      setIsAuthenticated(true);
    }
    setHasAttempted(true);
  }, []);

  const handleUnlock = () => {
    setIsAuthenticated(true);
    sessionStorage.setItem('jda_auth', 'true');
  };

  // Set page title
  useEffect(() => {
    document.title = siteConfig.title;
  }, []);

  if (!hasAttempted) {
    return (
      <div className="w-full h-screen bg-black flex items-center justify-center">
        <div className="text-green-500 font-mono animate-pulse">Loading...</div>
      </div>
    );
  }

  return (
    <main className="relative w-full min-h-screen bg-black text-white overflow-x-hidden">
      {/* Password Gate */}
      {!isAuthenticated && <PasswordGate onUnlock={handleUnlock} />}

      {/* Main Content */}
      {isAuthenticated && (
        <>
          {/* Fixed Navigation */}
          <nav className="fixed top-4 right-4 z-40 hidden md:flex items-center gap-2">
            <a 
              href="#books" 
              className="px-4 py-2 text-sm text-slate-400 hover:text-white bg-black/50 backdrop-blur-sm rounded-full border border-white/10 hover:border-cyan-400/50 transition-all"
            >
              Books
            </a>
            <a 
              href="#trinity" 
              className="px-4 py-2 text-sm text-slate-400 hover:text-white bg-black/50 backdrop-blur-sm rounded-full border border-white/10 hover:border-cyan-400/50 transition-all"
            >
              Trinity
            </a>
            <a 
              href="#albums" 
              className="px-4 py-2 text-sm text-slate-400 hover:text-white bg-black/50 backdrop-blur-sm rounded-full border border-white/10 hover:border-cyan-400/50 transition-all"
            >
              Albums
            </a>
            <a 
              href="#platforms" 
              className="px-4 py-2 text-sm text-slate-400 hover:text-white bg-black/50 backdrop-blur-sm rounded-full border border-white/10 hover:border-cyan-400/50 transition-all"
            >
              Connect
            </a>
          </nav>

          {/* Sections */}
          <Hero />
          <Books />
          <Trinity />
          <FeaturedRelease />
          <Albums />
          <Platforms />

          {/* Footer */}
          <footer className="w-full py-16 bg-black border-t border-white/10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
                {/* Brand */}
                <div className="md:col-span-2">
                  <h3 className="text-2xl font-bold text-white mb-2">JESS DAMAGED ARCHIVES</h3>
                  <p className="text-slate-400 mb-4 max-w-md">
                    A cyberpunk trilogy exploring the boundaries between human consciousness 
                    and artificial intelligence.
                  </p>
                </div>

                {/* Quick Links */}
                <div>
                  <h4 className="text-sm font-mono text-slate-500 mb-4">NAVIGATION</h4>
                  <ul className="space-y-2">
                    <li><a href="#books" className="text-slate-400 hover:text-cyan-400 transition-colors">The Books</a></li>
                    <li><a href="#trinity" className="text-slate-400 hover:text-cyan-400 transition-colors">The Trinity</a></li>
                    <li><a href="#albums" className="text-slate-400 hover:text-cyan-400 transition-colors">The 9-LP Canon</a></li>
                    <li><a href="#platforms" className="text-slate-400 hover:text-cyan-400 transition-colors">Connect</a></li>
                  </ul>
                </div>

                {/* Connect - Real Links Only */}
                <div>
                  <h4 className="text-sm font-mono text-slate-500 mb-4">CONNECT</h4>
                  <ul className="space-y-2">
                    <li>
                      <a 
                        href="https://twitter.com/DJiD01T" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-slate-400 hover:text-cyan-400 transition-colors"
                      >
                        X (Twitter)
                      </a>
                    </li>
                    <li>
                      <a 
                        href="https://www.youtube.com/@djid01t" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-slate-400 hover:text-cyan-400 transition-colors"
                      >
                        YouTube
                      </a>
                    </li>
                    <li>
                      <a 
                        href="https://open.spotify.com/artist/0EihiI3hgiPfIiyb154dgB" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-slate-400 hover:text-cyan-400 transition-colors"
                      >
                        Spotify
                      </a>
                    </li>
                    <li>
                      <a 
                        href="https://id01t.itch.io" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-slate-400 hover:text-cyan-400 transition-colors"
                      >
                        Itch.io
                      </a>
                    </li>
                    <li>
                      <a 
                        href="https://id01t.store" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-slate-400 hover:text-cyan-400 transition-colors"
                      >
                        HUB Store
                      </a>
                    </li>
                  </ul>
                </div>
              </div>

              {/* Bottom Bar */}
              <div className="pt-8 border-t border-white/10 flex flex-col md:flex-row items-center justify-between gap-4">
                <p className="text-sm text-slate-500">
                  © 2084 Jess Damaged Archives. All rights reserved.
                </p>
                <div className="flex items-center gap-4 text-sm text-slate-500">
                  <span className="font-mono text-cyan-400">ROOT_ACCESS GRANTED</span>
                </div>
              </div>
            </div>
          </footer>
        </>
      )}
    </main>
  );
}

export default App;
