import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BookOpen, Sparkles, Gift, Zap, Globe2, CalendarDays,
  CheckCircle2, Lock, Trophy, Loader2, PartyPopper, Award, Rocket, Cpu,
} from "lucide-react";
import { collectionApi, eventsApi } from "../services/api/collectionEvents.ts";
import useAuthStore from "../store/authStore";
import useTrack from "../hooks/useTrack";

const RARITY_COLORS = {
  common: "text-slate-300 border-slate-400/40 bg-slate-400/10",
  rare: "text-indigo-300 border-indigo-400/40 bg-indigo-400/10",
  epic: "text-purple-300 border-purple-400/40 bg-purple-400/10",
  legendary: "text-amber-300 border-amber-400/40 bg-amber-400/10",
};

const TABS = [
  { key: "collection", label: "Collection Book", icon: BookOpen },
  { key: "events", label: "Live Events", icon: Sparkles },
];

export default function CollectionEvents() {
  const user = useAuthStore((s) => s.user);
  const track = useTrack();
  const [activeTab, setActiveTab] = useState("collection");
  const [error, setError] = useState("");

  const [collection, setCollection] = useState(null);
  const [collectionLoading, setCollectionLoading] = useState(true);
  const [collectingId, setCollectingId] = useState(null);
  const [claiming, setClaiming] = useState(false);
  const [claimResult, setClaimResult] = useState(null);

  const [randomEvent, setRandomEvent] = useState(null);
  const [research, setResearch] = useState(null);
  const [festival, setFestival] = useState(null);
  const [eventsLoading, setEventsLoading] = useState(true);
  const [contributeAmount, setContributeAmount] = useState(100);
  const [contributing, setContributing] = useState(false);
  const [luckyRolling, setLuckyRolling] = useState(false);
  const [luckyResult, setLuckyResult] = useState(null);

  const loadCollection = useCallback(async () => {
    setCollectionLoading(true);
    setError("");
    try {
      const data = await collectionApi.get();
      setCollection(data);
    } catch (e) {
      setError(e.message || "Failed to load collection");
    } finally {
      setCollectionLoading(false);
    }
  }, []);

  const loadEvents = useCallback(async () => {
    setEventsLoading(true);
    setError("");
    try {
      const [randomData, researchData, festivalData] = await Promise.all([
        eventsApi.random().catch(() => null),
        eventsApi.research().catch(() => null),
        eventsApi.festival().catch(() => null),
      ]);
      setRandomEvent(randomData);
      setResearch(researchData);
      setFestival(festivalData);
    } catch (e) {
      setError(e.message || "Failed to load live events");
    } finally {
      setEventsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (activeTab === "collection") loadCollection();
    else loadEvents();
  }, [activeTab, loadCollection, loadEvents]);

  const handleEarn = async (companyId) => {
    if (!user) return;
    setCollectingId(companyId);
    setError("");
    try {
      const data = await collectionApi.earn(companyId);
      track("collection", "earn");
      setCollection((prev) => ({
        ...prev,
        owned_company_ids: data.owned_company_ids,
        xp_earned: data.xp_earned,
        completion_percent: data.completion_percent,
        complete: data.complete,
        completion_reward_claimed: data.completion_reward_claimed,
        date_first_completed: data.date_first_completed,
      }));
    } catch (e) {
      setError(e.message || "Failed to collect card");
    } finally {
      setCollectingId(null);
    }
  };

  const handleClaim = async () => {
    if (!user) return;
    setClaiming(true);
    setError("");
    try {
      const result = await collectionApi.complete();
      track("collection", "complete");
      setClaimResult(result);
      setCollection((prev) => ({
        ...prev,
        completion_reward_claimed: result.complete || prev.completion_reward_claimed,
        date_first_completed: result.date_first_completed || prev.date_first_completed,
      }));
    } catch (e) {
      setError(e.message || "Failed to claim reward");
    } finally {
      setClaiming(false);
    }
  };

  const handleContribute = async () => {
    if (!user) return;
    setContributing(true);
    setError("");
    try {
      const data = await eventsApi.contribute(contributeAmount);
      track("events", "research_contribute");
      setResearch(data);
    } catch (e) {
      setError(e.message || "Failed to contribute");
    } finally {
      setContributing(false);
    }
  };

  const handleLucky = async () => {
    if (!user) return;
    setLuckyRolling(true);
    setError("");
    setLuckyResult(null);
    try {
      const data = await eventsApi.lucky(3);
      track("events", "lucky");
      setLuckyResult(data);
    } catch (e) {
      setError(e.message || "Lucky compile failed");
    } finally {
      setLuckyRolling(false);
    }
  };

  const ownedCount = collection?.owned_company_ids?.length || 0;
  const completion = collection?.completion_percent || 0;
  const complete = collection?.complete || false;

  return (
    <div className="min-h-screen bg-slate-950">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-display font-bold text-white flex items-center gap-3">
              <Sparkles className="w-8 h-8 text-emerald-400" />
              Collection &amp; Events
            </h1>
            <p className="text-slate-400 mt-1">
              Collect company cards, chase global goals, and get lucky.
            </p>
          </div>
          {user && (
            <span className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 bg-white/5 text-xs font-mono text-slate-300">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
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
                    ? "border-emerald-500/50 bg-emerald-500/15 text-emerald-200"
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
          {activeTab === "collection" && (
            <motion.div
              key="collection"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
            >
              {collectionLoading || !collection ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center py-20 text-slate-500">
                  <Loader2 className="w-6 h-6 animate-spin mr-2" />
                  Loading collection...
                </div>
              ) : (
                <div>
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-6 mb-6">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-3">
                      <h2 className="flex items-center gap-2 text-lg font-display font-semibold text-white">
                        <Trophy className="w-5 h-5 text-amber-400" />
                        Company Card Collection
                      </h2>
                      <span className="text-sm font-mono text-slate-400">
                        {ownedCount} / {collection.cards?.length || 6} collected
                      </span>
                    </div>
                    <div className="h-4 rounded-full bg-slate-900 border border-white/10 overflow-hidden">
                      <motion.div
                        className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-indigo-500"
                        initial={{ width: "0%" }}
                        animate={{ width: `${completion}%` }}
                        transition={{ type: "spring", stiffness: 60, damping: 20 }}
                      />
                    </div>
                    <p className="text-right text-xs font-mono text-slate-500 mt-2">
                      {completion}% complete
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
                    {collection.cards.map((card) => {
                      const owned = collection.owned_company_ids.includes(card.id);
                      return (
                        <motion.div
                          key={card.id}
                          initial={{ opacity: 0, y: 12 }}
                          animate={{ opacity: 1, y: 0 }}
                          whileHover={{ y: -4 }}
                          className={`rounded-2xl border p-5 transition-all ${
                            owned
                              ? "border-emerald-500/60 bg-emerald-500/10 shadow-[0_0_24px_rgba(16,185,129,0.35)]"
                              : "border-white/10 bg-white/5"
                          }`}
                        >
                          <div className="flex items-start justify-between mb-4">
                            <div
                              className={`w-12 h-12 rounded-2xl border flex items-center justify-center text-2xl ${
                                owned
                                  ? "border-emerald-400/40 bg-emerald-400/10"
                                  : "border-white/10 bg-slate-950/60 grayscale opacity-60"
                              }`}
                            >
                              {owned ? card.emoji : <Lock className="w-5 h-5 text-slate-500" />}
                            </div>
                            <span
                              className={`px-2.5 py-1 rounded-full text-[10px] font-mono uppercase tracking-wider border ${
                                owned
                                  ? RARITY_COLORS[card.rarity] || RARITY_COLORS.common
                                  : "text-slate-500 border-white/10 bg-white/5"
                              }`}
                            >
                              {card.rarity}
                            </span>
                          </div>
                          <h3
                            className={`font-display font-bold text-lg mb-1 ${
                              owned ? "text-emerald-300" : "text-slate-400"
                            }`}
                          >
                            {card.company}
                          </h3>
                          <p className={`text-xs leading-relaxed mb-4 ${owned ? "text-slate-300" : "text-slate-500"}`}>
                            {card.description}
                          </p>
                          {owned ? (
                            <span className="flex items-center gap-1.5 text-xs font-mono text-emerald-400">
                              <CheckCircle2 className="w-4 h-4" />
                              Collected · +25 XP
                            </span>
                          ) : (
                            <button
                              onClick={() => handleEarn(card.id)}
                              disabled={!user || collectingId === card.id}
                              className="flex items-center gap-2 px-4 py-2 rounded-xl border border-white/10 bg-white/5 text-xs font-semibold text-slate-300 hover:border-emerald-500/40 hover:text-emerald-300 disabled:opacity-40 transition-all"
                            >
                              {collectingId === card.id ? (
                                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                              ) : (
                                <Gift className="w-3.5 h-3.5" />
                              )}
                              {user ? "Collect Card" : "Sign in to collect"}
                            </button>
                          )}
                        </motion.div>
                      );
                    })}
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-emerald-500/10 via-white/5 to-indigo-500/10 p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                      <h3 className="flex items-center gap-2 text-base font-display font-semibold text-white mb-1">
                        <Award className="w-4 h-4 text-amber-400" />
                        Collection Completion Reward
                      </h3>
                      <p className="text-sm text-slate-400">
                        Own all 6 company cards to claim{" "}
                        <span className="font-mono text-amber-300">+500 XP</span>
                        {collection.date_first_completed && (
                          <span className="block text-xs text-slate-500 mt-1">
                            First completed:{" "}
                            {new Date(collection.date_first_completed).toLocaleDateString()}
                          </span>
                        )}
                      </p>
                    </div>
                    {complete ? (
                      collection.completion_reward_claimed || claimResult ? (
                        <motion.div
                          initial={{ scale: 0.9, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-emerald-500/40 bg-emerald-500/10 text-sm font-mono text-emerald-300"
                        >
                          <PartyPopper className="w-4 h-4" />
                          Reward claimed
                        </motion.div>
                      ) : (
                        <button
                          onClick={handleClaim}
                          disabled={!user || claiming}
                          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-indigo-500 text-sm font-semibold text-slate-950 hover:from-emerald-400 hover:to-indigo-400 disabled:opacity-40 transition-all"
                        >
                          {claiming ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : (
                            <Gift className="w-4 h-4" />
                          )}
                          Claim Completion Reward
                        </button>
                      )
                    ) : (
                      <span className="flex items-center gap-2 text-xs font-mono text-slate-500">
                        <Lock className="w-3.5 h-3.5" />
                        Collect all 6 cards to unlock
                      </span>
                    )}
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === "events" && (
            <motion.div
              key="events"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.2 }}
            >
              {eventsLoading ? (
                <div className="rounded-2xl border border-white/10 bg-white/5 flex items-center justify-center py-20 text-slate-500">
                  <Loader2 className="w-6 h-6 animate-spin mr-2" />
                  Loading events...
                </div>
              ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-indigo-500/15 via-white/5 to-emerald-500/15 p-6">
                    <h3 className="flex items-center gap-2 text-sm font-mono uppercase tracking-wider text-indigo-300 mb-4">
                      <Zap className="w-4 h-4" />
                      Active Random Event
                    </h3>
                    {randomEvent ? (
                      <div className="flex items-start gap-4">
                        <div className="text-5xl">{randomEvent.emoji}</div>
                        <div>
                          <h2 className="text-xl font-display font-bold text-white mb-1">
                            {randomEvent.name}
                          </h2>
                          <p className="text-sm text-slate-300 mb-2">{randomEvent.effect}</p>
                          <p className="text-xs font-mono text-slate-500">
                            Expires{" "}
                            {new Date(randomEvent.expires_at).toLocaleTimeString()}
                          </p>
                        </div>
                      </div>
                    ) : (
                      <p className="text-sm text-slate-500">No active event.</p>
                    )}
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-white/5 p-6">
                    <h3 className="flex items-center gap-2 text-sm font-mono uppercase tracking-wider text-emerald-300 mb-4">
                      <CalendarDays className="w-4 h-4" />
                      Upcoming Festival
                    </h3>
                    {festival ? (
                      <div>
                        <div className="flex items-start gap-4 mb-3">
                          <div className="text-5xl">{festival.emoji}</div>
                          <div>
                            <h2 className="text-xl font-display font-bold text-white mb-1">
                              {festival.name}
                            </h2>
                            <p className="text-sm text-slate-300 mb-2">
                              {festival.date_range}
                            </p>
                            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full border border-amber-400/40 bg-amber-400/10 text-xs font-mono text-amber-300">
                              <Rocket className="w-3.5 h-3.5" />
                              {festival.bonus_multiplier}x XP boost
                            </span>
                          </div>
                        </div>
                      </div>
                    ) : (
                      <p className="text-sm text-slate-500">No upcoming festival.</p>
                    )}
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-white/5 p-6 lg:col-span-2">
                    <h3 className="flex items-center gap-2 text-sm font-mono uppercase tracking-wider text-emerald-300 mb-4">
                      <Globe2 className="w-4 h-4" />
                      Global Research Event
                    </h3>
                    {research ? (
                      <div>
                        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
                          <div>
                            <h2 className="text-lg font-display font-semibold text-white flex items-center gap-2">
                              <span>{research.emoji}</span>
                              {research.title}
                            </h2>
                            <p className="text-xs text-slate-500 mt-1">
                              Community goal reward:{" "}
                              <span className="text-amber-300 font-mono">
                                {research.reward_name}
                              </span>
                            </p>
                          </div>
                          <span className="text-sm font-mono text-slate-300">
                            {Number(research.contribution || 0).toLocaleString()}{" "}
                            <span className="text-slate-500">
                              / {Number(research.goal || 0).toLocaleString()}
                            </span>
                          </span>
                        </div>
                        <div className="h-4 rounded-full bg-slate-900 border border-white/10 overflow-hidden mb-3">
                          <motion.div
                            className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-indigo-500"
                            initial={{ width: "0%" }}
                            animate={{ width: `${Math.min(100, research.progress_percent || 0)}%` }}
                            transition={{ type: "spring", stiffness: 60, damping: 20 }}
                          />
                        </div>
                        <p className="text-right text-xs font-mono text-slate-500 mb-5">
                          {research.progress_percent}% complete
                        </p>
                        <div className="flex flex-wrap items-center gap-3">
                          <input
                            type="number"
                            min={1}
                            value={contributeAmount}
                            onChange={(e) => setContributeAmount(Number(e.target.value))}
                            className="w-32 px-3.5 py-2.5 rounded-xl bg-slate-950/60 border border-white/10 text-sm text-white focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/30"
                          />
                          <button
                            onClick={handleContribute}
                            disabled={!user || contributing || contributeAmount < 1}
                            className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-indigo-500 text-sm font-semibold text-slate-950 hover:from-emerald-400 hover:to-indigo-400 disabled:opacity-40 transition-all"
                          >
                            {contributing ? (
                              <Loader2 className="w-4 h-4 animate-spin" />
                            ) : (
                              <Globe2 className="w-4 h-4" />
                            )}
                            {user ? "Contribute" : "Sign in to contribute"}
                          </button>
                          {!user && (
                            <span className="text-xs text-slate-500">
                              Research is public — sign in to contribute.
                            </span>
                          )}
                        </div>
                      </div>
                    ) : (
                      <p className="text-sm text-slate-500">No active research event.</p>
                    )}
                  </div>

                  <div className="rounded-2xl border border-white/10 bg-gradient-to-br from-amber-500/10 via-white/5 to-emerald-500/10 p-6 lg:col-span-2">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                      <div>
                        <h3 className="flex items-center gap-2 text-sm font-mono uppercase tracking-wider text-amber-300 mb-2">
                          <Cpu className="w-4 h-4" />
                          Golden Compiler Easter Egg
                        </h3>
                        <p className="text-sm text-slate-300">
                          Every compile has a{" "}
                          <span className="font-mono text-amber-300">2% chance</span> of
                          summoning the legendary{" "}
                          <span className="text-amber-200">Golden Compiler</span> for +500 XP.
                        </p>
                        {luckyResult && (
                          <div
                            className={`mt-3 px-4 py-2.5 rounded-xl border text-sm font-mono ${
                              luckyResult.lucky
                                ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-300"
                                : "border-white/10 bg-white/5 text-slate-400"
                            }`}
                          >
                            {luckyResult.message}
                          </div>
                        )}
                      </div>
                      <button
                        onClick={handleLucky}
                        disabled={!user || luckyRolling}
                        className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-orange-500 text-sm font-bold text-slate-950 hover:from-amber-400 hover:to-orange-400 disabled:opacity-40 transition-all"
                      >
                        {luckyRolling ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <Cpu className="w-4 h-4" />
                        )}
                        {user ? "Try Lucky Compile" : "Sign in to roll"}
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="mt-10 flex items-center justify-center gap-2 text-xs text-slate-500 font-mono">
          <Sparkles className="w-3.5 h-3.5" />
          Random events reset hourly · Festivals rotate monthly
        </div>
      </div>
    </div>
  );
}
