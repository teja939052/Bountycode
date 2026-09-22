import { useState, useCallback, useEffect, useRef, useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence, useReducedMotion } from "framer-motion";
import {
  Flame, Map, ChevronRight, Star, Lock, CheckCircle2,
  Sparkles, ChevronDown, RotateCcw,
  Target, Brain, Swords, Play,
} from "lucide-react";
import { useQueryClient, useQuery } from "@tanstack/react-query";
import { useJourneyState, type JourneyWorld, type JourneyLevel } from "../hooks/useJourneyState";
import { useGamificationProfile } from "../hooks/useGamificationProfile";
import useAuthStore from "../store/authStore";
import { PlayerCharacter } from "../components/journey/PlayerCharacter";
import { LevelPlayer } from "../components/journey/LevelPlayer";
import VoyagePath from "../components/journey/VoyagePath";
import CampfireReview from "../components/journey/CampfireReview";
import LevelNode from "../components/journey/LevelNode";
import BadgeCard from "../components/journey/BadgeCard";
import ResultBanner from "../components/journey/ResultBanner";
import WorldSummary from "../components/journey/WorldSummary";
import { useMapState } from "../hooks/useMapState";
import { api } from "../services/api";
import { API_BASE } from "../services/api/request";

interface MapVoyageSectionProps {
  voyageWorld: string | undefined;
  setVoyageWorld: (id: string | undefined) => void;
  reduceMotion: boolean;
  user: { id?: string } | null;
  setCampfireOpen: (open: boolean) => void;
  setActiveLevel: (level: JourneyLevel | null) => void;
  activeLevelRecovered: React.MutableRefObject<boolean>;
  setActiveWorldId: (id: string | null) => void;
}

function MapVoyageSection({
  voyageWorld,
  setVoyageWorld,
  reduceMotion,
  user,
  setCampfireOpen,
  setActiveLevel,
  activeLevelRecovered,
  setActiveWorldId,
}: MapVoyageSectionProps) {
  const { data: map } = useMapState(voyageWorld);
  if (!map || !map.nodes?.length) return null;
  const worlds = map.all_worlds ?? [];
  const voyageDone = worlds.reduce((s, w) => s + (w.done || 0), 0);
  const voyageTotal = worlds.reduce((s, w) => s + (w.total || 0), 0);
  const voyagePct = voyageTotal > 0 ? Math.round((voyageDone / voyageTotal) * 100) : 0;
  const clearedWorlds = worlds.filter((w) => w.status === "completed");
  return (
    <section aria-label="Voyage chart">
      <div className="mb-3 flex items-center gap-3 rounded-2xl border border-default bg-card px-4 py-2.5">
        <span aria-hidden>🗺️</span>
        <div className="flex-1 min-w-0">
          <div className="flex items-baseline justify-between text-xs">
            <span className="font-semibold text-primary">Voyage progress</span>
            <span className="font-mono text-muted">{voyageDone}/{voyageTotal} · {voyagePct}%</span>
          </div>
          <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-black/5">
            <motion.div
              className="h-full rounded-full bg-accent-primary"
              initial={reduceMotion ? false : { width: 0 }}
              animate={{ width: `${voyagePct}%` }}
              transition={{ type: "spring", stiffness: 90, damping: 22 }}
            />
          </div>
        </div>
      </div>
      {clearedWorlds.length > 0 && user?.id && (
        <BadgeCard userId={user.id} cleared={clearedWorlds} />
      )}
      {worlds.length > 1 && (
        <div className="mb-3 flex gap-2 overflow-x-auto pb-1" role="tablist" aria-label="Worlds">
          {worlds.map((w) => {
            const selected = (voyageWorld ?? map.world?.id) === w.id;
            const locked = w.status === "locked";
            const icon = w.status === "completed" ? "✅" : w.status === "locked" ? "🔒" : w.status === "active" ? "⛵" : "🗺️";
            return (
              <button
                key={w.id}
                role="tab"
                aria-selected={selected}
                disabled={locked}
                title={locked ? "Clear the previous world first" : `${w.adventure_name} · ${w.done}/${w.total}`}
                onClick={() => setVoyageWorld(w.id)}
                className={`flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-semibold ${
                  selected
                    ? "border-accent-primary/40 bg-accent-primary/10 text-accent-primary"
                    : locked
                      ? "border-default bg-card text-muted"
                      : "border-default bg-card text-secondary hover:border-accent-primary/30"
                }`}
              >
                <span aria-hidden>{icon}</span>
                {w.adventure_name}
                <span className="opacity-70">{w.done}/{w.total}</span>
              </button>
            );
          })}
        </div>
      )}
      <VoyagePath
        key={map.world?.id ?? "world"}
        map={map}
        onCampfire={() => setCampfireOpen(true)}
        onAdvance={(node) => {
          setActiveLevel({
            id: node.level_id,
            title: node.title,
            icon: node.is_boss ? "👹" : "⚔️",
            kind: node.is_boss ? "boss" : "level",
            order: (map.character?.node_index as number) ?? 0,
            concept: node.title,
            canonical_skill: "",
            status: "current",
            mastery: Math.round(node.best_score),
            attempts: node.attempts,
            diamonds: node.diamonds,
            recovered: node.recovered === true,
          });
          activeLevelRecovered.current = node.recovered === true;
          setActiveWorldId(map.world?.id ?? "foundations");
        }}
      />
    </section>
  );
}

export default function JourneyPage() {
  const { data: state, isLoading, isError } = useJourneyState();
  const reduceMotion = useReducedMotion();
  const [activeLevel, setActiveLevel] = useState<JourneyLevel | null>(null);
  const [activeWorldId, setActiveWorldId] = useState<string | null>(null);
  const [banner, setBanner] = useState<{
    diamonds: number; stars?: number; combo?: number; streakMult?: number;
    critical?: boolean; recovered?: boolean;
  } | null>(null);
  const [showAllWorlds, setShowAllWorlds] = useState(false);

  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const user = useAuthStore((s) => s.user);

  const refreshMap = useCallback(() => {
    // Ship position is server-computed: refetch the map after any level
    // closes so a retry/return can never show a stale position.
    void queryClient.invalidateQueries({ queryKey: ["map", "state"] });
  }, [queryClient]);

  const handleContinue = useCallback((level: JourneyLevel, worldId: string) => {
    setActiveLevel(level);
    setActiveWorldId(worldId);
  }, []);

  const handleCloseLevel = useCallback(() => {
    setActiveLevel(null);
    setActiveWorldId(null);
    refreshMap();
  }, [refreshMap]);

  const handleLevelMastered = useCallback((diamonds: number, detail?: {
    stars?: number; reward?: Record<string, unknown>; xp_nominal?: number;
  }) => {
    setActiveLevel(null);
    setActiveWorldId(null);
    // One primary confirmation per event (juice standard): the result
    // banner renders the canonical award straight from the complete
    // response — stars, Diamonds, combo/streak/crit. No second fetch, no math.
    const reward = detail?.reward ?? {};
    setBanner({
      diamonds,
      stars: typeof detail?.stars === "number" ? detail.stars : undefined,
      combo: typeof reward.combo === "number" ? reward.combo : 0,
      streakMult: typeof reward.streak_multiplier === "number" ? reward.streak_multiplier : 1,
      critical: reward.critical_hit === true,
      recovered: activeLevelRecovered.current,
    });
    refreshMap();
  }, [refreshMap]);

  const [campfireOpen, setCampfireOpen] = useState(false);
  // Whether the level just sent to LevelPlayer was a fought-back recovery
  // (map node carried the recovered ring). Read once at mastery time.
  const activeLevelRecovered = useRef(false);

  const [voyageWorld, setVoyageWorld] = useState<string | undefined>(undefined);

  const [patternReadiness, setPatternReadiness] = useState<{
    patternId: string;
    masteryPercent: number;
    totalQuestions: number;
    solvedCount: number;
    nextPattern: string | null;
    companyReadiness: {
      overallPercent: number;
      sections: string[];
      nextUpId: string | null;
      weakestSection: string | null;
      weakestTitle: string | null;
    } | null;
  }>({
    patternId: "sliding-window",
    masteryPercent: 0,
    totalQuestions: 0,
    solvedCount: 0,
    nextPattern: null,
    companyReadiness: null,
  });

  const [mockInfluence, setMockInfluence] = useState<{
    totalScore: number;
    passingScore: number;
    passed: boolean;
    company: string;
  } | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await api.questions.getPatternReadiness("sliding-window");
        setPatternReadiness(res);
        setCompanyReadiness({
          overallPercent: res.masteryPercent,
          sections: ["sliding-window", "two-pointers", "binary-search", "hashing", "strings"].slice(0, 3),
          nextUpId: res.nextPattern || null,
          weakestSection: "min-swaps-group-ones",
          weakestTitle: "Min swaps to gather ones",
        });
      } catch (e) {
        // 401 or network error — keep defaults; UI falls back gracefully
      }
    })();
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem("mock_completion_TCS");
    if (stored) {
      const data = JSON.parse(stored);
      setMockInfluence({
        totalScore: data.total_score,
        passingScore: data.passing_score,
        passed: data.passed,
        company: data.company,
      });
      localStorage.removeItem("mock_completion_TCS");
    }
  }, []);

  const [companyReadiness, setCompanyReadiness] = useState<{
    overallPercent: number;
    sections: string[];
    nextUpId: string | null;
    weakestSection: string | null;
    weakestTitle: string | null;
  }>({
    overallPercent: 0,
    sections: [],
    nextUpId: null,
    weakestSection: null,
    weakestTitle: null,
  });

  const { character, worlds = [], stats } = state || {};
  const currentWorld = worlds.find(
    (w: JourneyWorld) => w.id === character?.position?.world_id,
  );
  const currentLevel = currentWorld?.towns
    ?.flatMap((t) => t.levels)
    ?.find((l: JourneyLevel) => l.id === character?.position?.level_id);

  const { data: worldContent } = useQuery({
    queryKey: ["world", "content", currentWorld?.id],
    queryFn: () => api.journey.getWorldView(currentWorld!.id),
    enabled: !!currentWorld?.id,
    staleTime: 60_000,
  });

  const currentLevelContent = useMemo(() => {
    if (!worldContent?.world?.towns) return null;
    const world = worldContent.world as Record<string, unknown>;
    const towns = world.towns as Array<Record<string, unknown>>;
    for (const town of towns) {
      const levels = town.levels as Array<Record<string, unknown>> | undefined;
      if (!levels) continue;
      const found = levels.find((l) => l.id === currentLevel?.id);
      if (found) return found as Record<string, unknown>;
    }
    return null;
  }, [worldContent, currentLevel?.id]);

  const { data: gp } = useGamificationProfile();

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
        <Link to="/journey" className="text-sm text-primary underline">Back to journey</Link>
      </div>
    );
  }

  const worldLevels = currentWorld?.towns?.flatMap((t) => t.levels) ?? [];
  const clearedLevels = worldLevels.filter((l) => l.status === "completed");
  const lastVictory = [...clearedLevels].sort((a, b) => b.order - a.order)[0] ?? null;
  const trackLabel = state.company
    ? `TRACK · ${state.company.target_role} · ${state.company.target}`.toUpperCase()
    : "TRACK · PLACEMENT PREP";
  const dailyCount = typeof gp?.daily_goal_count === "number" ? gp.daily_goal_count : null;
  const dailyTarget = typeof gp?.daily_goal_target === "number" ? gp.daily_goal_target : null;
  const dailyPct = dailyCount != null && dailyTarget ? Math.min(100, Math.round((dailyCount / dailyTarget) * 100)) : null;
  const rankTitle = (gp?.champion_title as string | undefined) || (gp?.title as string | undefined) || "Unranked";
  const rankEmoji = (gp?.title_emoji as string | undefined) || "🛡️";
  const missionStreak = typeof gp?.streak === "number" ? gp.streak : stats.streak;
  const missionStars = typeof gp?.stars_total === "number" ? gp.stars_total : 0;

  const todayReviews = state.today?.reviews || [];
  const todayPractice = state.today?.practice || [];
  const todayChallenge = state.today?.challenge;
  const todayRole = state.today?.role_activity;

  return (
    <div className="min-h-screen bg-base">
      <main className="mx-auto max-w-[800px] px-4 py-6 space-y-6">
        {/* ═══ V3: TODAY'S MISSION — one question answered: what next? ═══ */}
        <section aria-label="Today's mission" className="rounded-3xl border border-orange-200/60 bg-[#FFF7F2] p-5 shadow-sm">
          <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#E8590C]">⚡ Today's mission</p>
          <h2 className="font-display mt-1 text-xl font-black text-gray-900">
            {(state as any)?.next_action?.title || (currentLevel ? `Continue: ${currentLevel.title}` : "Start your first mission")}
          </h2>
          {(state as any)?.next_action?.reason && (
            <p className="mt-1 font-mono text-[11px] text-gray-500">Why? {(state as any).next_action.reason}</p>
          )}
          {(state as any)?.readiness != null && (
            <p className="mt-1 font-mono text-[11px] text-gray-500">
              🎯 {state.company?.target ?? "Placement"} readiness: {Math.round((state as any).readiness)}%
            </p>
          )}
          <div className="mt-3 flex flex-wrap gap-2">
            {currentLevel && currentWorld && (
              <button
                onClick={() => handleContinue(currentLevel, currentWorld.id)}
                className="flex min-h-[44px] items-center gap-2 rounded-xl bg-[#F4532F] px-5 font-bold text-white shadow-md hover:brightness-105"
              >
                <Play size={15} /> START MISSION →
              </button>
            )}
            <Link to="/practice" className="flex min-h-[44px] items-center rounded-xl border border-black/10 bg-white px-4 text-sm font-semibold text-gray-700">Practice freestyle</Link>
            <Link to="/target" className="flex min-h-[44px] items-center rounded-xl border border-black/10 bg-white px-4 text-sm font-semibold text-gray-700">Change target</Link>
          </div>
        </section>
        {/* ═══ LEVEL MAP header (hybrid) ═══ */}
        <motion.section
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          aria-label="Level map"
          className="relative overflow-hidden rounded-3xl border border-default bg-card p-5 sm:p-7"
        >
          {/* Ambient warmth */}
          <div className="pointer-events-none absolute inset-0" aria-hidden="true">
            <div className="absolute -right-20 -top-20 h-64 w-64 rounded-full bg-orange-200/40 blur-3xl" />
            <div className="absolute -left-20 -bottom-20 h-64 w-64 rounded-full bg-amber-200/40 blur-3xl" />
          </div>

          <div className="relative flex items-start justify-between gap-3">
            <div className="min-w-0">
              <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted">{trackLabel}</p>
              <h1 className="font-display mt-1 text-6xl font-black tracking-tight text-primary sm:text-7xl">
                CHART
              </h1>
              {dailyPct != null && dailyCount != null && dailyTarget ? (
                <div className="mt-3 flex max-w-xs items-center gap-2">
                  <div className="h-2.5 flex-1 overflow-hidden rounded-full bg-black/5">
                    <motion.div
                      className="h-full rounded-full bg-gradient-to-r from-orange-400 to-amber-500"
                      animate={{ width: `${dailyPct}%` }}
                      transition={{ duration: 1, ease: "easeOut" }}
                    />
                  </div>
                  <span className="font-mono text-xs text-muted">
                    {dailyCount}/{dailyTarget} today
                  </span>
                </div>
              ) : (
                <p className="mt-3 font-mono text-xs text-muted">
                  Level {stats.level} · {stats.diamonds.toLocaleString()} Diamonds · {stats.streak} day streak
                </p>
              )}
              <Link to="/target" className="mt-2 inline-block font-mono text-xs font-semibold tracking-widest text-[#E8590C] hover:underline">
                CHANGE TARGET →
              </Link>
            </div>
            <motion.div
              className="flex shrink-0 items-center gap-2 rounded-2xl bg-[#14141B] px-3.5 py-2.5 shadow-sm ring-1 ring-black/5"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            >
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#14141B] text-lg" aria-hidden="true">🛡️</span>
              <span>
                <span className="block font-mono text-[10px] uppercase tracking-widest text-white/60">Rank</span>
                <span className="block text-sm font-black text-white">{rankTitle}</span>
              </span>
            </motion.div>
          </div>

          <div className="mt-5 grid grid-cols-1 gap-4 lg:grid-cols-5">
            {/* Campaign card — the canonical VoyagePath map lives here */}
            <div className="relative overflow-hidden rounded-2xl bg-[#FFF7F2] p-4 shadow-sm ring-1 ring-orange-200/60 lg:col-span-3">
              <div className="mb-2 flex items-baseline justify-between">
                <div>
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-gray-400">
                    Campaign {(currentWorld?.order ?? 0) + 1}
                  </p>
                  <h2 className="font-display text-xl font-black tracking-tight text-gray-900">
                    {(currentWorld?.adventure_name || currentWorld?.title || "Boot Camp").toUpperCase()}
                  </h2>
                </div>
                <span className="font-mono text-[11px] font-semibold text-teal-600">
                  {clearedLevels.length} / {worldLevels.length || "–"} CLEARED
                </span>
              </div>
              <MapVoyageSection
                voyageWorld={voyageWorld}
                setVoyageWorld={setVoyageWorld}
                reduceMotion={reduceMotion}
                user={user}
                setCampfireOpen={setCampfireOpen}
                setActiveLevel={setActiveLevel}
                activeLevelRecovered={activeLevelRecovered}
                setActiveWorldId={setActiveWorldId}
              />
            </div>

            {/* Mission side panels */}
            <div className="flex flex-col gap-4 lg:col-span-2">
              <div className="rounded-2xl border border-orange-100 bg-[#FFF7F2] p-4 shadow-sm">
                <div className="flex items-center justify-between">
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#E8590C]">Active mission</p>
                  <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#14141B] text-white text-xs">
                    &lt;/&gt;
                  </span>
                </div>
                {currentLevel ? (
                  <>
                    <h3 className="font-display mt-1 text-2xl font-black tracking-tight text-gray-900">
                      {currentLevel.title.toUpperCase()}
                    </h3>
                    <p className="mt-1 font-mono text-[11px] uppercase text-gray-500">
                       {currentLevel.kind === "boss" ? "Boss Island" : "Stage"} {currentLevel.order} · {currentLevel.diamonds} Diamonds reward
                    </p>
                    <div className="mt-3 grid grid-cols-3 gap-2 text-center">
                      <div className="rounded-lg bg-white/70 px-2 py-2 ring-1 ring-black/5">
                        <p className="text-base font-black text-gray-900">+{currentLevel.diamonds}</p>
                        <p className="font-mono text-[9px] uppercase text-gray-400">Diamonds</p>
                      </div>
                      <div className="rounded-lg bg-white/70 px-2 py-2 ring-1 ring-black/5">
                        <p className="flex items-center justify-center gap-1 text-base font-black text-gray-900">
                          <Flame size={14} className="text-orange-500" />{missionStreak}
                        </p>
                        <p className="font-mono text-[9px] uppercase text-gray-400">Hearts</p>
                      </div>
                      <div className="rounded-lg bg-white/70 px-2 py-2 ring-1 ring-black/5">
                        <p className="flex items-center justify-center gap-1 text-base font-black text-gray-900">
                          <Star size={14} className="text-amber-500" />x{missionStars}
                        </p>
                        <p className="font-mono text-[9px] uppercase text-gray-400">Combo</p>
                      </div>
                    </div>
                    <button
                      onClick={() => currentWorld && handleContinue(currentLevel, currentWorld.id)}
                      className="mt-3 flex min-h-[48px] w-full items-center justify-center gap-2 rounded-xl bg-[#F4532F] font-bold text-white shadow-md transition hover:brightness-105 active:scale-[0.99]"
                    >
                      <Play size={16} /> BOARD THE ISLAND
                    </button>
                  </>
                ) : (
                  <p className="mt-2 text-sm text-gray-500">All stages clear. New campaigns soon.</p>
                )}
              </div>

              <div className="rounded-2xl bg-white/85 p-4 shadow-sm ring-1 ring-black/5">
                <div className="flex items-center justify-between">
                  <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-gray-400">Latest victory</p>
                  <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#14141B] text-lg">⭐</span>
                </div>
                {lastVictory ? (
                  <>
                    <p className="mt-1 text-2xl font-black text-[#F4532F]">+{lastVictory.diamonds} Diamonds</p>
                    <p className="mt-0.5 text-xs text-gray-500">
                      {lastVictory.title} cleared · mastery {lastVictory.mastery}%
                    </p>
                    {currentLevel && (
                      <p className="mt-1 text-xs text-gray-500">
                        Next unlock: <strong className="text-gray-900">{currentLevel.title}</strong>
                      </p>
                    )}
                  </>
                ) : (
                  <p className="mt-1 text-sm text-gray-500">
                    No victories yet — enter your first stage to start the trail.
                  </p>
                )}
              </div>
            </div>
          </div>
        </motion.section>

        {/* ═══ PRIMARY ACTION: What should I do right now? ═══ */}
        <section>
          {currentLevel ? (
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="rounded-2xl bg-accent-primary/5 border border-accent-primary/20 p-6 shadow-md"
            >
              {/* Journey memory */}
              {currentLevel.attempts > 0 && (
                <div className="text-xs text-muted mb-2 flex items-center gap-1">
                  <RotateCcw className="w-3 h-3" />
                  You left off here. Continue your journey.
                </div>
              )}

              <div className="flex items-start gap-4">
                <PlayerCharacter
                  state={"discovering"}
                  titleEmoji={character.title_emoji}
                  size="lg"
                />
                <div className="flex-1 min-w-0">
                  <div className="text-[11px] font-mono uppercase tracking-widest text-primary/70">
                    {currentWorld?.title} · Level {currentLevel.order}
                  </div>
                  <h2 className="text-xl font-bold leading-tight mt-1">
                    {currentLevel.icon} {currentLevel.title}
                  </h2>
                  <p className="text-sm text-muted mt-1">
                    "{currentLevel.mental_model || currentLevel.concept}"
                  </p>
                  {currentLevel.mastery > 0 && (
                    <div className="mt-3">
                      <div className="flex items-center justify-between text-[10px] text-muted mb-1">
                        <span>Mastery</span>
                        <span>{currentLevel.mastery}%</span>
                      </div>
                      <div className="h-1.5 bg-black/5 rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${currentLevel.mastery}%` }}
                          className="h-full bg-accent-primary rounded-full"
                        />
                      </div>
                    </div>
                  )}
                </div>
              </div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => handleContinue(currentLevel, currentWorld!.id)}
                className="mt-5 w-full rounded-xl bg-accent-primary hover:bg-accent-primary/90 text-white font-bold py-4 flex items-center justify-center gap-2 min-h-[52px] shadow-lg"
              >
                <Play className="w-5 h-5" />
                {currentLevel.attempts > 0 ? "Continue" : "Begin"}
                <ChevronRight className="w-5 h-5" />
              </motion.button>

              {/* Real lesson preview from backend */}
              {currentLevelContent && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="mt-4 rounded-xl border border-border bg-card p-4 space-y-3"
                >
                  <div className="text-[10px] font-mono uppercase tracking-widest text-primary mb-1">Lesson Preview</div>

                  {/* Discover content */}
                  {(currentLevelContent.discover as Record<string, unknown> | undefined)?.prompt && (
                    <div>
                      <div className="text-xs font-semibold text-secondary mb-1">Discover</div>
                      <p className="text-sm text-text-primary">
                        {(currentLevelContent.discover as Record<string, unknown>).prompt as string}
                      </p>
                    </div>
                  )}

                  {/* Mental model */}
                  {currentLevelContent.mental_model && (
                    <div>
                      <div className="text-xs font-semibold text-secondary mb-1">Mental Model</div>
                      <p className="text-sm text-text-primary italic">
                        {currentLevelContent.mental_model as string}
                      </p>
                    </div>
                  )}

                  {/* Code challenge preview */}
                  {(currentLevelContent.code as Record<string, unknown> | undefined)?.prompt && (
                    <div>
                      <div className="text-xs font-semibold text-secondary mb-1">Challenge</div>
                      <p className="text-sm text-text-primary">
                        {(currentLevelContent.code as Record<string, unknown>).prompt as string}
                      </p>
                    </div>
                  )}

                  {/* Predict question */}
                  {currentLevelContent.predict && (
                    <div>
                      <div className="text-xs font-semibold text-secondary mb-1">Predict</div>
                      <p className="text-sm text-text-primary">
                        {(currentLevelContent.predict as Record<string, unknown>).prompt as string}
                      </p>
                    </div>
                  )}
                </motion.div>
              )}

              <div className="mt-2 flex items-center justify-center gap-4 text-[11px] text-muted">
                <span className="flex items-center gap-1">
                  <Flame className="w-3 h-3 text-orange-500" /> {stats.streak} day streak
                </span>
                <span>·</span>
                <span>{currentLevel.diamonds} Diamonds reward</span>
              </div>
            </motion.div>
          ) : (
            <div className="rounded-2xl border border-accent-primary/20 bg-accent-primary/5 p-6 text-center">
              <div className="text-3xl mb-2">🎉</div>
              <h2 className="text-lg font-bold text-primary">All levels complete!</h2>
              <p className="text-sm text-secondary mt-1">You've mastered this world. More coming soon.</p>
            </div>
          )}
        </section>

        {/* ═══ ADVENTURE MAP: the map is home — winding path, ship, fog ═══ */}
        <MapVoyageSection
          voyageWorld={voyageWorld}
          setVoyageWorld={setVoyageWorld}
          reduceMotion={reduceMotion}
          user={user}
          setCampfireOpen={setCampfireOpen}
          setActiveLevel={setActiveLevel}
          activeLevelRecovered={activeLevelRecovered}
          setActiveWorldId={setActiveWorldId}
        />

        {/* ═══ PATTERN PROGRESS + COMPANY READINESS CARDS ═══ */}
        <section className="space-y-4">
          <div className="rounded-2xl border border-default bg-card p-4 shadow-sm">
            <h3 className="text-sm font-mono uppercase tracking-widest text-muted mb-2">Pattern Progress</h3>
            <div className="flex items-baseline gap-2">
              <div>
                <p className="text-[12px] font-medium text-muted">Mastery</p>
                <p className="text-3xl font-bold text-primary">{Math.round(patternReadiness.masteryPercent)}%</p>
              </div>
              <p className="text-[12px] text-muted">/{patternReadiness.totalQuestions}</p>
            </div>
            {patternReadiness.nextPattern && (
              <p className="mt-2 text-sm text-muted">
                {patternReadiness.masteryPercent >= 80 ? (
                  <span className="font-medium text-primary">Ready for {patternReadiness.nextPattern}</span>
                ) : (
                  "Continue practicing."
                )}
              </p>
            )}
            <button
              onClick={() => navigate(`/pattern/${patternReadiness.patternId}`)}
              className="mt-3 w-full rounded-xl bg-accent-primary hover:bg-accent-primary/90 text-white font-bold py-3 flex items-center justify-center gap-2">
              <Play className="w-4 h-4" /> Continue pattern
            </button>
          </div>

          <div className="rounded-2xl border border-default bg-card p-4 shadow-sm">
            <h3 className="text-sm font-mono uppercase tracking-widest text-muted mb-2">Company Readiness</h3>
            <p className="text-[12px] font-medium text-secondary">
              You are {companyReadiness.overallPercent}% ready for {/* company name from track or fallback */}
            </p>
            <p className="text-[10px] text-muted mt-1">
              {companyReadiness.overallPercent > 0 && "Coding pattern readiness reflects your verified pattern mastery progress."}
            </p>
            <p className="text-[10px] text-muted mt-1">
              {companyReadiness.overallPercent > 0 && "Coding pattern readiness reflects your verified pattern mastery progress."}
            </p>
            <p className="text-[10px] text-muted mt-1">
              {companyReadiness.overallPercent > 0 && "Coding pattern readiness reflects your verified pattern mastery progress."}
            </p>
            {companyReadiness.weakestSection && (
              <p className="mt-1 text-[10px] text-muted">
                Weakest: {companyReadiness.weakestTitle}
              </p>
            )}
            <div className="mt-2 flex gap-2">
              <button
                onClick={() => navigate(`/practice?section=${companyReadiness.weakestSection}`)}
                className="flex-1 rounded-xl bg-accent-primary/10 border border-accent-primary/20 text-accent-primary font-small py-2">
                Continue weak section
              </button>
              <button
                onClick={() => navigate(`/mock?company=TCS`)}
                className="flex-1 rounded-xl bg-accent-primary/10 border border-accent-primary/20 text-accent-primary font-small py-2">
                Focused mock
              </button>
              <button
                onClick={() => navigate(`/pattern/${patternReadiness.nextPattern ?? 'sliding-window'}`)}
                className="flex-1 rounded-xl bg-accent-primary/10 border border-accent-primary/20 text-accent-primary font-small py-2">
                Recommended pattern
              </button>
            </div>
          </div>
        </section>
        {(todayReviews.length > 0 || todayRole || todayChallenge) && (
          <section>
            <h2 className="text-xs font-mono uppercase tracking-widest text-muted mb-3 flex items-center gap-2">
              <Target className="w-3.5 h-3.5" /> Also Today
            </h2>
            <div className="space-y-2">
              {todayReviews.length > 0 && (
                <div className="rounded-xl border border-accent-warm/20 bg-accent-warm/5 p-3 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-accent-warm" />
                    <span className="text-sm font-medium text-primary">
                      {todayReviews.length} review{todayReviews.length > 1 ? "s" : ""} due
                    </span>
                  </div>
                  <button
                    onClick={() => setCampfireOpen(true)}
                    className="text-xs text-accent-warm font-medium bg-accent-warm/10 rounded-lg px-3 py-1.5"
                  >
                    Review
                  </button>
                </div>
              )}

              {todayRole && (
                <div className="rounded-xl border border-accent-primary/20 bg-accent-primary/5 p-3 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Brain className="w-4 h-4 text-accent-primary" />
                    <span className="text-sm font-medium text-primary truncate">
                      {todayRole.title}
                    </span>
                  </div>
                  <button className="text-xs text-accent-primary font-medium bg-accent-primary/10 rounded-lg px-3 py-1.5">
                    Start
                  </button>
                </div>
              )}

              {todayChallenge && (
                <div className="rounded-xl border border-accent-secondary/20 bg-accent-secondary/5 p-3 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Swords className="w-4 h-4 text-accent-secondary" />
                    <span className="text-sm font-medium text-primary truncate">
                      {todayChallenge.title}
                    </span>
                  </div>
                  <span className="text-[10px] text-accent-secondary font-medium bg-accent-secondary/10 px-2 py-1 rounded-full">
                    +{todayChallenge.xp_reward} Diamonds
                  </span>
                </div>
              )}
            </div>
          </section>
        )}

        {/* ═══ CURRENT WORLD PROGRESS ═══ */}
        {currentWorld && (
          <section>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xs font-mono uppercase tracking-widest text-muted flex items-center gap-2">
                <Map className="w-3.5 h-3.5" /> {currentWorld.title}
              </h2>
              <span className="text-xs text-muted font-medium">
                {currentWorld.towns.reduce((s, t) => s + t.levels.filter((l) => l.status === "completed").length, 0)}
                /{currentWorld.towns.reduce((s, t) => s + t.levels.length, 0)}
              </span>
            </div>

            <div className="relative pl-6">
              <div className="absolute left-[18px] top-1 bottom-1 w-[2px] bg-default rounded-full" />

              {currentWorld.towns.map((town) => {
                const townComplete = town.levels.every((l) => l.status === "completed");
                // Coddy-style section summary, all derived from the town's
                // own levels (already in state): counts, Diamonds on offer, boss.
                const townDone = town.levels.filter((l) => l.status === "completed").length;
                const townXp = town.levels.reduce((s, l) => s + (l.diamonds || 0), 0);
                const townBoss = town.levels.some((l) => l.kind === "boss");
                const townPct = town.levels.length > 0 ? Math.round((townDone / town.levels.length) * 100) : 0;
                const nextUp = town.levels.find((l) => l.status !== "completed" && l.status !== "locked");
                return (
                  <div key={town.id} className="mb-5 last:mb-0">
                    <button
                      onClick={() => nextUp && handleContinue(nextUp, currentWorld.id)}
                      disabled={!nextUp}
                      className="mb-2 w-full rounded-xl border border-border bg-white px-3 py-2 text-left transition-all hover:border-primary/30 disabled:cursor-default disabled:opacity-80"
                    >
                      <div className="flex items-center gap-2 text-[11px] font-mono uppercase tracking-widest text-text-muted">
                        <span className="truncate">{town.title}</span>
                        {townComplete && <CheckCircle2 className="w-3 h-3 shrink-0 text-emerald-500" />}
                        {townBoss && <span aria-hidden title="Guardian battle inside">🐉</span>}
                      </div>
                      <div className="mt-1 flex items-center gap-2 text-[11px] text-text-muted">
                        <span className="font-semibold">{townDone}/{town.levels.length} lessons</span>
                        <span>·</span>
                        <span>{townXp} Diamonds on offer</span>
                        {nextUp && <span className="ml-auto font-bold text-primary">Start →</span>}
                      </div>
                      <div className="mt-1.5 h-1 overflow-hidden rounded-full bg-zinc-100">
                        <motion.div
                          className="h-full rounded-full bg-emerald-500"
                          initial={reduceMotion ? false : { width: 0 }}
                          animate={{ width: `${townPct}%` }}
                          transition={{ type: "spring", stiffness: 120, damping: 22 }}
                        />
                      </div>
                    </button>
                    <div className="space-y-1.5">
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
              {showAllWorlds ? "Hide" : "Show"} All Worlds
            </button>

            <AnimatePresence>
              {showAllWorlds && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="overflow-hidden mt-4 space-y-3"
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

      <AnimatePresence>
        {activeLevel && activeWorldId && (
          <LevelPlayer
            worldId={activeWorldId}
            level={activeLevel}
            onClose={handleCloseLevel}
            onMastered={handleLevelMastered}
            worldContent={currentLevelContent}
          />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {banner && (
          <ResultBanner data={banner} onDone={() => setBanner(null)} />
        )}
      </AnimatePresence>

      <AnimatePresence>
        {campfireOpen && (
          <CampfireReview
            reviews={(todayReviews as unknown as Array<Record<string, unknown>>).map((r) => ({
              skill_id: typeof r.skill_id === "string" ? r.skill_id : undefined,
              concept_id: typeof r.concept_id === "string" ? r.concept_id : undefined,
              concept_name: typeof r.concept_name === "string" ? r.concept_name : undefined,
              title: typeof r.title === "string" ? r.title : undefined,
            }))}
            onClose={() => setCampfireOpen(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}