import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Compass, Map as MapIcon, RefreshCw, Ship } from "lucide-react";
import {
  MasteryBar,
  MentorAvatar,
  PageShell,
  ReadinessRing,
} from "../design-system";
import { Button } from "../design-system/Button";
import { grandLineApi } from "../services/api/grandLine";
import type {
  FleetEntry,
  GrandLineAssessment,
} from "../services/api/grandLine";

export default function GrandLine() {
  const [targets, setTargets] = useState<{ key: string; name: string }[]>([]);
  const [selectedTarget, setSelectedTarget] = useState<string>("");
  const [data, setData] = useState<GrandLineAssessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    grandLineApi
      .listTargets()
      .then(r => setTargets(r.targets))
      .catch(() => {});
  }, []);

  function load(target?: string) {
    setLoading(true);
    setError("");
    grandLineApi
      .assess(target || undefined)
      .then(setData)
      .catch(e =>
        setError(e instanceof Error ? e.message : "Assessment failed to load"),
      )
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    load();
  }, []);

  if (loading && !data) {
    return (
      <PageShell theme="focus">
        <div className="mx-auto max-w-4xl px-4 py-12">
          <div className="mx-auto flex h-64 max-w-md animate-pulse items-center justify-center rounded-2xl bg-surface">
            <Ship size={40} className="text-text-muted/40" />
          </div>
        </div>
      </PageShell>
    );
  }

  return (
    <PageShell theme="adventure">
      <div className="mx-auto max-w-4xl px-4 py-8 md:py-12">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <MentorAvatar size={56} mood="briefing" />
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-text-muted">
                Grand Line Assessment
              </p>
              <h1 className="text-2xl font-extrabold text-text md:text-3xl">
                Where do you stand?
              </h1>
              <p className="text-sm text-text-muted">{data?.summary}</p>
            </div>
          </div>
          <Button
            variant="outline"
            size="sm"
            loading={loading}
            onClick={() => load(selectedTarget)}
          >
            <RefreshCw size={14} /> Recalculate
          </Button>
        </header>

        {/* target picker */}
        <section className="bounty-card mb-6 p-4">
          <p className="mb-2 text-xs font-bold uppercase tracking-wider text-text-muted">
            Compare against a product-company target
          </p>
          <div className="flex flex-wrap gap-1.5">
            <button
              onClick={() => {
                setSelectedTarget("");
                load("");
              }}
              className={`rounded-full border px-3 py-1 text-xs font-semibold ${
                !selectedTarget
                  ? "border-primary bg-primary text-white"
                  : "border-line bg-surface text-text-muted hover:text-text"
              }`}
            >
              Fleet only
            </button>
            {targets.map(t => (
              <button
                key={t.key}
                onClick={() => {
                  setSelectedTarget(t.key);
                  load(t.key);
                }}
                className={`rounded-full border px-3 py-1 text-xs font-semibold ${
                  selectedTarget === t.key
                    ? "border-primary bg-primary text-white"
                    : "border-line bg-surface text-text-muted hover:text-text"
                }`}
              >
                {t.name}
              </button>
            ))}
          </div>
        </section>

        {error && (
          <p className="mb-4 rounded-lg border border-coral/30 bg-red-50 px-3 py-2 text-sm text-coral">
            {error}
          </p>
        )}

        {data && (
          <>
            {/* general readiness */}
            <section className="bounty-card mb-6 flex flex-col items-center gap-5 p-5 sm:flex-row">
              <ReadinessRing value={data.general.overall} size={116} label="Overall" />
              <div className="w-full flex-1 space-y-2.5">
                {Object.entries(data.general.categories).map(([key, cat], i) => (
                  <MasteryBar
                    key={key}
                    label={catLabel(key)}
                    value={cat.score}
                    tone={(["primary", "ocean", "tech", "gold", "coral", "rare"] as const)[i % 6]}
                    size="sm"
                  />
                ))}
              </div>
            </section>

            {/* fleet cards */}
            <section className="mb-6 grid gap-4 sm:grid-cols-3">
              {data.fleet.map(f => (
                <FleetCard key={f.company} entry={f} />
              ))}
            </section>

            {/* target card */}
            {data.target && (
              <section className="bounty-card mb-6 p-5">
                <div className="mb-3 flex items-center gap-2">
                  <Compass size={18} className="text-tech" />
                  <h2 className="text-sm font-extrabold uppercase tracking-widest text-text">
                    Target: {data.target.display_name}
                  </h2>
                  <span className="ml-auto rounded-full border border-line bg-canvas px-2.5 py-0.5 text-xs font-bold text-ocean">
                    {data.target.match_label} · {Math.round(data.target.company_score)}%
                  </span>
                </div>
                <p className="mb-3 text-sm text-text-muted">{data.target.verdict}</p>
                <div className="grid gap-2 sm:grid-cols-3">
                  {data.target.top_gaps.map(g => (
                    <GapPill key={g.label} label={g.label} hours={g.est_hours} score={g.score} />
                  ))}
                </div>
                {typeof data.target.weeks_remaining === "number" && (
                  <p className="mt-3 text-xs font-semibold text-text-muted">
                    Projected ready in ~{data.target.weeks_remaining} weeks
                    {data.target.estimated_date
                      ? ` (around ${new Date(data.target.estimated_date).toLocaleDateString()})`
                      : ""}
                  </p>
                )}
              </section>
            )}

            {/* voyage plan */}
            {data.voyage_plan.length > 0 && (
              <section className="bounty-card mb-6 p-5">
                <div className="mb-3 flex items-center gap-2">
                  <MapIcon size={18} className="text-reward" />
                  <h2 className="text-sm font-extrabold uppercase tracking-widest text-text">
                    Voyage plan — highest impact first
                  </h2>
                </div>
                <ol className="space-y-2.5">
                  {data.voyage_plan.map((g, i) => (
                    <li key={g.label} className="flex items-center gap-3">
                      <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-mint font-bold text-primary">
                        {i + 1}
                      </span>
                      <span className="flex-1 text-sm font-semibold text-text">
                        {g.label}
                      </span>
                      <span className="text-xs font-bold text-text-muted">
                        ~{g.est_hours}h focus
                      </span>
                    </li>
                  ))}
                </ol>
              </section>
            )}
          </>
        )}

        <p className="mt-8 text-center text-sm text-text-muted">
          Ready to drill?{" "}
          <Link to="/interview-terminal" className="font-semibold text-ocean underline">
            Interview Terminal →
          </Link>
        </p>
      </div>
    </PageShell>
  );
}

function FleetCard({ entry }: { entry: FleetEntry }) {
  const strong = entry.company_score >= 55;
  return (
    <div
      className={`rounded-xl border-2 p-4 ${
        strong ? "border-primary/40 bg-mint/30" : "border-line bg-surface"
      }`}
    >
      <div className="mb-1 flex items-center justify-between">
        <span className="font-extrabold text-text">{entry.display_name}</span>
        <span
          className={`text-lg font-extrabold ${strong ? "text-primary" : "text-text-muted"}`}
        >
          {Math.round(entry.company_score)}%
        </span>
      </div>
      <p className="text-[11px] font-bold uppercase tracking-wider text-ocean">
        {entry.match_label}
      </p>
      <p className="mt-2 min-h-[2.5rem] text-xs leading-relaxed text-text-muted">
        {entry.verdict}
      </p>
      <div className="mt-2 space-y-1.5">
        {entry.top_gaps.slice(0, 2).map(g => (
          <MasteryBar key={g.label} label={g.label} value={g.score} size="sm" tone="ocean" />
        ))}
      </div>
    </div>
  );
}

function GapPill({ label, hours, score }: { label: string; hours: number; score: number }) {
  return (
    <div className="rounded-lg border border-line bg-canvas p-3">
      <p className="text-xs font-bold text-text">{label}</p>
      <p className="text-lg font-extrabold text-tech">{hours}h</p>
      <p className="text-[11px] text-text-muted">now at {Math.round(score)}%</p>
    </div>
  );
}

function catLabel(key: string): string {
  const map: Record<string, string> = {
    dsa: "DSA",
    aptitude: "Aptitude",
    cs_fundamentals: "CS Fundamentals",
    coding: "Coding",
    interview: "Interview",
    resume: "Resume",
    projects: "Projects",
  };
  return map[key] ?? key;
}
