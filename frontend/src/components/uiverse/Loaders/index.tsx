// @ts-nocheck
import { motion } from "framer-motion";

export function OrbitLoader({ size = 48, color = "#38bdf8" }: { size?: number; color?: string }) {
  return (
    <div className="relative" style={{ width: size, height: size }}>
      <motion.div
        className="absolute inset-0 rounded-full border-2 border-transparent"
        style={{ borderTopColor: color, borderRightColor: color }}
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      />
      <motion.div
        className="absolute inset-1 rounded-full border-2 border-transparent"
        style={{ borderBottomColor: color, borderLeftColor: color }}
        animate={{ rotate: -360 }}
        transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
      />
    </div>
  );
}

export function DotWaveLoader({ dots = 5, color = "#38bdf8" }: { dots?: number; color?: string }) {
  return (
    <div className="flex items-center gap-1.5">
      {Array.from({ length: dots }).map((_, i) => (
        <motion.div
          key={i}
          className="h-2.5 w-2.5 rounded-full"
          style={{ backgroundColor: color }}
          animate={{ y: [0, -10, 0] }}
          transition={{ duration: 0.6, repeat: Infinity, delay: i * 0.1 }}
        />
      ))}
    </div>
  );
}

export function PulseLoader({ color = "#38bdf8" }: { color?: string }) {
  return (
    <motion.div
      className="rounded-full"
      style={{ width: 40, height: 40, backgroundColor: color }}
      animate={{ scale: [0.8, 1.2, 0.8], opacity: [0.6, 1, 0.6] }}
      transition={{ duration: 1.2, repeat: Infinity }}
    />
  );
}

export function SkeletonBlock({ width = "100%", height = 16, radius = 8 }: { width?: string; height?: number; radius?: number }) {
  return (
    <div
      className="w-full overflow-hidden rounded-md bg-gradient-to-r from-black/5 via-black/10 to-black/5"
      style={{ width, height, borderRadius: radius }}
    >
      <motion.div
        className="h-full w-full"
        animate={{ x: ["-100%", "100%"] }}
        transition={{ duration: 1.6, repeat: Infinity, ease: "linear" }}
        style={{ background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent)" }}
      />
    </div>
  );
}
