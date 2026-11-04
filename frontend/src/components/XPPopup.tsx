import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import { Zap, Flame, Trophy, ArrowUp } from "lucide-react";
import { CODDY, getLevelLabel } from "./gamification/palette";

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

  const lvl = getLevelLabel(level);
  const color = CODDY[lvl.color];

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed bottom-8 right-8 z-50 w-full sm:w-80"
          initial={{ opacity: 0, y: 40, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 40, scale: 0.9 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
        >
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.8, opacity: 0 }}
            transition={{ type: "spring", stiffness: 300, damping: 20, delay: 0.1 }}
            className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl shadow-2xl p-5 flex items-center gap-4"
            style={{
              boxShadow: `0 0 24px ${color.base}30`,
              backgroundColor: "rgba(255,255,255,0.9)",
            }}
          >
            <motion.div
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.2 }}
            >
              <div className="w-12 h-12 rounded-2xl flex items-center justify-center text-white shadow-lg" style={{
                background: `linear-gradient(135deg, ${color.base}, ${CODDY.indigo.base})`,
                boxShadow: `0 0 16px ${color.base}50`,
              }}>
                <Zap size={32} className="text-white" />
              </div>
            </motion.div>

            <div className="flex-1">
              <motion.p
                className="text-2xl font-display font-bold text-ink dark:text-white"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", delay: 0.3 }}
              >
                +{xpGained} XP
              </motion.p>
              <div className="flex items-center gap-3 text-sm text-slate-500 dark:text-slate-400 mt-1">
                {level && (
                  <span className="flex items-center gap-1">
                    <ArrowUp size={12} className="text-blue-500 dark:text-blue-400" />
                    <span className="font-bold text-ink dark:text-white">Level {level}</span>
                    <span className="text-[10px] px-1.5 py-[1px] rounded border border-white/30" style={{
                      backgroundColor: `${color.base}15`,
                      color: color.base,
                      border: `1px solid ${color.base}40`,
                    }}>
                      {lvl.label}
                    </span>
                  </span>
                )}
                {streak > 0 && (
                  <span className="flex items-center gap-1">
                    <Flame size={12} className="text-danger-500 dark:text-danger-400" />
                    <span className="font-bold text-ink dark:text-white">{streak}</span>
                    <span className="text-[10px]">day streak</span>
                  </span>
                )}
              </div>
            </div>

            {newBadges.length > 0 && (
              <motion.div
                className="flex items-center gap-1 bg-white border-border/20 rounded-full px-3 py-1.5 ml-2"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", delay: 0.5 }}
              >
                <Trophy size={14} className="text-warning-500" />
                <span className="text-sm font-bold text-ink dark:text-white">
                  {newBadges.length === 1 ? "New Badge!" : `${newBadges.length} Badges!`}
                </span>
              </motion.div>
            )}
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
