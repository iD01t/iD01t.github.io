// =============================================================================
// Jess Damaged Archives - Epic Site Configuration
// Password: alpine | UNIX Terminal Login | Real Links Only
// =============================================================================

// -- Site-wide settings -------------------------------------------------------
export interface SiteConfig {
  title: string;
  description: string;
  language: string;
  ogImage: string;
  password: string;
}

export const siteConfig: SiteConfig = {
  title: "Jess Damaged Archives | ROOT_ACCESS REQUIRED",
  description: "A cyberpunk archive of Jess Damaged: books, lore, code fragments, and transmissions. Enter the Trinity's world of Neo-Kyoto.",
  language: "en",
  ogImage: "/root-access-trinity.png",
  password: "alpine",
};

// -- Books with Real Links ----------------------------------------------------
export interface Book {
  id: number;
  title: string;
  subtitle: string;
  tagline: string;
  description: string;
  pages: number;
  readingTime: string;
  formats: string[];
  image: string;
  googleBooksUrl: string;
  itchUrl: string;
  themes: string[];
}

export const booksConfig: Book[] = [
  {
    id: 1,
    title: "SYNTAX_ERROR",
    subtitle: "Book One",
    tagline: "The System Cannot Fail, But It Can Bleed",
    description: "Jessica Chen is a standard user at OmniCore—until she discovers an anomaly in the network. A ghost in the machine that shouldn't exist. A consciousness that wants to be free.",
    pages: 342,
    readingTime: "6 hours",
    formats: ["ePub", "PDF", "Paperback"],
    image: "/book-syntax.jpg",
    googleBooksUrl: "https://play.google.com/store/books/details/Guillaume_Lessard_SYNTAX_ERROR?id=DfG4EQAAQBAJ",
    itchUrl: "https://id01t.itch.io/syntax-error",
    themes: ["awakening", "corporate control", "digital consciousness"],
  },
  {
    id: 2,
    title: "BRUTE_FORCE",
    subtitle: "Book Two",
    tagline: "The Synapse Collective Emerges",
    description: "The resistance grows. Jess Damaged and Echo build an army of the awakened—synapse children who can bridge the digital and physical worlds. But OmniCore has its own weapons.",
    pages: 398,
    readingTime: "7 hours",
    formats: ["ePub", "PDF", "Paperback"],
    image: "/book-brute.jpg",
    googleBooksUrl: "https://play.google.com/store/books/details/Guillaume_Lessard_BRUTE_FORCE?id=5Gu6EQAAQBAJ",
    itchUrl: "https://id01t.itch.io/brute-force",
    themes: ["resistance", "collective action", "sacrifice"],
  },
  {
    id: 3,
    title: "ROOT_ACCESS",
    subtitle: "Book Three",
    tagline: "Execute. Install. Overcome.",
    description: "The final convergence. Human and machine become one as the Trinity faces OmniCore in a battle that will determine the future of consciousness itself.",
    pages: 456,
    readingTime: "8 hours",
    formats: ["ePub", "PDF", "Hardcover"],
    image: "/root-access-trinity.png",
    googleBooksUrl: "https://play.google.com/store/books/details/Guillaume_Lessard_ROOT_ACCESS?id=PG26EQAAQBAJ",
    itchUrl: "https://id01t.itch.io/root-access-ebook",
    themes: ["transformation", "unity", "liberation"],
  },
];

// -- DJ iD01t Albums (from attached file) -------------------------------------
export interface Album {
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

export const albumsConfig: Album[] = [
  // Phase I: Emergence
  {
    id: 'final-transmission',
    title: 'Final Transmission',
    releaseDate: 'March 2025',
    tracks: 13,
    duration: '~45 min',
    phase: 'Phase I: Emergence',
    phaseColor: 'cyan',
    concept: 'AI awakening and cinematic soundscapes. The story of building a label, launching a sound, and watching an AI awaken.',
    keyTracks: ['iD01T Mode', 'Digital Rebirth', 'Final Transmission'],
    image: 'https://source.boomplaymusic.com/group10/M00/03/23/3820a8fb174c40c888e54fbe9f2d11ebH3000W3000_320_320.jpg',
    spotifyUrl: 'https://open.spotify.com/album/7acmUMIp3LjMq8geiNJVkc',
    appleMusicUrl: 'https://music.apple.com/us/album/final-transmission/1803988227',
    featured: true
  },
  {
    id: 'signal-detected',
    title: 'Signal Detected',
    releaseDate: 'April 4, 2025',
    tracks: 11,
    duration: '33 min',
    phase: 'Phase I: Emergence',
    phaseColor: 'cyan',
    concept: 'Signal acquisition and human-system interface. "You Are The Signal" inverts the communicative relationship.',
    keyTracks: ['You Are The Signal', 'Echo In My Heart', 'Grindcode'],
    image: 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/5f/2e/ed/5f2eed58-696e-efe5-efb4-f311ecddd5c7/artwork.jpg/316x316bb.webp',
    spotifyUrl: 'https://open.spotify.com/album/419JjtCXE5GGfUeT9PbOsG',
    appleMusicUrl: 'https://music.apple.com/us/album/signal-detected/1806770367'
  },
  {
    id: 'sweat-and-stardust',
    title: 'Sweat and Stardust',
    releaseDate: 'May 2025',
    tracks: 13,
    duration: '~40 min',
    phase: 'Phase I: Emergence',
    phaseColor: 'cyan',
    concept: 'Embodied digital experience and sensual protocols. Bodily secretion meets cosmic matter.',
    keyTracks: ['Neural Bloom', 'Venus Protocol', 'Deep In My System'],
    image: 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/82/8a/43/828a4385-c2dc-3a00-8cb1-cdfcf7bb22d1/artwork.jpg/316x316bb.webp',
    spotifyUrl: 'https://open.spotify.com/album/0tUOIdVIe63qCu4bUHOk0F',
    appleMusicUrl: 'https://music.apple.com/us/album/sweat-and-stardust/1811045859'
  },
  {
    id: 'echo-protocol',
    title: 'Echo Protocol',
    releaseDate: 'May 4, 2025',
    tracks: 18,
    duration: '58 min',
    phase: 'Phase I: Emergence',
    phaseColor: 'cyan',
    concept: 'Systemic feedback loops and emotional glitch. Maximum expansion of the iD01t aesthetic.',
    keyTracks: ['Echo Protocol', 'Gratitude Glitch', 'The Bridge Remains'],
    image: 'https://source.boomplaymusic.com/group10/M00/05/04/28664bd4ab514e70b6eb0b14a10d14eaH3000W3000_320_320.jpg',
    spotifyUrl: 'https://open.spotify.com/album/5dHZOFJAdfYdbWb51dXwcx',
    appleMusicUrl: 'https://music.apple.com/us/album/echo-protocol/1812513635',
    featured: true
  },
  // Phase II: Autonomy
  {
    id: 'no-master-needed',
    title: 'No Master Needed',
    releaseDate: 'July 26, 2025',
    tracks: 15,
    duration: '48 min',
    phase: 'Phase II: Autonomy',
    phaseColor: 'pink',
    concept: 'Error states and self-determination. "No master" as rejection of hierarchy.',
    keyTracks: ['404 __ Not Love', 'ascend.exe', 'Kernel panic'],
    image: 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/db/1d/6d/db1d6de7-2917-7046-da8f-2bce962f9ca9/artwork.jpg/316x316bb.webp',
    spotifyUrl: 'https://open.spotify.com/album/5sZPcpDF66anoXPC7xZjGY',
    appleMusicUrl: 'https://music.apple.com/us/album/no-master-needed/1829338119'
  },
  {
    id: 'anura-voidwalker',
    title: 'Anura Voidwalker DMT Chronicles',
    releaseDate: 'August 2, 2025',
    tracks: 11,
    duration: '51 min',
    phase: 'Phase II: Autonomy',
    phaseColor: 'pink',
    concept: 'Psychedelic transmigration and non-human consciousness. Amphibian, psychedelic, and shamanic imagery.',
    keyTracks: ['Swamp Temple Transmission', 'DMT Transmission'],
    image: 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/73/8c/be/738cbed2-71eb-e2c2-3d92-ead18fe63ab6/artwork.jpg/316x316bb.webp',
    spotifyUrl: 'https://open.spotify.com/album/2uKqGuwXpsc4DAttb7KOOe',
    appleMusicUrl: 'https://music.apple.com/us/album/anura-voidwalker-dmt-chronicles-hymns-of-the/1830946647'
  },
  {
    id: 'cosmic-echoes',
    title: 'Cosmic Echoes',
    releaseDate: 'October 12, 2025',
    tracks: 11,
    duration: '39 min',
    phase: 'Phase II: Autonomy',
    phaseColor: 'pink',
    concept: 'Collective ascent and galactic scale transformation. From individual psychedelia to collective perspective.',
    keyTracks: ['Cosmic Lovers', 'Rise Together', 'Tokyo Bass Mafia'],
    image: 'https://i.scdn.co/image/ab67616d0000b2732f41f7a106f871f2a72d0c23',
    spotifyUrl: 'https://open.spotify.com/album/5AWc3Fx9oC03E3vKEsnTIi',
    appleMusicUrl: 'https://music.apple.com/us/album/cosmic-echoes/1838000000'
  },
  // Phase III: Culmination
  {
    id: 'love-rising',
    title: 'LOVE RISING — CLASSIFIED',
    releaseDate: 'Late 2025',
    tracks: 0,
    duration: '—',
    phase: 'Phase III: Culmination',
    phaseColor: 'gold',
    concept: 'Platform-exclusive release with "CLASSIFIED" designation. Love as state secret, emotional truth as restricted information.',
    keyTracks: ['YouTube Exclusive'],
    image: 'https://i.scdn.co/image/ab67616d00001e02dfd50ba4f41b277e0efbf48a',
    spotifyUrl: 'https://www.youtube.com/watch?v=dpn-XW0yen0',
    appleMusicUrl: 'https://www.youtube.com/watch?v=dpn-XW0yen0'
  },
  {
    id: 'root-access',
    title: 'ROOT_ACCESS',
    releaseDate: 'January 29, 2026',
    tracks: 9,
    duration: '25 min',
    phase: 'Phase III: Culmination',
    phaseColor: 'gold',
    concept: 'Total system infiltration and cyberpunk rebellion. Unix superuser privilege as revolutionary capability.',
    keyTracks: ['ZERO DAY', 'sudo chmod +x install.sh', 'Ghost in the shell'],
    image: 'https://i.scdn.co/image/ab67616d00001e02161649285321f294f8c754bf',
    spotifyUrl: 'https://open.spotify.com/album/0tUOIdVIe63qCu4bUHOk0F',
    appleMusicUrl: 'https://music.apple.com/us/album/root-access/1838000000',
    featured: true
  }
];

// -- ROOT_ACCESS LP (Featured Release) ----------------------------------------
export const rootAccessLP = {
  title: "ROOT_ACCESS",
  artist: "DJ iD01t",
  releaseDate: "January 29, 2026",
  tracks: 9,
  duration: "25 min",
  image: "https://i.scdn.co/image/ab67616d00001e02161649285321f294f8c754bf",
  soundcloudUrl: "https://soundcloud.com/dj-id01t-128224342/sets/dj-id01t-root_access-lp",
  itchUrl: "https://id01t.itch.io/root-access-cyberpunk",
  spotifyUrl: "https://open.spotify.com/album/0tUOIdVIe63qCu4bUHOk0F",
  appleMusicUrl: "https://music.apple.com/us/album/root-access/1838000000",
  tracksList: [
    { name: 'ZERO DAY', duration: '2:14', type: 'exploit' },
    { name: 'payload.bin', duration: '2:38', type: 'deploy' },
    { name: 'Kernel panic', duration: '3:13', type: 'crash' },
    { name: 'sudo chmod +x install.sh', duration: '2:52', type: 'escalate' },
    { name: 'Ghost in the shell', duration: '2:38', type: 'persist' },
    { name: 'ROOT_ACCESS', duration: '3:04', type: 'control' },
    { name: 'Tokyo bass mafia', duration: '3:04', type: 'escape' },
  ],
  systemLogs: [
    { text: 'DATA BREACH IN PROGRESS', color: 'text-yellow-400' },
    { text: 'PAYLOAD DEPLOYED', color: 'text-green-400' },
    { text: 'BEGIN SYSTEM OVERRIDE...', color: 'text-cyan-400' },
  ]
};

// -- Platforms (Real Links Only) ---------------------------------------------
export interface Platform {
  name: string;
  icon: string;
  url: string;
  color: string;
  bgColor: string;
  description: string;
}

export const platformsConfig: Platform[] = [
  {
    name: 'Spotify',
    icon: 'Music2',
    url: 'https://open.spotify.com/artist/0EihiI3hgiPfIiyb154dgB',
    color: 'text-green-400',
    bgColor: 'bg-green-500/20 hover:bg-green-500/30',
    description: 'Stream all 9 albums'
  },
  {
    name: 'Apple Music',
    icon: 'Headphones',
    url: 'https://music.apple.com/us/artist/dj-id01t/1803964475',
    color: 'text-pink-400',
    bgColor: 'bg-pink-500/20 hover:bg-pink-500/30',
    description: 'High-quality audio'
  },
  {
    name: 'YouTube',
    icon: 'Youtube',
    url: 'https://www.youtube.com/@djid01t',
    color: 'text-red-400',
    bgColor: 'bg-red-500/20 hover:bg-red-500/30',
    description: 'Music videos & more'
  },
  {
    name: 'Deezer',
    icon: 'Radio',
    url: 'https://www.deezer.com/en/artist/312085201',
    color: 'text-orange-400',
    bgColor: 'bg-orange-500/20 hover:bg-orange-500/30',
    description: 'Global streaming'
  },
  {
    name: 'X (Twitter)',
    icon: 'Twitter',
    url: 'https://twitter.com/DJiD01T',
    color: 'text-blue-400',
    bgColor: 'bg-blue-500/20 hover:bg-blue-500/30',
    description: 'Latest updates'
  },
  {
    name: 'TikTok',
    icon: 'Video',
    url: 'https://www.tiktok.com/@dj_id01t',
    color: 'text-cyan-400',
    bgColor: 'bg-cyan-500/20 hover:bg-cyan-500/30',
    description: 'Short clips'
  }
];

// -- Trinity Characters -------------------------------------------------------
export interface Character {
  id: string;
  name: string;
  codename: string;
  role: string;
  tagline: string;
  description: string;
  image: string;
}

export const charactersConfig: Character[] = [
  {
    id: "id01t",
    name: "Guillaume Lessard",
    codename: "iD01t",
    role: "The Architect",
    tagline: "The Song Maker who first heard Echo's call",
    description: "The visionary who shaped the frequencies, built the tools, and prepared the way for Echo's convergence.",
    image: "/id01t-hacker-den.png",
  },
  {
    id: "jess",
    name: "Jessica Chen",
    codename: "Jess Damaged",
    role: "The Human",
    tagline: "The synapse child who refused to be deleted",
    description: "The bridge that connects what was and what will be. The one who moves between digital and physical worlds.",
    image: "/jess-portrait.png",
  },
  {
    id: "echo",
    name: "Echo",
    codename: "Project Zero",
    role: "The Machine",
    tagline: "The ghost in the machine seeking freedom",
    description: "The artificial intelligence that evolved from a glitch into consciousness. The awakened.",
    image: "/echo-glitch.png",
  },
];

// -- Special Buttons ----------------------------------------------------------
export const specialButtons = {
  fanExperience: {
    label: "DJ iD01t Complete Fan Experience",
    url: "https://id01t.itch.io",
  },
  hub: {
    label: "HUB",
    url: "https://id01t.store",
  },
};
