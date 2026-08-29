import { useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Flame, Map, ChevronRight, Star, Lock, CheckCircle2,
  Zap, Trophy, Coins, RotateCcw, Sparkles,
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
      <div className="min-h-[80vh] flex flex-col items-center justify-center gap-4 bg-[var(--pp-canvas)]">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
          className="h-12 w-12 rounded-full border-3 border-primary/20 border-t-primary"
        />
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-sm text-text-muted"
        >
          Loading your journey…
        </motion.p>
      </div>
    );
  }

  if (isError || !state) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center gap-4 bg-[var(--pp-canvas)] px-6 text-center">
        <p className="text-lg font-semibold text-text-primary">Journey unavailable</p>
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

  return (
    <div className="min-h-screen bg-gradient-to-b from-[var(--pp-canvas)] to-white">
      {/* ── Hero: Character + Stats ── */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-emerald-500/5" />
        <div className="relative mx-auto max-w-[800px] px-4 pt-6 pb-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ type: "spring", damping: 15 }}
              >
                <PlayerCharacter
                  state={celebrate ? "mastery" : currentLevel ? "discovering" : "idle"}
                  titleEmoji={character.title_emoji}
                  size="lg"
                />
              </motion.div>
              <div>
                <motion.h1
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  className="text-lg font-bold text-text-primary"
                >
                  {currentWorld?.title ?? "Your Journey"}
                </motion.h1>
                <motion.p
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.1 }}
                  className="text-xs text-text-muted"
                >
                  {currentWorld?.subtitle ?? "Learn. Practice. Master."}
                </motion.p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <StatBadge icon={<Flame className="w-3.5 h-3.5" />} value={stats.streak} color="text-orange-500" />
              <StatBadge icon={<Coins className="w-3.5 h-3.5" />} value={stats.coins} color="text-yellow-500" />
              <StatBadge icon={<Trophy className="w-3.5 h-3.5" />} value={character.level} color="text-primary" />
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-[800px] px-4 pb-24">
        {/* ── SRS reviews due ── */}
        <AnimatePresence>
          {state.today && Array.isArray(state.today.reviews) && state.today.reviews.length > 0 && (
            <motion.div
              initial={{ y: -10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="mb-6"
            >
              <ReviewsDue reviews={state.today.reviews} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Continue CTA ── */}
        {currentLevel && (
          <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="mb-8"
          >
            <ContinueCard
              level={currentLevel}
              world={currentWorld!}
              character={character.state as CharacterState}
              titleEmoji={character.title_emoji}
              onContinue={() => handleContinue(currentLevel, currentWorld!.id)}
            />
          </motion.div>
        )}

        {/* ── World Map ── */}
        <section>
          <motion.h2
            initial={{ x: -10, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="text-xs font-mono uppercase tracking-widest text-text-muted mb-6 flex items-center gap-2"
          >
            <Map className="w-3.5 h-3.5" /> Your Path
          </motion.h2>
          <div className="space-y-12">
            {worlds.map((world: JourneyWorld, wIdx: number) => (
              <motion.div
                key={world.id}
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 0.1 * wIdx }}
              >
                <WorldPath
                  world={world}
                  characterPosition={character.position}
                  onSelectLevel={(lvl) => handleContinue(lvl, world.id)}
                />
              </motion.div>
            ))}
          </div>
        </section>
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
      <Celebration
        show={celebrate}
        xp={celebrateXp}
        onComplete={() => setCelebrate(false)}
      />
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────── */

function StatBadge({ icon, value, color }: { icon: React.ReactNode; value: number; color: string }) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      className={`flex items-center gap-1 ${color} bg-white rounded-full px-2.5 py-1 shadow-sm border border-border text-xs font-semibold`}
    >
      {icon}
      <span>{value}</span>
    </motion.div>
  );
}

/* ─────────────────────────────────────────────────────────────────── */

interface ContinueCardProps {
  level: JourneyLevel;
  world: JourneyWorld;
  character: CharacterState;
  titleEmoji: string;
  onContinue: () => void;
}

function ContinueCard({ level, world, character, titleEmoji, onContinue }: ContinueCardProps) {
  return (
    <div className="relative rounded-2xl bg-gradient-to-br from-primary/5 via-white to-emerald-500/5 border border-primary/20 p-5 shadow-md overflow-hidden">
      <div className="absolute top-0 right-0 w-24 h-24 bg-primary/5 rounded-full -translate-y-8 translate-x-8" />
      <div className="relative flex items-start gap-4">
        <PlayerCharacter state={character} titleEmoji={titleEmoji} size="lg" />
        <div className="flex-1 min-w-0">
          <div className="text-[11px] font-mono uppercase tracking-widest text-primary/70">
            {world.title} · Next up
          </div>
          <h3 className="text-lg font-bold leading-tight mt-0.5">
            {level.icon} {level.title}
          </h3>
          <p className="text-sm text-text-muted mt-1">
            {level.concept} · <span className="text-yellow-600 font-medium">+{level.xp} XP</span>
          </p>
          {level.mastery > 0 && (
            <div className="mt-2">
              <div className="flex items-center justify-between text-[10px] text-text-muted mb-0.5">
                <span>Mastery</span>
                <span>{level.mastery}%</span>
              </div>
              <div className="h-1.5 bg-zinc-100 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${level.mastery}%` }}
                  transition={{ duration: 0.8, ease: "easeOut" }}
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
        className="relative mt-4 w-full rounded-xl bg-gradient-to-r from-primary to-primary-dark hover:shadow-lg text-white font-semibold py-3.5 px-4 flex items-center justify-center gap-2 transition-all focus:outline-none focus:ring-2 focus:ring-primary/40 min-h-[48px]"
      >
        <Zap className="w-4 h-4" />
        {level.attempts > 0 ? "Try Again" : "Continue"}
        <ChevronRight className="w-4 h-4" />
      </motion.button>
      {level.attempts > 0 && (
        <p className="text-xs text-text-muted mt-2 text-center flex items-center justify-center gap-1">
          <RotateCcw className="w-3 h-3" />
          Attempt {level.attempts + 1}
        </p>
      )}
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────── */

interface WorldPathProps {
  world: JourneyWorld;
  characterPosition: { world_id: string; town_id: string; level_id: string } | null;
  onSelectLevel: (level: JourneyLevel) => void;
}

function WorldPath({ world, characterPosition, onSelectLevel }: WorldPathProps) {
  const isWorldActive = characterPosition?.world_id === world.id;
  const totalLevels = world.towns.reduce((s, t) => s + t.levels.length, 0);
  const completedLevels = world.towns.reduce(
    (s, t) => s + t.levels.filter((l) => l.status === "completed").length, 0,
  );
  const townMastery = totalLevels > 0 ? Math.round((completedLevels / totalLevels) * 100) : 0;

  return (
    <div className="relative">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xl">{world.icon}</span>
          <h3 className="text-sm font-bold">{world.title}</h3>
          {world.status === "completed" && (
            <motion.span
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              className="text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full flex items-center gap-1"
            >
              <CheckCircle2 className="w-3 h-3" /> Complete
            </motion.span>
          )}
        </div>
        <span className="text-xs text-text-muted font-medium">{townMastery}%</span>
      </div>

      <div className="relative pl-8">
        <div className="absolute left-[22px] top-2 bottom-2 w-[2px] bg-border rounded-full" />
        <motion.div
          initial={{ height: 0 }}
          animate={{ height: `${townMastery}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
          className="absolute left-[22px] top-2 w-[2px] bg-gradient-to-b from-primary to-emerald-400 rounded-full"
          style={{ maxHeight: "calc(100% - 16px)" }}
        />

        {world.towns.map((town) => (
          <div key={town.id} className="mb-8 last:mb-0">
            <div className="text-[11px] font-mono uppercase tracking-widest text-text-muted mb-3 pl-1">
              {town.title}
            </div>
            <div className="space-y-3">
              {town.levels.map((lvl, idx) => {
                const isHere = isWorldActive && characterPosition?.level_id === lvl.id;
                return (
                  <motion.div
                    key={lvl.id}
                    initial={{ x: -10, opacity: 0 }}
                    animate={{ x: 0, opacity: 1 }}
                    transition={{ delay: idx * 0.05 }}
                  >
                    <LevelNode
                      level={lvl}
                      isCharacterHere={isHere}
                      onSelect={() => lvl.status !== "locked" && onSelectLevel(lvl)}
                    />
                  </motion.div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────────── */

interface LevelNodeProps {
  level: JourneyLevel;
  isCharacterHere: boolean;
  onSelect: () => void;
}

function LevelNode({ level, isCharacterHere, onSelect }: LevelNodeProps) {
  const isCompleted = level.status === "completed";
  const isLocked = level.status === "locked";
  const isCurrent = level.status === "current" || isCharacterHere;

  return (
    <motion.button
      whileHover={!isLocked ? { scale: 1.02, x: 4 } : {}}
      whileTap={!isLocked ? { scale: 0.98 } : {}}
      onClick={onSelect}
      disabled={isLocked}
      className={`relative flex items-center gap-3 w-full rounded-xl border px-4 py-3 text-left transition-all min-h-[56px] focus:outline-none focus:ring-2 focus:ring-primary/30 group
        ${isLocked ? "opacity-40 cursor-not-allowed border-border bg-zinc-50/50" : ""}
        ${isCurrent ? "border-primary bg-primary/5 shadow-md ring-1 ring-primary/20" : ""}
        ${isCompleted ? "border-emerald-200 bg-emerald-50/30" : ""}
        ${!isLocked && !isCurrent && !isCompleted ? "border-border bg-white hover:border-primary/30 hover:shadow-sm" : ""}
      `}
    >
      <div
        className={`absolute -left-[26px] top-1/2 -translate-y-1/2 flex h-7 w-7 items-center justify-center rounded-full border-2 text-xs shadow-sm
          ${isCompleted ? "bg-emerald-500 border-emerald-500 text-white" : ""}
          ${isCurrent ? "bg-primary border-primary text-white animate-pulse" : ""}
          ${isLocked ? "bg-zinc-200 border-zinc-300" : ""}
          ${!isCompleted && !isCurrent && !isLocked ? "bg-white border-zinc-300 group-hover:border-primary/40" : ""}
        `}
      >
        {isCompleted ? <CheckCircle2 className="w-3.5 h-3.5" /> :
         isLocked ? <Lock className="w-3 h-3 text-zinc-400" /> :
         isCurrent ? <Star className="w-3.5 h-3.5" /> :
         <span className="text-[10px]">{level.order}</span>}
      </div>

      <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg text-base
        ${isCompleted ? "bg-emerald-100" : isCurrent ? "bg-primary/10" : "bg-zinc-100 group-hover:bg-primary/5"}
      `}>
        {level.icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className={`text-sm font-semibold leading-tight ${level.kind === "boss" ? "text-amber-700" : ""}`}>
          {level.title}
          {level.kind === "boss" && <span className="ml-1 text-amber-500">🐉</span>}
        </div>
        <div className="text-[11px] text-text-muted flex items-center gap-2">
          <span>{level.concept}</span>
          <span className="text-yellow-600 font-medium">+{level.xp} XP</span>
          {isCompleted && <span className="text-emerald-600">✓</span>}
        </div>
      </div>
      {isCharacterHere ? (
        <motion.div
          animate={{ y: [0, -3, 0] }}
          transition={{ repeat: Infinity, duration: 1.5 }}
        >
          <PlayerCharacter state="idle" size="sm" />
        </motion.div>
      ) : isCompleted && level.mastery > 0 ? (
        <span className="text-xs text-emerald-600 font-bold">{level.mastery}%</span>
      ) : null}
    </motion.button>
  );
}

/* ─────────────────────────────────────────────────────────────────── */

interface ReviewsDueProps {
  reviews: Array<Record<string, unknown>>;
}

function ReviewsDue({ reviews }: ReviewsDueProps) {
  return (
    <div className="rounded-2xl border border-amber-200 bg-gradient-to-r from-amber-50 to-orange-50 p-4 shadow-sm">
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-sm font-bold text-amber-900 flex items-center gap-2">
          <Sparkles className="w-4 h-4" /> Reviews due
        </h3>
        <span className="text-xs text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">{reviews.length}</span>
      </div>
      <p className="text-xs text-amber-800 mb-3">
        Strengthen what you're forgetting — quick recall before new material.
      </p>
      <div className="space-y-1.5">
        {reviews.slice(0, 3).map((r, i) => (
          <div key={i} className="flex items-center justify-between text-xs bg-white/60 rounded-lg px-3 py-2">
            <span className="text-amber-900 truncate font-medium">
              {String(r.skill_id ?? r.problem_id ?? "Review")}
            </span>
            <span className="text-amber-600 shrink-0 ml-2">
              {r.is_due ? "due now" : "scheduled"}
            </span>
          </div>
        ))}
        {reviews.length > 3 && (
          <div className="text-xs text-amber-700 text-center">
            +{reviews.length - 3} more
          </div>
        )}
      </div>
    </div>
  );
}
