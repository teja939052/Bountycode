import { motion } from "framer-motion";

export default function ScoreRing({
  score = 0,
  label = "SCORE",
  size = "lg",
  color = "blue",
}) {
  const sizeMap = {
    sm: { ring: "w-20 h-20", text: "text-xl", label: "text-[8px]" },
    md: { ring: "w-28 h-28", text: "text-2xl", label: "text-[9px]" },
    lg: { ring: "w-36 h-36", text: "text-4xl", label: "text-[10px]" },
    xl: { ring: "w-44 h-44", text: "text-5xl", label: "text-xs" },
  };

  const colorMap = {
    blue: {
      text: "text-cyber-blue",
      glow: "drop-shadow-[0_0_15px_rgba(76,201,240,0.5)]",
      ring: "border-cyber-blue/30",
      ringFill: "border-cyber-blue",
    },
    green: {
      text: "text-cyber-green",
      glow: "drop-shadow-[0_0_15px_rgba(75,181,67,0.5)]",
      ring: "border-cyber-green/30",
      ringFill: "border-cyber-green",
    },
    purple: {
      text: "text-cyber-purple",
      glow: "drop-shadow-[0_0_15px_rgba(114,9,183,0.5)]",
      ring: "border-cyber-purple/30",
      ringFill: "border-cyber-purple",
    },
    amber: {
      text: "text-cyber-amber",
      glow: "drop-shadow-[0_0_15px_rgba(245,158,11,0.5)]",
      ring: "border-cyber-amber/30",
      ringFill: "border-cyber-amber",
    },
    red: {
      text: "text-cyber-red",
      glow: "drop-shadow-[0_0_15px_rgba(239,68,68,0.5)]",
      ring: "border-cyber-red/30",
      ringFill: "border-cyber-red",
    },
  };

  const s = sizeMap[size] || sizeMap.lg;
  const c = colorMap[color] || colorMap.blue;
  const isLow = score < 50;

  return (
    <div className="flex flex-col items-center justify-center relative">
      {/* Outer rotating ring */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ repeat: Infinity, duration: 25, ease: "linear" }}
        className={`absolute ${s.ring} rounded-full border-2 border-dashed ${c.ring} p-2`}
      />

      {/* Inner pulsing ring */}
      <motion.div
        animate={{ scale: [1, 1.03, 1], opacity: [0.3, 0.6, 0.3] }}
        transition={{ repeat: Infinity, duration: 3, ease: "easeInOut" }}
        className={`absolute ${s.ring} rounded-full border ${c.ringFill} opacity-20`}
        style={{ transform: "scale(1.15)" }}
      />

      {/* Score number */}
      <div className="z-10 text-center">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.6, type: "spring" }}
          className={`${s.text} font-display font-black tracking-tighter ${c.text} ${c.glow}`}
        >
          {Math.round(score)}%
        </motion.div>
        <div className={`${s.label} font-mono uppercase tracking-widest text-gray-500 mt-1`}>
          {label}
        </div>
      </div>
    </div>
  );
}
