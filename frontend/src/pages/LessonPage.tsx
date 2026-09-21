import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import Editor from "@monaco-editor/react";
import {
  Play,
  RotateCcw,
  Loader2,
  Terminal,
  CheckCircle2,
  XCircle,
  Lightbulb,
  ChevronLeft,
  ChevronRight,
  Zap,
  Trophy,
  Clock,
  SkipForward,
} from "lucide-react";
import api from "../services/api";
import { candyGradient } from "../components/candy/palette";
import type { CandyColor } from "../components/candy/palette";
import CelebrationOverlay from "../components/CelebrationOverlay";
import useReducedMotion from "../hooks/useReducedMotion";
import useAuthStore from "../store/authStore";

type LessonStep = {
  type: string;
  title: string;
  content?: string;
  narration?: string;
  code?: string;
  expected_output?: string;
  hint?: string;
  simulation?: { type: string; initial_state: string; user_can_run?: boolean };
  interaction?: {
    type: string;
    prompt?: string;
    reveal_after?: string;
  };
  question?: string;
  options?: Array<{ id: string; text: string; correct: boolean; explanation: string }>;
  explanation?: string;
  inputs_to_try?: string[];
  correct_set?: string[];
  function_name?: string;
  signature?: string;
  description?: string;
  starter_code?: string;
  test_cases?: Array<{ input: unknown[]; expected: unknown }>;
  hidden_test_cases?: Array<{ input: unknown[]; expected: unknown }>;
  hidden_tests?: number;
  diamonds?: number;
  scaffolded_hints?: Array<{ level: number; text: string }>;
  timed?: boolean;
  time_limit_minutes?: number;
  mastery_threshold?: number;
  answer_format?: string;
  expected_answer?: string;
  keywords?: string[];
  error?: string;
  fix?: string;
  repair_steps?: Array<{ title?: string; content: string; hint?: string }>;
  passing_score?: number;
  max_attempts?: number;
  is_debug?: boolean;
  buggy_code?: string;
  languages?: string[];
  starter_code_per_language?: Record<string, string>;
  signatures_per_language?: Record<string, string>;
};

type LessonContent = {
  lesson_id: string;
  title: string;
  description: string;
  difficulty: string;
  est_minutes: number;
  xp_reward: number;
  skills_taught: string[];
  story_context: {
    title: string;
    narration: string;
    setting: string;
    character: string;
    intro_text: string;
  };
  discovery: {
    title: string;
    steps: LessonStep[];
    conclusion: string;
  };
  prediction: LessonStep;
  guided_build: {
    title: string;
    steps: LessonStep[];
  };
  transfer_challenge: LessonStep;
  assessment: {
    title: string;
    description: string;
    questions: LessonStep[];
    mastery_threshold: number;
    diamonds: number;
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

type TestCaseResult = {
  test_case_index: number;
  passed: boolean;
  input: unknown;
  expected: string;
  actual: string;
  error: string | null;
};

type BuildResult = {
  passed: boolean;
  all_passed: boolean;
  passed_count: number;
  total_count: number;
  score: number;
  results: TestCaseResult[];
  error?: string;
  compile_error?: string;
  hidden_pass_rate?: number;
  hidden_results?: TestCaseResult[];
};

const ALL_PHASES = ["story", "discover", "manipulate", "predict", "build", "break", "debug", "retrieve", "transfer", "mastery", "assess", "complete"];

export default function LessonPage() {
  const { slug } = useParams();
  const lessonSlug = slug || "variables_state";
  const [phase, setPhase] = useState("story");
  const [lesson, setLesson] = useState<LessonContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeDiscoveryStep, setActiveDiscoveryStep] = useState(0);
  const [activeBuildStep, setActiveBuildStep] = useState(0);
  const [code, setCode] = useState("");
  const [running, setRunning] = useState(false);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [buildResult, setBuildResult] = useState<BuildResult | null>(null);
  const [hintLevel, setHintLevel] = useState(0);
  const [predictionAnswer, setPredictionAnswer] = useState("");
  const [predictionChecked, setPredictionChecked] = useState(false);
  const [assessmentAnswers, setAssessmentAnswers] = useState<Record<string, string>>({});
  const [assessmentScore, setAssessmentScore] = useState<number | null>(null);
  const [assessmentResult, setAssessmentResult] = useState<{
    score: number;
    passed: boolean;
    results: Array<{ index: number; type: string; correct: boolean; explanation: string }>;
    earned: number;
    total: number;
  } | null>(null);
  const [showCompletion, setShowCompletion] = useState(false);
  const [completionData, setCompletionData] = useState<any>(null);
  const [startTime] = useState(Date.now());
  const [attempts, setAttempts] = useState<Record<number, number>>({});
  const [showRepair, setShowRepair] = useState(false);
  const [transferAttempts, setTransferAttempts] = useState<Record<number, number>>({});
  const [showTransferRepair, setShowTransferRepair] = useState(false);
  const reduced = useReducedMotion();
  const { user } = useAuthStore();
  const transferInitRef = useRef(false);
  const { isBrowserNative, execute: browserExecute } = useBrowserRuntime();
  const navigate = useNavigate();

  useEffect(() => {
    api.lesson.getLesson<LessonContent>(lessonSlug).then(setLesson).finally(() => setLoading(false));
  }, [lessonSlug]);

  const currentBuildStep = lesson?.guided_build.steps[activeBuildStep];
  const totalBuildSteps = lesson?.guided_build.steps.length || 1;

  const startStep = currentBuildStep?.step_order;

  // Initialize code editor with starter code when build step changes
  useEffect(() => {
    if (currentBuildStep?.starter_code) {
      setCode(currentBuildStep.starter_code);
    } else if (currentBuildStep?.code) {
      setCode(currentBuildStep.code);
    }
    setBuildResult(null);
    setHintLevel(0);
    setOutput("");
    setError("");
    setShowRepair(false);
  }, [currentBuildStep]);

  useEffect(() => {
    if (phase === "transfer") {
      if (!transferInitRef.current && lesson?.transfer_challenge?.starter_code) {
        setCode(lesson.transfer_challenge.starter_code);
        transferInitRef.current = true;
        setBuildResult(null);
        setHintLevel(0);
        setOutput("");
        setError("");
        setTransferAttempts({});
        setShowTransferRepair(false);
      }
    } else {
      transferInitRef.current = false;
    }
  }, [phase, lesson]);

  const handleRunExplore = useCallback(async () => {
    if (!lesson || !code) return;
    setRunning(true);
    setOutput("");
    setError("");
    try {
      if (isBrowserNative("python")) {
        const result = await browserExecute("python", code, "", 10000);
        if (result.success) {
          setOutput(result.stdout || "(no output)");
        } else {
          setError(result.stderr || result.compile_error || "Execution failed");
        }
        return;
      }
      const result = await api.executeCompilerCode({
        code,
        language: "python",
        stdin: "",
        timeout: 10,
      });
      if (result.success) {
        setOutput(result.stdout || "(no output)");
      } else {
        setError(result.stderr || result.error || "Execution failed");
      }
    } catch (err: any) {
      setError(err.message || "Failed to execute");
    } finally {
      setRunning(false);
    }
  }, [code, lesson, isBrowserNative, browserExecute]);

  const handleSubmitBuild = useCallback(async () => {
    if (!lesson || !currentBuildStep) return;
    setRunning(true);
    setError("");
    setBuildResult(null);
    setShowRepair(false);
    try {
      const result: BuildResult = await api.lesson.submitBuild(lessonSlug, {
        code,
        function_name: currentBuildStep.function_name || "",
        language: "python",
        step_index: activeBuildStep,
      });
      setBuildResult(result);

      const stepAttempts = (attempts[activeBuildStep] || 0) + 1;
      setAttempts((prev) => ({ ...prev, [activeBuildStep]: stepAttempts }));

      if (!result.all_passed && stepAttempts < (currentBuildStep.max_attempts || 3)) {
        setShowRepair(true);
      }
    } catch (err: any) {
      setError(err.message || "Submission failed");
    } finally {
      setRunning(false);
    }
  }, [code, currentBuildStep, activeBuildStep, lesson, attempts]);

  const handleShowHint = useCallback(() => {
    if (!currentBuildStep?.scaffolded_hints || hintLevel >= currentBuildStep.scaffolded_hints.length) return;
    setHintLevel((prev) => prev + 1);
  }, [currentBuildStep, hintLevel]);

  const checkPrediction = useCallback(() => {
    setPredictionChecked(true);
  }, []);

  const predictionOption = lesson?.prediction.options.find((o) => o.id === predictionAnswer);
  const predictionCorrect = predictionChecked && predictionOption?.correct;

  const handleAssessSubmit = useCallback(async () => {
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);
    try {
      const result = await api.lesson.checkAssessment(lessonSlug, {
        answers: assessmentAnswers,
        time_spent_seconds: timeSpent,
      });
      setAssessmentResult(result);
      setAssessmentScore(result.score);
    } catch (err: any) {
      setError(err.message || "Assessment failed");
    }
  }, [assessmentAnswers, startTime]);

  const handleComplete = useCallback(async () => {
    if (assessmentScore === null) return;
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);
    try {
      const result = await api.lesson.completeLesson(lessonSlug, {
        score: assessmentScore,
        time_spent_seconds: timeSpent,
      });
      setCompletionData(result);
      setPhase("complete");
    } catch (err: any) {
      setError(err.message || "Completion failed");
    }
  }, [assessmentScore, startTime, lessonSlug]);

  if (loading || !lesson) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-surface-base">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto text-brand-sky" />
          <p className="mt-2 text-sm text-text-secondary">Loading the Memory Palace...</p>
        </div>
      </div>
    );
  }

  const storyBg = candyGradient("mint" as CandyColor);

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <AnimatePresence mode="wait">
        {/* STORY / CONTEXT PHASE */}
        {phase === "story" && (
          <motion.div
            key="story"
            className="min-h-screen flex flex-col items-center justify-center p-6"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div
              className="max-w-3xl mx-auto p-8 rounded-3xl border border-brand-primary/10 text-center"
              style={{
                background: `linear-gradient(135deg, ${storyBg}, rgba(0,201,167,0.05))`,
              }}
            >
              <div className="text-6xl mb-6">{lesson.story_context.character === "Memory Keeper" ? "🏠" : "📚"}</div>
              <h1 className="text-3xl font-bold text-text-primary mb-4">
                {lesson.story_context.title}
              </h1>
              <p className="text-lg text-text-secondary mb-6 leading-relaxed">
                {lesson.story_context.intro_text}
              </p>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("discover")}
                className="px-8 py-3 rounded-xl bg-brand-sky text-white font-bold text-sm hover:bg-brand-sky/90 transition-colors flex items-center gap-2 mx-auto"
              >
                Enter the Palace
                <ChevronRight size={16} />
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* DISCOVERY PHASE */}
        {phase === "discover" && (
          <motion.div
            key="discover"
            className="max-w-4xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-bold text-text-primary">{lesson.discovery.title}</h2>
              <div className="flex gap-1 text-xs text-text-secondary">
                Room {activeDiscoveryStep + 1} of {lesson.discovery.steps.length}
              </div>
            </div>

            <DiscoveryStepView
              step={lesson.discovery.steps[activeDiscoveryStep]}
              onInsight={handleRunExplore}
              codeState={{ code, setCode, output, setOutput, error, setError, running, setRunning }}
              reduced={reduced}
            />

            <div className="flex justify-between mt-8">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => {
                  if (activeDiscoveryStep > 0) setActiveDiscoveryStep((s) => s - 1);
                  else setPhase("story");
                }}
                className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/10 text-sm font-medium"
              >
                <ChevronLeft size={16} /> Previous
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => {
                  if (activeDiscoveryStep < lesson.discovery.steps.length - 1) {
                    setActiveDiscoveryStep((s) => s + 1);
                  } else {
                    setPhase("predict");
                  }
                }}
                className="px-4 py-2 rounded-xl bg-brand-sky text-white font-medium"
              >
                {activeDiscoveryStep < lesson.discovery.steps.length - 1 ? "Next" : "Continue"}
                <ChevronRight size={16} />
              </motion.button>
            </div>

            <div className="mt-6 text-xs text-text-secondary bg-surface-card/30 rounded-xl p-4 border border-brand-primary/5">
              <p className="mb-2">💡 Insight:</p>
              <p>{lesson.discovery.conclusion}</p>
            </div>
          </motion.div>
        )}

        {/* MANIPULATE PHASE */}
        {phase === "manipulate" && (
          <motion.div
            key="manipulate"
            className="max-w-3xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <h2 className="text-xl font-bold text-text-primary mb-6">Manipulate</h2>
            <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-6 mb-6">
              <p className="text-sm text-text-secondary mb-4">Complete the pattern below.</p>
              <div className="rounded-xl border border-brand-primary/10 overflow-hidden mb-4">
                <div className="h-52 sm:h-64">
                  <Editor
                    height="100%"
                    language="python"
                    theme="vs-dark"
                    value={code}
                    onChange={setCode}
                    options={{
                      minimap: { enabled: false },
                      fontSize: 13,
                      tabSize: 2,
                      lineNumbers: "on",
                      wordWrap: "on",
                      padding: { top: 8 },
                    }}
                  />
                </div>
              </div>
            </div>
            <div className="flex justify-between">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("discover")}
                className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/10 text-sm font-medium"
              >
                <ChevronLeft size={16} /> Back
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("predict")}
                className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold"
              >
                Continue to Predict <ChevronRight size={16} />
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* PREDICTION PHASE */}
        {phase === "predict" && (
          <motion.div
            key="predict"
            className="max-w-3xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <h2 className="text-xl font-bold text-text-primary mb-6">{lesson.prediction.title}</h2>

            <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-6 mb-6">
              <p className="text-sm text-text-secondary mb-4">{lesson.prediction.question}</p>
              <pre className="bg-surface-base/50 rounded-lg p-4 text-sm font-mono mb-4 overflow-x-auto">
                {lesson.prediction.code}
              </pre>

              <div className="space-y-2">
                {lesson.prediction.options.map((opt) => (
                  <label
                    key={opt.id}
                    className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-all ${
                      predictionAnswer === opt.id
                        ? "border-brand-sky bg-brand-sky/10"
                        : "border-brand-primary/10 hover:border-brand-primary/20"
                    }`}
                  >
                    <input
                      type="radio"
                      name="prediction"
                      value={opt.id}
                      checked={predictionAnswer === opt.id}
                      onChange={(e) => setPredictionAnswer(e.target.value)}
                      className="text-brand-sky focus:ring-brand-sky"
                    />
                    <span className="font-medium text-text-secondary">{opt.id.toUpperCase()}:</span>
                    <span>{opt.text}</span>
                  </label>
                ))}
              </div>

              {predictionChecked && predictionOption && (
                <motion.div
                  className={`mt-4 p-4 rounded-xl border ${
                    predictionCorrect
                      ? "bg-green-500/10 border-green-500/30"
                      : "bg-red-500/10 border-red-500/30"
                  }`}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <div className="flex items-center gap-2 mb-2">
                    {predictionCorrect ? <CheckCircle2 className="text-green-400" /> : <XCircle className="text-red-400" />}
                    <span className="font-bold">
                      {predictionCorrect ? "Correct!" : "Not quite"}
                    </span>
                  </div>
                  <p className="text-sm text-text-secondary">{predictionOption.explanation}</p>
                </motion.div>
              )}
            </div>

            <div className="flex justify-between">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("discover")}
                className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/10 text-sm font-medium"
              >
                <ChevronLeft size={16} /> Back
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("build")}
                className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold"
              >
                Continue to Build
                <ChevronRight size={16} />
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* GUIDED BUILD PHASE */}
        {phase === "build" && currentBuildStep && (
          <motion.div
            key="build"
            className="max-w-5xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <div className="mb-6">
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-xl font-bold text-text-primary">
                  {currentBuildStep.title}
                </h2>
                <div className="flex gap-2 text-xs text-text-secondary">
                  <span className="px-2 py-1 bg-surface-card/60 rounded-full">
                    Step {activeBuildStep + 1} of {totalBuildSteps}
                  </span>
                  {currentBuildStep.diamonds && (
                    <span className="px-2 py-1 bg-yellow-500/10 text-yellow-400 rounded-full">
                      +{currentBuildStep.diamonds} Diamonds
                    </span>
                  )}
                </div>
              </div>
              <p className="text-sm text-text-secondary">{currentBuildStep.description}</p>
              {currentBuildStep.signature && (
                <pre className="mt-2 text-xs font-mono text-text-secondary bg-surface-base/30 rounded px-3 py-2">
                  {currentBuildStep.signature}
                </pre>
              )}
            </div>

            <div className="space-y-4">
              {/* Hint Ladder */}
              {currentBuildStep.scaffolded_hints && (
                <div className="flex gap-2">
                  {currentBuildStep.scaffolded_hints.map((_, i) => (
                    <button
                      key={i}
                      onClick={() => setHintLevel(i + 1)}
                      disabled={i + 1 > hintLevel && !buildResult?.passed}
                      className={`p-2 rounded-lg text-xs font-medium transition-all ${
                        hintLevel >= i + 1
                          ? "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30"
                          : "bg-surface-card/40 text-text-secondary border border-brand-primary/10 disabled:opacity-50"
                      }`}
                      title={`Hint Level ${i + 1}`}
                    >
                      <Lightbulb size={14} className="inline mr-1" />
                      Hint {i + 1}
                    </button>
                  ))}
                </div>
              )}

              {hintLevel > 0 && currentBuildStep.scaffolded_hints?.[hintLevel - 1] && (
                <motion.div
                  className="p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/30"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <span className="text-xs font-mono text-yellow-400 uppercase">
                    Hint Level {hintLevel}
                  </span>
                  <p className="text-sm text-text-primary mt-1">
                    {currentBuildStep.scaffolded_hints[hintLevel - 1].text}
                  </p>
                </motion.div>
              )}

              {/* Debug: show buggy code as read-only */}
              {currentBuildStep.is_debug && currentBuildStep.buggy_code && (
                <div className="rounded-xl border border-red-500/20 bg-red-500/5 overflow-hidden mb-4">
                  <div className="flex items-center justify-between px-4 py-2 border-b border-red-500/10 bg-red-500/5">
                    <span className="text-xs font-mono text-red-400">Buggy code — do not edit</span>
                  </div>
                  <pre className="p-4 text-sm font-mono text-red-200 whitespace-pre-wrap overflow-x-auto">
                    {currentBuildStep.buggy_code}
                  </pre>
                </div>
              )}

              {/* Code Editor */}
              <div className="rounded-2xl border border-brand-primary/10 overflow-hidden bg-surface-card/95">
                <div className="flex items-center justify-between px-4 py-2 border-b border-brand-primary/10 bg-surface-base/50">
                  <span className="text-xs font-mono text-brand-secondary">Python</span>
                  <div className="flex gap-2">
                    <button
                      onClick={handleRunExplore}
                      disabled={running}
                      className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-mono text-brand-secondary hover:bg-surface-base/50 transition-colors"
                    >
                      {running ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />}
                      Run
                    </button>
                    <button
                      onClick={() => {
                        if (currentBuildStep?.starter_code) setCode(currentBuildStep.starter_code);
                        else if (currentBuildStep?.code) setCode(currentBuildStep.code);
                        setOutput("");
                        setError("");
                        setBuildResult(null);
                      }}
                      className="px-3 py-1 rounded-lg text-xs font-mono text-brand-secondary hover:bg-surface-base/50 transition-colors"
                    >
                      <RotateCcw size={12} />
                    </button>
                  </div>
                </div>
                <div className="h-52 sm:h-64">
                  <Editor
                    height="100%"
                    language="python"
                    theme="vs-dark"
                    value={code}
                    onChange={setCode}
                    options={{
                      minimap: { enabled: false },
                      fontSize: 13,
                      tabSize: 2,
                      lineNumbers: "on",
                      wordWrap: "on",
                      padding: { top: 8 },
                      bracketPairColorization: { enabled: true },
                      renderLineHighlight: "all",
                      smoothScrolling: true,
                    }}
                  />
                </div>
              </div>

              {/* Output */}
              {(output || error || buildResult) && (
                <div className="rounded-xl border border-brand-primary/10 bg-surface-base/50">
                  <div className="flex items-center gap-2 px-4 py-2 border-b border-brand-primary/5 text-xs font-mono text-brand-secondary">
                    <Terminal size={12} />
                    {error ? "Error" : "Output"}
                  </div>
                  {error ? (
                    <pre className="p-3 text-sm font-mono text-brand-coral whitespace-pre-wrap">
                      {error}
                    </pre>
                  ) : output ? (
                    <pre className="p-3 text-sm font-mono text-brand-secondary whitespace-pre-wrap">
                      {output}
                    </pre>
                  ) : buildResult ? (
                    <BuildResultsView result={buildResult} />
                  ) : null}
                </div>
              )}

              {/* Submit Button */}
              <div className="flex justify-between items-center">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleSubmitBuild}
                  disabled={running || (attempts[activeBuildStep] || 0) >= (currentBuildStep.max_attempts || 3)}
                  className="px-6 py-3 rounded-xl bg-green-500/20 text-green-400 font-bold border border-green-500/30 hover:bg-green-500/30 transition-colors flex items-center gap-2"
                >
                  {running ? <Loader2 size={16} className="animate-spin" /> : <Zap size={16} />}
                  {(attempts[activeBuildStep] || 0) >= (currentBuildStep.max_attempts || 3) ? "Max Attempts Reached" : "Submit Solution"}
                </motion.button>

                {buildResult?.all_passed && (
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => {
                      if (activeBuildStep < totalBuildSteps - 1) {
                        setActiveBuildStep((s) => s + 1);
                      } else {
                        setPhase("break");
                      }
                    }}
                    className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold flex items-center gap-2"
                  >
                    {activeBuildStep < totalBuildSteps - 1 ? "Next Exercise" : "Break the Code"}
                    <ChevronRight size={16} />
                  </motion.button>
                )}
              </div>

              {/* Repair Steps */}
              {showRepair && currentBuildStep.repair_steps && currentBuildStep.repair_steps.length > 0 && (
                <motion.div
                  className="mt-4 p-4 rounded-xl bg-orange-500/10 border border-orange-500/30"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <h3 className="text-sm font-bold text-orange-400 mb-2">🔧 Quick Repair</h3>
                  <div className="space-y-2">
                    {currentBuildStep.repair_steps.map((repair, i) => (
                      <div key={i} className="p-3 rounded-lg bg-surface-base/50">
                        {repair.title && <p className="text-sm font-bold text-text-primary mb-1">{repair.title}</p>}
                        <p className="text-sm text-text-secondary">{repair.content}</p>
                        {repair.hint && <p className="text-xs text-brand-sky mt-1">💡 {repair.hint}</p>}
                      </div>
                    ))}
                  </div>
                  <p className="text-xs text-text-secondary mt-2">
                    Attempts: {attempts[activeBuildStep] || 0} / {currentBuildStep.max_attempts || 3}
                  </p>
                </motion.div>
              )}
            </div>
          </motion.div>
        )}

        {/* BREAK PHASE */}
        {phase === "break" && (
          <motion.div
            key="break"
            className="max-w-3xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <h2 className="text-xl font-bold text-text-primary mb-6">Break It</h2>
            <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-6 mb-6">
              <p className="text-sm text-text-secondary mb-4">What happens when this code runs?</p>
              <pre className="bg-surface-base/50 rounded-lg p-4 text-sm font-mono mb-4 overflow-x-auto whitespace-pre-wrap">
                {currentBuildStep?.buggy_code || "// broken code will appear here"}
              </pre>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-text-primary mb-1">Your prediction:</label>
                <input
                  type="text"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-brand-primary/10 bg-surface-base text-text-primary focus:outline-none focus:ring-2 focus:ring-brand-sky/40"
                  placeholder="e.g. TypeError, infinite loop, wrong output..."
                  disabled={running}
                />
              </div>
            </div>
            <div className="flex justify-between">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("build")}
                className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/10 text-sm font-medium"
              >
                <ChevronLeft size={16} /> Back
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("debug")}
                className="px-6 py-3 rounded-xl bg-red-500/20 text-red-400 font-bold border border-red-500/30 hover:bg-red-500/30 transition-colors"
              >
                Continue to Debug <ChevronRight size={16} />
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* DEBUG PHASE */}
        {phase === "debug" && (
          <motion.div
            key="debug"
            className="max-w-5xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <div className="mb-6">
              <h2 className="text-xl font-bold text-text-primary">Debug</h2>
              <p className="text-sm text-text-secondary mt-2">Fix the broken code below.</p>
            </div>
            {currentBuildStep?.buggy_code && (
              <div className="rounded-xl border border-red-500/20 bg-red-500/5 overflow-hidden mb-4">
                <div className="flex items-center justify-between px-4 py-2 border-b border-red-500/10 bg-red-500/5">
                  <span className="text-xs font-mono text-red-400">Buggy code — do not edit</span>
                </div>
                <pre className="p-4 text-sm font-mono text-red-200 whitespace-pre-wrap overflow-x-auto">
                  {currentBuildStep.buggy_code}
                </pre>
              </div>
            )}
            <div className="rounded-2xl border border-brand-primary/10 overflow-hidden bg-surface-card/95 mb-6">
              <div className="flex items-center justify-between px-4 py-2 border-b border-brand-primary/10 bg-surface-base/50">
                <span className="text-xs font-mono text-brand-secondary">Python</span>
              </div>
              <div className="h-64 sm:h-80">
                <Editor
                  height="100%"
                  language="python"
                  theme="vs-dark"
                  value={code}
                  onChange={setCode}
                  options={{
                    minimap: { enabled: false },
                    fontSize: 13,
                    tabSize: 2,
                    lineNumbers: "on",
                    wordWrap: "on",
                    padding: { top: 8 },
                  }}
                />
              </div>
            </div>
            <div className="flex justify-between">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("break")}
                className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/10 text-sm font-medium"
              >
                <ChevronLeft size={16} /> Back
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("retrieve")}
                className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold"
              >
                Continue to Retrieve <ChevronRight size={16} />
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* RETRIEVE PHASE */}
        {phase === "retrieve" && (
          <motion.div
            key="retrieve"
            className="max-w-3xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <h2 className="text-xl font-bold text-text-primary mb-6">Recall</h2>
            <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-6 mb-6">
              <p className="text-sm text-text-secondary mb-4">Without looking at your notes, write what you remember.</p>
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                rows={6}
                className="w-full px-4 py-3 rounded-xl border border-brand-primary/10 bg-surface-base text-text-primary focus:outline-none focus:ring-2 focus:ring-brand-sky/40 resize-none"
                placeholder="Write what you remember..."
                disabled={running}
              />
            </div>
            <div className="flex justify-between">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("debug")}
                className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/10 text-sm font-medium"
              >
                <ChevronLeft size={16} /> Back
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("transfer")}
                className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold"
              >
                Continue to Transfer <ChevronRight size={16} />
              </motion.button>
            </div>
          </motion.div>
        )}

        {/* TRANSFER CHALLENGE PHASE */}
        {phase === "transfer" && (
          <motion.div
            key="transfer"
            className="max-w-5xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <div className="mb-6">
              <h2 className="text-xl font-bold text-text-primary">{lesson.transfer_challenge.title}</h2>
              <p className="text-sm text-text-secondary mt-2">
                {lesson.transfer_challenge.description_full || lesson.transfer_challenge.description}
              </p>
              {lesson.transfer_challenge.signature && (
                <pre className="mt-3 text-xs font-mono text-text-secondary bg-surface-base/30 rounded px-3 py-2">
                  {lesson.transfer_challenge.signature}
                </pre>
              )}
            </div>

            <div className="rounded-2xl border border-brand-primary/10 overflow-hidden bg-surface-card/95 mb-6">
              <div className="flex items-center justify-between px-4 py-2 border-b border-brand-primary/10 bg-surface-base/50">
                <span className="text-xs font-mono text-brand-secondary">Python</span>
              </div>
              <div className="h-64 sm:h-80">
                <Editor
                  height="100%"
                  language="python"
                  theme="vs-dark"
                  value={code}
                  onChange={(val) => setCode(val || "")}
                  options={{
                    minimap: { enabled: false },
                    fontSize: 13,
                    tabSize: 2,
                    lineNumbers: "on",
                    wordWrap: "on",
                    padding: { top: 8 },
                  }}
                />
              </div>
            </div>

            {/* Hints for transfer */}
            {lesson.transfer_challenge.scaffolded_hints && (
              <div className="mb-4 space-y-2">
                {lesson.transfer_challenge.scaffolded_hints.slice(0, hintLevel + 1).map((h, i) => (
                  <div key={i} className="p-3 rounded-lg bg-yellow-500/10 border border-yellow-500/30">
                    <span className="text-xs font-mono text-yellow-400">Hint {i + 1}</span>
                    <p className="text-sm text-text-primary mt-1">{h.text}</p>
                  </div>
                ))}
                <button
                  onClick={() => setHintLevel(hintLevel + 1)}
                  disabled={hintLevel >= (lesson.transfer_challenge.scaffolded_hints?.length || 0)}
                  className="text-xs text-brand-sky hover:text-brand-sky/80 font-medium flex items-center gap-1"
                >
                  <Lightbulb size={12} /> Show Hint
                </button>
              </div>
            )}

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={async () => {
                setRunning(true);
                setBuildResult(null);
                setShowTransferRepair(false);
                try {
                  const result: BuildResult = await api.lesson.submitTransfer(lessonSlug, {
                    code,
                    function_name: lesson.transfer_challenge.function_name || "",
                    language: "python",
                  });
                  setBuildResult(result);

                  const stepAttempts = (transferAttempts[0] || 0) + 1;
                  setTransferAttempts((prev) => ({ ...prev, [0]: stepAttempts }));

                  if (!result.all_passed && stepAttempts < (lesson.transfer_challenge.max_attempts || 3)) {
                    setShowTransferRepair(true);
                  }
                } catch (err: any) {
                  setError(err.message || "Submission failed");
                } finally {
                  setRunning(false);
                }
              }}
              disabled={running || !code || (transferAttempts[0] || 0) >= (lesson.transfer_challenge.max_attempts || 3)}
              className="px-6 py-3 rounded-xl bg-purple-500/20 text-purple-400 font-bold border border-purple-500/30 hover:bg-purple-500/30 transition-colors flex items-center gap-2"
            >
              {running ? <Loader2 size={16} className="animate-spin" /> : <Zap size={16} />}
              {(transferAttempts[0] || 0) >= (lesson.transfer_challenge.max_attempts || 3) ? "Max Attempts Reached" : "Submit Transfer Challenge"}
            </motion.button>

            {buildResult && (
              <BuildResultsView result={buildResult} />
            )}

            {/* Transfer Repair Steps */}
            {showTransferRepair && lesson.transfer_challenge.repair_steps && lesson.transfer_challenge.repair_steps.length > 0 && (
              <motion.div
                className="mt-4 p-4 rounded-xl bg-orange-500/10 border border-orange-500/30"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <h3 className="text-sm font-bold text-orange-400 mb-2">🔧 Quick Repair</h3>
                <div className="space-y-2">
                  {lesson.transfer_challenge.repair_steps.map((repair, i) => (
                    <div key={i} className="p-3 rounded-lg bg-surface-base/50">
                      {repair.title && <p className="text-sm font-bold text-text-primary mb-1">{repair.title}</p>}
                      <p className="text-sm text-text-secondary">{repair.content}</p>
                      {repair.hint && <p className="text-xs text-brand-sky mt-1">💡 {repair.hint}</p>}
                    </div>
                  ))}
                </div>
                <p className="text-xs text-text-secondary mt-2">
                  Attempts: {transferAttempts[0] || 0} / {lesson.transfer_challenge.max_attempts || 3}
                </p>
              </motion.div>
            )}
          </motion.div>
            <div className="flex justify-end">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("mastery")}
                className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold"
              >
                Continue to Mastery <ChevronRight size={16} />
              </motion.button>
            </div>
        )}

        {/* MASTERY PHASE */}
        {phase === "mastery" && (
          <motion.div
            key="mastery"
            className="max-w-3xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h2 className="text-xl font-bold text-text-primary mb-6">Mastery</h2>
             <p className="text-sm text-text-secondary">Consolidate your understanding and solidify your mastery of the concept.</p>
             <div className="flex justify-end mt-6">
               <motion.button
                 whileHover={{ scale: 1.05 }}
                 whileTap={{ scale: 0.95 }}
                 onClick={() => setPhase("assess")}
                 className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold"
               >
                 Continue to Assess <ChevronRight size={16} />
               </motion.button>
             </div>
           </motion.div>
        )}

        {/* ASSESSMENT PHASE */}
        {phase === "assess" && (
          <motion.div
            key="assess"
            className="max-w-3xl mx-auto p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
          >
            <div className="mb-6 flex items-center justify-between">
              <h2 className="text-xl font-bold text-text-primary">{lesson.assessment.title}</h2>
              <span className="px-3 py-1 rounded-full bg-surface-card/60 text-xs font-mono text-text-secondary">
                Pass: {lesson.assessment.mastery_threshold}%
              </span>
            </div>

            <div className="space-y-6">
              {lesson.assessment.questions.map((q, i) => (
                <AssessmentQuestion
                  key={i}
                  question={q}
                  index={i}
                  answer={assessmentAnswers[`q${i}`] || ""}
                  onChange={(val) => setAssessmentAnswers((prev) => ({ ...prev, [`q${i}`]: val }))}
                  result={assessmentResult?.results?.find((r) => r.index === i)}
                  reduced={reduced}
                />
              ))}
            </div>

            <div className="mt-8 flex justify-between">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setPhase("build")}
                className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/10 text-sm font-medium"
              >
                <ChevronLeft size={16} /> Back
              </motion.button>

              {assessmentResult ? (
                assessmentScore !== null && assessmentScore >= lesson.assessment.mastery_threshold ? (
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleComplete}
                    className="px-6 py-3 rounded-xl bg-green-500/20 text-green-400 font-bold border border-green-500/30 hover:bg-green-500/30 transition-colors flex items-center gap-2"
                  >
                    <Trophy size={16} />
                    Claim Rewards
                  </motion.button>
                ) : (
                  <div className="flex gap-2">
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => {
                        setAssessmentResult(null);
                        setAssessmentScore(null);
                        setAssessmentAnswers({});
                      }}
                      className="px-6 py-3 rounded-xl bg-orange-500/20 text-orange-400 font-bold border border-orange-500/30 hover:bg-orange-500/30 transition-colors flex items-center gap-2"
                    >
                      <RotateCcw size={16} />
                      Retry Assessment
                    </motion.button>
                    <span className="px-3 py-3 text-xs text-text-secondary">
                      Need {lesson.assessment.mastery_threshold}% to pass (got {assessmentScore}%)
                    </span>
                  </div>
                )
              ) : (
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleAssessSubmit}
                  className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold"
                >
                  Submit Assessment
                </motion.button>
              )}
            </div>
          </motion.div>
        )}

        {/* COMPLETE PHASE */}
        {phase === "complete" && assessmentScore !== null && (
          <motion.div
            key="complete"
            className="min-h-screen flex flex-col items-center justify-center p-6"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div
              className="max-w-2xl mx-auto p-8 rounded-3xl text-center"
              style={{
                background: `linear-gradient(135deg, ${candyGradient("gold" as CandyColor)}, rgba(255,215,0,0.05))`,
              }}
            >
              <div className="text-6xl mb-4">🏆</div>
              <h2 className="text-3xl font-bold text-text-primary mb-2">Lesson Complete!</h2>

              <div className="flex items-center justify-center gap-4 my-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-400">{assessmentScore}%</div>
                  <div className="text-xs text-text-secondary">Final Score</div>
                </div>
                <div className="w-px h-12 bg-brand-primary/20"></div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-brand-sky">+{lesson.xp_reward}</div>
                  <div className="text-xs text-text-secondary">Diamonds Earned</div>
                </div>
              </div>

              {completionData && (
                <div className="bg-surface-base/30 rounded-xl p-4 text-left space-y-2 mb-6">
                  <p className="text-xs text-text-secondary">Rewards claimed:</p>
                  <ul className="text-sm space-y-1">
                    <li>✅ +{completionData.xp_gained || 0} Diamonds</li>
                    {completionData.srs_enrolled && <li>📚 Concept enrolled in Spaced Repetition</li>}
                    {completionData.lesson_completed && <li>🏆 Mastery badge unlocked: first_variables</li>}
                  </ul>
                </div>
              )}

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate("/journey")}
                className="px-6 py-3 rounded-xl bg-brand-sky text-white font-bold"
              >
                Continue Learning
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function DiscoveryStepView({ step, onInsight, codeState, reduced }: {
  step: LessonStep;
  onInsight: () => void;
  codeState: {
    code: string;
    setCode: (v: string) => void;
    output: string;
    setOutput: (v: string) => void;
    error: string;
    setError: (v: string) => void;
    running: boolean;
    setRunning: (v: boolean) => void;
  };
  reduced: boolean;
}) {
  const { code, setCode, output, setOutput, error, setError, running, setRunning } = codeState;
  const [selectedValue, setSelectedValue] = useState<string | null>(null);
  const [checked, setChecked] = useState(false);
  const isCorrect = checked && step.answer ? selectedValue === step.answer : false;

  return (
    <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-6 mb-6">
      <h3 className="font-bold text-text-primary mb-3">{step.title}</h3>
      <p className="text-sm text-text-secondary mb-4 leading-relaxed">{step.content}</p>

      {step.simulation?.initial_state && (
        <pre className="text-xs font-mono bg-surface-base/30 rounded-lg p-3 mb-3 whitespace-pre-wrap">
          {step.simulation.initial_state}
        </pre>
      )}

      {step.narration && (
        <p className="text-sm italic text-text-secondary/70 mb-3">"{step.narration}"</p>
      )}

      {step.code && (
        <div className="rounded-xl border border-brand-primary/10 overflow-hidden mb-4">
          <div className="h-36 sm:h-44">
            <Editor
              height="100%"
              language="python"
              theme="vs-dark"
              value={code}
              onChange={setCode}
              options={{
                minimap: { enabled: false },
                fontSize: 13,
                tabSize: 2,
                readOnly: step.type === "predict",
              }}
            />
          </div>
        </div>
      )}

      {step.interaction?.type === "reveal_value" && (
        <button
          onClick={onInsight}
          className="px-4 py-2 rounded-xl bg-brand-sky/10 text-brand-sky text-sm font-medium hover:bg-brand-sky/20 transition-colors"
        >
          {step.interaction.prompt}
        </button>
      )}

      {step.interaction?.type === "select-value" && step.values && (
        <div className="space-y-2">
          <p className="text-sm font-medium text-text-primary mb-2">{step.interaction.prompt || step.prompt || "Choose the correct answer:"}</p>
          <div className="grid gap-2 sm:grid-cols-2">
            {(step.values as unknown[]).map((v, i) => {
              const valueStr = String(v);
              const isSelected = selectedValue === valueStr;
              const isCorrectAnswer = step.answer ? valueStr === step.answer : false;
              return (
                <button
                  key={i}
                  onClick={() => { if (!checked) { setSelectedValue(valueStr); } }}
                  disabled={checked}
                  className={`px-4 py-3 rounded-xl border text-sm font-medium transition-all min-h-[44px] ${
                    checked && isCorrectAnswer
                      ? "bg-green-500/10 border-green-500/30 text-green-400"
                      : checked && isSelected && !isCorrectAnswer
                        ? "bg-red-500/10 border-red-500/30 text-red-400"
                        : isSelected
                          ? "bg-brand-sky/10 border-brand-sky/30 text-brand-sky"
                          : "bg-surface-base border-brand-primary/10 hover:border-brand-primary/20 text-text-secondary"
                  }`}
                >
                  {valueStr}
                </button>
              );
            })}
          </div>
          {checked && step.answer && (
            <div className={`mt-3 p-3 rounded-lg border ${isCorrect ? "bg-green-500/10 border-green-500/30" : "bg-red-500/10 border-red-500/30"}`}>
              <p className={`text-sm font-medium ${isCorrect ? "text-green-400" : "text-red-400"}`}>
                {isCorrect ? "Correct!" : `Not quite. Expected: ${step.answer}`}
              </p>
              {step.explanation && <p className="text-xs text-text-secondary mt-1">{step.explanation}</p>}
            </div>
          )}
          {!checked && selectedValue && (
            <button
              onClick={() => setChecked(true)}
              className="mt-2 px-4 py-2 rounded-xl bg-brand-sky text-white text-sm font-medium hover:bg-brand-sky/90 transition-colors"
            >
              Check Answer
            </button>
          )}
        </div>
      )}

      {step.hint && (
        <div className="mt-3 p-3 rounded-lg bg-blue-500/10 border border-blue-500/30">
          <Lightbulb size={14} className="inline text-blue-400 mr-2" />
          <span className="text-sm text-blue-300">{step.hint}</span>
        </div>
      )}

      {step.inputs_to_try && (
        <div className="mt-3 space-y-1">
          <p className="text-xs font-mono text-text-secondary uppercase">Try these inputs:</p>
          {step.inputs_to_try.map((inp, i) => (
            <span key={i} className="inline-block px-2 py-1 mr-1 text-xs bg-surface-base/30 rounded">
              {inp}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function BuildResultsView({ result }: { result: BuildResult }) {
  const { passed_count, total_count, all_passed, score, results, hidden_pass_rate } = result;
  const passedPercentage = score || (passed_count / total_count) * 100;

  return (
    <div className="p-4">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {all_passed ? (
            <CheckCircle2 className="text-green-400 w-5 h-5" />
          ) : (
            <XCircle className="text-red-400 w-5 h-5" />
          )}
          <span className="font-bold">
            {passed_count}/{total_count} test cases passed
          </span>
        </div>
        <span className="text-sm font-mono text-text-secondary">{passedPercentage}%</span>
      </div>

      <div className="max-h-40 overflow-y-auto space-y-1 text-xs">
        {results.map((r) => (
          <div
            key={r.test_case_index}
            className={`flex items-center gap-2 p-2 rounded ${
              r.passed
                ? "bg-green-500/10 border border-green-500/20"
                : "bg-red-500/10 border border-red-500/20"
            }`}
          >
            {r.passed ? (
              <CheckCircle2 size={12} className="text-green-400" />
            ) : (
              <XCircle size={12} className="text-red-400" />
            )}
            <span>
              Test {r.test_case_index}: {"Expected " + (r.expected || "")} → {"Got " + (r.actual || "")}
            </span>
          </div>
        ))}
      </div>

      {hidden_pass_rate !== undefined && (
        <div className="mt-3 text-xs text-text-secondary">
          Hidden tests: {hidden_pass_rate}% pass rate
        </div>
      )}
    </div>
  );
}

function AssessmentQuestion({ question, index, answer, onChange, result, reduced }: {
  question: LessonStep;
  index: number;
  answer: string;
  onChange: (val: string) => void;
  result?: { correct: boolean; explanation: string } | null;
  reduced: boolean;
}) {
  if (question.type === "code_tracing") {
    return (
      <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-6">
        <p className="text-sm text-text-secondary mb-3">Trace this code and predict the final variable values:</p>
        <pre className="bg-surface-base/30 rounded-lg p-3 text-sm font-mono mb-3">
          {question.code}
        </pre>
        <input
          type="text"
          value={answer}
          onChange={(e) => onChange(e.target.value)}
          placeholder="e.g. x=-5, y=5, z=10"
          className="w-full px-3 py-2 rounded-lg bg-surface-base/50 border border-brand-primary/10 text-sm font-mono text-text-primary focus:outline-none focus:border-brand-sky/30"
        />
        {result && (
          <div className={`mt-3 p-3 rounded-lg ${result.correct ? "bg-green-500/10" : "bg-red-500/10"}`}>
            <p className="text-sm">{result.explanation}</p>
          </div>
        )}
      </div>
    );
  }

  if (question.type === "concept") {
    return (
      <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-6">
        <p className="text-sm text-text-secondary mb-3">{question.question}</p>
        <textarea
          value={answer}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Type your answer..."
          rows={3}
          className="w-full px-3 py-2 rounded-lg bg-surface-base/50 border border-brand-primary/10 text-sm text-text-primary focus:outline-none focus:border-brand-sky/30 resize-none"
        />
        {result && (
          <div className={`mt-3 p-3 rounded-lg ${result.correct ? "bg-green-500/10" : "bg-red-500/10"}`}>
            <p className="text-sm">{result.explanation}</p>
          </div>
        )}
      </div>
    );
  }

  if (question.type === "debug") {
    return (
      <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-6">
        <p className="text-sm text-text-secondary mb-3">{question.question}</p>
        <pre className="bg-surface-base/30 rounded-lg p-3 text-sm font-mono mb-3 whitespace-pre-wrap">
          {question.code}
        </pre>
        <p className="text-xs text-red-400 mb-2">Error: {question.error}</p>
        <input
          type="text"
          value={answer}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Fixed line of code"
          className="w-full px-3 py-2 rounded-lg bg-surface-base/50 border border-brand-primary/10 text-sm font-mono text-text-primary focus:outline-none focus:border-brand-sky/30"
        />
        {result && (
          <div className={`mt-3 p-3 rounded-lg ${result.correct ? "bg-green-500/10" : "bg-red-500/10"}`}>
            <p className="text-sm">{result.explanation}</p>
          </div>
        )}
      </div>
    );
  }

  return null;
}
