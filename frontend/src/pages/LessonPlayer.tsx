import { useState, useEffect, useCallback, useRef } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { useParams, Link, useSearchParams } from "react-router-dom";
import {
  ArrowLeft,
  CheckCircle2,
  XCircle,
  Loader2,
  ChevronRight,
  ChevronLeft,
  Code2,
} from "lucide-react";
import api from "../services/api";
import { LessonStepHints } from "../components/academy/LessonStepHints";

type Step = {
  step_number?: number;
  step_type: string;
  title: string;
  content?: string;
  prompt?: string;
  options?: string[];
  correct_order?: number[];
  explanation?: string;
  tip?: string;
  formula?: string;
  example?: string;
  code?: string;
  language?: string;
  starter_code?: string;
  expected_answer?: string;
  answer_placeholder?: string;
  hints?: string[];
};

type LessonContent = {
  slug?: string;
  title: string;
  domain?: string;
  mastery_threshold?: number;
  steps: Step[];
  assessment?: {
    questions: Array<{ prompt?: string; question?: string; options?: string[]; explanation?: string }>;
    mastery_threshold?: number;
  };
  next_lesson_slug?: string;
  next_lesson_title?: string;
};

const MCQ_TYPES = new Set(["interactive", "practice", "quiz", "debug_choice", "api_scenario"]);
const TEXT_TYPES = new Set(["code_lab", "predict_output", "fill_blank", "short_answer"]);
const ORDER_TYPES = new Set(["order_steps"]);

function normalizeText(value: string) {
  return value.trim().replace(/\s+/g, " ").toLowerCase();
}

/**
 * Progressive Academy lesson player (Coddy/scrim style).
 * Answers are graded on the server when possible. Hints never award mastery.
 */
export default function LessonPlayer() {
  const { slug } = useParams();
  const [searchParams] = useSearchParams();
  const queryClient = useQueryClient();
  const lessonSlug = slug || "successive_percentage_change";
  const trackId = searchParams.get("track_id") || undefined;
  const moduleId = searchParams.get("module_id") || undefined;
  const topicId = searchParams.get("topic_id") || undefined;

  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const [phase, setPhase] = useState<"learn" | "assessment" | "done">("learn");
  const [selected, setSelected] = useState<number | null>(null);
  const [textAnswer, setTextAnswer] = useState("");
  const [orderPick, setOrderPick] = useState<number[]>([]);
  const [feedback, setFeedback] = useState<{ correct: boolean; explanation: string } | null>(null);
  const [stepError, setStepError] = useState("");
  const [saving, setSaving] = useState(false);
  const [assessmentAnswers, setAssessmentAnswers] = useState<Record<string, number>>({});
  const [assessmentResult, setAssessmentResult] = useState<any>(null);
  const [assessmentError, setAssessmentError] = useState("");
  const startedAt = useRef(Date.now());

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setLesson(null);
    setCurrentStep(0);
    setPhase("learn");
    setSelected(null);
    setTextAnswer("");
    setOrderPick([]);
    setFeedback(null);
    setAssessmentAnswers({});
    setAssessmentResult(null);
    setAssessmentError("");
    startedAt.current = Date.now();

    Promise.all([
      api.companyLessons.getLesson(lessonSlug),
      api.companyLessons.getProgress(lessonSlug).catch(() => null),
    ])
      .then(([lessonRes, progressRes]: [any, any]) => {
        if (cancelled || !lessonRes?.data) return;
        const data = lessonRes.data as LessonContent;
        const steps = data.steps || [];
        const saved = Number(progressRes?.data?.current_step ?? 0);
        const restored = Number.isFinite(saved)
          ? Math.max(0, Math.min(saved, Math.max(steps.length - 1, 0)))
          : 0;
        setLesson(data);
        setCurrentStep(restored);
      })
      .catch(() => {
        if (!cancelled) setLesson(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [lessonSlug]);

  useEffect(() => {
    if (!lesson) return;
    const t = window.setTimeout(() => {
      api.companyLessons.saveProgress(lessonSlug, currentStep).catch(() => {});
    }, 300);
    return () => window.clearTimeout(t);
  }, [lesson, lessonSlug, currentStep]);

  const step = lesson?.steps?.[currentStep];

  const resetStepLocal = () => {
    setSelected(null);
    setTextAnswer(step?.starter_code || "");
    setOrderPick([]);
    setFeedback(null);
    setStepError("");
  };

  useEffect(() => {
    if (!step) return;
    setSelected(null);
    setTextAnswer(step.starter_code || "");
    setOrderPick([]);
    setFeedback(null);
    setStepError("");
  }, [currentStep, step?.step_type, step?.starter_code]);

  const checkMcq = useCallback(
    async (index: number) => {
      if (!lesson || !step || feedback || saving) return;
      if (!MCQ_TYPES.has(step.step_type)) return;
      setSelected(index);
      setStepError("");
      setSaving(true);
      try {
        const res: any = await api.companyLessons.answerStep(lessonSlug, currentStep, index);
        const data = res?.data;
        if (!data) throw new Error("Could not grade this answer.");
        setFeedback({
          correct: Boolean(data.correct),
          explanation: [data.feedback, data.explanation].filter(Boolean).join("\n\n") || "",
        });
        void queryClient.invalidateQueries({ queryKey: ["adaptive"] });
      } catch (err: any) {
        setSelected(null);
        setStepError(err?.message || "Could not check this answer.");
      } finally {
        setSaving(false);
      }
    },
    [lesson, step, feedback, saving, lessonSlug, currentStep, queryClient],
  );

  const checkText = async () => {
    if (!lesson || !step || feedback || saving) return;
    if (!TEXT_TYPES.has(step.step_type)) return;
    const answer = textAnswer.trim();
    if (!answer) {
      setStepError("Enter your answer or code before checking.");
      return;
    }
    setStepError("");
    setSaving(true);
    try {
      // Prefer server grading when API accepts string answers; fall back to local expected_answer.
      let graded: { correct: boolean; explanation: string } | null = null;
      try {
        const res: any = await api.companyLessons.answerStep(lessonSlug, currentStep, answer as any);
        if (res?.data) {
          graded = {
            correct: Boolean(res.data.correct),
            explanation: [res.data.feedback, res.data.explanation].filter(Boolean).join("\n\n") || "",
          };
        }
      } catch {
        graded = null;
      }
      if (!graded && step.expected_answer != null) {
        const ok = normalizeText(answer) === normalizeText(String(step.expected_answer));
        graded = {
          correct: ok,
          explanation: ok
            ? step.explanation || "Correct."
            : step.explanation || `Expected something like: ${step.expected_answer}`,
        };
      }
      if (!graded) {
        setStepError("This step could not be graded yet. Try the multiple-choice practice steps.");
        return;
      }
      setFeedback(graded);
      void queryClient.invalidateQueries({ queryKey: ["adaptive"] });
    } finally {
      setSaving(false);
    }
  };

  const checkOrder = async () => {
    if (!lesson || !step || feedback || saving) return;
    if (!ORDER_TYPES.has(step.step_type)) return;
    const options = step.options || [];
    if (orderPick.length !== options.length) {
      setStepError("Tap every step in the correct order.");
      return;
    }
    setSaving(true);
    setStepError("");
    try {
      let graded: { correct: boolean; explanation: string } | null = null;
      try {
        const res: any = await api.companyLessons.answerStep(lessonSlug, currentStep, orderPick as any);
        if (res?.data) {
          graded = {
            correct: Boolean(res.data.correct),
            explanation: [res.data.feedback, res.data.explanation].filter(Boolean).join("\n\n") || "",
          };
        }
      } catch {
        graded = null;
      }
      if (!graded && Array.isArray(step.correct_order)) {
        const ok =
          orderPick.length === step.correct_order.length &&
          orderPick.every((v, i) => v === step.correct_order![i]);
        graded = {
          correct: ok,
          explanation: ok ? step.explanation || "Correct order." : step.explanation || "Not the right order — try again.",
        };
      }
      if (!graded) {
        setStepError("Could not grade this ordering step.");
        return;
      }
      setFeedback(graded);
    } finally {
      setSaving(false);
    }
  };

  const toggleOrder = (index: number) => {
    if (feedback) return;
    setOrderPick((prev) => {
      if (prev.includes(index)) return prev.filter((x) => x !== index);
      return [...prev, index];
    });
  };

  const goNext = () => {
    if (!lesson || !step) return;
    const mustAttempt =
      MCQ_TYPES.has(step.step_type) || TEXT_TYPES.has(step.step_type) || ORDER_TYPES.has(step.step_type);
    if (mustAttempt && !feedback) {
      setStepError("Try this step before continuing. You will get feedback after your answer.");
      return;
    }
    if (currentStep < lesson.steps.length - 1) {
      setCurrentStep((s) => s + 1);
      resetStepLocal();
    } else {
      setPhase("assessment");
      setAssessmentError("");
    }
  };

  const goBack = () => {
    if (phase === "assessment") {
      setPhase("learn");
      setAssessmentError("");
      return;
    }
    if (currentStep > 0) {
      setCurrentStep((s) => s - 1);
    }
  };

  const submitAssessment = async () => {
    if (!lesson || saving) return;
    const questions = lesson.assessment?.questions || [];
    if (questions.length && Object.keys(assessmentAnswers).length < questions.length) {
      setAssessmentError("Answer every question before submitting.");
      return;
    }
    setSaving(true);
    setAssessmentError("");
    try {
      const res: any = await api.companyLessons.complete(lessonSlug, {
        answers: assessmentAnswers,
        time_spent_seconds: Math.max(0, Math.floor((Date.now() - startedAt.current) / 1000)),
        ...(trackId && moduleId ? { track_id: trackId, module_id: moduleId, topic_id: topicId } : {}),
      });
      const result = res?.data || null;
      setAssessmentResult(result);
      if (result?.passed) {
        setPhase("done");
        await Promise.all([
          queryClient.invalidateQueries({ queryKey: ["study", "today"] }),
          queryClient.invalidateQueries({ queryKey: ["adaptive"] }),
          queryClient.invalidateQueries({ queryKey: ["journey", "state"] }),
        ]);
      } else {
        setAssessmentError(
          `You scored ${result?.score ?? 0}%. You need ${result?.mastery_threshold ?? 70}% to pass. Review and retry.`,
        );
      }
    } catch (err: any) {
      setAssessmentError(err?.message || "Assessment submission failed.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-950 text-slate-300">
        <Loader2 className="animate-spin mr-2" size={20} /> Loading lesson…
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 text-slate-200 gap-3 px-4">
        <p>Lesson not found.</p>
        <Link to="/academy" className="text-emerald-400 font-semibold">
          ← Back to Academy
        </Link>
      </div>
    );
  }

  if (phase === "done") {
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center px-4">
        <div className="max-w-md w-full rounded-2xl border border-emerald-500/30 bg-slate-900 p-6 text-center">
          <CheckCircle2 className="mx-auto text-emerald-400 mb-3" size={40} />
          <h1 className="text-xl font-black">Lesson mastered</h1>
          <p className="mt-2 text-sm text-slate-400">
            Score {assessmentResult?.score ?? "—"}% · evidence saved to your skill graph.
          </p>
          <div className="mt-6 flex flex-col gap-2">
            {lesson.next_lesson_slug && (
              <Link
                to={`/learn/lesson/${lesson.next_lesson_slug}`}
                className="rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white"
              >
                Next: {lesson.next_lesson_title || lesson.next_lesson_slug}
              </Link>
            )}
            <Link to="/dashboard" className="rounded-xl border border-slate-600 px-4 py-2.5 text-sm font-semibold">
              Dashboard
            </Link>
            <Link to="/academy" className="text-sm text-slate-400 hover:text-slate-200">
              Academy
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (phase === "assessment") {
    const questions = lesson.assessment?.questions || [];
    return (
      <div className="min-h-screen bg-slate-950 text-slate-100">
        <div className="mx-auto max-w-2xl px-4 py-8">
          <button type="button" onClick={goBack} className="mb-4 inline-flex items-center gap-1 text-sm text-slate-400">
            <ChevronLeft size={16} /> Back to lesson
          </button>
          <h1 className="text-2xl font-black">Final check · {lesson.title}</h1>
          <p className="mt-1 text-sm text-slate-400">
            Server-graded. Mastery threshold{" "}
            {Math.round((lesson.assessment?.mastery_threshold ?? lesson.mastery_threshold ?? 0.7) * 100)}%.
          </p>
          <ol className="mt-6 space-y-5">
            {questions.map((q, qi) => (
              <li key={qi} className="rounded-2xl border border-slate-700 bg-slate-900/80 p-4">
                <p className="font-semibold text-sm">
                  {qi + 1}. {q.prompt || q.question}
                </p>
                <div className="mt-3 space-y-2">
                  {(q.options || []).map((opt, oi) => (
                    <button
                      key={oi}
                      type="button"
                      onClick={() => setAssessmentAnswers((prev) => ({ ...prev, [String(qi)]: oi }))}
                      className={`w-full text-left rounded-xl border px-3 py-2 text-sm ${
                        assessmentAnswers[String(qi)] === oi
                          ? "border-emerald-500 bg-emerald-500/10"
                          : "border-slate-700 hover:border-slate-500"
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </li>
            ))}
          </ol>
          {assessmentError && (
            <p className="mt-4 rounded-lg border border-rose-500/40 bg-rose-500/10 p-3 text-sm text-rose-200">
              {assessmentError}
            </p>
          )}
          <button
            type="button"
            disabled={saving}
            onClick={() => void submitAssessment()}
            className="mt-6 w-full rounded-xl bg-emerald-600 py-3 text-sm font-bold text-white disabled:opacity-50"
          >
            {saving ? "Grading…" : "Submit assessment"}
          </button>
        </div>
      </div>
    );
  }

  const progressPct = lesson.steps.length
    ? Math.round(((currentStep + 1) / lesson.steps.length) * 100)
    : 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-2xl px-4 py-6">
        <div className="mb-4 flex items-center justify-between gap-3">
          <Link to="/academy" className="inline-flex items-center gap-1 text-sm text-slate-400 hover:text-white">
            <ArrowLeft size={16} /> Academy
          </Link>
          <span className="text-xs text-slate-500">
            Step {currentStep + 1} / {lesson.steps.length}
          </span>
        </div>
        <div className="mb-4 h-1.5 rounded-full bg-slate-800">
          <div className="h-full rounded-full bg-emerald-500 transition-all" style={{ width: `${progressPct}%` }} />
        </div>
        <p className="text-[11px] font-bold uppercase tracking-wider text-emerald-500/90">{lesson.domain || "Lesson"}</p>
        <h1 className="mt-1 text-2xl font-black">{lesson.title}</h1>

        {step && (
          <div className="mt-6 rounded-2xl border border-slate-700 bg-slate-900/60 p-5">
            <div className="flex items-center gap-2">
              {TEXT_TYPES.has(step.step_type) && <Code2 size={16} className="text-sky-400" />}
              <h2 className="text-lg font-bold">{step.title}</h2>
            </div>
            {step.content && (
              <p className="mt-3 text-sm leading-relaxed text-slate-300 whitespace-pre-wrap">{step.content}</p>
            )}
            {step.formula && (
              <p className="mt-3 rounded-lg border border-sky-500/30 bg-sky-500/10 px-3 py-2 font-mono text-sm text-sky-200">
                {step.formula}
              </p>
            )}
            {step.example && (
              <p className="mt-3 text-sm text-slate-400">
                <span className="font-semibold text-slate-300">Example: </span>
                {step.example}
              </p>
            )}
            {step.code && (
              <pre className="mt-3 overflow-x-auto rounded-xl border border-slate-700 bg-black/40 p-3 font-mono text-xs text-sky-100">
                {step.code}
              </pre>
            )}
            {step.tip && <p className="mt-3 text-xs text-amber-200/90">💡 {step.tip}</p>}

            <div className="mt-4">
              <LessonStepHints slug={lessonSlug} stepIndex={currentStep} localHints={step.hints || []} />
            </div>

            {step.prompt && <p className="mt-4 text-sm font-semibold">{step.prompt}</p>}

            {MCQ_TYPES.has(step.step_type) && Array.isArray(step.options) && (
              <div className="mt-3 space-y-2">
                {step.options.map((opt, oi) => {
                  const isSelected = selected === oi;
                  const showResult = feedback && isSelected;
                  return (
                    <button
                      key={oi}
                      type="button"
                      disabled={Boolean(feedback) || saving}
                      onClick={() => void checkMcq(oi)}
                      className={`w-full text-left rounded-xl border px-3 py-2.5 text-sm transition ${
                        showResult
                          ? feedback!.correct
                            ? "border-emerald-500 bg-emerald-500/15"
                            : "border-rose-500 bg-rose-500/15"
                          : isSelected
                            ? "border-slate-400"
                            : "border-slate-700 hover:border-slate-500"
                      }`}
                    >
                      {opt}
                    </button>
                  );
                })}
              </div>
            )}

            {TEXT_TYPES.has(step.step_type) && (
              <div className="mt-3 space-y-2">
                <textarea
                  value={textAnswer}
                  onChange={(e) => setTextAnswer(e.target.value)}
                  disabled={Boolean(feedback) || saving}
                  rows={step.step_type === "code_lab" ? 8 : 3}
                  placeholder={step.answer_placeholder || (step.step_type === "code_lab" ? "Write your code…" : "Your answer…")}
                  className="w-full rounded-xl border border-slate-700 bg-black/30 px-3 py-2 font-mono text-sm text-slate-100 outline-none focus:border-emerald-500"
                />
                {!feedback && (
                  <button
                    type="button"
                    disabled={saving}
                    onClick={() => void checkText()}
                    className="rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
                  >
                    {saving ? "Checking…" : "Check answer"}
                  </button>
                )}
              </div>
            )}

            {ORDER_TYPES.has(step.step_type) && Array.isArray(step.options) && (
              <div className="mt-3 space-y-2">
                <p className="text-xs text-slate-400">Tap steps in the correct order. Tap again to undo.</p>
                {step.options.map((opt, oi) => {
                  const rank = orderPick.indexOf(oi);
                  return (
                    <button
                      key={oi}
                      type="button"
                      disabled={Boolean(feedback)}
                      onClick={() => toggleOrder(oi)}
                      className={`flex w-full items-center gap-2 rounded-xl border px-3 py-2.5 text-left text-sm ${
                        rank >= 0 ? "border-emerald-500 bg-emerald-500/10" : "border-slate-700 hover:border-slate-500"
                      }`}
                    >
                      <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-slate-800 text-[11px] font-bold">
                        {rank >= 0 ? rank + 1 : "·"}
                      </span>
                      {opt}
                    </button>
                  );
                })}
                {!feedback && (
                  <button
                    type="button"
                    disabled={saving}
                    onClick={() => void checkOrder()}
                    className="rounded-xl bg-sky-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
                  >
                    {saving ? "Checking…" : "Check order"}
                  </button>
                )}
              </div>
            )}

            {feedback && (
              <div
                className={`mt-4 flex gap-2 rounded-xl border p-3 text-sm ${
                  feedback.correct
                    ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-100"
                    : "border-rose-500/40 bg-rose-500/10 text-rose-100"
                }`}
              >
                {feedback.correct ? <CheckCircle2 size={18} className="shrink-0" /> : <XCircle size={18} className="shrink-0" />}
                <p className="whitespace-pre-wrap">{feedback.explanation || (feedback.correct ? "Correct." : "Not quite.")}</p>
              </div>
            )}

            {stepError && (
              <p className="mt-3 rounded-lg border border-rose-500/30 bg-rose-500/10 p-2 text-xs text-rose-200">{stepError}</p>
            )}
          </div>
        )}

        <div className="mt-6 flex items-center justify-between gap-3">
          <button
            type="button"
            onClick={goBack}
            disabled={currentStep === 0}
            className="inline-flex items-center gap-1 rounded-xl border border-slate-700 px-4 py-2 text-sm disabled:opacity-40"
          >
            <ChevronLeft size={16} /> Back
          </button>
          <button
            type="button"
            onClick={goNext}
            className="inline-flex items-center gap-1 rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white"
          >
            {currentStep >= lesson.steps.length - 1 ? "Final assessment" : "Continue"}
            <ChevronRight size={16} />
          </button>
        </div>
        <p className="mt-4 text-center text-[11px] text-slate-500">
          Progress is evidence-based. Hints help you learn — they never grant mastery.
        </p>
      </div>
    </div>
  );
}
