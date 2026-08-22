import { ReactNode } from "react";
import { colors, radii, shadows, motion, spacing, typography } from "..";

interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: ReactNode;
  action?: {
    label: string;
    onClick: () => void;
    variant?: "primary" | "secondary" | "ghost";
  };
  illustration?: "search" | "folder" | "calendar" | "code" | "trophy" | "leaf" | "custom";
  className?: string;
}

const illustrations: Record<NonNullable<EmptyStateProps["illustration"]>, ReactNode> = {
  search: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  ),
  folder: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </svg>
  ),
  calendar: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  ),
  code: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="16 18 22 12 16 6" />
      <polyline points="8 6 2 12 8 18" />
    </svg>
  ),
  trophy: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6" />
      <path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18" />
      <path d="M4 22h16" />
      <path d="M10 14.66V17a2 2 0 1 0 4 0v-2.34" />
      <path d="M18 5v8" />
      <path d="M6 5v8" />
    </svg>
  ),
  leaf: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 6.1 17 10.4 17 17.8" />
      <path d="M15.12 15.12A4 4 0 0 1 17.7 11.5" />
    </svg>
  ),
  custom: null,
};

export function EmptyState({
  title,
  description,
  icon,
  action,
  illustration = "folder",
  className = "",
}: EmptyStateProps) {
  const illus = illustration === "custom" ? icon : illustrations[illustration];

  return (
    <div className={`flex flex-col items-center text-center py-12 px-4 ${className}`}>
      <div
        className={`
          w-20 h-20 rounded-${radii.xl} flex items-center justify-center mx-auto mb-6
          bg-brand-mint text-brand-deep
        `}
      >
        {illus}
      </div>
      <h3 className="font-display text-2xl font-bold text-text-primary mb-2">
        {title}
      </h3>
      {description && (
        <p className="text-text-secondary max-w-sm mx-auto mb-6 leading-relaxed">
          {description}
        </p>
      )}
      {action && (
        <button
          onClick={action.onClick}
          className={`
            inline-flex items-center gap-2 px-6 py-3 rounded-${radii.button}
            font-semibold text-sm transition-all duration-200
            ${action.variant === "primary"
              ? `bg-gradient-to-r from-brand-primary to-brand-deep text-white hover:from-brand-deep hover:to-brand-darkest shadow-soft-md`
              : action.variant === "secondary"
              ? `bg-background-surfaceSecondary text-text-primary border border-border-primary hover:bg-background-secondary`
              : `text-brand-primary hover:bg-brand-mint`}
          `}
        >
          {action.label}
        </button>
      )}
    </div>
  );
}

interface LoadingStateProps {
  variant?: "spinner" | "dots" | "pulse" | "skeleton";
  size?: "sm" | "md" | "lg" | "xl";
  text?: string;
  className?: string;
}

export function LoadingState({
  variant = "spinner",
  size = "md",
  text,
  className = "",
}: LoadingStateProps) {
  const sizeClasses: Record<LoadingStateProps["size"], string> = {
    sm: "w-6 h-6",
    md: "w-8 h-8",
    lg: "w-12 h-12",
    xl: "w-16 h-16",
  };

  const textSizes: Record<LoadingStateProps["size"], string> = {
    sm: "text-xs",
    md: "text-sm",
    lg: "text-base",
    xl: "text-lg",
  };

  return (
    <div className={`flex flex-col items-center gap-3 ${className}`}>
      {variant === "spinner" && (
        <div
          className={`
            ${sizeClasses[size]}
            animate-spin rounded-full border-3 border-border-primary
            border-t-brand-primary
          `}
          role="status"
          aria-label="Loading"
        >
          <span className="sr-only">Loading...</span>
        </div>
      )}
      {variant === "dots" && (
        <div className="flex gap-1.5" role="status" aria-label="Loading">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className={`
                ${size === "sm" ? "w-1.5 h-1.5" : size === "md" ? "w-2 h-2" : size === "lg" ? "w-2.5 h-2.5" : "w-3 h-3"}
                rounded-full bg-brand-primary animate-bounce
              `}
              style={{ animationDelay: `${i * 150}ms` }}
            />
          ))}
        </div>
      )}
      {variant === "pulse" && (
        <div
          className={`
            ${size === "sm" ? "w-8 h-8" : size === "md" ? "w-12 h-12" : size === "lg" ? "w-16 h-16" : "w-20 h-20"}
            rounded-full bg-brand-mint animate-pulse
          `}
          role="status"
          aria-label="Loading"
        />
      )}
      {variant === "skeleton" && (
        <div className="w-full space-y-3" role="status" aria-label="Loading">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className={`
                h-4 rounded-${radii.md} bg-background-secondary animate-pulse
                ${size === "sm" ? "h-3" : size === "md" ? "h-4" : size === "lg" ? "h-5" : "h-6"}
              `}
            />
          ))}
        </div>
      )}
      {text && (
        <p className={`text-text-secondary font-medium ${textSizes[size]}`}>
          {text}
        </p>
      )}
    </div>
  );
}

interface ErrorStateProps {
  title: string;
  message?: string;
  code?: string | number;
  action?: {
    label: string;
    onClick: () => void;
    variant?: "primary" | "secondary" | "ghost";
  };
  illustration?: "alert" | "server" | "network" | "permission" | "notfound";
  className?: string;
}

const errorIllustrations: Record<NonNullable<ErrorStateProps["illustration"]>, ReactNode> = {
  alert: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" />
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  ),
  server: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <rect x="2" y="2" width="20" height="8" rx="2" ry="2" />
      <rect x="2" y="14" width="20" height="8" rx="2" ry="2" />
      <line x1="6" y1="6" x2="6.01" y2="6" />
      <line x1="6" y1="18" x2="6.01" y2="18" />
    </svg>
  ),
  network: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <line x1="1" y1="1" x2="23" y2="23" />
      <path d="M16.72 11.06A10.94 10.94 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M12 2a10 10 0 0 0-8.86 4" />
      <path d="M4.12 7.72a18.9 18.9 0 0 0 0 8.56" />
    </svg>
  ),
  permission: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  ),
  notfound: (
    <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  ),
};

export function ErrorState({
  title,
  message,
  code,
  action,
  illustration = "alert",
  className = "",
}: ErrorStateProps) {
  const illus = errorIllustrations[illustration];

  return (
    <div className={`flex flex-col items-center text-center py-12 px-4 ${className}`}>
      <div
        className={`
          w-20 h-20 rounded-${radii.xl} flex items-center justify-center mx-auto mb-6
          bg-error/10 text-error
        `}
      >
        {illus}
      </div>
      <h3 className="font-display text-2xl font-bold text-text-primary mb-2">
        {title}
      </h3>
      {message && (
        <p className="text-text-secondary max-w-sm mx-auto mb-6 leading-relaxed">
          {message}
        </p>
      )}
      {code && (
        <p className="text-xs font-mono text-text-dim mb-6">
          Error {code}
        </p>
      )}
      {action && (
        <button
          onClick={action.onClick}
          className={`
            inline-flex items-center gap-2 px-6 py-3 rounded-${radii.button}
            font-semibold text-sm transition-all duration-200
            ${action.variant === "primary"
              ? `bg-gradient-to-r from-brand-primary to-brand-deep text-white hover:from-brand-deep hover:to-brand-darkest shadow-soft-md`
              : action.variant === "secondary"
              ? `bg-background-surfaceSecondary text-text-primary border border-border-primary hover:bg-background-secondary`
              : `text-brand-primary hover:bg-brand-mint`}
          `}
        >
          {action.label}
        </button>
      )}
    </div>
  );
}