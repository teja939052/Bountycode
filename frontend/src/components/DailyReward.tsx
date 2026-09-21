import { useState, useRef } from 'react';
import { motion } from 'framer-motion';

const DAY_REWARDS = [
  { day: 1, reward: '10 Diamonds',      emoji: '⚡', claimed: false },
  { day: 2, reward: '25 Diamonds',      emoji: '⚡', claimed: false },
  { day: 3, reward: 'Streak 🔥',   emoji: '🧊', claimed: false },
  { day: 4, reward: '50 Diamonds',      emoji: '⚡', claimed: false },
  { day: 5, reward: '75 Diamonds',      emoji: '💎', claimed: false },
  { day: 6, reward: 'Double Diamonds',  emoji: '🔥', claimed: false },
  { day: 7, reward: 'Mystery 🎁', emoji: '🎁', claimed: false, special: true },
];

function Checkmark() {
  return (
    <svg className="w-4 h-4 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
    </svg>
  );
}

export default function DailyReward({ currentDay = 1, claimedDays = [], onClaim }) {
  const [justClaimed, setJustClaimed] = useState(null);
  const todayIndex = currentDay - 1;
  const todayClaimed = claimedDays.includes(currentDay);
  const confettiRef = useRef(null);

  const handleClaim = () => {
    if (todayClaimed || currentDay > 7) return;
    setJustClaimed(currentDay);
    onClaim?.(currentDay);

    // confetti burst
    if (confettiRef.current) {
      const colors = ['#22C55E', '#3B82F6', '#A855F7', '#EAB308', '#EC4899', '#F59E0B'];
      for (let i = 0; i < 40; i++) {
        const p = document.createElement('span');
        p.className = 'particle';
        p.style.background = colors[i % colors.length];
        p.style.left = `${45 + Math.random() * 10}%`;
        p.style.top = '50%';
        const angle = (i / 40) * Math.PI * 2;
        const dist = 60 + Math.random() * 80;
        p.style.setProperty('--tx', `${Math.cos(angle) * dist}px`);
        p.style.setProperty('--ty', `${Math.sin(angle) * dist - 40}px`);
        p.style.width = `${5 + Math.random() * 5}px`;
        p.style.height = p.style.width;
        p.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
        confettiRef.current.appendChild(p);
        setTimeout(() => p.remove(), 1100);
      }
    }
  };

  return (
    <div className="relative space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">
            Daily Login Rewards
          </h3>
          <p className="text-[10px] text-gray-400 mt-0.5">
            Day {Math.min(currentDay, 7)} of 7 — claim daily to earn bigger rewards
          </p>
        </div>
        <div className="flex items-center gap-1 text-xs font-mono text-gray-400">
          <span>🔥</span>
          <span>{claimedDays.length}/7</span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="relative h-1.5 bg-white/10 rounded-full overflow-hidden">
        <motion.div
          className="absolute inset-y-0 left-0 rounded-full"
          style={{
            background: 'linear-gradient(90deg, #34d399, #60a5fa, #a78bfa)',
          }}
          initial={{ width: 0 }}
          animate={{ width: `${(claimedDays.length / 7) * 100}%` }}
          transition={{ duration: 0.6, ease: 'easeOut' }}
        />
      </div>

      {/* Day cards */}
      <div className="grid grid-cols-4 sm:grid-cols-7 gap-2">
        {DAY_REWARDS.map((day, i) => {
          const isClaimed = claimedDays.includes(day.day);
          const isToday = day.day === currentDay;
          const isFuture = day.day > currentDay;
          const wasJustClaimed = justClaimed === day.day;

          return (
            <motion.div
              key={day.day}
              initial={{ opacity: 0, scale: 0.8, y: 12 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              transition={{ delay: i * 0.06, duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
              className={`
                relative flex flex-col items-center gap-1 p-2 rounded-xl border transition-all duration-300
                ${isClaimed
                  ? 'gamification-card border-emerald-500/30'
                  : isToday
                  ? 'gamification-card border-indigo-500/50 shadow-lg shadow-indigo-500/20'
                  : 'bg-white/5 border-white/10'
                }
                ${day.special && isToday ? 'border-purple-500/50 shadow-lg shadow-purple-500/20' : ''}
              `}
            >
              {/* Day number */}
              <span className="text-[8px] sm:text-[9px] font-mono text-gray-500 uppercase tracking-wider">
                D{day.day}
              </span>

              {/* Emoji */}
              <motion.div
                className={`text-lg sm:text-2xl ${isToday && !isClaimed ? 'animate-bounce' : ''}`}
                animate={wasJustClaimed ? { scale: [1, 1.4, 1], rotate: [0, 10, -10, 0] } : {}}
                transition={{ duration: 0.5 }}
              >
                {isClaimed ? (
                  <div className="w-5 h-5 sm:w-6 sm:h-6 rounded-full bg-emerald-500/20 flex items-center justify-center">
                    <Checkmark />
                  </div>
                ) : (
                  <span className={isFuture ? 'opacity-30 grayscale' : ''}>
                    {day.emoji}
                  </span>
                )}
              </motion.div>

              {/* Reward text */}
              <span
                className={`text-[8px] sm:text-[9px] font-mono leading-tight text-center ${
                  isClaimed
                    ? 'text-emerald-400/80'
                    : isToday
                    ? 'text-indigo-300 font-bold'
                    : 'text-gray-500'
                }`}
              >
                {day.reward}
              </span>

              {/* Today indicator */}
              {isToday && !isClaimed && (
                <motion.div
                  className="absolute -top-1 -right-1 w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-indigo-400"
                  animate={{ scale: [1, 1.3, 1], opacity: [1, 0.7, 1] }}
                  transition={{ repeat: Infinity, duration: 1.5 }}
                />
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Claim button */}
      {!todayClaimed && currentDay <= 7 && (
        <motion.button
          onClick={handleClaim}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="
            mt-4 w-full py-2.5 rounded-xl font-bold text-sm uppercase tracking-wider
            glass-button text-white
            hover:shadow-lg hover:shadow-indigo-500/25 transition-all duration-300
          "
        >
          Claim Day {currentDay} Reward
        </motion.button>
      )}

      {todayClaimed && (
        <div className="mt-4 text-center text-xs font-mono text-emerald-400/80 py-2">
          ✓ Today&apos;s reward claimed — come back tomorrow!
        </div>
      )}
    </div>
  );
}
