import { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import {
  BookOpen, Search, Filter, Building2, Tag, BarChart3,
  ExternalLink, ArrowRight, Lock, X, Zap, Plus, ThumbsUp,
  ThumbsDown, ChevronDown, ChevronLeft, ChevronRight,
  User, Briefcase, CheckCircle, Clock, TrendingUp,
  Target, Flame, Award, BarChart, Sparkles, ChevronUp,
  RotateCcw, Eye, Bookmark, Hash, ArrowUpDown, ArrowDown,
  ArrowUp, SortAsc
} from "lucide-react";
import AnimatedCard from "../components/motion/AnimatedCard";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import useReducedMotion from "../hooks/useReducedMotion";
import useAuthStore from "../store/authStore";
import { Emblem } from "../components/emblems";

const DIFFICULTY_COLORS = {
  easy: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  medium: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400",
  hard: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400",
  expert: "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400",
};

const DIFFICULTY_DOT = {
  easy: "bg-green-500",
  medium: "bg-yellow-500",
  hard: "bg-red-500",
  expert: "bg-purple-500",
};

const TYPE_COLORS = {
  coding: "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400",
  aptitude: "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400",
  behavioral: "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400",
  system_design: "bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400",
  hr: "bg-pink-100 dark:bg-pink-900/30 text-pink-700 dark:text-pink-400",
};

const TYPE_LABELS = {
  coding: "Coding",
  aptitude: "Aptitude",
  behavioral: "Behavioral",
  system_design: "System Design",
  hr: "HR",
};

const QUICK_FILTERS = [
  { key: "all", label: "All Problems", icon: <Hash size={13} /> },
  { key: "solved", label: "Solved", icon: <CheckCircle size={13} />, color: "text-green-400" },
  { key: "easy", label: "Easy", icon: <Target size={13} />, color: "text-green-400" },
  { key: "medium", label: "Medium", icon: <Target size={13} />, color: "text-yellow-400" },
  { key: "hard", label: "Hard", icon: <Target size={13} />, color: "text-red-400" },
];

const SORT_OPTIONS = [
  { key: "newest", label: "Newest", icon: <Clock size={12} /> },
  { key: "difficulty_asc", label: "Easy → Hard", icon: <ArrowUp size={12} /> },
  { key: "difficulty_desc", label: "Hard → Easy", icon: <ArrowDown size={12} /> },
  { key: "acceptance", label: "Acceptance %", icon: <BarChart size={12} /> },
  { key: "upvotes", label: "Most Upvoted", icon: <ThumbsUp size={12} /> },
  { key: "title", label: "A → Z", icon: <SortAsc size={12} /> },
];

export default function QuestionBank() {
  const { user } = useAuthStore();
  const [questions, setQuestions] = useState([]);
  const [stats, setStats] = useState(null);
  const [dailyChallenge, setDailyChallenge] = useState(null);
  const [solvedStatuses, setSolvedStatuses] = useState({});
  const [acceptanceRates, setAcceptanceRates] = useState({});
  const [filters, setFilters] = useState({ companies: [], roles: [], topics: [], sub_topics: [], types: [], difficulties: [] });
  const [selected, setSelected] = useState({ company: "", role: "", type: "", difficulty: "", topic: "", sub_topic: "", search: "" });
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showFilters, setShowFilters] = useState(false);
  const [showPaywall, setShowPaywall] = useState(false);
  const [showSubmit, setShowSubmit] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState("");
  const [quickFilter, setQuickFilter] = useState("all");
  const [showStats, setShowStats] = useState(true);
  const [sortBy, setSortBy] = useState("newest");
  const [sortMenuOpen, setSortMenuOpen] = useState(false);
  const reduced = useReducedMotion();

  const isPro = user?.plan === "pro" || user?.plan === "lifetime";
  const questionsPracticed = user?.question_bank_used || 0;
  const FREE_LIMIT = 5;
  const reachedFreeLimit = !isPro && questionsPracticed >= FREE_LIMIT;

  const handlePracticeClick = (questionId) => {
    if (reachedFreeLimit) {
      setShowPaywall(true);
      return;
    }
    window.location.href = `/solve/${questionId}`;
  };

  useEffect(() => {
    loadFilters();
    loadStats();
    api.getDailyChallenge().then(setDailyChallenge).catch(() => setDailyChallenge(null));
  }, []);

  useEffect(() => {
    loadQuestions();
  }, [selected, page]);

  const loadFilters = async () => {
    try {
      const data = await api.getQuestionFilters();
      setFilters(data);
    } catch {}
  };

  const loadStats = async () => {
    try {
      const data = await api.getQuestionStats();
      setStats(data);
    } catch {}
  };

  const loadQuestions = async () => {
    setLoading(true);
    try {
      const params = { ...selected, page, limit: 30 };
      Object.keys(params).forEach((k) => { if (!params[k]) delete params[k]; });
      const data = await api.browseQuestions(params);
      setQuestions(data.questions || []);
      setTotal(data.total || 0);
      setPages(data.pages || 0);
      if (data.questions?.length) {
        loadSolvedStatuses(data.questions.map(q => q.id));
        loadAcceptanceRates(data.questions.map(q => q.id));
      }
    } catch {} finally {
      setLoading(false);
    }
  };

  const loadSolvedStatuses = async (questionIds) => {
    try {
      const results = await Promise.all(
        questionIds.map(id => api.isQuestionSolved(id).catch(() => ({ solved: false })))
      );
      const statusMap = {};
      questionIds.forEach((id, i) => {
        statusMap[id] = results[i]?.solved || false;
      });
      setSolvedStatuses(prev => ({ ...prev, ...statusMap }));
    } catch {}
  };

  const loadAcceptanceRates = async (questionIds) => {
    try {
      const results = await Promise.all(
        questionIds.map(id => api.getAcceptanceRate(id).catch(() => null))
      );
      const rateMap = {};
      questionIds.forEach((id, i) => {
        if (results[i]) rateMap[id] = results[i];
      });
      setAcceptanceRates(prev => ({ ...prev, ...rateMap }));
    } catch {}
  };

  const handleFilterChange = (key, value) => {
    setSelected((prev) => ({ ...prev, [key]: value }));
    setPage(1);
  };

  const clearFilters = () => {
    setSelected({ company: "", role: "", type: "", difficulty: "", topic: "", sub_topic: "", search: "" });
    setPage(1);
  };

  const activeFilters = Object.values(selected).filter(Boolean).length;

  const handleQuickFilter = (filter) => {
    setQuickFilter(filter);
    if (filter === "all") {
      setSelected(prev => ({ ...prev, difficulty: "", search: "" }));
    } else if (filter === "solved") {
      // Handled client-side via solvedStatuses
      setSelected(prev => ({ ...prev, difficulty: "" }));
    } else {
      setSelected(prev => ({ ...prev, difficulty: filter }));
    }
    setPage(1);
  };

  const handleSubmitQuestion = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const form = e.target;
      const payload = {
        type: form.type.value,
        company: [form.company.value],
        role: form.role.value || "SDE",
        difficulty: form.difficulty.value || "medium",
        topic: form.topic.value,
        sub_topic: form.sub_topic.value,
        question: form.question.value,
        options: form.options.value.split("\n").filter(Boolean),
        correct_answer: form.correct_answer.value,
        explanation: form.explanation.value,
        hints: form.hints.value.split("\n").filter(Boolean),
        solution: {},
      };
      const data = await api.submitNewQuestion(payload);
      setSubmitted(data.id);
      setShowSubmit(false);
      form.reset();
      loadQuestions();
    } catch {} finally {
      setSubmitting(false);
    }
  };

  const handleUpvote = async (e, questionId) => {
    e.stopPropagation();
    try {
      await api.upvoteQuestion(questionId, 1);
      setQuestions((qs) => qs.map((q) => q.id === questionId ? { ...q, upvotes: (q.upvotes || 0) + 1 } : q));
    } catch {}
  };

  const filteredQuestions = useMemo(() => {
    let list = quickFilter === "solved"
      ? questions.filter(q => solvedStatuses[q.id])
      : [...questions];

    const diffOrder = { easy: 0, medium: 1, hard: 2, expert: 3 };
    switch (sortBy) {
      case "difficulty_asc":
        list.sort((a, b) => (diffOrder[a.difficulty] ?? 9) - (diffOrder[b.difficulty] ?? 9));
        break;
      case "difficulty_desc":
        list.sort((a, b) => (diffOrder[b.difficulty] ?? 9) - (diffOrder[a.difficulty] ?? 9));
        break;
      case "acceptance":
        list.sort((a, b) => (acceptanceRates[b.id]?.acceptance_rate ?? 0) - (acceptanceRates[a.id]?.acceptance_rate ?? 0));
        break;
      case "upvotes":
        list.sort((a, b) => (b.upvotes || 0) - (a.upvotes || 0));
        break;
      case "title":
        list.sort((a, b) => (a.question || a.question_title || "").localeCompare(b.question || b.question_title || ""));
        break;
      case "newest":
      default:
        break;
    }
    return list;
  }, [questions, quickFilter, solvedStatuses, sortBy, acceptanceRates]);

  const difficultyDistribution = useMemo(() => {
    if (!stats?.by_difficulty) return null;
    const { easy = 0, medium = 0, hard = 0, expert = 0 } = stats.by_difficulty;
    const total = easy + medium + hard + expert;
    if (total === 0) return null;
    return { easy, medium, hard, expert, total };
  }, [stats]);

  const renderAcceptanceBar = (questionId) => {
    const data = acceptanceRates[questionId];
    if (!data) return null;
    const rate = data.acceptance_rate;
    if (rate == null) return null;
    const barColor = rate >= 60 ? "bg-green-500" : rate >= 40 ? "bg-yellow-500" : "bg-red-500";
    return (
      <div className="flex items-center gap-1.5">
        <div className="w-16 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
          <div className={`h-full rounded-full ${barColor}`} style={{ width: `${Math.min(100, rate)}%` }} />
        </div>
        <span className="text-[10px] text-gray-500 dark:text-gray-400 tabular-nums">{rate}%</span>
      </div>
    );
  };

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div className="mb-6" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
                <BookOpen size={24} className="text-blue-600" />
              </div>
              <div>
                <h1 className="text-3xl font-bold dark:text-white">Question Bank</h1>
                <p className="text-gray-600 dark:text-gray-400">Practice curated questions from top companies</p>
              </div>
            </div>
            <button onClick={() => setShowSubmit(!showSubmit)} className="btn-primary flex items-center gap-2">
              <Plus size={16} /> Submit Question
            </button>
          </div>
        </motion.div>

        {dailyChallenge?.problem && (
          <motion.div
            className="mb-6 overflow-hidden rounded-2xl border border-indigo-200/60 dark:border-indigo-900/50 bg-gradient-to-r from-indigo-600 via-cyan-600 to-emerald-500 text-white shadow-lg"
            initial={reduced ? {} : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="p-5 sm:p-6 flex flex-col lg:flex-row lg:items-center gap-4">
              <div className="flex items-start gap-4 flex-1 min-w-0">
                <div className="w-12 h-12 rounded-2xl bg-white/15 flex items-center justify-center shrink-0">
                  <Sparkles size={22} />
                </div>
                <div className="min-w-0">
                  <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-white/70">Featured today</div>
                  <h2 className="mt-1 text-xl sm:text-2xl font-bold truncate">{dailyChallenge.problem.question_title || dailyChallenge.problem.question || "Today's Problem"}</h2>
                  <p className="mt-2 text-sm text-white/85">
                    {dailyChallenge.config?.category} · {dailyChallenge.config?.focus} · {dailyChallenge.streak_bonus || 0} XP bonus
                  </p>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-2 lg:justify-end shrink-0">
                <span className="px-3 py-1 rounded-full bg-white/15 text-xs font-semibold uppercase tracking-wide">
                  {dailyChallenge.config?.difficulty || "medium"}
                </span>
                <Link to="/daily-challenge" className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white text-indigo-700 font-semibold text-sm hover:bg-white/90 transition-colors">
                  Open Daily Challenge
                  <ArrowRight size={14} />
                </Link>
                {dailyChallenge.problem?.id && (
                  <Link to={`/solve/${dailyChallenge.problem.id}`} className="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-white/30 text-white font-semibold text-sm hover:bg-white/10 transition-colors">
                    Solve Now
                  </Link>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {/* Stats Summary (LeetCode-style) */}
        {showStats && stats && (
          <motion.div className="mb-6" initial={reduced ? {} : { opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-5">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-gray-700 dark:text-gray-300 flex items-center gap-2">
                  <BarChart size={14} /> Your Progress
                </h2>
                <button onClick={() => setShowStats(false)} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                  <ChevronUp size={14} />
                </button>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">{stats.total_solved || 0}</div>
                  <div className="text-[10px] text-gray-500 uppercase tracking-wide">Solved</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-500">{stats.easy_solved || 0}/{difficultyDistribution?.easy || 0}</div>
                  <div className="text-[10px] text-gray-500 uppercase tracking-wide">Easy</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-yellow-500">{stats.medium_solved || 0}/{difficultyDistribution?.medium || 0}</div>
                  <div className="text-[10px] text-gray-500 uppercase tracking-wide">Medium</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-500">{stats.hard_solved || 0}/{difficultyDistribution?.hard || 0}</div>
                  <div className="text-[10px] text-gray-500 uppercase tracking-wide">Hard</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-500">{stats.expert_solved || 0}/{difficultyDistribution?.expert || 0}</div>
                  <div className="text-[10px] text-gray-500 uppercase tracking-wide">Expert</div>
                </div>
              </div>
              {/* Difficulty distribution bar */}
              {difficultyDistribution && (
                <div className="mt-4">
                  <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden flex">
                    {(difficultyDistribution.easy / difficultyDistribution.total * 100) > 0 && (
                      <div className="h-full bg-green-500" style={{ width: `${difficultyDistribution.easy / difficultyDistribution.total * 100}%` }} />
                    )}
                    {(difficultyDistribution.medium / difficultyDistribution.total * 100) > 0 && (
                      <div className="h-full bg-yellow-500" style={{ width: `${difficultyDistribution.medium / difficultyDistribution.total * 100}%` }} />
                    )}
                    {(difficultyDistribution.hard / difficultyDistribution.total * 100) > 0 && (
                      <div className="h-full bg-red-500" style={{ width: `${difficultyDistribution.hard / difficultyDistribution.total * 100}%` }} />
                    )}
                    {(difficultyDistribution.expert / difficultyDistribution.total * 100) > 0 && (
                      <div className="h-full bg-purple-500" style={{ width: `${difficultyDistribution.expert / difficultyDistribution.total * 100}%` }} />
                    )}
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        )}

        {showStats === false && stats && (
          <button onClick={() => setShowStats(true)} className="mb-4 text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 flex items-center gap-1">
            <BarChart size={12} /> Show Stats
          </button>
        )}

        {/* Submit Form */}
        {showSubmit && (
          <AnimatedCard className="card mb-6">
            <h2 className="text-xl font-bold mb-4 dark:text-white">Submit a Question</h2>
            {submitted && <p className="text-sm text-green-600 mb-2">Submitted! ID: {submitted}</p>}
            <form onSubmit={handleSubmitQuestion} className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Type</label>
                <select name="type" className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm" required>
                  <option value="aptitude">Aptitude</option>
                  <option value="coding">Coding</option>
                  <option value="behavioral">Behavioral</option>
                  <option value="system_design">System Design</option>
                  <option value="hr">HR</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Company</label>
                <input name="company" className="input" placeholder="e.g. Google" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
                <input name="role" className="input" placeholder="SDE" defaultValue="SDE" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Difficulty</label>
                <select name="difficulty" className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm">
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                  <option value="expert">Expert</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Topic</label>
                <input name="topic" className="input" placeholder="e.g. Arrays" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sub Topic</label>
                <input name="sub_topic" className="input" placeholder="e.g. Sliding Window" />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Question</label>
                <textarea name="question" rows={3} className="input" placeholder="Enter the question text..." required />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Options (one per line, for MCQ)</label>
                <textarea name="options" rows={3} className="input" placeholder="Option A\nOption B\nOption C\nOption D" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Correct Answer</label>
                <input name="correct_answer" className="input" placeholder="e.g. Option A" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Explanation</label>
                <input name="explanation" className="input" placeholder="Why this is correct..." />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Hints (one per line)</label>
                <textarea name="hints" rows={2} className="input" placeholder="Hint 1\nHint 2" />
              </div>
              <div className="md:col-span-2 flex gap-2">
                <button type="submit" disabled={submitting} className="btn-primary">{submitting ? "Submitting..." : "Submit Question"}</button>
                <button type="button" onClick={() => setShowSubmit(false)} className="btn-secondary">Cancel</button>
              </div>
            </form>
          </AnimatedCard>
        )}

        {/* Quick Filters (LeetCode-style tabs) */}
        <div className="flex items-center gap-1 mb-4 overflow-x-auto pb-1">
          {QUICK_FILTERS.map((f) => (
            <button
              key={f.key}
              onClick={() => handleQuickFilter(f.key)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                quickFilter === f.key
                  ? "bg-primary-600 text-white shadow-sm"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
              }`}
            >
              {f.icon} <span className={f.key !== quickFilter && f.color ? f.color : ""}>{f.label}</span>
            </button>
          ))}
        </div>

        {/* Search + Filter + Sort */}
        <div className="flex gap-3 mb-6">
          <div className="relative flex-1">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search questions by name, topic, or company..."
              value={selected.search}
              onChange={(e) => handleFilterChange("search", e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-800 dark:text-white"
            />
          </div>
          {/* Sort Dropdown */}
          <div className="relative">
            <button
              onClick={() => setSortMenuOpen(!sortMenuOpen)}
              className="flex items-center gap-2 px-3 py-3 rounded-lg font-medium bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            >
              <ArrowUpDown size={16} />
              <span className="text-xs hidden sm:inline">{SORT_OPTIONS.find(s => s.key === sortBy)?.label || "Sort"}</span>
            </button>
            {sortMenuOpen && (
              <>
                <div className="fixed inset-0 z-30" onClick={() => setSortMenuOpen(false)} />
                <div className="absolute right-0 top-full mt-1 z-40 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-xl py-1 min-w-[160px]">
                  {SORT_OPTIONS.map((opt) => (
                    <button
                      key={opt.key}
                      onClick={() => { setSortBy(opt.key); setSortMenuOpen(false); }}
                      className={`flex items-center gap-2 w-full px-3 py-2 text-xs transition-colors ${
                        sortBy === opt.key
                          ? "bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400"
                          : "text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700"
                      }`}
                    >
                      {opt.icon} {opt.label}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-2 px-4 py-3 rounded-lg font-medium transition-colors ${
              showFilters || activeFilters > 0
                ? "bg-primary-600 text-white"
                : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
            }`}
          >
            <Filter size={18} />
            Filters {activeFilters > 0 && `(${activeFilters})`}
          </button>
        </div>

        {/* Advanced Filters */}
        {showFilters && (
          <motion.div className="card mb-6" initial={reduced ? {} : { opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }}>
            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Company</label>
                <select value={selected.company} onChange={(e) => handleFilterChange("company", e.target.value)} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm">
                  <option value="">All Companies</option>
                  {filters.companies.map((c) => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
                <select value={selected.role} onChange={(e) => handleFilterChange("role", e.target.value)} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm">
                  <option value="">All Roles</option>
                  {filters.roles.map((r) => <option key={r} value={r}>{r}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Type</label>
                <select value={selected.type} onChange={(e) => handleFilterChange("type", e.target.value)} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm">
                  <option value="">All Types</option>
                  {filters.types.map((t) => <option key={t} value={t}>{TYPE_LABELS[t] || t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Difficulty</label>
                <select value={selected.difficulty} onChange={(e) => handleFilterChange("difficulty", e.target.value)} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm">
                  <option value="">All Levels</option>
                  {filters.difficulties.map((d) => <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Topic</label>
                <select value={selected.topic} onChange={(e) => handleFilterChange("topic", e.target.value)} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm">
                  <option value="">All Topics</option>
                  {filters.topics.map((t) => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Sub Topic</label>
                <select value={selected.sub_topic} onChange={(e) => handleFilterChange("sub_topic", e.target.value)} className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 dark:text-white text-sm">
                  <option value="">All Sub Topics</option>
                  {filters.sub_topics.map((t) => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
            </div>
            {activeFilters > 0 && (
              <div className="mt-4 flex items-center gap-3">
                <button onClick={clearFilters} className="text-sm text-primary-600 hover:text-primary-700 font-medium flex items-center gap-1"><RotateCcw size={12} /> Clear all filters</button>
                <span className="text-sm text-gray-400">{total} questions found</span>
              </div>
            )}
          </motion.div>
        )}

        {/* Company Quick Chips */}
        {!showFilters && (
          <div className="flex flex-wrap gap-2 mb-6">
            {["TCS", "Infosys", "Google", "Amazon", "Microsoft", "Meta", "Wipro", "Uber"].map((c) => (
              <button key={c} onClick={() => handleFilterChange("company", selected.company === c ? "" : c)} className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${selected.company === c ? "bg-primary-600 text-white" : "bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"}`}>
                {c}
              </button>
            ))}
          </div>
        )}

        {/* Loading */}
        {loading ? (
          <div className="space-y-3">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="flex items-center gap-4">
                  <div className="h-6 w-6 bg-gray-200 dark:bg-gray-700 rounded" />
                  <div className="flex-1">
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-2" />
                    <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : filteredQuestions.length === 0 ? (
          <div className="card text-center py-12">
            <BookOpen size={48} className="mx-auto text-gray-300 dark:text-gray-600 mb-4" />
            <p className="text-gray-500 dark:text-gray-400 mb-2">No questions found</p>
            <p className="text-sm text-gray-400 dark:text-gray-500">Try adjusting your filters</p>
          </div>
        ) : (
          <StaggerContainer className="space-y-2">
            {filteredQuestions.map((q) => {
              const isSolved = solvedStatuses[q.id];
              const companyList = Array.isArray(q.company) ? q.company : [q.company].filter(Boolean);
              return (
                <StaggerItem key={q.id}>
                  <div
                    className={`group flex items-center gap-3 px-4 py-3 rounded-xl border transition-all cursor-pointer ${
                      isSolved
                        ? "bg-green-50 dark:bg-green-900/5 border-green-200 dark:border-green-800/50"
                        : "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800 hover:border-primary-300 dark:hover:border-primary-700 hover:shadow-sm"
                    }`}
                    onClick={() => handlePracticeClick(q.id)}
                  >
                    {/* Solved indicator */}
                    <div className="w-6 flex items-center justify-center shrink-0">
                      {isSolved ? (
                        <CheckCircle size={18} className="text-green-500" />
                      ) : (
                        <div className="w-4 h-4 rounded-full border-2 border-gray-300 dark:border-gray-600 group-hover:border-primary-500 transition-colors" />
                      )}
                    </div>

                    {/* Emblem */}
                    <Emblem
                      question={q}
                      difficulty={q.difficulty}
                      size="xs"
                      animated={false}
                      glow={false}
                    />

                    {/* Question Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-medium text-sm dark:text-white truncate">{q.question || q.question_title}</span>
                      </div>
                      <div className="flex items-center gap-2 mt-1 flex-wrap">
                        <span className={`text-[10px] px-1.5 py-0.5 rounded ${DIFFICULTY_COLORS[q.difficulty] || ""}`}>
                          {q.difficulty}
                        </span>
                        {companyList.slice(0, 2).map((co) => (
                          <span key={co} className="text-[10px] px-1.5 py-0.5 rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400">
                            {co}
                          </span>
                        ))}
                        <span className="text-[10px] text-gray-400">{q.topic}{q.sub_topic ? ` · ${q.sub_topic}` : ""}</span>
                      </div>
                    </div>

                    {/* Stats */}
                    <div className="hidden md:flex items-center gap-4 shrink-0">
                      {/* Acceptance Rate */}
                      {renderAcceptanceBar(q.id)}

                      {/* Upvotes */}
                      <div className="flex items-center gap-1 text-[10px] text-gray-400 min-w-[40px]">
                        <ThumbsUp size={10} />
                        <span className="tabular-nums">{q.upvotes || 0}</span>
                      </div>

                      {/* Type */}
                      <span className={`text-[10px] px-1.5 py-0.5 rounded ${TYPE_COLORS[q.type] || ""} min-w-[50px] text-center`}>
                        {TYPE_LABELS[q.type] || q.type}
                      </span>
                    </div>

                    {/* Arrow */}
                    <ArrowRight size={14} className="text-gray-300 group-hover:text-primary-500 transition-colors shrink-0" />
                  </div>
                </StaggerItem>
              );
            })}
          </StaggerContainer>
        )}

        {/* Pagination (LeetCode-style numbered) */}
        {pages > 1 && (
          <div className="flex items-center justify-center gap-1 mt-8">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 disabled:opacity-30"
            >
              <ChevronLeft size={16} />
            </button>
            {Array.from({ length: Math.min(pages, 7) }, (_, i) => {
              let pageNum;
              if (pages <= 7) {
                pageNum = i + 1;
              } else if (page <= 4) {
                pageNum = i + 1;
              } else if (page >= pages - 3) {
                pageNum = pages - 6 + i;
              } else {
                pageNum = page - 3 + i;
              }
              return (
                <button
                  key={pageNum}
                  onClick={() => setPage(pageNum)}
                  className={`w-8 h-8 rounded-lg text-xs font-medium transition-colors ${
                    page === pageNum
                      ? "bg-primary-600 text-white"
                      : "text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800"
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
            <button
              onClick={() => setPage(Math.min(pages, page + 1))}
              disabled={page === pages}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500 disabled:opacity-30"
            >
              <ChevronRight size={16} />
            </button>
            <span className="ml-3 text-xs text-gray-500">{total} problems</span>
          </div>
        )}

        {/* Free Tier Usage */}
        {!isPro && (
          <div className="mt-8 card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-600 dark:text-gray-400">Free Practice: {questionsPracticed}/{FREE_LIMIT} questions used</span>
              <Link to="/pricing" className="text-sm text-primary-600 hover:text-primary-700 font-medium">Upgrade to Pro →</Link>
            </div>
            <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div className={`h-full rounded-full transition-all ${reachedFreeLimit ? "bg-red-500" : "bg-primary-500"}`} style={{ width: `${Math.min(100, (questionsPracticed / FREE_LIMIT) * 100)}%` }} />
            </div>
            {reachedFreeLimit && <p className="text-xs text-red-500 mt-2">Free limit reached. Upgrade to Pro for unlimited practice.</p>}
          </div>
        )}

        {/* Paywall Modal */}
        <AnimatePresence>
          {showPaywall && (
            <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => setShowPaywall(false)}>
              <motion.div className="bg-white dark:bg-gray-900 rounded-2xl p-8 max-w-md w-full text-center" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }} onClick={(e) => e.stopPropagation()}>
                <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-2xl flex items-center justify-center mx-auto mb-4"><Lock size={32} className="text-primary-600" /></div>
                <h2 className="text-2xl font-bold mb-2 dark:text-white">Free Limit Reached</h2>
                <p className="text-gray-600 dark:text-gray-400 mb-6">You've used all {FREE_LIMIT} free practice questions this month. Upgrade to Pro for unlimited access to {total}+ curated questions.</p>
                <div className="bg-primary-50 dark:bg-primary-900/20 rounded-xl p-4 mb-6">
                  <div className="flex items-center justify-center gap-2 mb-2"><Zap size={18} className="text-primary-600" /><span className="font-bold text-primary-700 dark:text-primary-400">Pro — $9/mo</span></div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">Unlimited questions · Full solutions · Company filters · Mock tests</p>
                </div>
                <div className="flex gap-3">
                  <button onClick={() => setShowPaywall(false)} className="flex-1 px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 font-medium hover:bg-gray-200 dark:hover:bg-gray-700">Later</button>
                  <Link to="/pricing" className="flex-1 px-4 py-3 rounded-lg bg-primary-600 text-white font-medium hover:bg-primary-700 text-center" onClick={() => setShowPaywall(false)}>Upgrade to Pro</Link>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
