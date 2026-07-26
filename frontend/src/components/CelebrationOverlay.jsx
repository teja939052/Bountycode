import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";

const CONFETTI_COLORS = ["#6366f1", "#f59e0b", "#10b981", "#ef4444", "#ec4899", "#8b5cf6"];

function ConfettiPiece({ index, reduced }) {
  const color = CONFETTI_COLORS[index % CONFETTI_COLORS.length];
  const x = Math.random() * 400 - 200;
  const rotate = Math.random() * 720 - 360;
  const delay = Math.random() * 0.3;

  return (
    <motion.div
      className="absolute left-1/2 top-1/2 w-3 h-3 rounded-sm"
      style={{ backgroundColor: color }}
      initial={reduced ? { opacity: 1, scale: 1 } : { opacity: 1, scale: 1, x: 0, y: 0, rotate: 0 }}
      animate={
        reduced
          ? { opacity: 0 }
          : {
              x,
              y: [0, -100 - Math.random() * 200, 300],
              rotate,
              opacity: [1, 1, 0],
              scale: [1, 1.2, 0.5],
            }
      }
      transition={{ duration: 1.5, delay, ease: "easeOut" }}
    />
  );
}

export default function CelebrationOverlay({ show, type = "confetti", message = "", onClose }) {
  const reduced = useReducedMotion();
  const [visible, setVisible] = useState(show);

  useEffect(() => {
    setVisible(show);
    if (show && type !== "persistent") {
      const timer = setTimeout(() => {
        setVisible(false);
        onClose?.();
      }, 2500);
      return () => clearTimeout(timer);
    }
  }, [show, type, onClose]);

  const emojis = {
    badge: "🏆",
    streak: "🔥",
    levelup: "⬆️",
    confetti: "🎉",
    perfect: "💯",
  };

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center pointer-events-none"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <div className="relative">
            {!reduced && Array.from({ length: 30 }).map((_, i) => (
              <ConfettiPiece key={i} index={i} reduced={reduced} />
            ))}
            <motion.div
              className="text-6xl md:text-8xl"
              initial={reduced ? {} : { scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 260, damping: 20 }}
            >
              {emojis[type] || emojis.confetti}
            </motion.div>
            {message && (
              <motion.p
                className="text-center text-xl font-bold text-white mt-4 drop-shadow-lg"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
              >
                {message}
              </motion.p>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
