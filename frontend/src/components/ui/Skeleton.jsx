export default function Skeleton({ className = "", lines = 1, variant = "text" }) {
  const variants = {
    text: "h-4 rounded",
    heading: "h-8 rounded w-1/2",
    avatar: "h-12 w-12 rounded-full",
    card: "h-40 rounded-xl",
    button: "h-12 rounded-lg w-32",
  };

  if (lines > 1) {
    return (
      <div className="space-y-3 animate-pulse">
        {Array.from({ length: lines }).map((_, i) => (
          <div
            key={i}
            className={`bg-gray-200 dark:bg-gray-700 ${variants[variant] || variants.text} ${
              i === lines - 1 ? "w-3/4" : "w-full"
            }`}
          />
        ))}
      </div>
    );
  }

  return (
    <div className={`animate-pulse bg-gray-200 dark:bg-gray-700 ${variants[variant] || variants.text} ${className}`} />
  );
}

export function CardSkeleton() {
  return (
    <div className="card animate-pulse">
      <div className="flex items-center gap-4 mb-4">
        <div className="h-12 w-12 rounded-xl bg-gray-200 dark:bg-gray-700" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3" />
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-2/3" />
        </div>
      </div>
      <div className="space-y-2">
        <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded" />
        <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-5/6" />
      </div>
    </div>
  );
}

export function StatsSkeleton() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-pulse">
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="card text-center">
          <div className="h-8 w-16 bg-gray-200 dark:bg-gray-700 rounded mx-auto mb-2" />
          <div className="h-3 w-20 bg-gray-200 dark:bg-gray-700 rounded mx-auto" />
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
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3" />
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4" />
        </div>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="card h-48 bg-gray-200 dark:bg-gray-700 animate-pulse rounded-xl" />
          <div className="card h-48 bg-gray-200 dark:bg-gray-700 animate-pulse rounded-xl" />
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
