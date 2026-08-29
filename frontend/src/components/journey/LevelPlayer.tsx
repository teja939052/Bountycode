import { useState, useCallback, useRef } from "react";
import { motion } from "framer-motion";
import { X, Lightbulb, CheckCircle2, Loader2, Code2, Zap, ChevronRight } from "lucide-react";
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
  onMastered?: (xp: number) => void;
}

type Phase = "discover" | "code" | "testing" | "success";

/**
 * Lightweight level player overlay.
 *
 * Renders the level's discover → code → test → success loop using the
 * existing ``/api/v1/worlds`` level endpoints.  On completion it calls the
 * Study Engine's ``record_activity`` so mastery / SRS / XP all update, then
 * refreshes the journey state so the character visibly moves.
 */
export function LevelPlayer({ worldId, level, onClose, onMastered }: LevelPlayerProps) {
  const [phase, setPhase] = useState<Phase>("discover");
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");
  const [feedback, setFeedback] = useState<{ ok: boolean; msg: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [hintIdx, setHintIdx] = useState<number | null>(null);
  const [worldData, setWorldData] = useState<Record<string, unknown> | null>(null);
  const [openedBoxes, setOpenedBoxes] = useState<Set<number>>(new Set());

  // Get hint ladder for this problem (if any)
  const hintBoxes = useRef<Record<string, unknown> | null>(null);
  const attemptsRef = useRef(0);

  // Track lesson start
  useState(() => {
    analytics.lessonStarted(level.id, worldId);
    if (level.kind === "boss") analytics.bossStarted(level.id);
  });

  const loadWorld = useCallback(async () => {
    try {
      const res = await api.journey.getWorldView(worldId);
      setWorldData(res.world ?? res);
    } catch {
      setWorldData(null);
    }
  }, [worldId]);

  // Lazily load world detail on first render so we can surface story/tutor.
  useState(() => {
    void loadWorld();
  });

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
        setFeedback({ ok: false, msg: res.message ?? res.hint ?? "Not quite — try a hint!" });
        analytics.buildFailed(level.id, attemptsRef.current);
        if (res.hint_index != null) setHintIdx(res.hint_index);
      }
    } catch (e: unknown) {
      setFeedback({ ok: false, msg: e instanceof Error ? e.message : "Check failed." });
      analytics.buildFailed(level.id, attemptsRef.current);
    } finally {
      setBusy(false);
    }
  }, [worldId, level.id, code]);

  const handleComplete = useCallback(async () => {
    setBusy(true);
    try {
      await api.journey.completeLevel(worldId, level.id, { code, language, time_spent_seconds: 0 });
      // Fan-out to mastery / SRS / XP via the Study Engine.
      await api.journey.recordActivity({
        type: "learn",
        skill_id: level.canonical_skill || level.concept,
        passed: true,
        score: 100,
        time_spent: 0,
      });
      analytics.masteryAchieved(level.id, worldId, level.xp);
      refreshJourneyState();
      onMastered?.(level.xp);
    } catch (e: unknown) {
      setFeedback({ ok: false, msg: e instanceof Error ? e.message : "Complete failed." });
    } finally {
      setBusy(false);
    }
  }, [worldId, level.id, level.canonical_skill, level.concept, level.xp, code, onMastered]);

  const characterState = phase === "success" ? "correct" : phase === "discover" ? "discovering" : "thinking";

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
          {/* Discover phase */}
          {phase === "discover" && (
            <div className="space-y-3">
              <div className="rounded-xl bg-primary/5 border border-primary/10 p-4">
                <div className="text-xs font-mono uppercase tracking-widest text-primary mb-1">Discover</div>
                <p className="text-sm">
                  Every program needs to <strong>remember</strong> things. Let's see how.
                </p>
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
                  rows={6}
                  spellCheck={false}
                  className="w-full bg-transparent font-mono text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none resize-none min-h-[120px]"
                  placeholder="# write your solution here"
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
                boxes={[
                  { id: "h1", title: "A Nudge", icon: "🔍", description: "Think about the approach", hint: hintIdx !== null ? "" : "What's the simplest way to start? Look for patterns.", mental_model: "Start simple, then optimize.", xp_reward: 5, rarity: "common" },
                  { id: "h2", title: "The Pattern", icon: "🧩", description: "Which technique fits?", hint: "Think: have you seen a similar problem? What data structure helps here?", mental_model: "Most problems are patterns in disguise.", xp_reward: 10, rarity: "rare" },
                  { id: "h3", title: "The Approach", icon: "💡", description: "Here's the strategy", hint: "Break the problem into smaller steps. Solve each step, then combine.", mental_model: "Decompose → solve → combine.", xp_reward: 15, rarity: "epic", color: "#8B5CF6" },
                ]}
                openedIndices={openedBoxes}
                onOpen={(idx) => {
                  setOpenedBoxes((prev) => new Set([...prev, idx]));
                  setHintIdx(idx);
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
              className="space-y-5 py-4"
            >
              {/* Header */}
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
                  className="text-lg font-bold text-text-primary tracking-wide"
                >
                  MASTERY PROVEN
                </motion.h3>
              </div>

              {/* What you learned */}
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
                  {level.concept ? `${level.concept.charAt(0).toUpperCase() + level.concept.slice(1)} — a new tool for your engineering toolkit.` : "A new concept for your engineering toolkit."}
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

              {/* Divider */}
              <div className="flex items-center gap-3">
                <div className="flex-1 h-px bg-border" />
                <span className="text-[10px] text-text-muted uppercase tracking-widest">Unlock</span>
                <div className="flex-1 h-px bg-border" />
              </div>

              {/* Unlock consequence */}
              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.6 }}
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
                transition={{ delay: 0.7, type: "spring" }}
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
                className="w-full rounded-xl bg-gradient-to-r from-primary to-primary-dark hover:shadow-lg text-white font-semibold py-3.5 min-h-[48px] flex items-center justify-center gap-2 disabled:opacity-50"
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
