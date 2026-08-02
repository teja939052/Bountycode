import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";

const CONFETTI_COLORS = ["#6366f1", "#f59e0b", "#10b981", "#ef4444", "#ec4899", "#8b5cf6", "#06b6d4", "#f97316"];

const STREAK_EMOJIS = ["🔥", "🔥", "🔥", "⚡", "💥"];
const LEVEL_BG = ["from-indigo-900/95", "via-purple-900/95", "to-gray-900/95"];

const DIFFICULTY_CONFIG = {
  easy: { color: "text-green-400", label: "Easy" },
  medium: { color: "text-yellow-400", label: "Medium" },
  hard: { color: "text-red-400", label: "Hard" },
  expert: { color: "text-purple-400", label: "Expert" },
};

function randomBetween(min, max) {
  return min + Math.random() * (max - min);
}

function ConfettiPiece({ index, reduced }) {
  const color = CONFETTI_COLORS[index % CONFETTI_COLORS.length];
  const x = randomBetween(-250, 250);
  const y = randomBetween(-250, 50);
  const rotate = randomBetween(-720, 720);
  const delay = randomBetween(0, 0.3);
  const size = randomBetween(4, 10);

  return (
    <motion.div
      className="absolute rounded-sm"
      style={{
        width: size,
        height: size,
        backgroundColor: color,
        left: "50%",
        top: "50%",
      }}
      initial={reduced ? { opacity: 1, scale: 1 } : { opacity: 1, x: 0, y: 0, rotate: 0, scale: 1 }}
      animate={
        reduced
          ? { opacity: 0 }
          : { x, y, rotate, opacity: [1, 1, 0], scale: [1, 1.3, 0.3] }
      }
      transition={{ duration: 1.8, delay, ease: "easeOut" }}
    />
  );
}

function XPCountUp({ target, duration = 1500 }) {
  const [count, setCount] = useState(0);
  const startRef = useRef(null);
  const rafRef = useRef(null);

  useEffect(() => {
    if (target <= 0) { setCount(0); return; }
    startRef.current = null;
    const step = (timestamp) => {
      if (!startRef.current) startRef.current = timestamp;
      const progress = Math.min((timestamp - startRef.current) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setCount(Math.floor(eased * target));
      if (progress < 1) rafRef.current = requestAnimationFrame(step);
    };
    rafRef.current = requestAnimationFrame(step);
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); };
  }, [target, duration]);

  return <span>{count.toLocaleString()}</span>;
}

function ParticleBurst({ count = 12, colors = CONFETTI_COLORS }) {
  return (
    <>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="particle"
          style={{
            backgroundColor: colors[i % colors.length],
            "--tx": `${randomBetween(-120, 120)}px`,
            "--ty": `${randomBetween(-120, 120)}px`,
            animationDelay: `${randomBetween(0, 0.2)}s`,
            width: `${randomBetween(3, 7)}px`,
            height: `${randomBetween(3, 7)}px`,
          } as React.CSSProperties}
        />
      ))}
    </>
  );
}

function LevelUpContent({ title, subtitle, xp, onClose, reduced }) {
  const [flash, setFlash] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => setFlash(false), 600);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="relative flex flex-col items-center justify-center min-h-[60vh]">
      {flash && (
        <motion.div
          className="fixed inset-0 z-40 bg-white"
          initial={{ opacity: 0.9 }}
          animate={{ opacity: 0 }}
          transition={{ duration: 0.6 }}
        />
      )}

      <motion.div
        className="fixed inset-0 z-40 flex items-center justify-center pointer-events-none"
        initial={reduced ? { opacity: 1 } : { scale: 0, opacity: 1 }}
        animate={{ scale: 4, opacity: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        style={{ background: "radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%)" }}
      />

      <motion.div
        className="relative z-50 flex flex-col items-center gap-6"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        <motion.div
          className="text-8xl md:text-9xl pixel-font"
          initial={reduced ? {} : { scale: 0, rotate: -10 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: "spring", stiffness: 200, damping: 12, delay: 0.4 }}
        >
          ⬆️
        </motion.div>

        <motion.h1
          className="text-5xl md:text-7xl font-black text-white pixel-font tracking-wider text-center"
          style={{ textShadow: "0 0 40px rgba(99,102,241,0.6), 0 0 80px rgba(99,102,241,0.3)" }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          LEVEL UP!
        </motion.h1>

        <motion.div
          className="flex items-center gap-3 bg-indigo-500/20 backdrop-blur-md px-8 py-4 rounded-2xl border border-indigo-400/30"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8 }}
        >
          <span className="text-4xl">🏆</span>
          <span className="text-3xl font-bold text-white">{subtitle || "New Level Reached!"}</span>
        </motion.div>

        {xp > 0 && (
          <motion.div
            className="flex items-center gap-2 bg-yellow-500/20 backdrop-blur-md px-6 py-3 rounded-full border border-yellow-400/30"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.0 }}
          >
            <span className="text-yellow-300 text-xl font-bold">+<XPCountUp target={xp} /> XP</span>
          </motion.div>
        )}

        <ParticleBurst count={20} colors={["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd"]} />
      </motion.div>
    </div>
  );
}

function BadgeContent({ title, subtitle, reduced }) {
  return (
    <div className="relative flex flex-col items-center justify-center min-h-[60vh]">
      <motion.div
        className="relative z-50 flex flex-col items-center gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <motion.div
          className="relative"
          initial={reduced ? { opacity: 1 } : { scale: 0, rotate: 180, y: -100 }}
          animate={{ scale: 1, rotate: 0, y: 0 }}
          transition={{ type: "spring", stiffness: 180, damping: 14, delay: 0.2 }}
        >
          <div className="text-8xl md:text-9xl relative">
            <span className="holo-shimmer inline-block rounded-full p-2">{subtitle?.match(/[\u{1F300}-\u{1F9FF}]/u)?.[0] || "🏅"}</span>
          </div>
          <motion.div
            className="absolute -inset-4 rounded-full"
            style={{
              background: "linear-gradient(110deg, transparent 20%, rgba(255,255,255,0.4) 40%, rgba(255,255,255,0.7) 50%, rgba(255,255,255,0.4) 60%, transparent 80%)",
              backgroundSize: "200% 100%",
            }}
            animate={{ backgroundPosition: ["200% 0", "-200% 0"] }}
            transition={{ duration: 2.5, repeat: Infinity, ease: "linear" }}
          />
        </motion.div>

        <motion.h1
          className="text-4xl md:text-5xl font-black text-white pixel-font text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5 }}
        >
          New Badge Unlocked!
        </motion.h1>

        <motion.p
          className="text-2xl md:text-3xl font-bold text-yellow-300 text-center"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          {title || "Achievement Badge"}
        </motion.p>

        <ParticleBurst count={15} colors={["#f59e0b", "#eab308", "#fbbf24", "#fde68a"]} />
      </motion.div>
    </div>
  );
}

function SolveContent({ title, subtitle, xp, reduced }) {
  const difficulty = subtitle?.toLowerCase() || "";
  const diffConfig = DIFFICULTY_CONFIG[difficulty] || DIFFICULTY_CONFIG.easy;

  return (
    <div className="relative flex flex-col items-center justify-center min-h-[60vh]">
      <motion.div
        className="relative z-50 flex flex-col items-center gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <motion.div
          className="w-32 h-32 md:w-40 md:h-40 rounded-full bg-green-500/20 border-4 border-green-400 flex items-center justify-center"
          initial={reduced ? { opacity: 1, scale: 1 } : { scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.1 }}
        >
          <motion.span
            className="text-6xl md:text-7xl"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 300, delay: 0.3 }}
          >
            ✅
          </motion.span>
        </motion.div>

        <motion.h1
          className="text-4xl md:text-5xl font-black text-white text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          Problem Solved!
        </motion.h1>

        <motion.p
          className={`text-2xl font-bold ${diffConfig.color} pixel-font`}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          {diffConfig.label}
        </motion.p>

        {title && (
          <motion.p
            className="text-lg text-white/70 text-center max-w-md"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
          >
            {title}
          </motion.p>
        )}

        {xp > 0 && (
          <motion.div
            className="bg-green-500/20 backdrop-blur-md px-6 py-3 rounded-full border border-green-400/30"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <span className="text-green-300 text-xl font-bold">+<XPCountUp target={xp} /> XP</span>
          </motion.div>
        )}

        <ParticleBurst count={20} colors={["#10b981", "#34d399", "#6ee7b7", "#a7f3d0", "#6366f1", "#f59e0b"]} />
      </motion.div>
    </div>
  );
}

function StreakContent({ title, subtitle, xp, reduced }) {
  const days = parseInt(title) || 0;

  return (
    <div className="relative flex flex-col items-center justify-center min-h-[60vh]">
      <motion.div
        className="relative z-50 flex flex-col items-center gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <motion.div
          className="relative"
          initial={reduced ? { opacity: 1 } : { scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", stiffness: 200, damping: 12, delay: 0.1 }}
        >
          <motion.span
            className="text-8xl md:text-9xl inline-block streak-fire"
            animate={reduced ? {} : {
              scale: [1, 1.15, 1],
              rotate: [0, -5, 5, 0],
            }}
            transition={{ duration: 0.8, delay: 0.5 }}
          >
            🔥
          </motion.span>
          {Array.from({ length: 3 }).map((_, i) => (
            <motion.span
              key={i}
              className="absolute text-2xl"
              style={{
                top: `${-20 - i * 15}%`,
                left: `${40 + i * 20}%`,
              }}
              initial={{ opacity: 1, y: 0 }}
              animate={{ opacity: 0, y: -60 - i * 20 }}
              transition={{ duration: 1.2, delay: 0.3 + i * 0.2, ease: "easeOut" }}
            >
              {STREAK_EMOJIS[i % STREAK_EMOJIS.length]}
            </motion.span>
          ))}
        </motion.div>

        <motion.h1
          className="text-5xl md:text-7xl font-black text-white pixel-font text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          {days} Day Streak!
        </motion.h1>

        <motion.p
          className="text-2xl text-orange-300 font-bold text-center"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          {subtitle || "Incredible consistency!"}
        </motion.p>

        {xp > 0 && (
          <motion.div
            className="bg-orange-500/20 backdrop-blur-md px-6 py-3 rounded-full border border-orange-400/30"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <span className="text-orange-300 text-xl font-bold">+<XPCountUp target={xp} /> XP</span>
          </motion.div>
        )}

        <ParticleBurst count={16} colors={["#f97316", "#fb923c", "#fbbf24", "#f59e0b"]} />
      </motion.div>
    </div>
  );
}

function AchievementContent({ title, subtitle, xp, reduced }) {
  return (
    <div className="relative flex flex-col items-center justify-center min-h-[60vh]">
      <motion.div
        className="relative z-50 flex flex-col items-center gap-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <motion.div
          className="relative"
          initial={reduced ? { opacity: 1 } : { scale: 0, rotate: -20 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: "spring", stiffness: 180, damping: 13, delay: 0.2 }}
        >
          <motion.div
            className="text-8xl md:text-9xl"
            animate={reduced ? {} : {
              y: [0, -8, 0],
              rotate: [0, -3, 3, 0],
            }}
            transition={{ duration: 1.5, delay: 0.8, repeat: Infinity, repeatDelay: 2 }}
          >
            🏆
          </motion.div>
          <motion.div
            className="absolute -inset-4 rounded-full"
            style={{
              background: "radial-gradient(circle, rgba(234,179,8,0.3) 0%, transparent 70%)",
            }}
            animate={{ scale: [0.8, 1.2, 0.8], opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 2, repeat: Infinity }}
          />
        </motion.div>

        <motion.h1
          className="text-4xl md:text-5xl font-black text-white text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          Achievement Unlocked!
        </motion.h1>

        <motion.p
          className="text-2xl md:text-3xl font-bold text-yellow-300 pixel-font text-center"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
        >
          {title || "New Achievement"}
        </motion.p>

        {subtitle && (
          <motion.p
            className="text-lg text-white/60 text-center max-w-md"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.7 }}
          >
            {subtitle}
          </motion.p>
        )}

        {xp > 0 && (
          <motion.div
            className="bg-yellow-500/20 backdrop-blur-md px-6 py-3 rounded-full border border-yellow-400/30"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
          >
            <span className="text-yellow-300 text-xl font-bold">+<XPCountUp target={xp} /> XP</span>
          </motion.div>
        )}

        <ParticleBurst count={18} colors={["#eab308", "#facc15", "#fbbf24", "#fde68a", "#8b5cf6"]} />
      </motion.div>
    </div>
  );
}

const CONTENT_MAP = {
  levelup: LevelUpContent,
  badge: BadgeContent,
  solve: SolveContent,
  streak: StreakContent,
  achievement: AchievementContent,
};

export default function CelebrationOverlay({
  show,
  type = "confetti",
  title = "",
  subtitle = "",
  message = "",
  xp = 0,
  onClose,
  autoHide = true,
}: {
  show: boolean;
  type?: string;
  title?: string;
  subtitle?: string;
  message?: string;
  xp?: number;
  onClose?: () => void;
  autoHide?: boolean;
}) {
  const reduced = useReducedMotion();
  const [visible, setVisible] = useState(show);
  const [dismissed, setDismissed] = useState(false);

  const handleClose = useCallback(() => {
    setVisible(false);
    setDismissed(true);
    onClose?.();
  }, [onClose]);

  useEffect(() => {
    if (show) {
      setVisible(true);
      setDismissed(false);
      if (autoHide && type !== "confetti") {
        const timer = setTimeout(handleClose, 3500);
        return () => clearTimeout(timer);
      }
    }
  }, [show, autoHide, type, handleClose]);

  const isRPGType = ["levelup", "badge", "solve", "streak", "achievement"].includes(type);

  if (!visible || dismissed) return null;

  if (type === "confetti") {
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
                🎉
              </motion.div>
              {title && (
                <motion.p
                  className="text-center text-xl font-bold text-white mt-4 drop-shadow-lg"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                >
                  {title}
                </motion.p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    );
  }

  const ContentComponent = CONTENT_MAP[type];

  if (!ContentComponent) return null;

  return (
    <AnimatePresence onExitComplete={handleClose}>
      {visible && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center"
          style={{
            background: "linear-gradient(135deg, rgba(10,16,32,0.94) 0%, rgba(20,29,54,0.92) 55%, rgba(39,24,51,0.9) 100%)",
          }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          <ContentComponent
            title={title}
            subtitle={subtitle}
            xp={xp}
            onClose={handleClose}
            reduced={reduced}
          />

          <motion.button
            className="absolute top-6 right-6 z-50 w-10 h-10 rounded-full bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center text-white hover:bg-white/20 transition-colors"
            onClick={handleClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.2 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            ✕
          </motion.button>

          <motion.p
            className="absolute bottom-8 left-1/2 -translate-x-1/2 text-white/30 text-sm pixel-font"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.5 }}
          >
            Press ESC or click ✕ to continue
          </motion.p>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
