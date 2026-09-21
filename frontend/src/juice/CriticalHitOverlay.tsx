import { motion, AnimatePresence } from 'framer-motion';
import useReducedMotion from "../hooks/useReducedMotion";

export default function CriticalHitOverlay({ visible = true, text = 'CRITICAL HIT!', subtext = '+50% Bonus Diamonds' }) {
  const reduced = useReducedMotion();
  if (!visible) return null;

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none"
          initial={reduced ? { opacity: 1 } : { opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 1.5 }}
          transition={{ type: 'spring', stiffness: 300, damping: 15 }}
        >
          <div className="text-center">
            <motion.div
              className="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-300 via-orange-400 to-red-500"
              style={{
                textShadow: '0 0 60px rgba(245,158,11,0.8)',
                filter: 'drop-shadow(0 0 20px rgba(239,68,68,0.6))',
              }}
              animate={reduced ? {} : { scale: [1, 1.1, 1], rotate: [0, -2, 2, 0] }}
              transition={{ duration: 0.3, repeat: 3 }}
            >
              {text}
            </motion.div>
            {subtext && (
              <motion.div
                className="text-2xl md:text-3xl font-bold text-yellow-300 mt-2"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                {subtext}
              </motion.div>
            )}
            <motion.div
              className="text-6xl mt-4"
              animate={reduced ? {} : { scale: [0, 1.5, 1], rotate: [0, 360] }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              ⚡
            </motion.div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
