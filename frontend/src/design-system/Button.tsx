import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from "react";

/**
 * Button — V3 design system primitive.
 * Golden Hour Academy: dark canvas surface, vibrant orange primary,
 * subject-coded accents, crisp hover states, mobile-friendly touch targets.
 */

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "outline" | "danger" | "gold" | "ocean";
  size?: "sm" | "md" | "lg" | "xl";
  fullWidth?: boolean;
  loading?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
}

const VARIANT_CLASS: Record<NonNullable<ButtonProps["variant"]>, string> = {
  primary:
    "btn-primary bg-primary text-primary-text shadow-primary hover:bg-primary-dark hover:shadow-primary-lg active:scale-[0.97]",
  secondary:
    "bg-surface border border-border text-text hover:bg-surface-hover hover:border-primary/50 active:scale-[0.97]",
  ghost:
    "text-text hover:bg-primary/10 active:scale-[0.97]",
  outline:
    "border border-border text-text hover:bg-primary/5 hover:border-primary focus:ring-2 focus:ring-primary/20 active:scale-[0.97]",
  danger:
    "bg-subject-boss text-white shadow-boss hover:bg-red-600 active:scale-[0.97]",
  gold:
    "bg-subject-aptitude text-text shadow-aptitude hover:bg-amber-500 active:scale-[0.97]",
  ocean:
    "bg-subject-coding text-text shadow-coding hover:bg-cyan-500 active:scale-[0.97]",
};

const SIZE_CLASS = {
  sm: "px-3 py-1.5 text-xs gap-1.5 rounded-xl",
  md: "px-4 py-2 text-sm gap-2 rounded-xl",
  lg: "px-5 py-2.5 text-sm gap-2 rounded-xl",
  xl: "px-7 py-3.5 text-base gap-2.5 rounded-xl",
} as const;

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  {
    variant = "primary",
    size = "md",
    fullWidth = false,
    loading = false,
    leftIcon,
    rightIcon,
    className = "",
    children,
    disabled,
    ...rest
  },
  ref
) {
  return (
    <button
      ref={ref}
      disabled={disabled || loading}
      className={`${VARIANT_CLASS[variant]} ${SIZE_CLASS[size]} ${fullWidth ? "w-full" : ""} ${className}`}
      {...rest}
    >
      {loading ? (
        <>
          <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" opacity="0.25" />
            <path d="M12 2a10 10 0 0110 10" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
          </svg>
          <span>Loading…</span>
        </>
      ) : (
        <>
          {leftIcon && <span className="inline-flex shrink-0">{leftIcon}</span>}
          {children}
          {rightIcon && <span className="inline-flex shrink-0">{rightIcon}</span>}
        </>
      )}
    </button>
  );
});
