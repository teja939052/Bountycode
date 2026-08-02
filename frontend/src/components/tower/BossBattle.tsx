import { motion } from 'framer-motion';

// Boss encounter overlay — shows boss name, emoji, and fight button
export default function BossBattle({ boss, level, onFight, onSkip, canSkip = false }) {
  if (!boss) return null;

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      className="bg-gradient-to-b from-yellow-500/10 to-gray-900/60 border-2 border-yellow-500/40 rounded-2xl p-6 text-center"
    >
      {/* Boss emoji */}
      <motion.div
        className="text-6xl mb-3"
        animate={{ y: [0, -8, 0], rotate: [0, -3, 3, 0] }}
        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
      >
        {boss.emoji}
      </motion.div>

      {/* Boss name */}
      <h3 className="text-lg font-display font-black text-yellow-400 mb-1">
        {boss.name}
      </h3>
      <p className="text-xs font-mono text-gray-400 mb-1">
        Level {level} Boss Battle
      </p>
      <p className="text-[10px] font-mono text-gray-500 mb-4">
        Score {boss.required_score}%+ to defeat
      </p>

      {/* HP bar (visual only) */}
      <div className="mb-4">
        <div className="flex justify-between text-[9px] font-mono text-gray-500 mb-0.5">
          <span>BOSS HP</span>
          <span>100/100</span>
        </div>
        <div className="h-2 rounded bg-gray-700/40 overflow-hidden">
          <div className="h-full rounded bg-gradient-to-r from-red-500 to-yellow-500" style={{ width: '100%' }} />
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-3 justify-center">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onFight}
          className="px-6 py-2.5 rounded-xl bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-display font-bold text-sm uppercase tracking-wider hover:shadow-lg hover:shadow-yellow-500/20 transition-shadow"
        >
          ⚔️ Fight Boss
        </motion.button>
        {canSkip && (
          <button
            onClick={onSkip}
            className="px-4 py-2.5 rounded-xl border border-gray-600/40 text-gray-400 text-xs font-mono hover:border-gray-500 transition-colors"
          >
            🛡️ Skip
          </button>
        )}
      </div>
    </motion.div>
  );
}
