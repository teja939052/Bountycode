import type { ReactNode } from "react";

interface WarmEmptyStateProps {
  emoji?: string;
  title: string;
  copy?: string;
  action?: ReactNode;
  className?: string;
}

/**
 * Warm, inviting empty state — a friendly invitation to act, never a bare
 * gray "no data" box. For an anxious audience, "start here" beats "empty".
 */
export default function WarmEmptyState({
  emoji = "🌱",
  title,
  copy,
  action,
  className = "",
}: WarmEmptyStateProps) {
  return (
    <div className={`empty-warm ${className}`}>
      <span className="empty-emoji" role="img" aria-hidden="true">{emoji}</span>
      <div className="empty-title">{title}</div>
      {copy && <p className="empty-copy">{copy}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
