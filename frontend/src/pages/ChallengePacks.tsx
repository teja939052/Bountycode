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
      const data = await api.browseQuestions({ type: "coding", limit: 100 });
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
      <div className="min-h-screen flex items-center justify-center bg-surface-base">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-nature-leaf/30 border-t-[#4F8F57] rounded-full animate-spin" />
          <span className="text-sm font-mono text-text-muted">Opening packs...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-3">
<div className="p-3 bg-gradient-to-br from-[#D9EFCF] to-[#EDF5E6] rounded-2xl border border-nature-leaf/30">
          <Sword className="w-7 h-7 text-nature-blossom" />
            </div>
            <div>
              <h1 className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-[#2E6B35] via-[#4F8F57] to-[#7BB661] bg-clip-text text-transparent">
                Challenge Packs
              </h1>
              <p className="text-text-muted text-sm mt-1">
                Collect, solve, and master coding challenges — trading card style
              </p>
            </div>
          </div>
        </motion.div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3 mb-8">
          <div className="flex items-center gap-1.5 bg-white border border-nature-leaf/20 rounded-xl p-1">
            {RARITY_FILTERS.map((r) => (
              <button
                key={r}
                onClick={() => setRarityFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  rarityFilter === r
? "bg-nature-leaf text-text-primary shadow-lg shadow-[#4F8F57]/20"
            : "text-text-muted hover:text-text-primary"
                }`}
              >
                {r === "all" ? "All" : r.charAt(0).toUpperCase() + r.slice(1)}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-1.5 bg-white border border-nature-leaf/20 rounded-xl p-1">
            {DIFFICULTY_FILTERS.map((d) => (
              <button
                key={d}
                onClick={() => setDifficultyFilter(d)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                  difficultyFilter === d
                    ? "bg-amber-600 text-text-primary shadow-lg shadow-amber-600/20"
                    : "text-text-muted hover:text-text-primary"
                }`}
              >
                {d === "all" ? "All" : d.charAt(0).toUpperCase() + d.slice(1)}
              </button>
            ))}
          </div>

          <div className="flex-1 min-w-[200px] max-w-xs">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
              <input
                type="text"
                placeholder="Search challenges..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-white border border-nature-leaf/20 rounded-xl py-2 pl-10 pr-4 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-nature-leaf/60 transition-colors"
              />
            </div>
          </div>

          <div className="flex items-center gap-1 bg-white border border-nature-leaf/20 rounded-xl p-1">
            <button
              onClick={() => setViewMode("grid")}
              className={`p-2 rounded-lg transition-all ${viewMode === "grid" ? "bg-nature-leaf text-text-primary" : "text-text-muted hover:text-text-secondary"}`}
            >
              <Grid3x3 className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode("list")}
              className={`p-2 rounded-lg transition-all ${viewMode === "list" ? "bg-nature-leaf text-text-primary" : "text-text-muted hover:text-text-secondary"}`}
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Stats bar */}
        <div className="flex items-center justify-between mb-6 text-sm">
          <span className="text-text-muted">
            <span className="font-bold text-text-primary">{filtered.length}</span> challenges
            {filtered.length !== challenges.length && (
              <span className="text-text-muted"> (filtered from {challenges.length})</span>
            )}
          </span>
          <div className="flex items-center gap-3 text-xs text-text-muted">
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-[#9CA3AF]" /> Common
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500" /> Rare
            </span>
            <span className="flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-nature-leaf" /> Epic
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
                className="flex items-center gap-4 bg-white border border-nature-leaf/20 rounded-2xl p-4 hover:bg-surface-base hover:border-nature-leaf/30 transition-all cursor-pointer"
              >
                <div className="text-2xl">{challenge.icon || "⚔️"}</div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-sm text-text-primary truncate">{challenge.title}</h3>
                  <p className="text-xs text-text-muted truncate">{challenge.description || challenge.topic || ""}</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                    challenge.rarity === "legendary" ? "bg-[#FCEFD8] text-nature-sun" :
                    challenge.rarity === "rare" ? "bg-[#E8F1FA] text-nature-sky" :
                    challenge.rarity === "epic" ? "bg-nature-bark text-nature-blossom" :
                    "bg-surface-card text-text-muted"
                  }`}>
                    {challenge.rarity}
                  </span>
                  <span className={`px-2 py-0.5 rounded text-[10px] font-mono ${
                    challenge.difficulty === "hard" ? "text-red-600 bg-red-100" :
                    challenge.difficulty === "medium" ? "text-nature-sun bg-amber-100" :
                    "text-nature-blossom bg-emerald-100"
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
<Sword className="w-12 h-12 mx-auto text-[#C5C0B2] mb-4" />
          <p className="text-text-muted text-sm">No challenges match your filters.</p>
          <button
            onClick={() => { setRarityFilter("all"); setDifficultyFilter("all"); setSearchQuery(""); }}
            className="mt-4 px-4 py-2 bg-white hover:bg-surface-card text-text-secondary border border-nature-leaf/20 rounded-lg text-sm transition-colors"
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
          className="fixed inset-0 bg-surface-2 backdrop-blur-sm z-50 flex items-center justify-center p-4"
          onClick={() => setSelectedChallenge(null)}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            onClick={(e) => e.stopPropagation()}
            className="bg-white border border-nature-leaf/20 rounded-2xl w-full max-w-lg max-h-[80vh] overflow-y-auto shadow-2xl p-6"
          >
            <div className="flex items-start gap-4 mb-4">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[#D9EFCF] to-[#EDF5E6] flex items-center justify-center text-3xl shrink-0">
                {selectedChallenge.icon || "⚔️"}
              </div>
              <div className="flex-1 min-w-0">
                <h2 className="text-xl font-bold text-text-primary">{selectedChallenge.title}</h2>
                <div className="flex flex-wrap items-center gap-2 mt-2">
                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                    selectedChallenge.rarity === "legendary" ? "bg-[#FCEFD8] text-nature-sun border border-amber-500/30" :
                    selectedChallenge.rarity === "epic" ? "bg-nature-bark text-nature-blossom border border-nature-leaf/30" :
                    selectedChallenge.rarity === "rare" ? "bg-[#E8F1FA] text-nature-sky border border-blue-500/30" :
                    "bg-surface-card text-text-muted border border-nature-leaf/20"
                  }`}>
                    {selectedChallenge.rarity}
                  </span>
                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono border ${
                    selectedChallenge.difficulty === "hard" ? "text-red-600 bg-red-100 border-red-500/30" :
                    selectedChallenge.difficulty === "medium" ? "text-nature-sun bg-amber-100 border-amber-500/30" :
                    "text-nature-blossom bg-emerald-100 border-emerald-500/30"
                  }`}>
                    {selectedChallenge.difficulty}
                  </span>
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono bg-nature-bark text-nature-blossom border border-nature-leaf/30 flex items-center gap-1">
                    <Zap className="w-3 h-3" /> +{selectedChallenge.xp_reward} XP
                  </span>
                </div>
              </div>
            </div>

            <div className="prose prose-sm max-w-none text-text-secondary mb-6">
              {selectedChallenge.statement || selectedChallenge.description || "Solve this coding challenge to earn XP and collect this card."}
            </div>

            {selectedChallenge.tags && selectedChallenge.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-6">
                {selectedChallenge.tags.map((tag) => (
                  <span key={tag} className="px-2.5 py-1 rounded-lg bg-surface-card text-[11px] text-text-secondary font-mono border border-nature-leaf/20">
                    {tag}
                  </span>
                ))}
              </div>
            )}

            <div className="flex items-center gap-3">
              <Link
                to={selectedChallenge.id ? `/solve/${selectedChallenge.id}` : "/compiler"}
                className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-[#4F8F57] to-[#7BB661] hover:from-[#3F7A47] hover:to-[#4F8F57] text-text-primary rounded-xl font-medium text-sm transition-all shadow-lg shadow-[#4F8F57]/20"
                onClick={() => setSelectedChallenge(null)}
              >
                <Sparkles className="w-4 h-4" /> Solve Challenge
              </Link>
              <button
                onClick={() => setSelectedChallenge(null)}
                className="px-4 py-3 bg-white hover:bg-surface-card text-text-secondary border border-nature-leaf/20 rounded-xl text-sm transition-colors"
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
