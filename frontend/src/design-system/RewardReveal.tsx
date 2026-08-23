import { useEffect, useState } from "react";
import { MentorAvatar } from "./Mentor";
import { TreasureBadge } from "./Progress";

/**
 * RewardReveal — the payoff moment.
 * Shows REAL outcomes: mastery delta, readiness delta, what unlocked next.
 * One beat of gold light + scale-in. No confetti storms.
 */

export interface RewardRevealData {
  /** e.g. "Arrays & Hashing" */
  skillName: string;
  /** mastery before → after (0-100) */
  masteryBefore: number;
  masteryAfter: number;
  /** readiness before → after (0-100), optional */
  readinessBefore?: number;
  readinessAfter?: number;
  xpEarned: number;
  /** names of missions/nodes unlocked by this win */
  unlocks: string[];
  /** deterministic message from Captain Byte based on outcome size */
  mentorLine?: string;
}

interface RewardRevealProps {
  data: RewardRevealData;
  onContinue: () => void;
}

function Delta({ before, after }: { before: number; after: number }) {
  const delta = after - before;
  if (delta <= 0) return null;
  return (
    <span className="ml-1.5 rounded-full bg-primary-soft px-1.5 py-0.5 text-[11px] font-bold text-primary-dark">
      +{delta}
    </span>
  );
}

export function RewardReveal({ data, onContinue }: RewardRevealProps) {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    const t1 = setTimeout(() => setPhase(1), 350);
    const t2 = setTimeout(() => setPhase(2), 900);
    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  }, []);

  // Deterministic mentor line by mastery jump size
  const gain = data.masteryAfter - data.masteryBefore;
  const line =
    data.mentorLine ??
    (gain >= 20
      ? "That's a treasure haul. The next island is within reach."
      : gain >= 10
        ? "Solid work. Mastery is built one bounty at a time."
        : "Every rep counts. Keep sailing.");

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-canvas/90 p-4 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-label="Bounty complete"
      onClick={onContinue}
    >
      {/* Single gold light beat */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 transition-opacity duration-700"
        style={{
          background:
            "radial-gradient(ellipse at 50% 35%, rgba(234,183,77,0.18), transparent 60%)",
          opacity: phase >= 1 ? 1 : 0,
        }}
      />

      <div
        className="surface-bg relative w-full max-w-md rounded-3xl border border-reward/40 p-8 text-center shadow-modal"
        style={{
          animation: "scaleIn 400ms ease-out both",
          transform: phase >= 1 ? "translateY(0)" : "translateY(12px)",
          transition: "transform 500ms ease-out",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="mb-4 flex justify-center">
          <TreasureBadge size={64} />
        </div>

        <p className="adventure-label mx-auto w-fit">Bounty Collected</p>
        <h2 className="font-display mt-2 text-2xl font-extrabold text-text">{data.skillName}</h2>

        <div
          className="mt-6 grid grid-cols-3 gap-3 transition-all duration-500"
          style={{ opacity: phase >= 1 ? 1 : 0, transform: phase >= 1 ? "none" : "translateY(8px)" }}
        >
          <div className="rounded-xl border border-border bg-surface-2 p-3">
            <p className="text-[10px] font-bold uppercase tracking-wider text-text-muted">Mastery</p>
            <p className="font-display mt-1 text-lg font-extrabold text-text">{data.masteryAfter}%</p>
            <Delta before={data.masteryBefore} after={data.masteryAfter} />
          </div>
          {data.readinessAfter != null && (
            <div className="rounded-xl border border-border bg-surface-2 p-3">
              <p className="text-[10px] font-bold uppercase tracking-wider text-text-muted">Ready</p>
              <p className="font-display mt-1 text-lg font-extrabold text-text">{data.readinessAfter}%</p>
              {data.readinessBefore != null && (
                <Delta before={data.readinessBefore} after={data.readinessAfter} />
              )}
            </div>
          )}
          <div className="rounded-xl border border-border bg-surface-2 p-3">
            <p className="text-[10px] font-bold uppercase tracking-wider text-text-muted">XP</p>
            <p className="font-display mt-1 text-lg font-extrabold text-reward">+{data.xpEarned}</p>
          </div>
        </div>

        {data.unlocks.length > 0 && phase >= 2 && (
          <div className="mt-5 animate-fade-in rounded-xl border border-dashed border-ocean/50 bg-ocean-soft/40 p-4 text-left">
            <p className="text-xs font-bold uppercase tracking-wider text-ocean">Charted Next</p>
            <ul className="mt-2 space-y-1">
              {data.unlocks.slice(0, 4).map((u) => (
                <li key={u} className="flex items-center gap-2 text-sm text-text">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
                    <path
                      d="M5 13l4 4L19 7"
                      stroke="#5BA7A0"
                      strokeWidth="3"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  {u}
                </li>
              ))}
            </ul>
          </div>
        )}

        <div className="mt-6 flex items-center gap-3 rounded-xl bg-surface-2 p-3 text-left">
          <MentorAvatar size={44} mood="proud" />
          <p className="text-sm leading-snug text-text-muted">
            <span className="font-bold text-text">Captain Byte:</span> {line}
          </p>
        </div>

        <button type="button" onClick={onContinue} className="btn btn-primary mt-6 w-full py-3">
          Continue the Voyage
        </button>
      </div>
    </div>
  );
}
