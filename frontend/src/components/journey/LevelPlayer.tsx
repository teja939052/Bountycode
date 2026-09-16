import { useState, useCallback, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { X, CheckCircle2, Loader2, Code2, ChevronRight, Zap } from "lucide-react";
import api from "../../services/api";
import { refreshJourneyState } from "../../hooks/useJourneyState";
import { PlayerCharacter } from "./PlayerCharacter";
import analytics from "../../services/api/analytics";
import { MysteryBoxContainer } from "./MysteryBox";
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
  onMastered?: (xp: number, detail?: {
    stars?: number; reward?: Record<string, unknown>; xp_nominal?: number;
  }) => void;
}

interface LevelContent {
  discover?: { visual?: string; interaction?: string; prompt?: string; answer?: string; values?: unknown[] };
  manipulate?: { type?: string; template?: string; answer?: string; blocks?: string[]; hint?: string };
  predict?: { prompt?: string; answer?: string; explanation?: string };
  build?: { prompt?: string; starter?: string; placeholder?: string; language?: string };
  break_step?: { prompt?: string; broken_code?: string; expected_failure?: string };
  debug?: { prompt?: string; buggy_code?: string; fix_steps?: string[]; answer?: string };
  code?: { prompt?: string; starter?: string; placeholder?: string; language?: string };
  checks?: { required_patterns?: string[]; forbidden?: string[]; hint_triggers?: string[] };
  hints?: Array<{ title?: string; icon?: string; description?: string; hint?: string; mental_model?: string; xp_reward?: number; rarity?: string; color?: string }>;
  retrieval?: { prompt?: string; answer?: string; explanation?: string };
  transfer?: { prompt?: string; answer?: string; context?: string };
  success?: { world_before?: string; world_after?: string; world_reaction?: string; reward_text?: string; byte_line?: string; xp?: number };
  story?: { location?: string; npc?: string; line?: string };
  tutor?: { name?: string; avatar?: string; discover?: string; explain?: string };
  mental_model?: string;
}

interface Step {
  type: "discover" | "predict" | "code" | "break_step" | "debug" | "retrieval" | "transfer" | "success";
  content: LevelContent;
}

export function LevelPlayer({ worldId, level, onClose, onMastered }: LevelPlayerProps) {
  const [steps, setSteps] = useState<Step[]>([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [feedback, setFeedback] = useState<{ ok: boolean; msg: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [openedBoxes, setOpenedBoxes] = useState<Set<number>>(new Set());
  const [showSuccess, setShowSuccess] = useState(false);

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
    void (async () => {
      try {
        const res = await api.journey.getWorldView(worldId);
        const world = (res as Record<string, unknown>).world as Record<string, unknown> | undefined;
        if (world?.towns && Array.isArray(world.towns)) {
          const allLevels: unknown[] = [];
          for (const town of world.towns) {
            const t = town as Record<string, unknown>;
            if (Array.isArray(t.levels)) {
              allLevels.push(...t.levels);
            }
          }
          const current = allLevels.find((l) => (l as Record<string, unknown>).id === level.id) as Record<string, unknown> | undefined;
          if (current) {
            contentRef.current = current as LevelContent;
            const content = current as LevelContent;

            // Build step sequence from available content
            const builtSteps: Step[] = [];

            // Discover is always first
            if (content.discover || content.story || content.tutor) {
              builtSteps.push({ type: "discover", content });
            }

            // Predict comes after discover
            if (content.predict) {
              builtSteps.push({ type: "predict", content });
            }

            // Code/build comes next
            if (content.code || content.build) {
              builtSteps.push({ type: "code", content });
            }

            // Break step
            if (content.break_step) {
              builtSteps.push({ type: "break_step", content });
            }

            // Debug
            if (content.debug) {
              builtSteps.push({ type: "debug", content });
            }

            // Retrieval (SRS campfire)
            if (content.retrieval) {
              builtSteps.push({ type: "retrieval", content });
            }

            // Transfer
            if (content.transfer) {
              builtSteps.push({ type: "transfer", content });
            }

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
        }
      } catch {
        // content stays null; UI falls back to empty state
      }
    })();
  }, [worldId, level.id]);

  const advanceStep = useCallback(() => {
    if (currentStepIndex < steps.length - 1) {
      setCurrentStepIndex((prev) => prev + 1);
      setFeedback(null);
    } else {
      setShowSuccess(true);
    }
  }, [currentStepIndex, steps.length]);

  const handleAttempt = useCallback(async (stepCode: string, stepType: string) => {
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
        setFeedback({ ok: true, msg: (res as Record<string, unknown>).message as string || "Correct!" });
        setTimeout(() => {
          advanceStep();
        }, 800);
      } else {
        const hintIndex = (res as Record<string, unknown>).hint_index as number | null | undefined;
        setFeedback({ ok: false, msg: (res as Record<string, unknown>).message as string || "Not quite — try again!" });
        if (typeof hintIndex === "number") {
          setOpenedBoxes((prev) => new Set([...prev, hintIndex]));
        }
      }
    } catch (e: unknown) {
      setFeedback({ ok: false, msg: e instanceof Error ? e.message : "Check failed." });
    } finally {
      setBusy(false);
    }
  }, [worldId, level.id, language, advanceStep]);

  const handleComplete = useCallback(async () => {
    setBusy(true);
    try {
      const res = await api.journey.completeLevel(worldId, level.id, { code, language, time_spent_seconds: 0 });
      await api.journey.recordActivity({
        type: "learn",
        skill_id: level.canonical_skill || level.concept,
        passed: true,
        score: 100,
        time_spent: 0,
      });
      analytics.masteryAchieved(level.id, worldId, level.xp);
      refreshJourneyState();
      const xpAwarded = (res as Record<string, unknown>).xp_awarded as number | undefined;
      onMastered?.(xpAwarded ?? level.xp, {
        stars: (res as Record<string, unknown>).stars as number | undefined,
        reward: (res as Record<string, unknown>).reward as Record<string, unknown> | undefined,
        xp_nominal: (res as Record<string, unknown>).xp_nominal as number | undefined,
      });
    } catch (e: unknown) {
      setFeedback({ ok: false, msg: e instanceof Error ? e.message : "Complete failed." });
    } finally {
      setBusy(false);
    }
  }, [worldId, level.id, level.canonical_skill, level.concept, level.xp, code, language, onMastered]);

  const characterState = showSuccess ? "correct" : currentStep?.type === "discover" ? "discovering" : "thinking";

  // Get code content for editor
  const codeContent = currentStep?.content.code || currentStep?.content.build;
  const breakContent = currentStep?.content.break_step;
  const debugContent = currentStep?.content.debug;
  const codeStarter = codeContent?.starter || breakContent?.broken_code || debugContent?.buggy_code || code;
  const promptText = currentStep?.content.predict?.prompt || currentStep?.content.retrieval?.prompt || currentStep?.content.transfer?.prompt || codeContent?.prompt || breakContent?.prompt || debugContent?.prompt || "";

  if (steps.length === 0 && !showSuccess) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center sm:items-center justify-center p-0 sm:p-4"
      >
        <div className="bg-white rounded-t-2xl sm:rounded-2xl shadow-2xl max-h-[90vh] overflow-y-auto p-6 text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto mb-3 text-primary" />
          <p className="text-sm text-text-muted">Loading lesson content…</p>
        </div>
      </motion.div>
    );
  }

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

        {/* Body */}
        <div className="px-5 py-4 space-y-4">
          {showSuccess ? (
            /* ═══ SUCCESS ═══ */
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
                  ✨
                </motion.div>
                <motion.h3
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.3 }}
                  className="text-lg font-bold text-text-primary"
                >
                  MASTERY PROVEN
                </motion.h3>
              </div>

              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="rounded-xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-green-50 p-4"
              >
                <div className="text-xs font-mono uppercase tracking-widest text-emerald-700 mb-2">🧠 You learned</div>
                <p className="text-sm font-medium text-emerald-900 mb-3">
                  {level.concept ? `${level.concept.charAt(0).toUpperCase() + level.concept.slice(1)}` : "A new concept"} — a new tool for your engineering toolkit.
                </p>
                <ul className="space-y-1.5">
                  <li className="text-sm flex items-start gap-2 text-emerald-800">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                    <span>Understood the concept</span>
                  </li>
                  <li className="text-sm flex items-start gap-2 text-emerald-800">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                    <span>Predicted what would happen</span>
                  </li>
                  <li className="text-sm flex items-start gap-2 text-emerald-800">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                    <span>Built a working solution</span>
                  </li>
                  <li className="text-sm flex items-start gap-2 text-emerald-800">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
                    <span>Solved a new situation</span>
                  </li>
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
                  <Zap className="w-4 h-4" /> +{level.xp} XP
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
            <div className="space-y-3">
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
                <div className="text-3xl text-center">{currentStep.content.discover.visual}</div>
              )}
              {currentStep.content.discover?.prompt && (
                <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                  <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">Discover</div>
                  <p className="text-sm">{currentStep.content.discover.prompt}</p>
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
            </div>
          ) : currentStep?.type === "predict" ? (
            /* ═══ PREDICT ═══ */
            <div className="space-y-3">
              <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">Predict</div>
                <p className="text-sm font-medium">{currentStep.content.predict?.prompt}</p>
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
                <div className={`rounded-xl border px-3 py-2.5 text-sm ${feedback.ok ? "bg-emerald-50 border-emerald-200 text-emerald-800" : "bg-amber-50 border-amber-200 text-amber-900"}`}>
                  {feedback.msg}
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
            </div>
          ) : currentStep?.type === "retrieval" ? (
            /* ═══ RETRIEVAL ═══ */
            <div className="space-y-3">
              <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">🧠 Recall</div>
                <p className="text-sm font-medium">{currentStep.content.retrieval?.prompt}</p>
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
                <div className={`rounded-xl border px-3 py-2.5 text-sm ${feedback.ok ? "bg-emerald-50 border-emerald-200 text-emerald-800" : "bg-amber-50 border-amber-200 text-amber-900"}`}>
                  {feedback.msg}
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
            </div>
          ) : currentStep?.type === "transfer" ? (
            /* ═══ TRANSFER ═══ */
            <div className="space-y-3">
              <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">Transfer</div>
                <p className="text-sm font-medium">{currentStep.content.transfer?.prompt}</p>
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
                  className="w-full rounded-xl border border-border bg-[#0f172a] text-zinc-100 font-mono text-sm px-4 py-3 focus:outline-none focus:ring-2 focus:ring-primary/40 resize-none"
                  placeholder="# write your solution here"
                  disabled={busy}
                />
              </div>
              {feedback && (
                <div className={`rounded-xl border px-3 py-2.5 text-sm ${feedback.ok ? "bg-emerald-50 border-emerald-200 text-emerald-800" : "bg-amber-50 border-amber-200 text-amber-900"}`}>
                  {feedback.msg}
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
            </div>
          ) : (
            /* ═══ CODE / BREAK / DEBUG ═══ */
            <div className="space-y-3">
              {promptText && (
                <div className="rounded-xl bg-primary/5 border border-primary/10 p-3">
                  <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">
                    {currentStep?.type === "break_step" ? "Break" : currentStep?.type === "debug" ? "Debug" : "Challenge"}
                  </div>
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
                </div>
              )}

              {/* Mystery boxes — gamified hints */}
              <MysteryBoxContainer
                boxes={currentStep?.content.hints && currentStep.content.hints.length > 0 ? currentStep.content.hints.map((hint, idx) => ({
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
                })) : [
                  { id: "h1", title: "A Nudge", icon: "🔍", description: "Think about the approach", hint: "What's the simplest way to start? Look for patterns.", mental_model: "Start simple, then optimize.", xp_reward: 5, coin_reward: 0, rarity: "common" as const, color: "#94a3b8" },
                  { id: "h2", title: "The Pattern", icon: "🧩", description: "Which technique fits?", hint: "Think: have you seen a similar problem? What data structure helps here?", mental_model: "Most problems are patterns in disguise.", xp_reward: 10, coin_reward: 0, rarity: "rare" as const, color: "#3b82f6" },
                  { id: "h3", title: "The Approach", icon: "💡", description: "Here's the strategy", hint: "Break the problem into smaller steps. Solve each step, then combine.", mental_model: "Decompose → solve → combine.", xp_reward: 15, coin_reward: 0, rarity: "epic" as const, color: "#8b5cf6" },
                ]}
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
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}
