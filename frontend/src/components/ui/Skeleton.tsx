export default function Skeleton({ className = "", lines = 1, variant = "text" }) {
  const variants = {
    text: "h-4 rounded-full",
    heading: "h-8 rounded-full w-1/2",
    avatar: "h-12 w-12 rounded-full",
    card: "h-40 rounded-2xl",
    button: "h-12 rounded-xl w-32",
  };

  if (lines > 1) {
    return (
      <div className="space-y-3 animate-pulse">
        {Array.from({ length: lines }).map((_, i) => (
          <div
            key={i}
            className={`bg-brand-primary/10 ${variants[variant] || variants.text} ${
              i === lines - 1 ? "w-3/4" : "w-full"
            }`}
          />
        ))}
      </div>
    );
  }

  return (
    <div className={`animate-pulse bg-brand-primary/10 ${variants[variant] || variants.text} ${className}`} />
  );
}

export function CardSkeleton() {
  return (
    <div className="card animate-pulse">
      <div className="flex items-center gap-4 mb-4">
        <div className="h-12 w-12 rounded-xl bg-brand-primary/10" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-brand-primary/10 rounded-full w-1/3" />
          <div className="h-3 bg-brand-primary/10 rounded-full w-2/3" />
        </div>
      </div>
      <div className="space-y-2">
        <div className="h-3 bg-brand-primary/10 rounded-full" />
        <div className="h-3 bg-brand-primary/10 rounded-full w-5/6" />
      </div>
    </div>
  );
}

export function StatsSkeleton() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-pulse">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="card text-center">
          <div className="h-8 w-16 bg-brand-primary/10 rounded-full mx-auto mb-2" />
          <div className="h-3 w-20 bg-brand-primary/10 rounded-full mx-auto" />
        </div>
      ))}
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="space-y-2 animate-pulse">
          <div className="h-8 bg-brand-primary/10 rounded-full w-1/3" />
          <div className="h-4 bg-brand-primary/10 rounded-full w-1/4" />
        </div>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card h-48 bg-brand-primary/10 animate-pulse rounded-xl" />
          <div className="card h-48 bg-brand-primary/10 animate-pulse rounded-xl" />
        </div>
        <StatsSkeleton />
        <div className="grid md:grid-cols-3 gap-6">
          {Array.from({ length: 6 }).map((_, i) => (
            <CardSkeleton key={i} />
          ))}
        </div>
      </div>
    </div>
  );
}

export function QuestionCardSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="space-y-2">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 rounded-2xl border border-brand-primary/10 bg-surface-card px-4 py-3 animate-pulse">
          <div className="flex w-12 shrink-0 flex-col items-center justify-center text-center">
            <div className="h-2.5 w-8 bg-brand-primary/10 rounded" />
            <div className="mt-1 h-4 w-4 rounded-full bg-brand-primary/10" />
          </div>
          <div className="shrink-0 h-6 w-6 rounded bg-brand-primary/10" />
          <div className="min-w-0 flex-1 space-y-2">
            <div className="h-4 bg-brand-primary/10 rounded-full w-3/4" />
            <div className="flex items-center gap-2">
              <div className="h-3.5 w-12 bg-brand-primary/10 rounded" />
              <div className="h-3.5 w-14 bg-brand-primary/10 rounded-full" />
              <div className="h-3 w-20 bg-brand-primary/10 rounded" />
            </div>
          </div>
          <div className="hidden md:flex items-center gap-4 shrink-0">
            <div className="h-3 w-8 bg-brand-primary/10 rounded" />
            <div className="h-5 w-14 bg-brand-primary/10 rounded" />
          </div>
          <div className="shrink-0 h-3.5 w-3.5 bg-brand-primary/10 rounded" />
        </div>
      ))}
    </div>
  );
}

export function LeaderboardRowSkeleton({ count = 5 }: { count?: number }) {
  return (
    <div className="space-y-1.5">
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          className="flex items-center gap-2 sm:gap-4 px-3 sm:px-4 py-2.5 sm:py-3 rounded-xl border border-gray-700/20 bg-gray-900/20 animate-pulse"
        >
          <div className="w-8 text-center shrink-0">
            <div className="h-4 w-5 bg-gray-700/40 rounded mx-auto" />
          </div>
          <div className="w-7 h-7 sm:w-9 sm:h-9 rounded-lg bg-gray-700/30 shrink-0" />
          <div className="flex-1 min-w-0 space-y-1.5">
            <div className="h-3.5 bg-gray-700/40 rounded-full w-1/3" />
            <div className="h-2.5 bg-gray-700/30 rounded-full w-1/5" />
          </div>
          <div className="hidden sm:block text-center w-14 shrink-0">
            <div className="h-4 w-6 bg-gray-700/40 rounded mx-auto mb-1" />
            <div className="h-2 w-8 bg-gray-700/30 rounded mx-auto" />
          </div>
          <div className="hidden sm:block text-center w-16 shrink-0">
            <div className="h-4 w-10 bg-gray-700/40 rounded mx-auto mb-1" />
            <div className="h-2 w-6 bg-gray-700/30 rounded mx-auto" />
          </div>
          <div className="hidden md:flex text-center w-12 shrink-0 items-center justify-center gap-1">
            <div className="h-4 w-8 bg-gray-700/40 rounded" />
          </div>
        </div>
      ))}
    </div>
  );
}

export function DashboardCardSkeleton({ count = 4 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-pulse">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="card text-center py-5">
          <div className="h-10 w-10 bg-brand-primary/10 rounded-xl mx-auto mb-3" />
          <div className="h-6 w-16 bg-brand-primary/10 rounded-full mx-auto mb-2" />
          <div className="h-2.5 w-20 bg-brand-primary/10 rounded-full mx-auto" />
        </div>
      ))}
    </div>
  );
}

export function InterviewSkeleton() {
  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="flex items-center justify-between animate-pulse">
          <div className="flex items-center gap-3">
            <div className="h-8 w-8 rounded-lg bg-brand-primary/10" />
            <div className="h-5 w-32 bg-brand-primary/10 rounded" />
          </div>
          <div className="h-4 w-20 bg-brand-primary/10 rounded" />
        </div>
        <div className="h-2 w-full bg-brand-primary/10 rounded-full" />
        <div className="card p-6 space-y-4 animate-pulse">
          <div className="h-3 w-24 bg-brand-primary/10 rounded uppercase tracking-wider" />
          <div className="h-6 w-3/4 bg-brand-primary/10 rounded" />
          <div className="space-y-2">
            <div className="h-4 bg-brand-primary/10 rounded w-full" />
            <div className="h-4 bg-brand-primary/10 rounded w-5/6" />
          </div>
        </div>
        <div className="card p-6 animate-pulse">
          <div className="h-4 w-20 bg-brand-primary/10 rounded mb-3" />
          <div className="h-32 w-full bg-brand-primary/10 rounded-xl" />
        </div>
        <div className="flex gap-3 animate-pulse">
          <div className="h-12 flex-1 bg-brand-primary/10 rounded-xl" />
          <div className="h-12 w-32 bg-brand-primary/10 rounded-xl" />
        </div>
      </div>
    </div>
  );
}
