import { memo } from "react";
import { motion, AnimatePresence } from "framer-motion";

export type CharacterState =
  | "idle"
  | "walking"
  | "discovering"
  | "thinking"
  | "correct"
  | "struggling"
  | "boss"
  | "mastery";

interface PlayerCharacterProps {
  state?: CharacterState;
  titleEmoji?: string;
  size?: "sm" | "md" | "lg";
  className?: string;
}

const STATE_LABELS: Record<CharacterState, string> = {
  idle: "Standing by",
  walking: "On the move",
  discovering: "Looking around",
  thinking: "Thinking…",
  correct: "Nailed it!",
  struggling: "Working through it",
  boss: "Facing the boss",
  mastery: "Mastered!",
};

const STATE_BUBBLE: Partial<Record<CharacterState, string>> = {
  thinking: "💡",
  discovering: "👀",
  correct: "🎉",
  mastery: "🏆",
  struggling: "🤔",
  boss: "⚔️",
  walking: "🚶",
};

/**
 * Lightweight character avatar with smooth Framer Motion animations.
 *
 * Respects ``prefers-reduced-motion`` — Framer Motion handles this
 * automatically when the user has that setting enabled.
 */
function PlayerCharacterImpl({
  state = "idle",
  titleEmoji,
  size = "md",
  className = "",
}: PlayerCharacterProps) {
  const sizeClass =
    size === "sm" ? "w-10 h-10 text-lg" : size === "lg" ? "w-20 h-20 text-4xl" : "w-14 h-14 text-2xl";

  // State-driven animation variants
  const bodyAnimation: Record<CharacterState, any> = {
    idle: { scale: 1, rotate: 0 },
    walking: { y: [0, -4, 0], transition: { repeat: Infinity, duration: 0.6 } },
    discovering: { rotate: [0, -10, 10, 0], transition: { repeat: Infinity, duration: 1.5 } },
    thinking: { scale: [1, 1.02, 1], transition: { repeat: Infinity, duration: 2 } },
    correct: { scale: [1, 1.2, 1], rotate: [0, 10, -10, 0], transition: { duration: 0.5 } },
    struggling: { x: [0, -2, 2, 0], transition: { repeat: Infinity, duration: 0.8 } },
    boss: { scale: [1, 1.05, 1], transition: { repeat: Infinity, duration: 1 } },
    mastery: { scale: [1, 1.15, 1], rotate: [0, 5, -5, 0], transition: { duration: 0.6 } },
  };

  return (
    <div
      className={`relative inline-flex flex-col items-center select-none ${className}`}
      role="img"
      aria-label={`Your character, ${STATE_LABELS[state]}`}
    >
      <motion.div
        animate={bodyAnimation[state]}
        className={`${sizeClass} rounded-full bg-gradient-to-br from-sky-500 to-blue-700 flex items-center justify-center shadow-lg ring-2 ring-white/30`}
      >
        <span className="leading-none">{titleEmoji ?? "🏴‍☠️"}</span>
      </motion.div>

      {/* State bubble */}
      <AnimatePresence mode="wait">
        {STATE_BUBBLE[state] && (
          <motion.div
            key={state}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            className="absolute -top-1 -right-3 text-sm bg-white rounded-full shadow px-1.5 py-0.5 border border-zinc-200"
          >
            {STATE_BUBBLE[state]}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export const PlayerCharacter = memo(PlayerCharacterImpl);
