import { useState, useRef, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import gsap from 'gsap';

const REWARD_POOL = [
  { type: 'xp', amount: 25, label: '+25 XP', rarity: 'common', emoji: '⚡', color: '#9CA3AF' },
  { type: 'xp', amount: 50, label: '+50 XP', rarity: 'uncommon', emoji: '⚡', color: '#22C55E' },
  { type: 'xp', amount: 100, label: '+100 XP', rarity: 'rare', emoji: '⚡', color: '#3B82F6' },
  { type: 'xp', amount: 250, label: '+250 XP', rarity: 'epic', emoji: '⚡', color: '#A855F7' },
  { type: 'streak_freeze', amount: 1, label: 'Streak Freeze', rarity: 'rare', emoji: '🧊', color: '#3B82F6' },
  { type: 'streak_freeze', amount: 2, label: '2× Streak Freeze', rarity: 'epic', emoji: '🧊', color: '#A855F7' },
  { type: 'double_xp', amount: 1, label: 'Double XP (1 hr)', rarity: 'epic', emoji: '🔥', color: '#A855F7' },
  { type: 'badge_hint', amount: 1, label: 'Badge Hint', rarity: 'uncommon', emoji: '💡', color: '#22C55E' },
  { type: 'pro_trial', amount: 1, label: 'Pro 1-Day Trial', rarity: 'legendary', emoji: '👑', color: '#EAB308' },
  { type: 'mystery_multiplier', amount: 2, label: '2× Next Reward', rarity: 'legendary', emoji: '🎰', color: '#EAB308' },
];

const RARITY_WEIGHTS = {
  common: 35,
  uncommon: 28,
  rare: 20,
  epic: 12,
  legendary: 4,
  mythic: 1,
};

function weightedRandom() {
  const total = Object.values(RARITY_WEIGHTS).reduce((a, b) => a + b, 0);
  let r = Math.random() * total;
  for (const [rarity, weight] of Object.entries(RARITY_WEIGHTS)) {
    r -= weight;
    if (r <= 0) return rarity;
  }
  return 'common';
}

function rollReward() {
  const rarity = weightedRandom();
  const pool = REWARD_POOL.filter((r) => r.rarity === rarity);
  if (pool.length === 0) {
    const fallback = REWARD_POOL.filter((r) => r.rarity === 'common');
    return fallback[Math.floor(Math.random() * fallback.length)];
  }
  return pool[Math.floor(Math.random() * pool.length)];
}

function spawnBurst(container, color, count = 20) {
  for (let i = 0; i < count; i++) {
    const p = document.createElement('span');
    p.className = 'particle';
    p.style.background = color;
    p.style.left = '50%';
    p.style.top = '50%';
    const angle = (i / count) * Math.PI * 2;
    const dist = 40 + Math.random() * 60;
    p.style.setProperty('--tx', `${Math.cos(angle) * dist}px`);
    p.style.setProperty('--ty', `${Math.sin(angle) * dist}px`);
    p.style.width = `${4 + Math.random() * 5}px`;
    p.style.height = p.style.width;
    p.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
    container.appendChild(p);
    setTimeout(() => p.remove(), 1000);
  }
}

export default function MysteryBox({ onReward, canOpen = true, size = 'md' }) {
  const [state, setState] = useState('idle'); // idle | shaking | opening | revealed
  const [reward, setReward] = useState(null);
  const boxRef = useRef(null);

  const sizeMap = {
    sm: 'w-20 h-24 text-3xl',
    md: 'w-28 h-32 text-5xl',
    lg: 'w-36 h-40 text-6xl',
  };

  const handleOpen = useCallback(() => {
    if (state !== 'idle' || !canOpen) return;

    setState('shaking');

    setTimeout(() => {
      const rolled = rollReward();
      setReward(rolled);
      setState('opening');

      setTimeout(() => {
        setState('revealed');
        if (boxRef.current) {
          spawnBurst(boxRef.current, rolled.color, rolled.rarity === 'legendary' || rolled.rarity === 'mythic' ? 30 : 16);
        }
        onReward?.(rolled);
      }, 800);
    }, 1200);
  }, [state, canOpen, onReward]);

  const handleReset = useCallback(() => {
    setState('idle');
    setReward(null);
  }, []);

  return (
    <div className="relative inline-flex flex-col items-center gap-3">
      {/* Box */}
      <motion.div
        ref={boxRef}
        className={`
          relative ${sizeMap[size]} rounded-2xl cursor-pointer
          flex items-center justify-center
          border-2 border-purple-500/50
          ${state === 'idle' ? 'mystery-glow' : ''}
          ${state === 'shaking' ? 'mystery-shake' : ''}
          ${state === 'idle' && canOpen ? 'hover:border-purple-400' : ''}
        `}
        style={{
          background:
            state === 'revealed'
              ? 'linear-gradient(135deg, rgba(168,85,247,0.2), rgba(236,72,153,0.2))'
              : 'linear-gradient(135deg, rgba(88,28,135,0.4), rgba(147,51,234,0.3))',
        }}
        onClick={handleOpen}
        whileHover={state === 'idle' && canOpen ? { scale: 1.05, rotate: [-1, 1, -1, 0] } : {}}
        whileTap={state === 'idle' && canOpen ? { scale: 0.95 } : {}}
      >
        {/* Idle: Box icon */}
        <AnimatePresence mode="wait">
          {state === 'idle' && (
            <motion.div
              key="idle"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              exit={{ scale: 0, rotate: 180 }}
              className="select-none"
            >
              🎁
            </motion.div>
          )}
          {state === 'shaking' && (
            <motion.div
              key="shaking"
              initial={{ scale: 0.8 }}
              animate={{ scale: [0.8, 1.1, 0.9, 1.05, 1] }}
              className="select-none text-5xl"
            >
              ❓
            </motion.div>
          )}
          {state === 'opening' && (
            <motion.div
              key="opening"
              initial={{ scale: 0.5, rotate: -180 }}
              animate={{ scale: 1.5, rotate: 0, opacity: [1, 0] }}
              transition={{ duration: 0.6, ease: 'easeOut' }}
              className="select-none"
            >
              ✨
            </motion.div>
          )}
          {state === 'revealed' && reward && (
            <motion.div
              key="revealed"
              initial={{ scale: 0, rotate: -90 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: 'spring', stiffness: 400, damping: 15 }}
              className="select-none text-center"
            >
              <div className="text-4xl">{reward.emoji}</div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Shine overlay on idle */}
        {state === 'idle' && (
          <div className="absolute inset-0 rounded-2xl overflow-hidden pointer-events-none">
            <div className="absolute inset-0 holo-shimmer" />
          </div>
        )}
      </motion.div>

      {/* Label */}
      <AnimatePresence mode="wait">
        {state === 'idle' && (
          <motion.p
            key="idle-label"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="text-xs font-mono text-purple-400 uppercase tracking-wider"
          >
            {canOpen ? 'Tap to open' : 'Earned today'}
          </motion.p>
        )}
        {state === 'shaking' && (
          <motion.p
            key="shaking-label"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0.5, 1] }}
            className="text-xs font-mono text-purple-300 uppercase tracking-wider"
          >
            Unboxing...
          </motion.p>
        )}
        {state === 'revealed' && reward && (
          <motion.div
            key="revealed-label"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center"
          >
            <p
              className="text-sm font-display font-bold"
              style={{ color: reward.color }}
            >
              {reward.label}
            </p>
            <p
              className="text-[10px] font-mono uppercase tracking-widest mt-0.5"
              style={{ color: `${reward.color}99` }}
            >
              {reward.rarity}
            </p>
            <button
              onClick={handleReset}
              className="mt-2 text-[10px] font-mono text-gray-500 hover:text-gray-300 transition-colors"
            >
              close
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
