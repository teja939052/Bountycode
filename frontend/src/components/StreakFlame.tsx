import { motion } from "framer-motion";
import { Snowflake } from "lucide-react";

type StreakFlameProps = {
  streak: number;
  freezeActive?: boolean;
  size?: number;
};

function getMilestone(streak: number): number | null {
  if (streak >= 100) return 100;
  if (streak >= 30) return 30;
  if (streak >= 7) return 7;
  return null;
}

export default function StreakFlame({ streak, freezeActive, size = 28 }: StreakFlameProps) {
  const milestone = getMilestone(streak);
  const isMilestone = milestone !== null && streak > 0 && streak % milestone === 0;

  if (freezeActive) {
    return (
      <motion.div
        className="relative inline-flex items-center justify-center"
        style={{ width: size, height: size }}
        animate={{ rotate: [0, -6, 6, 0] }}
        transition={{ duration: 2.4, repeat: Infinity, ease: "linear" }}
      >
        <Snowflake size={size} className="text-sky-300" />
        {isMilestone && (
          <motion.span
            className="absolute -top-1 -right-1 text-[10px]"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 260, damping: 20 }}
          >
            🧊
          </motion.span>
        )}
      </motion.div>
    );
  }

  return (
    <motion.div
      className="relative inline-flex items-center justify-center"
      style={{ width: size, height: size }}
      animate={
        isMilestone
          ? { scale: [1, 1.25, 1], rotate: [0, -5, 5, 0] }
          : { scale: [1, 1.08, 1], rotate: [0, -3, 3, 0] }
      }
      transition={
        isMilestone
          ? { duration: 0.9, repeat: Infinity, repeatDelay: 1.2, ease: "easeInOut" }
          : { duration: 1.6, repeat: Infinity, ease: "linear" }
      }
    >
      <span className="text-[length:inherit] leading-none">🔥</span>
      {isMilestone && (
        <motion.span
          className="absolute -top-1 -right-1"
          initial={{ scale: 0, y: 4 }}
          animate={{ scale: 1, y: 0 }}
          transition={{ type: "spring", stiffness: 260, damping: 20, delay: 0.15 }}
        >
          <span className="text-[10px]">✨</span>
        </motion.span>
      )}
    </motion.div>
  );
}
