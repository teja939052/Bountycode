import { ReactNode, forwardRef, HTMLAttributes } from "react";
import { colors, radii, shadows, motion, spacing } from "..";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "elevated" | "outlined" | "glass" | "interactive";
  padding?: "none" | "sm" | "md" | "lg";
  hover?: boolean;
}

const variantStyles: Record<CardProps["variant"], string> = {
  default: `
    background: ${colors.background.surface};
    border: 1px solid ${colors.border.primary};
  `,
  elevated: `
    background: ${colors.background.surface};
    border: none;
    box-shadow: ${shadows.md};
  `,
  outlined: `
    background: ${colors.background.surface};
    border: 1px solid ${colors.border.primary};
  `,
  glass: `
    background: ${colors.glass.bg};
    backdrop-filter: blur(${colors.glass.blur});
    border: 1px solid rgba(255,255,255,0.2);
  `,
  interactive: `
    background: ${colors.background.surface};
    border: 1px solid ${colors.border.primary};
    transition: ${motion.transitions.normal};
    &:hover {
      border-color: ${colors.border.focus};
      box-shadow: ${shadows.glow};
      transform: translateY(-2px);
    }
  `,
};

const paddingStyles: Record<CardProps["padding"], string> = {
  none: "",
  sm: `p-${spacing.scale[3]}`,
  md: `p-${spacing.scale[4]}`,
  lg: `p-${spacing.scale[6]}`,
};

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    {
      variant = "default",
      padding = "md",
      hover = false,
      className = "",
      children,
      ...props
    },
    ref
  ) => {
    const effectiveVariant = hover && variant === "default" ? "interactive" : variant;

    return (
      <div
        ref={ref}
        className={`
          rounded-${radii.card}
          ${variantStyles[effectiveVariant]}
          ${paddingStyles[padding]}
          ${className}
        `}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";

export interface CardHeaderProps extends HTMLAttributes<HTMLDivElement> {}
export const CardHeader = forwardRef<HTMLDivElement, CardHeaderProps>(
  ({ className = "", children, ...props }, ref) => (
    <div
      ref={ref}
      className={`px-${spacing.scale[4]} py-${spacing.scale[3]} border-b border-${colors.border.primary} ${className}`}
      {...props}
    >
      {children}
    </div>
  )
);
CardHeader.displayName = "CardHeader";

export interface CardContentProps extends HTMLAttributes<HTMLDivElement> {}
export const CardContent = forwardRef<HTMLDivElement, CardContentProps>(
  ({ className = "", children, ...props }, ref) => (
    <div
      ref={ref}
      className={`p-${spacing.scale[4]} ${className}`}
      {...props}
    >
      {children}
    </div>
  )
);
CardContent.displayName = "CardContent";

export interface CardFooterProps extends HTMLAttributes<HTMLDivElement> {}
export const CardFooter = forwardRef<HTMLDivElement, CardFooterProps>(
  ({ className = "", children, ...props }, ref) => (
    <div
      ref={ref}
      className={`px-${spacing.scale[4]} py-${spacing.scale[3]} border-t border-${colors.border.primary} ${className}`}
      {...props}
    >
      {children}
    </div>
  )
);
CardFooter.displayName = "CardFooter";