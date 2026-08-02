import React, { useState, useEffect } from 'react';

const RARITY_COLORS = {
  common: { border: '#64748b', glow: 'rgba(100,116,139,0.3)', bg: 'from-slate-700 to-slate-800' },
  uncommon: { border: '#34d399', glow: 'rgba(52,211,153,0.3)', bg: 'from-emerald-700 to-emerald-900' },
  rare: { border: '#3b82f6', glow: 'rgba(59,130,246,0.3)', bg: 'from-blue-700 to-blue-900' },
  epic: { border: '#8b5cf6', glow: 'rgba(139,92,246,0.3)', bg: 'from-purple-700 to-purple-900' },
  legendary: { border: '#f59e0b', glow: 'rgba(245,158,11,0.3)', bg: 'from-amber-600 to-amber-800' },
};

export default function CardRevealCeremony({ card, onDismiss }) {
  const [flipped, setFlipped] = useState(false);
  const colors = RARITY_COLORS[card?.rarity] || RARITY_COLORS.common;

  useEffect(() => {
    const timer = setTimeout(() => setFlipped(true), 500);
    const dismiss = setTimeout(onDismiss, 3500);
    return () => { clearTimeout(timer); clearTimeout(dismiss); };
  }, []);

  return (
    <div className="fixed inset-0 z-[10000] flex items-center justify-center bg-black/60 backdrop-blur-sm"
         onClick={onDismiss}>

      <div className="perspective-1000" style={{ perspective: '1000px' }}>
        <div
          className="relative w-64 h-80 transition-transform duration-700 cursor-pointer"
          style={{
            transformStyle: 'preserve-3d',
            transform: flipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
          }}
        >
          <div className="absolute inset-0 rounded-2xl flex items-center justify-center"
            style={{
              backfaceVisibility: 'hidden',
              background: 'linear-gradient(135deg, #1e293b, #0f172a)',
              border: '2px solid #334155',
            }}>
            <div className="text-4xl opacity-50">?</div>
            <div className="absolute inset-0 rounded-2xl" style={{
              background: 'repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.02) 10px, rgba(255,255,255,0.02) 20px)',
            }} />
          </div>

          <div className="absolute inset-0 rounded-2xl p-6 flex flex-col items-center justify-center"
            style={{
              backfaceVisibility: 'hidden',
              transform: 'rotateY(180deg)',
              background: `linear-gradient(135deg, ${colors.bg.split(' ')[0]}, ${colors.bg.split(' ')[2]})`,
              border: `2px solid ${colors.border}`,
              boxShadow: `0 0 40px ${colors.glow}`,
            }}>
            <div className="text-5xl mb-3">{card?.emoji || '💎'}</div>
            <div className="text-lg font-bold text-white text-center">{card?.name || 'Mystery Card'}</div>
            <div className="text-xs mt-2 px-3 py-1 rounded-full font-medium"
              style={{ backgroundColor: colors.border + '40', color: colors.border }}>
              {card?.rarity || 'Common'}
            </div>
            {card?.description && (
              <div className="text-xs text-gray-400 text-center mt-3">{card.description}</div>
            )}
            <div className="absolute top-0 left-0 right-0 h-1 rounded-t-2xl" style={{ backgroundColor: colors.border }} />
          </div>
        </div>
      </div>
    </div>
  );
}
