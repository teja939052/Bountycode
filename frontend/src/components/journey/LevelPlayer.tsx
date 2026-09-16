import { useState, useCallback, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { X, Lightbulb, CheckCircle2, Loader2, Code2, ChevronRight } from "lucide-react";
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

type Phase = "discover" | "code" | "testing" | "success";

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

export function LevelPlayer({ worldId, level, onClose, onMastered }: LevelPlayerProps) {
  const [phase, setPhase] = useState<Phase>("discover");
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [feedback, setFeedback] = useState<{ ok: boolean; msg: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [openedBoxes, setOpenedBoxes] = useState<Set<number>>(new Set());

  const attemptsRef = useRef(0);
  const contentRef = useRef<LevelContent | null>(null);

  // Track lesson start
  useEffect(() => {
    analytics.lessonStarted(level.id, worldId);
    if (level.kind === "boss") analytics.bossStarted(level.id);
  }, [level.id, worldId, level.kind]);

  // Load world content from backend
  const loadWorld = useCallback(async () => {
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
          // Prefill code from backend content if available
          const codeContent = (current.code || current.build || {}) as Record<string, unknown>;
          const starter = typeof codeContent.starter === "string" ? codeContent.starter : "";
          if (starter && !code) {
            setCode(starter);
          }
          // Set language from content if available
          const contentLanguage = typeof codeContent.language === "string" ? codeContent.language : null;
          if (contentLanguage && !code) {
            setLanguage(contentLanguage);
          }
        }
      }
    } catch {
      // content stays null; UI falls back to empty state
    }
  }, [worldId, level.id, code]);

  useEffect(() => {
    void loadWorld();
  }, [loadWorld]);

  const content = contentRef.current;

  const handleAttempt = useCallback(async () => {
    setBusy(true);
    setFeedback(null);
    attemptsRef.current += 1;
    analytics.buildAttempted(level.id, code);
    try {
      const res = await api.journey.attemptLevel(worldId, level.id, {
        code,
        language,
        time_spent_seconds: 0,
      });
      if (res.passed) {
        setPhase("success");
        analytics.buildPassed(level.id, attemptsRef.current);
        if (level.kind === "boss") {
          analytics.bossPassed(level.id, attemptsRef.current);
        } else {
          analytics.transferAttempted(level.id);
        }
      } else {
        setFeedback({ ok: false, msg: (res as Record<string, unknown>).message as string || (res as Record<string, unknown>).hint as string || "Not quite — try a hint!" });
        analytics.buildFailed(level.id, attemptsRef.current);
      }
    } catch (e: unknown) {
      setFeedback({ ok: false, msg: e instanceof Error ? e.message : "Check failed." });
      analytics.buildFailed(level.id, attemptsRef.current);
    } finally {
      setBusy(false);
    }
  }, [worldId, level.id, code, language, level.kind]);

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

  const characterState = phase === "success" ? "correct" : phase === "discover" ? "discovering" : "thinking";

  // Real content from backend
  const discoverContent = content?.discover;
  const manipulateContent = content?.manipulate;
  const codeContent = content?.code || content?.build;
  const hintsContent = content?.hints;
  const storyContent = content?.story;
  const tutorContent = content?.tutor;
  const predictContent = content?.predict;
  const breakContent = content?.break_step;
  const debugContent = content?.debug;
  const retrievalContent = content?.retrieval;
  const transferContent = content?.transfer;

  const promptText = discoverContent?.prompt || predictContent?.prompt || breakContent?.prompt || debugContent?.prompt || retrievalContent?.prompt || transferContent?.prompt || codeContent?.prompt || level.concept || "";
  const codeStarter = codeContent?.starter || manipulateContent?.template || "";
  const codeLanguage = codeContent?.language || language;

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
            <PlayerCharacter state={characterState as "correct" | "discovering" | "thinking"} size="sm" />
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
          {/* Story / Tutor narration */}
          {(storyContent?.line || tutorContent?.discover) && (
            <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
              <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">
                {storyContent?.location || "Lesson"}
              </div>
              <p className="text-sm">
                {storyContent?.line || tutorContent?.discover}
                {storyContent?.npc ? ` — ${storyContent.npc}` : ""}
              </p>
            </div>
          )}

          {/* Discover phase */}
          {phase === "discover" && discoverContent && (
            <div className="space-y-3">
              <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">Discover</div>
                {discoverContent.visual && (
                  <div className="text-2xl mb-2">{discoverContent.visual}</div>
                )}
                <p className="text-sm">{discoverContent.prompt}</p>
              </div>
              <button
                onClick={() => {
                  setPhase("code");
                  analytics.discoveryCompleted(level.id);
                }}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2"
              >
                Try it <Lightbulb className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Predict phase */}
          {phase === "discover" && predictContent && !discoverContent && (
            <div className="space-y-3">
              <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">Predict</div>
                <p className="text-sm">{predictContent.prompt}</p>
              </div>
              <button
                onClick={() => {
                  setPhase("code");
                  analytics.discoveryCompleted(level.id);
                }}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2"
              >
                Check Prediction <Target className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Fallback discover if no content */}
          {phase === "discover" && !discoverContent && !predictContent && (
            <div className="space-y-3">
              <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">Discover</div>
                <p className="text-sm">{level.concept ? `${level.concept.charAt(0).toUpperCase() + level.concept.slice(1)}` : "A new concept"} — a new tool for your engineering toolkit.</p>
              </div>
              <button
                onClick={() => {
                  setPhase("code");
                  analytics.discoveryCompleted(level.id);
                }}
                className="w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3 min-h-[44px] flex items-center justify-center gap-2"
              >
                Try it <Lightbulb className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Code phase */}
          {(phase === "code" || phase === "testing") && (
            <div className="space-y-3">
              {/* Code prompt from backend */}
              {promptText && (
                <div className="rounded-xl bg-primary/5 border border-primary/10 p-3">
                  <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">Challenge</div>
                  <p className="text-sm">{promptText}</p>
                </div>
              )}

              {/* Language selector */}
              <div className="flex items-center gap-1 bg-zinc-50 rounded-lg p-1">
                <Code2 className="w-3.5 h-3.5 text-text-muted ml-2" />
                {LANGUAGES.map((lang) => (
                  <button
                    key={lang.id}
                    onClick={() => {
                      setLanguage(lang.id);
                      // Load starter code for this language from the API
                      void (async () => {
                        try {
                          const sig = level.canonical_skill || "def solution():";
                          const res = await fetch("/api/v1/compiler/starter-code", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ signature: `def solution(${sig.replace("coding.", "").replace(".", "_")}) -> int:`, language: lang.id }),
                          });
                          if (res.ok) {
                            const data = await res.json();
                            if (data.code) setCode(data.code);
                          }
                        } catch {
                          // Keep current code if API fails
                        }
                      })();
                    }}
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
                <div className="text-[11px] font-mono text-zinc-400 mb-1">your code ({codeLanguage || language})</div>
                <textarea
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  rows={6}
                  spellCheck={false}
                  className="w-full bg-transparent font-mono text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none resize-none min-h-[120px]"
                  placeholder={codeStarter || "# write your solution here"}
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

              {/* Mystery boxes — gamified hints from backend or fallback */}
              <MysteryBoxContainer
                boxes={(() => {
                  if (hintsContent && hintsContent.length > 0) {
                    return hintsContent.map((hint, idx) => ({
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
                    }));
                  }
                  return [
                    { id: "h1", title: "A Nudge", icon: "🔍", description: "Think about the approach", hint: "What's the simplest way to start? Look for patterns.", mental_model: "Start simple, then optimize.", xp_reward: 5, rarity: "common" as const, color: "#94a3b8", coin_reward: 0 },
                    { id: "h2", title: "The Pattern", icon: "🧩", description: "Which technique fits?", hint: "Think: have you seen a similar problem? What data structure helps here?", mental_model: "Most problems are patterns in disguise.", xp_reward: 10, rarity: "rare" as const, color: "#3b82f6", coin_reward: 0 },
                    { id: "h3", title: "The Approach", icon: "💡", description: "Here's the strategy", hint: "Break the problem into smaller steps. Solve each step, then combine.", mental_model: "Decompose → solve → combine.", xp_reward: 15, rarity: "epic" as const, color: "#8b5cf6", coin_reward: 0 },
                  ];
                })()}
                openedIndices={openedBoxes}
                onOpen={(idx) => {
                  setOpenedBoxes((prev) => new Set([...prev, idx]));
                }}
              />

              <div className="flex gap-2">
                <button
                  onClick={handleAttempt}
                  disabled={busy}
                  className="flex-1 rounded-xl bg-gradient-to-r from-primary to-primary-dark hover:shadow-lg text-white font-semibold py-2.5 min-h-[44px] flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <CheckCircle2 className="w-4 h-4" />}
                  Check
                </button>
              </div>
            </div>
          )}

          {/* Success phase — mastery proven */}
          {phase === "success" && (
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

              {/* What you learned — evidence-based */}
              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.4 }}
                className="rounded-xl border border-emerald-200 bg-gradient-to-br from-emerald-50 to-green-50 p-4"
              >
                <div className="text-xs font-mono uppercase tracking-widest text-emerald-700 mb-2">
                  🧠 You learned
                </div>
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

              {/* Unlock consequence */}
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
                <p className="text-sm text-text-primary font-medium">
                  🔓 The next path is now open
                </p>
                <p className="text-xs text-text-muted mt-1">
                  Your journey continues...
                </p>
              </motion.div>

              {/* Reward — secondary */}
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
          )}
        </div>
      </motion.div>
    </motion.div>
  );
}
