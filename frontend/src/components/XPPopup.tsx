import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import { Zap, Flame, Trophy, ArrowUp } from "lucide-react";

export default function XPPopup({ show, xpGained, level, streak, newBadges = [], onClose }) {
  const reduced = useReducedMotion();
  const [visible, setVisible] = useState(show);

  useEffect(() => {
    setVisible(show);
    if (show) {
      const timer = setTimeout(() => {
        setVisible(false);
        onClose?.();
      }, 3500);
      return () => clearTimeout(timer);
    }
  }, [show, onClose]);

  if (!visible || !xpGained) return null;

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed bottom-8 right-8 z-50"
          initial={reduced ? { opacity: 0 } : { opacity: 0, y: 50, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={reduced ? { opacity: 0 } : { opacity: 0, y: 50, scale: 0.8 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
        >
          <div className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-2xl shadow-2xl px-6 py-4 flex items-center gap-4">
            <motion.div
              initial={reduced ? {} : { scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.2 }}
            >
              <Zap size={32} className="text-yellow-200" />
            </motion.div>

            <div>
              <motion.p
                className="text-2xl font-bold"
                initial={reduced ? {} : { scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", delay: 0.3 }}
              >
                +{xpGained} XP
              </motion.p>
              <div className="flex items-center gap-3 text-sm text-yellow-100">
                {level && (
                  <span className="flex items-center gap-1">
                    <ArrowUp size={12} /> Level {level}
                  </span>
                )}
                {streak > 0 && (
                  <span className="flex items-center gap-1">
                    <Flame size={12} /> {streak} day streak
                  </span>
                )}
              </div>
            </div>

            {newBadges.length > 0 && (
              <motion.div
                className="flex items-center gap-1 bg-white/20 rounded-full px-3 py-1"
                initial={reduced ? {} : { scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", delay: 0.5 }}
              >
                <Trophy size={14} />
                <span className="text-sm font-medium">
                  {newBadges.length === 1 ? "New Badge!" : `${newBadges.length} Badges!`}
                </span>
              </motion.div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
