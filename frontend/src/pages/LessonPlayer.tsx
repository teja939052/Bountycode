// @ts-nocheck
import { useState, useEffect, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
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
  Compass,
} from "lucide-react";
import { Mentor, MentorMood } from "../design-system/Mentor";
import { lessonApi } from "../services/api/lesson";
import { missionApi } from "../services/api/missions";
import { BountyCodeLoader } from "../components/brand/BountyCodeBrandMotion";

type Phase =
  | "hook"
  | "see"
  | "understand"
  | "touch"
  | "predict"
  | "change"
  | "build"
  | "break"
  | "fix"
  | "retrieve"
  | "transfer"
  | "prove"
  | "reward";

type VisualPrimitive = {
  type: "highlight" | "move" | "transform" | "split" | "merge" | "compare" | "trace" | "reveal";
  instruction: string;
  data: Record<string, any>;
};

type DiscoveryStep = {
  action: string;
  narration: string;
  interaction: {
    type: "inspect_code" | "choose_outcome" | "visual_primitive";
    primitive?: VisualPrimitive;
    code?: string;
    expected_output?: string;
    prompt?: string;
    options?: Array<{ id: string; text: string; correct: boolean; explanation?: string }>;
    hint?: string;
  };
};

type BuildStep = {
  step_order: number;
  title: string;
  description: string;
  starter_code: string;
  function_name: string;
  signature: string;
  test_cases: Array<{ input: any[]; expected: any }>;
  hidden_test_cases: Array<{ input: any[]; expected: any }>;
  diamonds: number;
  captain_byte_moment?: string;
  scaffolded_hints: Array<{ level: number; text: string }>;
};

type AssessmentQuestion = {
  type: "code_tracing" | "concept" | "debug";
  code?: string;
  question: string;
  answer_format: string;
  expected_answer?: string;
  keywords?: string[];
  explanation: string;
  fix?: string;
  error?: string;
  options?: Array<{ id: string; text: string }>;
};

type LessonContent = {
  lesson_id: string;
  module_id: string;
  title: string;
  description: string;
  difficulty: string;
  est_minutes: number;
  xp_reward: number;
  skills_taught: string[];
  captain_byte: {
    intro: string;
    correct: string[];
    wrong: string[];
    after_break: string;
    after_mastery: string;
    retry_prompt: string;
  };
  story_context: {
    title: string;
    narration: string;
    setting: string;
    character: string;
    intro_text: string;
  };
  discovery: {
    title: string;
    visual_primitives: string[];
    steps: DiscoveryStep[];
    conclusion: string;
  };
  prediction: {
    title: string;
    captain_byte_intro: string;
    question: string;
    code?: string;
    options: Array<{ id: string; text: string; correct: boolean; explanation: string }>;
    explanation: string;
  };
  explain: {
    title: string;
    captain_byte_intro: string;
    prompt: string;
    answer_format: string;
    keywords: string[];
    min_words: number;
    model_answer: string;
    intention: string;
  };
  guided_build: {
    title: string;
    captain_byte_intro: string;
    steps: BuildStep[];
  };
  transfer_challenge: {
    title: string;
    captain_byte_intro: string;
    description: string;
    function_name: string;
    signature: string;
    description_full: string;
    test_cases: Array<{ input: any[]; expected: any }>;
    hidden_test_cases: Array<{ input: any[]; expected: any }>;
    time_limit_minutes: number;
    diamonds: number;
    scaffolded_hints: Array<{ level: number; text: string }>;
  };
  assessment: {
    title: string;
    captain_byte_intro: string;
    description: string;
    questions: AssessmentQuestion[];
    mastery_threshold: number;
    diamonds: number;
  };
  break: {
    title: string;
    captain_byte_intro: string;
    story: string;
    buggy_code: string;
    expected_output: string;
    actual_output: string;
    diagnosis: {
      question: string;
      options: Array<{ id: string; text: string; correct: boolean; why: string }>;
    };
    fix: string;
    fixed_code: string;
    explanation: string;
  };
  srs_enrollment: {
    concept_id: string;
    concept_name: string;
    review_intervals: number[];
    key_points: string[];
    spaced_fields: string[];
  };
  world_progression: {
    world_id: string;
    competency_id: string;
    unlocks_next: string[];
    tower_badge: string;
    world_node: {
      level: number;
      title: string;
      color: string;
      icon: string;
      description: string;
    };
  };
};

type AnswerResult = {
  correct: boolean;
  explanation: string;
} | null;

export default function LessonPlayer() {
  const { slug } = useParams();
  const lessonSlug = slug || "percentages";

  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [phase, setPhase] = useState<Phase>("hook");
  const [subPhase, setSubPhase] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null);
  const [answerResult, setAnswerResult] = useState<AnswerResult>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [completed, setCompleted] = useState(false);
  const [saving, setSaving] = useState(false);
  const [mistakeCount, setMistakeCount] = useState(0);
  const [captainByteMessage, setCaptainByteMessage] = useState<string>("");
  const [captainByteMood, setCaptainByteMood] = useState<MentorMood>("welcome");
  const [buildCode, setBuildCode] = useState("");
  const [buildRunning, setBuildRunning] = useState(false);
  const [buildResult, setBuildResult] = useState<any>(null);
  const [assessmentAnswers, setAssessmentAnswers] = useState<Record<string, string>>({});
  const [assessmentResult, setAssessmentResult] = useState<any>(null);
  const [breakDiagnosis, setBreakDiagnosis] = useState<string>("");
  const [breakFix, setBreakFix] = useState("");
  const [breakResult, setBreakResult] = useState<any>(null);

  useEffect(() => {
    // Redirect legacy /lab/lesson/:lessonId to the canonical lesson runtime.
    if (lessonSlug) {
      navigate(`/learn/coding?lesson=${encodeURIComponent(lessonSlug)}`, { replace: true });
    } else {
      navigate(`/learn/coding`, { replace: true });
    }
  }, [navigate, lessonSlug]);

  const showCaptainByte = useCallback(
    (message: string, mood: MentorMood = "explaining") => {
      setCaptainByteMessage(message);
      setCaptainByteMood(mood);
    },
    []
  );

  const handleDiscoveryAnswer = useCallback(
    (optionId: string, correct: boolean, explanation: string) => {
      setSelectedAnswer(optionId);
      setShowExplanation(true);
      if (correct) {
        setMistakeCount(0);
        const msgs = lesson?.captain_byte.correct || [];
        showCaptainByte(
          msgs[Math.min(mistakeCount, msgs.length - 1)] || msgs[0] || "Nice.",
          "proud"
        );
      } else {
        setMistakeCount((c) => c + 1);
        const msgs = lesson?.captain_byte.wrong || [];
        showCaptainByte(
          msgs[Math.min(mistakeCount, msgs.length - 1)] || msgs[0] || "Try again.",
          "correcting"
        );
      }
      setAnswerResult({ correct, explanation });
    },
    [lesson, mistakeCount, showCaptainByte]
  );

  const handlePredictAnswer = useCallback(
    (optionId: string, correct: boolean, explanation: string) => {
      setSelectedAnswer(optionId);
      setShowExplanation(true);
      if (correct) {
        setMistakeCount(0);
        showCaptainByte(lesson?.captain_byte.correct[0] || "Nice prediction.", "proud");
      } else {
        setMistakeCount((c) => c + 1);
        showCaptainByte(lesson?.captain_byte.wrong[0] || "Look at what changed.", "correcting");
      }
      setAnswerResult({ correct, explanation });
    },
    [lesson, showCaptainByte]
  );

  const goNext = useCallback(() => {
    if (!lesson) return;
    setSelectedAnswer(null);
    setAnswerResult(null);
    setShowExplanation(false);

    const phases: Phase[] = [
      "hook",
      "see",
      "understand",
      "touch",
      "predict",
      "change",
      "build",
      "break",
      "fix",
      "retrieve",
      "transfer",
      "prove",
      "reward",
    ];
    const currentIdx = phases.indexOf(phase);
    if (currentIdx < phases.length - 1) {
      const nextPhase = phases[currentIdx + 1];
      setPhase(nextPhase);
      setSubPhase(0);

      if (nextPhase === "build") {
        const firstStep = lesson.guided_build.steps[0];
        setBuildCode(firstStep?.starter_code || "");
        showCaptainByte(
          lesson.guided_build.captain_byte_intro || lesson.captain_byte.intro,
          "briefing"
        );
      } else if (nextPhase === "break") {
        showCaptainByte(lesson.break.captain_byte_intro, "serious");
      } else if (nextPhase === "prove") {
        showCaptainByte(lesson.assessment.captain_byte_intro, "serious");
      } else if (nextPhase === "reward") {
        showCaptainByte(lesson.captain_byte.after_mastery, "celebrating");
      }
    } else {
      handleComplete();
    }
  }, [lesson, phase, showCaptainByte]);

  const goBack = useCallback(() => {
    setSelectedAnswer(null);
    setAnswerResult(null);
    setShowExplanation(false);
    const phases: Phase[] = [
      "hook",
      "see",
      "understand",
      "touch",
      "predict",
      "change",
      "build",
      "break",
      "fix",
      "retrieve",
      "transfer",
      "prove",
      "reward",
    ];
    const currentIdx = phases.indexOf(phase);
    if (currentIdx > 0) {
      setPhase(phases[currentIdx - 1]);
      setSubPhase((s) => Math.max(0, s - 1));
    }
  }, [phase]);

  const handleComplete = useCallback(async () => {
    if (!lesson || saving) return;
    setSaving(true);
    try {
      setCompleted(true);
    } catch {
      setCompleted(true);
    } finally {
      setSaving(false);
    }
  }, [lesson, saving]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <BountyCodeLoader size={40} />
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
          <p className="text-sm text-text-secondary mb-4">Review the concepts anytime.</p>
          <div className="flex justify-center gap-3">
            <Link
              to="/learn"
              className="rounded-xl border border-white/10 px-4 py-2 text-sm hover:bg-white/5"
            >
              Back to Learn
            </Link>
            <button
              onClick={() => {
                setPhase("hook");
                setSubPhase(0);
                setSelectedAnswer(null);
                setAnswerResult(null);
                setShowExplanation(false);
                setCompleted(false);
                setMistakeCount(0);
                setBuildCode("");
                setBuildResult(null);
                setAssessmentAnswers({});
                setAssessmentResult(null);
                setBreakDiagnosis("");
                setBreakFix("");
                setBreakResult(null);
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

  const renderCaptainByte = () => (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="mb-6"
    >
      <Mentor mood={captainByteMood} message={captainByteMessage} size="full" />
    </motion.div>
  );

  const renderVisualPrimitive = (primitive: VisualPrimitive) => {
    switch (primitive.type) {
      case "highlight":
        return (
          <div className="rounded-xl border border-brand-sky/30 bg-brand-sky/10 p-4 mb-4">
            <p className="text-xs font-mono text-brand-sky mb-2">
              {primitive.instruction}
            </p>
            <div className="font-mono text-sm text-brand-secondary whitespace-pre-wrap">
              {JSON.stringify(primitive.data, null, 2)}
            </div>
          </div>
        );
      case "move":
        return (
          <div className="rounded-xl border border-brand-sky/30 bg-brand-sky/10 p-4 mb-4">
            <p className="text-xs font-mono text-brand-sky mb-2">
              {primitive.instruction}
            </p>
            <div className="font-mono text-sm text-brand-secondary">
              {JSON.stringify(primitive.data)}
            </div>
          </div>
        );
      default:
        return (
          <div className="rounded-xl border border-brand-sky/30 bg-brand-sky/10 p-4 mb-4">
            <p className="text-xs font-mono text-brand-sky">{primitive.instruction}</p>
          </div>
        );
    }
  };

  const renderHook = () => (
    <motion.div
      key="hook"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-white/10 bg-surface-base/80 p-6"
    >
      <div className="flex items-center gap-2 mb-4">
        <Compass className="h-5 w-5 text-brand-sky" />
        <h2 className="text-lg font-bold">{lesson.story_context.title}</h2>
      </div>
      <p className="text-sm leading-relaxed text-text-primary mb-4">
        {lesson.story_context.intro_text}
      </p>
      <p className="text-xs text-text-secondary mb-4">
        {lesson.story_context.setting} · {lesson.story_context.character}
      </p>
      {renderCaptainByte()}
      <button
        onClick={goNext}
        className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90"
      >
        Start Learning <ChevronRight size={14} className="inline ml-1" />
      </button>
    </motion.div>
  );

  const renderSee = () => {
    const step = lesson.discovery.steps[subPhase];
    if (!step) {
      setPhase("understand");
      return null;
    }
    const interaction = step.interaction;
    let answerCorrect: boolean | undefined;
    let answerExplanation = "";

    if (interaction.type === "choose_outcome" && interaction.options && selectedAnswer) {
      const selected = interaction.options.find((o) => o.id === selectedAnswer);
      answerCorrect = selected?.correct;
      answerExplanation = selected?.explanation || "";
    }

    return (
      <motion.div
        key={`see-${subPhase}`}
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="rounded-2xl border border-white/10 bg-surface-base/80 p-6"
      >
        <h2 className="text-lg font-bold mb-2">{lesson.discovery.title}</h2>
        <p className="text-sm leading-relaxed text-text-primary mb-4">
          {step.narration}
        </p>

        {interaction.type === "visual_primitive" && interaction.primitive && (
          <div>{renderVisualPrimitive(interaction.primitive)}</div>
        )}

        {interaction.type === "inspect_code" && interaction.code && (
          <div className="rounded-xl border border-white/5 bg-white/5 p-4 mb-4">
            <pre className="text-xs font-mono text-brand-secondary whitespace-pre-wrap">
              {interaction.code}
            </pre>
          </div>
        )}

        {interaction.type === "choose_outcome" && interaction.options && (
          <div className="space-y-2 mb-4">
            {interaction.options.map((opt) => {
              const isSelected = selectedAnswer === opt.id;
              let cls =
                "w-full text-left rounded-xl border px-4 py-3 text-sm transition-all ";
              if (showExplanation) {
                if (opt.correct) {
                  cls += "border-green-500/50 bg-green-500/10 text-green-300";
                } else if (isSelected && !opt.correct) {
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
                  key={opt.id}
                  onClick={() =>
                    handleDiscoveryAnswer(opt.id, opt.correct, opt.explanation || "")
                  }
                  disabled={showExplanation}
                  className={cls}
                >
                  <span className="font-mono mr-2 text-xs">{opt.id}.</span>
                  {opt.text}
                  {showExplanation && opt.correct && (
                    <CheckCircle2 className="inline ml-2 h-4 w-4 text-green-400" />
                  )}
                  {showExplanation && isSelected && !opt.correct && (
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

        {interaction.hint && !showExplanation && (
          <p className="text-xs text-text-secondary mb-4">💡 {interaction.hint}</p>
        )}

        <div className="flex items-center justify-between mt-4">
          <button
            onClick={goBack}
            disabled={subPhase === 0}
            className="rounded-xl border border-white/10 px-4 py-2 text-sm disabled:opacity-30 hover:bg-white/5"
          >
            <ArrowLeft size={14} className="inline mr-1" />
            Back
          </button>
          <button
            onClick={() => {
              if (!showExplanation) return;
              if (subPhase < lesson.discovery.steps.length - 1) {
                setSubPhase((s) => s + 1);
                setSelectedAnswer(null);
                setAnswerResult(null);
                setShowExplanation(false);
              } else {
                goNext();
              }
            }}
            disabled={!showExplanation}
            className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90 disabled:opacity-50"
          >
            {subPhase < lesson.discovery.steps.length - 1 ? (
              <>
                Next <ChevronRight size={14} className="inline ml-1" />
              </>
            ) : (
              <>
                Understand <ChevronRight size={14} className="inline ml-1" />
              </>
            )}
          </button>
        </div>
      </motion.div>
    );
  };

  const renderUnderstand = () => (
    <motion.div
      key="understand"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-2xl border border-white/10 bg-surface-base/80 p-6"
    >
      <h2 className="text-lg font-bold mb-2">{lesson.explain.title}</h2>
      <p className="text-sm leading-relaxed text-text-primary mb-4">
        {lesson.explain.prompt}
      </p>
      {renderCaptainByte()}
      <div className="rounded-xl border border-brand-sky/30 bg-brand-sky/10 p-4 mb-4">
        <p className="text-sm text-brand-sky">
          <strong>Key insight:</strong> {lesson.explain.model_answer}
        </p>
      </div>
      <div className="flex justify-end">
        <button
          onClick={goNext}
          className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90"
        >
          Predict <ChevronRight size={14} className="inline ml-1" />
        </button>
      </div>
    </motion.div>
  );

  const renderPredict = () => {
    const prediction = lesson.prediction;
    let answerCorrect: boolean | undefined;
    let answerExplanation = "";

    if (selectedAnswer && prediction.options) {
      const selected = prediction.options.find((o) => o.id === selectedAnswer);
      answerCorrect = selected?.correct;
      answerExplanation = selected?.explanation || "";
    }

    return (
      <motion.div
        key="predict"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl border border-white/10 bg-surface-base/80 p-6"
      >
        <h2 className="text-lg font-bold mb-2">{prediction.title}</h2>
        <p className="text-sm leading-relaxed text-text-primary mb-4">
          {prediction.question}
        </p>
        {prediction.code && (
          <div className="rounded-xl border border-white/5 bg-white/5 p-4 mb-4">
            <pre className="text-xs font-mono text-brand-secondary whitespace-pre-wrap">
              {prediction.code}
            </pre>
          </div>
        )}
        <div className="space-y-2 mb-4">
          {prediction.options.map((opt) => {
            const isSelected = selectedAnswer === opt.id;
            let cls =
              "w-full text-left rounded-xl border px-4 py-3 text-sm transition-all ";
            if (showExplanation) {
              if (opt.correct) {
                cls += "border-green-500/50 bg-green-500/10 text-green-300";
              } else if (isSelected && !opt.correct) {
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
                key={opt.id}
                onClick={() =>
                  handlePredictAnswer(opt.id, opt.correct, opt.explanation)
                }
                disabled={showExplanation}
                className={cls}
              >
                <span className="font-mono mr-2 text-xs">{opt.id}.</span>
                {opt.text}
                {showExplanation && opt.correct && (
                  <CheckCircle2 className="inline ml-2 h-4 w-4 text-green-400" />
                )}
                {showExplanation && isSelected && !opt.correct && (
                  <XCircle className="inline ml-2 h-4 w-4 text-red-400" />
                )}
              </button>
            );
          })}
        </div>

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

        {renderCaptainByte()}

        <div className="flex justify-end">
          <button
            onClick={goNext}
            disabled={!showExplanation}
            className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90 disabled:opacity-50"
          >
            {showExplanation ? (
              <>
                Change <ChevronRight size={14} className="inline ml-1" />
              </>
            ) : (
              "Make a prediction"
            )}
          </button>
        </div>
      </motion.div>
    );
  };

  const renderBuild = () => {
    const step = lesson.guided_build.steps[subPhase];
    if (!step) {
      setPhase("break");
      return null;
    }

    const runBuild = async () => {
      setBuildRunning(true);
      setBuildResult(null);
      try {
        const res: any = await lessonApi.submitBuild(lessonSlug, {
          code: buildCode,
          function_name: step.function_name,
          language: "python",
          step_index: subPhase,
        });
        setBuildResult(res);
        if (res.passed || res.score >= 70) {
          setMistakeCount(0);
          showCaptainByte(
            lesson.captain_byte.correct[Math.min(mistakeCount, lesson.captain_byte.correct.length - 1)],
            "proud"
          );
        } else {
          setMistakeCount((c) => c + 1);
          showCaptainByte(
            lesson.captain_byte.wrong[Math.min(mistakeCount, lesson.captain_byte.wrong.length - 1)],
            "correcting"
          );
        }
      } catch {
        setBuildResult({ error: "Failed to run code" });
      } finally {
        setBuildRunning(false);
      }
    };

    return (
      <motion.div
        key={`build-${subPhase}`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl border border-white/10 bg-surface-base/80 p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold">{step.title}</h2>
            <p className="text-xs text-text-secondary">
              Step {subPhase + 1}/{lesson.guided_build.steps.length}
            </p>
          </div>
          <span className="text-xs text-brand-sky">+{step.diamonds} 💎</span>
        </div>

        <p className="text-sm leading-relaxed text-text-primary mb-4">
          {step.description}
        </p>

        <div className="rounded-xl border border-white/5 bg-white/5 p-4 mb-4">
          <pre className="text-xs font-mono text-brand-secondary whitespace-pre-wrap">
            {step.signature}
          </pre>
        </div>

        <textarea
          value={buildCode}
          onChange={(e) => setBuildCode(e.target.value)}
          className="w-full h-40 rounded-xl border border-white/10 bg-surface-base p-4 font-mono text-sm text-text-primary focus:border-brand-sky focus:outline-none"
          placeholder={step.starter_code}
        />

        {buildResult && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-xl border p-4 mb-4 ${
              buildResult.passed || buildResult.score >= 70
                ? "border-green-500/30 bg-green-500/10"
                : "border-red-500/30 bg-red-500/10"
            }`}
          >
            <p className="text-sm">
              {buildResult.passed || buildResult.score >= 70 ? (
                <span className="text-green-300">
                  ✅ Passed! Score: {buildResult.score}%
                </span>
              ) : (
                <span className="text-red-300">
                  ❌ Not yet. Score: {buildResult.score}%
                </span>
              )}
            </p>
            {buildResult.results && (
              <div className="mt-2 space-y-1">
                {buildResult.results.map((r: any, i: number) => (
                  <p key={i} className="text-xs text-text-secondary">
                    Test {i + 1}: {r.passed ? "✅" : "❌"} {r.error || ""}
                  </p>
                ))}
              </div>
            )}
          </motion.div>
        )}

        {renderCaptainByte()}

        <div className="flex items-center justify-between mt-4">
          <button
            onClick={goBack}
            disabled={subPhase === 0}
            className="rounded-xl border border-white/10 px-4 py-2 text-sm disabled:opacity-30 hover:bg-white/5"
          >
            <ArrowLeft size={14} className="inline mr-1" />
            Back
          </button>
          <div className="flex gap-2">
            <button
              onClick={runBuild}
              disabled={buildRunning}
              className="rounded-xl border border-brand-sky/30 bg-brand-sky/10 px-4 py-2 text-sm text-brand-sky hover:bg-brand-sky/20 disabled:opacity-50"
            >
              {buildRunning ? (
                <Loader2 className="inline h-4 w-4 animate-spin" />
              ) : (
                "Run"
              )}
            </button>
            <button
              onClick={() => {
                if (subPhase < lesson.guided_build.steps.length - 1) {
                  setSubPhase((s) => s + 1);
                  setBuildCode(lesson.guided_build.steps[subPhase + 1]?.starter_code || "");
                  setBuildResult(null);
                  showCaptainByte(
                    lesson.guided_build.steps[subPhase + 1]?.captain_byte_moment ||
                      lesson.captain_byte.correct[0],
                    "explaining"
                  );
                } else {
                  goNext();
                }
              }}
              className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90"
            >
              {subPhase < lesson.guided_build.steps.length - 1 ? (
                <>
                  Next <ChevronRight size={14} className="inline ml-1" />
                </>
              ) : (
                <>
                  Prove <ChevronRight size={14} className="inline ml-1" />
                </>
              )}
            </button>
          </div>
        </div>
      </motion.div>
    );
  };

  const renderBreak = () => {
    const brk = lesson.break;
    let selectedDiagnosis: string | null = null;

    return (
      <motion.div
        key="break"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl border border-white/10 bg-surface-base/80 p-6"
      >
        <h2 className="text-lg font-bold mb-2">{brk.title}</h2>
        <p className="text-sm leading-relaxed text-text-primary mb-4">
          {brk.story}
        </p>

        <div className="rounded-xl border border-white/5 bg-white/5 p-4 mb-4">
          <pre className="text-xs font-mono text-brand-secondary whitespace-pre-wrap">
            {brk.buggy_code}
          </pre>
        </div>

        <p className="text-xs text-text-secondary mb-2">
          Expected: {brk.expected_output}
        </p>
        <p className="text-xs text-red-300 mb-4">
          Actual: {brk.actual_output}
        </p>

        <p className="text-sm font-bold mb-2">{brk.diagnosis.question}</p>
        <div className="space-y-2 mb-4">
          {brk.diagnosis.options.map((opt) => {
            const isSelected = breakDiagnosis === opt.id;
            let cls =
              "w-full text-left rounded-xl border px-4 py-3 text-sm transition-all ";
            if (breakResult) {
              if (opt.correct) {
                cls += "border-green-500/50 bg-green-500/10 text-green-300";
              } else if (isSelected && !opt.correct) {
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
                key={opt.id}
                onClick={() => setBreakDiagnosis(opt.id)}
                disabled={!!breakResult}
                className={cls}
              >
                <span className="font-mono mr-2 text-xs">{opt.id}.</span>
                {opt.text}
                {breakResult && opt.correct && (
                  <CheckCircle2 className="inline ml-2 h-4 w-4 text-green-400" />
                )}
                {breakResult && isSelected && !opt.correct && (
                  <XCircle className="inline ml-2 h-4 w-4 text-red-400" />
                )}
              </button>
            );
          })}
        </div>

        {breakResult && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-xl border border-green-500/30 bg-green-500/10 p-4 mb-4"
          >
            <p className="text-sm text-green-300">{brk.explanation}</p>
          </motion.div>
        )}

        {renderCaptainByte()}

        <div className="flex justify-end">
          <button
            onClick={() => {
              if (!breakDiagnosis) return;
              if (!breakResult) {
                const selected = brk.diagnosis.options.find(
                  (o) => o.id === breakDiagnosis
                );
                setBreakResult(selected);
                if (selected?.correct) {
                  showCaptainByte(lesson.captain_byte.after_break, "proud");
                }
              } else {
                goNext();
              }
            }}
            disabled={!breakDiagnosis}
            className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90 disabled:opacity-50"
          >
            {breakResult ? "Continue" : "Diagnose"}
          </button>
        </div>
      </motion.div>
    );
  };

  const renderProve = () => {
    const assessment = lesson.assessment;
    const allAnswered = assessment.questions.every(
      (q, i) => assessmentAnswers[`q${i}`] !== undefined
    );

    const submitAssessment = async () => {
      setSaving(true);
      try {
        const res: any = await lessonApi.checkAssessment(lessonSlug, {
          answers: assessmentAnswers,
          time_spent_seconds: 0,
        });
        setAssessmentResult(res);
        if (res.passed || res.score >= assessment.mastery_threshold) {
          setMistakeCount(0);
          showCaptainByte(lesson.captain_byte.after_mastery, "celebrating");
        } else {
          showCaptainByte(
            lesson.captain_byte.wrong[0] || "Review and try again.",
            "correcting"
          );
        }
      } catch {
        setAssessmentResult({ passed: false, score: 0 });
      } finally {
        setSaving(false);
      }
    };

    return (
      <motion.div
        key="prove"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-2xl border border-white/10 bg-surface-base/80 p-6"
      >
        <h2 className="text-lg font-bold mb-2">{assessment.title}</h2>
        <p className="text-sm text-text-secondary mb-4">{assessment.description}</p>

        {assessment.questions.map((q, i) => (
          <div key={i} className="mb-6">
            <p className="text-sm font-bold mb-2">
              Q{i + 1}: {q.question}
            </p>

            {q.type === "code_tracing" && q.code && (
              <div className="rounded-xl border border-white/5 bg-white/5 p-4 mb-3">
                <pre className="text-xs font-mono text-brand-secondary whitespace-pre-wrap">
                  {q.code}
                </pre>
              </div>
            )}

            {q.type === "debug" && q.code && (
              <div className="rounded-xl border border-red-500/20 bg-red-500/5 p-4 mb-3">
                <pre className="text-xs font-mono text-red-300 whitespace-pre-wrap">
                  {q.code}
                </pre>
                <p className="text-xs text-red-300 mt-2">Error: {q.error}</p>
              </div>
            )}

            <input
              type="text"
              value={assessmentAnswers[`q${i}`] || ""}
              onChange={(e) =>
                setAssessmentAnswers((a) => ({ ...a, [`q${i}`]: e.target.value }))
              }
              className="w-full rounded-xl border border-white/10 bg-surface-base px-4 py-3 text-sm text-text-primary focus:border-brand-sky focus:outline-none"
              placeholder="Your answer..."
              disabled={!!assessmentResult}
            />
          </div>
        ))}

        {assessmentResult && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-xl border p-4 mb-4 ${
              assessmentResult.passed || assessmentResult.score >= assessment.mastery_threshold
                ? "border-green-500/30 bg-green-500/10"
                : "border-red-500/30 bg-red-500/10"
            }`}
          >
            <p className="text-sm">
              {assessmentResult.passed || assessmentResult.score >= assessment.mastery_threshold ? (
                <span className="text-green-300">
                  ✅ Passed! Score: {assessmentResult.score}%
                </span>
              ) : (
                <span className="text-red-300">
                  ❌ Not yet. Score: {assessmentResult.score}%. Threshold:{" "}
                  {assessment.mastery_threshold}%
                </span>
              )}
            </p>
          </motion.div>
        )}

        {renderCaptainByte()}

        <div className="flex justify-end">
          <button
            onClick={submitAssessment}
            disabled={!allAnswered || !!assessmentResult || saving}
            className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90 disabled:opacity-50"
          >
            {saving ? (
              <Loader2 className="inline h-4 w-4 animate-spin" />
            ) : (
              "Submit Assessment"
            )}
          </button>
        </div>
      </motion.div>
    );
  };

  const renderReward = () => (
    <motion.div
      key="reward"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="rounded-2xl border border-white/10 bg-surface-base/80 p-6 text-center"
    >
      <Trophy className="mx-auto h-12 w-12 text-yellow-400 mb-3" />
      <h2 className="text-2xl font-bold mb-2">Lesson Complete!</h2>
      <p className="text-text-secondary mb-4">{lesson.title}</p>

      {renderCaptainByte()}

      <div className="flex justify-center gap-3 mt-6">
        <Link
          to="/learn"
          className="rounded-xl border border-white/10 px-4 py-2 text-sm hover:bg-white/5"
        >
          Back to Learn
        </Link>
        <button
          onClick={() => {
            setPhase("hook");
            setSubPhase(0);
            setSelectedAnswer(null);
            setAnswerResult(null);
            setShowExplanation(false);
            setMistakeCount(0);
            setBuildCode("");
            setBuildResult(null);
            setAssessmentAnswers({});
            setAssessmentResult(null);
            setBreakDiagnosis("");
            setBreakFix("");
            setBreakResult(null);
          }}
          className="rounded-xl bg-brand-sky px-4 py-2 text-sm text-white hover:bg-brand-sky/90"
        >
          Review Again
        </button>
      </div>
    </motion.div>
  );

  const renderPhase = () => {
    switch (phase) {
      case "hook":
        return renderHook();
      case "see":
        return renderSee();
      case "understand":
        return renderUnderstand();
      case "predict":
        return renderPredict();
      case "build":
        return renderBuild();
      case "break":
        return renderBreak();
      case "prove":
        return renderProve();
      case "reward":
        return renderReward();
      default:
        return renderHook();
    }
  };

  const phaseLabels: Record<Phase, string> = {
    hook: "Hook",
    see: "See",
    understand: "Understand",
    touch: "Touch",
    predict: "Predict",
    change: "Change",
    build: "Build",
    break: "Break",
    fix: "Fix",
    retrieve: "Retrieve",
    transfer: "Transfer",
    prove: "Prove",
    reward: "Reward",
  };

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
              {lesson.module_id} · {lesson.difficulty} · {lesson.est_minutes} min
            </p>
          </div>
          <div className="text-right">
            <p className="text-xs text-text-secondary">
              {phaseLabels[phase]}
            </p>
            </div>
        </div>
        <div className="h-2 rounded-full bg-white/5 overflow-hidden">
          <motion.div
            className="h-full bg-brand-sky"
            initial={{ width: 0 }}
            animate={{
              width: `${
                ((["hook", "see", "understand", "touch", "predict", "change", "build", "break", "fix", "retrieve", "transfer", "prove", "reward"].indexOf(phase) + 1) / 13) *
                100
              }%`,
            }}
            transition={{ duration: 0.3 }}
          />
        </div>
      </div>

      <AnimatePresence mode="wait">{renderPhase()}</AnimatePresence>
    </div>
  );
}
