import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Swords, Shield, Users, UserPlus, LogIn, Copy, Zap, Flame, Lock,
  CheckCircle2, Play, ChevronRight, Loader2, Crown, Crosshair, Gift,
  Code2, Mic, Briefcase, Medal, Trophy, PartyPopper,
} from "lucide-react";
import { guildsApi } from "../services/api/guilds.ts";
import { dungeonsApi } from "../services/api/dungeons.ts";
import useAuthStore from "../store/authStore";
import useTrack from "../hooks/useTrack";

const TABS = [
  { key: "guild", label: "Guild", icon: Shield },
  { key: "war", label: "Guild Wars", icon: Swords },
  { key: "dungeons", label: "Boss Dungeons", icon: Crosshair },
];

const CONTRIBUTE_OPTIONS = [10, 50, 100, 500];
const SCORE_OPTIONS = [10, 50, 100];
const LEVEL_TITLES = ["Rookie Guild", "Bronze Guild", "Silver Guild", "Gold Guild", "Legendary Guild"];
const LEVEL_THRESHOLDS = [0, 500, 1500, 3000, 6000];
const STAGE_ICONS = { OA: Code2, Interview: Mic, Behavioral: Briefcase };
const WAR_CAP = 5000;

function levelTitle(level) {
  return LEVEL_TITLES[Math.max(0, Math.min(LEVEL_TITLES.length - 1, level - 1))];
}

function nextThreshold(xp) {
  for (const t of LEVEL_THRESHOLDS) {
    if (xp < t) return t;
  }
  return LEVEL_THRESHOLDS[LEVEL_THRESHOLDS.length - 1];
}

function xpProgress(xp) {
  const thresholds = LEVEL_THRESHOLDS;
  let current = 0;
  let next = thresholds[thresholds.length - 1];
  for (let i = 0; i < thresholds.length; i++) {
    if (xp >= thresholds[i]) {
      current = thresholds[i];
      next = i + 1 < thresholds.length ? thresholds[i + 1] : thresholds[i];
    } else {
      break;
    }
  }
  if (current >= next) return 100;
  return Math.round(((xp - current) / (next - current)) * 100);
}

function formatRemaining(iso) {
  if (!iso) return "00:00:00";
  const diff = new Date(iso).getTime() - Date.now();
  if (diff <= 0) return "00:00:00";
  const h = Math.floor(diff / 3600000);
  const m = Math.floor((diff % 3600000) / 60000);
  const s = Math.floor((diff % 60000) / 1000);
  return [h, m, s].map((n) => String(n).padStart(2, "0")).join(":");
}

function copyCode(code) {
  if (navigator.clipboard) navigator.clipboard.writeText(code).catch(() => {});
}

export default function Dungeons() {
  const user = useAuthStore((s) => s.user);
  const track = useTrack();
  const [tab, setTab] = useState("guild");
  const [error, setError] = useState("");

  const [guild, setGuild] = useState(null);
  const [guildLoading, setGuildLoading] = useState(true);
  const [createName, setCreateName] = useState("");
  const [joinCode, setJoinCode] = useState("");
  const [busy, setBusy] = useState(false);

  const [leaderboard, setLeaderboard] = useState([]);
  const [war, setWar] = useState(null);
  const [warMySide, setWarMySide] = useState(null);
  const [warGuildId, setWarGuildId] = useState(null);
  const [warResult, setWarResult] = useState(null);
  const [scoreBusy, setScoreBusy] = useState(false);
  const [resolving, setResolving] = useState(false);

  const [dungeons, setDungeons] = useState([]);
  const [activeRun, setActiveRun] = useState(null);
  const [completed, setCompleted] = useState([]);
  const [dungeonLoading, setDungeonLoading] = useState(true);
  const [nowTick, setNowTick] = useState(0);

  const loadGuild = useCallback(async () => {
    if (!user) {
      setGuild(null);
      setGuildLoading(false);
      return;
    }
    setGuildLoading(true);
    try {
      const data = await guildsApi.my();
      setGuild(data);
    } catch (e) {
      setGuild(null);
      if (e.status !== 404) setError(e.message || "Failed to load guild");
    } finally {
      setGuildLoading(false);
    }
  }, [user]);

  const loadLeaderboard = useCallback(async () => {
    try {
      const data = await guildsApi.leaderboard();
      setLeaderboard(data.guilds || []);
    } catch (e) { /* ignore */ }
  }, []);

  const loadWar = useCallback(async () => {
    if (!user) return;
    try {
      const data = await guildsApi.activeWar();
      setWar(data.war);
      setWarMySide(data.my_side);
      setWarGuildId(data.guild_id);
    } catch (e) { /* ignore */ }
  }, [user]);

  const loadDungeons = useCallback(async () => {
    setDungeonLoading(true);
    try {
      const data = await dungeonsApi.list();
      setDungeons(data.dungeons || []);
      setActiveRun(data.active_run || null);
      setCompleted(data.completed || []);
    } catch (e) {
      setError(e.message || "Failed to load dungeons");
    } finally {
      setDungeonLoading(false);
    }
  }, []);

  useEffect(() => {
    loadGuild();
    loadLeaderboard();
    if (user) loadWar();
    loadDungeons();
  }, [loadGuild, loadLeaderboard, loadWar, loadDungeons, user]);

  useEffect(() => {
    if (tab !== "war" || !war) return;
    const t = setInterval(() => setNowTick(Date.now()), 1000);
    return () => clearInterval(t);
  }, [tab, war]);

  const handleCreate = async () => {
    setBusy(true);
    setError("");
    try {
      const data = await guildsApi.create(createName);
      track("guild", "create");
      setGuild(data);
      setCreateName("");
      loadLeaderboard();
    } catch (e) {
      setError(e.message || "Failed to create guild");
    } finally {
      setBusy(false);
    }
  };

  const handleJoin = async () => {
    setBusy(true);
    setError("");
    try {
      const data = await guildsApi.join(joinCode);
      track("guild", "join");
      setGuild(data);
      setJoinCode("");
      loadLeaderboard();
    } catch (e) {
      setError(e.message || "Failed to join guild");
    } finally {
      setBusy(false);
    }
  };

  const handleContribute = async (amount) => {
    setBusy(true);
    setError("");
    try {
      const data = await guildsApi.contribute(amount, "guild boost");
      track("guild", "contribute");
      setGuild(data);
      loadLeaderboard();
    } catch (e) {
      setError(e.message || "Contribution failed");
    } finally {
      setBusy(false);
    }
  };

  const handleChallenge = async (guildId) => {
    setBusy(true);
    setError("");
    try {
      await guildsApi.challenge(guildId);
      setWarResult(null);
      loadWar();
    } catch (e) {
      setError(e.message || "Challenge failed");
    } finally {
      setBusy(false);
    }
  };

  const handleScore = async (amount) => {
    if (!war || !warGuildId) return;
    setScoreBusy(true);
    setError("");
    try {
      await guildsApi.warScore(war.id, warGuildId, amount);
      track("guild", "war_score");
      loadWar();
    } catch (e) {
      setError(e.message || "Scoring failed");
    } finally {
      setScoreBusy(false);
    }
  };

  const handleResolve = async () => {
    if (!war) return;
    setResolving(true);
    setError("");
    try {
      const data = await guildsApi.resolveWar(war.id);
      setWarResult(data);
      loadWar();
      loadGuild();
      loadLeaderboard();
    } catch (e) {
      setError(e.message || "Resolve failed");
    } finally {
      setResolving(false);
    }
  };

  const handleStart = async (dungeonId) => {
    setBusy(true);
    setError("");
    try {
      await dungeonsApi.start(dungeonId, 0);
      track("dungeon", "start");
      loadDungeons();
    } catch (e) {
      setError(e.message || "Failed to start dungeon");
    } finally {
      setBusy(false);
    }
  };

  const handleAdvance = async (dungeonId, stageIndex) => {
    setBusy(true);
    setError("");
    try {
      await dungeonsApi.advance(dungeonId, stageIndex);
      track("dungeon", "advance");
      const target = dungeons.find((d) => d.id === dungeonId);
      if (target && stageIndex + 1 >= target.stages.length) track("dungeon", "complete");
      loadDungeons();
      loadGuild();
    } catch (e) {
      setError(e.message || "Failed to advance");
    } finally {
      setBusy(false);
    }
  };

  const warOver = war ? new Date(war.end).getTime() <= Date.now() : false;
  const myPoints = war && warMySide ? war.points?.[warMySide] || 0 : 0;
  const theirPoints = war && warMySide
    ? war.points?.[warMySide === "challenger" ? "defender" : "challenger"] || 0
    : 0;

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-display font-bold text-white flex items-center gap-3">
              <Swords className="w-8 h-8 text-emerald-400" />
              Guilds & Dungeons
            </h1>
            <p className="text-slate-400 mt-1">
              Build a guild, wage wars, and conquer company boss dungeons.
            </p>
          </div>
          {user && (
            <span className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 bg-white/5 text-xs font-mono text-slate-300">
              <Shield className="w-3.5 h-3.5 text-emerald-400" />
              {user.name}
            </span>
          )}
        </div>

        <div className="flex gap-2 mb-8 flex-wrap">
          {TABS.map((tabDef) => {
            const Icon = tabDef.icon;
            const active = tab === tabDef.key;
            return (
              <button
                key={tabDef.key}
                onClick={() => setTab(tabDef.key)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border transition-all ${
                  active
                    ? "border-indigo-500/50 bg-indigo-500/15 text-indigo-200"
                    : "border-white/10 bg-white/5 text-slate-400 hover:text-slate-200 hover:border-white/20"
                }`}
              >
                <Icon className="w-4 h-4" />
                {tabDef.label}
              </button>
            );
          })}
        </div>

        {error && (
          <div className="mb-6 rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
            {error}
          </div>
        )}

        <AnimatePresence mode="wait">
          {tab === "guild" && (
            <motion.div
              key="guild"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
            >
              {!user ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 py-16 text-center text-slate-400">
                  <LogIn className="w-10 h-10 mx-auto mb-3 text-indigo-400" />
                  Sign in to join a guild.
                </div>
              ) : guildLoading ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center py-16 text-slate-500">
                  <Loader2 className="w-6 h-6 animate-spin mr-2" />
                  Loading guild...
                </div>
              ) : !guild ? (
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                    <h2 className="text-lg font-display font-semibold text-white flex items-center gap-2 mb-1">
                      <Shield className="w-5 h-5 text-emerald-400" />
                      Create a Guild
                    </h2>
                    <p className="text-sm text-slate-400 mb-5">
                      Found your own guild and invite teammates with a join code.
                    </p>
                    <input
                      value={createName}
                      onChange={(e) => setCreateName(e.target.value)}
                      onKeyDown={(e) => { if (e.key === "Enter") handleCreate(); }}
                      placeholder="Guild name"
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/60 border border-white/10 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/30 transition-all mb-4"
                    />
                    <button
                      onClick={handleCreate}
                      disabled={busy || !createName.trim()}
                      className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-indigo-500 text-sm font-semibold text-slate-950 disabled:opacity-40 hover:from-emerald-400 hover:to-indigo-400 transition-all"
                    >
                      {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <Shield className="w-4 h-4" />}
                      Create Guild
                    </button>
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                    <h2 className="text-lg font-display font-semibold text-white flex items-center gap-2 mb-1">
                      <Users className="w-5 h-5 text-indigo-400" />
                      Join a Guild
                    </h2>
                    <p className="text-sm text-slate-400 mb-5">
                      Enter a 6-character code shared by your friends.
                    </p>
                    <input
                      value={joinCode}
                      onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                      onKeyDown={(e) => { if (e.key === "Enter") handleJoin(); }}
                      placeholder="XXXXXX"
                      maxLength={6}
                      className="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/60 border border-white/10 text-sm font-mono uppercase text-white placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 transition-all mb-4"
                    />
                    <button
                      onClick={handleJoin}
                      disabled={busy || joinCode.trim().length !== 6}
                      className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-xl border border-white/10 bg-white/5 text-sm font-semibold text-slate-200 disabled:opacity-40 hover:border-indigo-500/40 hover:text-indigo-300 transition-all"
                    >
                      <UserPlus className="w-4 h-4" />
                      Join with Code
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-indigo-500/15 via-white/5 to-emerald-500/15 p-6 sm:p-8">
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-6">
                      <div className="flex items-center gap-4">
                        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-emerald-500/30 to-indigo-500/30 border border-white/10 flex items-center justify-center">
                          <Shield className="w-7 h-7 text-emerald-400" />
                        </div>
                        <div>
                          <h2 className="text-2xl font-display font-bold text-white flex items-center gap-2">
                            {guild.name}
                            {guild.owner_id === user.id && <Crown className="w-4 h-4 text-amber-400" />}
                          </h2>
                          <p className="text-xs font-mono text-slate-400 mt-1">
                            Level {guild.level} · {levelTitle(guild.level)} · {guild.member_count} members
                          </p>
                        </div>
                      </div>
                      <div className="flex flex-col items-start sm:items-end gap-2">
                        <button
                          onClick={() => copyCode(guild.code)}
                          className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 bg-slate-950/60 text-xs font-mono text-emerald-300 hover:border-emerald-500/40 transition-all"
                        >
                          <Copy className="w-3.5 h-3.5" />
                          {guild.code}
                        </button>
                        <span className="text-xs text-slate-500">Your rank: #{guild.rank}</span>
                      </div>
                    </div>
                    <div className="mt-6">
                      <div className="mb-2 flex items-center justify-between text-sm font-mono">
                        <span className="text-slate-400">Guild XP</span>
                        <span className="text-white">
                          {guild.xp.toLocaleString()}{" "}
                          <span className="text-slate-500">/ {nextThreshold(guild.xp).toLocaleString()}</span>
                        </span>
                      </div>
                      <div className="h-3 rounded-full bg-slate-900 border border-white/10 overflow-hidden">
                        <motion.div
                          className="h-full rounded-full bg-gradient-to-r from-emerald-500 via-emerald-400 to-indigo-400"
                          initial={{ width: 0 }}
                          animate={{ width: `${xpProgress(guild.xp)}%` }}
                          transition={{ type: "spring", stiffness: 60, damping: 20 }}
                        />
                      </div>
                    </div>
                  </div>

                  <div className="grid lg:grid-cols-2 gap-6">
                    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                      <h3 className="flex items-center gap-2 text-lg font-display font-semibold text-white mb-1">
                        <Zap className="w-5 h-5 text-amber-400" />
                        Contribute XP
                      </h3>
                      <p className="text-sm text-slate-400 mb-5">
                        Power your guild toward the next tier.
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {CONTRIBUTE_OPTIONS.map((amount) => (
                          <button
                            key={amount}
                            onClick={() => handleContribute(amount)}
                            disabled={busy}
                            className="flex items-center gap-1 px-4 py-2.5 rounded-xl border border-white/10 bg-slate-950/60 text-sm font-semibold text-slate-200 disabled:opacity-40 hover:border-emerald-500/40 hover:text-emerald-300 transition-all"
                          >
                            <Flame className="w-4 h-4 text-emerald-400" />
                            +{amount}
                          </button>
                        ))}
                      </div>
                    </div>

                    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                      <h3 className="flex items-center gap-2 text-lg font-display font-semibold text-white mb-4">
                        <Users className="w-5 h-5 text-indigo-400" />
                        Members
                      </h3>
                      <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
                        {guild.members.map((m, i) => (
                          <div
                            key={m.user_id}
                            className={`flex items-center justify-between px-4 py-2.5 rounded-xl border transition-colors ${
                              m.user_id === user.id
                                ? "border-emerald-500/30 bg-emerald-500/10"
                                : "border-white/5 bg-white/[0.03]"
                            }`}
                          >
                            <div className="flex items-center gap-3">
                              <span className="w-6 text-center text-sm font-mono text-slate-500">
                                {i === 0 ? <Crown className="w-4 h-4 inline text-amber-400" /> : i + 1}
                              </span>
                              <span className="text-sm text-slate-200">{m.name}</span>
                              {m.user_id === user.id && (
                                <span className="text-[10px] font-mono text-emerald-400">you</span>
                              )}
                            </div>
                            <span className="text-sm font-mono text-emerald-400">
                              {(m.xp_contributed || 0).toLocaleString()} XP
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                    <h3 className="flex items-center gap-2 text-lg font-display font-semibold text-white mb-4">
                      <Trophy className="w-5 h-5 text-amber-400" />
                      Guild Leaderboard
                    </h3>
                    <div className="space-y-2">
                      {leaderboard.length === 0 ? (
                        <p className="text-sm text-slate-500 py-6 text-center">
                          No guilds yet. Be the first!
                        </p>
                      ) : (
                        leaderboard.map((entry, i) => (
                          <div
                            key={entry.id}
                            className={`flex items-center justify-between px-4 py-2.5 rounded-xl border transition-colors ${
                              entry.id === guild?.id
                                ? "border-emerald-500/30 bg-emerald-500/10"
                                : i < 3
                                ? "border-white/15 bg-white/10"
                                : "border-white/5 bg-white/[0.03]"
                            }`}
                          >
                            <div className="flex items-center gap-3">
                              <span className="w-8 text-center text-sm font-mono">
                                {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `${i + 1}`}
                              </span>
                              <div>
                                <div className="text-sm text-slate-200 flex items-center gap-2">
                                  {entry.name}
                                  {entry.id === guild?.id && (
                                    <span className="text-[10px] font-mono text-emerald-400">your guild</span>
                                  )}
                                </div>
                                <div className="text-[10px] font-mono text-slate-500">
                                  Lv {entry.level} · {levelTitle(entry.level)}
                                </div>
                              </div>
                            </div>
                            <span className="text-sm font-mono text-emerald-400">
                              {entry.xp.toLocaleString()} XP
                            </span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {tab === "war" && (
            <motion.div
              key="war"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
            >
              {!user ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 py-16 text-center text-slate-400">
                  <LogIn className="w-10 h-10 mx-auto mb-3 text-indigo-400" />
                  Sign in to wage guild wars.
                </div>
              ) : !guild ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 py-16 text-center text-slate-400">
                  <Swords className="w-10 h-10 mx-auto mb-3 text-indigo-400" />
                  Join or create a guild to start waging wars.
                </div>
              ) : (
                <div className="space-y-6">
                  {warResult && (
                    <motion.div
                      initial={{ scale: 0.95, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      className={`rounded-2xl border p-6 flex items-center gap-4 ${
                        warResult.winner_id === guild.id
                          ? "border-emerald-500/40 bg-emerald-500/10"
                          : warResult.winner_id
                          ? "border-rose-500/30 bg-rose-500/10"
                          : "border-white/10 bg-white/5"
                      }`}
                    >
                      <PartyPopper className={`w-8 h-8 shrink-0 ${warResult.winner_id ? "text-emerald-400" : "text-slate-400"}`} />
                      <div>
                        <h3 className="text-lg font-display font-semibold text-white">
                          {warResult.winner_id === guild.id
                            ? "Your guild won the war!"
                            : warResult.winner_id
                            ? "Your guild lost the war."
                            : "The war ended in a draw."}
                        </h3>
                        <p className="text-sm text-slate-400 mt-1">
                          {warResult.xp_awarded > 0
                            ? `Winning guild earned +${warResult.xp_awarded} XP.`
                            : "No XP awarded for a draw."}
                        </p>
                      </div>
                    </motion.div>
                  )}

                  {war ? (
                    <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-rose-500/10 via-white/5 to-indigo-500/10 p-6 sm:p-8">
                      <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-display font-semibold text-white flex items-center gap-2">
                          <Swords className="w-5 h-5 text-rose-400" />
                          Active Guild War
                        </h3>
                        <span className="flex items-center gap-2 text-xs font-mono text-slate-400">
                          <TimerIcon />
                          {warOver ? "War ended" : formatRemaining(war.end)}
                        </span>
                      </div>

                      <div className="flex items-center justify-between gap-4 mb-2">
                        <div className="flex-1">
                          <div className="text-sm font-semibold text-white mb-1">
                            {warMySide === "challenger" ? war.challenger_name : war.defender_name}
                            <span className="ml-2 text-[10px] font-mono text-emerald-400">you</span>
                          </div>
                          <div className="text-2xl font-mono font-bold text-emerald-400">{myPoints}</div>
                        </div>
                        <div className="text-xs font-mono text-slate-500 shrink-0">VS</div>
                        <div className="flex-1 text-right">
                          <div className="text-sm font-semibold text-white mb-1">
                            {warMySide === "challenger" ? war.defender_name : war.challenger_name}
                          </div>
                          <div className="text-2xl font-mono font-bold text-indigo-400">{theirPoints}</div>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3 mb-6">
                        <div className="h-3 rounded-full bg-slate-900 border border-white/10 overflow-hidden">
                          <motion.div
                            className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-emerald-400"
                            initial={{ width: 0 }}
                            animate={{ width: `${Math.min(100, (myPoints / WAR_CAP) * 100)}%` }}
                            transition={{ type: "spring", stiffness: 60, damping: 20 }}
                          />
                        </div>
                        <div className="h-3 rounded-full bg-slate-900 border border-white/10 overflow-hidden">
                          <motion.div
                            className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-indigo-400 ml-auto"
                            initial={{ width: 0 }}
                            animate={{ width: `${Math.min(100, (theirPoints / WAR_CAP) * 100)}%` }}
                            transition={{ type: "spring", stiffness: 60, damping: 20 }}
                          />
                        </div>
                      </div>

                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono text-slate-500 mr-1">Score</span>
                          {SCORE_OPTIONS.map((amount) => (
                            <button
                              key={amount}
                              onClick={() => handleScore(amount)}
                              disabled={scoreBusy || warOver}
                              className="px-3 py-2 rounded-xl border border-white/10 bg-slate-950/60 text-sm font-semibold text-slate-200 disabled:opacity-40 hover:border-emerald-500/40 hover:text-emerald-300 transition-all"
                            >
                              +{amount}
                            </button>
                          ))}
                        </div>
                        <button
                          onClick={handleResolve}
                          disabled={resolving || !warOver}
                          className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-emerald-500 text-sm font-semibold text-white disabled:opacity-40 hover:from-indigo-400 hover:to-emerald-400 transition-all"
                        >
                          {resolving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trophy className="w-4 h-4" />}
                          {warOver ? "Resolve War" : `Resolves in ${formatRemaining(war.end)}`}
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="rounded-2xl border border-white/10 bg-white/5 p-6 text-center text-slate-400">
                      <Swords className="w-8 h-8 mx-auto mb-2 text-slate-500" />
                      No active war. Challenge a guild below!
                    </div>
                  )}

                  <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                    <h3 className="flex items-center gap-2 text-lg font-display font-semibold text-white mb-4">
                      <Medal className="w-5 h-5 text-amber-400" />
                      Challenge a Guild
                    </h3>
                    <div className="space-y-2">
                      {leaderboard.filter((g) => g.id !== guild.id).length === 0 ? (
                        <p className="text-sm text-slate-500 py-6 text-center">
                          No rival guilds yet.
                        </p>
                      ) : (
                        leaderboard
                          .filter((g) => g.id !== guild.id)
                          .map((entry, i) => (
                            <div
                              key={entry.id}
                              className="flex items-center justify-between px-4 py-3 rounded-xl border border-white/5 bg-white/[0.03]"
                            >
                              <div className="flex items-center gap-3">
                                <span className="w-8 text-center text-sm font-mono text-slate-500">
                                  {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `${i + 1}`}
                                </span>
                                <div>
                                  <div className="text-sm text-slate-200">{entry.name}</div>
                                  <div className="text-[10px] font-mono text-slate-500">
                                    Lv {entry.level} · {entry.xp.toLocaleString()} XP
                                  </div>
                                </div>
                              </div>
                              <button
                                onClick={() => handleChallenge(entry.id)}
                                disabled={busy || !!war}
                                className="flex items-center gap-2 px-4 py-2 rounded-xl border border-rose-500/30 bg-rose-500/10 text-xs font-semibold text-rose-300 disabled:opacity-40 hover:border-rose-500/60 hover:text-rose-200 transition-all"
                              >
                                <Swords className="w-3.5 h-3.5" />
                                Challenge
                              </button>
                            </div>
                          ))
                      )}
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {tab === "dungeons" && (
            <motion.div
              key="dungeons"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
            >
              {dungeonLoading ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center py-16 text-slate-500">
                  <Loader2 className="w-6 h-6 animate-spin mr-2" />
                  Loading dungeons...
                </div>
              ) : (
                <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
                  {dungeons.map((d) => {
                    const isCompleted = completed.includes(d.id);
                    const isActive = activeRun && activeRun.dungeon_id === d.id;
                    const run = isActive ? activeRun : null;
                    return (
                      <div
                        key={d.id}
                        className="rounded-2xl border border-white/10 bg-white/5 p-5 flex flex-col"
                      >
                        <div className="flex items-center gap-3 mb-4">
                          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-500/25 to-indigo-500/25 border border-white/10 flex items-center justify-center text-2xl">
                            {d.emoji}
                          </div>
                          <div className="flex-1">
                            <h3 className="text-lg font-display font-bold text-white">{d.company}</h3>
                            <span className="inline-flex items-center gap-1 mt-0.5 text-[10px] font-mono text-indigo-300">
                              <Gift className="w-3 h-3" />
                              {d.reward_chest}
                            </span>
                          </div>
                          {isCompleted && (
                            <span className="flex items-center gap-1 px-2 py-1 rounded-full border border-emerald-500/40 bg-emerald-500/10 text-[10px] font-mono text-emerald-300">
                              <CheckCircle2 className="w-3 h-3" />
                              Cleared
                            </span>
                          )}
                        </div>

                        <div className="space-y-2 mb-5 flex-1">
                          {d.stages.map((stage, i) => {
                            const Icon = STAGE_ICONS[stage.type] || Code2;
                            const done = isCompleted || (run && run.completed_stages.includes(i));
                            const current = !isCompleted && run && i === run.current_stage;
                            const ready = !isCompleted && !run && i === 0;
                            return (
                              <div
                                key={i}
                                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl border transition-colors ${
                                  done
                                    ? "border-emerald-500/20 bg-emerald-500/5"
                                    : current
                                    ? "border-indigo-500/40 bg-indigo-500/10"
                                    : ready
                                    ? "border-white/15 bg-white/5"
                                    : "border-white/5 bg-white/[0.02]"
                                }`}
                              >
                                <span className={`shrink-0 ${done ? "text-emerald-400" : current ? "text-indigo-400" : "text-slate-600"}`}>
                                  {done ? (
                                    <CheckCircle2 className="w-4 h-4" />
                                  ) : current || ready ? (
                                    <Play className="w-4 h-4" />
                                  ) : (
                                    <Lock className="w-4 h-4" />
                                  )}
                                </span>
                                <Icon className={`w-3.5 h-3.5 shrink-0 ${done ? "text-emerald-400/70" : current ? "text-indigo-400" : "text-slate-600"}`} />
                                <div className="flex-1 min-w-0">
                                  <div className="text-xs font-semibold text-slate-200 truncate">{stage.title}</div>
                                  <div className="text-[10px] font-mono text-slate-500">
                                    Stage {i + 1} · {stage.type}
                                  </div>
                                </div>
                              </div>
                            );
                          })}
                        </div>

                        {isCompleted ? (
                          <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-center">
                            <div className="text-sm font-semibold text-emerald-300 flex items-center justify-center gap-2">
                              <PartyPopper className="w-4 h-4" />
                              Dungeon conquered! +150 XP
                            </div>
                            <div className="text-[11px] font-mono text-emerald-400/70 mt-0.5">
                              {d.reward_chest} unlocked
                            </div>
                          </div>
                        ) : run ? (
                          <button
                            onClick={() => handleAdvance(d.id, run.current_stage)}
                            disabled={busy}
                            className="w-full flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-indigo-500 text-sm font-semibold text-slate-950 disabled:opacity-40 hover:from-emerald-400 hover:to-indigo-400 transition-all"
                          >
                            {busy ? <Loader2 className="w-4 h-4 animate-spin" /> : <ChevronRight className="w-4 h-4" />}
                            Advance Stage {run.current_stage + 1} of 5
                          </button>
                        ) : (
                          <button
                            onClick={() => handleStart(d.id)}
                            disabled={busy || !!activeRun}
                            className="w-full flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl border border-white/10 bg-white/5 text-sm font-semibold text-slate-200 disabled:opacity-40 hover:border-indigo-500/40 hover:text-indigo-300 transition-all"
                          >
                            <Play className="w-4 h-4" />
                            Start Dungeon
                          </button>
                        )}
                      </div>
                    );
                  })}
                </div>
              )}

              <div className="mt-8 flex items-center justify-center gap-2 text-xs text-slate-500 font-mono">
                <Crosshair className="w-3.5 h-3.5" />
                Clear all 5 stages to unlock each company chest · +150 XP per dungeon
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function TimerIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="10" y1="2" x2="14" y2="2" />
      <line x1="12" y1="14" x2="15" y2="11" />
      <circle cx="12" cy="14" r="8" />
    </svg>
  );
}
