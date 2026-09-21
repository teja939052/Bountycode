import { motion } from "framer-motion";

export type BadgeRarity = "common" | "uncommon" | "rare" | "epic" | "legendary";

const RARITY_COLORS: Record<BadgeRarity, { border: string; glow: string; bg: string; text: string; ring: string }> = {
  common:    { border: "#9CA3AF", glow: "rgba(156,163,175,0.25)",  bg: "rgba(156,163,175,0.08)",  text: "#D1D5DB", ring: "#9CA3AF" },
  uncommon:  { border: "#22C55E", glow: "rgba(34,197,94,0.25)",   bg: "rgba(34,197,94,0.08)",   text: "#4ADE80", ring: "#22C55E" },
  rare:      { border: "#8B6BD9", glow: "rgba(139,107,217,0.3)",  bg: "rgba(139,107,217,0.1)",  text: "#A78BFA", ring: "#8B6BD9" },
  epic:      { border: "#EC4899", glow: "rgba(236,72,153,0.3)",   bg: "rgba(236,72,153,0.1)",   text: "#F472B6", ring: "#EC4899" },
  legendary: { border: "#EAB74D", glow: "rgba(234,183,77,0.35)",  bg: "linear-gradient(135deg, rgba(234,183,77,0.15), rgba(245,158,11,0.15))", text: "#FCD34D", ring: "#EAB74D" },
};

export interface BadgeCardProps {
  name: string;
  description?: string;
  icon?: string;
  rarity?: BadgeRarity;
  unlocked?: boolean;
  progress?: number;
  maxProgress?: number;
  onClick?: () => void;
  className?: string;
  compact?: boolean;
}

export default function BadgeCard({
  name,
  description,
  icon = "🏆",
  rarity = "common",
  unlocked = true,
  progress,
  maxProgress = 100,
  onClick,
  className = "",
  compact = false,
}: BadgeCardProps) {
  const style = RARITY_COLORS[rarity];
  const isComplete = unlocked || (progress !== undefined && progress >= maxProgress);
  const pct = progress !== undefined ? Math.min(100, Math.round((progress / maxProgress) * 100)) : (isComplete ? 100 : 0);

  if (compact) {
    return (
      <motion.div
        className={`
          relative overflow-hidden rounded-xl cursor-pointer border
          transition-all duration-300 shrink-0
          ${isComplete ? "" : "opacity-60"}
          ${className}
        `}
        style={{
          width: 64,
          background: style.bg,
          borderColor: style.border,
          boxShadow: isComplete ? style.glow : "none",
        }}
        onClick={onClick}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        title={name}
      >
        <div className="flex flex-col items-center justify-center gap-1 py-2.5 px-2">
          <div className="relative">
            <span className="text-xl filter drop-shadow-sm">{isComplete ? icon : "🔒"}</span>
            {isComplete && (
              <div className="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full flex items-center justify-center" style={{ background: style.border }}>
                <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="4">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              </div>
            )}
          </div>
          <span className="text-[9px] font-bold text-center leading-tight line-clamp-2 px-0.5" style={{ color: style.text }}>
            {name}
          </span>
        </div>
      </motion.div>
    );
  }

  return (
    <motion.article
      className={`
        relative overflow-hidden rounded-2xl p-4 cursor-pointer
        border transition-all duration-300 group
        ${isComplete ? "hover:shadow-lg" : "opacity-60"}
        ${className}
      `}
      style={{
        background: style.bg,
        borderColor: style.border,
        boxShadow: isComplete ? style.glow : "none",
      }}
      onClick={onClick}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      layout
    >
      {/* Rarity accent line */}
      <div className="absolute top-0 left-0 right-0 h-[2px]" style={{ background: `linear-gradient(90deg, transparent, ${style.border}, transparent)` }} />

      <div className="flex items-start gap-3">
        {/* Icon */}
        <div className="relative shrink-0">
          <div
            className="w-12 h-12 rounded-xl flex items-center justify-center text-xl"
            style={{
              background: isComplete ? `linear-gradient(135deg, ${style.border}20, ${style.border}05)` : "rgba(100,100,120,0.1)",
              border: `1px solid ${isComplete ? style.border : "rgba(100,100,120,0.2)"}`,
            }}
          >
            {isComplete ? (
              <span aria-hidden="true" className="text-2xl filter drop-shadow-sm">{icon}</span>
            ) : (
              <span className="text-lg grayscale opacity-40">{icon}</span>
            )}
          </div>
          {isComplete && (
            <div className="absolute -top-1 -right-1 w-5 h-5 rounded-full flex items-center justify-center" style={{ background: style.border }}>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="4">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
          )}
        </div>

        {/* Text */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2">
            <h3 className={`text-sm font-display font-bold truncate ${isComplete ? "text-text-primary" : "text-text-secondary"}`}>
              {name}
            </h3>
            <span className="shrink-0 text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded-full" style={{ background: `${style.border}15`, color: style.text }}>
              {rarity}
            </span>
          </div>
          {description && (
            <p className="mt-1 text-xs text-text-secondary line-clamp-2">{description}</p>
          )}

          {/* Progress bar for locked badges */}
          {!isComplete && progress !== undefined && (
            <div className="mt-2">
              <div className="flex items-center justify-between mb-1">
                <span className="text-[10px] font-mono text-text-dim">{pct}%</span>
                <span className="text-[10px] font-mono text-text-dim">{progress}/{maxProgress}</span>
              </div>
              <div className="h-1.5 rounded-full bg-gray-200 dark:bg-gray-700 overflow-hidden">
                <motion.div className="h-full rounded-full" style={{ background: style.border }} initial={{ width: 0 }} animate={{ width: `${pct}%` }} transition={{ duration: 0.8, ease: "easeOut" }} />
              </div>
            </div>
          )}
        </div>
      </div>
    </motion.article>
  );
}
