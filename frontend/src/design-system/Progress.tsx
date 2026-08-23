/**
 * Progress primitives — MasteryBar, ReadinessRing, TreasureBadge.
 * Real data only: these components always render actual progress.
 */

interface MasteryBarProps {
  /** 0–100 */
  value: number;
  label?: string;
  /** color key from the design system */
  tone?: "primary" | "gold" | "ocean" | "tech" | "coral" | "rare";
  size?: "sm" | "md";
  showValue?: boolean;
  className?: string;
}

const TONE_BG: Record<string, string> = {
  primary: "#22C55E",
  gold: "#EAB74D",
  ocean: "#5BA7A0",
  tech: "#4A90E2",
  coral: "#E96A5B",
  rare: "#8B6BD9",
};

export function MasteryBar({
  value,
  label,
  tone = "primary",
  size = "md",
  showValue = true,
  className = "",
}: MasteryBarProps) {
  const clamped = Math.max(0, Math.min(100, Math.round(value)));
  return (
    <div className={className}>
      {(label || showValue) && (
        <div className="mb-1 flex items-center justify-between text-xs">
          {label && <span className="font-medium text-text-muted">{label}</span>}
          {showValue && <span className="font-bold text-text">{clamped}%</span>}
        </div>
      )}
      <div
        className={`overflow-hidden rounded-full bg-mint ${size === "sm" ? "h-1.5" : "h-2.5"}`}
        role="progressbar"
        aria-valuenow={clamped}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label || "mastery"}
      >
        <div
          className="h-full rounded-full transition-all duration-500 ease-out"
          style={{ width: `${clamped}%`, backgroundColor: TONE_BG[tone] }}
        />
      </div>
    </div>
  );
}

interface ReadinessRingProps {
  /** 0–100 */
  value: number;
  size?: number;
  strokeWidth?: number;
  label?: string;
  className?: string;
}

/** Circular readiness gauge — the signature progress visual. */
export function ReadinessRing({
  value,
  size = 96,
  strokeWidth = 8,
  label = "ready",
  className = "",
}: ReadinessRingProps) {
  const clamped = Math.max(0, Math.min(100, Math.round(value)));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - clamped / 100);

  // Color escalates with readiness
  const color =
    clamped >= 80 ? "#22C55E" : clamped >= 50 ? "#5BA7A0" : clamped >= 25 ? "#EAB74D" : "#E96A5B";

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="#EAF7ED"
          strokeWidth={strokeWidth}
          fill="none"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          fill="none"
          style={{ transition: "stroke-dashoffset 700ms ease-out, stroke 300ms ease" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-display font-extrabold leading-none text-text" style={{ fontSize: size * 0.24 }}>
          {clamped}%
        </span>
        {label && (
          <span className="mt-0.5 text-[10px] font-bold uppercase tracking-wider text-text-muted">
            {label}
          </span>
        )}
      </div>
    </div>
  );
}

interface TreasureBadgeProps {
  size?: number;
  icon?: React.ReactNode;
  className?: string;
}

/** Gold seal for completed nodes/achievements. */
export function TreasureBadge({ size = 40, icon, className = "" }: TreasureBadgeProps) {
  return (
    <div
      className={`treasure-seal shrink-0 ${className}`}
      style={{ width: size, height: size }}
      aria-hidden="true"
    >
      {icon || (
        <svg width={size * 0.5} height={size * 0.5} viewBox="0 0 24 24" fill="none">
          <path
            d="M12 2l2.6 6.3L21 9l-5 4.4L17.5 20 12 16.5 6.5 20 8 13.4 3 9l6.4-.7L12 2z"
            fill="#7A5410"
          />
        </svg>
      )}
    </div>
  );
}
