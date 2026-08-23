import type { HTMLAttributes, ReactNode } from "react";

/**
 * Card — V2 design system primitive.
 * White surface, 1px border, soft shadow. Elevation on hover, never glow.
 */

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /** padding: none | sm | md (default) */
  pad?: "none" | "sm" | "md";
  interactive?: boolean;
  tone?: "default" | "bounty" | "boss" | "mint" | "sand";
  children?: ReactNode;
}

const PAD_CLASS = {
  none: "",
  sm: "p-4",
  md: "p-6",
} as const;

const TONE_CLASS = {
  default: "bg-surface border-border",
  bounty: "bounty-card",
  boss: "boss-card",
  mint: "bg-mint border-primary/20",
  sand: "parchment-bg border-sand",
} as const;

export function Card({
  pad = "md",
  interactive = false,
  tone = "default",
  className = "",
  children,
  ...rest
}: CardProps) {
  const base =
    tone === "bounty" || tone === "sand"
      ? `${TONE_CLASS[tone]} ${pad !== "none" ? PAD_CLASS[pad] : ""}`
      : `border shadow-card ${TONE_CLASS[tone]} ${pad !== "none" ? PAD_CLASS[pad] : ""}`;

  return (
    <div
      className={`rounded-2xl transition-all duration-200 ${
        interactive
          ? "cursor-pointer hover:-translate-y-0.5 hover:shadow-card-hover hover:border-primary/50"
          : ""
      } ${base} ${className}`}
      {...rest}
    >
      {children}
    </div>
  );
}

interface SectionHeaderProps {
  eyebrow?: string;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export function SectionHeader({ eyebrow, title, description, action, className = "" }: SectionHeaderProps) {
  return (
    <div className={`mb-5 flex items-end justify-between gap-4 ${className}`}>
      <div className="min-w-0">
        {eyebrow && <span className="adventure-label mb-2">{eyebrow}</span>}
        <h2 className="font-display text-xl font-extrabold text-text sm:text-2xl">{title}</h2>
        {description && <p className="mt-1 max-w-2xl text-sm text-text-muted">{description}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}
