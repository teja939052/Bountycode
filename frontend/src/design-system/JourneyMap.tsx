import type { ReactNode } from "react";
import { TreasureBadge } from "./Progress";

/**
 * JourneyMap primitives — IslandNode + BountyCard.
 * The Bounty Map is the signature visual: a dotted journey path
 * with island nodes (topics), boss nodes (assessments), treasure seals.
 */

export type NodeState = "locked" | "available" | "in_progress" | "completed" | "boss" | "boss_cleared";

export interface IslandNodeProps {
  state: NodeState;
  title: string;
  /** 0–100 mastery within this node */
  mastery?: number;
  icon?: ReactNode;
  isBoss?: boolean;
  onClick?: () => void;
  className?: string;
}

const STATE_RING: Record<NodeState, string> = {
  locked: "#DCE8DE",
  available: "#22C55E",
  in_progress: "#5BA7A0",
  completed: "#EAB74D",
  boss: "#E96A5B",
  boss_cleared: "#EAB74D",
};

export function IslandNode({
  state,
  title,
  mastery = 0,
  icon,
  isBoss = false,
  onClick,
  className = "",
}: IslandNodeProps) {
  const ringColor = STATE_RING[state];
  const isLocked = state === "locked";
  const isDone = state === "completed" || state === "boss_cleared";

  return (
    <button
      type="button"
      onClick={isLocked ? undefined : onClick}
      disabled={isLocked}
      aria-label={`${title}${isLocked ? " (locked)" : ""}`}
      className={`group relative flex flex-col items-center gap-2 outline-none ${className} ${
        isLocked ? "cursor-not-allowed opacity-60" : "cursor-pointer"
      }`}
    >
      {/* Island */}
      <div
        className={`relative flex items-center justify-center rounded-full transition-all duration-200 ${
          isBoss ? "h-[72px] w-[72px]" : "h-16 w-16"
        }`}
        style={{
          backgroundColor: isLocked ? "#F0F7F1" : isBoss ? "#FDEDEC" : "#FFFFFF",
          border: `3px solid ${ringColor}`,
          boxShadow:
            state === "available" || state === "boss"
              ? `0 0 0 6px ${ringColor}1A`
              : "0 1px 4px rgba(17,33,27,0.08)",
        }}
      >
        {isDone ? (
          <TreasureBadge size={32} />
        ) : icon ? (
          <span className={isLocked ? "text-text-muted/50" : ""}>{icon}</span>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            {isBoss ? (
              <path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4-6 4 1.5-7.5L2 9h7l3-7z" fill={STATE_RING[state]} />
            ) : (
              <circle cx="12" cy="12" r="8" fill={ringColor} opacity="0.85" />
            )}
          </svg>
        )}
        {/* In-progress pulse */}
        {state === "in_progress" && (
          <span
            className="absolute -right-1 -top-1 h-4 w-4 rounded-full border-2 border-white"
            style={{ backgroundColor: "#5BA7A0" }}
          />
        )}
      </div>
      {/* Label + mastery */}
      <div className="max-w-[120px] text-center">
        {title && <p className="text-xs font-bold leading-tight text-text">{title}</p>}
        {!isLocked && !isDone && mastery > 0 && (
          <div className="mt-1 h-1 w-full overflow-hidden rounded-full bg-mint">
            <div
              className="h-full rounded-full transition-all duration-500"
              style={{ width: `${mastery}%`, backgroundColor: ringColor }}
            />
          </div>
        )}
        {isLocked && <p className="mt-0.5 text-[10px] font-medium text-text-muted">Complete previous</p>}
      </div>
    </button>
  );
}

/** Dotted connector between nodes on the map. */
export function PathConnector({ progress = 0, className = "" }: { progress?: number; className?: string }) {
  return (
    <div className={`relative mx-auto h-10 w-1 overflow-hidden rounded-full bg-border ${className}`}>
      <div
        className="absolute left-0 top-0 w-full rounded-full bg-ocean transition-all duration-500"
        style={{ height: `${Math.max(0, Math.min(100, progress))}%` }}
      />
    </div>
  );
}

export interface BountyCardProps {
  title: string;
  subtitle?: string;
  difficulty?: "Easy" | "Medium" | "Hard" | "Boss";
  /** e.g. "Arrays", "Hash Maps" */
  topics?: string[];
  /** XP reward */
  reward?: number;
  mastery?: number;
  state?: Extract<NodeState, "locked" | "available" | "in_progress" | "completed">;
  onStart?: () => void;
  actionLabel?: string;
  children?: ReactNode;
  className?: string;
}

const DIFF_STYLE: Record<string, { bg: string; color: string }> = {
  Easy: { bg: "#DCFCE7", color: "#15803D" },
  Medium: { bg: "#FFF3D0", color: "#8a6414" },
  Hard: { bg: "#FDEDEC", color: "#C2410C" },
  Boss: { bg: "#E96A5B", color: "#FFFFFF" },
};

export function BountyCard({
  title,
  subtitle,
  difficulty,
  topics = [],
  reward,
  mastery = 0,
  state = "available",
  onStart,
  actionLabel = "Start Bounty",
  children,
  className = "",
}: BountyCardProps) {
  const diff = difficulty ? DIFF_STYLE[difficulty] : undefined;
  const isLocked = state === "locked";
  const isDone = state === "completed";

  return (
    <div className={`bounty-card p-5 ${className}`}>
      <div className="relative flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="mb-1.5 flex flex-wrap items-center gap-2">
            {difficulty && diff && (
              <span
                className="rounded-md px-2 py-0.5 text-[11px] font-bold uppercase tracking-wide"
                style={{ backgroundColor: diff.bg, color: diff.color }}
              >
                {difficulty}
              </span>
            )}
            {topics.slice(0, 3).map((t) => (
              <span key={t} className="badge-ocean badge">
                {t}
              </span>
            ))}
          </div>
          <h3 className="font-display truncate text-base font-extrabold text-text">{title}</h3>
          {subtitle && <p className="mt-0.5 line-clamp-2 text-xs text-text-muted">{subtitle}</p>}
        </div>
        {isDone && <TreasureBadge size={36} />}
        {reward != null && !isDone && (
          <div className="shrink-0 text-right">
            <p className="text-[10px] font-bold uppercase tracking-wider text-wood">Bounty</p>
            <p className="font-display text-lg font-extrabold leading-none text-reward">+{reward}</p>
            <p className="text-[10px] font-semibold text-text-muted">XP</p>
          </div>
        )}
      </div>

      {children && <div className="relative mt-3">{children}</div>}

      {mastery > 0 && (
        <div className="relative mt-3">
          <div className="mb-1 flex justify-between text-[11px] font-medium text-text-muted">
            <span>Mastery</span>
            <span>{Math.round(mastery)}%</span>
          </div>
          <div className="h-1.5 overflow-hidden rounded-full bg-white/70">
            <div
              className="h-full rounded-full bg-primary transition-all duration-500"
              style={{ width: `${mastery}%` }}
            />
          </div>
        </div>
      )}

      {onStart && !isLocked && (
        <button
          type="button"
          onClick={onStart}
          className={`btn mt-4 w-full ${isDone ? "btn-outline" : "btn-primary"}`}
        >
          {isDone ? "Practice Again" : actionLabel}
        </button>
      )}
    </div>
  );
}
