import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";

export default function ComboCounter({ combo = 0, multiplier = 1, visible = true }) {
  const reduced = useReducedMotion();
  if (!visible || combo < 2) return null;

  const label = combo >= 20 ? "GODLIKE" : combo >= 12 ? "UNSTOPPABLE" : combo >= 8 ? "INCREDIBLE" : combo >= 5 ? "ON FIRE" : "COMBO";

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed top-6 left-1/2 -translate-x-1/2 z-50"
          initial={reduced ? { opacity: 0 } : { opacity: 0, y: -30, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={reduced ? { opacity: 0 } : { opacity: 0, y: -30, scale: 0.8 }}
          transition={{ type: "spring", stiffness: 300, damping: 20 }}
        >
          <div
            className="px-6 py-3 rounded-full border-2 shadow-2xl flex items-center gap-3"
            style={{
              background: "linear-gradient(135deg, rgba(99,102,241,0.95), rgba(236,72,153,0.95))",
              borderColor: "rgba(255,255,255,0.3)",
              boxShadow: "0 0 30px rgba(99,102,241,0.6), 0 0 60px rgba(236,72,153,0.3)",
            }}
          >
            <motion.span
              className="text-2xl"
              animate={reduced ? {} : { scale: [1, 1.3, 1], rotate: [0, -10, 10, 0] }}
              transition={{ duration: 0.6, repeat: Infinity, repeatDelay: 0.5 }}
            >
              ⚡
            </motion.span>
            <div className="text-center">
              <div className="text-xs font-mono uppercase tracking-widest text-white/70">{label}</div>
              <div className="text-2xl font-black text-white leading-none">{combo}x</div>
            </div>
            <div className="text-right">
              <div className="text-[10px] font-mono text-white/70">MULTIPLIER</div>
              <div className="text-lg font-bold text-yellow-300">x{multiplier.toFixed(2)}</div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
