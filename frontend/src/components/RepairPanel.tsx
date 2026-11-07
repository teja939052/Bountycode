import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Wrench, CheckCircle, XCircle, ArrowRight, AlertTriangle } from "lucide-react";
import api from "../services/api";

/**
 * Repair Panel — surfaces the closed-loop repair missions created when an
 * assessment (OA / interview) fails a weakness, and runs a verified-only
 * focused retest so the student can prove capability and advance.
 *
 * Composition only: reads `repair_service` missions + `repair` retest routes.
 * No new systems.
 */
export default function RepairPanel() {
  const [missions, setMissions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeMission, setActiveMission] = useState<any>(null);
  const [retest, setRetest] = useState<{
    skill: string;
    questions: any[];
  } | null>(null);
  const [retestLoading, setRetestLoading] = useState(false);
  const [answers, setAnswers] = useState<Record<string, any>>({});
  const [codeAnswers, setCodeAnswers] = useState<Record<string, string>>({});
  const [submitLoading, setSubmitLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    let alive = true;
    api
      .getRepairMissions()
      .then((data: any) => {
        if (!alive) return;
        setMissions(data?.missions ?? []);
      })
      .catch(() => {
        if (alive) setError("Could not load repair missions.");
      })
      .finally(() => alive && setLoading(false));
    return () => {
      alive = false;
    };
  }, []);

  if (loading) return null;
  if (!missions.length) return null;

  const openRetest = async (mission: any) => {
    const skill = mission?.weaknesses?.[0];
    if (!skill) return;
    setActiveMission(mission);
    setRetest(null);
    setResult(null);
    setAnswers({});
    setCodeAnswers({});
    setRetestLoading(true);
    setError("");
    try {
      const data = await api.getRepairRetest(skill, 3);
      setRetest({ skill, questions: data?.questions ?? [] });
      // Pre-fill coding starters so a coding-only retest is solvable inline.
      const starters: Record<string, string> = {};
      (data?.questions ?? []).forEach((q: any) => {
        if (q?.kind === "code") {
          starters[q.id] = typeof q?.starter_code?.python === "string"
            ? q.starter_code.python
            : "def solve(...):\n    pass";
        }
      });
      setCodeAnswers(starters);
    } catch {
      setError("Could not load retest questions.");
    } finally {
      setRetestLoading(false);
    }
  };

  const submitRetest = async () => {
    if (!retest) return;
    setSubmitLoading(true);
    setError("");
    try {
      const answersArr = retest.questions.map((q: any) =>
        q.kind === "code"
          ? { question_id: q.id, code: codeAnswers[q.id] ?? "", language: "python" }
          : { question_id: q.id, answer: answers[q.id] }
      );
      const data = await api.submitRepairRetest({
        skill: retest.skill,
        answers: answersArr,
      });
      setResult(data);
      if (data?.passed) {
        api
          .completeRepairMission(activeMission?.id)
          .catch(() => undefined);
        setMissions((prev) => prev.filter((m) => m.id !== activeMission?.id));
      }
    } catch {
      setError("Could not submit retest.");
    } finally {
      setSubmitLoading(false);
    }
  };

  const codingQs = retest?.questions.filter((q) => q.kind === "code") ?? [];
  const mcqQs = retest?.questions.filter((q) => q.kind !== "code") ?? [];
  const allAnswered = (retest?.questions ?? []).every((q: any) =>
    q.kind === "code"
      ? (codeAnswers[q.id]?.trim()?.length ?? 0) > 0
      : answers[q.id] !== undefined
  );

  return (
    <motion.div
      className="gamification-card rounded-2xl overflow-hidden"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.15 }}
    >
      <div className="flex items-center gap-2 px-5 pt-5 pb-3">
        <Wrench size={20} className="text-indigo-400" />
        <h2 className="text-base font-bold text-white uppercase tracking-wide">Repair Missions</h2>
        <span className="ml-auto rounded bg-indigo-500/15 px-2 py-0.5 font-mono text-[10px] text-indigo-300">
          {missions.length} pending
        </span>
      </div>
      <p className="px-5 pb-3 font-mono text-xs text-gray-400">
        Close the loop: focused lessons + a verified retest prove you&apos;ve repaired
        the weakness.
      </p>

      {error && (
        <div className="mx-5 mb-3 flex items-center gap-2 rounded bg-red-500/10 px-3 py-2 text-xs text-red-300">
          <AlertTriangle size={14} /> {error}
        </div>
      )}

      <div className="space-y-3 px-5 pb-5">
        {missions.map((m, idx) => (
          <motion.div
            key={m.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.04 }}
            className="rounded-xl border border-white/10 bg-white/5 p-3"
          >
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="font-bold text-sm text-white">
                  {m.title}
                </p>
                <p className="font-mono text-[10px] text-gray-400">
                  {(m.weaknesses ?? []).join(", ")}
                  {m.recommended_lessons?.length
                    ? ` · ${m.recommended_lessons.length} lesson(s)`
                    : ""}
                </p>
              </div>
              <button
                onClick={() => openRetest(m)}
                className="glass-button flex items-center gap-1 whitespace-nowrap text-xs"
              >
                Focus &amp; Retest <ArrowRight size={14} />
              </button>
            </div>
          </motion.div>
        ))}
      </div>

      <AnimatePresence>
        {activeMission && retest && (
          <motion.div
            className="border-t border-white/10 px-5 py-5"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
          >
            {retestLoading ? (
              <p className="font-mono text-xs text-gray-400">Loading retest…</p>
            ) : result ? (
              <motion.div
                initial={{ scale: 0.95, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className={`rounded-xl border p-4 ${
                  result.passed
                    ? "border-emerald-500/30 bg-emerald-500/10"
                    : "border-red-500/30 bg-red-500/10"
                }`}
              >
                <p className="flex items-center gap-2 font-bold text-white">
                  {result.passed ? (
                    <CheckCircle size={18} className="text-emerald-400" />
                  ) : (
                    <XCircle size={18} className="text-red-400" />
                  )}
                  {result.passed ? "Weakness repaired — ready to advance!" : "Keep going — deeper repair scheduled."}
                </p>
                <p className="mt-1 font-mono text-xs text-gray-400">
                  {result.correct}/{result.total} correct ({result.pct}%)
                </p>
              </motion.div>
            ) : (
              <div className="space-y-4">
                <p className="font-mono text-xs text-gray-400">
                  Verified retest for <span className="text-indigo-300">{retest.skill}</span> —
                  pass ≥80% to advance.
                </p>
                {mcqQs.map((q, i) => (
                  <div key={q.id}>
                    <p className="mb-2 text-sm text-white">
                      {i + 1}. {q.question}
                    </p>
                    <div className="space-y-1">
                      {(q.options ?? []).map((opt: any, oi: number) => (
                        <label
                          key={oi}
                          className={`flex cursor-pointer items-center gap-2 rounded-xl border px-3 py-2 text-sm transition-colors ${
                            answers[q.id] === oi
                              ? "border-indigo-500/50 bg-indigo-500/10"
                              : "border-white/10 hover:bg-white/5"
                          }`}
                        >
                          <input
                            type="radio"
                            name={q.id}
                            checked={answers[q.id] === oi}
                            onChange={() =>
                              setAnswers((prev) => ({ ...prev, [q.id]: oi }))
                            }
                            className="accent-indigo-400"
                          />
                          <span className="text-gray-200">{opt}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
                {codingQs.length > 0 && (
                  <div className="space-y-3">
                    <p className="font-mono text-[10px] text-gray-400">
                      {codingQs.length} coding question(s) — the retest invokes
                      your function against the verified test cases.
                    </p>
                    {codingQs.map((q: any, ci: number) => (
                      <div key={q.id}>
                        <p className="mb-2 text-sm text-white">
                          {mcqQs.length + ci + 1}. {q.question}
                        </p>
                        {Array.isArray(q.test_cases) &&
                          q.test_cases.length > 0 && (
                            <p className="mb-1 font-mono text-[10px] text-gray-500">
                              Example input:{" "}
                              {q.test_cases
                                .map((t: any) =>
                                  Array.isArray(t?.input)
                                    ? JSON.stringify(t.input)
                                    : String(t?.input ?? "")
                                )
                                .join("  ·  ")}
                            </p>
                          )}
                        <textarea
                          value={
                            codeAnswers[q.id] ??
                            "def solve(...):\n    pass"
                          }
                          onChange={(e) =>
                            setCodeAnswers((prev) => ({
                              ...prev,
                              [q.id]: e.target.value,
                            }))
                          }
                          spellCheck={false}
                          rows={8}
                          className="w-full rounded-xl border border-white/10 bg-black/30 p-3 font-mono text-xs text-gray-200 outline-none focus:border-indigo-500/50"
                        />
                      </div>
                    ))}
                  </div>
                )}
                <motion.button
                  onClick={submitRetest}
                  disabled={submitLoading || !allAnswered}
                  className="glass-button text-xs disabled:opacity-50 disabled:cursor-not-allowed"
                  whileHover={{ scale: 1.01 }}
                  whileTap={{ scale: 0.99 }}
                >
                  {submitLoading ? "Grading…" : "Submit Retest"}
                </motion.button>
                {!allAnswered && (
                  <p className="font-mono text-[10px] text-amber-300/80">
                    Answer every question to submit the retest.
                  </p>
                )}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
