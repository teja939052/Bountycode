import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowLeft, ArrowRight, CheckCircle2, Play, Timer } from "lucide-react";
import PatternTracer from "../components/interactivity/PatternTracer";
import ExplainAloud from "../components/interactivity/ExplainAloud";
import CodeFillInTheBlank from "../components/interactivity/CodeFillInTheBlank";
import useReducedMotion from "../hooks/useReducedMotion";
import { missionApi } from "../services/api/missions";
import Spinner from "../components/ui/Spinner";

/**
 * Sliding Window flagship mission (World 1).
 *
 * ONE guided experience on the proven roads: Discover → Manipulate →
 * Predict → Build → Break → Debug → Transfer → Prove → MISSION CLEAR.
 * Interactive stages reuse the existing components (they post their own
 * graded evidence); only Prove posts the mission-graded event with an
 * idempotency key. No new backend, no new XP paths.
 */
const SKILL_ID = "dsa.sliding_window";
const STORE_KEY = "swm.step.v1";
const PROVE_SECONDS = 180;

type MCQ = { id: string; q: string; code?: string; options: string[]; correct: number; explain: string; codeIfMissed: string };

const PREDICT: MCQ = {
  id: "predict",
  q: "Trace it in your head first — what is best after the loop?",
  code: "arr = [2, 1, 5, 1, 3]\nk = 3\nwindow_sum = sum(arr[:k])  # 8\nbest = window_sum\nfor right in range(k, len(arr)):\n    window_sum += arr[right] - arr[right - k]\n    best = max(best, window_sum)",
  options: ["9", "8", "7", "6"],
  correct: 0,
  explain: "right=3: 8+1−2=7 (best 8). right=4: 7+3−1=9 (best 9).",
  codeIfMissed: "CONCEPT_GAP",
};

const BREAK_Q: MCQ = {
  id: "break",
  q: "This code returns 12 instead of 9 on [2,1,5,1,3], k=3. What broke?",
  code: "def max_window_sum(arr, k):\n    window_sum = sum(arr[:k])\n    best = window_sum\n    for right in range(k, len(arr)):\n        window_sum += arr[right]\n        best = max(best, window_sum)\n    return best",
  options: [
    "best starts too low",
    "Old elements never leave — arr[right-k] is never subtracted, the sum grows forever",
    "range should start at 0",
    "max() should be min()",
  ],
  correct: 1,
  explain: "A window must slide both ways: +arr[right], −arr[right−k]. Without the subtraction it is a growing prefix sum.",
  codeIfMissed: "DEBUGGING",
};

const DEBUG_Q: MCQ = {
  id: "debug",
  q: "Fix it — which line belongs inside the loop after adding arr[right]?",
  options: [
    "window_sum -= arr[right - k]",
    "window_sum += arr[right - k]",
    "window_sum = sum(arr[:k])",
    "left += k",
  ],
  correct: 0,
  explain: "Subtract the element falling out of the window's left edge.",
  codeIfMissed: "IMPLEMENTATION_ERROR",
};

const TRANSFER_Q: MCQ = {
  id: "transfer",
  q: "New context, same pattern: longest substring without repeating characters. When do you move left?",
  options: [
    "When s[right] is already inside the current window",
    "After every 3 steps",
    "Only at the end",
    "Never — left stays at 0",
  ],
  correct: 0,
  explain: "Variable windows shrink exactly when the constraint breaks — here, a duplicate appears.",
  codeIfMissed: "TRANSFER_FAILURE",
};

const PROVE_QS: MCQ[] = [
  {
    id: "prove-1",
    q: "k=3 over [2,1,5,1,3]. Maximum window sum?",
    options: ["8", "7", "9", "6"],
    correct: 2,
    explain: "[2,1,5]=8, [1,5,1]=7, [5,1,3]=9.",
    codeIfMissed: "CONCEPT_GAP",
  },
  {
    id: "prove-2",
    q: "Time complexity of fixed sliding-window max?",
    options: ["O(n)", "O(n log n)", "O(n·k)", "O(k)"],
    correct: 0,
    explain: "Each element enters and leaves once.",
    codeIfMissed: "COMPLEXITY_ERROR",
  },
  {
    id: "prove-3",
    q: "Variable window: when to shrink from the left?",
    options: ["When the window violates its constraint", "Always after k steps", "When the sum is too large", "At each step"],
    correct: 0,
    explain: "Shrink on constraint violation — duplicates, sum over target, too many distinct.",
    codeIfMissed: "PATTERN_RECOGNITION",
  },
];

const STAGES = ["Intro", "Discover", "Manipulate", "Predict", "Build", "Break", "Debug", "Transfer", "Prove"] as const;

function MCQBlock({ mcq, picked, setPicked, revealed }: { mcq: MCQ; picked: number | null; setPicked: (i: number) => void; revealed: boolean }) {
  return (
    <div>
      <p className="text-[15px] font-semibold text-text-primary leading-snug">{mcq.q}</p>
      {mcq.code && (
        <pre className="mt-3 rounded-xl bg-gray-950 p-3 font-mono text-[12px] leading-relaxed text-cyan-300 overflow-x-auto">{mcq.code}</pre>
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
          {picked === mcq.correct ? "Correct. " : "Not quite. "}{mcq.explain}
        </p>
      )}
    </div>
  );
}

export default function SlidingWindowMission() {
  const navigate = useNavigate();
  const reduced = useReducedMotion();
  const [stage, setStage] = useState<number>(() => {
    try {
      return Math.min(Number(localStorage.getItem(STORE_KEY) ?? 0), STAGES.length - 1);
    } catch {
      return 0;
    }
  });
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [revealed, setRevealed] = useState<Record<string, boolean>>({});
  const [proveLeft, setProveLeft] = useState(PROVE_SECONDS);
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const attemptKey = useRef(
    typeof crypto !== "undefined" && "randomUUID" in crypto ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2)}`,
  );
  const startRef = useRef(Date.now());

  useEffect(() => {
    try {
      localStorage.setItem(STORE_KEY, String(stage));
    } catch { /* private mode */ }
  }, [stage]);

  // Prove countdown — auto-submit on timeout (TIME_MANAGEMENT evidence).
  useEffect(() => {
    if (stage !== 8) return;
    if (proveLeft <= 0) {
      void submitProve(true);
      return;
    }
    const t = setTimeout(() => setProveLeft((s) => s - 1), 1000);
    return () => clearTimeout(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [stage, proveLeft]);

  const stageMCQ: Record<number, MCQ> = useMemo(
    () => ({ 3: PREDICT, 5: BREAK_Q, 6: DEBUG_Q, 7: TRANSFER_Q }),
    [],
  );

  const checkMCQ = (n: number) => {
    if (n === 8) return true;
    const mcq = stageMCQ[n];
    if (!mcq) return true; // non-quiz stages advance freely
    if (answers[mcq.id] == null) return false;
    setRevealed((r) => ({ ...r, [mcq.id]: true }));
    return true;
  };

  const next = () => {
    if (!checkMCQ(stage)) return;
    setStage((s) => Math.min(s + 1, STAGES.length - 1));
    window.scrollTo({ top: 0, behavior: reduced ? "auto" : "smooth" });
  };

  const submitProve = async (timedOut = false) => {
    if (submitting) return;
    setSubmitting(true);
    setSubmitError(null);
    const codes = new Set<string>();
    let correct = 0;
    PROVE_QS.forEach((q) => {
      if (answers[q.id] === q.correct) correct++;
      else codes.add(q.codeIfMissed);
    });
    if (timedOut) codes.add("TIME_MANAGEMENT");
    const score = Math.round((correct / PROVE_QS.length) * 100);
    try {
      const res = (await missionApi.recordActivity({
        type: "practice",
        skill_id: SKILL_ID,
        passed: score >= 60,
        score,
        attempts: 1,
        time_spent: Math.round((Date.now() - startRef.current) / 1000),
        hints_used: 0,
        diagnosis_codes: [...codes],
        source: "sliding_window_mission",
        idempotency_key: attemptKey.current,
      })) as any;
      const activity = res?.data ?? res;
      try {
        localStorage.removeItem(STORE_KEY);
      } catch { /* ignore */ }
      navigate("/mission/sliding-window/result", {
        state: {
          mission: {
            id: "sliding-window",
            kind: "lesson",
            title: "Sliding Window",
            description: "Fixed + variable windows, proven under time.",
            skill_id: SKILL_ID,
            estimated_minutes: 18,
            to: "/pattern/sliding-window",
            to_label: "Review pattern",
            status: "completed",
          },
          activity,
        },
      });
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : "Could not record evidence — your answers are safe, retry.");
    } finally {
      setSubmitting(false);
    }
  };

  const mm = String(Math.floor(proveLeft / 60)).padStart(1, "0");
  const ss = String(proveLeft % 60).padStart(2, "0");

  return (
    <div className="min-h-screen bg-base px-4 pb-28 pt-4 md:pb-12">
      <div className="mx-auto w-full max-w-xl space-y-4">
        <div className="flex items-center justify-between gap-2">
          <Link to="/journey" className="inline-flex min-h-[44px] items-center gap-1 font-mono text-xs text-text-muted">
            <ArrowLeft size={14} /> Journey
          </Link>
          <span className="font-mono text-[11px] text-text-muted">
            {STAGES[stage]} · {stage + 1}/{STAGES.length}
          </span>
        </div>

        <div className="h-2 overflow-hidden rounded-full bg-black/10" role="progressbar" aria-valuenow={stage + 1} aria-valuemin={1} aria-valuemax={STAGES.length}>
          <motion.div
            className="h-full rounded-full bg-gradient-to-r from-orange-500 to-amber-400"
            animate={{ width: `${((stage + 1) / STAGES.length) * 100}%` }}
            transition={reduced ? { duration: 0 } : { type: "spring", stiffness: 120, damping: 20 }}
          />
        </div>
        <div className="flex gap-1.5 overflow-x-auto pb-1" aria-label="Stages">
          {STAGES.map((s, i) => (
            <button
              key={s}
              onClick={() => i <= stage && setStage(i)}
              className={`shrink-0 rounded-full px-2.5 py-1.5 font-mono text-[10px] ${
                i === stage ? "bg-[#14141B] text-white" : i < stage ? "bg-emerald-100 text-emerald-800" : "bg-black/5 text-text-muted"
              }`}
            >
              {s}
            </button>
          ))}
        </div>

        {stage === 0 && (
          <section className="rounded-3xl border border-orange-200/60 bg-[#FFF7F2] p-5 shadow-sm">
            <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#E8590C]">⚡ Mission briefing</p>
            <h1 className="font-display mt-1 text-3xl font-black text-gray-900">Sliding Window</h1>
            <p className="mt-2 text-sm leading-relaxed text-gray-600">
              Brute force re-sums every window — O(n·k). The window slides: one element enters, one leaves,
              each index touched twice. That is the whole trick, and it buys you O(n).
            </p>
            <div className="mt-3 flex flex-wrap gap-2 font-mono text-[11px] text-gray-500">
              <span className="rounded-full border border-black/10 bg-white px-2.5 py-1">⏱ ~18 min</span>
              <span className="rounded-full border border-black/10 bg-white px-2.5 py-1">🎯 dsa.sliding_window</span>
              <span className="rounded-full border border-black/10 bg-white px-2.5 py-1">◆ server-awarded XP</span>
            </div>
          </section>
        )}

        {stage === 1 && (
          <section className="rounded-3xl border border-default bg-card p-5">
            <h2 className="font-display text-xl font-black">Discover — say it in your words</h2>
            <p className="mt-1 text-sm text-text-muted">Why does the window stay O(n)? Type it. Keyword match, not a speech grade.</p>
            <div className="mt-3"><ExplainAloud /></div>
          </section>
        )}

        {stage === 2 && (
          <section className="rounded-3xl border border-default bg-card p-5">
            <h2 className="font-display text-xl font-black">Manipulate — drag the window</h2>
            <p className="mt-1 text-sm text-text-muted">Step through. Watch left chase right. Feel the O(n).</p>
            <div className="mt-3"><PatternTracer /></div>
          </section>
        )}

        {[3, 5, 6, 7].includes(stage) && (
          <section className="rounded-3xl border border-default bg-card p-5">
            <h2 className="font-display text-xl font-black">
              {stage === 3 && "Predict — no running it first"}
              {stage === 5 && "Break — find the bug"}
              {stage === 6 && "Debug — fix it"}
              {stage === 7 && "Transfer — new disguise"}
            </h2>
            <div className="mt-3">
              <MCQBlock
                mcq={stageMCQ[stage]}
                picked={answers[stageMCQ[stage].id] ?? null}
                setPicked={(i) => {
                  setAnswers((a) => ({ ...a, [stageMCQ[stage].id]: i }));
                  setRevealed((r) => ({ ...r, [stageMCQ[stage].id]: true }));
                }}
                revealed={!!revealed[stageMCQ[stage].id]}
              />
            </div>
          </section>
        )}

        {stage === 4 && (
          <section className="rounded-3xl border border-default bg-card p-5">
            <h2 className="font-display text-xl font-black">Build — write the shrink</h2>
            <p className="mt-1 text-sm text-text-muted">Choose the line, then prove it on the real judge.</p>
            <div className="mt-3"><CodeFillInTheBlank /></div>
            <Link to="/problems?topic=sliding-window" className="mt-3 inline-flex min-h-[48px] items-center gap-2 rounded-xl border border-black/10 bg-white px-4 text-sm font-semibold">
              <Play size={14} /> Solve on the judge
            </Link>
          </section>
        )}

        {stage === 8 && (
          <section className="rounded-3xl border border-default bg-card p-5">
            <div className="flex items-center justify-between">
              <h2 className="font-display text-xl font-black">Prove — timed</h2>
              <span className={`inline-flex items-center gap-1 rounded-full px-3 py-1.5 font-mono text-xs font-bold ${proveLeft < 30 ? "bg-red-100 text-red-700" : "bg-black/5 text-text-secondary"}`}>
                <Timer size={12} /> {mm}:{ss}
              </span>
            </div>
            <p className="mt-1 text-sm text-text-muted">3 questions. ≥60 to pass. Timeout submits automatically.</p>
            <div className="mt-4 space-y-5">
              {PROVE_QS.map((q, qi) => (
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
          </section>
        )}

        <div className="fixed inset-x-0 bottom-0 z-40 border-t border-black/10 bg-white/95 px-4 pt-3 backdrop-blur md:static md:rounded-2xl md:border" style={{ paddingBottom: "max(0.75rem, env(safe-area-inset-bottom))" }}>
          <div className="mx-auto flex w-full max-w-xl gap-2">
            <button
              onClick={() => setStage((s) => Math.max(0, s - 1))}
              disabled={stage === 0}
              className="inline-flex min-h-[48px] flex-1 items-center justify-center gap-1 rounded-xl border border-black/10 text-sm font-semibold disabled:opacity-40"
            >
              <ArrowLeft size={15} /> Back
            </button>
            {stage < 8 ? (
              <button
                onClick={next}
                className="inline-flex min-h-[48px] flex-[2] items-center justify-center gap-1 rounded-xl bg-[#F4532F] text-sm font-bold text-white"
              >
                Continue <ArrowRight size={15} />
              </button>
            ) : (
              <button
                onClick={() => void submitProve(false)}
                disabled={submitting || PROVE_QS.some((q) => answers[q.id] == null)}
                className="inline-flex min-h-[48px] flex-[2] items-center justify-center gap-1 rounded-xl bg-[#F4532F] text-sm font-bold text-white disabled:opacity-40"
              >
                {submitting ? <Spinner size={15} /> : <CheckCircle2 size={15} />} Complete & record
              </button>
            )}
          </div>
          {stage === 8 && PROVE_QS.some((q) => answers[q.id] == null) && (
            <p className="mx-auto mt-1 w-full max-w-xl text-center font-mono text-[11px] text-text-muted">Answer all 3 to submit.</p>
          )}
          {[3, 5, 6, 7].includes(stage) && answers[stageMCQ[stage].id] == null && (
            <p className="mx-auto mt-1 w-full max-w-xl text-center font-mono text-[11px] text-text-muted">Pick an answer to continue — wrong answers are data, not failure.</p>
          )}
        </div>
      </div>
    </div>
  );
}
