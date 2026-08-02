import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import api from "../services/api";
import ChallengePackCard from "../components/ChallengePackCard";
import {
  Sparkles, Sword, Zap, Star, Filter, Search,
  Grid3x3, List, SlidersHorizontal, ArrowLeft,
} from "lucide-react";

const RARITY_FILTERS = ["all", "common", "uncommon", "rare", "epic", "legendary"];
const DIFFICULTY_FILTERS = ["all", "easy", "medium", "hard"];

export default function ChallengePacks() {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rarityFilter, setRarityFilter] = useState("all");
  const [difficultyFilter, setDifficultyFilter] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [viewMode, setViewMode] = useState("grid");
  const [selectedChallenge, setSelectedChallenge] = useState(null);

  useEffect(() => { loadChallenges(); }, []);

  const loadChallenges = async () => {
    setLoading(true); setError(null);
    try {
      const data = await api.browseQuestions({ type: "coding", limit: 50 });
      const enhanced = (data.questions || data.problems || []).map((q) => ({
        ...q,
        title: q.question_title || q.title,
        rarity: getRarity(q.difficulty),
        icon: getIcon(q.topic || q.category || ""),
        tags: [q.topic, q.company].filter(Boolean),
        xp_reward: q.difficulty === "hard" ? 100 : q.difficulty === "medium" ? 50 : 25,
        locked: false,
      }));
      setChallenges(enhanced);
    } catch (err) {
      setError("Failed to load challenge packs.");
    } finally {
      setLoading(false);
    }
  };

  const getRarity = (difficulty) => {
    const map = { easy: "common", medium: "rare", hard: "legendary" };
    return map[difficulty] || "common";
  };

  const getIcon = (topic) => {
    const icons = {
      "Arrays": "📊", "Strings": "📝", "Linked Lists": "🔗",
      "Trees": "🌳", "Graphs": "🕸️", "Dynamic Programming": "🧩",
      "Sorting": "🔄", "Searching": "🔍", "Stack": "📚",
      "Queue": "🚶", "Hash Table": "🔑", "Math": "🔢",
      "Recursion": "🔄", "Greedy": "💰", "Binary": "0️⃣1️⃣",
      "Matrix": "🧮",
    };
    return icons[topic] || "⚔️";
  };

  const filtered = challenges.filter((c) => {
    if (rarityFilter !== "all" && c.rarity !== rarityFilter) return false;
    if (difficultyFilter !== "all" && c.difficulty !== difficultyFilter) return false;
    if (searchQuery && !(c.title || "").toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0a0a0f]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin" />
          <span className="text-sm font-mono text-slate-400">Opening packs...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-slate-100">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-3">
            <div className="p-3 bg-gradient-to-br from-purple-500/20 to-pink-500/20 rounded-2xl border border-purple-500/30">
              <Sword className="w-7 h-7 text-purple-400" />
            </div>
            <div>
              <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-white via-purple-200 to-pink-200 bg-clip-text text-transparent">
                Challenge Packs
              </h1>
              <p className="text-slate-400 text-sm mt-1">
                Collect, solve, and master coding challenges — trading card style
              </p>
            </div>
          </div>
        </motion.div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3 mb-8">
          <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {RARITY_FILTERS.map((r) => (
              <button
                key={r}
                onClick={() => setRarityFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  rarityFilter === r
                    ? "bg-purple-600 text-white shadow-lg shadow-purple-600/20"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {r === "all" ? "All" : r.charAt(0).toUpperCase() + r.slice(1)}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 rounded-xl p-1">
            {DIFFICULTY_FILTERS.map((d) => (
              <button
                key={d}
                onClick={() => setDifficultyFilter(d)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  difficultyFilter === d
                    ? "bg-amber-600 text-white shadow-lg shadow-amber-600/20"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {d === "all" ? "All" : d.charAt(0).toUpperCase() + d.slice(1)}
              </button>
            ))}
          </div>

          <div className="flex-1 min-w-[200px] max-w-xs">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                type="text"
                placeholder="Search challenges..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl py-2 pl-10 pr-4 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-purple-500/50 transition-colors"
              />
            </div>
          </div>

          <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1">
            <button
              onClick={() => setViewMode("grid")}
              className={`p-2 rounded-lg transition-all ${viewMode === "grid" ? "bg-slate-800 text-white" : "text-slate-500 hover:text-slate-300"}`}
            >
              <Grid3x3 className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`p-2 rounded-lg transition-all ${viewMode === "list" ? "bg-slate-800 text-white" : "text-slate-500 hover:text-slate-300"}`}
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Stats bar */}
        <div className="flex items-center justify-between mb-6 text-sm">
          <span className="text-slate-400">
            <span className="font-bold text-white">{filtered.length}</span> challenges
            {filtered.length !== challenges.length && (
              <span className="text-slate-500"> (filtered from {challenges.length})</span>
            )}
          </span>
          <div className="flex items-center gap-3 text-xs text-slate-500">
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-slate-600" /> Common
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500" /> Rare
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-purple-500" /> Epic
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-amber-500" /> Legendary
            </span>
          </div>
        </div>

        {/* Cards grid */}
        {viewMode === "grid" ? (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
            {filtered.map((challenge, idx) => (
              <ChallengePackCard
                key={challenge.id || challenge._id || idx}
                challenge={challenge}
                index={idx}
                compact={true}
                onOpen={(c) => setSelectedChallenge(c)}
              />
            ))}
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map((challenge, idx) => (
              <motion.div
                key={challenge.id || challenge._id || idx}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.03 }}
                onClick={() => setSelectedChallenge(challenge)}
                className="flex items-center gap-4 bg-slate-900/80 border border-slate-800 rounded-xl p-4 hover:bg-slate-800/80 hover:border-slate-700 transition-all cursor-pointer"
              >
                <div className="text-2xl">{challenge.icon || "⚔️"}</div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-sm text-white truncate">{challenge.title}</h3>
                  <p className="text-xs text-slate-500 truncate">{challenge.description || challenge.topic || ""}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                    challenge.rarity === "legendary" ? "bg-amber-700/30 text-amber-400" :
                    challenge.rarity === "rare" ? "bg-blue-700/30 text-blue-400" :
                    challenge.rarity === "epic" ? "bg-purple-700/30 text-purple-400" :
                    "bg-slate-700/30 text-slate-400"
                  }`}>
                    {challenge.rarity}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${
                    challenge.difficulty === "hard" ? "text-red-400 bg-red-900/20" :
                    challenge.difficulty === "medium" ? "text-amber-400 bg-amber-900/20" :
                    "text-emerald-400 bg-emerald-900/20"
                  }`}>
                    {challenge.difficulty}
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {filtered.length === 0 && (
          <div className="text-center py-20">
            <Sword className="w-12 h-12 mx-auto text-slate-700 mb-4" />
            <p className="text-slate-500 text-sm">No challenges match your filters.</p>
            <button
              onClick={() => { setRarityFilter("all"); setDifficultyFilter("all"); setSearchQuery(""); }}
              className="mt-4 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm transition-colors"
            >
              Clear Filters
            </button>
          </div>
        )}
      </div>

      {/* Challenge detail modal */}
      {selectedChallenge && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedChallenge(null)}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-slate-900 border border-slate-800 rounded-2xl w-full max-w-lg max-h-[80vh] overflow-y-auto shadow-2xl p-6"
          >
            <div className="flex items-start gap-4 mb-4">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500/20 to-pink-500/20 flex items-center justify-center text-3xl shrink-0">
                {selectedChallenge.icon || "⚔️"}
              </div>
              <div className="flex-1 min-w-0">
                <h2 className="text-xl font-bold text-white">{selectedChallenge.title}</h2>
                <div className="flex flex-wrap items-center gap-2 mt-2">
                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                    selectedChallenge.rarity === "legendary" ? "bg-amber-700/30 text-amber-400 border border-amber-500/30" :
                    selectedChallenge.rarity === "epic" ? "bg-purple-700/30 text-purple-400 border border-purple-500/30" :
                    selectedChallenge.rarity === "rare" ? "bg-blue-700/30 text-blue-400 border border-blue-500/30" :
                    "bg-slate-700/30 text-slate-400 border border-slate-600/30"
                  }`}>
                    {selectedChallenge.rarity}
                  </span>
                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono border ${
                    selectedChallenge.difficulty === "hard" ? "text-red-400 bg-red-900/20 border-red-500/30" :
                    selectedChallenge.difficulty === "medium" ? "text-amber-400 bg-amber-900/20 border-amber-500/30" :
                    "text-emerald-400 bg-emerald-900/20 border-emerald-500/30"
                  }`}>
                    {selectedChallenge.difficulty}
                  </span>
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono bg-indigo-900/20 text-indigo-400 border border-indigo-500/30 flex items-center gap-1">
                    <Zap className="w-3 h-3" /> +{selectedChallenge.xp_reward} XP
                  </span>
                </div>
              </div>
            </div>

            <div className="prose prose-sm prose-invert max-w-none text-slate-300 mb-6">
              {selectedChallenge.statement || selectedChallenge.description || "Solve this coding challenge to earn XP and collect this card."}
            </div>

            {selectedChallenge.tags && selectedChallenge.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-6">
                {selectedChallenge.tags.map((tag) => (
                  <span key={tag} className="px-2.5 py-1 rounded-lg bg-slate-800 text-[11px] text-slate-300 font-mono border border-slate-700/50">
                    {tag}
                  </span>
                ))}
              </div>
            )}

            <div className="flex items-center gap-3">
              <Link
                to={selectedChallenge.id ? `/solve/${selectedChallenge.id}` : "/compiler"}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-500 hover:to-pink-500 text-white rounded-xl font-medium text-sm transition-all shadow-lg shadow-purple-600/20"
                onClick={() => setSelectedChallenge(null)}
              >
                <Sparkles className="w-4 h-4" /> Solve Challenge
              </Link>
              <button
                onClick={() => setSelectedChallenge(null)}
                className="px-4 py-3 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-sm transition-colors"
              >
                Close
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}
