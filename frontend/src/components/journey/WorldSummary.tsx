import type { JourneyWorld } from "../../hooks/useJourneyState";

export default function WorldSummary({ world }: { world: JourneyWorld }) {
  const total = world.towns.reduce((s, t) => s + t.levels.length, 0);
  const done = world.towns.reduce((s, t) => s + t.levels.filter((l) => l.status === "completed").length, 0);
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  const isLocked = world.status === "locked";

  return (
    <div className={`rounded-xl border border-default bg-card p-3 flex items-center gap-3 ${isLocked ? "opacity-40" : ""}`}>
      <span className="text-xl">{world.icon}</span>
      <div className="flex-1 min-w-0">
        <div className="text-sm font-bold text-primary">{world.title}</div>
        <div className="text-[11px] text-muted">{world.subtitle}</div>
      </div>
      <div className="text-right shrink-0">
        <div className="text-sm font-bold text-primary">{pct}%</div>
      </div>
    </div>
  );
}
