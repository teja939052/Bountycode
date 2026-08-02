import React, { useState, useEffect } from 'react';

export default function StreakCeremony({ days, onDismiss }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    requestAnimationFrame(() => setShow(true));
    const timer = setTimeout(onDismiss, 3000);
    return () => clearTimeout(timer);
  }, []);

  const getMessage = () => {
    if (days >= 30) return { title: 'Legendary Streak!', msg: '30 days of fire! You are unstoppable!' };
    if (days >= 21) return { title: 'Diamond Streak!', msg: '21 days blazing! Almost there!' };
    if (days >= 14) return { title: 'Gold Streak!', msg: '14 days strong! Halfway to legend!' };
    if (days >= 7) return { title: 'Silver Streak!', msg: '7 days on fire! Keep the flame alive!' };
    return { title: `${days} Day Streak!`, msg: 'Your consistency is building power!' };
  };

  const { title, msg } = getMessage();

  return (
    <div className={`fixed inset-0 z-[10000] flex items-center justify-center transition-all duration-700 ${
      show ? 'opacity-100' : 'opacity-0'
    }`}
      style={{
        background: show
          ? 'radial-gradient(circle at 50% 50%, rgba(245,158,11,0.3) 0%, rgba(15,23,42,0.85) 70%)'
          : 'rgba(15,23,42,0)',
      }}
      onClick={onDismiss}
    >
      <div className="text-center">
        <div className="text-8xl mb-4" style={{
          animation: 'streakBlaze 0.8s ease-in-out infinite alternate',
          filter: 'drop-shadow(0 0 40px rgba(245,158,11,0.6))',
        }}>
          🔥
        </div>

        <div className="text-3xl font-bold text-amber-400 mb-2">{title}</div>
        <div className="text-lg text-amber-200/80 mb-6">{msg}</div>

        <div className="flex justify-center gap-1">
          {Array.from({ length: 7 }, (_, i) => (
            <div key={i} className="w-2 rounded-full" style={{
              height: 20 + Math.random() * 30,
              background: `linear-gradient(to top, #f59e0b, #ef4444)`,
              animation: `flameFlicker ${0.3 + Math.random() * 0.3}s ease-in-out ${i * 0.1}s infinite alternate`,
              opacity: 0.6 + Math.random() * 0.4,
            }} />
          ))}
        </div>
      </div>
    </div>
  );
}
