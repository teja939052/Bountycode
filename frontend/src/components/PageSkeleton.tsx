import Skeleton from "./ui/Skeleton";

export default function PageSkeleton() {
  return (
    <div className="min-h-screen px-4 py-6 md:py-8">
      <div className="mx-auto max-w-7xl space-y-6 animate-pulse">
        <div className="h-10 w-1/3 rounded-full bg-brand-primary/10" />
        <div className="h-4 w-1/4 rounded-full bg-brand-primary/10" />

        <div className="space-y-6 pt-2">
          <div className="card p-5">
            <Skeleton lines={2} variant="heading" />
            <div className="mt-4 space-y-3">
              <Skeleton lines={4} variant="card" />
            </div>
          </div>

          <div className="card p-5">
            <Skeleton lines={1} variant="heading" />
            <div className="mt-4 space-y-3">
              <Skeleton lines={3} variant="card" />
            </div>
          </div>

          <div className="card p-5">
            <Skeleton lines={1} variant="heading" />
            <div className="mt-4 space-y-3">
              <Skeleton lines={3} variant="card" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
