import { motion } from 'framer-motion';
import CountUp from 'react-countup';

function xpForLevel(level: number): number {
  return ((level - 1) ** 2) * 50;
}

function xpForNextLevel(level: number): number {
  return (level ** 2) * 50;
}

function getLevelForXP(diamonds: number): number {
  if (diamonds <= 0) return 1;
  return Math.max(1, Math.min(100, Math.floor(Math.sqrt(diamonds / 50)) + 1));
}

function getLevelColor(level: number) {
  if (level >= 90) return { from: '#EC4899', to: '#A855F7', label: 'Mythic', glow: 'rgba(236,72,153,0.35)' };
  if (level >= 70) return { from: '#EAB308', to: '#F59E0B', label: 'Legendary', glow: 'rgba(234,179,8,0.35)' };
  if (level >= 50) return { from: '#A855F7', to: '#6366F1', label: 'Epic', glow: 'rgba(168,85,247,0.35)' };
  if (level >= 30) return { from: '#3B82F6', to: '#2563EB', label: 'Rare', glow: 'rgba(59,130,246,0.35)' };
  if (level >= 10) return { from: '#22C55E', to: '#16A34A', label: 'Uncommon', glow: 'rgba(34,197,94,0.35)' };
  return { from: '#9CA3AF', to: '#6B7280', label: 'Common', glow: 'rgba(156,163,175,0.25)' };
}

export { getLevelForXP, xpForLevel, xpForNextLevel, getLevelColor };

type DiamondsBarProps = {
  diamonds?: number;
  /** Backend-owned level. When provided, the bar renders it directly —
   * the client must never recompute level from Diamonds (single source of
   * truth lives in record_practice). Falls back to the legacy curve only
   * for callers without profile data. */
  level?: number;
  /** Diamonds counted inside the current level + Diamonds needed to finish it.
   * When provided with `level`, progress renders from backend numbers. */
  xpIntoLevel?: number;
  xpForNext?: number;
  showLevel?: boolean;
  compact?: boolean;
  variant?: 'bar' | 'ring';
  className?: string;
  color?: { from: string; to: string; label: string; glow: string };
};

export default function DiamondsBar({ diamonds = 0, level: levelProp, xpIntoLevel, xpForNext, showLevel = true, compact = false, variant = 'bar', className = '', color: colorProp }: DiamondsBarProps) {
  const level = levelProp ?? 1;
  const currentLevelXP = xpForLevel(level);
  const nextLevelXP = xpForNextLevel(level);
  const into = xpIntoLevel ?? (diamonds - currentLevelXP);
  const span = xpForNext ?? (nextLevelXP - currentLevelXP);
  const progress = span > 0 ? (into / span) * 100 : 100;
  const color = colorProp || getLevelColor(level);

  if (variant === 'ring') {
    const radius = 38;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (progress / 100) * circumference;
    return (
      <div className={`relative inline-flex items-center justify-center ${className}`}>
        <svg width="96" height="96" viewBox="0 0 96 96" className="drop-shadow-lg">
          <circle cx="48" cy="48" r={radius} fill="none" stroke="currentColor" strokeWidth="6" className="text-gray-200 dark:text-gray-800" />
          <motion.circle
            cx="48" cy="48" r={radius}
            fill="none"
            stroke={color.from}
            strokeWidth="6"
            strokeLinecap="round"
            className="progress-ring-circle"
            strokeDasharray={circumference}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.1, ease: 'easeOut' }}
            style={{ filter: `drop-shadow(0 0 8px ${color.glow})` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          {showLevel && (
            <span className="text-2xl font-black font-display" style={{ color: color.from }}>{level}</span>
          )}
          <span className="text-[9px] font-mono text-gray-500 uppercase tracking-wider">{color.label}</span>
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      {showLevel && (
        <div className="relative shrink-0">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center font-display font-black text-sm diamonds-orb"
            style={{
              background: `linear-gradient(135deg, ${color.from}30, ${color.to}20)`,
              border: `2px solid ${color.from}50`,
              color: color.from,
              boxShadow: `0 0 18px ${color.glow}`,
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
            <div className="relative h-2 bg-gray-800 rounded-full overflow-hidden flex-1">
              <div className="absolute inset-0 bg-gradient-to-r from-ocean/10 to-ocean/5" />
              <motion.div
                className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-ocean to-sky"
                style={{ width: `${progress}%` }}
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
              >
                <div className="absolute inset-y-0 right-0 w-6 bg-gradient-to-r from-transparent to-white/30" />
              </motion.div>
            </div>
            <span className="text-[10px] font-mono text-gray-500 shrink-0">
              <CountUp end={diamonds} duration={1.5} /> Diamonds
            </span>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-1">
              <span className="text-[10px] font-mono text-gray-500">Level {level}</span>
              <span className="text-[10px] font-mono text-gray-600">
                <CountUp end={into} duration={1.2} /> / {span} Diamonds
              </span>
            </div>
            <div className="relative h-2.5 bg-gray-800 rounded-full overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-ocean/10 to-ocean/5" />
              {[25, 50, 75].map((mark) => (
                <div key={mark} className="absolute inset-y-0 w-px bg-white/10" style={{ left: `${mark}%` }} />
              ))}
              <motion.div
                className="absolute inset-y-0 left-0 rounded-full bg-gradient-to-r from-ocean to-sky"
                style={{ width: `${progress}%` }}
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
              >
                <div className="absolute inset-0 overflow-hidden rounded-full">
                  <div className="absolute inset-y-0 right-0 w-8 bg-gradient-to-r from-transparent to-white/30" />
                  <div className="absolute inset-0 holo-shimmer opacity-50" style={{ animationDuration: '2s' }} />
                </div>
              </motion.div>
            </div>
            <div className="mt-1 text-[10px] font-mono text-gray-500">
              {Math.max(0, Math.round(span - into))} Diamonds to Level {level + 1}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
