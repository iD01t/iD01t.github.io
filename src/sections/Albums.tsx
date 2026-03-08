import { useEffect, useRef, useState } from 'react';
import { Play, Music, Calendar, ChevronDown, ChevronUp, Zap } from 'lucide-react';
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

interface Single {
  id: string;
  title: string;
  releaseDate: string;
  duration: string;
  concept: string;
  image: string;
  spotifyUrl: string;
  appleMusicUrl?: string;
}

// Singles data - move to ../config when ready
// Note: Love Rising albumsConfig entry should use:
//   image: 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/60/25/05/60250592-e6af-c195-2ae3-e03a37f75a26/artwork.jpg/316x316bb.webp'
//   appleMusicUrl: 'https://music.apple.com/ca/album/love-rising/1881282585'
const singlesConfig: Single[] = [
  {
    id: 'brute-force',
    title: 'BRUTE_FORCE',
    releaseDate: 'Mar 4, 2026',
    duration: '2:58',
    concept: 'A relentless, high-energy assault on the senses - raw power distilled into pure electronic force.',
    image: 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/5e/5f/4b/5e5f4ba6-4f7c-2c0f-a233-631e1a7e9120/artwork.jpg/208x208bb.webp',
    spotifyUrl: 'https://open.spotify.com/album/6qHqwS3bNMu8qqHDlMPraL',
    appleMusicUrl: 'https://music.apple.com/ca/song/brute-force/1882616414',
  },
  {
    id: 'syntax-error',
    title: 'SYNTAX_ERROR',
    releaseDate: 'Mar 4, 2026',
    duration: '2:59',
    concept: 'When the code breaks and beauty emerges from the glitch - a meditation on failure as creation.',
    image: 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/e2/27/9f/e2279f2c-17f3-6f62-ade9-b30d25bfb3a4/artwork.jpg/316x316bb.webp',
    spotifyUrl: 'https://open.spotify.com/album/0mkG4oS3fTcn1NIj1jN4xI',
    appleMusicUrl: 'https://music.apple.com/ca/album/syntax-error/1882480691?i=1882480695',
  },
];

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
    if (cardRef.current) observer.observe(cardRef.current);
    return () => observer.disconnect();
  }, []);

  const phaseColors: Record<string, { bg: string; border: string; text: string; glow: string }> = {
    cyan:  { bg: 'bg-cyan-500/10',   border: 'border-cyan-500/30',   text: 'text-cyan-400',   glow: 'shadow-cyan-500/20'   },
    pink:  { bg: 'bg-pink-500/10',   border: 'border-pink-500/30',   text: 'text-pink-400',   glow: 'shadow-pink-500/20'   },
    gold:  { bg: 'bg-yellow-500/10', border: 'border-yellow-500/30', text: 'text-yellow-400', glow: 'shadow-yellow-500/20' },
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
        <div className="relative aspect-square overflow-hidden">
          <img
            src={album.image}
            alt={album.title}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
          <div className={`absolute top-4 left-4 px-3 py-1 rounded-full ${colors.bg} ${colors.border} border`}>
            <span className={`text-xs font-medium ${colors.text}`}>{album.phase}</span>
          </div>
          {album.featured && (
            <div className="absolute top-4 right-4 px-3 py-1 rounded-full bg-gradient-to-r from-purple-600 to-blue-600">
              <span className="text-xs font-medium text-white">Featured</span>
            </div>
          )}
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
                <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Key Tracks</h4>
                <div className="flex flex-wrap gap-2">
                  {album.keyTracks.map((track, i) => (
                    <span key={i} className={`px-3 py-1 rounded-full text-xs ${colors.bg} ${colors.text} border ${colors.border}`}>
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

const SingleCard = ({ single, index }: { single: Single; index: number }) => {
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
    if (cardRef.current) observer.observe(cardRef.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={cardRef}
      className={`group relative transition-all duration-700 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'
      }`}
      style={{ transitionDelay: `${index * 100}ms` }}
    >
      <div className="bg-white/5 backdrop-blur-sm rounded-2xl overflow-hidden transition-all duration-500 hover:shadow-xl shadow-orange-500/10 border border-white/10 hover:border-orange-500/30">
        <div className="relative aspect-square overflow-hidden">
          <img
            src={single.image}
            alt={single.title}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
          <div className="absolute top-4 left-4 px-3 py-1 rounded-full bg-orange-500/10 border border-orange-500/30">
            <span className="text-xs font-medium text-orange-400 flex items-center gap-1">
              <Zap className="w-3 h-3" />
              Single
            </span>
          </div>
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
            <a
              href={single.spotifyUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center hover:bg-white/30 transition-colors"
            >
              <Play className="w-8 h-8 text-white ml-1" />
            </a>
          </div>
          <div className="absolute bottom-0 left-0 right-0 p-4">
            <h3 className="text-xl font-bold text-white">{single.title}</h3>
            <div className="flex items-center gap-4 mt-2 text-sm text-slate-400">
              <span className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                {single.releaseDate}
              </span>
              <span className="flex items-center gap-1">
                <Music className="w-4 h-4" />
                {single.duration}
              </span>
            </div>
          </div>
        </div>
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
              <p className="text-sm text-slate-300">{single.concept}</p>
              <div className="flex gap-3">
                <a
                  href={single.spotifyUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium transition-colors"
                >
                  <Play className="w-4 h-4" />
                  Spotify
                </a>
                {single.appleMusicUrl && (
                  <a
                    href={single.appleMusicUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-white rounded-lg text-sm font-medium transition-colors"
                  >
                    <Music className="w-4 h-4" />
                    Apple Music
                  </a>
                )}
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
    if (sectionRef.current) observer.observe(sectionRef.current);
    return () => observer.disconnect();
  }, []);

  const phases = [
    { name: 'Phase I: Emergence',    color: 'cyan', description: 'AI awakening to maximum expansion', albums: albumsConfig.filter((a: Album) => a.phase === 'Phase I: Emergence')    },
    { name: 'Phase II: Autonomy',    color: 'pink', description: 'Error states to collective ascent',  albums: albumsConfig.filter((a: Album) => a.phase === 'Phase II: Autonomy')    },
    { name: 'Phase III: Culmination', color: 'gold', description: 'Classified love to system access',  albums: albumsConfig.filter((a: Album) => a.phase === 'Phase III: Culmination') },
  ];

  return (
    <section
      ref={sectionRef}
      id="albums"
      className="relative py-24 bg-[#0a0a0f]"
    >
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
        <div
          className={`text-center mb-16 transition-all duration-700 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <h2 className="text-4xl md:text-5xl font-black text-white mb-4">
            The <span className="bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">9-LP Canon</span>
            <span className="block text-2xl md:text-3xl mt-2 bg-gradient-to-r from-orange-400 to-yellow-400 bg-clip-text text-transparent">
              + Singles
            </span>
          </h2>
          <p className="text-xl text-slate-400 max-w-3xl mx-auto">
            Journey through cinematic soundscapes and emotional depths.
            Each album tells a unique story through immersive electronic compositions.
          </p>
          <div className="flex flex-wrap justify-center gap-8 mt-8">
            <div className="text-center">
              <div className="text-3xl font-bold text-cyan-400">9</div>
              <div className="text-xs text-slate-500 uppercase tracking-wider">LPs</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-400">{singlesConfig.length}</div>
              <div className="text-xs text-slate-500 uppercase tracking-wider">Singles</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400">111+</div>
              <div className="text-xs text-slate-500 uppercase tracking-wider">Total Tracks</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-pink-400">12+</div>
              <div className="text-xs text-slate-500 uppercase tracking-wider">Months</div>
            </div>
          </div>
        </div>

        <div className="space-y-24">
          {phases.map((phase, phaseIndex) => (
            <div key={phase.name}>
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
                  <span className="text-xl font-bold">{phaseIndex + 1}</span>
                </div>
                <div>
                  <h3 className="text-2xl font-bold text-white">{phase.name}</h3>
                  <p className="text-slate-400 text-sm">{phase.description}</p>
                </div>
              </div>
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                {phase.albums.map((album: Album, index: number) => (
                  <AlbumCard key={album.id} album={album} index={phaseIndex * 4 + index} />
                ))}
              </div>
            </div>
          ))}
        </div>

        {singlesConfig.length > 0 && (
          <div className="mt-24">
            <div
              className={`flex items-center gap-4 mb-8 transition-all duration-700 ${
                isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8'
              }`}
            >
              <div className="w-12 h-12 rounded-xl flex items-center justify-center bg-orange-500/20 text-orange-400">
                <Zap className="w-6 h-6" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-white">Singles</h3>
                <p className="text-slate-400 text-sm">Standalone transmissions from the iD01T universe</p>
              </div>
            </div>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {singlesConfig.map((single: Single, index: number) => (
                <SingleCard key={single.id} single={single} index={index} />
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
