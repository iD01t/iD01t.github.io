import { useRef, useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { 
  Github, 
  Star, 
  GitFork, 
  ExternalLink,
  Search,
  Code2,
  Terminal,
  Cpu,
  Music,
  BookOpen,
  Gamepad2
} from 'lucide-react';

interface Repo {
  id: string;
  name: string;
  description: string;
  language: string;
  stars: number;
  forks: number;
  category: 'app' | 'music' | 'tool' | 'ebook' | 'game' | 'other';
  url: string;
}

const repos: Repo[] = [
  {
    id: '1',
    name: 'iD01t.github.io',
    description: 'iD01t Productions Store - Main website and digital storefront',
    language: 'HTML',
    stars: 3,
    forks: 0,
    category: 'app',
    url: 'https://github.com/iD01t/iD01t.github.io'
  },
  {
    id: '2',
    name: 'ROOT_ACCESS',
    description: 'DJ iD01t ROOT_ACCESS Album - Cyberpunk electronic music project',
    language: 'Audio',
    stars: 2,
    forks: 0,
    category: 'music',
    url: 'https://github.com/iD01t/ROOT_ACCESS'
  },
  {
    id: '3',
    name: 'AI-2.0-CREATOR-SYSTEM',
    description: 'AI-powered content creation system for modern creators',
    language: 'Python',
    stars: 2,
    forks: 1,
    category: 'tool',
    url: 'https://github.com/iD01t/AI-2.0-CREATOR-SYSTEM'
  },
  {
    id: '4',
    name: 'iD01t-iSpeedupOS-MacOS',
    description: 'macOS optimization and performance tuning utility',
    language: 'Python',
    stars: 1,
    forks: 0,
    category: 'app',
    url: 'https://github.com/iD01t/iD01t-iSpeedupOS-MacOS'
  },
  {
    id: '5',
    name: 'Py2Win',
    description: 'Convert Python scripts to Windows executables with one click',
    language: 'Python',
    stars: 1,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/Py2Win'
  },
  {
    id: '6',
    name: 'sacred-frequency-generator',
    description: 'Generate sacred frequencies for meditation and healing',
    language: 'Python',
    stars: 1,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/sacred-frequency-generator'
  },
  {
    id: '7',
    name: 'eBooks',
    description: 'Collection of technical eBooks and educational content',
    language: 'Markdown',
    stars: 1,
    forks: 0,
    category: 'ebook',
    url: 'https://github.com/iD01t/eBooks'
  },
  {
    id: '8',
    name: 'iD01t_Ecosystem_Audit',
    description: 'Complete audit and documentation of the iD01t ecosystem',
    language: 'Markdown',
    stars: 0,
    forks: 0,
    category: 'other',
    url: 'https://github.com/iD01t/iD01t_Ecosystem_Audit'
  },
  {
    id: '9',
    name: 'asset_ripper',
    description: 'Extract and manage digital assets from various sources',
    language: 'JavaScript',
    stars: 0,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/asset_ripper'
  },
  {
    id: '10',
    name: 'sticker_mule_cli',
    description: 'Command-line interface for Sticker Mule API',
    language: 'JavaScript',
    stars: 0,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/sticker_mule_cli'
  },
  {
    id: '11',
    name: 'prompt_weaver',
    description: 'Advanced prompt engineering and management tool',
    language: 'JavaScript',
    stars: 0,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/prompt_weaver'
  },
  {
    id: '12',
    name: 'local_sentry',
    description: 'Local error tracking and monitoring solution',
    language: 'JavaScript',
    stars: 0,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/local_sentry'
  },
  {
    id: '13',
    name: 'go_pack_go',
    description: 'Go package management and build tool',
    language: 'JavaScript',
    stars: 0,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/go_pack_go'
  },
  {
    id: '14',
    name: 'MusicForge-Pro',
    description: 'Professional music production and editing tools',
    language: 'TypeScript',
    stars: 0,
    forks: 0,
    category: 'music',
    url: 'https://github.com/iD01t/MusicForge-Pro'
  },
  {
    id: '15',
    name: 'LastBroadcast',
    description: 'Indie game project with unique storytelling',
    language: 'TypeScript',
    stars: 0,
    forks: 0,
    category: 'game',
    url: 'https://github.com/iD01t/LastBroadcast'
  },
  {
    id: '16',
    name: 'html2win',
    description: 'Convert HTML applications to Windows executables',
    language: 'HTML',
    stars: 0,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/html2win'
  },
  {
    id: '17',
    name: 'Py2Win-Pro',
    description: 'Professional Python to Windows converter with advanced features',
    language: 'Python',
    stars: 0,
    forks: 0,
    category: 'tool',
    url: 'https://github.com/iD01t/Py2Win-Pro'
  },
];

const categories = [
  { id: 'all', name: 'All', icon: Code2 },
  { id: 'app', name: 'Apps', icon: Terminal },
  { id: 'tool', name: 'Tools', icon: Cpu },
  { id: 'music', name: 'Music', icon: Music },
  { id: 'ebook', name: 'eBooks', icon: BookOpen },
  { id: 'game', name: 'Games', icon: Gamepad2 },
];

const languageColors: Record<string, string> = {
  Python: 'bg-blue-500',
  JavaScript: 'bg-yellow-500',
  TypeScript: 'bg-blue-600',
  HTML: 'bg-orange-500',
  Markdown: 'bg-gray-500',
  Audio: 'bg-green-500',
};

function RepoCard({ repo }: { repo: Repo }) {
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
    <Card
      ref={ref}
      className={`group relative overflow-hidden bg-card/50 border-border/50 hover:border-primary/50 transition-all duration-500 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      }`}
    >
      <CardContent className="p-5">
        <div className="flex items-start justify-between gap-4 mb-3">
          <div className="flex items-center gap-2">
            <Github className="w-5 h-5 text-muted-foreground" />
            <h3 className="font-semibold line-clamp-1 group-hover:text-primary transition-colors">
              {repo.name}
            </h3>
          </div>
          <a 
            href={repo.url}
            target="_blank"
            rel="noopener noreferrer"
            className="opacity-0 group-hover:opacity-100 transition-opacity"
          >
            <ExternalLink className="w-4 h-4 text-muted-foreground hover:text-primary" />
          </a>
        </div>

        <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
          {repo.description}
        </p>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5">
              <span className={`w-3 h-3 rounded-full ${languageColors[repo.language] || 'bg-gray-400'}`} />
              <span className="text-xs text-muted-foreground">{repo.language}</span>
            </div>
          </div>

          <div className="flex items-center gap-3 text-sm text-muted-foreground">
            <span className="flex items-center gap-1">
              <Star className="w-4 h-4" />
              {repo.stars}
            </span>
            <span className="flex items-center gap-1">
              <GitFork className="w-4 h-4" />
              {repo.forks}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function GitHubRepos() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const filteredRepos = repos.filter((repo) => {
    const matchesSearch = 
      repo.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      repo.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || repo.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <section id="github" className="relative py-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 px-4 py-1">
            <Github className="w-3 h-3 mr-1" />
            Open Source
          </Badge>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-4">
            GitHub <span className="text-gradient">Repositories</span>
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Explore our collection of {repos.length}+ open-source projects. 
            From AI tools to music production, find something that sparks your creativity.
          </p>
        </div>

        {/* Search and Filter */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search repositories..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          
          <div className="flex gap-2 overflow-x-auto pb-2 sm:pb-0">
            {categories.map((cat) => (
              <Button
                key={cat.id}
                variant={selectedCategory === cat.id ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedCategory(cat.id)}
                className="flex items-center gap-1 whitespace-nowrap"
              >
                <cat.icon className="w-3 h-3" />
                {cat.name}
              </Button>
            ))}
          </div>
        </div>

        {/* Repos Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
          {filteredRepos.map((repo) => (
            <RepoCard key={repo.id} repo={repo} />
          ))}
        </div>

        {filteredRepos.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">No repositories found matching your criteria.</p>
          </div>
        )}

        {/* CTA */}
        <div className="text-center">
          <Button size="lg" variant="outline" className="group" asChild>
            <a 
              href="https://github.com/iD01t"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Github className="w-5 h-5 mr-2" />
              View All Repositories
              <ExternalLink className="w-4 h-4 ml-2" />
            </a>
          </Button>
        </div>
      </div>
    </section>
  );
}
