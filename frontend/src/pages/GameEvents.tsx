import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Swords, Trophy, Zap, Flame, CalendarDays, Medal, Crown,
  Gamepad2, Crosshair, Gift, ArrowRight, Loader2, TrendingUp,
  Skull, ShieldCheck,
} from "lucide-react";
import { gameEventsApi } from "../services/api/gameEvents.ts";
import useAuthStore from "../store/authStore";
import useTrack from "../hooks/useTrack";

const THEME_EMOJI = {
  Cyberpunk: "🛸",
  "Neon City": "🌆",
  "Crystal Caverns": "💎",
  "Desert Storm": "🌪️",
  Frostbound: "❄️",
  "Ember Arena": "🔥",
  "Galactic Frontier": "🚀",
  "Neo Tokyo": "🏙️",
  "Wild West": "🤠",
  "Medieval Quest": "🏰",
  Steampunk: "⚙️",
  "Solar Flare": "☀️",
  "Deep Sea": "🌊",
  "Jungle Run": "🌴",
  "Volcanic Isle": "🌋",
  "Ice Palace": "🏔️",
  "Sky Pirates": "🏴‍☠️",
  Underground: "🕳️",
  "Time Rift": "⏳",
  "Void Runner": "🌌",
};

const TABS = [
  { key: "boss", label: "Daily Boss", icon: Swords },
  { key: "seasons", label: "Seasons", icon: Trophy },
  { key: "combo", label: "Combo", icon: Zap },
];

function themeEmoji(theme) {
  return THEME_EMOJI[theme] || "🎮";
}

function medalFor(index) {
  if (index === 0) return "🥇";
  if (index === 1) return "🥈";
  if (index === 2) return "🥉";
  return `${index + 1}`;
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

function formatHp(hp) {
  return Number(hp || 0).toLocaleString();
}

export default function GameEvents() {
  const user = useAuthStore((s) => s.user);
  const track = useTrack();
  const [activeTab, setActiveTab] = useState("boss");
  const [error, setError] = useState("");

  const [boss, setBoss] = useState(null);
  const [bossLoading, setBossLoading] = useState(true);
  const [attacking, setAttacking] = useState(false);
  const [lastDamage, setLastDamage] = useState(null);
  const [claiming, setClaiming] = useState(false);
  const [claimed, setClaimed] = useState(false);

  const [season, setSeason] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [seasonLoading, setSeasonLoading] = useState(true);
  const [seasonXp, setSeasonXp] = useState(0);

  const [combo, setCombo] = useState({ consecutive: 0, multiplier: 1, best: 0 });
  const [comboLoading, setComboLoading] = useState(true);

  const loadBoss = useCallback(async () => {
    setBossLoading(true);
    setError("");
    try {
      const data = await gameEventsApi.boss();
      setBoss(data);
    } catch (e) {
      setError(e.message || "Failed to load boss");
    } finally {
      setBossLoading(false);
    }
  }, []);

  const loadSeason = useCallback(async () => {
    setSeasonLoading(true);
    setError("");
    try {
      const seasonData = await gameEventsApi.seasons();
      setSeason(seasonData);
      const [lbData, comboData] = await Promise.all([
        gameEventsApi.seasonLeaderboard(seasonData.id).catch(() => ({ leaderboard: [] })),
        user ? gameEventsApi.combo().catch(() => null) : Promise.resolve(null),
      ]);
      setLeaderboard(lbData.leaderboard || []);
      if (comboData) {
        setCombo(comboData);
        const seasonEntry = lbData.leaderboard?.find((e) => e.user_id === user?.id);
        if (seasonEntry) setSeasonXp(seasonEntry.xp);
      }
    } catch (e) {
      setError(e.message || "Failed to load season");
    } finally {
      setSeasonLoading(false);
    }
  }, [user]);

  const loadCombo = useCallback(async () => {
    setComboLoading(true);
    setError("");
    try {
      const data = await gameEventsApi.combo();
      setCombo(data);
    } catch (e) {
      setError(e.message || "Failed to load combo");
    } finally {
      setComboLoading(false);
    }
  }, []);

  useEffect(() => {
    loadBoss();
    loadSeason();
    if (user) loadCombo();
  }, [loadBoss, loadSeason, loadCombo, user]);

  useEffect(() => {
    if (activeTab === "seasons") track("season", "view");
  }, [activeTab, track]);

  const handleAttack = async () => {
    if (!user) return;
    if (!boss) return;
    setAttacking(true);
    setError("");
    const damage = Math.floor(Math.random() * 451) + 50;
    try {
      const data = await gameEventsApi.attackBoss(boss.id, damage);
      track("boss", "attack");
      setLastDamage(data.damage);
      setBoss((prev) => ({
        ...prev,
        hp_remaining: data.hp_remaining,
        percent: data.percent,
        defeated: data.defeated,
        today_player_damage: (prev?.today_player_damage || 0) + data.damage,
      }));
    } catch (e) {
      setError(e.message || "Attack failed");
    } finally {
      setAttacking(false);
    }
  };

  const handleClaim = async () => {
    if (!boss) return;
    setClaiming(true);
    setError("");
    try {
      await gameEventsApi.claimBoss(boss.id);
      track("boss", "claim");
      setClaimed(true);
    } catch (e) {
      setError(e.message || "Claim failed");
      setClaimed(true);
    } finally {
      setClaiming(false);
    }
  };

  const handleCombo = async (success) => {
    setError("");
    try {
      const data = await gameEventsApi.recordCombo(success);
      track("combo", success ? "success" : "fail");
      setCombo(data);
    } catch (e) {
      setError(e.message || "Failed to record combo");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-display font-bold text-white flex items-center gap-3">
              <Gamepad2 className="w-8 h-8 text-emerald-400" />
              Game Events
            </h1>
            <p className="text-slate-400 mt-1">
              Community boss raids, seasonal grinds, and combo streaks.
            </p>
          </div>
          {user && (
            <span className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 bg-white/5 text-xs font-mono text-slate-300">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              {user.name}
            </span>
          )}
        </div>

        <div className="flex gap-2 mb-8">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.key;
            return (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium border transition-all ${
                  active
                    ? "border-indigo-500/50 bg-indigo-500/15 text-indigo-200"
                    : "border-white/10 bg-white/5 text-slate-400 hover:text-slate-200 hover:border-white/20"
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
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
          {activeTab === "boss" && (
            <motion.div
              key="boss"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
            >
              <div className="rounded-2xl border border-white/10 bg-white/5 p-6 sm:p-8">
                {bossLoading || !boss ? (
                  <div className="flex items-center justify-center py-16 text-slate-500">
                    <Loader2 className="w-6 h-6 animate-spin mr-2" />
                    Loading boss...
                  </div>
                ) : (
                  <div>
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                      <div className="flex items-center gap-4">
                        <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-rose-500/30 to-indigo-500/30 border border-white/10 flex items-center justify-center">
                          <Skull className="w-7 h-7 text-rose-400" />
                        </div>
                        <div>
                          <h2 className="text-xl font-display font-bold text-white flex items-center gap-2">
                            {boss.name}
                            <Crosshair className="w-4 h-4 text-rose-400" />
                          </h2>
                          <p className="text-xs font-mono text-slate-400 mt-0.5">
                            {boss.date} · ends {new Date(boss.ends_at).toLocaleTimeString()}
                          </p>
                        </div>
                      </div>
                      {lastDamage && !boss.defeated && (
                        <span className="text-sm font-mono text-emerald-400">
                          +{lastDamage} dealt
                        </span>
                      )}
                    </div>

                    <div className="mb-2 flex items-center justify-between text-sm font-mono">
                      <span className="text-slate-400">Community HP</span>
                      <span className="text-white">
                        {formatHp(boss.hp_remaining)}{" "}
                        <span className="text-slate-500">/ {formatHp(boss.hp_total)}</span>
                      </span>
                    </div>
                    <div className="h-4 rounded-full bg-slate-900 border border-white/10 overflow-hidden mb-2">
                      <motion.div
                        className="h-full rounded-full bg-gradient-to-r from-rose-500 via-indigo-500 to-emerald-400"
                        initial={{ width: "100%" }}
                        animate={{ width: `${Math.max(0, Math.min(100, boss.percent))}%` }}
                        transition={{ type: "spring", stiffness: 60, damping: 20 }}
                      />
                    </div>
                    <p className="text-right text-xs font-mono text-slate-500 mb-6">
                      {boss.percent}% remaining
                    </p>

                    <div className="flex flex-wrap items-center justify-between gap-4">
                      <div className="flex items-center gap-2 text-sm text-slate-300">
                        <Flame className="w-4 h-4 text-orange-400" />
                        Your damage today:{" "}
                        <span className="font-mono text-white">
                          {formatHp(boss.today_player_damage || 0)}
                        </span>
                      </div>
                      {!boss.defeated ? (
                        <button
                          onClick={handleAttack}
                          disabled={!user || attacking}
                          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-rose-500 to-indigo-500 text-sm font-semibold text-white disabled:opacity-40 hover:from-rose-400 hover:to-indigo-400 transition-all"
                        >
                          {attacking ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : (
                            <Crosshair className="w-4 h-4" />
                          )}
                          {user ? "Attack Boss" : "Sign in to attack"}
                        </button>
                      ) : (
                        <motion.div
                          initial={{ scale: 0.9, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          className="flex items-center gap-4"
                        >
                          <span className="px-3 py-1.5 rounded-full border border-emerald-500/40 bg-emerald-500/10 text-emerald-300 text-xs font-mono">
                            Defeated! +100 XP
                          </span>
                          {claimed ? (
                            <span className="flex items-center gap-2 text-sm text-slate-400">
                              <Gift className="w-4 h-4 text-emerald-400" />
                              Reward claimed
                            </span>
                          ) : (
                            <button
                              onClick={handleClaim}
                              disabled={!user || claiming}
                              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-indigo-500 text-sm font-semibold text-slate-950 disabled:opacity-40 hover:from-emerald-400 hover:to-indigo-400 transition-all"
                            >
                              {claiming ? (
                                <Loader2 className="w-4 h-4 animate-spin" />
                              ) : (
                                <Gift className="w-4 h-4" />
                              )}
                              Claim 50 XP
                            </button>
                          )}
                        </motion.div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {activeTab === "seasons" && (
            <motion.div
              key="seasons"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
            >
              {seasonLoading ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center py-16 text-slate-500">
                  <Loader2 className="w-6 h-6 animate-spin mr-2" />
                  Loading season...
                </div>
              ) : season ? (
                <div className="space-y-6">
                  <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-indigo-500/15 via-white/5 to-emerald-500/15 p-6 sm:p-8">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6">
                      <div className="flex items-center gap-4">
                        <div className="text-5xl">{themeEmoji(season.theme)}</div>
                        <div>
                          <div className="flex items-center gap-2 text-xs font-mono text-indigo-300 mb-1">
                            <Crown className="w-3.5 h-3.5" />
                            Current Season
                          </div>
                          <h2 className="text-2xl font-display font-bold text-white">
                            {season.name}
                          </h2>
                          <p className="text-slate-400 mt-1 text-sm">
                            <CalendarDays className="w-4 h-4 inline mr-1" />
                            {formatDate(season.start_date)} → {formatDate(season.end_date)}
                          </p>
                        </div>
                      </div>
                      <div className="flex gap-3">
                        <div className="rounded-xl border border-indigo-500/30 bg-indigo-500/10 px-4 py-3 text-center">
                          <div className="text-[10px] uppercase tracking-wider text-indigo-300 font-mono">
                            Exclusive Card
                          </div>
                          <div className="text-sm text-white font-medium mt-1">
                            {season.exclusive_card}
                          </div>
                        </div>
                        <div className="rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-center">
                          <div className="text-[10px] uppercase tracking-wider text-emerald-300 font-mono">
                            Badge
                          </div>
                          <div className="text-sm text-white font-medium mt-1">
                            {season.badge}
                          </div>
                        </div>
                      </div>
                    </div>
                    {user && (
                      <div className="mt-6 pt-4 border-t border-white/10 flex items-center gap-2 text-sm text-slate-300">
                        <TrendingUp className="w-4 h-4 text-emerald-400" />
                        Your season XP:{" "}
                        <span className="font-mono text-white">{formatHp(seasonXp)}</span>
                      </div>
                    )}
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                    <h3 className="flex items-center gap-2 text-lg font-display font-semibold text-white mb-4">
                      <Medal className="w-5 h-5 text-amber-400" />
                      Season Leaderboard
                    </h3>
                    <div className="space-y-2">
                      {leaderboard.length === 0 ? (
                        <p className="text-sm text-slate-500 py-8 text-center">
                          No points earned yet this season.
                        </p>
                      ) : (
                        leaderboard.map((entry, i) => (
                          <div
                            key={entry.user_id}
                            className={`flex items-center justify-between px-4 py-2.5 rounded-xl border transition-colors ${
                              i < 3
                                ? "border-white/15 bg-white/10"
                                : "border-white/5 bg-white/[0.03]"
                            }`}
                          >
                            <div className="flex items-center gap-3">
                              <span className="w-8 text-center text-sm font-mono">
                                {medalFor(i)}
                              </span>
                              <span className="text-sm text-slate-200">
                                {entry.user_name}
                              </span>
                              {i === 0 && (
                                <Crown className="w-3.5 h-3.5 text-amber-400" />
                              )}
                            </div>
                            <span className="text-sm font-mono text-emerald-400">
                              {formatHp(entry.xp)} XP
                            </span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="rounded-2xl border border-white/10 bg-white/5 py-16 text-center text-slate-500">
                  Failed to load season.
                </div>
              )}
            </motion.div>
          )}

          {activeTab === "combo" && (
            <motion.div
              key="combo"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
            >
              {!user ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 py-16 text-center text-slate-400">
                  Sign in to track your combo streak.
                </div>
              ) : comboLoading ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center py-16 text-slate-500">
                  <Loader2 className="w-6 h-6 animate-spin mr-2" />
                  Loading combo...
                </div>
              ) : (
                <div className="rounded-2xl border border-white/10 bg-white/5 p-6 sm:p-8">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-6 mb-8">
                    <div>
                      <h2 className="text-lg font-display font-semibold text-white flex items-center gap-2 mb-1">
                        <Zap className="w-5 h-5 text-amber-400" />
                        Combo Streak
                      </h2>
                      <p className="text-sm text-slate-400">
                        Chain correct answers to build your multiplier.
                      </p>
                    </div>
                    <motion.div
                      key={combo.multiplier}
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      className={`w-24 h-24 rounded-2xl border-2 flex flex-col items-center justify-center font-mono ${
                        combo.multiplier >= 4
                          ? "border-amber-400/60 bg-amber-500/15 text-amber-300"
                          : combo.multiplier >= 2
                          ? "border-emerald-400/60 bg-emerald-500/15 text-emerald-300"
                          : "border-white/15 bg-white/5 text-slate-300"
                      }`}
                    >
                      <span className="text-3xl font-bold">x{combo.multiplier}</span>
                      <span className="text-[10px] uppercase tracking-wider opacity-70 mt-0.5">
                        multiplier
                      </span>
                    </motion.div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 mb-8">
                    <div className="rounded-xl border border-white/10 bg-slate-950/50 p-4 text-center">
                      <div className="text-3xl font-mono font-bold text-white">
                        {combo.consecutive}
                      </div>
                      <div className="text-xs text-slate-400 mt-1 font-mono">
                        CONSECUTIVE
                      </div>
                    </div>
                    <div className="rounded-xl border border-white/10 bg-slate-950/50 p-4 text-center">
                      <div className="text-3xl font-mono font-bold text-indigo-300">
                        {combo.best}
                      </div>
                      <div className="text-xs text-slate-400 mt-1 font-mono">BEST</div>
                    </div>
                  </div>

                  <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4 mb-6 text-center">
                    <p className="text-sm text-slate-300 font-mono">
                      +{Math.max(0, 10 * (combo.multiplier - 1))} bonus XP at current multiplier
                    </p>
                    <p className="text-xs text-slate-500 mt-1">
                      Every 3 correct answers raises the multiplier up to x5.
                    </p>
                  </div>

                  <div className="flex gap-3">
                    <button
                      onClick={() => handleCombo(true)}
                      className="flex-1 flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-emerald-600 text-sm font-semibold text-slate-950 hover:from-emerald-400 hover:to-emerald-500 transition-all"
                    >
                      <ShieldCheck className="w-4 h-4" />
                      Correct
                    </button>
                    <button
                      onClick={() => handleCombo(false)}
                      className="flex-1 flex items-center justify-center gap-2 px-5 py-3 rounded-xl border border-white/10 bg-white/5 text-sm font-semibold text-slate-300 hover:border-rose-500/40 hover:text-rose-300 transition-all"
                    >
                      <Skull className="w-4 h-4" />
                      Wrong
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="mt-10 flex items-center justify-center gap-2 text-xs text-slate-500 font-mono">
          <ArrowRight className="w-3.5 h-3.5" />
          Game events reset daily · Season resets monthly
        </div>
      </div>
    </div>
  );
}
