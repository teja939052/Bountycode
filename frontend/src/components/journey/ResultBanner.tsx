import { useEffect } from "react";
import { motion } from "framer-motion";
import { useReducedMotion } from "framer-motion";

export default function ResultBanner({
  data,
  onDone,
}: {
  data: {
    diamonds: number;
    stars?: number;
    combo?: number;
    streakMult?: number;
    critical?: boolean;
    recovered?: boolean;
  };
  onDone: () => void;
}) {
  const reduceMotion = useReducedMotion();
  useEffect(() => {
    const t = window.setTimeout(onDone, reduceMotion ? 2500 : 2200);
    return () => window.clearTimeout(t);
  }, [onDone, reduceMotion]);
  const stars = data.stars ?? 0;
  return (
    <motion.div
      initial={reduceMotion ? false : { scale: 0.92, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0.96, opacity: 0 }}
      transition={{ type: "spring", stiffness: 260, damping: 22 }}
      className="fixed inset-x-0 bottom-24 z-50 mx-auto w-fit max-w-[92vw]"
      role="status"
      aria-label={`Level cleared: ${stars} stars, ${data.diamonds} Diamonds`}
    >
      <div className="rounded-2xl border border-accent-warm/40 bg-card px-5 py-4 text-center shadow-lg backdrop-blur">
        <div className="flex items-center justify-center gap-1 text-2xl" aria-hidden>
          {[1, 2, 3].map((i) => (
            <motion.span
              key={i}
              initial={reduceMotion ? false : { scale: 0, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ delay: reduceMotion ? 0 : 0.15 + i * 0.18, type: "spring", stiffness: 400, damping: 15 }}
            >
              {i <= stars ? "★" : "☆"}
            </motion.span>
          ))}
        </div>
        <p className="mt-1 text-2xl font-black text-accent-warm">+{data.diamonds} Diamonds</p>
        <div className="mt-1 flex items-center justify-center gap-3 text-[11px] font-mono text-muted">
          {data.combo != null && data.combo > 1 && <span>🔥 combo ×{data.combo}</span>}
          {data.streakMult != null && data.streakMult > 1 && <span>streak ×{data.streakMult}</span>}
          {data.critical && <span>💥 critical</span>}
        </div>
        {data.recovered && (
          <p className="mt-1 text-[11px] font-bold text-accent-secondary">Fought back · recovery counts</p>
        )}
        <button onClick={onDone} className="mt-2 min-h-[44px] w-full rounded-xl bg-accent-primary py-2 text-sm font-bold text-white">
          Continue sailing
        </button>
      </div>
    </motion.div>
  );
}
