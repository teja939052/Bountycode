import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { trendingChallengesApi } from "../services/api/trendingChallenges.ts";
import useAuthStore from "../store/authStore";
import { Flame, Sparkles, TrendingUp, Zap, Star, ChevronRight, RefreshCw } from "lucide-react";

export default function TrendingChallenges() {
  const user = useAuthStore((s) => s.user);
  const [feed, setFeed] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [engaging, setEngaging] = useState(null);
  const [campus, setCampus] = useState("");

  const loadData = useCallback(async () => {
    try {
      const [f, s] = await Promise.all([
        trendingChallengesApi.feed(10),
        trendingChallengesApi.stats(),
      ]);
      setFeed(f.feed || []);
      setStats(s);
      setCampus(f.campus || "");
    } catch (e) {
      setError(e.message || "Could not load trending feed");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleEngage = async (questionId) => {
    setEngaging(questionId);
    setError("");
    try {
      const res = await trendingChallengesApi.engage(questionId);
      setFeed((prev) =>
        prev.map((item) =>
          item.question_id === questionId
            ? { ...item, participants: (item.participants || 0) + 1, score: (item.score || 0) + res.bonus_xp }
            : item
        )
      );
      setStats((prev) => prev ? { ...prev, today_engaged: (prev.today_engaged || 0) + 1 } : prev);
    } catch (e) {
      setError(e.message || "Engagement failed");
    } finally {
      setEngaging(null);
    }
  };

  const difficultyColor = (diff) => {
    if (diff === "Hard") return "text-red-400 bg-red-500/10";
    if (diff === "Medium") return "text-amber-400 bg-amber-500/10";
    return "text-green-400 bg-green-500/10";
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
        <div className="animate-pulse text-indigo-300">Loading Trending...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white px-4 py-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold">
            <span className="bg-gradient-to-r from-orange-400 via-red-500 to-pink-500 bg-clip-text text-transparent">
              Trending Challenges
            </span>
          </h1>
          <p className="text-slate-400 mt-2">
            What's hot right now. Don't miss out — FOMO is real.
          </p>
          {campus && (
            <p className="text-sm text-indigo-300 mt-1">
              📍 {campus}
            </p>
          )}
        </div>

        {/* Stats */}
        {stats && (
          <div className="flex justify-center gap-6 mb-8">
            <div className="text-center">
              <div className="text-2xl font-bold text-amber-400">{stats.today_engaged || 0}</div>
              <div className="text-xs text-slate-500">Today Engaged</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-400">{stats.total_engaged || 0}</div>
              <div className="text-xs text-slate-500">Total Engaged</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-rose-400">{stats.daily_limit - (stats.today_engaged || 0)}</div>
              <div className="text-xs text-slate-500">Remaining Today</div>
            </div>
          </div>
        )}

        {error && (
          <p className="text-center text-amber-400 text-sm mb-4 bg-amber-500/10 border border-amber-500/30 rounded-lg py-2 px-4 max-w-md mx-auto">
            {error}
          </p>
        )}

        {/* Feed */}
        <div className="space-y-4">
          {feed.map((item, idx) => (
            <motion.div
              key={item.question_id + idx}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
              className="rounded-2xl border border-slate-700 bg-slate-900/60 p-5 hover:border-indigo-500/50 transition-all"
            >
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{item.icon}</span>
                  <div>
                    <h3 className="font-bold text-slate-200">{item.name}</h3>
                    <p className="text-xs text-slate-500">{item.description}</p>
                  </div>
                </div>
                <span className={`text-xs font-bold px-2 py-1 rounded-full ${difficultyColor(item.difficulty)}`}>
                  {item.difficulty}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 text-xs text-slate-400">
                  <span className="flex items-center gap-1">
                    <Star className="h-3 w-3 text-amber-400" />
                    {item.participants || 0} solving
                  </span>
                  <span className="flex items-center gap-1">
                    <TrendingUp className="h-3 w-3 text-emerald-400" />
                    {item.score || 0} pts
                  </span>
                  <span className="flex items-center gap-1">
                    <Flame className="h-3 w-3 text-red-400" />
                    {item.topic}
                  </span>
                </div>
                <button
                  onClick={() => handleEngage(item.question_id)}
                  disabled={engaging === item.question_id}
                  className="rounded-lg bg-indigo-600 px-4 py-2 text-xs font-bold text-white hover:bg-indigo-500 disabled:opacity-50 flex items-center gap-1"
                >
                  {engaging === item.question_id ? (
                    <RefreshCw className="h-3 w-3 animate-spin" />
                  ) : (
                    <Zap className="h-3 w-3" />
                  )}
                  Engage +15 XP
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        {feed.length === 0 && !loading && (
          <p className="text-center text-slate-500 mt-8">
            No trending challenges right now. Check back soon!
          </p>
        )}
      </div>
    </div>
  );
}