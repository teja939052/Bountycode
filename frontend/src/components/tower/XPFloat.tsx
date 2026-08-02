import { motion, AnimatePresence } from 'framer-motion';

// Floating XP animation — shows XP gain after solving
export default function XPFloat({ amount, visible, onComplete }) {
  return (
    <AnimatePresence>
      {visible && amount > 0 && (
        <motion.div
          initial={{ y: 0, opacity: 1, scale: 0.8 }}
          animate={{ y: -80, opacity: 0, scale: 1.2 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 1.5, ease: 'easeOut' }}
          onAnimationComplete={onComplete}
          className="fixed top-1/2 left-1/2 -translate-x-1/2 z-50 pointer-events-none"
        >
          <span className="text-3xl font-display font-black text-green-400 drop-shadow-lg">
            +{amount} XP
          </span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
