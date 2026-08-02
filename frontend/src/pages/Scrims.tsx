import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import ScrimPlayer from "../components/ScrimPlayer";
import Skeleton from "../components/ui/Skeleton";
import {
  Search, Clock, User, ThumbsUp, Play, Video, ChevronLeft, ChevronRight,
  Filter, X, Sparkles, Code2, BookOpen, Layers, GitBranch,
  Database, Share2, Hash, SlidersHorizontal,
} from "lucide-react";

const TOPICS = [
  "arrays", "linked-lists", "stack", "graph", "sorting", "dp",
  "sql", "system-design", "strings", "trees", "recursion", "binary-search"
];

const DIFFICULTIES = ["beginner", "intermediate", "advanced"];
const LANGUAGES = ["python", "javascript", "java", "cpp", "sql"];

const TOPIC_ICONS = {
  "arrays": Layers, "linked-lists": GitBranch, "stack": Layers,
  "graph": Share2, "sorting": Hash, "dp": Sparkles,
  "sql": Database, "system-design": Code2, "strings": BookOpen,
};

const DIFFICULTY_COLORS = {
  beginner: "border-emerald-500/30 bg-emerald-500/10 text-emerald-400",
  intermediate: "border-amber-500/30 bg-amber-500/10 text-amber-400",
  advanced: "border-rose-500/30 bg-rose-500/10 text-rose-400",
};

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, "0")}`;
}

export default function Scrims() {
  const { scrimId } = useParams();
  const navigate = useNavigate();
  const [scrims, setScrims] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [filters, setFilters] = useState({ topic: "", difficulty: "", language: "", search: "" });
  const [showFilters, setShowFilters] = useState(false);
  const [selectedScrim, setSelectedScrim] = useState(null);
  const [playingScrim, setPlayingScrim] = useState(null);

  const loadScrims = useCallback(async () => {
    setLoading(true);
    try {
      const params: any = { page, limit: 12 };
      if (filters.topic) params.topic = filters.topic;
      if (filters.difficulty) params.difficulty = filters.difficulty;
      if (filters.language) params.language = filters.language;
      if (filters.search) params.search = filters.search;
      const data = await api.getScrims(params);
      setScrims(data.scrims || []);
      setTotal(data.total || 0);
    } catch (e) {
      console.error("Failed to load scrims:", e);
    } finally {
      setLoading(false);
    }
  }, [page, filters]);

  useEffect(() => { loadScrims(); }, [loadScrims]);

  useEffect(() => {
    if (scrimId && !playingScrim) {
      api.getScrim(scrimId).then(data => {
        if (data) setPlayingScrim(data);
      }).catch(() => navigate("/scrims"));
    }
  }, [scrimId]);

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPage(1);
  };

  const clearFilters = () => {
    setFilters({ topic: "", difficulty: "", language: "", search: "" });
    setPage(1);
  };

  const hasFilters = Object.values(filters).some(v => v);

  if (playingScrim) {
    return (
      <div className="relative min-h-screen">
        <ScrimPlayer
          scrim={playingScrim}
          onBack={() => { setPlayingScrim(null); navigate("/scrims"); }}
          onLike={async () => {
            await api.likeScrim(playingScrim.id);
            setPlayingScrim(prev => ({ ...prev, likes: (prev.likes || 0) + 1 }));
          }}
        />
      </div>
    );
  }

  const totalPages = Math.ceil(total / 12);

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-display font-bold text-white flex items-center gap-3">
              <Video className="w-8 h-8 text-indigo-400" />
              Interactive Scrims
            </h1>
            <p className="text-slate-400 mt-1">
              Watch coding screencasts. Pause and edit the code at any point.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                type="text" placeholder="Search scrims..."
                value={filters.search}
                onChange={e => handleFilterChange("search", e.target.value)}
                className="w-56 pl-9 pr-3 py-2 rounded-xl border border-slate-700 bg-slate-800/60 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              />
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className={`flex items-center gap-2 px-3 py-2 rounded-xl border text-sm transition-all ${
                showFilters || hasFilters
                  ? "border-indigo-500/40 bg-indigo-500/10 text-indigo-400"
                  : "border-slate-700 bg-slate-800/60 text-slate-400 hover:text-slate-200"
              }`}
            >
              <SlidersHorizontal className="w-4 h-4" />
              Filters
              {hasFilters && <span className="w-2 h-2 rounded-full bg-indigo-400" />}
            </button>
          </div>
        </div>

        <AnimatePresence>
          {showFilters && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden mb-6"
            >
              <div className="p-4 rounded-2xl border border-slate-700/60 bg-slate-800/40 backdrop-blur-sm">
                <div className="flex flex-wrap items-center gap-3">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono uppercase tracking-wider text-slate-500">Topic</span>
                    <select
                      value={filters.topic}
                      onChange={e => handleFilterChange("topic", e.target.value)}
                      className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-sm text-slate-200"
                    >
                      <option value="">All</option>
                      {TOPICS.map(t => <option key={t} value={t}>{t}</option>)}
                    </select>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono uppercase tracking-wider text-slate-500">Difficulty</span>
                    <select
                      value={filters.difficulty}
                      onChange={e => handleFilterChange("difficulty", e.target.value)}
                      className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-sm text-slate-200"
                    >
                      <option value="">All</option>
                      {DIFFICULTIES.map(d => <option key={d} value={d}>{d}</option>)}
                    </select>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono uppercase tracking-wider text-slate-500">Language</span>
                    <select
                      value={filters.language}
                      onChange={e => handleFilterChange("language", e.target.value)}
                      className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-1.5 text-sm text-slate-200"
                    >
                      <option value="">All</option>
                      {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
                    </select>
                  </div>
                  {hasFilters && (
                    <button onClick={clearFilters} className="flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-slate-200 hover:bg-slate-700/50">
                      <X className="w-3 h-3" /> Clear
                    </button>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="rounded-2xl border border-slate-700/60 bg-slate-800/40 p-5">
                <Skeleton className="h-4 w-3/4 mb-3" />
                <Skeleton className="h-3 w-full mb-2" />
                <Skeleton className="h-3 w-2/3 mb-4" />
                <div className="flex gap-2">
                  <Skeleton className="h-5 w-16 rounded-full" />
                  <Skeleton className="h-5 w-14 rounded-full" />
                </div>
              </div>
            ))}
          </div>
        ) : scrims.length === 0 ? (
          <div className="text-center py-20">
            <Video className="w-16 h-16 mx-auto text-slate-600 mb-4" />
            <h3 className="text-lg font-semibold text-slate-300 mb-2">No scrims found</h3>
            <p className="text-slate-500 text-sm">Try adjusting your filters or search terms.</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {scrims.map((scrim, idx) => (
                <motion.button
                  key={scrim.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  onClick={() => { setPlayingScrim(scrim); navigate(`/scrims/${scrim.id}`); }}
                  className="group relative text-left rounded-2xl border border-slate-700/60 bg-slate-800/40 p-5 hover:border-indigo-500/40 hover:bg-slate-800/60 transition-all duration-300"
                >
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <h3 className="text-base font-semibold text-slate-100 group-hover:text-indigo-300 transition-colors line-clamp-1">
                      {scrim.title}
                    </h3>
                    <div className="shrink-0 w-9 h-9 rounded-xl bg-indigo-500/20 flex items-center justify-center">
                      <Play className="w-4 h-4 text-indigo-400" />
                    </div>
                  </div>

                  <p className="text-xs text-slate-500 line-clamp-2 mb-4 leading-relaxed">
                    {scrim.description}
                  </p>

                  <div className="flex flex-wrap items-center gap-2 mb-4">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border ${DIFFICULTY_COLORS[scrim.difficulty] || "border-slate-600 text-slate-400"}`}>
                      {scrim.difficulty}
                    </span>
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border border-sky-500/30 bg-sky-500/10 text-sky-400">
                      {scrim.language}
                    </span>
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border border-violet-500/30 bg-violet-500/10 text-violet-400">
                      {scrim.topic}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-slate-500">
                    <span className="flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5" />
                      {formatDuration(scrim.duration_seconds)}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <User className="w-3.5 h-3.5" />
                      {scrim.author_name}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <ThumbsUp className="w-3.5 h-3.5" />
                      {scrim.likes || 0}
                    </span>
                  </div>
                </motion.button>
              ))}
            </div>

            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-3 mt-10">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage(p => p - 1)}
                  className="flex items-center gap-1 px-4 py-2 rounded-xl border border-slate-700 bg-slate-800/60 text-sm text-slate-300 disabled:opacity-40 hover:border-indigo-500/40 transition-all"
                >
                  <ChevronLeft className="w-4 h-4" /> Prev
                </button>
                <span className="text-sm text-slate-500">
                  Page {page} of {totalPages}
                </span>
                <button
                  disabled={page >= totalPages}
                  onClick={() => setPage(p => p + 1)}
                  className="flex items-center gap-1 px-4 py-2 rounded-xl border border-slate-700 bg-slate-800/60 text-sm text-slate-300 disabled:opacity-40 hover:border-indigo-500/40 transition-all"
                >
                  Next <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
