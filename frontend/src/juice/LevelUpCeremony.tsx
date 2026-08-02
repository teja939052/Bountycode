import React, { useState, useEffect } from 'react';

export default function LevelUpCeremony({ level, onDismiss }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    requestAnimationFrame(() => setShow(true));
    const timer = setTimeout(onDismiss, 3000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={`fixed inset-0 z-[10000] flex items-center justify-center transition-all duration-700 ${
      show ? 'opacity-100 scale-100' : 'opacity-0 scale-50'
    }`}
      style={{
        background: show
          ? 'radial-gradient(circle at 50% 50%, rgba(99,102,241,0.4) 0%, rgba(15,23,42,0.85) 70%)'
          : 'rgba(15,23,42,0)',
      }}
      onClick={onDismiss}
    >
      <div className="text-center">
        <div className="text-8xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 mb-4"
             style={{
               filter: 'drop-shadow(0 0 30px rgba(99,102,241,0.5))',
               animation: 'levelUpPulse 1s ease-in-out infinite',
             }}>
          {level}
        </div>

        <div className="text-4xl font-bold text-white mb-2 tracking-wider"
             style={{ animation: 'floatUp 0.6s ease-out 0.3s both' }}>
          LEVEL UP!
        </div>

        <div className="text-lg text-indigo-300" style={{ animation: 'floatUp 0.6s ease-out 0.6s both' }}>
          You're getting stronger, adventurer.
        </div>

        <div className="flex justify-center gap-3 mt-6" style={{ animation: 'floatUp 0.6s ease-out 0.9s both' }}>
          {['⭐', '✨', '💫', '⭐', '✨'].map((s, i) => (
            <span key={i} className="text-2xl" style={{
              animation: `starSpin 2s ease-in-out ${i * 0.2}s infinite`,
            }}>{s}</span>
          ))}
        </div>
      </div>
    </div>
  );
}
