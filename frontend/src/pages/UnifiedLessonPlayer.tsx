// @ts-nocheck
import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, Link, useNavigate, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  XCircle,
  Lightbulb,
  BookOpen,
  Trophy,
  Loader2,
  ChevronRight,
  Timer,
  Sparkles,
  Target,
  Zap,
  Shield,
  RefreshCw,
  Compass,
} from "lucide-react";
import { lessonApi } from "../services/api/lesson";
import { missionApi } from "../services/api/missions";
import { BountyCodeLoader } from "../components/brand/BountyCodeBrandMotion";

const STEP_ICONS = {
  discover: <Compass size={18} />,
  understand: <BookOpen size={18} />,
  manipulate: <Zap size={18} />,
  predict: <Target size={18} />,
  build: <Sparkles size={18} />,
  break_step: <XCircle size={18} />,
  debug: <RefreshCw size={18} />,
  retrieval: <Shield size={18} />,
  transfer: <Trophy size={18} />,
};

const STEP_LABELS = {
  discover: "Discover",
  understand: "Understand",
  manipulate: "Manipulate",
  predict: "Predict",
  build: "Build",
  break_step: "Break",
  debug: "Debug",
  retrieval: "Retrieve",
  transfer: "Transfer",
};

type Domain = "coding" | "behavioral" | "system_design" | "aptitude";

type StepContent = {
  step_index: number;
  step_name: string;
  domain: Domain;
  content: Record<string, any>;
  interaction_kind: string;
  mastery_threshold: number;
};

type SessionState = {
  session_id: string;
  domain: Domain;
  current_step: number;
  total_steps: number;
  step_results: Array<{
    step_index: number;
    step_name: string;
    passed: boolean;
    score: number;
    message: string;
    evidence: Record<string, any>;
    feedback: Record<string, any>;
    time_spent_seconds: number;
  }>;
  reteach_pending: Record<string, any> | null;
  mastery_unlocked: boolean;
  completed: boolean;
};

type MissionData = {
  id: string;
  title: string;
  briefing: string;
  why?: string;
  skillId: string;
  estimatedMinutes: number;
  stages: Array<{
    kind: string;
    title?: string;
    subtitle?: string;
    interaction?: Record<string, any>;
    mcqs?: Array<{
      id: string;
      q: string;
      code?: string;
      options: string[];
      correct: number;
      explain: string;
      codeIfMissed: string;
    }>;
    sequence?: Array<{ level: string; items: Array<{ label: string; to: string }> }>;
    judgeTo?: string;
    judgeLabel?: string;
  }>;
};

export default function UnifiedLessonPlayer() {
  const { domain: domainParam } = useParams<{ domain: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const legacyLessonSlug = searchParams.get("lesson") || searchParams.get("legacy") || "";

  const [domain, setDomain] = useState<Domain>("coding");
  const [session, setSession] = useState<SessionState | null>(null);
  const [currentStep, setCurrentStep] = useState<StepContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [answerResult, setAnswerResult] = useState<{
    passed: boolean;
    score: number;
    message: string;
    diagnosis: Record<string, any> | null;
    reteach_required: boolean;
    mastery_unlocked: boolean;
    reward: Record<string, any>;
    next_step: Record<string, any> | null;
  } | null>(null);
  const [hint, setHint] = useState<string>("");
  const [showHint, setShowHint] = useState(false);
  const [mission, setMission] = useState<MissionData | null>(null);
  const [diamondsEarned, setDiamondsEarned] = useState(0);
  const [mistakeCount, setMistakeCount] = useState(0);
  const [startTime] = useState(Date.now());

  const [codeAnswer, setCodeAnswer] = useState("");
  const [textAnswer, setTextAnswer] = useState("");
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [selectedComponent, setSelectedComponent] = useState<string | null>(null);
  const [selectedIssue, setSelectedIssue] = useState<string | null>(null);
  const [selectedFailure, setSelectedFailure] = useState<string | null>(null);
  const [fixesApplied, setFixesApplied] = useState<string[]>([]);
  const [matches, setMatches] = useState<Record<string, string>>({});
  const [improvedAnswer, setImprovedAnswer] = useState("");
  const [diagramDescription, setDiagramDescription] = useState("");

  const sessionRef = useRef<string | null>(null);

  // Initialize domain from URL param
  useEffect(() => {
    const validDomains: Domain[] = ["coding", "behavioral", "system_design", "aptitude"];
    const initialDomain = domainParam && validDomains.includes(domainParam as Domain)
      ? (domainParam as Domain)
      : "coding";
    setDomain(initialDomain);
  }, [domainParam]);

  // Load mission metadata only when we don't have a direct lesson slug
  useEffect(() => {
    if (legacyLessonSlug) {
      setMission(null);
      return;
    }
    const missionMap: Record<string, string> = {
      coding: "trace_variables",
      behavioral: "trace_variables",
      system_design: "trace_variables",
      aptitude: "percentages",
    };
    const missionId = missionMap[domain] || "trace_variables";
    try {
      import("../data/missions/patterns").then((module) => {
        const missionData = module.MISSIONS[missionId];
        if (missionData) {
          setMission(missionData as MissionData);
        }
      }).catch(() => {
        // Mission data not available, continue without it
      });
    } catch (e) {
      // Ignore mission loading errors
    }
  }, [domain, legacyLessonSlug]);

  // Start lesson session
  const startLesson = useCallback(async () => {
    setLoading(true);
    setAnswerResult(null);
    setShowHint(false);
    setHint("");
    setCodeAnswer("");
    setTextAnswer("");
    setSelectedOption(null);
    setSelectedComponent(null);
    setSelectedIssue(null);
    setSelectedFailure(null);
    setFixesApplied([]);
    setMatches({});
    setImprovedAnswer("");
    setDiagramDescription("");

    try {
      const params: Record<string, any> = {
        domain,
        mastery_threshold: 80,
      };
      if (legacyLessonSlug) {
        params.topic = legacyLessonSlug;
        params.difficulty = "medium";
      } else {
        if (domain === "coding") {
          params.world_id = "foundations";
          params.level_id = "level-1";
        }
        if (domain === "behavioral" || domain === "system_design") {
          params.company = "general";
          params.role = "sde";
        }
        if (domain === "aptitude") {
          params.topic = "percentages";
          params.difficulty = "medium";
        }
      }

      const res = await lessonApi.startLessonPlayer(params);
      if (res?.session_id) {
        setSession(res as SessionState);
        setCurrentStep(res.step as StepContent);
        sessionRef.current = res.session_id;
      }
    } catch (e) {
      console.error("Failed to start lesson:", e);
    } finally {
      setLoading(false);
    }
  }, [domain, legacyLessonSlug]);

  useEffect(() => {
    if (domain) {
      startLesson();
    }
  }, [domain, legacyLessonSlug, startLesson]);

  const submitAnswer = useCallback(async () => {
    if (!session || !currentStep || submitting) return;
    setSubmitting(true);
    setAnswerResult(null);
    setShowHint(false);

    try {
      const payload: Record<string, any> = {
        step_index: currentStep.step_index,
        time_spent_seconds: Math.round((Date.now() - startTime) / 1000),
      };

      const stepName = currentStep.step_name;
      if (stepName === "discover" || stepName === "understand" || stepName === "retrieval") {
        payload.answer = textAnswer || "Read the content.";
      } else if (stepName === "manipulate") {
        if (selectedComponent) payload.selected_component = selectedComponent;
        else if (textAnswer) payload.answer = textAnswer;
        else payload.answer = "manipulated";
      } else if (stepName === "predict") {
        if (selectedOption) payload.selected_option = selectedOption;
        else payload.answer = textAnswer || codeAnswer;
      } else if (stepName === "build") {
        payload.code = codeAnswer;
        payload.language = "python";
      } else if (stepName === "break_step") {
        if (selectedIssue) payload.selected_issue = selectedIssue;
        else payload.answer = textAnswer || codeAnswer;
      } else if (stepName === "debug") {
        if (improvedAnswer) payload.improved_answer = improvedAnswer;
        else payload.code = codeAnswer;
        payload.language = "python";
      } else if (stepName === "transfer") {
        if (domain === "system_design") {
          payload.answer = textAnswer;
          payload.diagram_description = diagramDescription;
          payload.question = currentStep.content?.question || "";
        } else {
          payload.code = codeAnswer;
          payload.language = "python";
          if (improvedAnswer) payload.improved_answer = improvedAnswer;
        }
      }

      const res = await lessonApi.submitLessonPlayer(session.session_id, payload);
      if (res) {
        setAnswerResult({
          passed: res.passed || false,
          score: res.score || 0,
          message: res.message || "",
          diagnosis: res.diagnosis || null,
          reteach_required: res.reteach_required || false,
          mastery_unlocked: res.mastery_unlocked || false,
          reward: res.reward || {},
          next_step: res.next_step || null,
        });

        if (res.passed) {
          if (res.mastery_unlocked) {
            setDiamondsEarned((prev) => prev + (res.reward?.diamonds || 0));
          }
        } else {
          setMistakeCount((prev) => prev + 1);
        }

        // Advance to next step if available
        if (res.next_step && !res.reteach_required) {
          setCurrentStep(res.next_step.step as StepContent);
        }
      }
    } catch (e) {
      console.error("Failed to submit answer:", e);
      setAnswerResult({
        passed: false,
        score: 0,
        message: "Submission failed. Please try again.",
        diagnosis: null,
        reteach_required: false,
        mastery_unlocked: false,
        reward: {},
        next_step: null,
      });
    } finally {
      setSubmitting(false);
    }
  }, [session, currentStep, submitting, domain, codeAnswer, textAnswer, selectedOption, selectedComponent, selectedIssue, selectedFailure, improvedAnswer, diagramDescription, startTime]);

  const requestHint = useCallback(async () => {
    if (!session || !currentStep) return;
    try {
      const res = await lessonApi.requestLessonPlayerHint(
        session.session_id,
        currentStep.step_index
      );
      if (res?.hint) {
        setHint(res.hint);
        setShowHint(true);
      }
    } catch (e) {
      console.error("Failed to get hint:", e);
      setHint("Review the step content and try again.");
      setShowHint(true);
    }
  }, [session, currentStep]);

  const resetForm = useCallback(() => {
    setCodeAnswer("");
    setTextAnswer("");
    setSelectedOption(null);
    setSelectedComponent(null);
    setSelectedIssue(null);
    setSelectedFailure(null);
    setFixesApplied([]);
    setMatches({});
    setImprovedAnswer("");
    setDiagramDescription("");
    setAnswerResult(null);
    setShowHint(false);
    setHint("");
  }, []);

  const advanceStep = useCallback(() => {
    if (!session || !currentStep) return;
    const nextStepIndex = currentStep.step_index + 1;
    if (nextStepIndex < (session.total_steps || 9)) {
      // The backend will return the next step in the response,
      // but if we need to manually advance, we can do so here
      resetForm();
    }
  }, [session, currentStep, resetForm]);

  const handleRetry = useCallback(() => {
    resetForm();
  }, [resetForm]);

  const handleReteach = useCallback(async () => {
    if (!session) return;
    try {
      const res = await lessonApi.getLessonPlayerReteach(session.session_id);
      if (res?.plan) {
        setHint(`Reteach: ${res.reteach_action || "Review the concept again."}`);
        setShowHint(true);
      }
    } catch (e) {
      console.error("Failed to get reteach plan:", e);
    }
  }, [session]);

  const handleComplete = useCallback(async () => {
    if (!session) return;
    try {
      await lessonApi.completeLessonPlayer(session.session_id);
      // Navigate to results or next mission
      navigate(`/missions/${domain}`);
    } catch (e) {
      console.error("Failed to complete session:", e);
    }
  }, [session, domain, navigate]);

  // Render current step content
  const renderStepContent = () => {
    if (!currentStep) return null;
    const content = currentStep.content || {};
    const stepName = currentStep.step_name;

    switch (stepName) {
      case "discover":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Explore the concept"}</h3>
              {content.question && (
                <p className="mt-2 text-sm text-text-muted">{content.question}</p>
              )}
              {content.requirements && (
                <ul className="mt-2 space-y-1">
                  {content.requirements.map((req: string, i: number) => (
                    <li key={i} className="text-sm text-text-secondary">• {req}</li>
                  ))}
                </ul>
              )}
            </div>
            <textarea
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="What do you observe? Write your thoughts..."
              className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm"
              rows={4}
            />
          </div>
        );

      case "understand":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Understand the concept"}</h3>
              {content.explanation && (
                <p className="mt-2 text-sm text-text-secondary">{content.explanation}</p>
              )}
              {content.components && (
                <div className="mt-3 space-y-2">
                  {Object.entries(content.components).map(([key, val]: [string, any]) => (
                    <div key={key} className="rounded-xl bg-white p-3">
                      <span className="font-mono text-xs font-bold text-primary">{key}</span>
                      <p className="text-sm text-text-secondary">{val.label || val.description}</p>
                    </div>
                  ))}
                </div>
              )}
              {content.dimensions && (
                <div className="mt-3 space-y-2">
                  {content.dimensions.map((dim: any, i: number) => (
                    <div key={i} className="rounded-xl bg-white p-3">
                      <span className="font-mono text-xs font-bold text-primary">{dim.name}</span>
                      <p className="text-sm text-text-secondary">{dim.description}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <textarea
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="Explain in your own words..."
              className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm"
              rows={3}
            />
          </div>
        );

      case "manipulate":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Practice the concept"}</h3>
              {content.sentences && (
                <div className="mt-3 space-y-2">
                  {content.sentences.map((sent: any, i: number) => (
                    <div key={i} className="rounded-xl bg-white p-3">
                      <p className="text-sm">{sent.text}</p>
                      <div className="mt-2 flex gap-2">
                        {["S", "T", "A", "R"].map((comp) => (
                          <button
                            key={comp}
                            onClick={() => setSelectedComponent(comp)}
                            className={`rounded-lg px-3 py-1.5 text-xs font-bold transition-colors ${
                              selectedComponent === comp
                                ? "bg-primary text-white"
                                : "bg-black/5 hover:bg-black/10"
                            }`}
                          >
                            {comp}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
              {content.components && (
                <div className="mt-3 space-y-2">
                  {content.components.map((comp: any, i: number) => (
                    <div key={i} className="rounded-xl bg-white p-3">
                      <p className="text-sm font-semibold">{comp.name}</p>
                      <p className="text-xs text-text-muted">{comp.purpose}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
            <textarea
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="Your manipulation..."
              className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm"
              rows={3}
            />
          </div>
        );

      case "predict":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Predict the outcome"}</h3>
              {content.sample_answer && (
                <pre className="mt-2 rounded-xl bg-gray-950 p-3 font-mono text-xs text-cyan-300">
                  {content.sample_answer}
                </pre>
              )}
              {content.simple_design && (
                <p className="mt-2 text-sm text-text-secondary">{content.simple_design}</p>
              )}
              {content.options && (
                <div className="mt-3 space-y-2">
                  {content.options.map((opt: any, i: number) => (
                    <button
                      key={i}
                      onClick={() => setSelectedOption(opt.id)}
                      className={`w-full rounded-xl border px-4 py-3 text-left text-sm transition-colors ${
                        selectedOption === opt.id
                          ? "border-primary bg-primary/5"
                          : "border-black/10 hover:border-black/20"
                      }`}
                    >
                      {opt.text}
                    </button>
                  ))}
                </div>
              )}
            </div>
            <textarea
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="Your prediction..."
              className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm"
              rows={2}
            />
          </div>
        );

      case "build":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Build the solution"}</h3>
              {content.guidelines && (
                <ul className="mt-2 space-y-1">
                  {content.guidelines.map((guide: string, i: number) => (
                    <li key={i} className="text-sm text-text-secondary">• {guide}</li>
                  ))}
                </ul>
              )}
              {content.components_to_include && (
                <p className="mt-2 text-xs text-text-muted">
                  Include: {content.components_to_include.join(", ")}
                </p>
              )}
            </div>
            <textarea
              value={codeAnswer}
              onChange={(e) => setCodeAnswer(e.target.value)}
              placeholder="Write your code or solution here..."
              className="w-full rounded-2xl border border-black/10 bg-gray-950 p-4 font-mono text-sm text-cyan-300"
              rows={8}
            />
          </div>
        );

      case "break_step":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Find the bug"}</h3>
              {content.sample_bad && (
                <pre className="mt-2 rounded-xl bg-red-50 p-3 font-mono text-xs text-red-700">
                  {content.sample_bad}
                </pre>
              )}
              {content.design && (
                <p className="mt-2 text-sm text-text-secondary">{content.design}</p>
              )}
              {content.broken_design && (
                <p className="mt-2 text-sm text-text-secondary">{content.broken_design}</p>
              )}
            </div>
            <textarea
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="What's wrong here? Identify the issue..."
              className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm"
              rows={3}
            />
          </div>
        );

      case "debug":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Fix the problem"}</h3>
              {content.weak_answer && (
                <div className="mt-2 rounded-xl bg-red-50 p-3">
                  <p className="text-xs font-semibold text-red-700">Weak answer:</p>
                  <p className="text-sm text-text-secondary">{content.weak_answer}</p>
                </div>
              )}
              {content.improvement_guide && (
                <ul className="mt-2 space-y-1">
                  {content.improvement_guide.map((guide: string, i: number) => (
                    <li key={i} className="text-sm text-text-secondary">• {guide}</li>
                  ))}
                </ul>
              )}
              {content.fixes_required && (
                <div className="mt-3 space-y-2">
                  {content.fixes_required.map((fix: string, i: number) => (
                    <label key={i} className="flex items-center gap-2 rounded-xl bg-white p-3">
                      <input
                        type="checkbox"
                        checked={fixesApplied.includes(fix)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setFixesApplied([...fixesApplied, fix]);
                          } else {
                            setFixesApplied(fixesApplied.filter((f) => f !== fix));
                          }
                        }}
                        className="h-4 w-4 rounded"
                      />
                      <span className="text-sm">{fix}</span>
                    </label>
                  ))}
                </div>
              )}
            </div>
            <textarea
              value={improvedAnswer || textAnswer}
              onChange={(e) => {
                setImprovedAnswer(e.target.value);
                setTextAnswer(e.target.value);
              }}
              placeholder="Write your improved answer..."
              className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm"
              rows={4}
            />
          </div>
        );

      case "retrieval":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Recall what you learned"}</h3>
              {content.answer && (
                <div className="mt-2 rounded-xl bg-blue-50 p-3">
                  <p className="text-xs font-semibold text-blue-700">Expected answer:</p>
                  <p className="text-sm text-text-secondary">{content.answer}</p>
                </div>
              )}
              {content.explanation && (
                <p className="mt-2 text-sm text-text-secondary">{content.explanation}</p>
              )}
            </div>
            <textarea
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="Recall and write the answer from memory..."
              className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm"
              rows={3}
            />
          </div>
        );

      case "transfer":
        return (
          <div className="space-y-4">
            <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
              <h3 className="font-display text-lg font-bold">{content.prompt || "Transfer your knowledge"}</h3>
              {content.guidelines && (
                <ul className="mt-2 space-y-1">
                  {content.guidelines.map((guide: string, i: number) => (
                    <li key={i} className="text-sm text-text-secondary">• {guide}</li>
                  ))}
                </ul>
              )}
              {content.requirements && (
                <ul className="mt-2 space-y-1">
                  {content.requirements.map((req: string, i: number) => (
                    <li key={i} className="text-sm text-text-secondary">• {req}</li>
                  ))}
                </ul>
              )}
              {content.components_to_consider && (
                <p className="mt-2 text-xs text-text-muted">
                  Consider: {content.components_to_consider.join(", ")}
                </p>
              )}
            </div>
            {domain === "system_design" && (
              <textarea
                value={diagramDescription}
                onChange={(e) => setDiagramDescription(e.target.value)}
                placeholder="Describe your architecture diagram..."
                className="w-full rounded-2xl border border-black/10 bg-white p-4 text-sm"
                rows={3}
              />
            )}
            <textarea
              value={codeAnswer || improvedAnswer || textAnswer}
              onChange={(e) => {
                setCodeAnswer(e.target.value);
                setImprovedAnswer(e.target.value);
                setTextAnswer(e.target.value);
              }}
              placeholder="Write your solution here..."
              className="w-full rounded-2xl border border-black/10 bg-gray-950 p-4 font-mono text-sm text-cyan-300"
              rows={8}
            />
          </div>
        );

      default:
        return (
          <div className="rounded-2xl border border-black/5 bg-surface-2 p-4">
            <p className="text-sm text-text-muted">Complete this step to continue.</p>
          </div>
        );
    }
  };

  // Show loading state
  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <BountyCodeLoader size={32} />
          <p className="mt-3 text-sm text-text-muted">Loading {domain} lesson...</p>
        </div>
      </div>
    );
  }

  // Show error state
  if (!session || !currentStep) {
    return (
      <div className="flex min-h-screen items-center justify-center px-4">
        <div className="text-center">
          <p className="font-bold text-text-primary">Failed to load lesson</p>
          <button
            onClick={startLesson}
            className="btn-primary mt-4 inline-block text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const stepProgress = ((currentStep.step_index + 1) / (session.total_steps || 9)) * 100;

  return (
    <div className="min-h-screen bg-base px-4 pb-32 pt-4 md:pb-16">
      <div className="mx-auto w-full max-w-2xl space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between gap-2">
          <Link
            to="/journey"
            className="inline-flex min-h-[44px] items-center gap-1 font-mono text-xs text-text-muted"
          >
            <ArrowLeft size={14} /> Journey
          </Link>
          <div className="flex items-center gap-3">
            <span className="font-mono text-[11px] text-text-muted">
              {STEP_LABELS[currentStep.step_name] || currentStep.step_name} · {currentStep.step_index + 1}/{session.total_steps || 9}
            </span>
            <span className="font-mono text-[11px] text-text-muted">
              💎 {diamondsEarned}
            </span>
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-2 overflow-hidden rounded-full bg-black/10" role="progressbar">
          <motion.div
            className="h-full rounded-full bg-gradient-to-r from-primary to-orange-400"
            animate={{ width: `${stepProgress}%` }}
            transition={reduced ? { duration: 0 } : { type: "spring", stiffness: 120, damping: 20 }}
          />
        </div>

        {/* Mistake counter */}
        {mistakeCount > 0 && (
          <div className="flex items-center gap-2 rounded-2xl border border-orange-200 bg-orange-50 p-3 text-sm text-orange-700">
            <Lightbulb size={16} />
            <span>{mistakeCount} mistake{mistakeCount !== 1 ? "s" : ""} — that's data, not failure.</span>
          </div>
        )}

        {/* Hint display */}
        {showHint && hint && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="rounded-2xl border border-blue-200 bg-blue-50 p-4"
          >
            <div className="flex items-start gap-2">
              <Lightbulb size={18} className="shrink-0 text-blue-600" />
              <div>
                <p className="text-sm font-semibold text-blue-900">Hint</p>
                <p className="mt-1 text-sm text-blue-700">{hint}</p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Answer result feedback */}
        {answerResult && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`rounded-2xl border p-4 ${
              answerResult.passed
                ? "border-emerald-200 bg-emerald-50"
                : "border-red-200 bg-red-50"
            }`}
          >
            <div className="flex items-start gap-2">
              {answerResult.passed ? (
                <CheckCircle2 size={18} className="shrink-0 text-emerald-600" />
              ) : (
                <XCircle size={18} className="shrink-0 text-red-600" />
              )}
              <div className="flex-1">
                <p className={`text-sm font-semibold ${answerResult.passed ? "text-emerald-900" : "text-red-900"}`}>
                  {answerResult.passed ? "Correct!" : "Not quite right"}
                </p>
                {answerResult.message && (
                  <p className="mt-1 text-sm text-text-secondary">{answerResult.message}</p>
                )}
                {answerResult.feedback && Object.keys(answerResult.feedback).length > 0 && (
                  <div className="mt-2 rounded-xl bg-white/80 p-3">
                    <pre className="text-xs text-text-muted">
                      {JSON.stringify(answerResult.feedback, null, 2)}
                    </pre>
                  </div>
                )}
                {answerResult.mastery_unlocked && (
                  <div className="mt-3 rounded-xl bg-emerald-100 p-3">
                    <p className="text-sm font-bold text-emerald-900">🎉 Mastery Unlocked!</p>
                    {answerResult.reward && Object.keys(answerResult.reward).length > 0 && (
                      <div className="mt-1 font-mono text-xs text-emerald-700">
                        {answerResult.reward.diamonds && <span>💎 +{answerResult.reward.diamonds} </span>}
                        {answerResult.reward.combo && <span>🔥 Combo x{answerResult.reward.combo} </span>}
                        {answerResult.reward.streak_multiplier && answerResult.reward.streak_multiplier > 1 && (
                          <span>⚡ x{answerResult.reward.streak_multiplier}</span>
                        )}
                      </div>
                    )}
                  </div>
                )}
                {answerResult.reteach_required && (
                  <div className="mt-3">
                    <button
                      onClick={handleReteach}
                      className="inline-flex items-center gap-2 rounded-xl bg-orange-500 px-4 py-2 text-sm font-bold text-white"
                    >
                      <RefreshCw size={14} /> Get Reteach Plan
                    </button>
                  </div>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {/* Step content */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep.step_index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.18 }}
          >
            {renderStepContent()}
          </motion.div>
        </AnimatePresence>

        {/* Action buttons */}
        <div
          className="fixed inset-x-0 bottom-0 z-40 border-t border-black/10 bg-white/95 px-4 pt-3 backdrop-blur md:static md:rounded-2xl md:border"
          style={{ paddingBottom: "max(0.75rem, env(safe-area-inset-bottom))" }}
        >
          <div className="mx-auto flex w-full max-w-2xl gap-2">
            <button
              onClick={() => setShowHint(!showHint)}
              className="inline-flex min-h-[48px] items-center justify-center gap-1 rounded-xl border border-black/10 px-4 text-sm font-semibold"
            >
              <Lightbulb size={15} /> Hint
            </button>
            <button
              onClick={resetForm}
              className="inline-flex min-h-[48px] items-center justify-center gap-1 rounded-xl border border-black/10 px-4 text-sm font-semibold"
            >
              Reset
            </button>
            {answerResult && !answerResult.passed && (
              <button
                onClick={handleRetry}
                className="inline-flex min-h-[48px] items-center justify-center gap-1 rounded-xl border border-black/10 px-4 text-sm font-semibold"
              >
                <RefreshCw size={15} /> Retry
              </button>
            )}
            <button
              onClick={submitAnswer}
              disabled={submitting || !codeAnswer && !textAnswer && !selectedOption && !selectedComponent && !improvedAnswer}
              className="inline-flex min-h-[48px] flex-[2] items-center justify-center gap-1 rounded-xl bg-[#F4532F] text-sm font-bold text-white shadow-lg shadow-orange-500/20 disabled:opacity-40"
            >
              {submitting ? <BountyCodeLoader size={18} dark /> : <CheckCircle2 size={15} />}
              {answerResult ? (answerResult.passed ? "Continue" : "Submit") : "Submit"}
            </button>
            {answerResult?.mastery_unlocked && (
              <button
                onClick={handleComplete}
                className="inline-flex min-h-[48px] items-center justify-center gap-1 rounded-xl bg-emerald-500 px-4 text-sm font-bold text-white"
              >
                <Trophy size={15} /> Finish
              </button>
            )}
          </div>
          {!answerResult && !codeAnswer && !textAnswer && !selectedOption && (
            <p className="mx-auto mt-1 w-full max-w-2xl text-center font-mono text-[11px] text-text-muted">
              Answer the question to continue.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
