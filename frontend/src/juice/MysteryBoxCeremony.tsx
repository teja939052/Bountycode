import React, { useState, useEffect } from 'react';

const REWARD_TYPES = {
  xp: { emoji: '⚡', label: 'XP Boost', color: '#a78bfa' },
  badge: { emoji: '🏅', label: 'Badge', color: '#34d399' },
  streak_freeze: { emoji: '❄️', label: 'Streak Freeze', color: '#60a5fa' },
  double_xp: { emoji: '×2', label: 'Double XP', color: '#f472b6' },
  coins: { emoji: '🪙', label: 'Coins', color: '#fbbf24' },
  mystery: { emoji: '🎁', label: 'Mystery Prize', color: '#a78bfa' },
};

export default function MysteryBoxCeremony({ reward, onDismiss, play }) {
  const [phase, setPhase] = useState('idle');
  const [particles, setParticles] = useState([]);

  useEffect(() => {
    const shakeTimer = setTimeout(() => setPhase('shaking'), 100);
    const glowTimer = setTimeout(() => setPhase('glowing'), 900);
    const openTimer = setTimeout(() => {
      setPhase('opening');
      const newParticles = Array.from({ length: 20 }, (_, i) => ({
        id: i,
        x: 50 + (Math.random() - 0.5) * 20,
        y: 50 + (Math.random() - 0.5) * 20,
        vx: (Math.random() - 0.5) * 200,
        vy: -Math.random() * 200 - 50,
        color: ['#a78bfa', '#6366f1', '#34d399', '#f59e0b', '#f472b6'][Math.floor(Math.random() * 5)],
        size: Math.random() * 8 + 4,
        delay: Math.random() * 0.2,
      }));
      setParticles(newParticles);
    }, 1700);
    const revealTimer = setTimeout(() => setPhase('revealed'), 2500);

    return () => {
      clearTimeout(shakeTimer);
      clearTimeout(glowTimer);
      clearTimeout(openTimer);
      clearTimeout(revealTimer);
    };
  }, []);

  const rewardType = REWARD_TYPES[reward?.type] || REWARD_TYPES.mystery;

  return (
    <div className="fixed inset-0 z-[10000] flex items-center justify-center bg-black/60 backdrop-blur-sm"
         onClick={() => phase === 'revealed' && onDismiss()}>

      <div className="relative" style={{ width: 200, height: 200 }}>
        {(phase === 'glowing' || phase === 'opening') && (
          <div className="absolute inset-0 rounded-2xl"
            style={{
              background: `radial-gradient(circle at 50% 50%, ${rewardType.color}60 0%, transparent 70%)`,
              animation: 'mysteryGlow 0.5s ease-in-out infinite alternate',
            }}
          />
        )}

        <div
          className={`absolute inset-4 rounded-2xl flex items-center justify-center cursor-pointer
            ${phase === 'shaking' ? 'mystery-shake' : ''}
            ${phase === 'glowing' ? 'mystery-glow' : ''}
          `}
          style={{
            background: `linear-gradient(135deg, ${rewardType.color}30, ${rewardType.color}10)`,
            border: `2px solid ${rewardType.color}50`,
            boxShadow: phase === 'glowing' ? `0 0 60px ${rewardType.color}40` : 'none',
            transition: 'all 0.3s ease',
          }}
          onClick={() => phase === 'idle' && setPhase('shaking')}
        >
          <div className="absolute -top-1 left-0 right-0 h-1/2 rounded-t-2xl transition-transform duration-500"
            style={{
              background: `linear-gradient(135deg, ${rewardType.color}40, ${rewardType.color}20)`,
              borderBottom: `2px solid ${rewardType.color}30`,
              transform: phase === 'opening' || phase === 'revealed' ? 'translateY(-100%) rotateX(180deg)' : 'none',
              transformOrigin: 'bottom',
            }}
          />

          {phase === 'revealed' ? (
            <div className="text-center animate-bounce-in">
              <div className="text-6xl mb-2">{rewardType.emoji}</div>
              <div className="text-white font-bold text-lg" style={{ color: rewardType.color }}>
                {reward?.label || rewardType.label}
              </div>
              {reward?.amount && (
                <div className="text-2xl font-bold text-white mt-1">
                  +{reward.amount} {reward.type === 'xp' ? 'XP' : ''}
                </div>
              )}
            </div>
          ) : (
            <div className="text-5xl opacity-80">🎁</div>
          )}
        </div>

        {phase !== 'revealed' && (
          <div className="absolute -bottom-8 left-0 right-0 text-center text-sm text-gray-400 font-medium">
            {phase === 'idle' ? 'Tap to open!' : phase === 'shaking' ? 'Shaking...' : phase === 'glowing' ? 'Almost...' : ''}
          </div>
        )}

        {particles.map((p) => (
          <div
            key={p.id}
            className="absolute rounded-full"
            style={{
              width: p.size,
              height: p.size,
              backgroundColor: p.color,
              left: `${p.x}%`,
              top: `${p.y}%`,
              animation: `particleFly ${1 + p.delay}s ease-out forwards`,
              boxShadow: `0 0 6px ${p.color}`,
              '--tx': `${p.vx}px`,
              '--ty': `${p.vy}px`,
            } as React.CSSProperties}
          />
        ))}
      </div>
    </div>
  );
}
