import { ReactNode } from "react";
import { colors, radii, motion, spacing } from "..";

interface ProgressBarProps {
  value: number;
  max?: number;
  size?: "sm" | "md" | "lg" | "xl";
  color?: "primary" | "xp" | "achievement" | "boss" | "info" | "success" | "warning";
  showLabel?: boolean;
  label?: ReactNode;
  animated?: boolean;
  striped?: boolean;
  rounded?: boolean;
  className?: string;
}

const sizeStyles: Record<ProgressBarProps["size"], string> = {
  sm: `h-${spacing.scale[1]}`,
  md: `h-${spacing.scale[2]}`,
  lg: `h-${spacing.scale[3]}`,
  xl: `h-${spacing.scale[4]}`,
};

const colorStyles: Record<ProgressBarProps["color"], string> = {
  primary: colors.brand.primary,
  xp: colors.semantic.xp,
  achievement: colors.semantic.achievement,
  boss: colors.semantic.boss,
  info: colors.semantic.info,
  success: colors.semantic.success,
  warning: colors.semantic.warning,
};

export function ProgressBar({
  value,
  max = 100,
  size = "md",
  color = "primary",
  showLabel = false,
  label,
  animated = false,
  striped = false,
  rounded = true,
  className = "",
}: ProgressBarProps) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));

  return (
    <div className={className}>
      {(showLabel || label) && (
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-sm font-medium text-text-primary">
            {label ?? `${Math.round(percentage)}%`}
          </span>
          {showLabel && (
            <span className="text-sm font-mono text-text-secondary">
              {value} / {max}
            </span>
          )}
        </div>
      )}
      <div
        className={`
          relative overflow-hidden bg-background-secondary
          ${sizeStyles[size]}
          ${rounded ? `rounded-${radii.full}` : `rounded-${radii.md}`}
          ${className}
        `}
        role="progressbar"
        aria-valuenow={percentage}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={label || "Progress"}
      >
        <div
          className={`
            h-full transition-all duration-500 ease-out
            ${rounded ? `rounded-${radii.full}` : `rounded-${radii.md}`}
            ${animated ? "animate-pulse" : ""}
            ${striped ? "bg-gradient-to-r bg-[length:20px_100%] animate-[stripe_1s_linear_infinite]" : ""}
          `}
          style={{
            width: `${percentage}%`,
            backgroundColor: colorStyles[color],
          }}
        />
      </div>
      <style jsx>{`
        @keyframes stripe {
          from { background-position: 0 0; }
          to { background-position: 40px 0; }
        }
      `}</style>
    </div>
  );
}

export function CircularProgress({
  value,
  max = 100,
  size = 64,
  strokeWidth = 6,
  color = "primary",
  showValue = true,
  label,
  className = "",
}: {
  value: number;
  max?: number;
  size?: number;
  strokeWidth?: number;
  color?: ProgressBarProps["color"];
  showValue?: boolean;
  label?: string;
  className?: string;
}) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference * (1 - percentage / 100);

  return (
    <div className={`relative inline-flex items-center justify-center ${className}`} style={{ width: size, height: size }}>
      <svg width={size} height={size} style={{ transform: "rotate(-90deg)" }}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colors.border.primary}
          strokeWidth={strokeWidth}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colors[color] || colors.brand.primary}
          strokeWidth={strokeWidth}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          style={{
            transition: "stroke-dashoffset 500ms ease-out",
            transformOrigin: "center",
          }}
        />
      </svg>
      {(showValue || label) && (
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          {showValue && (
            <span className="font-display font-bold text-text-primary" style={{ fontSize: size / 3 }}>
              {Math.round(percentage)}%
            </span>
          )}
          {label && (
            <span className="text-xs text-text-secondary font-mono uppercase tracking-wider mt-1">
              {label}
            </span>
          )}
        </div>
      )}
    </div>
  );
}