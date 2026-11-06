import { useState, useEffect, useCallback } from "react";
import { useParams, Link, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  CheckCircle2,
  XCircle,
  Lightbulb,
  BookOpen,
  Trophy,
  Loader2,
  ChevronRight,
} from "lucide-react";
import api from "../services/api";

type Step = {
  step_number: number;
  step_type: "explain" | "interactive" | "practice" | "assessment";
  title: string;
  content?: string;
  example?: string;
  formula?: string;
  tip?: string;
  prompt?: string;
  options?: string[];
  correct_index?: number;
  explanation?: string;
};

type LessonContent = {
  id: string;
  slug: string;
  title: string;
  domain: string;
  difficulty: string;
  duration_min: number;
  xp_reward: number;
  mastery_threshold: number;
  steps: Step[];
  practice_questions: string[];
  assessment: {
    questions: Step[];
    mastery_threshold: number;
    duration_sec: number;
  };
  srs_cards: Array<{ type: string; question: string; answer: string }>;
};

type AnswerResult = {
  correct: boolean;
  explanation: string;
} | null;

export default function LessonPlayer() {
  const { slug } = useParams();
  const [searchParams] = useSearchParams();
  const lessonSlug = slug || "successive_percentage_change";
  const trackId = searchParams.get("track_id") || undefined;
  const moduleId = searchParams.get("module_id") || undefined;

  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const [phase, setPhase] = useState<"learn" | "assessment">("learn");
  const [assessmentAnswers, setAssessmentAnswers] = useState<Record<string, number>>({});
  const [assessmentResult, setAssessmentResult] = useState<any>(null);
  const [assessmentError, setAssessmentError] = useState("");
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [answerResult, setAnswerResult] = useState<AnswerResult>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [completionData, setCompletionData] = useState<any>(null);
  const [saving, setSaving] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);
  const [attemptedCount, setAttemptedCount] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setCurrentStep(0);
    setPhase("learn");
    setAssessmentAnswers({});
    setAssessmentResult(null);
    setAssessmentError("");
    setSelectedAnswer(null);
    setAnswerResult(null);
    setShowExplanation(false);
    setCompleted(false);
    setCompletionData(null);
    setCorrectCount(0);
    setAttemptedCount(0);

    api.companyLessons
      .getLesson(lessonSlug)
      .then((res: any) => {
        if (!cancelled && res?.data) {
          setLesson(res.data);
        }
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

  const handleAnswer = useCallback(
    (index: number) => {
      if (!lesson || answerResult !== null) return;
      const step = lesson.steps[currentStep];
      if (step.step_type !== "interactive" && step.step_type !== "practice") return;
      if (step.correct_index == null) return;

      setSelectedAnswer(index);
      setAttemptedCount((c) => c + 1);
      const correct = index === step.correct_index;
      if (correct) {
        setCorrectCount((c) => c + 1);
      }
      setAnswerResult({
        correct,
        explanation: step.explanation || "",
      });
      setShowExplanation(true);
    },
    [lesson, currentStep, answerResult]
  );

  const goNext = useCallback(() => {
    if (!lesson) return;
    if (currentStep < lesson.steps.length - 1) {
      setCurrentStep((s) => s + 1);
      setSelectedAnswer(null);
      setAnswerResult(null);
      setShowExplanation(false);
    } else {
      setPhase("assessment");
      setAssessmentError("");
    }
  }, [lesson, currentStep]);

  const goBack = useCallback(() => {
    if (phase === "assessment") {
      setPhase("learn");
      setAssessmentResult(null);
      setAssessmentError("");
      return;
    }
    if (currentStep > 0) {
      setCurrentStep((s) => s - 1);
      setSelectedAnswer(null);
      setAnswerResult(null);
      setShowExplanation(false);
    }
  }, [currentStep, phase]);

  const handleComplete = useCallback(async () => {
    if (!lesson || saving) return;
    setSaving(true);
    setAssessmentError("");
    try {
      const res: any = await api.companyLessons.complete(lessonSlug, {
        answers: assessmentAnswers,
        time_spent_seconds: 0,
        ...(trackId && moduleId ? { track_id: trackId, module_id: moduleId } : {}),
      });
      const result = res?.data || null;
      setAssessmentResult(result);
      if (result?.passed) {
        setCompletionData(result);
        setCompleted(true);
      } else {
        setAssessmentError(
          `You scored ${result?.score ?? 0}%. You need ${result?.mastery_threshold ?? 70}% to pass. Review the explanations and retry.`
        );
      }
    } catch (error: any) {
      setAssessmentError(error?.message || "Assessment submission failed. Please try again.");
    } finally {
      setSaving(false);
    }
  }, [lesson, lessonSlug, assessmentAnswers, trackId, moduleId, saving]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <Loader2 className="h-8 w-8 animate-spin text-brand-sky" />
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-10 text-center">
        <h1 className="text-2xl font-bold mb-2">Lesson not found</h1>
        <p className="text-text-secondary mb-4">
          The lesson "{lessonSlug}" could not be loaded.
        </p>
        <Link to="/learn" className="text-brand-sky hover:underline">
          Back to Learn
        </Link>
      </div>
    );
  }

  if (completed) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl border border-white/10 bg-surface-base/80 p-6 text-center"
        >
          <Trophy className="mx-auto h-12 w-12 text-yellow-400 mb-3" />
          <h1 className="text-2xl font-bold mb-2">Lesson Complete!</h1>
          <p className="text-text-secondary mb-1">{lesson.title}</p>
          <p className="text-sm text-text-secondary mb-4">
            {completionData?.passed
              ? "You passed! Keep practicing to master this pattern."
              : "Keep practicing. Review the explanation and try again."}
          </p>
          {completionData && (
            <p className="text-sm text-brand-sky mb-4">
              XP earned: {completionData.xp_earned || lesson.xp_reward}
            </p>
          )}
          <div className="flex justify-center gap-3">
            <Link
              to="/learn"
              className="rounded-xl border border-white/10 px-4 py-2 text-sm hover:bg-white/5"
            >
              Back to Learn
            </Link>
            <button
              onClick={() => {
                setCurrentStep(0);
                setSelectedAnswer(null);
                setAnswerResult(null);
                setShowExplanation(false);
                setCompleted(false);
                setCompletionData(null);
                setCorrectCount(0);
                setAttemptedCount(0);
              }}
              className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90"
            >
              Review Again
            </button>
          </div>
        </motion.div>
      </div>
    );
  }

  if (phase === "assessment") {
    const questions = lesson.assessment?.questions || [];
    const allAnswered = questions.length > 0 && questions.every((_, index) => assessmentAnswers[String(index)] !== undefined);
    return (
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="mb-6">
          <Link to="/learn" className="inline-flex items-center gap-1 text-xs text-text-secondary hover:text-text-primary">
            <ArrowLeft size={12} /> Learn
          </Link>
          <p className="mt-3 text-[10px] font-mono uppercase tracking-wider text-brand-sky">Final mastery check</p>
          <h1 className="mt-1 text-2xl font-bold">{lesson.title}</h1>
          <p className="mt-1 text-sm text-text-secondary">
            Answer all {questions.length} questions. Pass mark: {Math.round(lesson.assessment.mastery_threshold * 100)}%.
          </p>
        </div>

        {assessmentError && (
          <div role="alert" className="mb-4 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">
            {assessmentError}
          </div>
        )}

        <div className="space-y-4">
          {questions.map((question, index) => {
            const result = assessmentResult?.results?.find((item: any) => item.index === index);
            const chosen = assessmentAnswers[String(index)];
            return (
              <section key={index} className="rounded-2xl border border-white/10 bg-surface-base/80 p-5">
                <p className="mb-3 text-[10px] font-mono uppercase tracking-wider text-brand-sky">Question {index + 1}</p>
                <h2 className="mb-4 text-base font-semibold text-text-primary">{question.prompt || question.title}</h2>
                <div className="space-y-2">
                  {(question.options || []).map((option, optionIndex) => {
                    const isCorrect = result && result.correct_index === optionIndex;
                    const isChosen = chosen === optionIndex;
                    const style = result
                      ? isCorrect
                        ? "border-green-500/50 bg-green-500/10 text-green-200"
                        : isChosen
                          ? "border-red-500/50 bg-red-500/10 text-red-200"
                          : "border-white/5 bg-white/5 text-text-secondary"
                      : isChosen
                        ? "border-brand-sky/50 bg-brand-sky/10 text-brand-sky"
                        : "border-white/10 hover:border-white/20 hover:bg-white/5";
                    return (
                      <button
                        key={optionIndex}
                        type="button"
                        disabled={!!assessmentResult}
                        onClick={() => setAssessmentAnswers((previous) => ({ ...previous, [String(index)]: optionIndex }))}
                        className={`w-full rounded-xl border px-4 py-3 text-left text-sm transition-all ${style}`}
                      >
                        <span className="mr-2 font-mono text-xs">{String.fromCharCode(65 + optionIndex)}.</span>
                        {option}
                        {result && isCorrect && <CheckCircle2 className="ml-2 inline h-4 w-4 text-green-400" />}
                        {result && isChosen && !result.correct && <XCircle className="ml-2 inline h-4 w-4 text-red-400" />}
                      </button>
                    );
                  })}
                </div>
                {result?.explanation && (
                  <p className="mt-3 rounded-lg bg-white/5 p-3 text-xs leading-relaxed text-text-secondary">{result.explanation}</p>
                )}
              </section>
            );
          })}
        </div>

        {assessmentResult && !assessmentResult.passed && (
          <button
            type="button"
            onClick={() => {
              setAssessmentAnswers({});
              setAssessmentResult(null);
              setAssessmentError("");
            }}
            className="mt-5 rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-3 text-sm font-semibold text-amber-200"
          >
            Retry assessment
          </button>
        )}

        <div className="mt-6 flex items-center justify-between gap-3">
          <button type="button" onClick={goBack} className="rounded-xl border border-white/10 px-4 py-3 text-sm hover:bg-white/5">
            <ArrowLeft size={14} className="mr-1 inline" /> Back to lesson
          </button>
          <button
            type="button"
            onClick={handleComplete}
            disabled={!allAnswered || saving || !!assessmentResult}
            className="rounded-xl bg-brand-sky px-5 py-3 text-sm font-bold text-white disabled:cursor-not-allowed disabled:opacity-40"
          >
            {saving ? <Loader2 className="inline h-4 w-4 animate-spin" /> : "Submit assessment"}
          </button>
        </div>
      </div>
    );
  }

  const step = lesson.steps[currentStep];
  const progress = ((currentStep + 1) / (lesson.steps.length + 1)) * 100;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <div>
            <Link
              to="/learn"
              className="text-xs text-text-secondary hover:text-text-primary inline-flex items-center gap-1"
            >
              <ArrowLeft size={12} />
              Learn
            </Link>
            <h1 className="text-xl font-bold mt-1">{lesson.title}</h1>
            <p className="text-xs text-text-secondary">
              {lesson.domain} · {lesson.difficulty} · {lesson.duration_min} min
            </p>
          </div>
          <div className="text-right">
            <p className="text-xs text-text-secondary">
              Step {currentStep + 1}/{lesson.steps.length + 1}
            </p>
            <p className="text-xs text-brand-sky">+{lesson.xp_reward} XP</p>
          </div>
        </div>
        <div className="h-2 rounded-full bg-white/5 overflow-hidden">
          <motion.div
            className="h-full bg-brand-sky"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          transition={{ duration: 0.2 }}
          className="rounded-2xl border border-white/10 bg-surface-base/80 p-6"
        >
          <div className="flex items-start justify-between gap-3 mb-4">
            <div>
              <span className="text-[10px] font-mono uppercase tracking-wider text-brand-sky">
                {step.step_type}
              </span>
              <h2 className="text-lg font-bold mt-1">{step.title}</h2>
            </div>
            {step.step_type === "interactive" || step.step_type === "practice" ? (
              <Lightbulb className="h-5 w-5 text-yellow-400 shrink-0" />
            ) : (
              <BookOpen className="h-5 w-5 text-brand-sky shrink-0" />
            )}
          </div>

          {step.content && (
            <p className="text-sm leading-relaxed text-text-primary mb-4">
              {step.content}
            </p>
          )}

          {step.example && (
            <div className="rounded-xl border border-white/5 bg-white/5 p-4 mb-4">
              <p className="text-xs font-mono text-brand-secondary">{step.example}</p>
            </div>
          )}

          {step.formula && (
            <div className="rounded-xl border border-brand-sky/30 bg-brand-sky/10 p-4 mb-4">
              <p className="text-sm font-mono text-brand-sky">{step.formula}</p>
            </div>
          )}

          {step.tip && (
            <div className="rounded-xl border border-yellow-500/30 bg-yellow-500/10 p-3 mb-4">
              <p className="text-xs text-yellow-200">💡 {step.tip}</p>
            </div>
          )}

          {(step.step_type === "interactive" || step.step_type === "practice") &&
            step.options && (
              <div className="space-y-2 mb-4">
                {step.options.map((opt, idx) => {
                  const isSelected = selectedAnswer === idx;
                  const isCorrect = step.correct_index === idx;
                  let cls =
                    "w-full text-left rounded-xl border px-4 py-3 text-sm transition-all ";
                  if (showExplanation) {
                    if (isCorrect) {
                      cls += "border-green-500/50 bg-green-500/10 text-green-300";
                    } else if (isSelected && !isCorrect) {
                      cls += "border-red-500/50 bg-red-500/10 text-red-300";
                    } else {
                      cls += "border-white/5 bg-white/5 text-text-secondary";
                    }
                  } else {
                    cls += isSelected
                      ? "border-brand-sky/50 bg-brand-sky/10 text-brand-sky"
                      : "border-white/10 hover:border-white/20 hover:bg-white/5";
                  }

                  return (
                    <button
                      key={idx}
                      onClick={() => handleAnswer(idx)}
                      disabled={showExplanation}
                      className={cls}
                    >
                      <span className="font-mono mr-2 text-xs">
                        {String.fromCharCode(65 + idx)}.
                      </span>
                      {opt}
                      {showExplanation && isCorrect && (
                        <CheckCircle2 className="inline ml-2 h-4 w-4 text-green-400" />
                      )}
                      {showExplanation && isSelected && !isCorrect && (
                        <XCircle className="inline ml-2 h-4 w-4 text-red-400" />
                      )}
                    </button>
                  );
                })}
              </div>
            )}

          {showExplanation && answerResult && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`rounded-xl border p-4 mb-4 ${
                answerResult.correct
                  ? "border-green-500/30 bg-green-500/10"
                  : "border-red-500/30 bg-red-500/10"
              }`}
            >
              <p
                className={`text-sm ${
                  answerResult.correct ? "text-green-300" : "text-red-300"
                }`}
              >
                {answerResult.explanation}
              </p>
            </motion.div>
          )}

          <div className="flex items-center justify-between mt-4">
            <button
              onClick={goBack}
              disabled={currentStep === 0}
              className="rounded-xl border border-white/10 px-4 py-2 text-sm disabled:opacity-30 hover:bg-white/5"
            >
              <ArrowLeft size={14} className="inline mr-1" />
              Back
            </button>

            <div className="flex items-center gap-2 text-xs text-text-secondary">
              <span>
                {correctCount}/{attemptedCount} practice checks correct
              </span>
            </div>

            <button
              onClick={goNext}
              disabled={saving}
              className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90 disabled:opacity-50"
            >
              {saving ? (
                <Loader2 className="inline h-4 w-4 animate-spin" />
              ) : currentStep === lesson.steps.length - 1 ? (
                <>
                  Finish <Trophy size={14} className="inline ml-1" />
                </>
              ) : (
                <>
                  Next <ChevronRight size={14} className="inline ml-1" />
                </>
              )}
            </button>
          </div>
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
