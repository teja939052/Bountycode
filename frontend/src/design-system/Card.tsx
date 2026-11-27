import type { HTMLAttributes, ReactNode } from "react";

/**
 * Card — V3 design system primitive.
 * Golden Hour Academy: dark surface, subtle border, soft shadow,
 * elevation on hover, optional subject-coded tones.
 */

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  /** padding: none | sm | md (default) */
  pad?: "none" | "sm" | "md";
  interactive?: boolean;
  tone?: "default" | "bounty" | "boss" | "mint" | "sand" | "coding" | "aptitude" | "reasoning" | "verbal" | "interview";
  children?: ReactNode;
}

const PAD_CLASS = {
  none: "",
  sm: "p-4",
  md: "p-6",
} as const;

const TONE_CLASS = {
  default: "bg-surface border border-border shadow-card",
  bounty: "bg-surface border border-gold/30 shadow-bounty",
  boss: "bg-subject-boss/10 border border-subject-boss/30 shadow-boss",
  mint: "bg-subject-verbal/10 border border-subject-verbal/30 shadow-verbal",
  sand: "bg-subject-aptitude/10 border border-subject-aptitude/30 shadow-aptitude",
  coding: "bg-subject-coding/10 border border-subject-coding/30 shadow-coding",
  aptitude: "bg-subject-aptitude/10 border border-subject-aptitude/30 shadow-aptitude",
  reasoning: "bg-subject-reasoning/10 border border-subject-reasoning/30 shadow-reasoning",
  verbal: "bg-subject-verbal/10 border border-subject-verbal/30 shadow-verbal",
  interview: "bg-subject-interview/10 border border-subject-interview/30",
} as const;

export function Card({
  pad = "md",
  interactive = false,
  tone = "default",
  className = "",
  children,
  ...rest
}: CardProps) {
  const base = `${TONE_CLASS[tone]} ${pad !== "none" ? PAD_CLASS[pad] : ""}`;

  return (
    <div
      className={`rounded-2xl transition-all duration-200 ${
        interactive
          ? "cursor-pointer hover:-translate-y-1 hover:border-primary/50 hover:shadow-card-hover"
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
    <div className={`mb-6 flex items-end justify-between gap-4 ${className}`}>
      <div className="min-w-0">
        {eyebrow && (
          <span className="inline-block mb-2 px-2 py-0.5 rounded-full text-xs font-bold tracking-wider text-primary bg-primary/10 border border-primary/20">
            {eyebrow}
          </span>
        )}
        <h2 className="font-display text-xl font-extrabold text-text sm:text-2xl">{title}</h2>
        {description && <p className="mt-1 max-w-2xl text-sm text-text-muted">{description}</p>}
      </div>
      {action && <div className="shrink-0">{action}</div>}
    </div>
  );
}
