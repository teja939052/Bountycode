import type { ReactNode } from "react";
import type { LucideIcon } from "lucide-react";

interface EmptyStateProps {
  icon?: LucideIcon;
  title: string;
  description?: string;
  actionLabel?: string;
  onAction?: () => void;
  actionTo?: string;
  children?: ReactNode;
}

export default function EmptyState({
  icon: Icon,
  title,
  description,
  actionLabel,
  onAction,
  children,
}: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 text-center">
      <div className="w-16 h-16 rounded-2xl bg-brand-primary/10 flex items-center justify-center mb-4">
        {Icon ? (
          <Icon size={28} className="text-brand-dim" />
        ) : (
          <span className="text-2xl">📭</span>
        )}
      </div>
      <h3 className="text-sm font-display font-bold text-brand-primary mb-1">{title}</h3>
      {description && (
        <p className="text-xs text-brand-secondary max-w-xs mb-4">{description}</p>
      )}
      {actionLabel && onAction && (
        <button
          onClick={onAction}
          className="inline-flex items-center justify-center gap-2 rounded-xl bg-brand-primary px-5 py-2.5 text-xs font-bold text-text-primary hover:bg-brand-primary/80 transition-colors"
        >
          {actionLabel}
        </button>
      )}
      {children}
    </div>
  );
}
