import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import { Zap, Flame, Trophy, ArrowUp } from "lucide-react";

type BadgeItem = { id: string; name?: string; icon?: string; rarity?: string };

type DiamondsPopupProps = {
  show: boolean;
  xpGained: number;
  level?: number;
  streak?: number;
  newBadges?: BadgeItem[] | string[];
  critical?: boolean;
  criticalBonus?: number;
  onClose?: () => void;
};

const RARITY_COLOR: Record<string, string> = {
  common: "#9CA3AF",
  uncommon: "#22C55E",
  rare: "#8B6BD9",
  epic: "#EC4899",
  legendary: "#EAB74D",
};

export default function DiamondsPopup({ show, xpGained, level, streak, newBadges = [], critical = false, criticalBonus = 0, onClose }: DiamondsPopupProps) {
  const reduced = useReducedMotion();
  const [visible, setVisible] = useState(show);

  useEffect(() => {
    setVisible(show);
    if (show) {
      const timer = setTimeout(() => {
        setVisible(false);
        onClose?.();
      }, 4000);
      return () => clearTimeout(timer);
    }
  }, [show, onClose]);

  if (!visible || !xpGained) return null;

  const badges: BadgeItem[] = newBadges.map((b) => (typeof b === "string" ? { id: b, icon: "🏆", rarity: "common" } : b));

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed bottom-6 right-6 z-50"
          initial={reduced ? { opacity: 0 } : { opacity: 0, y: 40, scale: 0.85 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={reduced ? { opacity: 0 } : { opacity: 0, y: 40, scale: 0.85 }}
          transition={{ type: "spring", stiffness: 260, damping: 20 }}
        >
          <div
            className="gamification-border-gradient rounded-2xl p-5 flex items-center gap-4 min-w-[280px]"
            style={{
              background: critical
                ? 'linear-gradient(135deg, rgba(245,158,11,0.92), rgba(239,68,68,0.92))'
                : 'linear-gradient(135deg, rgba(99,102,241,0.88), rgba(139,92,246,0.88))',
            }}
          >
            <motion.div
              initial={reduced ? {} : { scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.15 }}
              className="shrink-0"
            >
              {critical ? (
                <span className="text-4xl">⚡</span>
              ) : (
                <Zap size={34} className="text-yellow-200" />
              )}
            </motion.div>

            <div className="flex-1 min-w-0">
              <motion.p
                className="text-2xl font-black text-white tracking-tight"
                initial={reduced ? {} : { scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", delay: 0.25 }}
              >
                {critical ? 'CRITICAL HIT!' : `+${xpGained} Diamonds`}
              </motion.p>
              {critical && criticalBonus && (
                <div className="text-sm text-yellow-100 font-semibold tick-up">+{criticalBonus} bonus Diamonds</div>
              )}
              <div className="flex items-center gap-3 text-sm text-white/80 mt-0.5">
                {level && !critical && (
                  <span className="flex items-center gap-1 font-medium">
                    <ArrowUp size={12} /> Level {level}
                  </span>
                )}
                {streak > 0 && !critical && (
                  <span className="flex items-center gap-1 font-medium">
                    <Flame size={12} /> {streak} day streak
                  </span>
                )}
              </div>
            </div>

            {badges.length > 0 && (
              <motion.div
                className="flex items-center gap-1.5 bg-white/20 backdrop-blur-md border border-white/25 rounded-full px-3 py-1.5"
                initial={reduced ? {} : { scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", delay: 0.45 }}
              >
                <div className="flex items-center gap-1">
                  {badges.slice(0, 3).map((badge) => {
                    const rarityColor = RARITY_COLOR[badge.rarity || "common"] || "#D1D5DB";
                    return (
                      <span
                        key={badge.id}
                        className="text-sm leading-none"
                        style={{ filter: `drop-shadow(0 0 4px ${rarityColor})` }}
                        title={badge.name || badge.id}
                      >
                        {badge.icon || "🏆"}
                      </span>
                    );
                  })}
                </div>
                <span className="text-sm font-bold text-white">
                  {badges.length === 1 ? "New Badge!" : `${badges.length} Badges!`}
                </span>
              </motion.div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
