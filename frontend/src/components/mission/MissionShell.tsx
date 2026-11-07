import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, Play, RefreshCw } from "lucide-react";
import api from "../../services/api";
import Spinner from "../ui/Spinner";
import RepairPanel from "../RepairPanel";
import {
  missionFromJourneyNext,
  missionFromRepairMission,
  stepsForMission,
  type ActivityResult,
  type Mission,
} from "../../types/mission";

/**
 * Universal Mission Shell (V4 Phase 1).
 *
 * ONE renderer for every mission kind. It renders NO content of its own —
 * steps deep-link to the existing engines (lesson player, question bank,
 * verified retest, mock OA, interview, SRS), and completion posts to the
 * canonical sink (POST /api/v1/study/activity → mastery + SRS +
 * record_practice + LearningEvent). Backend decides progression: id "next"
 * resolves from journey/state at render time.
 *
 * Supported ids:
 *   next               → backend-decided next action
 *   repair:<missionId> → persisted repair mission (from /api/v1/repair/missions)
 *   retest:<skill>     → verified-only retest for a weakness skill
 *   level:<world>:<lv> → world level mission (runs in the Journey map)
 */
export default function MissionShell() {
  const { missionId = "next" } = useParams();
  const navigate = useNavigate();
  const [mission, setMission] = useState<Mission | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // One idempotency key per mission attempt (stable across double-clicks,
  // fresh per mount). Replays with this key return the prior result with
  // zero re-award — replaying cannot farm XP or mastery.
  const attemptKey = useRef<string>(
    typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(36).slice(2)}`,
  );
  const [score, setScore] = useState(80);
  const [passed, setPassed] = useState(true);
  const [minutes, setMinutes] = useState(15);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    let alive = true;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        if (missionId === "next") {
          const state = (await api.mission.getJourneyState()) as any;
          const next = state?.next ?? state?.next_action ?? null;
          if (alive) setMission(missionFromJourneyNext(next));
        } else if (missionId.startsWith("repair:")) {
          const id = decodeURIComponent(missionId.slice("repair:".length));
          const data = (await api.mission.listRepairMissions()) as any;
          const list: any[] = data?.missions ?? data ?? [];
          const found = list.find((m) => String(m?.mission_id ?? m?.id) === id);
          if (!found) throw new Error("Repair mission not found");
          if (alive) setMission(missionFromRepairMission(found));
        } else if (missionId.startsWith("retest:")) {
          const skill = decodeURIComponent(missionId.slice("retest:".length));
          if (alive) {
            setMission({
              id: missionId,
              kind: "retest",
              title: `Retest: ${skill}`,
              description: "Verified-only retest — ≥80% to advance, else deeper repair.",
              skill_id: skill,
              estimated_minutes: 15,
              to: `/mission/retest:${encodeURIComponent(skill)}`,
              to_label: "Open retest",
              status: "available",
            });
          }
        } else if (missionId.startsWith("level:")) {
          const [, world, level] = missionId.split(":");
          if (alive) {
            setMission({
              id: missionId,
              kind: "lesson",
              title: level ? `Level: ${level}` : "World level",
              description: world ? `World ${world} — runs in the Journey map.` : "Runs in the Journey map.",
              estimated_minutes: 20,
              to: "/journey",
              to_label: "Open in Journey map",
              status: "available",
            });
          }
        } else {
          throw new Error("Unknown mission");
        }
      } catch (e) {
        if (alive) setError(e instanceof Error ? e.message : "Failed to load mission");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, [missionId]);

  const steps = useMemo(() => (mission ? stepsForMission(mission) : []), [mission]);

  const logEvidence = async () => {
    if (!mission) return;
    setSubmitting(true);
    try {
      const res = (await api.mission.recordActivity({
        type: mission.kind === "lesson" ? "learn" : "practice",
        skill_id: mission.skill_id ?? "general.practice",
        passed,
        score,
        attempts: 1,
        time_spent: minutes * 60,
        source: "mission_shell",
        idempotency_key: attemptKey.current,
      })) as any;
      const activity: ActivityResult = (res?.data ?? res) as ActivityResult;
      navigate(`/mission/${encodeURIComponent(mission.id)}/result`, {
        state: { mission, activity },
      });
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to record evidence");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner />
      </div>
    );
  }

  if (error || !mission) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center">
          <p className="font-bold text-text-primary">Mission unavailable</p>
          <p className="text-sm text-text-muted font-mono mt-1">{error ?? "Unknown error"}</p>
          <Link to="/journey" className="btn-primary text-sm mt-4 inline-flex items-center gap-2">
            <ArrowLeft size={14} /> Back to Journey
          </Link>
        </div>
      </div>
    );
  }

  const isRepair = mission.kind === "repair" || mission.kind === "retest";

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 pb-24 md:pb-8">
      <div className="mx-auto max-w-3xl space-y-6">
        <Link to="/journey" className="text-xs font-mono text-text-muted inline-flex items-center gap-1">
          <ArrowLeft size={12} /> Journey
        </Link>

        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <p className="text-[10px] font-mono uppercase tracking-widest text-primary">
            ⚡ Mission · {mission.kind}
          </p>
          <h1 className="font-display text-2xl font-black text-text-primary mt-1">{mission.title}</h1>
          <p className="text-sm text-text-muted mt-1">{mission.description}</p>
          <div className="mt-3 flex flex-wrap gap-2 font-mono text-[11px] text-text-muted">
            <span className="rounded-full border border-black/10 px-2.5 py-1">⏱ {mission.estimated_minutes} min</span>
            {mission.skill_id && (
              <span className="rounded-full border border-black/10 px-2.5 py-1">🎯 {mission.skill_id}</span>
            )}
            {mission.xp_reward != null && (
              <span className="rounded-full border border-black/10 px-2.5 py-1">◆ {mission.xp_reward} XP quoted</span>
            )}
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            <Link to={mission.to} className="btn-primary text-sm inline-flex items-center gap-2">
              <Play size={14} /> {mission.to_label} →
            </Link>
            <Link to="/practice" className="btn-secondary text-sm">
              Freestyle practice
            </Link>
          </div>
        </div>

        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <h2 className="section-header text-lg mb-3">Mission steps</h2>
          <ol className="space-y-2">
            {steps.map((s, i) => (
              <li key={i} className="flex items-center gap-3 rounded-xl border border-black/5 bg-surface-2 px-3 py-2.5">
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 font-mono text-[11px] font-bold text-primary">
                  {i + 1}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-bold text-text-primary capitalize">{s.label} <span className="font-mono font-normal text-text-muted">· {s.type}</span></p>
                  <p className="text-xs text-text-muted">{s.detail}</p>
                </div>
                {s.to && (
                  <Link to={s.to} className="btn-ghost text-xs inline-flex items-center gap-1 shrink-0">
                    {s.to_label ?? "Open"} <ArrowRight size={12} />
                  </Link>
                )}
              </li>
            ))}
          </ol>
        </div>

        {isRepair && (
          <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
            <h2 className="section-header text-lg mb-3">Repair &amp; retest</h2>
            <RepairPanel />
          </div>
        )}

        <div className="rounded-2xl border border-border bg-white p-5 shadow-card">
          <h2 className="section-header text-lg mb-1">Log evidence</h2>
          <p className="text-xs text-text-muted font-mono mb-4">
            Posts to the canonical sink — server returns the authoritative score, diamonds and mastery.
          </p>
          <div className="grid gap-4 sm:grid-cols-3">
            <label className="text-xs font-mono text-text-secondary">
              Score: {score}
              <input type="range" min={0} max={100} value={score} onChange={(e) => setScore(Number(e.target.value))} className="w-full" />
            </label>
            <label className="text-xs font-mono text-text-secondary">
              Minutes: {minutes}
              <input type="range" min={5} max={120} step={5} value={minutes} onChange={(e) => setMinutes(Number(e.target.value))} className="w-full" />
            </label>
            <label className="text-xs font-mono text-text-secondary flex items-center gap-2">
              <input type="checkbox" checked={passed} onChange={(e) => setPassed(e.target.checked)} />
              Passed
            </label>
          </div>
          <button onClick={logEvidence} disabled={submitting} className="btn-primary text-sm mt-4 inline-flex items-center gap-2">
            {submitting ? <Spinner size={14} /> : <RefreshCw size={14} />} Complete mission &amp; record →
          </button>
        </div>
      </div>
    </div>
  );
}
