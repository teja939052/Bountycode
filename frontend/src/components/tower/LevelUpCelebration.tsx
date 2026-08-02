import { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { getTitleForLevel } from './towerData';

// Full-screen level up celebration — GoT/BB style
export default function LevelUpCelebration({ oldLevel, newLevel, visible, onClose }) {
  const [, emoji] = getTitleForLevel(newLevel);

  useEffect(() => {
    if (!visible) return;
    const timer = setTimeout(() => onClose?.(), 4000);
    return () => clearTimeout(timer);
  }, [visible, onClose]);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[90] flex items-center justify-center bg-black/80 backdrop-blur-sm"
          onClick={onClose}
        >
          {/* Burst particles */}
          <div className="absolute inset-0 overflow-hidden pointer-events-none">
            {Array.from({ length: 30 }).map((_, i) => (
              <motion.div
                key={i}
                className="absolute w-1 h-1 rounded-full"
                style={{ background: ['#4CC9F0', '#7209B7', '#22c55e', '#F59E0B', '#ec4899'][i % 5] }}
                initial={{
                  x: '50vw', y: '50vh', opacity: 0, scale: 0,
                }}
                animate={{
                  x: `${50 + (Math.random() - 0.5) * 80}vw`,
                  y: `${50 + (Math.random() - 0.5) * 80}vh`,
                  opacity: [0, 1, 0],
                  scale: [0, 2, 0],
                }}
                transition={{
                  duration: 1.5 + Math.random(),
                  delay: Math.random() * 0.5,
                  ease: 'easeOut',
                }}
              />
            ))}
          </div>

          <motion.div
            initial={{ scale: 0.3, opacity: 0, rotate: -10 }}
            animate={{ scale: 1, opacity: 1, rotate: 0 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ duration: 0.6, ease: [0.34, 1.56, 0.64, 1] }}
            onClick={(e) => e.stopPropagation()}
            className="relative text-center px-8"
          >
            {/* Emoji */}
            <motion.div
              className="text-7xl mb-4"
              animate={{ y: [0, -10, 0], scale: [1, 1.1, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {emoji}
            </motion.div>

            {/* Level Up text */}
            <motion.h2
              className="text-3xl sm:text-4xl font-display font-black text-white mb-2"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              LEVEL UP!
            </motion.h2>

            <motion.div
              className="flex items-center justify-center gap-3 mb-4"
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <span className="text-lg font-mono text-gray-400">{oldLevel}</span>
              <span className="text-cyber-blue text-xl">→</span>
              <span className="text-2xl font-display font-black text-cyber-blue">{newLevel}</span>
            </motion.div>

            <motion.p
              className="text-sm font-mono text-gray-400"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.8 }}
            >
              Tap anywhere to continue
            </motion.p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
