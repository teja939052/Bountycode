import { useState, useEffect, useCallback, useRef } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
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
  ChevronUp,
  ChevronDown,
  Play,
  RotateCcw,
  Layers,
} from "lucide-react";
import { compilerApi } from "../services/api/coding";
import api from "../services/api";
import { useBrowserRuntime } from "../hooks/useBrowserRuntime";
import { Card } from "../components/design-system/Card";
import CodeTracer from "../components/learning/CodeTracer";
import LearningResourcesPanel from "../components/learning/LearningResourcesPanel";

type Step = {
  step_number: number;
  step_type: "explain" | "interactive" | "practice" | "assessment" | "predict_output" | "fill_blank" | "order_steps" | "code_lab" | "sql_lab" | "debug_choice" | "api_scenario";
  title: string;
  content?: string;
  example?: string;
  formula?: string;
  tip?: string;
  code?: string;
  language?: string;
  answer_placeholder?: string;
  prompt?: string;
  options?: string[];
  correct_index?: number;
  correct_order?: number[];
  explanation?: string;
  starter_code?: string;
  expected_output?: string;
  schema_preview?: string;
  sample_data?: string;
  request_preview?: string;
  log_output?: string;
  hints?: string[];
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
  learning_objectives?: string[];
  prerequisites?: string[];
  concepts?: string[];
  worked_examples?: Array<{ title: string; input: string; trace: string[]; output: string; explanation: string }>;
  common_misconceptions?: Array<{ misconception: string; correction: string }>;
  company_applications?: Array<{ company: string; skill: string; practice: string }>;
  next_lesson_slug?: string;
  next_lesson_title?: string;
  quest?: {
    chapter?: string;
    rank?: string;
    story?: string;
    mission?: string;
    success_criteria?: string[];
  };
};

type AnswerResult = {
  correct: boolean;
  correctIndex: number | null;
  correctAnswer?: string;
  explanation: string;
  correctOrder?: number[];
  feedback?: string;
  sqlResults?: Array<Record<string, unknown>>;
} | null;

export default function LessonPlayer() {
  const { slug } = useParams();
  const queryClient = useQueryClient();
  const { data: learnerProfileResult } = useQuery({
    queryKey: ["academy", "learner-profile"],
    queryFn: () => api.lessons.progress(),
    staleTime: 5 * 60_000,
    retry: 1,
  });
  const [searchParams] = useSearchParams();
  const lessonSlug = slug || "successive_percentage_change";
  const trackId = searchParams.get("track_id") || undefined;
  const moduleId = searchParams.get("module_id") || undefined;
  const topicId = searchParams.get("topic_id") || undefined;
  const learnerProfile = (learnerProfileResult as any)?.profile;
  const learningPreference = learnerProfile?.learning_preference || "mixed";
  const learningMode = {
    mixed: { label: "Balanced mode", description: "Read the concept, follow a worked example, then practise it." },
    examples_first: { label: "Examples first", description: "Start by understanding a solved example, then connect it to the underlying rule." },
    hands_on: { label: "Hands-on mode", description: "Move quickly into guided steps, code tracing and practice. The reference guide remains available below." },
    visual: { label: "Visual mode", description: "Use the step sequence, worked traces and concrete examples to build a mental picture." },
    reading: { label: "Reading mode", description: "Keep the full concept guide, worked examples and common mistakes open while learning." },
  }[learningPreference] || { label: "Balanced mode", description: "Read the concept, follow a worked example, then practise it." };

  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const [phase, setPhase] = useState<"learn" | "assessment">("learn");
  const [assessmentAnswers, setAssessmentAnswers] = useState<Record<string, number>>({});
  const [assessmentResult, setAssessmentResult] = useState<any>(null);
  const [assessmentError, setAssessmentError] = useState("");
  const [stepError, setStepError] = useState("");
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [answerResult, setAnswerResult] = useState<AnswerResult>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [completionData, setCompletionData] = useState<any>(null);
  const [saving, setSaving] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);
  const [attemptedCount, setAttemptedCount] = useState(0);
  const [textAnswer, setTextAnswer] = useState("");
  const [sequenceOrder, setSequenceOrder] = useState<number[]>([]);
  const [codeDraft, setCodeDraft] = useState("");
  const [codeLabResult, setCodeLabResult] = useState<{
    success: boolean; passed: boolean; stdout: string; stderr: string;
  } | null>(null);
  const [hintsRevealed, setHintsRevealed] = useState(0);
  const { execute: runBrowserCode } = useBrowserRuntime();
  const lessonStartedAt = useRef<number>(Date.now());
  const progressLoaded = useRef(false);
  const [resumedFromStep, setResumedFromStep] = useState(false);
  const [traceResult, setTraceResult] = useState<any>(null);
  const [isGeneratingTrace, setIsGeneratingTrace] = useState(false);

  const generateTrace = useCallback(async () => {
    if (!codeDraft.trim()) return;
    setIsGeneratingTrace(true);
    try {
      const result = await compilerApi.traceCode({ code: codeDraft, language: "python", stdin: "" });
      setTraceResult(result);
    } catch (e: any) {
      setTraceResult({ error: e?.detail || "Trace generation failed", steps: [] });
    } finally {
      setIsGeneratingTrace(false);
    }
  }, [codeDraft]);

  useEffect(() => {
    let cancelled = false;
    progressLoaded.current = false;
    setLoading(true);
    setLesson(null);
    lessonStartedAt.current = Date.now();
    setCurrentStep(0);
    setResumedFromStep(false);
    setPhase("learn");
    setAssessmentAnswers({});
    setAssessmentResult(null);
    setAssessmentError("");
    setStepError("");
    setSelectedAnswer(null);
    setAnswerResult(null);
    setShowExplanation(false);
    setCompleted(false);
    setCompletionData(null);
    setCorrectCount(0);
    setAttemptedCount(0);
    setSequenceOrder([]);
    setCodeDraft("");
    setCodeLabResult(null);
    setHintsRevealed(0);

    Promise.all([
      api.lessons.get(lessonSlug),
      api.lessons.progress().catch(() => null),
    ])
      .then(([lessonResponse, progressResponse]: [any, any]) => {
        if (cancelled || !lessonResponse?.data) return;
        const steps = lessonResponse.data.steps || [];
        const savedStep = Number(progressResponse?.data?.current_step ?? 0);
        const restoredStep = Number.isInteger(savedStep)
          ? Math.max(0, Math.min(savedStep, Math.max(steps.length - 1, 0)))
          : 0;
        setLesson(lessonResponse.data);
        setCurrentStep(restoredStep);
        setResumedFromStep(Boolean(progressResponse?.data?.has_progress && restoredStep > 0));
        progressLoaded.current = true;
      })
      .catch(() => {
        if (!cancelled) setLesson(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
      progressLoaded.current = false;
    };
  }, [lessonSlug, trackId, moduleId, topicId]);

  useEffect(() => {
    if (!lesson || !progressLoaded.current) return;
    const timeoutId = window.setTimeout(() => {
      api.lessons.completeStep({ lesson_id: lessonSlug, step_id: String(currentStep) }).catch(() => {
        // Resume data is a convenience. A temporary save failure must not block learning.
      });
    }, 250);
    return () => window.clearTimeout(timeoutId);
  }, [lesson, lessonSlug, currentStep]);

  useEffect(() => {
    setTextAnswer("");
    setCodeLabResult(null);
    setHintsRevealed(0);
    const activeStep = lesson?.steps?.[currentStep];
    setSequenceOrder(
      activeStep?.step_type === "order_steps"
        ? (activeStep.options || []).map((_, index) => index)
        : [],
    );
    setCodeDraft(activeStep?.step_type === "code_lab" ? activeStep.starter_code || "" : "");
  }, [currentStep, lessonSlug, lesson]);

  const handleAnswer = useCallback(
    async (index: number) => {
      if (!lesson || answerResult !== null || saving) return;
      const step = lesson.steps[currentStep];
      if (!["interactive", "practice", "debug_choice", "api_scenario"].includes(step.step_type)) return;

      setSelectedAnswer(index);
      setStepError("");
      setSaving(true);
      try {
        const response: any = await api.lessons.completeStep({ lesson_id: lessonSlug, step_id: String(currentStep), answer: String(index)});
        const result = response?.data;
        if (!result) throw new Error("The answer could not be graded.");
        setAttemptedCount((count) => count + 1);
        if (result.correct) setCorrectCount((count) => count + 1);
        setAnswerResult({
          correct: Boolean(result.correct),
          correctIndex: Number(result.correct_index),
          explanation: [result.feedback, result.explanation].filter(Boolean).join("\n\n"),
        });
        setShowExplanation(true);
        void queryClient.invalidateQueries({ queryKey: ["adaptive"] });
      } catch (error: any) {
        setSelectedAnswer(null);
        setStepError(error?.message || "Could not check this answer. Please retry.");
      } finally {
        setSaving(false);
      }
    },
    [lesson, lessonSlug, currentStep, answerResult, saving, queryClient]
  );

  const handleTextAnswer = useCallback(async () => {
    if (!lesson || !textAnswer.trim() || answerResult !== null || saving) return;
    const step = lesson.steps[currentStep];
    if (!["predict_output", "fill_blank", "sql_lab"].includes(step.step_type)) return;

    setStepError("");
    setSaving(true);
    try {
      const response: any = await api.lessons.completeStep({ lesson_id: lessonSlug, step_id: String(currentStep), answer: String(textAnswer)} );
      const result = response?.data;
      if (!result) throw new Error("The answer could not be graded.");
      setAttemptedCount((count) => count + 1);
      if (result.correct) setCorrectCount((count) => count + 1);
      const explanation = [result.feedback, result.explanation].filter(Boolean).join("\n\n");
      setAnswerResult({
        correct: Boolean(result.correct),
        correctIndex: null,
        correctAnswer: result.correct_answer || "",
        explanation,
        feedback: result.feedback || "",
        sqlResults: Array.isArray(result.student_results) ? result.student_results : undefined,
      });
      setShowExplanation(true);
      void queryClient.invalidateQueries({ queryKey: ["adaptive"] });
    } catch (error: any) {
      setStepError(error?.message || "Could not check this answer. Please retry.");
    } finally {
      setSaving(false);
    }
  }, [lesson, lessonSlug, currentStep, textAnswer, answerResult, saving, queryClient]);

  const handleSequenceAnswer = useCallback(async () => {
    if (!lesson || answerResult !== null || saving) return;
    const step = lesson.steps[currentStep];
    if (step.step_type !== "order_steps") return;

    setStepError("");
    setSaving(true);
    try {
      const response: any = await api.lessons.completeStep({ lesson_id: lessonSlug, step_id: String(currentStep), answer: String(sequenceOrder)} );
      const result = response?.data;
      if (!result) throw new Error("The sequence could not be graded.");
      setAttemptedCount((count) => count + 1);
      if (result.correct) setCorrectCount((count) => count + 1);
      setAnswerResult({
        correct: Boolean(result.correct),
        correctIndex: null,
        correctOrder: Array.isArray(result.correct_order) ? result.correct_order : undefined,
        explanation: result.explanation || "",
      });
      setShowExplanation(true);
      void queryClient.invalidateQueries({ queryKey: ["adaptive"] });
    } catch (error: any) {
      setStepError(error?.message || "Could not check this sequence. Please retry.");
    } finally {
      setSaving(false);
    }
  }, [lesson, lessonSlug, currentStep, sequenceOrder, answerResult, saving, queryClient]);

  const handleRunCodeLab = useCallback(async () => {
    if (!lesson || saving) return;
    const step = lesson.steps[currentStep];
    if (step.step_type !== "code_lab") return;
    if ((step.language || "javascript").toLowerCase() !== "javascript") {
      setStepError("This browser lab currently supports JavaScript. Use the full compiler for other languages.");
      return;
    }

    setStepError("");
    setSaving(true);
    setCodeLabResult(null);
    setAnswerResult(null);
    setShowExplanation(false);
    try {
      const run = await runBrowserCode("javascript", codeDraft, "", 3000);
      if (!run.success) {
        setCodeLabResult({ success: false, passed: false, stdout: run.stdout || "", stderr: run.stderr || "" });
        setStepError(run.stderr || "The code could not be run. Check the error and try again.");
        return;
      }

      // The expected output stays on the server. This check is formative only;
      // it does not award XP or certify placement mastery.
      const response: any = await api.lessons.completeStep({ lesson_id: lessonSlug, step_id: String(currentStep), answer: String(run.stdout || "")} );
      const grade = response?.data;
      if (!grade) throw new Error("The output could not be checked.");
      const passed = Boolean(grade.correct);
      setAttemptedCount((count) => count + 1);
      if (passed) setCorrectCount((count) => count + 1);
      setCodeLabResult({ success: true, passed, stdout: run.stdout || "", stderr: "" });
      setAnswerResult({
        correct: passed,
        correctIndex: null,
        explanation: [grade.feedback, grade.explanation].filter(Boolean).join("\n\n"),
        feedback: grade.feedback || "",
      });
      setShowExplanation(true);
      void queryClient.invalidateQueries({ queryKey: ["adaptive"] });
    } catch (error: any) {
      setCodeLabResult({ success: false, passed: false, stdout: "", stderr: error?.message || "The browser runner could not start." });
      setStepError(error?.message || "The browser runner could not start. Please retry.");
    } finally {
      setSaving(false);
    }
  }, [lesson, lessonSlug, currentStep, saving, runBrowserCode, codeDraft, queryClient]);

  const retryCurrentStep = useCallback(() => {
    if (!lesson) return;
    setAnswerResult(null);
    setShowExplanation(false);
    setSelectedAnswer(null);
    setTextAnswer("");
    setCodeLabResult(null);
    setStepError("");
    const step = lesson.steps[currentStep];
    if (step.step_type === "order_steps") {
      setSequenceOrder((step.options || []).map((_, index) => index));
    }
  }, [lesson, currentStep]);

  const goNext = useCallback(() => {
    if (!lesson) return;
    const step = lesson.steps[currentStep];
    const mustAttempt = ["interactive", "practice", "predict_output", "fill_blank", "order_steps", "code_lab", "sql_lab", "debug_choice", "api_scenario"].includes(step.step_type);
    const stepCompleted = step.step_type === "code_lab"
      ? Boolean(codeLabResult?.passed)
      : step.step_type === "sql_lab"
        ? Boolean(answerResult?.correct)
        : Boolean(answerResult);
    if (mustAttempt && !stepCompleted) {
      setStepError(
        step.step_type === "code_lab"
          ? "Run the code and pass the output check before continuing."
          : step.step_type === "sql_lab"
            ? "Revise your query until it returns the required result before continuing."
            : "Try this practice step before continuing. You will see feedback after your answer.",
      );
      return;
    }
    if (currentStep < lesson.steps.length - 1) {
      setCurrentStep((s) => s + 1);
      setSelectedAnswer(null);
      setAnswerResult(null);
      setShowExplanation(false);
    } else {
      setPhase("assessment");
      setAssessmentError("");
    }
  }, [lesson, currentStep, answerResult, codeLabResult]);

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
      const res: any = await api.lessons.completeStep({
        lesson_id: lessonSlug,
        step_id: "final",
        ...(trackId && moduleId ? { track_id: trackId, module_id: moduleId, topic_id: topicId } : {}),
      });
      const result = res?.data || null;
      setAssessmentResult(result);
      if (result?.passed) {
        setCompletionData(result);
        setCompleted(true);
        await Promise.all([
          queryClient.invalidateQueries({ queryKey: ["company-tracks"] }),
          queryClient.invalidateQueries({ queryKey: ["journey", "state"] }),
          queryClient.invalidateQueries({ queryKey: ["study", "today"] }),
          queryClient.invalidateQueries({ queryKey: ["adaptive"] }),
        ]);
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
  }, [lesson, lessonSlug, assessmentAnswers, trackId, moduleId, topicId, saving, queryClient]);

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
        <Link to="/academy" className="text-brand-sky hover:underline">
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
              ? trackId && completionData?.module_completed
                ? "All required topic skills are verified. Your company module is complete."
                : trackId && completionData?.module_result
                  ? `Topic mastery verified: ${completionData.module_result.mastered_topics?.length ?? 1} of ${completionData.module_result.required_topics?.length ?? "the"} required skills. Continue with the next topic to finish this module.`
                  : "You passed the final assessment. Keep the skill fresh with spaced practice."
              : "Keep practicing. Review the explanation and try again."}
          </p>
          {completionData && (
            <p className="text-sm text-brand-sky mb-4">
              XP earned: {completionData.xp_earned ?? 0}
            </p>
          )}
          <div className="flex justify-center gap-3">
            <Link
              to="/academy"
              className="rounded-xl border border-white/10 px-4 py-2 text-sm hover:bg-white/5"
            >
              {trackId ? "Back to company track" : "Back to Learn"}
            </Link>
            {completionData?.passed && lesson.next_lesson_slug && !trackId ? (
              <Link
                to={`/learn/lesson/${lesson.next_lesson_slug}`}
                className="inline-flex items-center gap-2 rounded-xl bg-brand-sky px-4 py-2 text-sm font-semibold text-white hover:bg-brand-sky/90"
              >
                {lesson.next_lesson_title || "Next lesson"} <ChevronRight size={15} />
              </Link>
            ) : (
              <button
                onClick={() => {
                  setCurrentStep(0);
                  setResumedFromStep(false);
                  setPhase("learn");
                  setAssessmentAnswers({});
                  setAssessmentResult(null);
                  setAssessmentError("");
                  setStepError("");
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
            )}
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
          <Link to="/academy" className="inline-flex items-center gap-1 text-xs text-text-secondary hover:text-text-primary">
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
  const preferredLanguage = String(learnerProfile?.preferred_language || "cpp").toLowerCase();
  const preferredLanguageLabel = ({
    c: "C",
    cpp: "C++",
    java: "Java",
    python: "Python",
    javascript: "JavaScript",
  } as Record<string, string>)[preferredLanguage] || preferredLanguage.toUpperCase();
  const authoredLanguages = Array.from(new Set(
    (lesson.steps || [])
      .map((item) => String(item.language || "").trim())
      .filter(Boolean),
  ));
  const languageGuidance = authoredLanguages.length
    ? `This lesson's runnable examples use ${authoredLanguages.join(", ")}. Use the compiler for independent practice in ${preferredLanguageLabel}.`
    : `Use the compiler for independent solutions in ${preferredLanguageLabel}.`;

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <div className="mb-6">
        {resumedFromStep && (
          <p className="mb-3 rounded-lg border border-brand-sky/20 bg-brand-sky/5 px-3 py-2 text-xs text-brand-sky">
            Welcome back — your last position has been restored.
          </p>
        )}
        <div className="flex items-center justify-between mb-2">
          <div>
            <Link
              to="/academy"
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
        <div
          className="h-2 rounded-full bg-white/5 overflow-hidden"
          role="progressbar"
          aria-label="Lesson progress"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(progress)}
        >
          <motion.div
            className="h-full bg-brand-sky"
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      <section className="mb-4 rounded-2xl border border-brand-sky/20 bg-brand-sky/5 p-4">
        <p className="text-[10px] font-mono uppercase tracking-wider text-brand-sky">Your learning mode · {learningMode.label}</p>
        <p className="mt-1 text-sm leading-6 text-text-primary">{learningMode.description}</p>
        <p className="mt-2 text-xs leading-5 text-text-secondary">Preferred coding language: {preferredLanguageLabel}. {languageGuidance}</p>
      </section>

      {lesson.quest && (
        <section className="mb-4 overflow-hidden rounded-2xl border border-violet-400/20 bg-gradient-to-br from-violet-500/10 via-surface-base/80 to-surface-base/80 p-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-[10px] font-mono font-bold uppercase tracking-wider text-violet-300">Story mission · {lesson.quest.chapter || "Academy quest"}</p>
            {lesson.quest.rank && <span className="rounded-full border border-violet-300/20 bg-violet-300/10 px-2.5 py-1 text-[10px] font-semibold text-violet-200">{lesson.quest.rank}</span>}
          </div>
          {lesson.quest.story && <p className="mt-3 text-sm leading-6 text-text-primary">{lesson.quest.story}</p>}
          {lesson.quest.mission && (
            <div className="mt-3 rounded-xl border border-white/10 bg-black/10 p-3">
              <p className="text-[10px] font-bold uppercase tracking-wider text-violet-200">Your mission</p>
              <p className="mt-1 text-sm leading-6 text-text-primary">{lesson.quest.mission}</p>
            </div>
          )}
          {lesson.quest.success_criteria?.length ? (
            <div className="mt-3">
              <p className="text-[10px] font-bold uppercase tracking-wider text-text-secondary">Quest objectives</p>
              <ul className="mt-2 grid gap-1.5 sm:grid-cols-2">
                {lesson.quest.success_criteria.map((criterion, index) => (
                  <li key={index} className="flex gap-2 text-xs leading-5 text-text-secondary">
                    <span className="font-mono text-violet-300">{String(index + 1).padStart(2, "0")}</span>
                    {criterion}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </section>
      )}

      {lesson.learning_objectives?.length ? (
        <section className="mb-4 rounded-2xl border border-brand-sky/20 bg-brand-sky/5 p-4">
          <p className="text-[10px] font-mono uppercase tracking-wider text-brand-sky">By the end of this lesson</p>
          <ul className="mt-2 space-y-1.5">
            {lesson.learning_objectives.map((objective, index) => (
              <li key={index} className="flex gap-2 text-sm text-text-primary"><CheckCircle2 size={15} className="mt-0.5 shrink-0 text-brand-sky"/>{objective}</li>
            ))}
          </ul>
          {lesson.prerequisites?.length ? <p className="mt-3 text-xs text-text-secondary">Recommended first: {lesson.prerequisites.join(", ").split("_").join(" ")}</p> : null}
        </section>
      ) : null}

      <LearningResourcesPanel domain={lesson.domain} topic={[lessonSlug, lesson.title, ...(lesson.concepts || [])].join(" ")} />

      {(lesson.worked_examples?.length || lesson.common_misconceptions?.length || lesson.company_applications?.length || lesson.srs_cards?.length) ? (
        <details open={learningPreference !== "hands_on"} className="mb-4 rounded-2xl border border-white/10 bg-surface-base/70 p-4">
          <summary className="cursor-pointer text-sm font-semibold text-text-primary">Deep dive: worked examples, common mistakes and placement practice</summary>
          <div className="mt-4 space-y-5">
            {lesson.concepts?.length ? (
              <div><h3 className="text-xs font-bold uppercase tracking-wider text-brand-sky">Key concepts</h3><div className="mt-2 flex flex-wrap gap-2">{lesson.concepts.map((concept) => <span key={concept} className="rounded-full bg-white/5 px-2.5 py-1 text-xs text-text-secondary">{concept}</span>)}</div></div>
            ) : null}
            {lesson.worked_examples?.length ? (
              <div><h3 className="text-xs font-bold uppercase tracking-wider text-brand-sky">Worked examples</h3><div className="mt-2 space-y-3">{lesson.worked_examples.map((example, index) => (
                <article key={index} className="rounded-xl border border-white/10 p-3">
                  <h4 className="text-sm font-semibold text-text-primary">{example.title}</h4>
                  <pre className="mt-2 overflow-x-auto rounded-lg bg-black/20 p-2 text-xs text-text-secondary">{example.input}</pre>
                  <ol className="mt-2 list-decimal space-y-1 pl-5 text-xs text-text-secondary">{example.trace.map((line, lineIndex) => <li key={lineIndex}>{line}</li>)}</ol>
                  <p className="mt-2 text-sm font-semibold text-text-primary">Result: {example.output}</p>
                  <p className="mt-1 text-xs leading-5 text-text-secondary">{example.explanation}</p>
                </article>
              ))}</div></div>
            ) : null}
            {lesson.common_misconceptions?.length ? (
              <div><h3 className="text-xs font-bold uppercase tracking-wider text-brand-sky">Common mistakes to avoid</h3><div className="mt-2 space-y-2">{lesson.common_misconceptions.map((item, index) => (
                <div key={index} className="rounded-xl bg-amber-500/5 p-3"><p className="text-xs font-semibold text-amber-200">Misconception: {item.misconception}</p><p className="mt-1 text-xs leading-5 text-text-secondary">Correct idea: {item.correction}</p></div>
              ))}</div></div>
            ) : null}
            {lesson.company_applications?.length ? (
              <div><h3 className="text-xs font-bold uppercase tracking-wider text-brand-sky">How this appears in placement preparation</h3><div className="mt-2 grid gap-2 sm:grid-cols-2">{lesson.company_applications.map((item, index) => (
                <div key={index} className="rounded-xl border border-white/10 p-3"><p className="text-sm font-semibold text-text-primary">{item.company}</p><p className="mt-1 text-xs text-text-secondary">{item.skill}</p><p className="mt-1 text-xs text-text-secondary">Practice: {item.practice}</p></div>
              ))}</div></div>
            ) : null}
            {lesson.srs_cards?.length ? (
              <div><h3 className="text-xs font-bold uppercase tracking-wider text-brand-sky">Quick revision cards</h3><div className="mt-2 space-y-2">{lesson.srs_cards.map((card, index) => (
                <details key={index} className="rounded-xl border border-white/10 p-3"><summary className="cursor-pointer text-xs font-semibold text-text-primary">{card.question}</summary><p className="mt-2 text-xs leading-5 text-text-secondary">{card.answer}</p></details>
              ))}</div></div>
            ) : null}
          </div>
        </details>
      ) : null}

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
            {["interactive", "practice", "predict_output", "fill_blank", "order_steps", "code_lab", "sql_lab", "debug_choice", "api_scenario"].includes(step.step_type) ? (
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

          {step.request_preview && (
            <div className="mb-4 rounded-xl border border-white/10 bg-[#101820] p-4">
              <p className="mb-2 text-[10px] font-mono uppercase tracking-wider text-sky-300">Request / response context</p>
              <pre className="overflow-x-auto whitespace-pre-wrap text-xs leading-5 text-slate-100">{step.request_preview}</pre>
            </div>
          )}

          {step.log_output && (
            <div className="mb-4 rounded-xl border border-amber-500/20 bg-amber-500/5 p-4">
              <p className="mb-2 text-[10px] font-mono uppercase tracking-wider text-amber-200">Observed log</p>
              <pre className="overflow-x-auto whitespace-pre-wrap text-xs leading-5 text-amber-100">{step.log_output}</pre>
            </div>
          )}

          {step.code && (
            <pre className="mb-4 overflow-x-auto rounded-xl border border-white/10 bg-[#101820] p-4 text-sm leading-6 text-slate-100">
              <code>{step.code}</code>
            </pre>
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

          {step.hints && step.hints.length > 0 && (
            <div className="mb-4 rounded-xl border border-yellow-500/20 bg-yellow-500/5 p-3">
              <button
                type="button"
                onClick={() => setHintsRevealed((count) => Math.min(count + 1, step.hints!.length))}
                disabled={hintsRevealed >= step.hints.length}
                className="text-xs font-semibold text-yellow-200 disabled:opacity-50"
              >
                {hintsRevealed >= step.hints.length ? "All hints revealed" : `Reveal hint ${hintsRevealed + 1} of ${step.hints.length}`}
              </button>
              {hintsRevealed > 0 && (
                <p className="mt-2 text-xs leading-relaxed text-text-secondary">{step.hints[hintsRevealed - 1]}</p>
              )}
            </div>
          )}
          {stepError && (
            <p role="alert" className="mb-4 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-200">
              {stepError}
            </p>
          )}

          {step.step_type === "order_steps" && (
            <div className="mb-4 rounded-xl border border-white/10 bg-white/[0.03] p-4">
              {step.prompt && <p className="mb-3 text-sm font-semibold text-text-primary">{step.prompt}</p>}
              <ol className="space-y-2" aria-label="Reorder the steps">
                {sequenceOrder.map((optionIndex, position) => (
                  <li key={optionIndex} className="flex items-center gap-2 rounded-lg border border-white/10 bg-surface-base px-3 py-2">
                    <span className="w-6 shrink-0 text-center font-mono text-xs text-brand-sky">{position + 1}</span>
                    <span className="min-w-0 flex-1 text-sm text-text-primary">{step.options?.[optionIndex]}</span>
                    <button
                      type="button"
                      aria-label={`Move ${step.options?.[optionIndex]} up`}
                      disabled={position === 0 || showExplanation || saving}
                      onClick={() => setSequenceOrder((order) => {
                        const next = [...order];
                        [next[position - 1], next[position]] = [next[position], next[position - 1]];
                        return next;
                      })}
                      className="rounded-md p-1 hover:bg-white/10 disabled:opacity-30"
                    >
                      <ChevronUp size={16} />
                    </button>
                    <button
                      type="button"
                      aria-label={`Move ${step.options?.[optionIndex]} down`}
                      disabled={position === sequenceOrder.length - 1 || showExplanation || saving}
                      onClick={() => setSequenceOrder((order) => {
                        const next = [...order];
                        [next[position], next[position + 1]] = [next[position + 1], next[position]];
                        return next;
                      })}
                      className="rounded-md p-1 hover:bg-white/10 disabled:opacity-30"
                    >
                      <ChevronDown size={16} />
                    </button>
                  </li>
                ))}
              </ol>
              <button
                type="button"
                onClick={() => void handleSequenceAnswer()}
                disabled={saving || showExplanation || sequenceOrder.length < 2}
                className="mt-3 min-h-10 rounded-lg bg-brand-sky px-4 text-sm font-semibold text-white disabled:opacity-40"
              >
                {saving ? "Checking…" : "Check sequence"}
              </button>
              {showExplanation && answerResult?.correctOrder && (
                <p className="mt-3 text-xs leading-relaxed text-text-secondary">
                  Correct sequence: {answerResult.correctOrder.map((index) => step.options?.[index]).join(" → ")}
                </p>
              )}
            </div>
          )}

          {step.step_type === "code_lab" && (
            <div className="mb-4 rounded-xl border border-white/10 bg-white/[0.03] p-4">
              {step.prompt && <p className="mb-3 text-sm font-semibold text-text-primary">{step.prompt}</p>}
              <div className="mb-2 flex items-center justify-between text-[11px] text-text-secondary">
                <span>JavaScript · runs in a disposable browser worker</span>
                <button
                  type="button"
                  onClick={() => { setCodeDraft(step.starter_code || ""); setCodeLabResult(null); setAnswerResult(null); setShowExplanation(false); setStepError(""); }}
                  className="inline-flex items-center gap-1 rounded-md px-2 py-1 hover:bg-white/10"
                >
                  <RotateCcw size={12} /> Reset starter
                </button>
              </div>
              <textarea
                aria-label="Edit the exercise code"
                spellCheck={false}
                autoCapitalize="off"
                autoCorrect="off"
                value={codeDraft}
                onChange={(event) => { setCodeDraft(event.target.value); setCodeLabResult(null); setAnswerResult(null); setShowExplanation(false); setStepError(""); }}
                disabled={saving}
                rows={9}
                className="w-full resize-y rounded-lg border border-white/10 bg-[#101820] p-3 font-mono text-xs leading-6 text-slate-100 outline-none focus:border-brand-sky"
              />
              <div className="mt-3 flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => void handleRunCodeLab()}
                  disabled={saving || !codeDraft.trim()}
                  className="inline-flex min-h-10 items-center gap-2 rounded-lg bg-brand-sky px-4 text-sm font-semibold text-white disabled:opacity-40"
                >
                  <Play size={14} /> {saving ? "Running…" : "Run code"}
                </button>
                <span className="text-[11px] text-text-secondary">No server compiler call for this exercise.</span>
              </div>
              {codeLabResult && (
                <div className={`mt-3 rounded-lg border p-3 ${codeLabResult.passed ? "border-green-500/30 bg-green-500/10" : "border-amber-500/30 bg-amber-500/10"}`}>
                  <p className="mb-2 text-xs font-semibold">
                    {codeLabResult.passed ? "Output check passed" : "Output check not passed"}
                  </p>
                  <p className="text-[11px] text-text-secondary">Your output</p>
                  <pre className="mt-1 overflow-x-auto whitespace-pre-wrap font-mono text-xs text-text-primary">{codeLabResult.stdout || (codeLabResult.stderr ? "" : "(no output)")}</pre>
                  {codeLabResult.stderr && <pre className="mt-2 overflow-x-auto whitespace-pre-wrap text-xs text-red-300">{codeLabResult.stderr}</pre>}
                  <p className="mt-2 text-[11px] text-text-secondary">The expected output stays hidden; use the feedback and hints to revise your code.</p>
                </div>
              )}
              {codeDraft.trim() && (
                <div className="mt-4">
                  <button
                    type="button"
                    onClick={generateTrace}
                    disabled={isGeneratingTrace}
                    className="w-full flex items-center justify-center gap-2 rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-xs font-semibold text-brand-sky hover:bg-white/10 transition-colors"
                  >
                    {isGeneratingTrace ? (
                      <Loader2 size={12} className="animate-spin" />
                    ) : (
                      <Layers size={12} />
                    )}
                    Visual Execution Trace
                  </button>
                  {traceResult && (
                    <div className="mt-3 rounded-xl border border-white/10 bg-[#0d1117] overflow-hidden">
                      <div className="bg-[#161b22] border-b border-white/5 px-4 py-2 flex items-center justify-between">
                        <span className="text-xs font-mono text-text-muted">Step-by-step execution</span>
                        <span className="text-[10px] font-mono text-text-muted">{traceResult.steps.length} steps</span>
                      </div>
                      <CodeTracer
                        code={codeDraft}
                        language="python"
                        className="mt-0"
                      />
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {step.step_type === "sql_lab" && (
            <div className="mb-4 rounded-xl border border-white/10 bg-white/[0.03] p-4">
              {step.prompt && <p className="mb-3 text-sm font-semibold text-text-primary">{step.prompt}</p>}
              {step.schema_preview && (
                <div className="mb-3">
                  <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-text-secondary">Schema</p>
                  <pre className="overflow-x-auto rounded-lg bg-[#101820] p-3 font-mono text-xs leading-5 text-slate-100">{step.schema_preview}</pre>
                </div>
              )}
              {step.sample_data && (
                <div className="mb-3">
                  <p className="mb-1 text-[11px] font-semibold uppercase tracking-wide text-text-secondary">Sample rows</p>
                  <pre className="overflow-x-auto rounded-lg bg-[#101820] p-3 font-mono text-xs leading-5 text-slate-100">{step.sample_data}</pre>
                </div>
              )}
              <label className="mb-1 block text-[11px] font-semibold uppercase tracking-wide text-text-secondary" htmlFor="lesson-sql-query">Your SQL query</label>
              <textarea
                id="lesson-sql-query"
                aria-label="Write your SQL query"
                spellCheck={false}
                autoCapitalize="off"
                autoCorrect="off"
                value={textAnswer}
                onChange={(event) => setTextAnswer(event.target.value)}
                disabled={showExplanation || saving}
                rows={7}
                maxLength={8000}
                placeholder={step.answer_placeholder || "SELECT ..."}
                className="w-full resize-y rounded-lg border border-white/10 bg-[#101820] p-3 font-mono text-xs leading-6 text-slate-100 outline-none focus:border-brand-sky disabled:opacity-60"
              />
              <div className="mt-3 flex items-center justify-between gap-2">
                <span className="text-[11px] text-text-secondary">Fresh in-memory SQLite dataset · no paid compiler call</span>
                <button
                  type="button"
                  onClick={() => void handleTextAnswer()}
                  disabled={!textAnswer.trim() || saving || showExplanation}
                  className="min-h-10 rounded-lg bg-brand-sky px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {saving ? "Checking…" : "Check query"}
                </button>
              </div>
              {answerResult?.sqlResults && answerResult.sqlResults.length > 0 && (
                <pre className="mt-3 overflow-x-auto rounded-lg bg-[#101820] p-3 font-mono text-xs leading-5 text-slate-100">{JSON.stringify(answerResult.sqlResults, null, 2)}</pre>
              )}
            </div>
          )}

          {(step.step_type === "predict_output" || step.step_type === "fill_blank") && (
            <div className="mb-4 rounded-xl border border-white/10 bg-white/[0.03] p-4">
              {step.prompt && <p className="mb-3 text-sm font-semibold text-text-primary">{step.prompt}</p>}
              <div className="flex flex-col gap-2 sm:flex-row">
                <input
                  type="text"
                  aria-label="Your answer"
                  value={textAnswer}
                  onChange={(event) => setTextAnswer(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter" && !saving && !showExplanation && textAnswer.trim()) {
                      void handleTextAnswer();
                    }
                  }}
                  placeholder={step.answer_placeholder || "Type your answer"}
                  disabled={showExplanation || saving}
                  maxLength={1000}
                  className="min-h-11 min-w-0 flex-1 rounded-lg border border-white/10 bg-surface-base px-3 text-sm text-text-primary outline-none focus:border-brand-sky disabled:opacity-60"
                />
                <button
                  type="button"
                  onClick={() => void handleTextAnswer()}
                  disabled={!textAnswer.trim() || saving || showExplanation}
                  className="min-h-11 rounded-lg bg-brand-sky px-4 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-40"
                >
                  {saving ? "Checking…" : "Check answer"}
                </button>
              </div>
              {showExplanation && answerResult?.correctAnswer && !answerResult.correct && (
                <p className="mt-3 text-xs text-text-secondary">
                  Expected answer: <code className="rounded bg-white/10 px-1.5 py-0.5 text-brand-sky">{answerResult.correctAnswer}</code>
                </p>
              )}
            </div>
          )}

          {(["interactive", "practice", "debug_choice", "api_scenario"].includes(step.step_type)) &&
            step.options && (
              <div className="space-y-2 mb-4">
                {step.options.map((opt, idx) => {
                  const isSelected = selectedAnswer === idx;
                  const isCorrect = answerResult?.correctIndex === idx;
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
                className={`mb-1 text-xs font-bold uppercase tracking-wide ${
                  answerResult.correct ? "text-green-300" : "text-red-300"
                }`}
              >
                {answerResult.correct ? "Correct — nice work" : "Not quite — learn from the feedback"}
              </p>
              <p className="text-sm leading-6 text-text-primary">
                {answerResult.explanation || "Review the worked example and try the concept again."}
              </p>
              {!answerResult.correct && step.step_type !== "code_lab" && (
                <button
                  type="button"
                  onClick={retryCurrentStep}
                  className="mt-3 rounded-lg border border-white/15 px-3 py-2 text-xs font-semibold text-text-primary hover:bg-white/5"
                >
                  Try again
                </button>
              )}
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
              disabled={saving || (
                ["interactive", "practice", "predict_output", "fill_blank", "order_steps", "debug_choice", "api_scenario"].includes(step.step_type)
                && !answerResult
              ) || (step.step_type === "code_lab" && !codeLabResult?.passed) || (step.step_type === "sql_lab" && !answerResult?.correct)}
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
