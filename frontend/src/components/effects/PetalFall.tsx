import { useEffect, useRef, useState } from "react";
import { motion, useReducedMotion } from "framer-motion";

type Petal = {
  id: number;
  left: number;
  delay: number;
  duration: number;
  size: number;
  sway: number;
  opacity: number;
  swayDir: number;
};

const PETAL_COUNT = 12;

function random(min: number, max: number) {
  return Math.random() * (max - min) + min;
}

export default function PetalFall() {
  const reducedMotion = useReducedMotion();
  const [petals, setPetals] = useState<Petal[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (reducedMotion) return;
    const items: Petal[] = Array.from({ length: PETAL_COUNT }, (_, i) => ({
      id: i,
      left: random(0, 100),
      delay: random(0, 10),
      duration: random(12, 24),
      size: random(6, 14),
      sway: random(20, 80),
      opacity: random(0.25, 0.7),
      swayDir: Math.random() > 0.5 ? 1 : -1,
    }));
    setPetals(items);
  }, [reducedMotion]);

  if (reducedMotion || petals.length === 0) return null;

  return (
    <div
      ref={containerRef}
      className="pointer-events-none fixed inset-0 z-[60] overflow-hidden"
      aria-hidden="true"
    >
      {petals.map((p) => (
        <motion.div
          key={p.id}
          className="absolute top-[-20px] rounded-full"
          style={{
            left: `${p.left}%`,
            width: p.size,
            height: p.size * 0.6,
            background:
              "radial-gradient(circle at 30% 30%, rgba(255,255,255,0.9), rgba(255,183,178,0.7))",
            boxShadow: "0 0 4px rgba(255,183,178,0.4)",
            opacity: p.opacity,
          }}
          animate={{
            y: ["0vh", "105vh"],
            x: [0, p.sway * p.swayDir, -p.sway * 0.5, 0],
            rotate: [0, 180, 360],
            scale: [1, 1.1, 0.95, 1],
          }}
          transition={{
            duration: p.duration,
            delay: p.delay,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      ))}
    </div>
  );
}
