import { useEffect, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface CelebrationProps {
  show: boolean;
  diamonds?: number;
  onComplete?: () => void;
}

/**
 * Celebration overlay — confetti + Diamonds burst + mastery message.
 *
 * Uses Framer Motion for smooth physics-based confetti.
 * Respects prefers-reduced-motion (Framer Motion handles automatically).
 */
export function Celebration({ show, diamonds = 50, onComplete }: CelebrationProps) {
  const [visible, setVisible] = useState(false);

  const handleComplete = useCallback(() => {
    setVisible(false);
    onComplete?.();
  }, [onComplete]);

  useEffect(() => {
    if (show) {
      setVisible(true);
      const timer = setTimeout(handleComplete, 3000);
      return () => clearTimeout(timer);
    }
  }, [show, handleComplete]);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-[60] pointer-events-none flex items-center justify-center"
          aria-live="polite"
          aria-label={`Mastered! +${diamonds} Diamonds`}
        >
          {/* Confetti */}
          <div className="absolute inset-0 overflow-hidden">
            {Array.from({ length: 30 }).map((_, i) => (
              <motion.div
                key={i}
                initial={{
                  y: -20,
                  x: typeof window !== "undefined" ? Math.random() * window.innerWidth : 0,
                  opacity: 1,
                  scale: 0.5 + Math.random() * 0.5,
                }}
                animate={{
                  y: typeof window !== "undefined" ? window.innerHeight + 20 : 800,
                  opacity: 0,
                  rotate: Math.random() * 720 - 360,
                }}
                transition={{
                  duration: 2 + Math.random(),
                  ease: "easeOut",
                  delay: Math.random() * 0.3,
                }}
                className="absolute w-2.5 h-2.5 rounded-sm"
                style={{
                  backgroundColor: ["#22C55E", "#EAB74D", "#3B82F6", "#EC4899", "#8B5CF6", "#F97316"][i % 6],
                  left: `${(i * 3.33) % 100}%`,
                }}
              />
            ))}
          </div>

          {/* Diamonds burst card */}
          <motion.div
            initial={{ scale: 0.3, opacity: 0, y: 20 }}
            animate={{ scale: 1, opacity: 1, y: 0 }}
            exit={{ scale: 0.8, opacity: 0, y: -20 }}
            transition={{ type: "spring", damping: 12, stiffness: 200 }}
            className="bg-white rounded-3xl shadow-2xl px-10 py-8 text-center border border-primary/10"
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="text-5xl mb-3"
            >
              🎉
            </motion.div>
            <motion.h3
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.3 }}
              className="text-xl font-bold text-text-primary"
            >
              Level Mastered!
            </motion.h3>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.5, type: "spring" }}
              className="mt-2 text-yellow-600 font-bold text-lg"
            >
              +{diamonds} Diamonds
            </motion.div>
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
              className="text-xs text-text-muted mt-2"
            >
              Your character moves forward!
            </motion.p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
