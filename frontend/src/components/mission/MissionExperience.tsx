// @ts-nocheck
import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ArrowLeft, ArrowRight, CheckCircle2, Play, Timer } from "lucide-react";
import useReducedMotion from "../../hooks/useReducedMotion";
import { missionApi } from "../../services/api/missions";
import Spinner from "../ui/Spinner";
import InteractionHost from "./InteractionHost";
import { getMission, type MissionMCQ, type MissionStage } from "../../data/missions/patterns";

/**
 * Universal mission renderer (ADR: BOUNTYCODE_CURRICULUM_STRUCTURE).
 *
 * Canonical stage vocabulary (backend STEP_TYPES):
 *   discover → manipulate → predict → build → break → debug → retrieve → transfer → mastery
 *
 * Composition chrome (not teaching stages): intro, practice, recognize (→predict),
 * prove (→mastery/timed_prove).
 *
 * Interaction subtypes live under stage.interaction.kind — never as top-level
 * step types. Only the mastery/prove stage posts the graded mission event
 * (idempotency key per attempt). Add content, never pages.
 */

const STAGE_ORDER = [
  "intro",
  "discover",
  "recognize",
  "manipulate",
  "predict",
  "build",
  "practice",
  "break",
  "debug",
  "retrieve",
  "transfer",
  "prove",
  "mastery",
] as const;

const STAGE_LABELS: Record<string, string> = {
  intro: "Intro",
  discover: "Discover",
  recognize: "Recognize",
  manipulate: "Manipulate",
  predict: "Predict",
  build: "Build",
  practice: "Practice",
  break: "Break",
  debug: "Debug",
  retrieve: "Retrieve",
  transfer: "Transfer",
  prove: "Prove",
  mastery: "Mastery",
};

function isMasteryStage(s: MissionStage): boolean {
  return s.kind === "prove" || s.kind === "mastery";
}

function stageTitle(s: MissionStage): string {
  return s.title || STAGE_LABELS[s.kind] || s.kind;
}

function stageSubtitle(s: MissionStage): string {
  return s.subtitle || "";
}

function isQuizStage(s: MissionStage): boolean {
  return (s.mcqs?.length ?? 0) > 0 && !isMasteryStage(s);
}

function MCQBlock({
  mcq,
  picked,
  setPicked,
  revealed,
}: {
  mcq: MissionMCQ;
  picked: number | null;
  setPicked: (i: number) => void;
  revealed: boolean;
}) {
  return (
    <div>
      <p className="text-[15px] font-semibold text-text-primary leading-snug">{mcq.q}</p>
      {mcq.code && (
        <pre className="mt-3 overflow-x-auto rounded-xl bg-gray-950 p-3 font-mono text-[12px] leading-relaxed text-cyan-300">
          {mcq.code}
        </pre>
      )}
      <div className="mt-3 space-y-2">
        {mcq.options.map((o, i) => {
          const isRight = revealed && i === mcq.correct;
          const isWrongPick = revealed && picked === i && i !== mcq.correct;
          return (
            <button
              key={i}
              onClick={() => !revealed && setPicked(i)}
              disabled={revealed}
              className={`min-h-[48px] w-full rounded-xl border px-3 py-3 text-left text-sm transition-colors ${
                isRight
                  ? "border-emerald-500 bg-emerald-50 font-semibold"
                  : isWrongPick
                    ? "border-red-400 bg-red-50"
                    : picked === i
                      ? "border-primary/60 bg-primary/5"
                      : "border-black/10 bg-white"
              }`}
            >
              {o}
            </button>
          );
        })}
      </div>
      {revealed && (
        <p className={`mt-2 text-[13px] ${picked === mcq.correct ? "text-emerald-700" : "text-red-600"}`}>
          {picked === mcq.correct ? "Correct. " : "Not quite. "}
          {mcq.explain}
        </p>
      )}
    </div>
  );
}

function StageShell({
  title,
  subtitle,
  children,
  aside,
}: {
  title: string;
  subtitle: string;
  children?: React.ReactNode;
  aside?: React.ReactNode;
}) {
  return (
    <section className="rounded-3xl border border-default bg-card p-5">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <h2 className="font-display text-xl font-black">{title}</h2>
          <p className="mt-1 text-sm text-text-muted">{subtitle}</p>
        </div>
        {aside}
      </div>
      {children && <div className="mt-3">{children}</div>}
    </section>
  );
}

export default function MissionExperience({ missionId }: { missionId: string }) {
  const navigate = useNavigate();
  const reduced = useReducedMotion();
  const mission = getMission(missionId);

  const [stage, setStage] = useState<number>(0);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [revealed, setRevealed] = useState<Record<string, boolean>>({});
  const proveStage = mission?.stages.find((s) => isMasteryStage(s));
  const proveLimit = proveStage?.timeLimitSeconds ?? 180;
  const [proveLeft, setProveLeft] = useState(proveLimit);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const attemptKey = useRef(
    typeof crypto !== "undefined" && "randomUUID" in crypto
      ? crypto.randomUUID()
      : `${Date.now()}-${Math.random().toString(36).slice(2)}`,
  );
  const startRef = useRef(Date.now());

  useEffect(() => {
    if (!mission || !mission.stages[stage] || !isMasteryStage(mission.stages[stage])) return;
    if (proveLeft <= 0) {
      void submitProve(true);
      return;
    }
    const t = setTimeout(() => setProveLeft((s) => s - 1), 1000);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stage, proveLeft, mission]);

  if (!mission) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4">
        <div className="text-center">
          <p className="font-bold text-text-primary">Mission not found</p>
          <p className="font-mono text-xs text-text-muted mt-1">{missionId}</p>
          <Link to="/journey" className="btn-primary text-sm mt-4 inline-block">
            Back to Journey
          </Link>
        </div>
      </div>
    );
  }

  const current = mission.stages[stage];
  const proveMCQs = proveStage?.mcqs ?? [];
  const passScore = proveStage?.passScore ?? 60;

  const canAdvance = (): boolean => {
    if (isMasteryStage(current)) return true;
    if (!isQuizStage(current)) return true;
    const mcq = current.mcqs![0];
    return answers[mcq.id] != null;
  };

  const next = () => {
    if (!canAdvance()) return;
    setStage((s) => Math.min(s + 1, mission.stages.length - 1));
    window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
  };

  const submitProve = async (timedOut = false) => {
    if (submitting || !proveStage) return;
    setSubmitting(true);
    setSubmitError(null);
    const codes = new Set<string>();
    let correct = 0;
    proveMCQs.forEach((q) => {
      if (answers[q.id] === q.correct) correct++;
      else codes.add(q.codeIfMissed);
    });
    if (timedOut) codes.add("TIME_MANAGEMENT");

    mission.stages.forEach((s) => {
      if (isMasteryStage(s)) return;
      const q = s.mcqs?.[0];
      if (!q) return;
      const picked = answers[q.id];
      if (picked == null) return;
      if (picked !== q.correct) codes.add(q.codeIfMissed);
    });

    const score = proveMCQs.length ? Math.round((correct / proveMCQs.length) * 100) : 0;
    try {
      const res = (await missionApi.recordActivity({
        lesson_id: mission.skillId,
        activity_type: "practice",
        score,
        passed: score >= passScore,
        time_spent_seconds: Math.round((Date.now() - startRef.current) / 1000),
        diagnosis_codes: [...codes],
        metadata: {
          mission_id: mission.id,
          mission_title: mission.title,
          attempt_uuid: attemptKey.current,
          prove_time_limit: proveLimit,
        },
      })) as any;
      const activity = res?.data ?? res;
      navigate(`/mission/${mission.id.replace(/_/g, "-")}/result`, {
        state: {
          mission: {
            id: mission.id,
            kind: "lesson",
            title: mission.title,
            description: `Proven under time in ~${mission.estimatedMinutes} min.`,
            skill_id: mission.skillId,
            estimated_minutes: mission.estimatedMinutes,
            to: "/practice",
            to_label: "Keep practicing",
            status: "completed",
          },
          activity,
        },
      });
    } catch (e) {
      setSubmitError(
        e instanceof Error ? e.message : "Could not record evidence — your answers are safe, retry.",
      );
    } finally {
      setSubmitting(false);
    }
  };

  const mm = String(Math.floor(proveLeft / 60)).padStart(1, "0");
  const ss = String(proveLeft % 60).padStart(2, "0");
  const kindRank = (k: string) => STAGE_ORDER.indexOf(k as (typeof STAGE_ORDER)[number]);
  const currentRank = kindRank(current.kind);
  const hasSequence = (s: MissionStage) => (s.sequence?.length ?? 0) > 0;
  const hasJudge = (s: MissionStage) => !!s.judgeTo;
  const hasInteraction = (s: MissionStage) =>
    !!s.interaction || !!s.component || hasJudge(s);

  return (
    <div className="min-h-screen bg-base px-4 pb-32 pt-4 md:pb-16">
      <div className="mx-auto w-full max-w-xl space-y-4">
        <div className="flex items-center justify-between gap-2">
          <Link to="/journey" className="inline-flex min-h-[44px] items-center gap-1 font-mono text-xs text-text-muted">
            <ArrowLeft size={14} /> Journey
          </Link>
          <span className="font-mono text-[11px] text-text-muted">
            {stageTitle(current)} · {stage + 1}/{mission.stages.length}
          </span>
        </div>

        <div
          className="h-2 overflow-hidden rounded-full bg-black/10"
          role="progressbar"
          aria-valuenow={stage + 1}
          aria-valuemin={1}
          aria-valuemax={mission.stages.length}
        >
          <motion.div
            className="h-full rounded-full bg-gradient-to-r from-orange-500 to-amber-400"
            animate={{ width: `${((stage + 1) / mission.stages.length) * 100}%` }}
            transition={reduced ? { duration: 0 } : { type: "spring", stiffness: 120, damping: 20 }}
          />
        </div>

        <AnimatePresence mode="wait">
          {current.kind === "intro" && (
            <motion.section
              key="intro"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
              className="rounded-3xl border border-orange-200/60 bg-[#FFF7F2] p-5 shadow-sm"
            >
              <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#E8590C]">⚔ Bounty briefing</p>
              <h1 className="font-display mt-1 text-3xl font-black text-gray-900">{mission.title}</h1>
              {mission.why && (
                <div className="mt-3 rounded-xl border border-orange-200 bg-white/80 p-3 text-sm text-gray-700 shadow-sm">
                  <span className="font-bold text-orange-700">Why this?</span> {mission.why}
                </div>
              )}
              <p className="mt-2 text-sm leading-relaxed text-gray-600">{mission.briefing}</p>
              <div className="mt-3 flex flex-wrap gap-2 font-mono text-[11px] text-gray-500">
                <span className="rounded-full border border-black/10 bg-white px-2.5 py-1">⏱ ~{mission.estimatedMinutes} min</span>
                <span className="rounded-full border border-black/10 bg-white px-2.5 py-1">🎯 {mission.skillId}</span>
                <span className="rounded-full border border-black/10 bg-white px-2.5 py-1">◆ server-awarded XP</span>
              </div>
              {(current.interaction || current.mcqs) && (
                <div className="mt-4">
                  {current.interaction && (
                    <InteractionHost stage={current} skillId={mission.skillId} />
                  )}
                  {current.mcqs?.[0] && (
                    <div className="mt-3">
                      <MCQBlock
                        mcq={current.mcqs[0]}
                        picked={answers[current.mcqs[0].id] ?? null}
                        setPicked={(i) => {
                          setAnswers((a) => ({ ...a, [current.mcqs![0].id]: i }));
                          setRevealed((r) => ({ ...r, [current.mcqs![0].id]: true }));
                        }}
                        revealed={!!revealed[current.mcqs[0].id]}
                      />
                    </div>
                  )}
                </div>
              )}
            </motion.section>
          )}

          {current.kind !== "intro" &&
            !isMasteryStage(current) &&
            !hasSequence(current) &&
            (hasInteraction(current) || isQuizStage(current) || currentRank >= 0) && (
            <motion.section
              key={`stage-${stage}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.18 }}
              className="rounded-3xl border border-default bg-card p-5 shadow-sm"
            >
              <StageShell
                title={stageTitle(current)}
                subtitle={stageSubtitle(current)}
                aside={
                  current.interaction?.kind ? (
                    <span className="shrink-0 rounded-full bg-surface-2 px-2 py-1 font-mono text-[10px] text-text-muted">
                      {current.interaction.kind}
                    </span>
                  ) : null
                }
              >
                {hasInteraction(current) && (
                  <div className="mb-3">
                    <InteractionHost stage={current} skillId={mission.skillId} />
                  </div>
                )}
                {current.judgeTo && (
                  <Link
                    to={current.judgeTo}
                    className="inline-flex min-h-[48px] items-center gap-2 rounded-xl border border-black/10 bg-white px-4 text-sm font-semibold"
                  >
                    <Play size={14} /> {current.judgeLabel ?? "Solve on the judge"}
                  </Link>
                )}
                {isQuizStage(current) && (
                  <div className={hasInteraction(current) || current.judgeTo ? "mt-3" : ""}>
                    <MCQBlock
                      mcq={current.mcqs![0]}
                      picked={answers[current.mcqs![0].id] ?? null}
                      setPicked={(i) => {
                        setAnswers((a) => ({ ...a, [current.mcqs![0].id]: i }));
                        setRevealed((r) => ({ ...r, [current.mcqs![0].id]: true }));
                      }}
                      revealed={!!revealed[current.mcqs![0].id]}
                    />
                  </div>
                )}
              </StageShell>
            </motion.section>
          )}

          {hasSequence(current) && (
            <motion.section
              key={`seq-${stage}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.18 }}
            >
              <StageShell title={stageTitle(current)} subtitle={stageSubtitle(current)}>
                <div className="space-y-3">
                  {current.sequence!.map((lvl) => (
                    <div key={lvl.level} className="rounded-2xl border border-black/5 bg-surface-2 p-3">
                      <p className="mb-2 font-mono text-[10px] uppercase tracking-widest text-text-muted">{lvl.level}</p>
                      <div className="space-y-2">
                        {lvl.items.map((it) => (
                          <Link
                            key={it.to}
                            to={it.to}
                            className="flex min-h-[48px] items-center justify-between gap-2 rounded-xl border border-black/10 bg-white px-3 py-2.5 text-sm font-semibold"
                          >
                            {it.label} <ArrowRight size={14} className="shrink-0 text-text-muted" />
                          </Link>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
                <p className="mt-2 font-mono text-[11px] text-text-muted">
                  Solves post real evidence to {mission.skillId} — then come back and Prove.
                </p>
              </StageShell>
            </motion.section>
          )}

          {isMasteryStage(current) && (
            <motion.section
              key="mastery"
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="rounded-3xl border border-orange-200/60 bg-gradient-to-b from-orange-50 to-white p-5 shadow-sm"
            >
              <div className="flex items-center justify-between">
                <h2 className="font-display text-xl font-black text-gray-900">{stageTitle(current)}</h2>
                <span
                  className={`inline-flex items-center gap-1 rounded-full px-3 py-1.5 font-mono text-xs font-bold ${
                    proveLeft < 30 ? "bg-red-100 text-red-700" : "bg-black/5 text-text-secondary"
                  }`}
                >
                  <Timer size={12} /> {mm}:{ss}
                </span>
              </div>
              <p className="mt-1 text-sm text-text-muted">{stageSubtitle(current) || "Timed prove. All questions required."}</p>
              <div className="mt-4 space-y-5">
                {proveMCQs.map((q, qi) => (
                  <div key={q.id} className="rounded-2xl border border-black/5 bg-surface-2 p-3">
                    <p className="mb-2 font-mono text-[10px] uppercase tracking-widest text-text-muted">Q{qi + 1}</p>
                    <MCQBlock
                      mcq={q}
                      picked={answers[q.id] ?? null}
                      setPicked={(i) => setAnswers((a) => ({ ...a, [q.id]: i }))}
                      revealed={false}
                    />
                  </div>
                ))}
              </div>
              {submitError && (
                <p className="mt-3 rounded-xl border border-red-200 bg-red-50 p-3 text-xs text-red-700">{submitError}</p>
              )}
            </motion.section>
          )}
        </AnimatePresence>

        <div
          className="fixed inset-x-0 bottom-0 z-40 border-t border-black/10 bg-white/95 px-4 pt-3 backdrop-blur md:static md:rounded-2xl md:border"
          style={{ paddingBottom: "max(0.75rem, env(safe-area-inset-bottom))" }}
        >
          <div className="mx-auto flex w-full max-w-xl gap-2">
            <button
              onClick={() => setStage((s) => Math.max(0, s - 1))}
              disabled={stage === 0}
              className="inline-flex min-h-[48px] flex-1 items-center justify-center gap-1 rounded-xl border border-black/10 text-sm font-semibold disabled:opacity-40"
            >
              <ArrowLeft size={15} /> Back
            </button>
            {!isMasteryStage(current) ? (
              <button
                onClick={next}
                className="inline-flex min-h-[48px] flex-[2] items-center justify-center gap-1 rounded-xl bg-[#F4532F] text-sm font-bold text-white shadow-lg shadow-orange-500/20"
              >
                Continue <ArrowRight size={15} />
              </button>
            ) : (
              <button
                onClick={() => void submitProve(false)}
                disabled={submitting || proveMCQs.some((q) => answers[q.id] == null)}
                className="inline-flex min-h-[48px] flex-[2] items-center justify-center gap-1 rounded-xl bg-[#F4532F] text-sm font-bold text-white shadow-lg shadow-orange-500/20 disabled:opacity-40"
              >
                {submitting ? <Spinner size={15} /> : <CheckCircle2 size={15} />} Complete & record
              </button>
            )}
          </div>
          {isMasteryStage(current) && proveMCQs.some((q) => answers[q.id] == null) && (
            <p className="mx-auto mt-1 w-full max-w-xl text-center font-mono text-[11px] text-text-muted">
              Answer all {proveMCQs.length} to submit.
            </p>
          )}
          {isQuizStage(current) && answers[current.mcqs![0].id] == null && (
            <p className="mx-auto mt-1 w-full max-w-xl text-center font-mono text-[11px] text-text-muted">
              Pick an answer to continue — wrong answers are data, not failure.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
