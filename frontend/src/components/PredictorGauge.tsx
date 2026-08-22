import { useEffect, useRef, useState } from "react";
import { motion, useSpring, useTransform } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";

export default function PredictorGauge({
  probability = 0,
  size = 220,
  band = null,
}: {
  probability?: number;
  size?: number;
  band?: { range?: string; low?: number; high?: number } | null;
}) {
  const reduced = useReducedMotion();
  const [mounted, setMounted] = useState(false);
  const springVal = useSpring(0, { stiffness: 60, damping: 20 });
  const needleRotation = useTransform(springVal, [0, 100], [-135, 135]);

  useEffect(() => {
    setMounted(true);
    springVal.set(probability);
  }, [probability, springVal]);

  const radius = size / 2 - 16;
  const circumference = Math.PI * radius;
  const dashOffset = circumference - (probability / 100) * circumference;

  const getGradientColors = (pct) => {
    if (pct >= 80) return ["#10b981", "#34d399"];
    if (pct >= 60) return ["#f59e0b", "#fbbf24"];
    if (pct >= 40) return ["#f97316", "#fb923c"];
    return ["#ef4444", "#f87171"];
  };

  const [c1, c2] = getGradientColors(probability);

  return (
    <div className="relative flex items-center justify-center" style={{ width: size, height: size * 0.65 }}>
      <svg width={size} height={size * 0.65} viewBox={`0 0 ${size} ${size * 0.65}`}>
        <defs>
          <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#ef4444" />
            <stop offset="50%" stopColor="#f59e0b" />
            <stop offset="100%" stopColor="#10b981" />
          </linearGradient>
        </defs>

        {/* Background arc */}
        <path
          d={describeArc(size / 2, size * 0.6, radius, -180, 0)}
          fill="none"
          stroke="#e5e7eb"
          strokeWidth="12"
          strokeLinecap="round"
        />

        {/* Progress arc */}
        {mounted && (
          <motion.path
            d={describeArc(size / 2, size * 0.6, radius, -180, -180 + (probability / 100) * 180)}
            fill="none"
            stroke={`url(#gaugeGrad)`}
            strokeWidth="12"
            strokeLinecap="round"
            initial={reduced ? {} : { pathLength: 0, opacity: 0 }}
            animate={{ pathLength: 1, opacity: 1 }}
            transition={{ duration: 1.5, ease: "easeOut", delay: 0.3 }}
          />
        )}

        {/* Needle */}
        <motion.g
          style={{ originX: `${size / 2}px`, originY: `${size * 0.6}px`, rotate: needleRotation }}
        >
          <line
            x1={size / 2}
            y1={size * 0.6}
            x2={size / 2}
            y2={size * 0.6 - radius + 10}
            stroke="#374151"
            strokeWidth="3"
            strokeLinecap="round"
          />
          <circle cx={size / 2} cy={size * 0.6} r="6" fill="#374151" />
        </motion.g>
      </svg>

      {/* Center text */}
      <div className="absolute bottom-2 text-center">
        <motion.p
          className="text-3xl font-bold"
          style={{ color: c1 }}
          initial={reduced ? {} : { opacity: 0, scale: 0.5 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8, type: "spring", stiffness: 200 }}
        >
          {probability}%
        </motion.p>
        <p className="text-xs text-gray-500 dark:text-gray-400">Placement Probability</p>
        {band && (
          <p className="text-[11px] text-gray-400 dark:text-gray-500 mt-0.5">
            Range {band.range}
          </p>
        )}
      </div>
    </div>
  );
}

function describeArc(cx, cy, r, startAngle, endAngle) {
  const start = polarToCartesian(cx, cy, r, endAngle);
  const end = polarToCartesian(cx, cy, r, startAngle);
  const largeArcFlag = endAngle - startAngle <= 180 ? "0" : "1";
  return `M ${start.x} ${start.y} A ${r} ${r} 0 ${largeArcFlag} 0 ${end.x} ${end.y}`;
}

function polarToCartesian(cx, cy, r, angleDeg) {
  const rad = ((angleDeg - 90) * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}
