import { useEffect } from 'react';
import { motion } from 'framer-motion';
import CountUp from 'react-countup';
import { Zap, Flame, Trophy } from 'lucide-react';
import { getLevelForXP, getXPForLevel, getLevelLabel, CODDY } from './gamification/palette';

const LEVEL_THRESHOLDS = [
  0, 100, 300, 600, 1000, 1600, 2400, 3400, 4600, 6000,
  7800, 10000, 12600, 15600, 19200, 23400, 28200, 33800, 40200, 47600,
];

export { getLevelForXP, getXPForLevel };

export default function XPBar({ xp = 0, showLevel = true, compact = false, className = '', streak = 0, league }) {
  const level = getLevelForXP(xp);
  const currentLevelXP = getXPForLevel(level);
  const nextLevelXP = getXPForLevel(level + 1);
  const progress = nextLevelXP > currentLevelXP
    ? Math.min(100, Math.max(0, ((xp - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100))
    : 100;
  const label = getLevelLabel(level);
  const color = CODDY[label.color];

  return (
    <div className={`flex items-center gap-3 min-w-0 ${className}`}>
      {showLevel && (
        <div className="shrink-0 relative">
          <div
            className="w-10 h-10 rounded-xl flex items-center justify-center font-display font-bold text-sm shadow-lg"
            style={{
              background: `linear-gradient(135deg, ${color.light}40, ${CODDY.blue.light}20)`,
              border: `2px solid ${color.base}80`,
              color: color.base,
              boxShadow: `0 0 16px ${color.base}40`,
            }}
          >
            {level}
          </div>
          <span
            className="absolute -bottom-[14px] -right-px text-[9px] font-mono font-bold px-2 py-[2px] rounded-md"
            style={{ backgroundColor: `${color.base}15`, color: color.base, border: `1px solid ${color.base}40` }}
          >
            {label.label}
          </span>
        </div>
      )}

      <div className="flex-1 min-w-0">
        {compact ? (
          <div className="flex items-center gap-2.5">
            <div className="flex-1 h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden border border-white/30 dark:border-white/10">
              <motion.div
                className="h-full rounded-full relative"
                style={{ background: `linear-gradient(90deg, ${color.base}, ${CODDY.blue.base})` }}
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
              >
                <div className="absolute inset-0 overflow-hidden rounded-full">
                  <div className="absolute inset-0 holo-shimmer opacity-50" style={{ animationDuration: '2s' }} />
                </div>
              </motion.div>
            </div>
            <span className="text-[10px] font-mono font-bold text-ink dark:text-slate-300 shrink-0">
              <CountUp end={xp} duration={1.5} /> XP
            </span>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-2 gap-2">
              <div className="flex items-center gap-1">
                <Zap size={13} className="text-warning-500 dark:text-warning-400" />
                <span className="text-[11px] font-mono font-bold text-ink dark:text-slate-300">
                  <CountUp end={xp - currentLevelXP} duration={1.2} /> <span className="text-[10px] opacity-70">/{nextLevelXP - currentLevelXP}</span> XP
                </span>
              </div>
              {league && (
                <span className="flex items-center gap-1.5 px-2.5 py-[3px] rounded-full bg-ink dark:bg-slate-800 border border-white/20 text-[10px] font-bold text-white">
                  <Trophy size={11} className="text-warning-500" />
                  #{league}
                </span>
              )}
            </div>
            <div className="h-3 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden border border-white/30 dark:border-white/10">
              <motion.div
                className="h-full rounded-full relative"
                style={{ background: `linear-gradient(90deg, ${color.base}, ${CODDY.blue.base})` }}
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 1.2, ease: 'easeOut' }}
              >
                <div className="absolute inset-0 overflow-hidden rounded-full">
                  <div className="absolute inset-0 holo-shimmer opacity-50" style={{ animationDuration: '2s' }} />
                </div>
              </motion.div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
