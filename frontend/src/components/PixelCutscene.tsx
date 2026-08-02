import { useState, useEffect, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";

function DragonPixelArt() {
  return (
    <div className="relative w-48 h-48 md:w-64 md:h-64">
      <div className="absolute inset-0 grid grid-cols-8 grid-rows-8 gap-0">
        {[
          "00000000",
          "00111100",
          "01222210",
          "12233221",
          "12233221",
          "01222210",
          "00111100",
          "00000000",
        ].map((row, r) =>
          row.split("").map((pixel, c) => {
            const colors = {
              "0": "transparent",
              "1": "#8b0000",
              "2": "#ff4444",
              "3": "#ffcc00",
            };
            const size = 100 / 8;
            return (
              <div
                key={`${r}-${c}`}
                style={{
                  width: `${size}%`,
                  height: `${size}%`,
                  backgroundColor: colors[pixel] || "transparent",
                }}
              />
            );
          })
        )}
      </div>
    </div>
  );
}

function TrophyPixelArt() {
  return (
    <div className="relative w-32 h-32 md:w-48 md:h-48">
      <div className="absolute inset-0 grid grid-cols-6 grid-rows-6 gap-0">
        {[
          "001100",
          "011110",
          "111111",
          "011110",
          "001100",
          "011110",
        ].map((row, r) =>
          row.split("").map((pixel, c) => {
            const colors = {
              "0": "transparent",
              "1": "#fbbf24",
            };
            const size = 100 / 6;
            return (
              <div
                key={`${r}-${c}`}
                style={{
                  width: `${size}%`,
                  height: `${size}%`,
                  backgroundColor: colors[pixel] || "transparent",
                }}
              />
            );
          })
        )}
      </div>
    </div>
  );
}

function WalkingCharacter() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setStep(s => (s + 1) % 4), 250);
    return () => clearInterval(interval);
  }, []);

  const legOffsets = [0, -3, 0, 3];

  return (
    <div className="relative w-24 h-32 md:w-32 md:h-40">
      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        initial={{ x: -200 }}
        animate={{ x: 0 }}
        transition={{ duration: 1.5, ease: "easeOut" }}
      >
        <div className="flex flex-col items-center">
          {/* Head */}
          <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-amber-300 border-2 border-amber-600" />
          {/* Body */}
          <div className="w-10 h-12 md:w-12 md:h-14 bg-indigo-500 rounded-sm border border-indigo-700 flex items-center justify-center">
            <div className="w-4 h-6 bg-indigo-300 rounded-sm" />
          </div>
          {/* Legs */}
          <div className="flex gap-1">
            <div
              className="w-3 h-6 bg-blue-600 rounded-sm transition-transform"
              style={{ transform: `translateY(${legOffsets[step]}px)` }}
            />
            <div
              className="w-3 h-6 bg-blue-600 rounded-sm transition-transform"
              style={{ transform: `translateY(${legOffsets[(step + 2) % 4]}px)` }}
            />
          </div>
        </div>
      </motion.div>
    </div>
  );
}

function BookOpening() {
  return (
    <motion.div
      className="relative w-40 h-32 md:w-56 md:h-44"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        initial={{ rotateY: 0 }}
        animate={{ rotateY: -180 }}
        transition={{ duration: 1.5, ease: "easeInOut" }}
        style={{ transformStyle: "preserve-3d", perspective: 600 }}
      >
        <div className="w-full h-full bg-gradient-to-br from-amber-700 to-amber-900 rounded-r-lg border-2 border-amber-500 flex items-center justify-center">
          <span className="text-4xl md:text-6xl">📖</span>
        </div>
      </motion.div>
      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        initial={{ rotateY: 180 }}
        animate={{ rotateY: 0 }}
        transition={{ duration: 1.5, ease: "easeInOut", delay: 0.1 }}
        style={{ transformStyle: "preserve-3d", perspective: 600 }}
      >
        <div className="w-full h-full bg-gradient-to-br from-amber-600 to-amber-800 rounded-l-lg border-2 border-amber-500 flex items-center justify-center">
          <span className="text-4xl md:text-6xl">📜</span>
        </div>
      </motion.div>
    </motion.div>
  );
}

function SparkleParticles({ count = 15 }) {
  const particles = Array.from({ length: count }).map((_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: 2 + Math.random() * 4,
    delay: Math.random() * 0.5,
  }));

  return (
    <>
      {particles.map((p) => (
        <motion.div
          key={p.id}
          className="absolute rounded-full"
          style={{
            left: `${p.x}%`,
            top: `${p.y}%`,
            width: p.size,
            height: p.size,
            backgroundColor: "#fbbf24",
          }}
          initial={{ opacity: 0, scale: 0 }}
          animate={{
            opacity: [0, 1, 0],
            scale: [0, 1.5, 0],
          }}
          transition={{
            duration: 1.5,
            delay: p.delay,
            repeat: Infinity,
            repeatDelay: 1,
          }}
        />
      ))}
    </>
  );
}

const SCENE_CONFIG = {
  chapter: {
    bgClass: "from-gray-900 via-indigo-950 to-gray-900",
    content: ChapterScene,
  },
  boss: {
    bgClass: "from-red-950 via-red-900 to-rose-950",
    content: BossScene,
  },
  victory: {
    bgClass: "from-gray-900 via-emerald-950 to-gray-900",
    content: VictoryScene,
  },
  welcome: {
    bgClass: "from-indigo-950 via-purple-950 to-gray-900",
    content: WelcomeScene,
  },
};

function ChapterScene({ title, subtitle, onContinue, reduced }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-8 px-4">
      <BookOpening />

      <motion.div
        className="text-center space-y-3"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
      >
        <motion.p
          className="text-amber-400 text-sm md:text-base font-mono uppercase tracking-[0.3em]"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
        >
          Chapter {subtitle || "I"}
        </motion.p>
        <motion.h1
          className="text-4xl md:text-6xl font-black text-white pixel-font"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.2 }}
        >
          {title || "The Journey Begins"}
        </motion.h1>
        <motion.p
          className="text-white/50 text-sm mt-4"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.6 }}
        >
          Press any key or click to continue
        </motion.p>
      </motion.div>
    </div>
  );
}

function BossScene({ title, subtitle, onContinue, reduced }) {
  const [shake, setShake] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => setShake(false), 1500);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-6 px-4">
      <motion.div
        className={`relative ${shake ? "pixel-glitch" : ""}`}
        initial={{ opacity: 0, scale: 0.5 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <DragonPixelArt />
        <motion.div
          className="absolute -inset-8 rounded-full"
          style={{
            background: "radial-gradient(circle, rgba(239,68,68,0.2) 0%, transparent 70%)",
          }}
          animate={{ scale: [0.8, 1.2, 0.8], opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      </motion.div>

      <motion.div
        className="text-center space-y-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <motion.p
          className="text-red-400 text-sm font-mono uppercase tracking-[0.3em]"
          animate={reduced ? {} : { opacity: [1, 0.5, 1] }}
          transition={{ duration: 1, repeat: Infinity }}
        >
          ⚔️ Boss Encounter ⚔️
        </motion.p>
        <motion.h1
          className="text-4xl md:text-5xl font-black text-red-400 pixel-font"
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ type: "spring", delay: 0.7 }}
        >
          BOSS: {title || "Unknown"}
        </motion.h1>
        {subtitle && (
          <p className="text-white/60 text-sm">{subtitle}</p>
        )}
      </motion.div>

      <motion.p
        className="text-white/30 text-sm mt-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
      >
        Press any key or click to continue
      </motion.p>
    </div>
  );
}

function VictoryScene({ title, subtitle, onContinue, reduced }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-6 px-4">
      <div className="relative">
        <motion.div
          initial={{ y: 200, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ type: "spring", stiffness: 150, damping: 15, delay: 0.2 }}
        >
          <TrophyPixelArt />
        </motion.div>
        <SparkleParticles count={20} />
      </div>

      <motion.div
        className="text-center space-y-3"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
      >
        <motion.h1
          className="text-5xl md:text-7xl font-black pixel-font"
          style={{
            background: "linear-gradient(90deg, #fbbf24, #f59e0b, #fbbf24, #eab308, #fbbf24)",
            backgroundSize: "200% auto",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
          animate={{ backgroundPosition: ["0% center", "200% center"] }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
        >
          Victory!
        </motion.h1>
        {title && (
          <p className="text-2xl font-bold text-white">{title}</p>
        )}
        {subtitle && (
          <p className="text-white/60 max-w-md">{subtitle}</p>
        )}
      </motion.div>

      <motion.p
        className="text-white/30 text-sm mt-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.5 }}
      >
        Press any key or click to continue
      </motion.p>
    </div>
  );
}

function WelcomeScene({ title, subtitle, onContinue, reduced }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-6 px-4">
      <WalkingCharacter />

      <motion.div
        className="text-center space-y-3"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.2 }}
      >
        <motion.h1
          className="text-4xl md:text-6xl font-black text-white pixel-font"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.4 }}
        >
          Welcome, Adventurer!
        </motion.h1>
        <motion.p
          className="text-lg text-indigo-300"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.7 }}
        >
          {title || "Your quest awaits..."}
        </motion.p>
        {subtitle && (
          <motion.p
            className="text-white/50 text-sm max-w-md"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 2.0 }}
          >
            {subtitle}
          </motion.p>
        )}
      </motion.div>

      <motion.p
        className="text-white/40 text-sm mt-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 2.2 }}
      >
        Press any key or click to continue
      </motion.p>
    </div>
  );
}

export default function PixelCutscene({
  show,
  scene = "chapter",
  title = "",
  subtitle = "",
  onComplete,
  autoHide = false,
  autoHideDelay = 4000,
}) {
  const reduced = useReducedMotion();
  const [visible, setVisible] = useState(show);
  const keyHandlerRef = useRef(null);

  const handleContinue = useCallback(() => {
    setVisible(false);
    onComplete?.();
  }, [onComplete]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === "Escape") {
      handleContinue();
    } else if (["Enter", " "].includes(e.key)) {
      e.preventDefault();
      handleContinue();
    }
  }, [handleContinue]);

  useEffect(() => {
    setVisible(show);
    if (show) {
      if (autoHide) {
        const timer = setTimeout(handleContinue, autoHideDelay);
        return () => clearTimeout(timer);
      }
    }
  }, [show, autoHide, autoHideDelay, handleContinue]);

  useEffect(() => {
    if (visible) {
      keyHandlerRef.current = handleKeyDown;
      window.addEventListener("keydown", handleKeyDown);
      return () => window.removeEventListener("keydown", handleKeyDown);
    }
  }, [visible, handleKeyDown]);

  const config = SCENE_CONFIG[scene] || SCENE_CONFIG.chapter;
  const ContentComponent = config.content;

  if (!show && !visible) return null;

  return (
    <AnimatePresence onExitComplete={() => setVisible(false)}>
      {visible && (
        <motion.div
          className={`fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br ${config.bgClass}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
          onClick={handleContinue}
        >
          <ContentComponent
            title={title}
            subtitle={subtitle}
            onContinue={handleContinue}
            reduced={reduced}
          />

          <motion.button
            className="absolute top-6 right-6 z-50 w-10 h-10 rounded-full bg-white/10 backdrop-blur-md border border-white/20 flex items-center justify-center text-white hover:bg-white/20 transition-colors"
            onClick={(e) => { e.stopPropagation(); handleContinue(); }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1.0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
          >
            ✕
          </motion.button>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
