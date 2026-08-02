import React, { useState, useEffect } from 'react';

export default function BadgeCeremony({ badge, onDismiss }) {
  const [show, setShow] = useState(false);

  useEffect(() => {
    requestAnimationFrame(() => setShow(true));
    const timer = setTimeout(onDismiss, 3500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={`fixed inset-0 z-[10000] flex items-center justify-center transition-all duration-700 ${
      show ? 'opacity-100' : 'opacity-0'
    }`}
      style={{
        background: show
          ? 'radial-gradient(circle at 50% 50%, rgba(52,211,153,0.25) 0%, rgba(15,23,42,0.85) 70%)'
          : 'rgba(15,23,42,0)',
      }}
      onClick={onDismiss}
    >
      <div className="text-center">
        <div className="w-32 h-32 rounded-full mx-auto mb-6 flex items-center justify-center relative holo-shimmer"
          style={{
            background: 'linear-gradient(135deg, #34d399, #6366f1, #34d399)',
            backgroundSize: '200% 200%',
            animation: 'badgeReveal 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both, holoShimmer 3s ease-in-out infinite',
            boxShadow: '0 0 60px rgba(52,211,153,0.4)',
          }}>
          <span className="text-5xl">{badge?.emoji || '🏅'}</span>
        </div>

        <div className="text-2xl font-bold text-emerald-400 mb-2"
             style={{ animation: 'floatUp 0.6s ease-out 0.3s both' }}>
          New Badge Unlocked!
        </div>
        <div className="text-lg text-gray-300" style={{ animation: 'floatUp 0.6s ease-out 0.5s both' }}>
          {badge?.name || 'Achievement Unlocked'}
        </div>
        {badge?.description && (
          <div className="text-sm text-gray-500 mt-2" style={{ animation: 'floatUp 0.6s ease-out 0.7s both' }}>
            {badge.description}
          </div>
        )}
      </div>
    </div>
  );
}
