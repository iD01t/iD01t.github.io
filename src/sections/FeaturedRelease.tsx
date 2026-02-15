import { useEffect, useRef, useState } from 'react';
import { Play, ExternalLink, Terminal, AlertTriangle, CheckCircle } from 'lucide-react';
import { rootAccessLP } from '../config';

export default function FeaturedRelease() {
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
      { threshold: 0.2 }
    );

    if (sectionRef.current) {
      observer.observe(sectionRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <section 
      ref={sectionRef}
      id="featured"
      className="relative py-24 overflow-hidden bg-gradient-to-br from-emerald-950 via-teal-950 to-cyan-950"
    >
      {/* Background Effects */}
      <div className="absolute inset-0 opacity-30" style={{
        backgroundImage: `
          linear-gradient(rgba(0, 255, 136, 0.1) 1px, transparent 1px),
          linear-gradient(90deg, rgba(0, 255, 136, 0.1) 1px, transparent 1px)
        `,
        backgroundSize: '50px 50px'
      }} />
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl" />
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl" />

      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div 
          className={`text-center mb-16 transition-all duration-700 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/30 mb-6">
            <span className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse" />
            <span className="text-sm text-cyan-400 font-medium">NOW STREAMING</span>
          </div>
          
          <h2 className="text-4xl md:text-5xl lg:text-6xl font-black text-white mb-4">
            <span className="bg-gradient-to-r from-cyan-400 via-emerald-400 to-green-400 bg-clip-text text-transparent">ROOT_ACCESS</span> LP
          </h2>
          
          <p className="text-xl text-emerald-100/80 max-w-2xl mx-auto">
            The complete cyberpunk electronic journey. System override complete.
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left: Album Art */}
          <div 
            className={`relative transition-all duration-700 ${
              isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-12'
            }`}
            style={{ transitionDelay: '200ms' }}
          >
            <div className="relative group">
              {/* Glow Effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/40 to-emerald-500/40 rounded-2xl blur-3xl scale-110 group-hover:scale-125 transition-transform duration-500" />
              
              {/* Album Image */}
              <img
                src={rootAccessLP.image}
                alt="ROOT_ACCESS Album Cover"
                className="relative w-full max-w-md mx-auto rounded-2xl shadow-2xl"
                style={{
                  filter: 'drop-shadow(0 0 20px rgba(0, 255, 136, 0.3))'
                }}
              />
              
              {/* Floating Elements */}
              <div className="absolute -top-4 -right-4 px-3 py-1 bg-cyan-500/20 backdrop-blur-sm border border-cyan-500/40 rounded text-xs text-cyan-300 font-mono">
                v9.0.1
              </div>
              <div className="absolute -bottom-4 -left-4 px-3 py-1 bg-emerald-500/20 backdrop-blur-sm border border-emerald-500/40 rounded text-xs text-emerald-300 font-mono">
                {rootAccessLP.duration} MIN
              </div>
            </div>

            {/* Stream Buttons */}
            <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href={rootAccessLP.soundcloudUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-3 px-8 py-4 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-full font-semibold hover:from-orange-600 hover:to-orange-700 transition-all hover:scale-105 shadow-lg hover:shadow-orange-500/30"
              >
                <Play className="w-5 h-5" />
                Stream on SoundCloud
                <ExternalLink className="w-4 h-4" />
              </a>
              <a
                href={rootAccessLP.itchUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center justify-center gap-3 px-8 py-4 bg-gradient-to-r from-rose-500 to-pink-600 text-white rounded-full font-semibold hover:from-rose-600 hover:to-pink-700 transition-all hover:scale-105 shadow-lg hover:shadow-rose-500/30"
              >
                <ExternalLink className="w-5 h-5" />
                Get on Itch.io
              </a>
            </div>
          </div>

          {/* Right: Player & Tracklist */}
          <div 
            className={`space-y-6 transition-all duration-700 ${
              isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-12'
            }`}
            style={{ transitionDelay: '400ms' }}
          >
            {/* SoundCloud Player */}
            <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-1 overflow-hidden border border-white/10">
              <iframe
                width="100%"
                height="300"
                scrolling="no"
                frameBorder="no"
                allow="autoplay"
                src="https://w.soundcloud.com/player/?url=https%3A//soundcloud.com/dj-id01t-128224342/sets/dj-id01t-root_access-lp&color=%2300ff88&auto_play=false&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"
                className="rounded-xl"
              />
            </div>

            {/* System Logs */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 space-y-2 border border-white/10">
              {rootAccessLP.systemLogs.map((log, index) => (
                <div 
                  key={index}
                  className={`flex items-center gap-3 text-sm font-mono transition-all duration-500 ${
                    isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4'
                  }`}
                  style={{ transitionDelay: `${600 + index * 100}ms` }}
                >
                  {index === 0 && <AlertTriangle className={`w-4 h-4 ${log.color}`} />}
                  {index === 1 && <CheckCircle className={`w-4 h-4 ${log.color}`} />}
                  {index === 2 && <Terminal className={`w-4 h-4 ${log.color}`} />}
                  <span className={log.color}>{log.text}</span>
                </div>
              ))}
            </div>

            {/* Track List */}
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10">
              <h3 className="text-sm font-semibold text-slate-400 mb-4 uppercase tracking-wider">
                Track Sequence
              </h3>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {rootAccessLP.tracksList.map((track, index) => (
                  <div
                    key={index}
                    className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-white/5 transition-colors group cursor-pointer"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-xs text-slate-500 w-6">{index + 1}</span>
                      <span className="text-sm text-slate-300 group-hover:text-cyan-400 transition-colors font-mono">
                        {track.name}
                      </span>
                    </div>
                    <span className="text-xs text-slate-500">{track.duration}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
