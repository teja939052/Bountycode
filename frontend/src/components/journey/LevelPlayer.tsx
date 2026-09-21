import { useState, useCallback, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import {
  X,
  CheckCircle2,
  Loader2,
  Code2,
  ChevronRight,
  Zap,
  Lightbulb,
  Bug,
  Trophy,
  Brain,
  Rocket,
} from "lucide-react";
import api from "../../services/api";
import { refreshJourneyState } from "../../hooks/useJourneyState";
import { PlayerCharacter } from "./PlayerCharacter";
import analytics from "../../services/api/analytics";
import { MysteryBoxContainer } from "./MysteryBox";
import { useGamificationState } from "../../hooks/useGamificationState";
import type { JourneyLevel } from "../../hooks/useJourneyState";

const LANGUAGES = [
  { id: "python", name: "Python", icon: "🐍" },
  { id: "java", name: "Java", icon: "☕" },
  { id: "cpp", name: "C++", icon: "⚡" },
  { id: "c", name: "C", icon: "🔧" },
];

interface LevelPlayerProps {
  worldId: string;
  level: JourneyLevel;
  onClose: () => void;
  onMastered?: (diamonds: number, detail?: {
    stars?: number;
    reward?: Record<string, unknown>;
    xp_nominal?: number;
  }) => void;
  worldContent?: LevelContent | null;
}

interface LevelContent {
  discover?: {
    visual?: string;
    interaction?: string;
    prompt?: string;
    answer?: string;
    values?: unknown[];
  };
  manipulate?: {
    type?: string;
    template?: string;
    answer?: string;
    blocks?: string[];
    hint?: string;
  };
  predict?: { prompt?: string; answer?: string; explanation?: string };
  build?: {
    prompt?: string;
    starter?: string;
    placeholder?: string;
    language?: string;
  };
  break_step?: {
    prompt?: string;
    broken_code?: string;
    expected_failure?: string;
  };
  debug?: {
    prompt?: string;
    buggy_code?: string;
    fix_steps?: string[];
    answer?: string;
  };
  code?: {
    prompt?: string;
    starter?: string;
    placeholder?: string;
    language?: string;
  };
  checks?: {
    required_patterns?: string[];
    forbidden?: string[];
    hint_triggers?: string[];
  };
  hints?: Array<{
    title?: string;
    icon?: string;
    description?: string;
    hint?: string;
    mental_model?: string;
    xp_reward?: number;
    rarity?: string;
    color?: string;
  }>;
  retrieval?: { prompt?: string; answer?: string; explanation?: string };
  transfer?: { prompt?: string; answer?: string; context?: string };
  success?: {
    world_before?: string;
    world_after?: string;
    world_reaction?: string;
    reward_text?: string;
    byte_line?: string;
    diamonds?: number;
  };
  story?: { location?: string; npc?: string; line?: string };
  tutor?: { name?: string; avatar?: string; discover?: string; explain?: string };
  mental_model?: string;
}

type StepType =
  | "discover"
  | "manipulate"
  | "predict"
  | "build"
  | "break_step"
  | "debug"
  | "retrieval"
  | "transfer"
  | "mastery"
  | "success";

interface Step {
  type: StepType;
  content: LevelContent;
}

interface RunOutput {
  stdout?: string | null;
  stderr?: string | null;
  error?: string | null;
  expected?: string | null;
  error_type?: string | null;
}

interface AttemptFeedback {
  ok: boolean;
  msg: string;
  runOutput?: RunOutput | null;
}

function RunOutputPanel({ output }: { output: RunOutput }) {
  if (!output) return null;
  const stdout = (output.stdout || "").trim();
  const errs: string[] = [];
  if (output.error) errs.push(output.error);
  if (output.stderr && output.stderr !== output.stdout) errs.push(output.stderr);
  const error = errs.join("\n");
  const expected = (output.expected || "").trim();
  if (!stdout && !error && !expected) return null;
  return (
    <div className="mt-2.5 rounded-lg border border-border bg-[#0f172a] text-xs font-mono space-y-2 p-3">
      {stdout ? (
        <div>
          <div className="text-[10px] uppercase tracking-widest text-text-muted mb-0.5">Your output</div>
          <pre className="whitespace-pre-wrap break-words text-zinc-200 leading-relaxed">{stdout}</pre>
        </div>
      ) : null}
      {error ? (
        <div>
          <div className="text-[10px] uppercase tracking-widest text-red-400 mb-0.5">Error</div>
          <pre className="whitespace-pre-wrap break-words text-red-300 leading-relaxed">{error}</pre>
        </div>
      ) : null}
      {expected && expected !== stdout ? (
        <div>
          <div className="text-[10px] uppercase tracking-widest text-text-muted mb-0.5">Expected</div>
          <pre className="whitespace-pre-wrap break-words text-zinc-200 leading-relaxed">{expected}</pre>
        </div>
      ) : null}
    </div>
  );
}

const STEP_META: Record<StepType, { icon: typeof Lightbulb; label: string; color: string }> = {
  discover: { icon: Lightbulb, label: "Discover", color: "text-blue-600 bg-blue-50 border-blue-200" },
  manipulate: { icon: Code2, label: "Manipulate", color: "text-purple-600 bg-purple-50 border-purple-200" },
  predict: { icon: Brain, label: "Predict", color: "text-amber-600 bg-amber-50 border-amber-200" },
  build: { icon: Code2, label: "Build", color: "text-emerald-600 bg-emerald-50 border-emerald-200" },
  break_step: { icon: Bug, label: "Break", color: "text-red-600 bg-red-50 border-red-200" },
  debug: { icon: Bug, label: "Debug", color: "text-orange-600 bg-orange-50 border-orange-200" },
  retrieval: { icon: Brain, label: "Recall", color: "text-indigo-600 bg-indigo-50 border-indigo-200" },
  transfer: { icon: Rocket, label: "Transfer", color: "text-teal-600 bg-teal-50 border-teal-200" },
  mastery: { icon: Trophy, label: "Prove", color: "text-yellow-600 bg-yellow-50 border-yellow-200" },
  success: { icon: Trophy, label: "Victory", color: "text-emerald-600 bg-emerald-50 border-emerald-200" },
};

export function LevelPlayer({ worldId, level, onClose, onMastered, worldContent: worldContentProp }: LevelPlayerProps) {
  const { refetch: refetchGamification } = useGamificationState();
  const [steps, setSteps] = useState<Step[]>([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [code, setCode] = useState("");
  const [prediction, setPrediction] = useState("");
  const [language, setLanguage] = useState("python");
  const [feedback, setFeedback] = useState<AttemptFeedback | null>(null);
  const [busy, setBusy] = useState(false);
  const [openedBoxes, setOpenedBoxes] = useState<Set<number>>(new Set());
  const [showSuccess, setShowSuccess] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);

  const attemptsRef = useRef(0);
  const contentRef = useRef<LevelContent | null>(null);

  const currentStep = steps[currentStepIndex];
  const isLastStep = currentStepIndex === steps.length - 1;

  // Track lesson start
  useEffect(() => {
    analytics.lessonStarted(level.id, worldId);
    if (level.kind === "boss") analytics.bossStarted(level.id);
  }, [level.id, worldId, level.kind]);

  // Load world content from backend and build step sequence
  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        setLoadError(null);
        let content: LevelContent | null | undefined = null;

        if (worldContentProp && typeof worldContentProp === "object") {
          content = worldContentProp;
        } else {
          const res = await api.journey.getWorldView(worldId);
          const world = (res as Record<string, unknown>).world as Record<string, unknown> | undefined;
          if (!world?.towns || !Array.isArray(world.towns)) {
            if (!cancelled) setLoadError("World data is missing towns.");
            return;
          }
          const allLevels: unknown[] = [];
          for (const town of world.towns) {
            const t = town as Record<string, unknown>;
            if (Array.isArray(t.levels)) {
              allLevels.push(...t.levels);
            }
          }
          content = allLevels.find((l) => (l as Record<string, unknown>).id === level.id) as
            | Record<string, unknown>
            | undefined;
        }

        if (!content) {
          if (!cancelled) setLoadError("Level data not found in world content.");
          return;
        }

        contentRef.current = content as LevelContent;

        const builtSteps: Step[] = [];

        // Discover is always first
        if (content.discover || content.story || content.tutor) {
          builtSteps.push({ type: "discover", content: content as LevelContent });
        }

        // Manipulate after discover
        if (content.manipulate) {
          builtSteps.push({ type: "manipulate", content: content as LevelContent });
        }

        // Predict comes after discover/manipulate
        if (content.predict) {
          builtSteps.push({ type: "predict", content: content as LevelContent });
        }

        // Build comes next
        if (content.code || content.build) {
          builtSteps.push({ type: "build", content: content as LevelContent });
        }

        // Break step
        if (content.break_step) {
          builtSteps.push({ type: "break_step", content: content as LevelContent });
        }

        // Debug
        if (content.debug) {
          builtSteps.push({ type: "debug", content: content as LevelContent });
        }

        // Retrieval (SRS campfire)
        if (content.retrieval) {
          builtSteps.push({ type: "retrieval", content: content as LevelContent });
        }

        // Transfer
        if (content.transfer) {
          builtSteps.push({ type: "transfer", content: content as LevelContent });
        }

        // Mastery
        if (content.mastery || content.mastery_evidence) {
          builtSteps.push({ type: "mastery", content: content as LevelContent });
        }

        if (!cancelled) {
          setSteps(builtSteps);

          // Prefill code from backend content
          const codeContent = content.code || content.build || {};
          const starter = typeof codeContent.starter === "string" ? codeContent.starter : "";
          if (starter) {
            setCode(starter);
          }
          const contentLanguage = typeof codeContent.language === "string" ? codeContent.language : null;
          if (contentLanguage) {
            setLanguage(contentLanguage);
          }
        }
      } catch (e: unknown) {
        if (!cancelled) {
          setLoadError(e instanceof Error ? e.message : "Failed to load lesson content.");
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [worldId, level.id, worldContentProp]);

  const advanceStep = useCallback(() => {
    if (currentStepIndex < steps.length - 1) {
      const nextIndex = currentStepIndex + 1;
      const nextType = steps[nextIndex]?.type;
      setCurrentStepIndex(nextIndex);
      setFeedback(null);
      if (nextType === "predict" || nextType === "retrieval" || nextType === "transfer" || nextType === "mastery") {
        setCode("");
      }
      if (nextType === "break_step") {
        setCode("");
        setPrediction("");
      }
      if (nextType === "manipulate") {
        setCode("");
      }
    } else {
      setShowSuccess(true);
    }
  }, [currentStepIndex, steps]);

  const handleAttempt = useCallback(
    async (stepCode: string, stepType: string) => {
      setBusy(true);
      setFeedback(null);
      attemptsRef.current += 1;

      try {
        const res = await api.journey.attemptLevel(worldId, level.id, {
          code: stepCode,
          language,
          time_spent_seconds: 0,
          step_type: stepType,
        });

        if ((res as Record<string, unknown>).passed) {
          setFeedback({
            ok: true,
            msg: (res as Record<string, unknown>).message as string || "Correct!",
            runOutput: (res as Record<string, unknown>).run_output as RunOutput | null | undefined,
          });
          setTimeout(() => {
            advanceStep();
          }, 800);
        } else {
          const hintIndex = (res as Record<string, unknown>).hint_index as number | null | undefined;
          setFeedback({
            ok: false,
            msg: (res as Record<string, unknown>).message as string || "Not quite — try again!",
            runOutput: (res as Record<string, unknown>).run_output as RunOutput | null | undefined,
          });
          if (typeof hintIndex === "number") {
            setOpenedBoxes((prev) => new Set([...prev, hintIndex]));
          }
        }
      } catch (e: unknown) {
        setFeedback({ ok: false, msg: e instanceof Error ? e.message : "Check failed." });
      } finally {
        setBusy(false);
      }
    },
    [worldId, level.id, language, advanceStep],
  );

  const handleComplete = useCallback(async () => {
    setBusy(true);
    try {
      const res = await api.journey.completeLevel(worldId, level.id, {
        code,
        language,
        time_spent_seconds: 0,
      });
      analytics.masteryAchieved(level.id, worldId, level.diamonds);
      refreshJourneyState();

      const xpAwarded = (res as Record<string, unknown>).xp_awarded as number | undefined;
      const reward = (res as Record<string, unknown>).reward as Record<string, unknown> | undefined;
      const xpNominal = (res as Record<string, unknown>).xp_nominal as number | undefined;

      if (xpAwarded) {
        window.dispatchEvent(
          new CustomEvent("diamonds-gained", {
            detail: {
              diamonds: xpAwarded,
              level: 0,
              streak: typeof reward?.new_streak === "number" ? reward.new_streak : 0,
              badges: [] as string[],
              critical: reward?.critical_hit === true,
            },
          }),
        );
        window.dispatchEvent(
          new CustomEvent("juice:diamonds", {
            detail: {
              amount: xpAwarded,
              leveledUp: false,
              newLevel: undefined,
              coins: 0,
              stars: (res as Record<string, unknown>).stars as number | undefined,
              streak: typeof reward?.new_streak === "number" ? reward.new_streak : 0,
              combo: typeof reward?.combo === "number" ? reward.combo : undefined,
              critical: reward?.critical_hit ? 10 : 1,
              criticalBonus: 0,
              streakMultiplier: typeof reward?.streak_multiplier === "number" ? reward.streak_multiplier : 1,
              streakFrozen: false,
              freezesRemaining: 0,
              dailyGoal: undefined,
              milestone: undefined,
              bossLevel: level.kind === "boss" ? level.order : null,
              baseXP: xpNominal,
              multipliers: {
                streak: typeof reward?.streak_multiplier === "number" ? reward.streak_multiplier : 1,
                combo: typeof reward?.combo === "number" ? reward.combo : 1,
                first_of_day: false,
                critical: reward?.critical_hit ? 10 : 1,
                double_xp: false,
              },
            },
          }),
        );
      }

      await refetchGamification();

      onMastered?.(xpAwarded ?? level.diamonds, {
        stars: (res as Record<string, unknown>).stars as number | undefined,
        reward: reward,
        xp_nominal: xpNominal,
      });
    } catch (e: unknown) {
      setFeedback({ ok: false, msg: e instanceof Error ? e.message : "Complete failed." });
    } finally {
      setBusy(false);
    }
  }, [worldId, level.id, level.diamonds, level.kind, level.order, code, language, onMastered, refetchGamification]);

  const characterState = showSuccess
    ? "correct"
    : currentStep?.type === "discover"
      ? "discovering"
      : "thinking";

  // Get code content for editor
  const codeContent = currentStep?.content.code || currentStep?.content.build;
  const breakContent = currentStep?.content.break_step;
  const debugContent = currentStep?.content.debug;
  const codeStarter =
    codeContent?.starter || debugContent?.buggy_code || breakContent?.broken_code || code;
  const promptText =
    currentStep?.content.predict?.prompt ||
    currentStep?.content.retrieval?.prompt ||
    currentStep?.content.transfer?.prompt ||
    codeContent?.prompt ||
    breakContent?.prompt ||
    debugContent?.prompt ||
    "";

  if (steps.length === 0 && !showSuccess) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center sm:items-center justify-center p-0 sm:p-4"
      >
        <div className="bg-white rounded-t-2xl sm:rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto p-6 text-center">
          {loadError ? (
            <>
              <p className="text-sm font-semibold text-red-700 mb-2">Could not load this level</p>
              <p className="text-xs text-text-muted mb-4">{loadError}</p>
              <button
                onClick={onClose}
                className="px-4 py-2 rounded-lg bg-black text-white text-sm font-semibold"
              >
                Close
              </button>
            </>
          ) : (
            <>
              <Loader2 className="w-8 h-8 animate-spin mx-auto mb-3 text-primary" />
              <p className="text-sm text-text-muted">Loading lesson content…</p>
            </>
          )}
        </div>
      </motion.div>
    );
  }

  const stepTitle = currentStep?.content.mental_model || level.concept;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-end sm:items-center justify-center p-0 sm:p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ y: 40, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: 40, opacity: 0 }}
        transition={{ type: "spring", damping: 25, stiffness: 300 }}
        className="w-full sm:max-w-lg bg-white rounded-t-2xl sm:rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-3 border-b border-border sticky top-0 bg-white rounded-t-2xl z-10">
          <div className="flex items-center gap-2 min-w-0">
            <PlayerCharacter state={characterState} size="sm" />
            <div className="min-w-0">
              <div className="text-sm font-bold truncate">{level.title}</div>
              <div className="text-[11px] text-text-muted truncate">{level.concept}</div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg hover:bg-zinc-100 min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Step indicator */}
        {!showSuccess && steps.length > 1 && (
          <div className="px-5 py-2 flex items-center gap-1.5 overflow-x-auto">
            {steps.map((step, idx) => {
              const meta = STEP_META[step.type];
              const Icon = meta.icon;
              const active = idx === currentStepIndex;
              const done = idx < currentStepIndex;
              return (
                <div
                  key={idx}
                  className={`flex items-center gap-1 px-2 py-1 rounded-full text-[10px] font-mono whitespace-nowrap border ${
                    done
                      ? "bg-emerald-50 border-emerald-200 text-emerald-700"
                      : active
                        ? meta.color
                        : "bg-zinc-50 border-border text-text-muted"
                  }`}
                >
                  <Icon size={10} />
                  <span>{meta.label}</span>
                </div>
              );
            })}
          </div>
        )}

        {/* Body */}
        <div className="px-5 py-4 space-y-4">
          {showSuccess ? (
            /* ═══ VICTORY ═══ */
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ type: "spring", damping: 15 }}
              className="space-y-4 py-4"
            >
              <div className="text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.2, type: "spring" }}
                  className="text-4xl mb-2"
                >
                  🏆
                </motion.div>
                <motion.h3
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="text-lg font-bold text-text-primary"
                >
                  MISSION COMPLETE
                </motion.h3>
                <motion.p
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.35 }}
                  className="text-sm text-text-muted mt-1"
                >
                  {level.title} — MASTERED
                </motion.p>
              </div>

              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="rounded-xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-green-50 p-4"
              >
                <div className="text-xs font-mono uppercase tracking-widest text-emerald-700 mb-2">🧠 You learned</div>
                <p className="text-sm font-medium text-emerald-900 mb-3">
                  {stepTitle} — a new tool for your engineering toolkit.
                </p>
                <ul className="space-y-1.5">
                  {(currentStep?.content.mastery_evidence && currentStep.content.mastery_evidence.length > 0
                    ? currentStep.content.mastery_evidence
                    : ["Understood the concept", "Predicted what would happen", "Built a working solution", "Solved a new situation"]
                  ).map((item, idx) => (
                    <li key={idx} className="text-sm flex items-start gap-2 text-emerald-800">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>

              <div className="flex items-center gap-3">
                <div className="flex-1 h-px bg-border" />
                <span className="text-[10px] text-text-muted uppercase tracking-widest">Unlock</span>
                <div className="flex-1 h-px bg-border" />
              </div>

              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.5 }}
                className="text-center"
              >
                <p className="text-sm text-text-primary font-medium">🔓 The next path is now open</p>
                <p className="text-xs text-text-muted mt-1">Your journey continues...</p>
              </motion.div>

              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.6, type: "spring" }}
                className="flex items-center justify-center gap-4 text-sm"
              >
                <span className="flex items-center gap-1 text-yellow-600 font-semibold">
                  <Zap className="w-4 h-4" /> +{level.diamonds} Diamonds
                </span>
                <span className="text-text-muted">·</span>
                <span className="flex items-center gap-1 text-yellow-500 font-semibold">
                  +5 🪙
                </span>
              </motion.div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={handleComplete}
                disabled={busy}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3.5 min-h-[48px] flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <ChevronRight className="w-4 h-4" />}
                Continue Journey
              </motion.button>
            </motion.div>
          ) : currentStep?.type === "discover" ? (
            /* ═══ DISCOVER ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              {(currentStep.content.story?.line || currentStep.content.tutor?.discover) && (
                <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                  <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">
                    {currentStep.content.story?.location || "Lesson"}
                  </div>
                  <p className="text-sm">
                    {currentStep.content.story?.line || currentStep.content.tutor?.discover}
                    {currentStep.content.story?.npc ? ` — ${currentStep.content.story.npc}` : ""}
                  </p>
                </div>
              )}
              {currentStep.content.discover?.visual && (
                <div className="text-center py-4">
                  <pre className="text-sm font-mono bg-surface-2 rounded-xl p-4 inline-block text-left overflow-x-auto">
                    {currentStep.content.discover.visual}
                  </pre>
                </div>
              )}
              {currentStep.content.discover?.interaction && (
                <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                  <div className="text-xs font-mono uppercase tracking-widest text-primary mb-2">Quick Check</div>
                  <p className="text-sm mb-3">{currentStep.content.discover.prompt}</p>
                  <div className="flex flex-wrap gap-2">
                    {(currentStep.content.discover.values || []).map((v, i) => (
                      <button
                        key={i}
                        onClick={() => setCode(String(v))}
                        className={`px-4 py-2 rounded-xl border text-sm font-medium transition-all min-h-[44px] ${
                          code === String(v)
                            ? "bg-primary text-white border-primary"
                            : "bg-white border-border hover:border-primary/40"
                        }`}
                      >
                        {String(v)}
                      </button>
                    ))}
                  </div>
                </div>
              )}
              {currentStep.content.mental_model && (
                <div className="rounded-xl bg-blue-50 border border-blue-100 p-3">
                  <div className="text-xs font-mono uppercase tracking-widest text-blue-600 mb-1">Mental Model</div>
                  <p className="text-sm text-blue-900 italic">{currentStep.content.mental_model}</p>
                </div>
              )}
              <button
                onClick={advanceStep}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2"
              >
                {currentStepIndex < steps.length - 1 ? "Continue" : "Begin Coding"} <ChevronRight className="w-4 h-4" />
              </button>
            </motion.div>
          ) : currentStep?.type === "manipulate" ? (
            /* ═══ MANIPULATE ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              <div className="rounded-xl bg-purple-50 border border-purple-200 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-purple-700 mb-1">Manipulate</div>
                <p className="text-sm font-medium text-purple-900">{currentStep.content.manipulate?.hint || "Fill in the blanks"}</p>
              </div>
              {currentStep.content.manipulate?.template && (
                <div>
                  <label className="block text-xs font-mono uppercase tracking-widest text-text-muted mb-1">
                    Complete the code
                  </label>
                  <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    rows={8}
                    spellCheck={false}
                    className="w-full rounded-xl border border-border bg-[#0f172a] text-zinc-100 font-mono text-sm px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/40 resize-none"
                    placeholder="# complete the code"
                    disabled={busy}
                  />
                </div>
              )}
              {feedback && (
                <div
                  className={`rounded-xl border px-3 py-2.5 text-sm ${
                    feedback.ok
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                      : "bg-amber-50 border-amber-200 text-amber-900"
                  }`}
                >
                  {feedback.msg}
                  {feedback.runOutput ? <RunOutputPanel output={feedback.runOutput} /> : null}
                </div>
              )}
              <div className="flex gap-2">
                <button
                  onClick={() => handleAttempt(code, "manipulate")}
                  disabled={busy || !code.trim()}
                  className="flex-1 rounded-xl bg-gradient-to-r from-primary to-primary-dark hover:shadow-lg text-white font-semibold py-2.5 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                  Check
                </button>
                <button
                  onClick={advanceStep}
                  disabled={busy}
                  className="rounded-xl border border-border hover:bg-zinc-50 text-text-secondary font-semibold py-2.5 px-4 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  Skip <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            </motion.div>
          ) : currentStep?.type === "predict" ? (
            /* ═══ PREDICT ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              <div className="rounded-xl bg-amber-50 border border-amber-200 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-amber-700 mb-1">Predict</div>
                <p className="text-sm font-medium text-amber-900">{currentStep.content.predict?.prompt}</p>
              </div>
              <div>
                <label className="block text-xs font-mono uppercase tracking-widest text-text-muted mb-1">Your prediction</label>
                <input
                  type="text"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  className="w-full rounded-xl border border-border bg-surface-base px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/40"
                  placeholder="Type your answer..."
                  disabled={busy}
                />
              </div>
              {feedback && (
                <div
                  className={`rounded-xl border px-3 py-2.5 text-sm ${
                    feedback.ok
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                      : "bg-amber-50 border-amber-200 text-amber-900"
                  }`}
                >
                  {feedback.msg}
                  {feedback.runOutput ? <RunOutputPanel output={feedback.runOutput} /> : null}
                </div>
              )}
              <button
                onClick={() => handleAttempt(code, "predict")}
                disabled={busy || !code.trim()}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                Check Prediction
              </button>
            </motion.div>
          ) : currentStep?.type === "retrieval" ? (
            /* ═══ RETRIEVAL ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              <div className="rounded-xl bg-indigo-50 border border-indigo-200 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-indigo-700 mb-1">🧠 Recall</div>
                <p className="text-sm font-medium text-indigo-900">{currentStep.content.retrieval?.prompt}</p>
              </div>
              <div>
                <label className="block text-xs font-mono uppercase tracking-widest text-text-muted mb-1">Your answer</label>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  rows={4}
                  className="w-full rounded-xl border border-border bg-surface-base px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-primary/40 resize-none"
                  placeholder="Write what you remember..."
                  disabled={busy}
                />
              </div>
              {feedback && (
                <div
                  className={`rounded-xl border px-3 py-2.5 text-sm ${
                    feedback.ok
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                      : "bg-amber-50 border-amber-200 text-amber-900"
                  }`}
                >
                  {feedback.msg}
                  {feedback.runOutput ? <RunOutputPanel output={feedback.runOutput} /> : null}
                </div>
              )}
              <button
                onClick={() => handleAttempt(code, "retrieval")}
                disabled={busy || !code.trim()}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                Submit Answer
              </button>
            </motion.div>
          ) : currentStep?.type === "transfer" ? (
            /* ═══ TRANSFER ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              <div className="rounded-xl bg-teal-50 border border-teal-200 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-teal-700 mb-1">Transfer</div>
                <p className="text-sm font-medium text-teal-900">{currentStep.content.transfer?.prompt}</p>
                {currentStep.content.transfer?.context && (
                  <p className="text-xs text-text-muted mt-1">{currentStep.content.transfer.context}</p>
                )}
              </div>
              <div>
                <label className="block text-xs font-mono uppercase tracking-widest text-text-muted mb-1">Your solution</label>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  rows={8}
                  spellCheck={false}
                  className="w-full rounded-xl border border-border bg-[#0f172a] text-zinc-100 font-mono text-sm px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/40 resize-none"
                  placeholder="# write your solution here"
                  disabled={busy}
                />
              </div>
              {feedback && (
                <div
                  className={`rounded-xl border px-3 py-2.5 text-sm ${
                    feedback.ok
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                      : "bg-amber-50 border-amber-200 text-amber-900"
                  }`}
                >
                  {feedback.msg}
                  {feedback.runOutput ? <RunOutputPanel output={feedback.runOutput} /> : null}
                </div>
              )}
              <button
                onClick={() => handleAttempt(code, "transfer")}
                disabled={busy || !code.trim()}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                Submit Transfer
              </button>
            </motion.div>
          ) : currentStep?.type === "mastery" ? (
            /* ═══ MASTERY ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              <div className="rounded-xl bg-yellow-50 border border-yellow-200 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-yellow-700 mb-1">Mastery</div>
                <p className="text-sm font-medium text-yellow-900">
                  {currentStep.content.mastery || "Prove you can apply this independently."}
                </p>
                {currentStep.content.mastery_evidence?.length > 0 && (
                  <ul className="mt-2 space-y-1">
                    {currentStep.content.mastery_evidence.map((item, idx) => (
                      <li key={idx} className="text-xs text-yellow-800 list-disc list-inside">{item}</li>
                    ))}
                  </ul>
                )}
              </div>
              <div>
                <label className="block text-xs font-mono uppercase tracking-widest text-text-muted mb-1">Your solution</label>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  rows={8}
                  spellCheck={false}
                  className="w-full rounded-xl border border-border bg-[#0f172a] text-zinc-100 font-mono text-sm px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/40 resize-none"
                  placeholder="# write your mastery solution here"
                  disabled={busy}
                />
              </div>
              {feedback && (
                <div
                  className={`rounded-xl border px-3 py-2.5 text-sm ${
                    feedback.ok
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                      : "bg-amber-50 border-amber-200 text-amber-900"
                  }`}
                >
                  {feedback.msg}
                  {feedback.runOutput ? <RunOutputPanel output={feedback.runOutput} /> : null}
                </div>
              )}
              <button
                onClick={() => handleAttempt(code, "mastery")}
                disabled={busy || !code.trim()}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trophy className="w-4 h-4" />}
                Submit Mastery
              </button>
            </motion.div>
          ) : currentStep?.type === "break_step" ? (
            /* ═══ BREAK — predict the failure ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              {promptText && (
                <div className="rounded-xl bg-red-50 border border-red-200 p-4">
                  <div className="text-xs font-mono uppercase tracking-widest text-red-700 mb-1">Break it</div>
                  <p className="text-sm font-medium text-red-900">{promptText}</p>
                </div>
              )}
              {currentStep.content.break_step?.broken_code && (
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-mono uppercase tracking-widest text-text-muted">Read-only — what will happen?</label>
                    <span className="text-xs font-mono text-primary">{language}</span>
                  </div>
                  <pre className="w-full rounded-xl border border-border bg-[#0f172a] text-zinc-100 font-mono text-sm px-4 py-3 overflow-x-auto whitespace-pre-wrap">{currentStep.content.break_step.broken_code}</pre>
                </div>
              )}
              <div>
                <label className="block text-xs font-mono uppercase tracking-widest text-text-muted mb-1">Your prediction</label>
                <input
                  type="text"
                  value={prediction}
                  onChange={(e) => setPrediction(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && prediction.trim() && !busy) handleAttempt(prediction, "break_step");
                  }}
                  className="w-full rounded-xl border border-border bg-[#0f172a] text-zinc-100 font-mono text-sm px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/40"
                  placeholder="e.g. it raises a TypeError because you cannot add a number to text"
                  disabled={busy}
                />
              </div>
              {feedback && (
                <div
                  className={`rounded-xl border px-3 py-2.5 text-sm ${
                    feedback.ok
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                      : "bg-amber-50 border-amber-200 text-amber-900"
                  }`}
                >
                  {feedback.msg}
                  {feedback.runOutput ? <RunOutputPanel output={feedback.runOutput} /> : null}
                </div>
              )}
              <button
                onClick={() => handleAttempt(prediction, "break_step")}
                disabled={busy || !prediction.trim()}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
              >
                {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                Check Prediction
              </button>
            </motion.div>
          ) : currentStep?.type === "debug" ? (
            /* ═══ DEBUG ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              <div className="rounded-xl bg-orange-50 border border-orange-200 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-orange-700 mb-1">Debug</div>
                <p className="text-sm font-medium text-orange-900">{promptText || "Find and fix the bug."}</p>
              </div>
              {currentStep.content.debug?.buggy_code && (
                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-mono uppercase tracking-widest text-text-muted">Broken code</label>
                    <span className="text-xs font-mono text-primary">{language}</span>
                  </div>
                  <pre className="w-full rounded-xl border border-border bg-[#0f172a] text-zinc-100 font-mono text-sm px-4 py-3 overflow-x-auto whitespace-pre-wrap">{currentStep.content.debug.buggy_code}</pre>
                </div>
              )}
              <div>
                <label className="block text-xs font-mono uppercase tracking-widest text-text-muted mb-1">Your fix</label>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  rows={8}
                  spellCheck={false}
                  className="w-full rounded-xl border border-border bg-[#0f172a] text-zinc-100 font-mono text-sm px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/40 resize-none"
                  placeholder="# paste your fix"
                  disabled={busy}
                />
              </div>
              {feedback && (
                <div
                  className={`rounded-xl border px-3 py-2.5 text-sm ${
                    feedback.ok
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                      : "bg-amber-50 border-amber-200 text-amber-900"
                  }`}
                >
                  {feedback.msg}
                  {feedback.runOutput ? <RunOutputPanel output={feedback.runOutput} /> : null}
                </div>
              )}
              <div className="flex gap-2">
                <button
                  onClick={() => handleAttempt(code, "debug")}
                  disabled={busy || !code.trim()}
                  className="flex-1 rounded-xl bg-gradient-to-r from-primary to-primary-dark hover:shadow-lg text-white font-semibold py-2.5 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                  {isLastStep ? "Complete" : "Check"}
                </button>
                {!isLastStep && (
                  <button
                    onClick={advanceStep}
                    disabled={busy}
                    className="rounded-xl border border-border hover:bg-zinc-50 text-text-secondary font-semibold py-2.5 px-4 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    Skip <ChevronRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </motion.div>
          ) : (
            /* ═══ BUILD / CODE ═══ */
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-3"
            >
              {promptText && (
                <div className="rounded-xl bg-emerald-50 border border-emerald-200 p-3">
                  <div className="text-xs font-mono uppercase tracking-widest text-emerald-700 mb-1">Challenge</div>
                  <p className="text-sm">{promptText}</p>
                </div>
              )}

              {/* Language selector */}
              <div className="flex items-center gap-1 bg-zinc-50 rounded-lg p-1">
                <Code2 className="w-3.5 h-3.5 text-text-muted ml-2" />
                {LANGUAGES.map((lang) => (
                  <button
                    key={lang.id}
                    onClick={() => setLanguage(lang.id)}
                    className={`flex-1 flex items-center justify-center gap-1 py-1.5 px-2 rounded-md text-xs font-medium transition-colors min-h-[32px] ${
                      language === lang.id
                        ? "bg-white shadow-sm text-primary border border-border"
                        : "text-text-muted hover:text-text-primary"
                    }`}
                  >
                    <span>{lang.icon}</span>
                    <span>{lang.name}</span>
                  </button>
                ))}
              </div>

              <div className="rounded-xl bg-[#0f172a] p-3">
                <div className="text-[11px] font-mono text-zinc-400 mb-1">your code ({language})</div>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  rows={8}
                  spellCheck={false}
                  className="w-full bg-transparent font-mono text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none resize-none min-h-[160px]"
                  placeholder={codeStarter as string || "# write your solution here"}
                />
              </div>

              {feedback && (
                <div
                  className={`rounded-xl border px-3 py-2.5 text-sm ${
                    feedback.ok
                      ? "bg-emerald-50 border-emerald-200 text-emerald-800"
                      : "bg-amber-50 border-amber-200 text-amber-900"
                  }`}
                >
                  {feedback.msg}
                  {feedback.runOutput ? <RunOutputPanel output={feedback.runOutput} /> : null}
                </div>
              )}

              {/* Mystery boxes — gamified hints */}
              <MysteryBoxContainer
                boxes={
                  currentStep?.content.hints && currentStep.content.hints.length > 0
                    ? currentStep.content.hints.map((hint, idx) => ({
                        id: `hint-${idx}`,
                        title: hint.title || `Hint ${idx + 1}`,
                        icon: hint.icon || "💡",
                        description: hint.description || "",
                        hint: typeof hint === "string" ? hint : hint.hint || "",
                        mental_model: hint.mental_model || "",
                        xp_reward: typeof hint.xp_reward === "number" ? hint.xp_reward : 5,
                        coin_reward: 0,
                        rarity: hint.rarity || "common",
                        color: hint.color || "#8B5CF6",
                      }))
                    : [
                        {
                          id: "h1",
                          title: "A Nudge",
                          icon: "🔍",
                          description: "Think about the approach",
                          hint: "What's the simplest way to start? Look for patterns.",
                          mental_model: "Start simple, then optimize.",
                          xp_reward: 5,
                          coin_reward: 0,
                          rarity: "common" as const,
                          color: "#94a3b8",
                        },
                        {
                          id: "h2",
                          title: "The Pattern",
                          icon: "🧩",
                          description: "Which technique fits?",
                          hint: "Think: have you seen a similar problem? What data structure helps here?",
                          mental_model: "Most problems are patterns in disguise.",
                          xp_reward: 10,
                          coin_reward: 0,
                          rarity: "rare" as const,
                          color: "#3b82f6",
                        },
                        {
                          id: "h3",
                          title: "The Approach",
                          icon: "💡",
                          description: "Here's the strategy",
                          hint: "Break the problem into smaller steps. Solve each step, then combine.",
                          mental_model: "Decompose → solve → combine.",
                          xp_reward: 15,
                          coin_reward: 0,
                          rarity: "epic" as const,
                          color: "#8b5cf6",
                        },
                      ]
                }
                openedIndices={openedBoxes}
                onOpen={(idx) => {
                  setOpenedBoxes((prev) => new Set([...prev, idx]));
                }}
              />

              <div className="flex gap-2">
                <button
                  onClick={() => handleAttempt(code, currentStep?.type || "code")}
                  disabled={busy || !code.trim()}
                  className="flex-1 rounded-xl bg-gradient-to-r from-primary to-primary-dark hover:shadow-lg text-white font-semibold py-2.5 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                  {isLastStep ? "Complete" : "Check"}
                </button>
                {!isLastStep && (
                  <button
                    onClick={advanceStep}
                    disabled={busy}
                    className="rounded-xl border border-border hover:bg-zinc-50 text-text-secondary font-semibold py-2.5 px-4 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
                  >
                    Skip <ChevronRight className="w-4 h-4" />
                  </button>
                )}
              </div>
            </motion.div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}
