import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";

const LOADING_MESSAGES = [
  "Entering the realm...",
  "Preparing your quest...",
  "Summoning challenges...",
  "Sharpening your skills...",
  "Loading the arena...",
  "Forging your path...",
  "Gathering intelligence...",
  "Activating power-ups...",
  "Brewing wisdom potion...",
  "Calibrating the oracle...",
  "Unlocking achievements...",
  "Warming up the compiler...",
  "Polishing the leaderboard...",
  "Feeding the hamsters...",
  "Consulting the ancients...",
  "Decrypting the matrix...",
];

const TIPS = [
  "Consistency beats intensity — show up every day.",
  "Streaks multiply your XP gains.",
  "Reviewing your old solutions reinforces learning.",
  "Explain concepts aloud to deepen understanding.",
  "Mix easy and hard problems for balanced growth.",
  "Taking breaks improves problem-solving ability.",
  "Focus on weak areas to level up faster.",
  "Mock interviews build real-world confidence.",
  "System design interviews test trade-off thinking.",
  "A well-optimized resume opens more doors.",
];

export default function RPGLoadingScreen({
  loading = true,
  progress = 0,
  message,
  tipInterval = 5000,
  variant = "fullscreen",
}) {
  const [displayMessage, setDisplayMessage] = useState(message || LOADING_MESSAGES[0]);
  const [tip, setTip] = useState("");
  const [progressValue, setProgressValue] = useState(0);

  const currentMessage = useMemo(() => {
    if (message) return message;
    return LOADING_MESSAGES[Math.floor(Math.random() * LOADING_MESSAGES.length)];
  }, [message]);

  useEffect(() => {
    if (!loading) return;

    const msgInterval = setInterval(() => {
      const next = LOADING_MESSAGES[Math.floor(Math.random() * LOADING_MESSAGES.length)];
      setDisplayMessage(next);
    }, 3000);

    const tipIntervalId = setInterval(() => {
      const next = TIPS[Math.floor(Math.random() * TIPS.length)];
      setTip(next);
    }, tipInterval);

    return () => {
      clearInterval(msgInterval);
      clearInterval(tipIntervalId);
    };
  }, [loading, tipInterval]);

  useEffect(() => {
    if (!loading) {
      setProgressValue(100);
      return;
    }
    if (progress > 0) {
      setProgressValue(progress);
      return;
    }

    const interval = setInterval(() => {
      setProgressValue(prev => {
        const next = prev + Math.random() * 8;
        return next >= 90 ? 90 : next;
      });
    }, 400);

    return () => clearInterval(interval);
  }, [loading, progress]);

  useEffect(() => {
    if (loading) {
      setTip(TIPS[Math.floor(Math.random() * TIPS.length)]);
    }
  }, [loading]);

  const content = (
    <div className="flex flex-col items-center justify-center gap-6">
      {/* Spinning sword icon */}
      <motion.div
        className="relative w-16 h-16 md:w-20 md:h-20"
        animate={{ rotate: 360 }}
        transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
      >
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-4xl md:text-5xl">⚔️</span>
        </div>
        <motion.div
          className="absolute -inset-4 rounded-full border-2 border-dashed border-indigo-400/30"
          animate={{ rotate: -360 }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
        />
      </motion.div>

      {/* Pixel loading text */}
      <AnimatePresence mode="wait">
        <motion.p
          key={displayMessage}
          className="text-white/70 text-lg pixel-font"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.3 }}
        >
          {displayMessage}
        </motion.p>
      </AnimatePresence>

      {/* XP-style progress bar */}
      <div className="w-64 md:w-80">
        <div className="flex items-center justify-between text-xs text-white/40 font-mono mb-2">
          <span>Loading...</span>
          <span>{Math.round(progressValue)}%</span>
        </div>
        <div className="h-3 rounded-full bg-white/10 overflow-hidden border border-white/5">
          <motion.div
            className="h-full rounded-full bg-gradient-to-r from-indigo-500 via-purple-400 to-amber-400 xp-bar-glow"
            initial={{ width: "0%" }}
            animate={{ width: `${progressValue}%` }}
            transition={{ duration: 0.3, ease: "easeOut" }}
          />
        </div>
        <div className="mt-1 flex justify-between text-[10px] text-white/20 font-mono">
          <span>▮▮▮▮▮▮▮▮▮▮</span>
          <span>XP: {Math.floor(progressValue * 10)}/{1000}</span>
        </div>
      </div>

      {/* Tip */}
      <AnimatePresence mode="wait">
        {tip && (
          <motion.div
            key={tip}
            className="max-w-xs text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.5 }}
          >
            <p className="text-[10px] uppercase tracking-[0.2em] text-amber-400/60 font-mono mb-1">
              💡 Pro Tip
            </p>
            <p className="text-white/40 text-xs leading-relaxed">{tip}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );

  if (variant === "inline") {
    return (
      <AnimatePresence>
        {loading && (
          <motion.div
            className="flex flex-col items-center justify-center py-16"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            {content}
          </motion.div>
        )}
      </AnimatePresence>
    );
  }

  return (
    <AnimatePresence>
      {loading && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center bg-gray-950"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          {content}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
