import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence, useReducedMotion } from "framer-motion";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Flame, Coins, Lock, Check, ChevronLeft, Trophy,
  Crown, Target, Anchor,
} from "lucide-react";
import { useJourneyState, type JourneyLevel, type JourneyWorld } from "../hooks/useJourneyState";
import { useGamificationProfile } from "../hooks/useGamificationProfile";
import { gamificationApi } from "../services/api/gamification";
import type { LeaderboardEntry } from "../services/api/types";
import { LevelPlayer } from "../components/journey/LevelPlayer";

/* ═══════════════════════════════════════════════════════════════════
   LevelMap — Pirate adventure map: fleets → ports → stages.

   REUSE ONLY, no new systems:
   - Nodes + statuses come from useJourneyState (canonical journey state).
    - Streak/coins/level come from useGamificationProfile (canonical owner).
    - Leaderboard comes from the gamification leaderboard endpoints.
   - Tapping a node routes to the SAME destinations as JourneyPage:
     foundations → /lesson/:id, everything else → LevelPlayer overlay.
   ═══════════════════════════════════════════════════════════════════ */

const LANE = [0, 52, 88, 52, 0, -52, -88, -52];

type NodeStatus = "completed" | "current" | "unlocked" | "locked";

function nodeColors(status: NodeStatus, isBoss: boolean) {
  if (status === "locked") {
    return { bg: "bg-[#E5E5E5]", edge: "border-[#CFCFCF]", icon: "text-[#AFAFAF]" };
  }
  if (isBoss) {
    return { bg: "bg-[#E96A5B]", edge: "border-[#C4503F]", icon: "text-white" };
  }
  return { bg: "bg-[#1E6091]", edge: "border-[#154c7a]", icon: "text-white" };
}

function LevelNode({
  level,
  status,
  laneX,
  isCurrent,
  onSelect,
}: {
  level: JourneyLevel;
  status: NodeStatus;
  laneX: number;
  isCurrent: boolean;
  onSelect: () => void;
}) {
  const reduceMotion = useReducedMotion();
  const isBoss = level.kind === "boss";
  const locked = status === "locked";
  const c = nodeColors(status, isBoss);

  return (
    <div className="relative flex flex-col items-center" style={{ transform: `translateX(${laneX}px)` }}>
      {isCurrent && (
        <motion.div
          initial={reduceMotion ? {} : { opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className={`absolute -top-12 z-10 ${reduceMotion ? "" : "animate-bounce"}`}
        >
          <button
            onClick={onSelect}
            className="rounded-2xl border-2 border-[#1E6091] bg-white px-4 py-2 font-round text-sm font-extrabold tracking-wide text-[#1E6091] shadow-md"
          >
            BOARD
          </button>
          <div className="mx-auto h-3 w-3 rotate-45 border-r-2 border-b-2 border-[#1E6091] bg-white" style={{ marginTop: -8 }} />
        </motion.div>
      )}
      <motion.button
        type="button"
        onClick={onSelect}
        disabled={locked}
        title={locked ? `${level.title} — clear previous stages first` : level.title}
        aria-label={`${level.title} — ${status}`}
        whileTap={locked || reduceMotion ? {} : { scale: 0.92 }}
        className={`relative flex h-[70px] w-[70px] items-center justify-center rounded-full border-b-8 text-2xl transition-transform ${c.bg} ${c.edge} ${
          locked ? "cursor-not-allowed" : "cursor-pointer hover:brightness-110 active:translate-y-1 active:border-b-4"
        } ${isCurrent && !reduceMotion ? "animate-[pulse-ring_2s_ease-out_infinite]" : ""}`}
      >
        {isCurrent && (
          <span className="absolute -inset-2 rounded-full border-4 border-[#1E6091]/40" aria-hidden="true" />
        )}
        {locked ? (
          <Lock size={26} className={c.icon} />
        ) : status === "completed" && !isBoss ? (
          <span className={c.icon} aria-hidden="true">
            <Check size={30} strokeWidth={4} />
          </span>
        ) : isBoss ? (
          <Crown size={28} className={c.icon} />
        ) : (
          <span className="text-[26px] leading-none" aria-hidden="true">{level.icon || "⚓"}</span>
        )}
      </motion.button>
      {status === "completed" && (
        <span className="mt-1.5 rounded-full bg-[#DCFCE7] px-2 py-0.5 font-round text-[11px] font-extrabold text-[#15803D]">
          {level.mastery}%
        </span>
      )}
      {isCurrent && (
        <span className="mt-1.5 max-w-[140px] truncate font-round text-xs font-bold text-[#4B4B4B]">
          {level.title}
        </span>
      )}
    </div>
  );
}

export default function LevelMap() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { data: state, isLoading, isError } = useJourneyState();
  const { data: profile } = useGamificationProfile();
  const { data: board } = useQuery({
    queryKey: ["gamification", "leaderboard", "weekly", "top5"],
    queryFn: () => gamificationApi.getLeaderboard(5, "weekly"),
    staleTime: 60_000,
    retry: 1,
  });
  const { data: myRank } = useQuery({
    queryKey: ["gamification", "leaderboard", "me", "weekly"],
    queryFn: () => gamificationApi.getMyRank("weekly"),
    staleTime: 60_000,
    retry: 1,
  });

  const [activeLevel, setActiveLevel] = useState<JourneyLevel | null>(null);
  const [activeWorldId, setActiveWorldId] = useState<string | null>(null);

  const worlds = state?.worlds ?? [];
  const defaultWorld = state?.character?.position?.world_id ?? worlds[0]?.id;
  const [worldId, setWorldId] = useState<string | null>(null);
  const world: JourneyWorld | undefined =
    worlds.find((w) => w.id === (worldId ?? defaultWorld)) ?? worlds[0];

  const handleSelect = (level: JourneyLevel, wid: string) => {
    if (level.status === "locked") return;
    setActiveLevel(level);
    setActiveWorldId(wid);
  };

  const handleMastered = () => {
    setActiveLevel(null);
    setActiveWorldId(null);
    void queryClient.invalidateQueries({ queryKey: ["journey", "state"] });
  };

  if (isLoading) {
    return (
      <div className="mx-auto max-w-6xl px-4 py-10">
        <div className="flex items-center justify-center gap-6">
          {[0, 1, 2, 3].map((i) => (
            <div key={i} className="h-[70px] w-[70px] animate-pulse rounded-full bg-gray-200" />
          ))}
        </div>
      </div>
    );
  }

  if (isError || !state || !world) {
    return (
      <div className="mx-auto flex min-h-[60vh] max-w-xl flex-col items-center justify-center gap-3 px-6 text-center">
        <p className="font-round text-2xl font-extrabold text-[#4B4B4B]">Chart unavailable</p>
        <p className="text-sm text-gray-500">Your voyage is saved — open the map instead.</p>
        <Link to="/journey" className="font-round rounded-2xl bg-[#1E6091] px-6 py-3 font-extrabold text-white border-b-4 border-[#154c7a]">
          Open chart
        </Link>
      </div>
    );
  }

  const streak = typeof profile?.streak === "number" ? profile.streak : state.stats.streak;
  const coins = typeof profile?.coins === "number" ? profile.coins : state.stats.coins;
  const entries: LeaderboardEntry[] = Array.isArray(board) ? board : [];

  return (
    <div className="min-h-screen bg-white">
      {/* ═══ Top stat bar ═══ */}
      <div className="sticky top-0 z-30 border-b-2 border-[#E5E5E5] bg-white/95 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-center gap-6 px-4 py-3 sm:gap-10">
          <span className="flex items-center gap-1.5 font-round text-lg font-extrabold text-[#FF9600]" title="Day streak">
            <Flame size={22} className="fill-[#FF9600] text-[#FF9600]" />{streak}
          </span>
          <span className="flex items-center gap-1.5 font-round text-lg font-extrabold text-[#1CB0F6]" title="Coins">
            <Coins size={22} className="text-[#1CB0F6]" />{coins}
          </span>
          <span className="hidden items-center gap-1.5 font-round text-lg font-extrabold text-[#CE82FF] sm:flex" title="Level">
            <Target size={22} />{profile?.level ?? state.stats.level}
          </span>
        </div>
      </div>

      {/* ═══ Fleet switcher ═══ */}
      {worlds.length > 1 && (
        <div className="mx-auto flex max-w-6xl gap-2 overflow-x-auto px-4 pt-4" role="tablist" aria-label="Fleets">
          {worlds.map((w) => {
            const selected = w.id === world.id;
            const locked = w.status === "locked";
            const name = w.adventure_name ?? w.title;
            return (
              <button
                key={w.id}
                role="tab"
                aria-selected={selected}
                disabled={locked}
                onClick={() => setWorldId(w.id)}
                className={`flex shrink-0 items-center gap-1.5 rounded-2xl border-2 px-4 py-2 font-round text-sm font-extrabold ${
                  selected
                    ? "border-[#1E6091] bg-[#E8F4FD] text-[#154c7a]"
                    : locked
                    ? "border-[#E5E5E5] bg-white text-[#AFAFAF]"
                    : "border-[#E5E5E5] bg-white text-[#777]"
                }`}
              >
                <span aria-hidden="true">{locked ? "🔒" : w.icon}</span>
                {name}
              </button>
            );
          })}
        </div>
      )}

      <main className="mx-auto grid max-w-6xl grid-cols-1 gap-8 px-4 py-6 lg:grid-cols-[1fr_320px]">
        {/* ═══ Winding sea route ═══ */}
        <div className="relative">
          <div className="pointer-events-none absolute bottom-8 left-1/2 top-8 w-1 -translate-x-1/2 rounded-full bg-[#E5E5E5]" aria-hidden="true" />
          {world.towns
            .slice()
            .sort((a, b) => a.order - b.order)
            .map((town, ti) => (
              <section key={town.id} aria-label={town.title} className="relative mb-10">
                <div className="relative z-10 mx-auto mb-8 max-w-md overflow-hidden rounded-2xl bg-[#1E6091] p-4 text-white shadow-md">
                  <div className="flex items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <ChevronLeft className="text-white/70" />
                      <div>
                        <p className="font-round text-xs font-bold uppercase tracking-wider text-white/80">
                          Port {ti + 1}, Anchor {town.order}
                        </p>
                        <h2 className="font-round text-xl font-extrabold leading-tight">
                          {town.icon} {town.title}
                        </h2>
                      </div>
                    </div>
                    <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border-2 border-white/40">
                      <Anchor size={22} />
                    </span>
                  </div>
                </div>

                <div className="relative z-10 flex flex-col items-center gap-7">
                  {town.levels
                    .slice()
                    .sort((a, b) => a.order - b.order)
                    .map((level, li) => {
                      const status = level.status as NodeStatus;
                      const isCurrent = status === "current";
                      return (
                        <LevelNode
                          key={level.id}
                          level={level}
                          status={status}
                          laneX={LANE[li % LANE.length]}
                          isCurrent={isCurrent}
                          onSelect={() => handleSelect(level, world.id)}
                        />
                      );
                    })}
                </div>
              </section>
            ))}
        </div>

        {/* ═══ Side panel — all live data ═══ */}
        <aside className="space-y-4 lg:sticky lg:top-20 lg:self-start">
          <Link
            to="/leaderboard"
            className="flex items-center gap-4 rounded-2xl border-2 border-[#E5E5E5] bg-white p-4 transition hover:border-[#1E6091]"
          >
            <Trophy size={34} className="shrink-0 text-[#CE82FF]" />
            <span>
              <span className="block font-round text-base font-extrabold text-[#4B4B4B]">Crew Leaderboard</span>
              <span className="block text-sm text-[#777]">
                {myRank && myRank.rank ? `You are #${myRank.rank} this week` : "Climb the weekly board"}
              </span>
            </span>
          </Link>

          <div className="rounded-2xl border-2 border-[#E5E5E5] bg-white p-4">
            <div className="mb-3 flex items-center justify-between">
              <h3 className="font-round text-base font-extrabold text-[#4B4B4B]">Weekly Top 5</h3>
              <Link to="/leaderboard" className="font-round text-xs font-extrabold uppercase text-[#1CB0F6] hover:underline">
                Board
              </Link>
            </div>
            {entries.length === 0 && (
              <p className="text-sm text-[#777]">No rankings yet — sail a stage to appear.</p>
            )}
            <div className="space-y-3">
              {entries.slice(0, 5).map((entry, i) => (
                <div key={entry.user_id || i} className="flex items-center gap-3">
                  <span className="font-round text-sm font-extrabold text-[#999]">#{i + 1}</span>
                  <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[#F5F5F5] text-sm">
                    {entry.avatar || "🏴‍☠️"}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-sm font-semibold text-[#4B4B4B]">{entry.name}</p>
                    <p className="text-xs text-[#999]">{entry.diamonds?.toLocaleString?.() ?? 0} Diamonds</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </aside>
      </main>

      {/* ═══ Level Player overlay ═══ */}
      <AnimatePresence>
        {activeLevel && activeWorldId && (
          <LevelPlayer
            worldId={activeWorldId}
            level={activeLevel}
            onClose={() => {
              setActiveLevel(null);
              setActiveWorldId(null);
            }}
            onMastered={handleMastered}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
