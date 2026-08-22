import { ReactNode } from "react";
import { colors, radii, shadows, motion, spacing } from "..";

interface QuestCardProps {
  title: string;
  description?: string;
  status: "available" | "active" | "completed" | "locked";
  type?: "main" | "side" | "daily" | "boss";
  progress?: number;
  maxProgress?: number;
  xpReward?: number;
  icon?: ReactNode;
  tags?: string[];
  onClick?: () => void;
  className?: string;
  children?: ReactNode;
}

const typeStyles: Record<QuestCardProps["type"], string> = {
  main: `border-l-4 border-brand-primary`,
  side: `border-l-4 border-info`,
  daily: `border-l-4 border-xp`,
  boss: `border-l-4 border-boss`,
};

const statusStyles: Record<QuestCardProps["status"], string> = {
  available: `bg-background-surfaceSecondary border-border-primary`,
  active: `bg-brand-mint/30 border-brand-primary/30 ring-1 ring-brand-primary/20`,
  completed: `bg-success/5 border-success/30`,
  locked: `bg-background-surfaceSecondary/50 border-border-primary/50 opacity-60`,
};

function getIcon(status: QuestCardProps["status"], icon?: ReactNode) {
  if (icon) return icon;
  return (
    <svg
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {status === "completed" && <polyline points="20 6 9 17 4 12" />}
      {status === "active" && <circle cx="12" cy="12" r="8" />}
      {status === "locked" && (
        <>
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
          <path d="M7 11V7a5 5 0 0 1 10 0v4" />
        </>
      )}
      {status === "available" && (
        <>
          <path d="M9 11l3 3L22 4" />
          <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7" />
        </>
      )}
    </svg>
  );
}

function getIconBg(status: QuestCardProps["status"]) {
  switch (status) {
    case "completed":
      return "bg-success text-white";
    case "active":
      return "bg-brand-primary text-white animate-pulse";
    case "locked":
      return "bg-background-secondary text-text-dim";
    case "available":
    default:
      return "bg-brand-mint text-brand-deep";
  }
}

export function QuestCard({
  title,
  description,
  status = "available",
  type = "main",
  progress,
  maxProgress = 100,
  xpReward,
  icon,
  tags = [],
  onClick,
  className = "",
  children,
}: QuestCardProps) {
  return (
    <article
      className={`
        relative group rounded-${radii.card} p-5 transition-all duration-300
        ${typeStyles[type]}
        ${statusStyles[status]}
        ${onClick ? "cursor-pointer hover:shadow-glow hover:border-brand-primary/50" : ""}
        ${className}
      `}
      onClick={onClick}
    >
      <div className="flex items-start gap-3">
        <div
          className={`
            flex-shrink-0 w-12 h-12 rounded-${radii.md} flex items-center justify-center
            ${getIconBg(status)}
          `}
        >
          {getIcon(status, icon)}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between gap-2 mb-1.5">
            <h3
              className={`
                font-display font-semibold text-lg truncate
                ${status === "completed" ? "text-text-primary" : ""}
                ${status === "active" ? "text-brand-primary" : ""}
                ${status === "locked" ? "text-text-dim" : "text-text-primary"}
              `}
            >
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
            {description && (
              <p className="text-sm text-text-secondary line-clamp-2">{description}</p>
            )}
          </div>

          {(progress !== undefined || tags.length > 0) && (
            <div className="mt-4 flex items-center gap-3 flex-wrap">
              {progress !== undefined && (
                <div className="flex-1 min-w-[120px]">
                  <ProgressBar
                    value={progress}
                    max={maxProgress}
                    size="sm"
                    color={type === "boss" ? "boss" : "primary"}
                    showLabel
                  />
                </div>
              )}
              {tags.map((tag) => (
                <span
                  key={tag}
                  className={`
                    px-2 py-0.5 rounded-${radii.badge} text-xs font-medium
                    ${tag === "main" ? "bg-brand-mint text-brand-deep" : ""}
                    ${tag === "side" ? "bg-info/10 text-info" : ""}
                    ${tag === "daily" ? "bg-xp/10 text-xp" : ""}
                    ${tag === "boss" ? "bg-boss/10 text-boss" : ""}
                    ${tag === "new" ? "bg-success/10 text-success" : ""}
                  `}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {children && <div className="mt-4">{children}</div>}
        </div>
      </div>

      {status === "active" && (
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-brand-primary to-brand-tertiary rounded-b-lg" />
      )}
    </article>
  );
}

interface QuestChainProps {
  quests: QuestCardProps[];
  orientation?: "vertical" | "horizontal";
  className?: string;
}

export function QuestChain({
  quests,
  orientation = "vertical",
  className = "",
}: QuestChainProps) {
  return (
    <div className={`relative ${className}`}>
      {orientation === "vertical" && (
        <div className="absolute left-6 top-0 bottom-0 w-px bg-gradient-to-b from-border-primary to-transparent" />
      )}
      <div className={orientation === "horizontal" ? "flex gap-4 overflow-x-auto pb-4" : "space-y-4"}>
        {quests.map((quest, idx) => (
          <div key={quest.title} className={orientation === "horizontal" ? "flex-shrink-0 w-80" : ""}>
            {orientation === "vertical" && idx > 0 && (
              <div className="absolute left-5 top-0 bottom-0 w-px bg-gradient-to-b from-transparent via-border-primary to-transparent" />
            )}
            <QuestCard {...quest} />
          </div>
        ))}
      </div>
    </div>
  );
}