import { useState } from 'react';
import { charactersConfig } from '../config';
import { Cpu, User, Bot, X, Quote } from 'lucide-react';

const iconMap: Record<string, React.ElementType> = {
  'iD01t': Cpu,
  'Jess Damaged': User,
  'Echo': Bot,
};

const accentColors = [
  { primary: '#00D4FF', bg: 'from-cyan-500/20 to-blue-500/20' },
  { primary: '#FF00AA', bg: 'from-pink-500/20 to-purple-500/20' },
  { primary: '#00FF88', bg: 'from-green-500/20 to-emerald-500/20' },
];

export default function Trinity() {
  const [selectedCharacter, setSelectedCharacter] = useState<typeof charactersConfig[0] | null>(null);

  return (
    <section id="trinity" className="w-full py-24 bg-[#0a0a0f]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <span className="inline-block px-3 py-1 mb-4 text-xs font-mono text-pink-400 border border-pink-400/30 rounded-full">
            [THE CONVERGENCE]
          </span>
          <h2 className="text-4xl md:text-5xl font-black text-white mb-4">
            THE <span className="bg-gradient-to-r from-cyan-400 via-pink-400 to-green-400 bg-clip-text text-transparent">TRINITY</span>
          </h2>
          <p className="text-slate-400 max-w-xl mx-auto">
            Three elements, each necessary, each incomplete without the others. 
            The Architect, The Human, and The Machine.
          </p>
        </div>

        {/* Character Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {charactersConfig.map((character, index) => {
            const Icon = iconMap[character.name] || User;
            const colors = accentColors[index];

            return (
              <div
                key={character.id}
                className="group relative"
              >
                {/* Glow Effect */}
                <div 
                  className="absolute -inset-0.5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-sm"
                  style={{ background: `linear-gradient(135deg, ${colors.primary}, transparent)` }}
                />

                {/* Card */}
                <div className="relative bg-[#050508] border border-white/10 rounded-2xl overflow-hidden h-full">
                  {/* Image */}
                  <div className="relative h-72 overflow-hidden">
                    <img
                      src={character.image}
                      alt={character.name}
                      className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                    />
                    <div 
                      className="absolute inset-0"
                      style={{ background: `linear-gradient(to top, #050508, transparent)` }}
                    />

                    {/* Role Badge */}
                    <div 
                      className="absolute top-4 left-4 px-3 py-1 rounded-full text-xs font-mono font-bold"
                      style={{ 
                        backgroundColor: `${colors.primary}20`,
                        color: colors.primary,
                        border: `1px solid ${colors.primary}40`
                      }}
                    >
                      <span className="flex items-center gap-2">
                        <Icon className="w-4 h-4" />
                        {character.role}
                      </span>
                    </div>
                  </div>

                  {/* Content */}
                  <div className="p-6">
                    <h3 
                      className="text-2xl font-bold mb-1 transition-colors"
                      style={{ color: colors.primary }}
                    >
                      {character.codename}
                    </h3>
                    <p className="text-slate-500 text-sm mb-3">{character.name}</p>
                    <p className="text-slate-400 text-sm mb-6">
                      {character.description}
                    </p>

                    {/* CTA */}
                    <button
                      onClick={() => setSelectedCharacter(character)}
                      className="w-full py-3 rounded-lg font-medium transition-all"
                      style={{ 
                        backgroundColor: `${colors.primary}15`,
                        color: colors.primary,
                        border: `1px solid ${colors.primary}40`
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.backgroundColor = `${colors.primary}30`;
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.backgroundColor = `${colors.primary}15`;
                      }}
                    >
                      View Dossier
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Quote */}
        <div className="mt-16 text-center">
          <Quote className="w-8 h-8 text-white/20 mx-auto mb-4" />
          <blockquote className="text-xl md:text-2xl text-slate-400 italic max-w-2xl mx-auto">
            "The wall between human and machine was never real. It was just a door we hadn't learned to open yet."
          </blockquote>
          <cite className="block mt-4 text-cyan-400 font-mono not-italic">— Echo</cite>
        </div>
      </div>

      {/* Character Modal */}
      {selectedCharacter && (
        <div 
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm p-4"
          onClick={() => setSelectedCharacter(null)}
        >
          <div 
            className="w-full max-w-2xl bg-[#0a0a0f] border border-white/20 rounded-2xl overflow-hidden"
            onClick={e => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="relative h-64 overflow-hidden">
              <img
                src={selectedCharacter.image}
                alt={selectedCharacter.name}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0f] via-transparent to-transparent" />
              <button
                onClick={() => setSelectedCharacter(null)}
                className="absolute top-4 right-4 w-10 h-10 bg-black/50 rounded-full flex items-center justify-center text-white hover:bg-black/70 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
              <div className="absolute bottom-6 left-6">
                <span className="text-xs font-mono text-slate-400">DOSSIER: {selectedCharacter.id.toUpperCase()}</span>
                <h3 className="text-3xl font-bold text-white">{selectedCharacter.codename}</h3>
                <p className="text-slate-400">{selectedCharacter.name}</p>
              </div>
            </div>

            {/* Modal Content */}
            <div className="p-8">
              <div className="mb-6">
                <span className="inline-block px-3 py-1 rounded-full text-sm font-mono bg-white/10 text-slate-300">
                  {selectedCharacter.role}
                </span>
              </div>
              <p className="text-slate-300 leading-relaxed text-lg">
                {selectedCharacter.description}
              </p>
              <div className="mt-6 pt-6 border-t border-white/10">
                <p className="text-slate-500 text-sm italic">
                  "{selectedCharacter.tagline}"
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
