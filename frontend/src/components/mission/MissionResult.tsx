import { Link, useLocation, useNavigate } from "react-router-dom";
import { ArrowRight, RotateCcw } from "lucide-react";
import { starsForScore, type ActivityResult, type Mission } from "../../types/mission";

/**
 * Mission result screen. Displays ONLY authoritative server numbers from
 * record_activity (score, diamonds, mastery_before/after, diagnosis_codes) —
 * never client-computed rewards. Next step comes from a journey refetch.
 */
export default function MissionResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = (location.state ?? {}) as { mission?: Mission; activity?: ActivityResult };
  const { mission, activity } = state;

  if (!mission || !activity) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center">
          <p className="font-bold text-text-primary">No result to show</p>
          <p className="text-sm text-text-muted font-mono mt-1">Complete a mission to see authoritative results.</p>
          <button onClick={() => navigate("/journey")} className="btn-primary text-sm mt-4">
            Back to Journey
          </button>
        </div>
      </div>
    );
  }

  const stars = starsForScore(activity.score);
  const masteryDelta =
    activity.mastery_before != null && activity.mastery_after != null
      ? Math.round((activity.mastery_after - activity.mastery_before) * 10) / 10
      : null;
  const codes = activity.diagnosis_codes ?? [];

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 pb-24 md:pb-8">
      <div className="mx-auto max-w-2xl space-y-6">
        <div className="rounded-2xl border border-border bg-white p-6 shadow-card text-center">
          <p className="text-[10px] font-mono uppercase tracking-widest text-primary">Mission clear</p>
          <h1 className="font-display text-2xl font-black text-text-primary mt-1">{mission.title}</h1>
          <p className="mt-2 text-3xl tracking-widest" aria-label={`${stars} of 5 stars`}>
            {"★".repeat(stars)}
            <span className="opacity-30">{"★".repeat(5 - stars)}</span>
          </p>
          <div className="mt-4 grid grid-cols-3 gap-3">
            <div className="rounded-xl bg-surface-2 border border-black/5 p-3">
              <p className="text-[10px] font-mono uppercase text-text-muted">Score</p>
              <p className="font-display text-lg font-black">{Math.round(activity.score)}</p>
            </div>
            <div className="rounded-xl bg-surface-2 border border-black/5 p-3">
              <p className="text-[10px] font-mono uppercase text-text-muted">◆ Diamonds</p>
              <p className="font-display text-lg font-black">+{activity.diamonds}</p>
            </div>
            <div className="rounded-xl bg-surface-2 border border-black/5 p-3">
              <p className="text-[10px] font-mono uppercase text-text-muted">Mastery Δ</p>
              <p className="font-display text-lg font-black">
                {masteryDelta == null ? "—" : `${masteryDelta > 0 ? "+" : ""}${masteryDelta}`}
              </p>
            </div>
          </div>
          <p className="mt-2 font-mono text-[11px] text-text-muted">
            {activity.passed ? "Passed" : "Not passed"} · server-recorded{activity.xp_applied === false ? " (reward pending)" : ""}
          </p>
        </div>

        {codes.length > 0 && (
          <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
            <h2 className="section-header text-lg mb-2">Diagnosis</h2>
            <div className="flex flex-wrap gap-2">
              {codes.map((c) => (
                <span key={c} className="rounded-full border border-amber-200 bg-amber-50 px-3 py-1 font-mono text-[11px] text-amber-800">
                  {c}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <h2 className="section-header text-lg mb-1">Next</h2>
          <p className="text-xs text-text-muted font-mono mb-4">
            Your Journey re-ranks from this evidence — continue to see the backend-decided next mission.
          </p>
          <div className="flex flex-wrap gap-2">
            <button onClick={() => navigate("/journey")} className="btn-primary text-sm inline-flex items-center gap-2">
              Continue → <ArrowRight size={14} />
            </button>
            <Link to="/skills" className="btn-secondary text-sm">
              View skills
            </Link>
            <button onClick={() => navigate(-1)} className="btn-ghost text-sm inline-flex items-center gap-2">
              <RotateCcw size={12} /> Back
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
