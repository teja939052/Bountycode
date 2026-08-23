import { motion } from "framer-motion";

export default function StreakConstellation({ streak = 0, maxStreak = 30 }) {
  const getStarCount = () => Math.min(streak, 30);
  const isSupernova = streak >= 30;

  const starPositions = Array.from({ length: 30 }).map((_, i) => {
    const angle = (i / 30) * Math.PI * 2;
    const radius = 60 + (i % 3) * 15;
    return {
      x: 80 + Math.cos(angle) * radius,
      y: 80 + Math.sin(angle) * radius,
      active: i < streak,
      size: 2 + (i < streak ? 1 : 0),
    };
  });

  return (
    <div className="relative">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div>
          <span className="text-[10px] font-mono text-cyber-blue/70 tracking-widest uppercase">
            Practice Streak //
          </span>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-display font-black text-text-primary">
              {streak}
            </span>
            <span className="text-xs font-mono text-gray-500">days</span>
          </div>
        </div>
        {isSupernova && (
          <motion.div
            animate={{ scale: [1, 1.1, 1], opacity: [0.8, 1, 0.8] }}
            transition={{ repeat: Infinity, duration: 2 }}
            className="px-3 py-1 rounded-full bg-cyber-purple/20 border border-cyber-purple/40 text-purple-300 text-[10px] font-mono uppercase tracking-wider"
          >
            Supernova
          </motion.div>
        )}
      </div>

      {/* Constellation map */}
      <div className="relative h-40 bg-space-void/50 rounded-xl border border-space-border overflow-hidden">
        {/* Grid background */}
        <div className="absolute inset-0 ambient-grid opacity-20" />

        <svg viewBox="0 0 160 160" className="w-full h-full">
          {/* Connection lines */}
          {starPositions.filter(s => s.active).map((star, i, arr) => {
            if (i === 0) return null;
            const prev = arr[i - 1];
            return (
              <motion.line
                key={`line-${i}`}
                x1={prev.x} y1={prev.y}
                x2={star.x} y2={star.y}
                stroke="rgba(76,201,240,0.3)"
                strokeWidth="0.5"
                initial={{ pathLength: 0, opacity: 0 }}
                animate={{ pathLength: 1, opacity: 1 }}
                transition={{ delay: i * 0.05, duration: 0.3 }}
              />
            );
          })}

          {/* Stars */}
          {starPositions.map((star, i) => (
            <motion.circle
              key={i}
              cx={star.x}
              cy={star.y}
              r={star.size}
              fill={star.active ? "#4CC9F0" : "rgba(76,201,240,0.15)"}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: i * 0.03 }}
            />
          ))}

          {/* Glow effect for supernova */}
          {isSupernova && (
            <motion.circle
              cx="80" cy="80" r="70"
              fill="none"
              stroke="rgba(114,9,183,0.3)"
              strokeWidth="1"
              animate={{ r: [65, 75, 65], opacity: [0.2, 0.5, 0.2] }}
              transition={{ repeat: Infinity, duration: 3 }}
            />
          )}
        </svg>
      </div>

      {/* Progress to next milestone */}
      <div className="mt-3">
        <div className="flex justify-between text-[10px] font-mono text-gray-500 mb-1">
          <span>Next: {streak < 7 ? "7-day" : streak < 14 ? "14-day" : streak < 30 ? "30-day Supernova" : "Keep going!"}</span>
          <span>{Math.min(streak, 30)}/30</span>
        </div>
        <div className="h-1 bg-space-void rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-cyber-blue to-cyber-purple rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${(Math.min(streak, 30) / 30) * 100}%` }}
            transition={{ duration: 1, delay: 0.3 }}
          />
        </div>
      </div>
    </div>
  );
}
