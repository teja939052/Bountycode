import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";

interface SuccessGlowProps {
  /** Increment this to trigger a fresh burst (a key, not a boolean toggle). */
  burst: number;
  /** Element position for the burst origin. Defaults to the viewport center. */
  anchorEl?: HTMLElement | null;
  color?: string;
}

/**
 * Variable-reward moment: a single soft glow burst that appears ONLY when the
 * caller fires a genuine success (correct answer, milestone, offer logged).
 * It is never ambient — the whole point is that it is earned, so it stays rare.
 */
export default function SuccessGlow({ burst, anchorEl, color = "#4F8F57" }: SuccessGlowProps) {
  const reduced = useReducedMotion();
  const [pos, setPos] = useState<{ x: number; y: number } | null>(null);

  useEffect(() => {
    if (!burst) return;
    let x = typeof window !== "undefined" ? window.innerWidth / 2 : 0;
    let y = typeof window !== "undefined" ? window.innerHeight / 2 : 0;
    if (anchorEl) {
      const r = anchorEl.getBoundingClientRect();
      x = r.left + r.width / 2;
      y = r.top + r.height / 2;
    }
    setPos({ x, y });
    const t = setTimeout(() => setPos(null), reduced ? 400 : 1100);
    return () => clearTimeout(t);
  }, [burst, anchorEl, reduced]);

  return (
    <AnimatePresence>
      {pos && (
        <motion.div
          key={burst}
          className="pointer-events-none fixed inset-0 z-[70]"
          style={{ transformOrigin: `${pos.x}px ${pos.y}px` }}
          initial={{ opacity: 0.85 }}
          animate={{ opacity: 0 }}
          exit={{ opacity: 0 }}
          transition={{ duration: reduced ? 0.3 : 0.9, ease: "easeOut" }}
        >
          <motion.div
            className="absolute rounded-full"
            style={{
              left: pos.x - 8,
              top: pos.y - 8,
              width: 16,
              height: 16,
              background: `radial-gradient(circle, ${color}55 0%, transparent 65%)`,
            }}
            initial={{ scale: 1 }}
            animate={{ scale: reduced ? 6 : 34 }}
            transition={{ duration: reduced ? 0.3 : 0.8, ease: [0.22, 1, 0.36, 1] }}
          />
          <motion.div
            className="absolute rounded-full border-2"
            style={{
              left: pos.x - 20,
              top: pos.y - 20,
              width: 40,
              height: 40,
              borderColor: `${color}66`,
            }}
            initial={{ scale: 0.5, opacity: 0.9 }}
            animate={{ scale: reduced ? 1.2 : 8, opacity: 0 }}
            transition={{ duration: reduced ? 0.3 : 0.75, ease: "easeOut" }}
          />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
