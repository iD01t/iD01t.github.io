import { useEffect, useRef, useState } from 'react';
import { Play, Music, Calendar, ChevronDown, ChevronUp } from 'lucide-react';
import { albumsConfig } from '../config';

interface Album {
  id: string;
  title: string;
  releaseDate: string;
  tracks: number;
  duration: string;
  phase: string;
  phaseColor: string;
  concept: string;
  keyTracks: string[];
  image: string;
  spotifyUrl: string;
  appleMusicUrl: string;
  featured?: boolean;
}

const AlbumCard = ({ album, index }: { album: Album; index: number }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const cardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (cardRef.current) {
      observer.observe(cardRef.current);
    }

    return () => observer.disconnect();
  }, []);

  const phaseColors: Record<string, { bg: string; border: string; text: string; glow: string }> = {
    cyan: {
      bg: 'bg-cyan-500/10',
      border: 'border-cyan-500/30',
      text: 'text-cyan-400',
      glow: 'shadow-cyan-500/20'
    },
    pink: {
      bg: 'bg-pink-500/10',
      border: 'border-pink-500/30',
      text: 'text-pink-400',
      glow: 'shadow-pink-500/20'
    },
    gold: {
      bg: 'bg-yellow-500/10',
      border: 'border-yellow-500/30',
      text: 'text-yellow-400',
      glow: 'shadow-yellow-500/20'
    }
  };

  const colors = phaseColors[album.phaseColor];

  return (
    <div
      ref={cardRef}
      className={`group relative transition-all duration-700 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'
      }`}
      style={{ transitionDelay: `${index * 100}ms` }}
    >
      <div 
        className={`bg-white/5 backdrop-blur-sm rounded-2xl overflow-hidden transition-all duration-500 hover:shadow-xl ${colors.glow} border border-white/10 hover:border-white/20 ${
          album.featured ? `border-2 ${colors.border}` : ''
        }`}
      >
        {/* Album Cover */}
        <div className="relative aspect-square overflow-hidden">
          <img
            src={album.image}
            alt={album.title}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
          
          {/* Phase Badge */}
          <div className={`absolute top-4 left-4 px-3 py-1 rounded-full ${colors.bg} ${colors.border} border`}>
            <span className={`text-xs font-medium ${colors.text}`}>{album.phase}</span>
          </div>

          {/* Featured Badge */}
          {album.featured && (
            <div className="absolute top-4 right-4 px-3 py-1 rounded-full bg-gradient-to-r from-purple-600 to-blue-600">
              <span className="text-xs font-medium text-white">Featured</span>
            </div>
          )}

          {/* Play Overlay */}
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <a
              href={album.spotifyUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center hover:bg-white/30 transition-colors"
            >
              <Play className="w-8 h-8 text-white ml-1" />
            </a>
          </div>

          {/* Title Overlay */}
          <div className="absolute bottom-0 left-0 right-0 p-4">
            <h3 className="text-xl font-bold text-white">{album.title}</h3>
            <div className="flex items-center gap-4 mt-2 text-sm text-slate-400">
              <span className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                {album.releaseDate}
              </span>
              {album.tracks > 0 && (
                <span className="flex items-center gap-1">
                  <Music className="w-4 h-4" />
                  {album.tracks} tracks
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Expandable Content */}
        <div className="p-4">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="w-full flex items-center justify-between text-sm text-slate-400 hover:text-white transition-colors"
          >
            <span>View Details</span>
            {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>

          {isExpanded && (
            <div className="mt-4 space-y-4 animate-in slide-in-from-top-2">
              <p className="text-sm text-slate-300">{album.concept}</p>
              
              <div>
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
                  Key Tracks
                </h4>
                <div className="flex flex-wrap gap-2">
                  {album.keyTracks.map((track, i) => (
                    <span
                      key={i}
                      className={`px-3 py-1 rounded-full text-xs ${colors.bg} ${colors.text} border ${colors.border}`}
                    >
                      {track}
                    </span>
                  ))}
                </div>
              </div>

              <div className="flex gap-3">
                <a
                  href={album.spotifyUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors"
                >
                  <Play className="w-4 h-4" />
                  Spotify
                </a>
                <a
                  href={album.appleMusicUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-sm font-medium transition-colors"
                >
                  <Music className="w-4 h-4" />
                  Apple Music
                </a>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default function Albums() {
  const [isVisible, setIsVisible] = useState(false);
  const sectionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold: 0.1 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  const phases = [
    { name: 'Phase I: Emergence', color: 'cyan', description: 'AI awakening to maximum expansion', albums: albumsConfig.filter(a => a.phase === 'Phase I: Emergence') },
    { name: 'Phase II: Autonomy', color: 'pink', description: 'Error states to collective ascent', albums: albumsConfig.filter(a => a.phase === 'Phase II: Autonomy') },
    { name: 'Phase III: Culmination', color: 'gold', description: 'Classified love to system access', albums: albumsConfig.filter(a => a.phase === 'Phase III: Culmination') }
  ];

  return (
    <section 
      ref={sectionRef}
      id="albums"
      className="relative py-24 bg-[#0a0a0f]"
    >
      {/* Background */}
      <div className="absolute inset-0 opacity-30" style={{
        backgroundImage: `
          linear-gradient(rgba(0, 212, 255, 0.1) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 212, 255, 0.1) 1px, transparent 1px)
        `,
        backgroundSize: '50px 50px'
      }} />
      <div className="absolute top-1/4 left-0 w-96 h-96 bg-purple-600/5 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 right-0 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div 
          className={`text-center mb-16 transition-all duration-700 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <h2 className="text-4xl md:text-5xl font-black text-white mb-4">
            The <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">9-LP Canon</span>
          </h2>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Journey through cinematic soundscapes and emotional depths. 
            Each album tells a unique story through immersive electronic compositions.
          </p>
          
          {/* Stats */}
          <div className="flex flex-wrap justify-center gap-8 mt-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-cyan-400">111</div>
              <div className="text-xs text-slate-500 uppercase tracking-wider">Total Tracks</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400">254+</div>
              <div className="text-xs text-slate-500 uppercase tracking-wider">Minutes</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-pink-400">11</div>
              <div className="text-xs text-slate-500 uppercase tracking-wider">Months</div>
            </div>
          </div>
        </div>

        {/* Phases */}
        <div className="space-y-24">
          {phases.map((phase, phaseIndex) => (
            <div key={phase.name}>
              {/* Phase Header */}
              <div 
                className={`flex items-center gap-4 mb-8 transition-all duration-700 ${
                  isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8'
                }`}
                style={{ transitionDelay: `${phaseIndex * 200}ms` }}
              >
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                  phase.color === 'cyan' ? 'bg-cyan-500/20 text-cyan-400' :
                  phase.color === 'pink' ? 'bg-pink-500/20 text-pink-400' :
                  'bg-yellow-500/20 text-yellow-400'
                }`}>
                  <span className="text-xl font-bold">
                    {phaseIndex + 1}
                  </span>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-white">{phase.name}</h3>
                  <p className="text-slate-400 text-sm">{phase.description}</p>
                </div>
              </div>

              {/* Albums Grid */}
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {phase.albums.map((album, index) => (
                  <AlbumCard key={album.id} album={album} index={phaseIndex * 4 + index} />
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
