import { ReactNode } from "react";
import { colors, radii, shadows, motion, spacing, typography } from "..";

interface AchievementProps {
  title: string;
  description?: string;
  icon?: ReactNode;
  rarity?: "common" | "uncommon" | "rare" | "epic" | "legendary";
  unlocked?: boolean;
  unlockedAt?: string;
  progress?: number;
  maxProgress?: number;
  xpReward?: number;
  onClick?: () => void;
  className?: string;
}

const rarityStyles: Record<AchievementProps["rarity"], { bg: string; border: string; glow: string; text: string }> = {
  common: {
    bg: colors.background.surfaceSecondary,
    border: colors.border.primary,
    glow: "none",
    text: colors.text.primary,
  },
  uncommon: {
    bg: "rgba(59,130,246,0.05)",
    border: colors.semantic.info,
    glow: `0 0 15px rgba(59,130,246,0.15)`,
    text: colors.semantic.info,
  },
  rare: {
    bg: "rgba(139,92,246,0.05)",
    border: colors.semantic.rare,
    glow: `0 0 15px rgba(139,92,246,0.15)`,
    text: colors.semantic.rare,
  },
  epic: {
    bg: "rgba(236,72,153,0.05)",
    border: colors.semantic.rare,
    glow: `0 0 20px rgba(236,72,153,0_2)`,
    text: "#EC4899",
  },
  legendary: {
    bg: "linear-gradient(135deg, rgba(234,179,8,0.1) 0%, rgba(245,158,11,0.1) 100%)",
    border: colors.semantic.achievement,
    glow: `0 0 25px rgba(234,179,8,0.25)`,
    text: colors.semantic.achievement,
  },
};

export function Achievement({
  title,
  description,
  icon,
  rarity = "common",
  unlocked = false,
  unlockedAt,
  progress,
  maxProgress = 100,
  xpReward,
  onClick,
  className = "",
}: AchievementProps) {
  const style = rarityStyles[rarity];
  const isUnlocked = unlocked || (progress !== undefined && progress >= maxProgress);

  return (
    <article
      className={`
        relative group rounded-${radii.card} p-5 transition-all duration-300
        border cursor-pointer
        ${unlocked ? "hover:shadow-glow hover:border-brand-primary/50" : "opacity-60 hover:opacity-80"}
        ${className}
      `}
      style={{
        background: style.bg,
        borderColor: style.border,
        boxShadow: style.glow,
      }}
      onClick={onClick}
    >
      <div className="flex items-start gap-4">
        <div
          className={`
            flex-shrink-0 w-16 h-16 rounded-${radii.lg} flex items-center justify-center relative overflow-hidden
            ${unlocked ? "" : "grayscale opacity-50"}
          `}
          style={{
            background: isUnlocked
              ? `linear-gradient(135deg, ${style.border}15 0%, ${style.border}05 100%)`
              : colors.background.surfaceSecondary,
            border: `1px solid ${style.border}`,
          }}
        >
          {icon || (
            <svg
              width="32"
              height="32"
              viewBox="0 0 24 24"
              fill="none"
              stroke={isUnlocked ? "currentColor" : colors.text.dim}
              strokeWidth={isUnlocked ? 2 : 1.5}
              strokeLinecap="round"
              strokeLinejoin="round"
              className={`
                transition-colors duration-300
                ${isUnlocked ? `text-${rarity === "legendary" ? "achievement" : rarity === "epic" ? "rare" : rarity === "rare" ? "rare" : rarity === "uncommon" ? "info" : "primary"}` : "text-text-dim"}
              `}
            >
              {rarity === "legendary" && (
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 12 9.27 2.91 8.26 9 2 12z" />
              )}
              {rarity === "epic" && (
                <>
                  <circle cx="12" cy="12" r="10" />
                  <path d="M12 6v6l4 2" />
                </>
              )}
              {rarity === "rare" && (
                <>
                  <path d="M12 2L2 7l10 5 10-5-10-5z" />
                  <path d="M2 17l10 5 10-5" />
                  <path d="M2 12l10 5 10-5" />
                </>
              )}
              {rarity === "uncommon" && (
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l5-4.87L12 2z" />
              )}
              {rarity === "common" && (
                <circle cx="12" cy="12" r="10" />
              )}
            </svg>
          )}

          {!unlocked && progress !== undefined && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/50 rounded-lg">
              <span className="text-sm font-bold text-white">
                {Math.round((progress / maxProgress) * 100)}%
              </span>
            </div>
          )}

          {isUnlocked && (
            <div className="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-success flex items-center justify-center">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="3">
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
          )}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1.5">
            <h3 className={`
              font-display font-semibold text-lg truncate
              ${unlocked ? "text-text-primary" : "text-text-secondary"}
            `}>
              {title}
              {xpReward && (
                <span className="ml-2 inline-flex items-center gap-1 text-xs font-mono text-xp font-semibold">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 12 9.27 2.91 8.26 9 2 12z" />
                  </svg>
                  +{xpReward}
                </span>
              )}
            </h3>
            <div className="flex items-center gap-2">
              <span className={`
                px-2 py-0.5 rounded-${radii.badge} text-xs font-medium uppercase tracking-wider
                ${rarity === "legendary" ? "bg-achievement/10 text-achievement" : ""}
                ${rarity === "epic" ? "bg-rare/10 text-rare" : ""}
                ${rarity === "rare" ? "bg-rare/10 text-rare" : ""}
                ${rarity === "uncommon" ? "bg-info/10 text-info" : ""}
                ${rarity === "common" ? "bg-border-primary/10 text-text-secondary" : ""}
              `}>
                {rarity}
              </span>
              {!unlocked && progress !== undefined && (
                <span className="text-xs font-mono text-text-dim">
                  {Math.round((progress / maxProgress) * 100)}%
                </span>
              )}
            </div>
          </div>

          {description && (
            <p className="mt-2 text-sm text-text-secondary">{description}</p>
          )}

          {unlockedAt && (
            <p className="mt-3 text-xs font-mono text-text-dim flex items-center gap-1">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
              </svg>
              Unlocked {unlockedAt}
            </p>
          )}

          {!unlocked && progress !== undefined && (
            <div className="mt-3">
              <ProgressBar
                value={progress}
                max={maxProgress}
                size="sm"
                color={rarity === "legendary" ? "achievement" : rarity === "epic" ? "rare" : rarity === "rare" ? "rare" : rarity === "uncommon" ? "info" : "primary"}
                showLabel
              />
            </div>
          )}
        </div>
      </div>

      {unlocked && (
        <div className="absolute top-2 right-2 w-8 h-8 rounded-full bg-success/20 flex items-center justify-center">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke={colors.semantic.success} strokeWidth="2.5">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        </div>
      )}
    </article>
  );
}

interface AchievementGridProps {
  achievements: AchievementProps[];
  columns?: { sm?: number; md?: number; lg?: number };
  className?: string;
}

export function AchievementGrid({
  achievements,
  columns = { sm: 1, md: 2, lg: 3 },
  className = "",
}: AchievementGridProps) {
  return (
    <div
      className={`
        grid gap-4
        grid-cols-${columns.sm}
        sm:grid-cols-${columns.md}
        lg:grid-cols-${columns.lg}
        ${className}
      `}
    >
      {achievements.map((achievement) => (
        <Achievement key={achievement.title} {...achievement} />
      ))}
    </div>
  );
}