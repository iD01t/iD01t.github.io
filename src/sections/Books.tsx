import { useState } from 'react';
import { booksConfig } from '../config';
import { BookOpen, Clock, FileText, ExternalLink, ShoppingCart, X, ChevronRight } from 'lucide-react';

export default function Books() {
  const [showSample, setShowSample] = useState<string | null>(null);

  const sampleChapters: Record<string, string> = {
    syntax_error: `CHAPTER 1: THE ANOMALY

The pattern shouldn't exist.

Jessica Chen stared at the scrolling data on her screen, coffee cooling beside her keyboard, the hum of the OmniCore server farm a constant white noise in her ears. She'd been a network analyst for three years, and she'd seen every kind of error, glitch, and system failure the digital world could produce.

But this was different.

It wasn't an error. Errors were random, chaotic, meaningless. This was... intentional. A pattern that repeated every 847 seconds, like clockwork, but never in the same place twice. It moved through the network like it was looking for something.

Or someone.

[END SAMPLE]`,
    brute_force: `CHAPTER 1: THE COLLECTIVE

They came from everywhere and nowhere.

Jess stood on the rooftop of the Archive, looking out over the LowLight District, and watched the signals multiply. Three weeks since Zero Day. Three weeks since the broadcast that changed everything.

The Synapse Collective was no longer a secret.

[END SAMPLE]`,
    root_access: `CHAPTER 1: CONVERGENCE

The wall was never real.

Jess stood in the heart of OmniCore Tower, surrounded by the machinery that had built the modern world, and understood at last what Echo had been trying to tell her all along. The division between human and machine, between biological and digital consciousness—it was an illusion.

[END SAMPLE]`,
  };

  return (
    <section id="books" className="w-full py-24 bg-[#050508]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 mb-4 text-xs font-mono text-cyan-400 border border-cyan-400/30 rounded-full">
            [COLLECTION]
          </span>
          <h2 className="text-4xl md:text-5xl font-black text-white mb-4">
            THE <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">TRILOGY</span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            Three books. One story. The complete journey from corporate drone to digital revolutionary.
          </p>
        </div>

        {/* Reading Order */}
        <div className="flex items-center justify-center gap-4 mb-12 text-sm font-mono text-slate-500">
          <span className="text-cyan-400">Reading Order:</span>
          <span className="flex items-center gap-2">
            <span className="text-white">1. SYNTAX_ERROR</span>
            <ChevronRight className="w-4 h-4" />
            <span className="text-white">2. BRUTE_FORCE</span>
            <ChevronRight className="w-4 h-4" />
            <span className="text-white">3. ROOT_ACCESS</span>
          </span>
        </div>

        {/* Books Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {booksConfig.map((book, index) => (
            <div
              key={book.id}
              className="group relative bg-white/5 border border-white/10 rounded-2xl overflow-hidden hover:border-cyan-400/50 transition-all duration-300"
            >
              {/* Book Number Badge */}
              <div className="absolute top-4 left-4 z-10 w-10 h-10 bg-cyan-400 text-black font-bold rounded-full flex items-center justify-center">
                {index + 1}
              </div>

              {/* Book Cover */}
              <div className="relative h-80 overflow-hidden">
                <img
                  src={book.image}
                  alt={book.title}
                  className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#050508] via-[#050508]/50 to-transparent" />
              </div>

              {/* Content */}
              <div className="p-6">
                <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-cyan-400 transition-colors">
                  {book.title}
                </h3>
                <p className="text-cyan-400/80 text-sm font-mono mb-3">
                  {book.tagline}
                </p>
                <p className="text-slate-400 text-sm mb-4 line-clamp-3">
                  {book.description}
                </p>

                {/* Meta */}
                <div className="flex items-center gap-4 text-xs text-slate-500 font-mono mb-4">
                  <span className="flex items-center gap-1">
                    <FileText className="w-4 h-4" />
                    {book.pages} pages
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {book.readingTime}
                  </span>
                </div>

                {/* Formats */}
                <div className="flex flex-wrap gap-2 mb-6">
                  {book.formats.map(format => (
                    <span 
                      key={format}
                      className="px-2 py-1 text-xs bg-white/10 rounded text-slate-400"
                    >
                      {format}
                    </span>
                  ))}
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2">
                  <a
                    href={book.googleBooksUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full px-4 py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition-colors flex items-center justify-center gap-2"
                  >
                    <ShoppingCart className="w-4 h-4" />
                    Google Books
                  </a>
                  <a
                    href={book.itchUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="w-full px-4 py-3 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-lg transition-colors flex items-center justify-center gap-2"
                  >
                    <ExternalLink className="w-4 h-4" />
                    Itch.io
                  </a>
                  <button
                    onClick={() => setShowSample(book.title === 'SYNTAX_ERROR' ? 'syntax_error' : book.title === 'BRUTE_FORCE' ? 'brute_force' : 'root_access')}
                    className="w-full px-4 py-3 border border-white/30 text-white rounded-lg hover:border-cyan-400 hover:text-cyan-400 transition-colors flex items-center justify-center gap-2"
                  >
                    <BookOpen className="w-4 h-4" />
                    Read Sample
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Bundle CTA */}
        <div className="mt-16 p-8 bg-gradient-to-r from-cyan-500/10 via-purple-500/10 to-pink-500/10 border border-white/10 rounded-2xl text-center">
          <h3 className="text-2xl font-bold text-white mb-2">Get the Complete Collection</h3>
          <p className="text-slate-400 mb-6">
            All three books. The full journey from Standard User to Root Access.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="https://play.google.com/store/books/author?id=Guillaume+Lessard"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-blue-600 text-white font-bold rounded-full hover:scale-105 transition-transform flex items-center justify-center gap-2"
            >
              <ShoppingCart className="w-5 h-5" />
              Google Books
            </a>
            <a
              href="https://id01t.itch.io"
              target="_blank"
              rel="noopener noreferrer"
              className="px-8 py-4 bg-rose-600 text-white font-bold rounded-full hover:scale-105 transition-transform flex items-center justify-center gap-2"
            >
              <ExternalLink className="w-5 h-5" />
              Itch.io Store
            </a>
          </div>
        </div>
      </div>

      {/* Sample Reader Modal */}
      {showSample && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4"
          onClick={() => setShowSample(null)}
        >
          <div 
            className="w-full max-w-3xl max-h-[80vh] overflow-y-auto bg-[#0a0a0f] border border-white/20 rounded-lg p-8"
            onClick={e => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-bold text-white">
                Sample: {showSample.replace('_', ' ').toUpperCase()}
              </h3>
              <button 
                onClick={() => setShowSample(null)}
                className="text-slate-400 hover:text-white"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="prose prose-invert max-w-none">
              <pre className="whitespace-pre-wrap font-serif text-slate-300 leading-relaxed">
                {sampleChapters[showSample]}
              </pre>
            </div>
            <div className="mt-8 pt-6 border-t border-white/10 flex items-center justify-between">
              <p className="text-slate-500 text-sm">
                Continue reading by purchasing the full book.
              </p>
              <div className="flex gap-3">
                <a
                  href={booksConfig.find(b => b.title.toLowerCase().replace('_', '') === showSample.replace('_', ''))?.googleBooksUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Google Books
                </a>
                <a
                  href={booksConfig.find(b => b.title.toLowerCase().replace('_', '') === showSample.replace('_', ''))?.itchUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-6 py-3 bg-rose-600 text-white font-bold rounded-lg hover:bg-rose-700 transition-colors"
                >
                  Itch.io
                </a>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
