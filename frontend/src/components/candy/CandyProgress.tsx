import { motion } from "framer-motion";
import { candyGradient } from "./palette";
import type { CandyColor } from "./palette";

type Props = {
  value: number;
  max?: number;
  color?: CandyColor;
  size?: "sm" | "md";
  label?: string;
  className?: string;
  showPercent?: boolean;
};

export default function CandyProgress({
  value,
  max = 100,
  color = "strawberry",
  size = "md",
  label,
  className = "",
  showPercent = true,
}: Props) {
  const pct = Math.max(0, Math.min(100, (value / max) * 100));

  return (
    <div className={`w-full ${className}`}>
      {label && (
        <div className="mb-1.5 flex items-center justify-between font-mono text-[10px] font-bold uppercase tracking-[0.18em] text-text-primary/60">
          <span>{label}</span>
          {showPercent && (
            <span className="font-black text-text-primary">{Math.round(pct)}%</span>
          )}
        </div>
      )}
      <div
        className={`relative w-full overflow-hidden rounded-full bg-surface-2 shadow-inner ${
          size === "sm" ? "h-2.5" : "h-3.5"
        }`}
      >
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="candy-shimmer relative h-full rounded-full"
          style={{ background: candyGradient(color, 90) }}
        />
      </div>
    </div>
  );
}
