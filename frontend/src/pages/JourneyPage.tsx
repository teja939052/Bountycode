import { useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Flame, Map, ChevronRight, Star, Lock, CheckCircle2,
  Zap, Trophy, Coins, RotateCcw, Sparkles, ChevronDown,
  Target, Brain, Swords,
} from "lucide-react";
import { useJourneyState, type JourneyWorld, type JourneyLevel } from "../hooks/useJourneyState";
import { PlayerCharacter, type CharacterState } from "../components/journey/PlayerCharacter";
import { LevelPlayer } from "../components/journey/LevelPlayer";
import { Celebration } from "../components/journey/Celebration";

export default function JourneyPage() {
  const { data: state, isLoading, isError } = useJourneyState();
  const [activeLevel, setActiveLevel] = useState<JourneyLevel | null>(null);
  const [activeWorldId, setActiveWorldId] = useState<string | null>(null);
  const [celebrate, setCelebrate] = useState(false);
  const [celebrateXp, setCelebrateXp] = useState(50);
  const [showAllWorlds, setShowAllWorlds] = useState(false);

  const handleContinue = useCallback((level: JourneyLevel, worldId: string) => {
    setActiveLevel(level);
    setActiveWorldId(worldId);
  }, []);

  const handleCloseLevel = useCallback(() => {
    setActiveLevel(null);
    setActiveWorldId(null);
  }, []);

  const handleLevelMastered = useCallback((xp: number) => {
    setActiveLevel(null);
    setActiveWorldId(null);
    setCelebrateXp(xp);
    setCelebrate(true);
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center gap-4">
        <div className="h-12 w-12 animate-spin rounded-full border-3 border-primary/20 border-t-primary" />
        <p className="text-sm text-text-muted">Loading your journey…</p>
      </div>
    );
  }

  if (isError || !state) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center gap-4 px-6 text-center">
        <p className="text-lg font-semibold">Journey unavailable</p>
        <Link to="/dashboard" className="text-sm text-primary underline">Back to dashboard</Link>
      </div>
    );
  }

  const { character, worlds, stats } = state;
  const currentWorld = worlds.find(
    (w: JourneyWorld) => w.id === character.position?.world_id,
  );
  const currentLevel = currentWorld?.towns
    .flatMap((t) => t.levels)
    .find((l: JourneyLevel) => l.id === character.position?.level_id);

  // Gather today's activities
  const todayReviews = state.today?.reviews || [];
  const todayPractice = state.today?.practice || [];
  const todayChallenge = state.today?.challenge;
  const todayRole = state.today?.role_activity;

  return (
    <div className="min-h-screen bg-gradient-to-b from-[var(--pp-canvas)] to-white">
      {/* ── Header: Character + Stats ── */}
      <header className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b border-border">
        <div className="mx-auto max-w-[800px] px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <PlayerCharacter
              state={celebrate ? "mastery" : currentLevel ? "discovering" : "idle"}
              titleEmoji={character.title_emoji}
              size="md"
            />
            <div>
              <div className="text-sm font-bold">{character.title} Lv.{character.level}</div>
              <div className="text-[11px] text-text-muted">{currentWorld?.title ?? "Your Journey"}</div>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <span className="flex items-center gap-1 text-orange-500 font-semibold">
              <Flame className="w-3.5 h-3.5" /> {stats.streak}
            </span>
            <span className="flex items-center gap-1 text-yellow-500 font-semibold">
              <Coins className="w-3.5 h-3.5" /> {stats.coins}
            </span>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-[800px] px-4 py-6 space-y-6">
        {/* ═══ TODAY SECTION ═══ */}
        <section>
          <h2 className="text-xs font-mono uppercase tracking-widest text-text-muted mb-3 flex items-center gap-2">
            <Target className="w-3.5 h-3.5" /> Today
          </h2>

          <div className="space-y-3">
            {/* ── Primary Action: Continue Lesson ── */}
            {currentLevel && (
              <ContinueCard
                level={currentLevel}
                world={currentWorld!}
                character={character.state as CharacterState}
                titleEmoji={character.title_emoji}
                onContinue={() => handleContinue(currentLevel, currentWorld!.id)}
              />
            )}

            {/* ── SRS Reviews ── */}
            {todayReviews.length > 0 && (
              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                className="rounded-xl border border-amber-200 bg-amber-50/50 p-4"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-bold text-amber-900 flex items-center gap-2">
                    <Sparkles className="w-4 h-4" /> Review
                  </h3>
                  <span className="text-[10px] text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">
                    {todayReviews.length} due
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {todayReviews.slice(0, 5).map((r, i) => (
                    <span key={i} className="text-xs bg-white rounded-lg px-3 py-1.5 border border-amber-200 text-amber-900 font-medium">
                      {String(r.skill_id ?? r.problem_id ?? "Review").replace(/_/g, " ")}
                    </span>
                  ))}
                  {todayReviews.length > 5 && (
                    <span className="text-xs text-amber-600 self-center">+{todayReviews.length - 5} more</span>
                  )}
                </div>
              </motion.div>
            )}

            {/* ── Role Activity ── */}
            {todayRole && (
              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.1 }}
                className="rounded-xl border border-primary/20 bg-primary/5 p-4"
              >
                <div className="flex items-center gap-3">
                  <Brain className="w-5 h-5 text-primary shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-text-primary">{todayRole.title}</div>
                    <div className="text-[11px] text-text-muted">{todayRole.description || "Role-specific practice"}</div>
                  </div>
                  <button className="text-xs text-primary font-medium shrink-0">Start →</button>
                </div>
              </motion.div>
            )}

            {/* ── Challenge ── */}
            {todayChallenge && (
              <motion.div
                initial={{ y: 10, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.15 }}
                className="rounded-xl border border-purple-200 bg-purple-50/50 p-4"
              >
                <div className="flex items-center gap-3">
                  <Swords className="w-5 h-5 text-purple-600 shrink-0" />
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-text-primary">{todayChallenge.title}</div>
                    <div className="text-[11px] text-text-muted">{todayChallenge.description || "Optional challenge"}</div>
                  </div>
                  <span className="text-[10px] text-purple-600 font-medium bg-purple-100 px-2 py-0.5 rounded-full shrink-0">
                    +{todayChallenge.xp_reward} XP
                  </span>
                </div>
              </motion.div>
            )}
          </div>
        </section>

        {/* ═══ CURRENT WORLD PROGRESS ═══ */}
        {currentWorld && (
          <section>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xs font-mono uppercase tracking-widest text-text-muted flex items-center gap-2">
                <Map className="w-3.5 h-3.5" /> {currentWorld.title}
              </h2>
              <span className="text-xs text-text-muted font-medium">
                {currentWorld.towns.reduce((s, t) => s + t.levels.filter((l) => l.status === "completed").length, 0)}
                /{currentWorld.towns.reduce((s, t) => s + t.levels.length, 0)} complete
              </span>
            </div>

            <div className="relative pl-6">
              {/* Vertical spine */}
              <div className="absolute left-[18px] top-1 bottom-1 w-[2px] bg-border rounded-full" />

              {currentWorld.towns.map((town) => {
                const townComplete = town.levels.every((l) => l.status === "completed");
                return (
                  <div key={town.id} className="mb-6 last:mb-0">
                    <div className="text-[11px] font-mono uppercase tracking-widest text-text-muted mb-2 flex items-center gap-2">
                      {town.title}
                      {townComplete && <CheckCircle2 className="w-3 h-3 text-emerald-500" />}
                    </div>
                    <div className="space-y-2">
                      {town.levels.map((lvl) => {
                        const isHere = character.position?.level_id === lvl.id;
                        return (
                          <LevelNode
                            key={lvl.id}
                            level={lvl}
                            isCharacterHere={isHere}
                            onSelect={() => lvl.status !== "locked" && handleContinue(lvl, currentWorld.id)}
                          />
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        )}

        {/* ═══ OTHER WORLDS (COLLAPSED) ═══ */}
        {worlds.length > 1 && (
          <section>
            <button
              onClick={() => setShowAllWorlds(!showAllWorlds)}
              className="flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-text-muted hover:text-text-primary transition-colors"
            >
              <ChevronDown className={`w-3.5 h-3.5 transition-transform ${showAllWorlds ? "rotate-180" : ""}`} />
              {showAllWorlds ? "Hide" : "Show"} Other Worlds
            </button>

            <AnimatePresence>
              {showAllWorlds && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden mt-4 space-y-6"
                >
                  {worlds
                    .filter((w: JourneyWorld) => w.id !== character.position?.world_id)
                    .map((world: JourneyWorld) => (
                      <WorldSummary key={world.id} world={world} />
                    ))}
                </motion.div>
              )}
            </AnimatePresence>
          </section>
        )}
      </main>

      {/* ── Level player overlay ── */}
      <AnimatePresence>
        {activeLevel && activeWorldId && (
          <LevelPlayer
            worldId={activeWorldId}
            level={activeLevel}
            onClose={handleCloseLevel}
            onMastered={handleLevelMastered}
          />
        )}
      </AnimatePresence>

      {/* ── Celebration overlay ── */}
      <Celebration show={celebrate} xp={celebrateXp} onComplete={() => setCelebrate(false)} />
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════ */

function ContinueCard({ level, world, character, titleEmoji, onContinue }: {
  level: JourneyLevel; world: JourneyWorld; character: CharacterState; titleEmoji: string; onContinue: () => void;
}) {
  return (
    <div className="rounded-2xl border border-primary/20 bg-gradient-to-br from-primary/5 to-emerald-500/5 p-5 shadow-sm">
      <div className="flex items-start gap-4">
        <PlayerCharacter state={character} titleEmoji={titleEmoji} size="lg" />
        <div className="flex-1 min-w-0">
          <div className="text-[11px] font-mono uppercase tracking-widest text-primary/70">
            {world.title}
          </div>
          <h3 className="text-lg font-bold leading-tight mt-0.5">{level.icon} {level.title}</h3>
          <p className="text-sm text-text-muted mt-1">
            {level.concept} · <span className="text-yellow-600 font-medium">+{level.xp} XP</span>
          </p>
          {level.mastery > 0 && (
            <div className="mt-2">
              <div className="h-1.5 bg-zinc-100 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${level.mastery}%` }}
                  className="h-full bg-gradient-to-r from-primary to-emerald-400 rounded-full"
                />
              </div>
            </div>
          )}
        </div>
      </div>
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onContinue}
        className="mt-4 w-full rounded-xl bg-primary hover:bg-primary-dark text-white font-semibold py-3.5 flex items-center justify-center gap-2 min-h-[48px]"
      >
        <Zap className="w-4 h-4" />
        {level.attempts > 0 ? "Try Again" : "Continue"}
        <ChevronRight className="w-4 h-4" />
      </motion.button>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════ */

function LevelNode({ level, isCharacterHere, onSelect }: {
  level: JourneyLevel; isCharacterHere: boolean; onSelect: () => void;
}) {
  const isCompleted = level.status === "completed";
  const isLocked = level.status === "locked";
  const isCurrent = level.status === "current" || isCharacterHere;

  return (
    <motion.button
      whileHover={!isLocked ? { x: 4 } : {}}
      whileTap={!isLocked ? { scale: 0.98 } : {}}
      onClick={onSelect}
      disabled={isLocked}
      className={`relative flex items-center gap-3 w-full rounded-lg border px-3 py-2.5 text-left transition-all min-h-[48px]
        ${isLocked ? "opacity-40 cursor-not-allowed border-border bg-zinc-50/50" : ""}
        ${isCurrent ? "border-primary bg-primary/5 shadow-sm" : ""}
        ${isCompleted ? "border-emerald-200 bg-emerald-50/30" : ""}
        ${!isLocked && !isCurrent && !isCompleted ? "border-border bg-white hover:border-primary/30" : ""}
      `}
    >
      <div className={`absolute -left-[22px] top-1/2 -translate-y-1/2 flex h-6 w-6 items-center justify-center rounded-full border-2 text-[10px]
        ${isCompleted ? "bg-emerald-500 border-emerald-500 text-white" : ""}
        ${isCurrent ? "bg-primary border-primary text-white animate-pulse" : ""}
        ${isLocked ? "bg-zinc-200 border-zinc-300" : ""}
        ${!isCompleted && !isCurrent && !isLocked ? "bg-white border-zinc-300" : ""}
      `}>
        {isCompleted ? <CheckCircle2 className="w-3 h-3" /> :
         isLocked ? <Lock className="w-2.5 h-2.5 text-zinc-400" /> :
         isCurrent ? <Star className="w-3 h-3" /> :
         <span>{level.order}</span>}
      </div>
      <div className="flex h-8 w-8 items-center justify-center rounded-lg text-sm shrink-0 bg-zinc-100">
        {level.icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className={`text-sm font-semibold leading-tight ${level.kind === "boss" ? "text-amber-700" : ""}`}>
          {level.title} {level.kind === "boss" && "🐉"}
        </div>
        <div className="text-[10px] text-text-muted">{level.concept} · +{level.xp} XP</div>
      </div>
      {isCharacterHere && <PlayerCharacter state="idle" size="sm" />}
    </motion.button>
  );
}

/* ═══════════════════════════════════════════════════════════════════ */

function WorldSummary({ world }: { world: JourneyWorld }) {
  const total = world.towns.reduce((s, t) => s + t.levels.length, 0);
  const done = world.towns.reduce((s, t) => s + t.levels.filter((l) => l.status === "completed").length, 0);
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;
  const isLocked = world.status === "locked";

  return (
    <div className={`rounded-xl border p-4 ${isLocked ? "opacity-40 border-border bg-zinc-50" : "border-border bg-white"}`}>
      <div className="flex items-center gap-3">
        <span className="text-xl">{world.icon}</span>
        <div className="flex-1 min-w-0">
          <div className="text-sm font-bold">{world.title}</div>
          <div className="text-[11px] text-text-muted">{world.subtitle}</div>
        </div>
        <div className="text-right shrink-0">
          <div className="text-sm font-bold">{pct}%</div>
          <div className="text-[10px] text-text-muted">{done}/{total}</div>
        </div>
      </div>
      <div className="mt-2 h-1.5 bg-zinc-100 rounded-full overflow-hidden">
        <div className="h-full bg-primary rounded-full transition-all" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
