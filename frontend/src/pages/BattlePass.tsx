import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { battlePassApi } from "../services/api/battlePass.ts";
import useAuthStore from "../store/authStore";
import { Flame, Gift, Crown, Calendar, Zap, Star, CheckCircle, Lock, X } from "lucide-react";

const FREE_REWARDS = [
  { tier: 1, type: "title", label: "Newbie", icon: "🌱" },
  { tier: 2, type: "emote", label: "Wave", icon: "👋" },
  { tier: 3, type: "coins", label: "100 Coins", icon: "🪙" },
  { tier: 4, type: "frame", label: "Blue Circuit", icon: "🔵" },
  { tier: 5, type: "title", label: "Problem Solver", icon: "🧠" },
  { tier: 6, type: "emote", label: "Fire", icon: "🔥" },
  { tier: 7, type: "coins", label: "250 Coins", icon: "🪙" },
  { tier: 8, type: "skin", label: "Default Skin", icon: "🛡️" },
  { tier: 9, type: "emote", label: "Sparkles", icon: "✨" },
  { tier: 10, type: "title", label: "Code Warrior", icon: "⚔️" },
  { tier: 11, type: "coins", label: "400 Coins", icon: "🪙" },
  { tier: 12, type: "frame", label: "Red Dragon", icon: "🔴" },
  { tier: 13, type: "emote", label: "Thumbs Up", icon: "👍" },
  { tier: 14, type: "coins", label: "600 Coins", icon: "🪙" },
  { tier: 15, type: "title", label: "Debug Dynamo", icon: "🐛" },
  { tier: 16, type: "emote", label: "Clap", icon: "👏" },
  { tier: 17, type: "coins", label: "800 Coins", icon: "🪙" },
  { tier: 18, type: "frame", label: "Golden Flame", icon: "🟡" },
  { tier: 19, type: "emote", label: "Mind Blown", icon: "🤯" },
  { tier: 20, type: "title", label: "Algorithm Apprentice", icon: "🎓" },
];

const PREMIUM_REWARDS = [
  { tier: 21, type: "cosmetic", label: "Premium Visor", icon: "🥽" },
  { tier: 22, type: "title", label: "Leader's Edge", icon: "👑" },
  { tier: 23, type: "emote", label: "Robot", icon: "🤖" },
  { tier: 24, type: "coins", label: "1000 Coins", icon: "🪙" },
  { tier: 25, type: "frame", label: "Neon Grid", icon: "🟣" },
  { tier: 26, type: "skin", label: "Plasma Blade", icon: "⚡" },
  { tier: 27, type: "emote", label: "Suspense", icon: "😏" },
  { tier: 28, type: "coins", label: "1500 Coins", icon: "🪙" },
  { tier: 29, type: "title", label: "FAANG Aspirant", icon: "🏢" },
  { tier: 30, type: "cosmetic", label: "Dragon Wing", icon: "🐉" },
];

export default function BattlePass() {
  const user = useAuthStore((s) => s.user);
  const [track, setTrack] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("daily");
  const [processing, setProcessing] = useState(null);
  const [lastReward, setLastReward] = useState(null);
  const [showPremium, setShowPremium] = useState(false);

  const loadTrack = useCallback(async () => {
    try {
      const data = await battlePassApi.track();
      setTrack(data);
    } catch (e) {
      setError(e.message || "Could not load battle pass");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadTrack();
  }, [loadTrack]);

  const claimDaily = async () => {
    setProcessing("daily");
    try {
      const res = await battlePassApi.dailyLogin();
      setLastReward({ type: "daily", xp: res.xp_gained, streak: res.streak, message: res.message });
      const refreshed = await battlePassApi.track();
      setTrack(refreshed);
    } catch (e) {
      setError(e.message || "Daily claim failed");
    } finally {
      setProcessing(null);
    }
  };

  const claimReward = async (tier) => {
    setProcessing("claim-" + tier);
    try {
      await battlePassApi.claim(tier);
      setLastReward({ type: "tier", tier, message: `Tier ${tier} claimed!` });
      const refreshed = await battlePassApi.track();
      setTrack(refreshed);
    } catch (e) {
      setError(e.message || "Claim failed");
    } finally {
      setProcessing(null);
    }
  };

  const activatePremium = async () => {
    setProcessing("premium");
    try {
      await battlePassApi.activatePremium();
      setShowPremium(true);
      const refreshed = await battlePassApi.track();
      setTrack(refreshed);
    } catch (e) {
      setError(e.message || "Could not activate premium");
    } finally {
      setProcessing(null);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base text-text-primary">
        <div className="animate-pulse text-nature-blossom">Loading Battle Pass...</div>
      </div>
    );
  }

  const currentTier = track?.current_tier || 0;
  const xpCurrent = track?.total_xp || 0;
  const progressInTier = Math.min(100, ((xpCurrent % 50) / 50) * 100);
  const hasPremium = track?.has_premium || false;
  const dailyBonus = track?.daily_bonus_available || false;
  const streak = track?.daily_login_count || 0;

  const allRewards = [...FREE_REWARDS, ...(hasPremium ? PREMIUM_REWARDS : [])];

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">⚔️ Battle Pass</h1>
          <p className="text-text-muted mt-2">Earn XP daily, climb tiers, unlock exclusive rewards.</p>
        </div>

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4 bg-amber-500/10 border border-amber-500/30 rounded-lg py-2 px-4 max-w-md mx-auto">
            {error}
          </p>
        )}

        {/* Stats bar */}
        <div className="grid grid-cols-4 gap-3 mb-6">
          <div className="bg-white border border-nature-leaf/20 rounded-xl p-3 text-center">
            <div className="text-2xl font-bold text-nature-blossom">Tier {currentTier}</div>
            <div className="text-xs text-text-muted">Current Tier</div>
          </div>
          <div className="bg-white border border-nature-leaf/20 rounded-xl p-3 text-center">
            <div className="text-2xl font-bold text-amber-400">{xpCurrent} XP</div>
            <div className="text-xs text-text-muted">Total XP</div>
          </div>
          <div className="bg-white border border-nature-leaf/20 rounded-xl p-3 text-center">
            <div className="text-2xl font-bold text-orange-400">{streak} 🔥</div>
            <div className="text-xs text-text-muted">Day Streak</div>
          </div>
          <div className="bg-white border border-nature-leaf/20 rounded-xl p-3 text-center">
            <div className="text-2xl font-bold text-nature-blossom">{track?.claimed || 0}</div>
            <div className="text-xs text-text-muted">Claimed</div>
          </div>
        </div>

        {/* XP Progress Bar */}
        <div className="mb-6 bg-[#E5E0D3] rounded-full h-4 overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-[#4F8F57] to-[#7BB661] rounded-full transition-all duration-500"
            style={{ width: `${progressInTier}%` }}
          />
        </div>
        <p className="text-center text-xs text-text-muted mb-6">
          {Math.min(50, xpCurrent % 50)} / 50 XP in Tier {currentTier}
        </p>

        {/* Daily Login */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-6 bg-gradient-to-r from-amber-100 to-orange-100 border border-amber-500/30 rounded-2xl p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold text-amber-600 flex items-center gap-2">
                <Calendar className="h-5 w-5" />
                Daily Login
              </h2>
              <p className="text-sm text-text-muted mt-1">
                {dailyBonus ? `+${25 + streak * 10} XP bonus today! Streak: ${streak} days` : "Check in daily to build your streak"}
              </p>
            </div>
            <button
              onClick={claimDaily}
              disabled={processing === "daily" || !dailyBonus}
              className="rounded-xl bg-amber-500 px-5 py-2 font-bold text-slate-900 hover:bg-amber-400 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {processing === "daily" ? "..." : dailyBonus ? "Claim" : "Coming Soon"}
            </button>
          </div>
          {streak >= 3 && (
            <div className="mt-3 flex gap-2">
              {[1, 2, 3, 4, 5, 6, 7].map((day) => (
                <div
                  key={day}
                  className={`h-8 w-8 rounded-lg flex items-center justify-center text-xs font-bold ${
                    day <= streak ? "bg-amber-500 text-slate-900" : "bg-surface-card text-text-muted"
                  }`}
                >
                  {day}
                </div>
              ))}
              <span className="text-xs text-text-muted ml-2 self-center">
                {streak}/7 days — +{streak * 10} bonus XP
              </span>
            </div>
          )}
        </motion.div>

        {/* Premium Toggle */}
        {!hasPremium && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mb-6 bg-gradient-to-r from-[#EDF5E6] to-[#D9EFCF] border border-nature-leaf/30 rounded-2xl p-6 text-center"
          >
            <Crown className="h-8 w-8 text-nature-blossom mx-auto mb-2" />
            <h2 className="text-xl font-bold text-nature-blossom">Premium Battle Pass</h2>
            <p className="text-sm text-text-muted mt-1">Unlock 20 exclusive tiers with premium cosmetics and titles.</p>
            <button
              onClick={activatePremium}
              disabled={processing === "premium"}
              className="mt-3 rounded-xl bg-nature-leaf px-6 py-2 font-bold text-white hover:bg-nature-moss disabled:opacity-50"
            >
              {processing === "premium" ? "Activating..." : "Activate Premium — Free"}
            </button>
          </motion.div>
        )}

        {/* Reward Tiers */}
        <div className="mb-6">
          <h2 className="text-xl font-bold text-text-primary mb-4">Reward Tiers</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {allRewards.map((r) => {
              const unlocked = r.tier <= currentTier;
              const claimed = (track?.rewards || []).some((rw) => rw.tier === r.tier && rw.claimed);
              return (
                <motion.div
                  key={r.tier}
                  className={`rounded-xl border p-3 text-center transition ${
                    unlocked
                      ? "border-nature-leaf/30 bg-surface-card"
                      : "border-nature-leaf/20 bg-surface-card opacity-50"
                  }`}
                >
                  <div className="text-2xl mb-1">{r.icon}</div>
                  <div className="text-xs font-bold text-text-secondary">Tier {r.tier}</div>
                  <div className="text-xs text-text-muted mt-1">{r.label}</div>
                  {unlocked && !claimed && (
                    <button
                      onClick={() => claimReward(r.tier)}
                      disabled={processing === "claim-" + r.tier}
                      className="mt-2 w-full rounded-lg bg-nature-leaf px-2 py-1 text-xs font-bold text-white hover:bg-nature-moss disabled:opacity-50"
                    >
                      {processing === "claim-" + r.tier ? "..." : "Claim"}
                    </button>
                  )}
                  {claimed && (
                    <div className="mt-2 text-xs text-green-400">Claimed ✓</div>
                  )}
                </motion.div>
              );
            })}
          </div>
        </div>

        {/* Last Reward Celebration */}
        <AnimatePresence>
          {lastReward && (
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.5 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
              onClick={() => setLastReward(null)}
            >
              <motion.div
                className="bg-white border-2 border-amber-400 rounded-3xl p-8 text-center max-w-sm mx-4 shadow-[0_0_40px_rgba(127,182,97,0.35)]"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="text-5xl mb-4">{lastReward.type === "daily" ? "🔥" : "🎉"}</div>
                <h3 className="text-2xl font-bold text-amber-600 mb-2">
                  {lastReward.type === "daily" ? "Daily Bonus!" : "Tier Unlocked!"}
                </h3>
                {lastReward.xp && (
                  <p className="text-lg text-text-secondary">+{lastReward.xp} XP</p>
                )}
                {lastReward.streak && (
                  <p className="text-sm text-amber-600">Streak: {lastReward.streak} days 🔥</p>
                )}
                {lastReward.tier && (
                  <p className="text-sm text-nature-blossom">Tier {lastReward.tier} reward claimed!</p>
                )}
                <button
                  onClick={() => setLastReward(null)}
                  className="mt-6 w-full bg-nature-leaf hover:bg-nature-moss text-white font-semibold rounded-xl py-3 transition"
                >
                  Awesome
                </button>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}