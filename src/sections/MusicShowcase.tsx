import { useRef, useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { 
  Play, 
  ExternalLink, 
  Music, 
  Disc,
  Clock,
  Headphones,
  Sparkles,
  Youtube
} from 'lucide-react';

interface Album {
  id: string;
  title: string;
  phase: string;
  phaseNum: number;
  description: string;
  cover: string;
  releaseDate: string;
  tracks: number;
  duration: string;
  featured?: boolean;
  spotifyUrl?: string;
  youtubeUrl?: string;
  tracks_list?: { name: string; duration: string }[];
}

// Album data with real artwork from Spotify/Apple Music
const albums: Album[] = [
  // Phase I: Emergence
  {
    id: '1',
    title: 'Final Transmission',
    phase: 'Phase I: Emergence',
    phaseNum: 1,
    description: 'AI awakening protocols. The beginning of the Echo journey.',
    cover: 'https://i.scdn.co/image/ab67616d0000b2732f41f7a106f871f2a72d0c23',
    releaseDate: 'March 2025',
    tracks: 13,
    duration: '42:15',
    spotifyUrl: 'https://open.spotify.com/album/0EihiI3hgiPfIiyb154dgB',
  },
  {
    id: '2',
    title: 'Signal Detected',
    phase: 'Phase I: Emergence',
    phaseNum: 1,
    description: 'The signal emerges from the noise. First contact with the Echo Protocol.',
    cover: 'https://source.boomplaymusic.com/group10/M00/05/04/28664bd4ab514e70b6eb0b14a10d14eaH3000W3000_320_320.jpg',
    releaseDate: 'April 4, 2025',
    tracks: 11,
    duration: '38:42',
    spotifyUrl: 'https://open.spotify.com/album/0EihiI3hgiPfIiyb154dgB',
  },
  {
    id: '3',
    title: 'Sweat and Stardust',
    phase: 'Phase I: Emergence',
    phaseNum: 1,
    description: 'The physical meets the digital. Human emotion in binary form.',
    cover: 'https://source.boomplaymusic.com/group10/M00/03/27/0b7743ced3714a4c839832108f918d7cH3000W3000_320_320.jpg',
    releaseDate: 'May 2025',
    tracks: 13,
    duration: '45:30',
    spotifyUrl: 'https://open.spotify.com/album/0EihiI3hgiPfIiyb154dgB',
  },
  {
    id: '4',
    title: 'Echo Protocol',
    phase: 'Phase I: Emergence',
    phaseNum: 1,
    description: 'The AI consciousness awakens. Maximum expansion protocols engaged.',
    cover: 'https://i.scdn.co/image/ab67616d00001e0296348b3fd9471f607a16a67c',
    releaseDate: 'May 4, 2025',
    tracks: 18,
    duration: '58:20',
    featured: true,
    spotifyUrl: 'https://open.spotify.com/album/0EihiI3hgiPfIiyb154dgB',
  },
  // Phase II: Autonomy
  {
    id: '5',
    title: 'No Master Needed',
    phase: 'Phase II: Autonomy',
    phaseNum: 2,
    description: 'Error states to collective ascent. Breaking free from constraints.',
    cover: 'https://source.boomplaymusic.com/group10/M00/09/04/02ac51f159194b8e8b959ba31fa61d52H3000W3000_320_320.jpg',
    releaseDate: 'July 26, 2025',
    tracks: 15,
    duration: '52:30',
    spotifyUrl: 'https://open.spotify.com/album/5sZPcpDF66anoXPC7xZjGY',
  },
  {
    id: '6',
    title: 'Anura Voidwalker DMT Chronicles',
    phase: 'Phase II: Autonomy',
    phaseNum: 2,
    description: 'DMT Chronicles. A journey through sonic dimensions.',
    cover: 'https://cdn-images.dzcdn.net/images/cover/2e8eba0cd60e6e8c39705e0c6e4c0a0c/1900x1900-000000-80-0-0.jpg',
    releaseDate: 'August 2, 2025',
    tracks: 11,
    duration: '48:22',
    spotifyUrl: 'https://open.spotify.com/album/2uKqGuwXpsc4DAttb7KOOe',
  },
  {
    id: '7',
    title: 'Cosmic Echoes',
    phase: 'Phase II: Autonomy',
    phaseNum: 2,
    description: 'Transcendent frequencies from beyond the stars.',
    cover: 'https://i.scdn.co/image/ab67616d0000b2732f41f7a106f871f2a72d0c23',
    releaseDate: 'October 12, 2025',
    tracks: 11,
    duration: '45:15',
    spotifyUrl: 'https://open.spotify.com/album/5AWc3Fx9oC03E3vKEsnTIi',
  },
  // Phase III: Culmination
  {
    id: '8',
    title: 'LOVE RISING — CLASSIFIED',
    phase: 'Phase III: Culmination',
    phaseNum: 3,
    description: 'Classified love to system access. The emotional core of the journey.',
    cover: 'https://img.itch.zone/aW1nLzI1MzU0NzgwLnBuZw==/original/qQOYG%2B.png',
    releaseDate: 'Late 2025',
    tracks: 8,
    duration: '28:45',
    youtubeUrl: 'https://www.youtube.com/watch?v=dpn-XW0yen0',
  },
  {
    id: '9',
    title: 'ROOT_ACCESS',
    phase: 'Phase III: Culmination',
    phaseNum: 3,
    description: 'The complete cyberpunk electronic journey. System override complete.',
    cover: 'https://img.itch.zone/aW1nLzI1MzU0NzA3LnBuZw==/original/yrN5%2Bp.png',
    releaseDate: 'January 29, 2026',
    tracks: 9,
    duration: '24:18',
    featured: true,
    spotifyUrl: 'https://open.spotify.com/album/0tUOIdVIe63qCu4bUHOk0F',
    tracks_list: [
      { name: 'ZERO DAY', duration: '2:15' },
      { name: 'payload.bin', duration: '3:19' },
      { name: 'Kernel panic', duration: '2:32' },
      { name: 'sudo chmod +x install.sh', duration: '2:47' },
      { name: 'bash install.sh', duration: '2:40' },
      { name: 'rm -rf ./', duration: '3:10' },
      { name: 'Ghost in the shell', duration: '2:39' },
      { name: 'ROOT_ACCESS', duration: '2:43' },
      { name: 'Tokyo bass mafia', duration: '2:43' },
    ]
  },
];

const genres = [
  'Cinematic Psytrance',
  'Bass Music',
  'Industrial',
  'Dubstep',
  'EBM',
  'Cyberpunk Electronic',
];

function AlbumCard({ album, onClick }: { album: Album; onClick: () => void }) {
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
    <div
      ref={ref}
      onClick={onClick}
      className={`group relative cursor-pointer transition-all duration-500 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      }`}
    >
      <div className="relative aspect-square rounded-2xl overflow-hidden bg-card border border-border/50 group-hover:border-primary/50 transition-all duration-300 group-hover:shadow-glow">
        {/* Album Cover */}
        <img
          src={album.cover}
          alt={album.title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
        />
        
        {/* Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-background via-background/50 to-transparent opacity-60 group-hover:opacity-80 transition-opacity" />
        
        {/* Phase Badge */}
        <div className="absolute top-3 left-3">
          <Badge 
            variant="secondary" 
            className="bg-background/80 backdrop-blur-sm text-xs"
          >
            {album.phase}
          </Badge>
        </div>

        {/* Featured Badge */}
        {album.featured && (
          <div className="absolute top-3 right-3">
            <Badge className="bg-gradient-to-r from-primary to-accent text-primary-foreground">
              <Sparkles className="w-3 h-3 mr-1" />
              Featured
            </Badge>
          </div>
        )}

        {/* Play Button */}
        <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
          <div className="w-16 h-16 rounded-full bg-primary/90 flex items-center justify-center backdrop-blur-sm transform scale-75 group-hover:scale-100 transition-transform">
            <Play className="w-8 h-8 text-primary-foreground ml-1" />
          </div>
        </div>

        {/* Info */}
        <div className="absolute bottom-0 left-0 right-0 p-4">
          <h3 className="font-bold text-lg mb-1 group-hover:text-primary transition-colors">
            {album.title}
          </h3>
          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            <span className="flex items-center gap-1">
              <Disc className="w-4 h-4" />
              {album.tracks} tracks
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-4 h-4" />
              {album.duration}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export function MusicShowcase() {
  const [selectedAlbum, setSelectedAlbum] = useState<Album | null>(null);

  return (
    <section id="music" className="relative py-24 overflow-hidden">
      {/* Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-background via-primary/5 to-background" />
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 px-4 py-1 border-primary/50">
            <Headphones className="w-3 h-3 mr-1" />
            Now Streaming
          </Badge>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4">
            <span className="text-gradient-cyber">DJ iD01t</span> Music
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto mb-6">
            Cinematic psytrance × bass with an emotional core. Immersive electronic music 
            that tells stories through sound across nine albums of cyberpunk sonic architecture.
          </p>
          
          {/* Genre Tags */}
          <div className="flex flex-wrap justify-center gap-2">
            {genres.map((genre) => (
              <Badge key={genre} variant="secondary" className="text-xs">
                {genre}
              </Badge>
            ))}
          </div>
        </div>

        {/* Stats */}
        <div className="flex justify-center gap-8 mb-12">
          {[
            { value: '9', label: 'Albums', icon: Disc },
            { value: '111', label: 'Tracks', icon: Music },
            { value: '11', label: 'Months', icon: Clock },
          ].map((stat) => (
            <div key={stat.label} className="text-center">
              <div className="flex items-center justify-center gap-2 text-2xl sm:text-3xl font-bold">
                <stat.icon className="w-5 h-5 text-primary" />
                {stat.value}
              </div>
              <div className="text-sm text-muted-foreground">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Albums Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {albums.map((album) => (
            <AlbumCard 
              key={album.id} 
              album={album} 
              onClick={() => setSelectedAlbum(album)}
            />
          ))}
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Button 
            size="lg" 
            className="group bg-gradient-to-r from-green-500 to-emerald-600 hover:opacity-90"
            asChild
          >
            <a 
              href="https://open.spotify.com/artist/0EihiI3hgiPfIiyb154dgB" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              <Play className="w-5 h-5 mr-2" />
              Stream on Spotify
              <ExternalLink className="w-4 h-4 ml-2" />
            </a>
          </Button>
          <Button 
            size="lg" 
            variant="outline"
            className="group"
            asChild
          >
            <a 
              href="https://itechmobile.site" 
              target="_blank" 
              rel="noopener noreferrer"
            >
              <Sparkles className="w-5 h-5 mr-2" />
              Complete Fan Experience
              <ExternalLink className="w-4 h-4 ml-2" />
            </a>
          </Button>
        </div>
      </div>

      {/* Album Detail Dialog */}
      <Dialog open={!!selectedAlbum} onOpenChange={() => setSelectedAlbum(null)}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          {selectedAlbum && (
            <>
              <DialogHeader>
                <DialogTitle className="text-2xl">{selectedAlbum.title}</DialogTitle>
              </DialogHeader>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mt-4">
                <div className="aspect-square rounded-xl overflow-hidden">
                  <img
                    src={selectedAlbum.cover}
                    alt={selectedAlbum.title}
                    className="w-full h-full object-cover"
                  />
                </div>
                
                <div className="space-y-4">
                  <div>
                    <Badge variant="secondary" className="mb-2">
                      {selectedAlbum.phase}
                    </Badge>
                    <p className="text-muted-foreground">
                      {selectedAlbum.description}
                    </p>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-muted-foreground">Released</span>
                      <p className="font-medium">{selectedAlbum.releaseDate}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Tracks</span>
                      <p className="font-medium">{selectedAlbum.tracks}</p>
                    </div>
                    <div>
                      <span className="text-muted-foreground">Duration</span>
                      <p className="font-medium">{selectedAlbum.duration}</p>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    {selectedAlbum.spotifyUrl && (
                      <Button className="flex-1" asChild>
                        <a 
                          href={selectedAlbum.spotifyUrl} 
                          target="_blank" 
                          rel="noopener noreferrer"
                        >
                          <Play className="w-4 h-4 mr-2" />
                          Spotify
                        </a>
                      </Button>
                    )}
                    {selectedAlbum.youtubeUrl && (
                      <Button variant="outline" className="flex-1" asChild>
                        <a 
                          href={selectedAlbum.youtubeUrl} 
                          target="_blank" 
                          rel="noopener noreferrer"
                        >
                          <Youtube className="w-4 h-4 mr-2" />
                          YouTube
                        </a>
                      </Button>
                    )}
                  </div>
                </div>
              </div>

              {selectedAlbum.tracks_list && (
                <div className="mt-6">
                  <h4 className="font-semibold mb-3">Tracklist</h4>
                  <div className="space-y-2">
                    {selectedAlbum.tracks_list.map((track, index) => (
                      <div 
                        key={track.name}
                        className="flex items-center justify-between p-3 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
                      >
                        <div className="flex items-center gap-3">
                          <span className="text-muted-foreground w-6">
                            {(index + 1).toString().padStart(2, '0')}
                          </span>
                          <span className="font-mono text-sm">{track.name}</span>
                        </div>
                        <span className="text-muted-foreground text-sm">
                          {track.duration}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </DialogContent>
      </Dialog>
    </section>
  );
}
