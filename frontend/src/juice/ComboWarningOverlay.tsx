import { motion, AnimatePresence } from 'framer-motion';
import useReducedMotion from "../hooks/useReducedMotion";

export default function ComboWarningOverlay({ seconds = 0, visible = true }) {
  const reduced = useReducedMotion();
  if (!visible || seconds > 15) return null;

  const urgency = seconds <= 5 ? 'critical' : seconds <= 10 ? 'warning' : 'info';
  const colors = {
    critical: { border: 'rgba(239,68,68,0.6)', bg: 'rgba(239,68,68,0.1)', text: '#fca5a5', pulse: '#ef4444' },
    warning: { border: 'rgba(245,158,11,0.5)', bg: 'rgba(245,158,11,0.1)', text: '#fcd34d', pulse: '#f59e0b' },
    info: { border: 'rgba(59,130,246,0.4)', bg: 'rgba(59,130,246,0.1)', text: '#93c5fd', pulse: '#3b82f6' },
  };
  const c = colors[urgency];

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed top-20 left-1/2 -translate-x-1/2 z-50"
          initial={reduced ? { opacity: 0 } : { opacity: 0, y: -20, scale: 0.9 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: -20 }}
        >
          <div className="px-6 py-3 rounded-2xl border-2 backdrop-blur-md flex items-center gap-3"
            style={{
              borderColor: c.border,
              backgroundColor: c.bg,
              boxShadow: `0 0 30px ${c.border}`,
            }}>
            <motion.div
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: c.pulse }}
              animate={reduced ? {} : { scale: [1, 1.5, 1], opacity: [1, 0.5, 1] }}
              transition={{ duration: 1, repeat: Infinity }}
            />
            <div>
              <div className="text-xs font-mono uppercase tracking-widest" style={{ color: c.text }}>
                Combo Decay in {seconds}s
              </div>
              <div className="text-sm font-bold text-white">
                Keep the streak alive!
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
