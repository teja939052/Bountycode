import { motion } from 'framer-motion';

// Visual tower grid showing level progression with XP bar
// Candy Crush-style level map

const FLOOR_SIZE = 10; // levels per floor

export default function TowerProgress({ level = 1, xp = 0, xpToNext = 100, xpForCurrent = 0, title = 'Hatchling', titleEmoji = '🐣' }) {
  const progress = xpToNext > 0 ? ((xp - xpForCurrent) / (xpToNext - xpForCurrent)) * 100 : 0;
  const currentFloor = Math.floor((level - 1) / FLOOR_SIZE);
  const startLevel = currentFloor * FLOOR_SIZE + 1;

  return (
    <div className="bg-gray-900/60 border border-gray-700/30 rounded-2xl p-4 sm:p-6">
      {/* Header */}
      <div className="text-center mb-4">
        <div className="flex items-center justify-center gap-2 mb-1">
          <span className="text-2xl">{titleEmoji}</span>
          <h2 className="text-lg sm:text-xl font-display font-black text-white">
            Level {level}
          </h2>
        </div>
        <p className="text-xs font-mono text-gray-400">{title}</p>
      </div>

      {/* XP Bar */}
      <div className="mb-5">
        <div className="flex justify-between text-[10px] font-mono text-gray-500 mb-1">
          <span>{xp} XP</span>
          <span>{xpToNext} XP</span>
        </div>
        <div className="h-3 rounded-full bg-gray-700/40 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${Math.min(progress, 100)}%` }}
            transition={{ duration: 1.2, ease: 'easeOut' }}
            className="h-full rounded-full bg-gradient-to-r from-cyber-purple via-cyber-blue to-cyan-400"
          />
        </div>
        <p className="text-center text-[10px] font-mono text-gray-500 mt-1">
          {xpToNext - xp} XP to next level
        </p>
      </div>

      {/* Floor Grid */}
      <div className="grid grid-cols-5 sm:grid-cols-10 gap-1.5">
        {Array.from({ length: FLOOR_SIZE }, (_, i) => {
          const lvl = startLevel + i;
          const isCurrent = lvl === level;
          const isCompleted = lvl < level;
          const isBoss = lvl % 10 === 0;
          const isLocked = lvl > level + 5;

          return (
            <motion.div
              key={lvl}
              initial={{ scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: i * 0.04, duration: 0.3 }}
              className={`relative aspect-square rounded-lg flex items-center justify-center text-[9px] sm:text-[10px] font-mono font-bold border transition-all ${
                isCurrent
                  ? 'bg-cyber-blue/20 border-cyber-blue/60 text-cyber-blue shadow-cyber-blue scale-110'
                  : isBoss
                    ? isCompleted
                      ? 'bg-yellow-500/20 border-yellow-500/40 text-yellow-400'
                      : 'bg-gray-800/60 border-yellow-500/20 text-yellow-500/40'
                    : isCompleted
                      ? 'bg-cyber-purple/15 border-cyber-purple/30 text-cyber-purple'
                      : isLocked
                        ? 'bg-gray-800/30 border-gray-700/20 text-gray-600'
                        : 'bg-gray-800/40 border-gray-700/30 text-gray-500'
              }`}
            >
              {isBoss && isCompleted ? '👑' : isBoss ? '⚡' : lvl}
              {isCurrent && (
                <motion.div
                  className="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full bg-cyber-blue"
                  animate={{ scale: [1, 1.3, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                />
              )}
            </motion.div>
          );
        })}
      </div>

      {/* Floor Label */}
      <div className="text-center mt-3">
        <span className="text-[9px] font-mono text-gray-600">
          Floor {currentFloor + 1} — Levels {startLevel}–{startLevel + FLOOR_SIZE - 1}
        </span>
      </div>
    </div>
  );
}
