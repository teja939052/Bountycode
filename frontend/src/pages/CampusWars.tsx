import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { campusWarsApi } from "../services/api/campusWars.ts";
import useAuthStore from "../store/authStore";
import { Sword, Trophy, Flame, CheckCircle, Gift, Calendar, Zap } from "lucide-react";

export default function CampusWars() {
  const user = useAuthStore((s) => s.user);
  const [dailyQuests, setDailyQuests] = useState([]);
  const [claimedQuests, setClaimedQuests] = useState([]);
  const [weeklyChallenges, setWeeklyChallenges] = useState([]);
  const [userProgress, setUserProgress] = useState(null);
  const [claimedTiers, setClaimedTiers] = useState([]);
  const [badges, setBadges] = useState<Array<{ earned: boolean; tier?: number; id?: string; name?: string }>>([]);
  const [ranks, setRanks] = useState<Record<string, { threshold: number; icon: string }>>({});
  const [activeTab, setActiveTab] = useState("daily");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [processingQuest, setProcessingQuest] = useState(false);
  const [lastReward, setLastReward] = useState(null);

  const loadAll = useCallback(async () => {
    try {
      const [dailies, weekly, userBadges, allRanks] = await Promise.all([
        campusWarsApi.dailyQuests(),
        campusWarsApi.weeklyChallenges(),
        campusWarsApi.badges(),
        campusWarsApi.ranks(),
      ]);
      const today = dailies.date || "";
      setDailyQuests(dailies.quests || []);
      setClaimedQuests(dailies.claimed || []);
      setWeeklyChallenges(weekly.challenges || []);
      setUserProgress(weekly.user_progress || {});
      setClaimedTiers(weekly.claimed_tiers || []);
      setBadges(userBadges.badges || []);
      setRanks(allRanks.ranks || {});
    } catch (e) {
      setError(e.message || "Could not load campus wars data");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  const claimDaily = async (questId) => {
    setProcessingQuest(true);
    setError("");
    try {
      const res = await campusWarsApi.claimDailyQuest(questId);
      setClaimedQuests((prev) => [...prev, questId]);
      setLastReward({
        type: "daily",
        title: "Daily Quest Complete!",
        xp: res.xp_gained,
        coins: res.coins_gained,
      });
    } catch (e) {
      setError(e.message || "Could not claim quest");
    } finally {
      setProcessingQuest(false);
    }
  };

  const claimWeekly = async (tier) => {
    try {
      const res = await campusWarsApi.claimWeeklyReward(tier);
      setClaimedTiers((prev) => [...prev, tier]);
      setLastReward({
        type: "weekly",
        title: `T${tier} Unlocked!`,
        coins: res.coins_gained,
        rewards: res.rewards,
      });
    } catch (e) {
      setError(e.message || "Could not claim weekly reward");
    }
  };

  const getRankBadge = (xp) => {
    let current = "Recruit";
    let icon = "🌱";
    for (const [rank, data] of Object.entries(ranks)) {
      if (xp >= data.threshold) {
        current = rank;
        icon = data.icon;
      }
    }
    return { rank: current, icon };
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-base text-text-primary">
        <div className="animate-pulse text-nature-blossom">Loading Campus Wars...</div>
      </div>
    );
  }

  const myRank = getRankBadge(userProgress?.xp || 0);
  const earnedBadges = badges.filter((b) => b.earned);

  return (
    <div className="min-h-screen bg-surface-base text-text-primary px-4 py-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">⚔️ Campus Wars</h1>
          <p className="text-text-muted mt-2">Weekly college challenges, daily quests, and badge battles.</p>
        </div>

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4 bg-amber-500/10 border border-amber-500/30 rounded-lg py-2 px-4 max-w-md mx-auto">
            {error}
          </p>
        )}

        {/* Rank badge display */}
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="mb-8 bg-gradient-to-r from-[#EDF5E6] to-[#D9EFCF] border border-nature-leaf/30 rounded-2xl p-6 text-center"
        >
          <div className="text-5xl mb-2">{myRank.icon}</div>
          <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-600 to-orange-500">
            {myRank.rank}
          </h2>
          <p className="text-text-secondary mt-1">College: {user?.college || "Not set"}</p>
          <p className="text-text-muted text-sm">
            XP: {userProgress?.xp || 0} | Badges: {earnedBadges.length}/{badges.length}
          </p>
        </motion.div>

        {/* Tabs */}
        <div className="mb-6 border-b border-[#EDEAE0]">
          <nav className="flex gap-6">
            {[
              { key: "daily", label: "Daily Quests", icon: Calendar },
              { key: "weekly", label: "Weekly Challenges", icon: Flame },
              { key: "badges", label: "Badge Collection", icon: Gift },
            ].map((t) => {
              const Icon = t.icon;
              return (
                <button
                  key={t.key}
                  onClick={() => setActiveTab(t.key)}
                  className={"flex items-center gap-2 pb-3 px-1 text-sm font-medium transition " +
                    (activeTab === t.key
                      ? "text-nature-blossom border-b-2 border-[#4F8F57]"
                      : "text-text-muted hover:text-text-secondary")}
                >
                  <Icon className="h-4 w-4" />
                  {t.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Daily Quests */}
        <AnimatePresence mode="wait">
          {activeTab === "daily" && (
            <motion.div
              key="daily"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="space-y-4"
            >
              {dailyQuests.map((q) => {
                const claimed = claimedQuests.includes(q.id);
                return (
                  <motion.div
                    key={q.id}
                    className="bg-white border border-nature-leaf/20 rounded-xl p-5 flex items-center justify-between"
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex h-10 w-10 items-center justify-center rounded-full bg-surface-card">
                        <CheckCircle className="h-5 w-5 text-nature-blossom" />
                      </div>
                      <div>
                        <h3 className="font-bold text-text-primary">{q.title}</h3>
                        <p className="text-sm text-text-muted">{q.desc}</p>
                        <div className="flex items-center gap-3 mt-1">
                          <span className="text-xs text-amber-600">+{q.xp} XP</span>
                          <span className="text-xs text-yellow-600">+{q.coins} 🪙</span>
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => claimDaily(q.id)}
                      disabled={claimed || processingQuest}
                      className={"rounded-lg px-4 py-2 font-semibold text-sm transition " +
                        (claimed
                          ? "bg-surface-card text-text-muted cursor-not-allowed"
                          : processingQuest
                          ? "bg-surface-card text-text-muted cursor-wait"
                          : "bg-nature-leaf text-text-primary hover:bg-nature-moss")}
                    >
                      {claimed ? "Claimed" : processingQuest ? "..." : "Claim"}
                    </button>
                  </motion.div>
                );
              })}
            </motion.div>
          )}

          {activeTab === "weekly" && (
            <motion.div
              key="weekly"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="space-y-4"
            >
              {weeklyChallenges.map((ch) => {
                const canClaim = (userProgress?.xp || 0) >= ch.tier * 100;
                const claimed = claimedTiers.includes(ch.tier);
                return (
                  <motion.div
                    key={ch.id}
                    className="bg-white border border-nature-leaf/20 rounded-xl p-5"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="font-bold text-text-primary flex items-center gap-2">
                          <Flame className="h-4 w-4 text-amber-400" />
                          {ch.title}
                        </h3>
                        <span className="text-xs text-text-muted">Tier {ch.tier} challenge</span>
                      </div>
                      <span className={`text-xs font-bold px-2 py-1 rounded ${
                        claimed
                          ? "bg-green-500/20 text-green-600"
                          : canClaim
                          ? "bg-amber-500/20 text-amber-600"
                          : "bg-surface-card text-text-muted"
                      }`}>
                        {claimed ? "CLAIMED" : canClaim ? "AVAILABLE" : "LOCKED"}
                      </span>
                    </div>
                    <p className="text-sm text-text-secondary mb-3">{ch.desc}</p>
                    <div className="flex flex-wrap gap-2">
                      {ch.rewards.map((r, i) => (
                        <span key={i} className="text-xs px-2 py-1 bg-surface-card rounded">
                          {r.type === "coins" ? `${r.amount} 🪙` :
                           r.type === "xp_boost_2x_24h" ? "2x XP (24h)" :
                           r.type === "badge" ? `Badge: ${r.id}` :
                           r.type === "title" ? `Title: ${r.value}` :
                           r.type === "cosmetic" ? `Cosmetic: ${r.value}` : r.type}
                        </span>
                      ))}
                    </div>
                    {!claimed && canClaim && (
                      <button
                        onClick={() => claimWeekly(ch.tier)}
                        className="mt-3 rounded-lg bg-gradient-to-r from-amber-500 to-orange-500 px-4 py-2 text-sm font-bold text-slate-900 shadow hover:from-amber-400 hover:to-orange-400"
                      >
                        Claim T{ch.tier} Reward
                      </button>
                    )}
                  </motion.div>
                );
              })}
            </motion.div>
          )}

          {activeTab === "badges" && (
            <motion.div
              key="badges"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="space-y-6"
            >
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-text-primary">Earned Badges</h2>
                <span className="text-sm text-text-muted">{earnedBadges.length} / {badges.length} collected</span>
              </div>
              <div className="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-8 gap-4">
                {badges.map((b) => {
                  const color = b.tier === 3 ? "from-yellow-400 to-amber-500" :
                               b.tier === 2 ? "from-slate-300 to-slate-400" :
                               "from-amber-700 to-amber-800";
                  return (
                    <motion.div
                      key={b.id}
                      className={"rounded-xl p-2 text-center " +
                        (b.earned ? "bg-gradient-to-br " + color : "bg-surface-card border border-nature-leaf/20")}
                      animate={{ rotate: b.earned ? [0, 5, -5, 0] : 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <div className="text-2xl mb-1">
                        {b.earned ? "✨" : "🔒"}
                      </div>
                      <span className="text-xs text-text-secondary block truncate">
                        {b.tier === 3 ? "🥇" : b.tier === 2 ? "🥈" : "🥉"} {b.name.split(" ")[0]}
                      </span>
                    </motion.div>
                  );
                })}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Reward celebration */}
      <AnimatePresence>
        {lastReward && (
          <motion.div
            initial={{ opacity: 0, scale: 0.3 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.3 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-surface-2 backdrop-blur-sm"
            onClick={() => setLastReward(null)}
          >
            <motion.div
              className="bg-white border-2 border-yellow-400 rounded-3xl p-8 text-center max-w-sm mx-4 shadow-[0_0_40px_rgba(127,182,97,0.35)]"
              onClick={(e) => e.stopPropagation()}
            >
              <motion.div animate={{ scale: [1, 1.2, 1] }} className="text-6xl mb-4">
                {lastReward.type === "daily" ? "🎁" : "🏆"}
              </motion.div>
              <h3 className="text-2xl font-bold text-yellow-600 mb-2">{lastReward.title}</h3>
              <div className="space-y-2 text-text-secondary">
                {lastReward.xp && <p>⚡ +{lastReward.xp} XP</p>}
                {lastReward.coins && <p>🪙 +{lastReward.coins} Coins</p>}
                {lastReward.rewards && lastReward.rewards.map((r, i) => (
                  <p key={i}>
                    {r.type === "coins" ? `🪙 ${r.amount} Coins` :
                     r.type === "badge" ? `🎖️ Badge: ${r.id}` :
                     r.type === "title" ? `⭐ Title: ${r.value}` : r}
                  </p>
                ))}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
