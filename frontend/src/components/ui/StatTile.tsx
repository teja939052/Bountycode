import type { ReactNode } from "react";
import AnimatedNumber from "../motion/AnimatedNumber";

interface StatTileProps {
  value: number;
  label: string;
  icon?: ReactNode;
  sub?: string;
  suffix?: string;
  accent?: "coral" | "teal" | "sky" | "lavender" | "gold";
  variant?: "dark" | "light";
  size?: "sm" | "lg";
  className?: string;
}

const ACCENTS = {
  coral: "text-brand-coral",
  teal: "text-brand-teal",
  sky: "text-brand-sky",
  lavender: "text-brand-lavender",
  gold: "text-brand-gold",
};

/**
 * A stat card where the number is the hero: big, friendly, count-up on load.
 * The label is a small muted caption underneath. Theme-aware via brand CSS
 * vars, so the same component works on the dark app surface and light cards.
 * `size="sm"` for compact 3-up grids, `size="lg"` for hero stats.
 */
export default function StatTile({
  value,
  label,
  icon,
  sub,
  suffix = "",
  accent = "coral",
  variant = "dark",
  size = "lg",
  className = "",
}: StatTileProps) {
  const a = ACCENTS[accent] || ACCENTS.coral;

  if (variant === "light") {
    return (
      <div className={`rounded-2xl bg-white border border-gray-100 shadow-card px-5 py-6 text-center transition-transform duration-150 hover:-translate-y-0.5 ${className}`}>
        <div className={`mb-2 flex items-center justify-center gap-1.5 ${a}`}>
          {icon}
          {sub && <span className="text-[10px] font-mono uppercase tracking-wider text-text-light">{sub}</span>}
        </div>
        <div className={`stat-numeral text-4xl ${a}`}>
          <AnimatedNumber value={value} />
          {suffix}
        </div>
        <div className="mt-1.5 text-[11px] font-medium text-text-light">{label}</div>
      </div>
    );
  }

  return (
    <div className={`rounded-2xl border border-brand-primary/10 bg-brand-primary/5 px-4 py-5 text-center transition-transform duration-150 hover:-translate-y-0.5 ${className}`}>
      <div className={`mb-1.5 flex items-center justify-center ${a}`}>
        {icon}
        {sub && <span className="ml-1.5 text-[9px] font-mono uppercase tracking-wider text-brand-dim">{sub}</span>}
      </div>
      <div className={`stat-numeral ${size === "sm" ? "text-2xl" : "text-4xl"} text-brand-primary`}>
        <AnimatedNumber value={value} />
        {suffix}
      </div>
      <div className="mt-1 text-[9px] font-mono uppercase tracking-wider text-brand-dim">{label}</div>
    </div>
  );
}
