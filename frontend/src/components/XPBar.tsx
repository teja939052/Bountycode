import { useEffect } from 'react';
import { motion } from 'framer-motion';
import CountUp from 'react-countup';

function xpForLevel(level: number): number {
  return ((level - 1) ** 2) * 50;
}

function xpForNextLevel(level: number): number {
  return (level ** 2) * 50;
}

function getLevelForXP(xp: number): number {
  if (xp <= 0) return 1;
  return Math.max(1, Math.min(100, Math.floor(Math.sqrt(xp / 50)) + 1));
}

function getLevelColor(level: number) {
  if (level >= 90) return { from: '#EC4899', to: '#A855F7', label: 'Mythic' };
  if (level >= 70) return { from: '#EAB308', to: '#F59E0B', label: 'Legendary' };
  if (level >= 50) return { from: '#A855F7', to: '#6366F1', label: 'Epic' };
  if (level >= 30) return { from: '#3B82F6', to: '#2563EB', label: 'Rare' };
  if (level >= 10) return { from: '#22C55E', to: '#16A34A', label: 'Uncommon' };
  return { from: '#9CA3AF', to: '#6B7280', label: 'Common' };
}

export { getLevelForXP, xpForLevel, xpForNextLevel, getLevelColor };

export default function XPBar({ xp = 0, showLevel = true, compact = false, className = '' }) {
  const level = getLevelForXP(xp);
  const currentLevelXP = xpForLevel(level);
  const nextLevelXP = xpForNextLevel(level);
  const progress = nextLevelXP > currentLevelXP
    ? ((xp - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100
    : 100;
  const color = getLevelColor(level);

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      {showLevel && (
        <div className="relative shrink-0">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center font-display font-black text-sm"
            style={{
              background: `linear-gradient(135deg, ${color.from}30, ${color.to}20)`,
              border: `2px solid ${color.from}50`,
              color: color.from,
              boxShadow: `0 0 12px ${color.from}20`,
            }}
          >
            {level}
          </div>
          <span
            className="absolute -bottom-1 -right-1 text-[8px] font-mono px-1 rounded"
            style={{ backgroundColor: `${color.from}20`, color: color.from }}
          >
            {color.label}
          </span>
        </div>
      )}

      <div className="flex-1 min-w-0">
        {compact ? (
          <div className="flex items-center gap-2">
            <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
              <motion.div
                className="h-full rounded-full"
                style={{ background: `linear-gradient(90deg, ${color.from}, ${color.to})` }}
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
              />
            </div>
            <span className="text-[10px] font-mono text-gray-500 shrink-0">
              <CountUp end={xp} duration={1.5} /> XP
            </span>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-1">
              <span className="text-[10px] font-mono text-gray-500">
                Level {level}
              </span>
              <span className="text-[10px] font-mono text-gray-600">
                <CountUp end={xp - currentLevelXP} duration={1.2} /> / {nextLevelXP - currentLevelXP} XP
              </span>
            </div>
            <div className="h-2.5 bg-gray-800 rounded-full overflow-hidden">
              <motion.div
                className="h-full rounded-full relative"
                style={{ background: `linear-gradient(90deg, ${color.from}, ${color.to})` }}
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
              >
                {/* Shine effect */}
                <div className="absolute inset-0 overflow-hidden rounded-full">
                  <div
                    className="absolute inset-0 holo-shimmer opacity-40"
                    style={{ animationDuration: '2s' }}
                  />
                </div>
              </motion.div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
