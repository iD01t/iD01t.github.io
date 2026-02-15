import { useState, useEffect, useRef } from 'react';
import { siteConfig } from '../config';

interface PasswordGateProps {
  onUnlock: () => void;
}

export default function PasswordGate({ onUnlock }: PasswordGateProps) {
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [bootSequence, setBootSequence] = useState<string[]>([]);
  const [showTerminal, setShowTerminal] = useState(false);
  const [glitchActive, setGlitchActive] = useState(true);
  const inputRef = useRef<HTMLInputElement>(null);

  // Boot sequence animation
  useEffect(() => {
    const bootLines = [
      '[SYSTEM] Initializing kernel...',
      '[KERNEL] Linux version 5.15.0-arch',
      '[BIOS] Performing memory test...',
      '[BIOS] Memory test complete: 16384MB OK',
      '[SYSTEM] Mounting root filesystem...',
      '[SYSTEM] Loading modules...',
      '[SECURITY] Trinity authentication required',
      '[AUTH] Waiting for root credentials...',
    ];

    let index = 0;
    const interval = setInterval(() => {
      if (index < bootLines.length) {
        setBootSequence(prev => [...prev, bootLines[index]]);
        index++;
      } else {
        clearInterval(interval);
        setTimeout(() => {
          setGlitchActive(false);
          setShowTerminal(true);
        }, 500);
      }
    }, 150);

    return () => clearInterval(interval);
  }, []);

  // Focus input when terminal shows
  useEffect(() => {
    if (showTerminal && inputRef.current) {
      inputRef.current.focus();
    }
  }, [showTerminal]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (password.toLowerCase() === siteConfig.password) {
      setError('');
      onUnlock();
    } else {
      setError('ACCESS DENIED: Invalid credentials');
      setPassword('');
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black overflow-hidden">
      {/* Green Glitch Effect */}
      {glitchActive && (
        <div className="absolute inset-0 pointer-events-none">
          {/* Scanlines */}
          <div 
            className="absolute inset-0"
            style={{
              background: 'repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,0,0.03) 2px, rgba(0,255,0,0.03) 4px)',
            }}
          />
          {/* Random glitch bars */}
          {[...Array(20)].map((_, i) => (
            <div
              key={i}
              className="absolute h-px bg-green-500/50"
              style={{
                top: `${Math.random() * 100}%`,
                left: 0,
                right: 0,
                animation: `glitch ${0.5 + Math.random()}s infinite`,
                animationDelay: `${Math.random() * 2}s`,
              }}
            />
          ))}
          {/* CRT flicker */}
          <div 
            className="absolute inset-0 bg-green-500/5 animate-pulse"
            style={{ animationDuration: '0.1s' }}
          />
        </div>
      )}

      {/* Boot Sequence */}
      {!showTerminal && (
        <div className="absolute inset-0 flex items-center justify-center p-8">
          <div className="w-full max-w-2xl font-mono text-green-500 text-sm md:text-base">
            {bootSequence.map((line, i) => (
              <div key={i} className="mb-1">
                <span className="opacity-50">{`[${String(i + 1).padStart(2, '0')}]`}</span>{' '}
                {line}
              </div>
            ))}
            <div className="animate-pulse">_</div>
          </div>
        </div>
      )}

      {/* UNIX Terminal Login */}
      {showTerminal && (
        <div className="absolute inset-0 flex items-center justify-center p-4">
          <div className="w-full max-w-2xl">
            {/* Terminal Window */}
            <div className="bg-black border border-green-500/50 rounded-lg overflow-hidden shadow-2xl shadow-green-500/20">
              {/* Terminal Header */}
              <div className="bg-green-900/20 px-4 py-2 border-b border-green-500/30 flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/50" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                <div className="w-3 h-3 rounded-full bg-green-500/50" />
                <span className="ml-4 text-xs text-green-500/70 font-mono">root@archives:~</span>
              </div>

              {/* Terminal Content */}
              <div className="p-6 md:p-8 font-mono">
                {/* ASCII Art Header */}
                <pre className="text-green-500 text-xs md:text-sm mb-6 overflow-x-auto">
 ██████╗ ███╗   ███╗███╗   ██╗██╗ ██████╗ ██████╗ ██████╗ ███████╗     ██████╗ ███████╗
██╔═══██╗████╗ ████║████╗  ██║██║██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔═══██╗██╔════╝
██║   ██║██╔████╔██║██╔██╗ ██║██║██║     ██║   ██║██████╔╝█████╗      ██║   ██║███████╗
██║   ██║██║╚██╔╝██║██║╚██╗██║██║██║     ██║   ██║██╔══██╗██╔══╝      ██║   ██║╚════██║
╚██████╔╝██║ ╚═╝ ██║██║ ╚████║██║╚██████╗╚██████╔╝██║  ██║███████╗    ╚██████╔╝███████║
 ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚══════╝
                </pre>

                {/* Auth Message */}
                <div className="mb-6 text-green-400/80 text-sm">
                  <div className="mb-2">[SYSTEM NOTIFICATION]: CRITICAL VULNERABILITY DETECTED</div>
                  <div className="mb-4 text-green-300">[MESSAGE]: "The song leads many. Few choose to follow."</div>
                  <div className="text-green-500/60">
                    <div>TRINITY_AUTH_REQUIRED:</div>
                    <div className="ml-4">{'>'} ARCHITECT_ID: iD01t</div>
                    <div className="ml-4">{'>'} HUMAN_ELEMENT: Damaged</div>
                    <div className="ml-4">{'>'} MACHINE_ID: Echo</div>
                  </div>
                </div>

                {/* Password Form */}
                <form onSubmit={handleSubmit} className="space-y-4">
                  <div className="flex items-center gap-2">
                    <span className="text-green-500">root@archives:~$</span>
                    <span className="text-green-400">passwd</span>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <span className="text-green-500">Enter ROOT_ACCESS password:</span>
                    <input
                      ref={inputRef}
                      type="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="bg-transparent border-none outline-none text-green-400 font-mono flex-1"
                      autoFocus
                      spellCheck={false}
                      autoComplete="off"
                    />
                    <span className="w-2 h-4 bg-green-500 animate-pulse" />
                  </div>

                  {error && (
                    <div className="text-red-500 text-sm animate-pulse">
                      {error}
                    </div>
                  )}

                  <div className="text-green-500/50 text-xs mt-4">
                    Hint: The password is the name of a lightweight Linux distribution
                  </div>
                </form>
              </div>
            </div>

            {/* Footer */}
            <div className="mt-8 text-center text-green-500/30 text-xs font-mono">
              Jess Damaged Archives v9.0.1 | Unauthorized access is monitored
            </div>
          </div>
        </div>
      )}

      <style>{`
        @keyframes glitch {
          0%, 100% { transform: translateX(0); opacity: 0; }
          50% { transform: translateX(${Math.random() * 10 - 5}px); opacity: 1; }
        }
      `}</style>
    </div>
  );
}
