import { forwardRef, type ReactNode } from "react";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "elevated" | "outlined" | "glass" | "dark";
  padding?: "none" | "sm" | "md" | "lg";
  radius?: "sm" | "md" | "lg" | "xl" | "full";
  hover?: boolean;
}

const paddingStyles: Record<string, string> = {
  none: "p-0",
  sm: "p-3",
  md: "p-5",
  lg: "p-8",
};

const radiusStyles: Record<string, string> = {
  sm: "rounded-md",
  md: "rounded-xl",
  lg: "rounded-2xl",
  xl: "rounded-3xl",
  full: "rounded-full",
};

const variantStyles: Record<string, string> = {
  default:
    "bg-surface border border-border/40 shadow-card",
  elevated:
    "bg-surface border border-border/60 shadow-card-hover hover:shadow-modal transition-shadow duration-200",
  outlined:
    "bg-surface border-2 border-primary/40 hover:border-primary transition-colors duration-200",
  glass:
    "bg-white/70 border border-white/40 backdrop-blur-md shadow-card",
  dark:
    "bg-[#0d1117] border border-white/10 text-text-primary shadow-card",
};

export const Card = forwardRef<HTMLDivElement, CardProps>(
  (
    { variant = "default", padding = "md", radius = "md", hover = true, className = "", children, ...props },
    ref
  ) => {
    return (
      <div
        ref={ref}
        className={`${variantStyles[variant]} ${radiusStyles[radius]} ${paddingStyles[padding]} ${
          hover ? "transition-all duration-200 hover:border-primary/30 hover:shadow-card-hover" : ""
        } ${className}`}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = "Card";
export default Card;

export function CardGrid({ children, className = "", cols = 3 }: { children?: ReactNode; className?: string; cols?: number }) {
  const colMap: Record<number, string> = {
    1: "grid-cols-1",
    2: "grid-cols-1 sm:grid-cols-2",
    3: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3",
    4: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-4",
  };
  return (
    <div className={`grid gap-5 ${colMap[cols] || colMap[3]} ${className}`}>
      {children}
    </div>
  );
}
