import { useState, useEffect, useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useQuestionFilters, useQuestionStats, useBrowseQuestions, useSolvedStatus, useDailyChallenge } from "../hooks/useQuestions";
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
import useReducedMotion from "../hooks/useReducedMotion";
import useAuthStore from "../store/authStore";
import { Emblem } from "../components/emblems";
import { GROUP_META, GROUP_ORDER, topicGroup } from "../utils/topicGroups";
import VirtualList from "../components/ui/VirtualList";
import { QuestionCardSkeleton } from "../components/ui/Skeleton";

interface QuestionFilters {
  company: string;
  role: string;
  type: string;
  difficulty: string;
  topic: string;
  sub_topic: string;
  pattern: string;
  source: string;
  search: string;
}

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
  system_design: "bg-indigo-100 dark:bg-indigo-900/30 text-brand-primary dark:text-indigo-400",
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

const CATEGORY_FILTERS = [
  { key: "all", label: "All Categories" },
  ...GROUP_ORDER.map((key) => ({ key, label: GROUP_META[key].label })),
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
  const navigate = useNavigate();
  const [selected, setSelected] = useState<QuestionFilters>({ company: "", role: "", type: "", difficulty: "", topic: "", sub_topic: "", pattern: "", source: "", search: "" });
  const [page, setPage] = useState(1);
  const [quickFilter, setQuickFilter] = useState("all");
  const [category, setCategory] = useState("all");
  const [showStats, setShowStats] = useState(true);
  const [sortBy, setSortBy] = useState("newest");
  const [sortMenuOpen, setSortMenuOpen] = useState(false);
  const [randomLoading, setRandomLoading] = useState(false);
  const [showPaywall, setShowPaywall] = useState(false);
  const [showSubmit, setShowSubmit] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState("");

  // TanStack Query data
  const { data: filtersData, isLoading: filtersLoading, refetch: refetchFilters } = useQuestionFilters();
  const { data: statsData, isLoading: statsLoading, refetch: refetchStats } = useQuestionStats();
  const { data: dailyChallengeData, isLoading: dailyChallengeLoading } = useDailyChallenge();
  const { data: browseData, isLoading: browseLoading, refetch: refetchBrowse } = useBrowseQuestions(
    { companies: filtersData?.companies || [], roles: filtersData?.roles || [], topics: filtersData?.topics || [], sub_topics: filtersData?.sub_topics || [], types: filtersData?.types || [], difficulties: filtersData?.difficulties || [], patterns: filtersData?.patterns || [], sources: filtersData?.sources || [] },
    1,
    80
  );
  const { data: solvedMap, isLoading: solvedLoading } = useSolvedStatus([]);

  const questions = browseData?.questions || [];
  const stats = statsData;
  const total = browseData?.total || 0;
  const pages = browseData?.pages || 0;
  const reduced = useReducedMotion();

  const isPro = user?.plan === "pro" || user?.plan === "lifetime";
  const questionsPracticed = Number(user?.usage?.question_bank_used) || 0;
  const FREE_LIMIT = 5;
  const reachedFreeLimit = !isPro && questionsPracticed >= FREE_LIMIT;

  const handlePracticeClick = (questionId) => {
    if (reachedFreeLimit) {
      setShowPaywall(true);
      return;
    }
    navigate(`/solve/${questionId}`);
  };

  const handleRandomPractice = async () => {
    if (reachedFreeLimit) {
      setShowPaywall(true);
      return;
    }

    setRandomLoading(true);
    try {
      const params: Record<string, string> = {};
      if (selected.company) params.company = selected.company;
      if (selected.role) params.role = selected.role;
      if (selected.topic) params.topic = selected.topic;
      if (selected.type) params.type = selected.type;
      if (selected.difficulty) params.difficulty = selected.difficulty;
      if (selected.source) params.source = selected.source;
      const data = await api.questions.getRandom(params);
      const targetId = data?.id || data?.question_id || data?.problem?.id;
      if (targetId) {
        navigate(`/solve/${targetId}`);
      } else {
        setShowPaywall(false);
      }
    } catch {
      setShowPaywall(false);
    } finally {
      setRandomLoading(false);
    }
  };

  useEffect(() => {
    refetchFilters();
    refetchStats();
    refetchBrowse({ companies: selected.company, roles: selected.role, topics: selected.topics, sub_topics: selected.sub_topics, types: selected.types, difficulties: selected.difficulties, patterns: selected.patterns, sources: selected.sources });
  }, [selected, refetchFilters, refetchStats, refetchBrowse]);

  const handleFilterChange = (key: keyof QuestionFilters, value: string) => {
    setSelected((prev) => ({ ...prev, [key]: value }));
    setPage(1);
    refetchBrowse({ companies: selected.company, roles: selected.role, topics: selected.topics, sub_topics: selected.sub_topics, types: selected.types, difficulties: selected.difficulties, patterns: selected.patterns, sources: selected.sources });
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

    if (category !== "all") {
      list = list.filter((q) => topicGroup(q.topic) === category);
    }

    const diffOrder = { easy: 0, medium: 1, hard: 2, expert: 3 };
    switch (sortBy) {
      case "difficulty_asc":
        list.sort((a, b) => (diffOrder[a.difficulty] ?? 9) - (diffOrder[b.difficulty] ?? 9));
        break;
      case "difficulty_desc":
        list.sort((a, b) => (diffOrder[b.difficulty] ?? 9) - (diffOrder[a.difficulty] ?? 9));
        break;
      case "acceptance":
        list.sort((a, b) => (b.acceptance_rate ?? 0) - (a.acceptance_rate ?? 0));
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
  }, [questions, quickFilter, solvedStatuses, sortBy, acceptanceRates, category]);

  const difficultyDistribution = useMemo(() => {
    if (!stats?.by_difficulty) return null;
    const { easy = 0, medium = 0, hard = 0, expert = 0 } = stats.by_difficulty;
    const total = easy + medium + hard + expert;
    if (total === 0) return null;
    return { easy, medium, hard, expert, total };
  }, [stats]);

  const renderAcceptanceBar = (q) => {
    const rate = q.acceptance_rate;
    if (rate == null) return null;
    const barColor = rate >= 60 ? "bg-green-500" : rate >= 40 ? "bg-yellow-500" : "bg-red-500";
    return (
      <div className="flex items-center gap-1.5">
        <div className="w-16 h-1.5 bg-surface-border rounded-full overflow-hidden">
          <div className={`h-full rounded-full ${barColor}`} style={{ width: `${Math.min(100, rate)}%` }} />
        </div>
        <span className="text-[10px] text-brand-dim tabular-nums">{rate}%</span>
      </div>
    );
  };

  return (
     <div className="page-surface min-h-screen py-6 px-3 sm:px-4">
       <div className="mx-auto max-w-4xl lg:max-w-6xl">
         {/* Header */}
         <motion.div className="mb-6" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
           <div className="rounded-3xl border border-black/5 bg-white border-border/90 p-4 sm:p-5 shadow-soft-lg">
             <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
               <div className="max-w-3xl">
                <div className="inline-flex items-center gap-2 rounded-full border border-brand-sky/20 bg-brand-sky/10 px-3 py-1 text-[10px] font-mono uppercase tracking-[0.28em] text-brand-sky">
                  <Sparkles size={10} />
                  LeetCode-style practice hub
                </div>
                <h1 className="mt-3 text-3xl font-black tracking-tight text-text-primary md:text-4xl">
                  Solve better questions, faster
                </h1>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-text-muted">
                  Browse curated company questions, jump into a random solve, or filter by topic and difficulty to build real interview readiness.
                </p>
                <div className="mt-4 flex flex-wrap items-center gap-2">
                  <button
                    onClick={handleRandomPractice}
                    disabled={randomLoading}
                    className="inline-flex items-center gap-2 rounded-xl bg-brand-sky px-4 py-2.5 text-sm font-bold text-text-primary shadow-soft-md transition-transform hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
                  >
                    {randomLoading ? <Zap size={14} className="animate-pulse" /> : <ArrowRight size={14} />}
                    Random solve
                  </button>
                <button onClick={() => setShowFilters(true)} 
className="inline-flex items-center gap-2 rounded-xl border border-brand-primary/20 bg-surface-card px-4 py-2.5 text-sm font-semibold 
text-brand-secondary transition-colors hover:border-brand-sky/30 hover:text-brand-sky">
                    <Filter size={14} />
                    Filters
                  </button>
                  <button onClick={() => setShowSubmit(!showSubmit)} className="inline-flex items-center gap-2 rounded-xl border border-brand-coral/20 bg-brand-coral-pale px-4 py-2.5 text-sm font-semibold text-brand-coral transition-colors hover:bg-brand-coral/10">
                    <Plus size={14} />
                    Submit question
                  </button>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:w-[460px]">
                <div className="rounded-2xl border border-black/5 bg-white p-4 text-center shadow-sm">
                  <div className="text-2xl font-black text-brand-primary">{stats?.total_solved || 0}</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-brand-dim">Solved</div>
                </div>
                <div className="rounded-2xl border border-black/5 bg-white p-4 text-center shadow-sm">
                  <div className="text-2xl font-black text-brand-primary">{stats?.acceptance_rate || 0}%</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-brand-dim">Avg acceptance</div>
                </div>
                <div className="rounded-2xl border border-black/5 bg-white p-4 text-center shadow-sm">
                  <div className="text-2xl font-black text-brand-primary">{questions.length}</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-brand-dim">Loaded</div>
                </div>
                <div className="rounded-2xl border border-black/5 bg-white p-4 text-center shadow-sm">
                  <div className="text-2xl font-black text-brand-primary">{pages || 1}</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-brand-dim">Pages</div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {dailyChallenge?.problem && (
          <motion.div
            className="mb-6 overflow-hidden rounded-2xl border border-indigo-200/60 dark:border-indigo-900/50 bg-gradient-to-r from-indigo-600 via-cyan-600 to-emerald-500 text-text-primary shadow-lg"
            initial={reduced ? {} : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="p-5 sm:p-6 flex flex-col lg:flex-row lg:items-center gap-4">
              <div className="flex items-start gap-4 flex-1 min-w-0">
                <div className="w-12 h-12 rounded-2xl bg-brand-primary/15 flex items-center justify-center shrink-0">
                  <Sparkles size={22} />
                </div>
                <div className="min-w-0">
                  <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-text-primary/70">Featured today</div>
                  <h2 className="mt-1 text-xl sm:text-2xl font-bold truncate">{dailyChallenge.problem.question_title || dailyChallenge.problem.question || "Today's Problem"}</h2>
                  <p className="mt-2 text-sm text-text-primary/85">
                    {dailyChallenge.config?.category} · {dailyChallenge.config?.focus} · {dailyChallenge.streak_bonus || 0} XP bonus
                  </p>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-2 lg:justify-end shrink-0">
                <span className="px-3 py-1 rounded-full bg-brand-primary/15 text-xs font-semibold uppercase tracking-wide">
                  {dailyChallenge.config?.difficulty || "medium"}
                </span>
                <Link to="/daily-challenge" className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-surface-card text-brand-primary font-semibold text-sm hover:bg-surface-card/90 transition-colors">
                  Open Daily Challenge
                  <ArrowRight size={14} />
                </Link>
                {dailyChallenge.problem?.id && (
                  <Link to={`/solve/${dailyChallenge.problem.id}`} className="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-white/30 text-text-primary font-semibold text-sm hover:bg-surface-card/10 transition-colors">
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
            <div className="rounded-xl border border-black/5 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-brand-primary flex items-center gap-2">
                  <BarChart size={14} /> Your Progress
                </h2>
                <button onClick={() => setShowStats(false)} className="text-brand-dim hover:text-brand-primary">
                  <ChevronUp size={14} />
                </button>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-brand-primary">{stats.total_solved || 0}</div>
                  <div className="text-[10px] text-brand-dim uppercase tracking-wide">Solved</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-brand-emerald">{stats.easy_solved || 0}/{difficultyDistribution?.easy || 0}</div>
                  <div className="text-[10px] text-brand-dim uppercase tracking-wide">Easy</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-brand-gold">{stats.medium_solved || 0}/{difficultyDistribution?.medium || 0}</div>
                  <div className="text-[10px] text-brand-dim uppercase tracking-wide">Medium</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-red-500">{stats.hard_solved || 0}/{difficultyDistribution?.hard || 0}</div>
                  <div className="text-[10px] text-brand-muted uppercase tracking-wide">Hard</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-500">{stats.expert_solved || 0}/{difficultyDistribution?.expert || 0}</div>
                  <div className="text-[10px] text-brand-muted uppercase tracking-wide">Expert</div>
                </div>
              </div>
              {/* Difficulty distribution bar */}
              {difficultyDistribution && (
                <div className="mt-4">
                  <div className="flex h-2 overflow-hidden rounded-full bg-surface-2">
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
          <button onClick={() => setShowStats(true)} className="mb-4 text-xs text-brand-dim hover:text-brand-primary flex items-center gap-1">
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
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Type</label>
                <select name="type" className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm" required>
                  <option value="aptitude">Aptitude</option>
                  <option value="coding">Coding</option>
                  <option value="behavioral">Behavioral</option>
                  <option value="system_design">System Design</option>
                  <option value="hr">HR</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Company</label>
                <input name="company" className="input" placeholder="e.g. Google" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Role</label>
                <input name="role" className="input" placeholder="SDE" defaultValue="SDE" />
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Difficulty</label>
                <select name="difficulty" className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                  <option value="expert">Expert</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Topic</label>
                <input name="topic" className="input" placeholder="e.g. Arrays" required />
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Sub Topic</label>
                <input name="sub_topic" className="input" placeholder="e.g. Sliding Window" />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Question</label>
                <textarea name="question" rows={3} className="input" placeholder="Enter the question text..." required />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Options (one per line, for MCQ)</label>
                <textarea name="options" rows={3} className="input" placeholder="Option A\nOption B\nOption C\nOption D" />
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Correct Answer</label>
                <input name="correct_answer" className="input" placeholder="e.g. Option A" />
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Explanation</label>
                <input name="explanation" className="input" placeholder="Why this is correct..." />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Hints (one per line)</label>
                <textarea name="hints" rows={2} className="input" placeholder="Hint 1\nHint 2" />
              </div>
              <div className="md:col-span-2 flex gap-2">
                <button type="submit" disabled={submitting} className="btn-primary">{submitting ? "Submitting..." : "Submit Question"}</button>
                <button type="button" onClick={() => setShowSubmit(false)} className="btn-secondary">Cancel</button>
              </div>
            </form>
          </AnimatedCard>
        )}

        {/* Category Filters (Patterns / Algorithms / Data Structures) */}
        <div className="flex items-center gap-1 mb-2 overflow-x-auto pb-1">
          {CATEGORY_FILTERS.map((f) => {
            const meta = f.key === "all" ? null : GROUP_META[f.key];
            return (
              <button
                key={f.key}
                onClick={() => setCategory(f.key)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap border ${
                  category === f.key
                    ? "bg-primary-600 text-text-primary border-primary-600 shadow-sm"
                    : `border-brand-primary/10 bg-surface-card text-brand-muted hover:bg-surface-card/70 dark:hover:bg-gray-700 ${meta?.tag || ""}`
                }`}
              >
                {meta && f.key !== category ? meta.label : f.label}
              </button>
            );
          })}
        </div>
        <div className="flex items-center gap-1 mb-4 overflow-x-auto pb-1">
          {QUICK_FILTERS.map((f) => (
            <button
              key={f.key}
              onClick={() => handleQuickFilter(f.key)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all whitespace-nowrap ${
                quickFilter === f.key
                  ? "bg-primary-600 text-text-primary shadow-sm"
                  : "bg-white text-brand-muted hover:bg-surface-2"
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
              className="w-full pl-10 pr-4 py-3 border border-brand-primary/20 border-brand-primary/15 rounded-lg focus:ring-2 focus:ring-primary-500 bg-surface-card bg-surface-card dark:text-white"
            />
          </div>
          {/* Sort Dropdown */}
          <div className="relative">
            <button
               onClick={() => setSortMenuOpen(!sortMenuOpen)}
               className="flex items-center gap-2 rounded-lg bg-white px-3 py-3 font-medium text-brand-secondary text-brand-muted transition-colors hover:bg-surface-2"
             >
               <ArrowUpDown size={16} />
               <span className="text-xs hidden sm:inline">{SORT_OPTIONS.find(s => s.key === sortBy)?.label || "Sort"}</span>
              {SORT_OPTIONS.find(s => s.key === sortBy)?.icon && (
                <span className="w-1.5 h-1.5 rounded-full bg-vibe-accent" />
              )}
             </button>
             {sortMenuOpen && (
               <>
                 <div className="fixed inset-0 z-30" onClick={() => setSortMenuOpen(false)} />
                <div className="absolute right-0 left-0 top-full z-40 mt-1 w-full rounded-lg border border-black/5 bg-white py-1 shadow-xl sm:left-auto sm:w-auto sm:min-w-[176px]">
                  {SORT_OPTIONS.map((opt) => (
                    <button
                      key={opt.key}
                      onClick={() => { setSortBy(opt.key); setSortMenuOpen(false); }}
                      className={`flex items-center justify-between gap-2 w-full px-3 py-2.5 text-xs transition-colors ${
                        sortBy === opt.key
                          ? "bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 font-semibold"
                          : "text-brand-secondary text-brand-muted hover:bg-surface-card dark:hover:bg-gray-700"
                      }`}
                    >
                      <span className="flex items-center gap-1.5">{opt.icon} {opt.label}</span>
                      {sortBy === opt.key && (
                        <svg className="w-3 h-3 text-primary-500" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 0 1 0 1.414l-6 6a1 1 0 0 1-1.414 0l-3-3a1 1 0 1 1 1.414-1.414L10 10.586l5.293-5.293a1 1 0 0 1 1.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
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
                ? "bg-primary-600 text-text-primary"
                : "bg-white text-brand-secondary text-brand-muted hover:bg-surface-2"
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
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Company</label>
                <select value={selected.company} onChange={(e) => handleFilterChange("company", e.target.value)} className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
                  <option value="">All Companies</option>
                  {filters.companies.map((c) => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Role</label>
                <select value={selected.role} onChange={(e) => handleFilterChange("role", e.target.value)} className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
                  <option value="">All Roles</option>
                  {filters.roles.map((r) => <option key={r} value={r}>{r}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Type</label>
                <select value={selected.type} onChange={(e) => handleFilterChange("type", e.target.value)} className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
                  <option value="">All Types</option>
                  {filters.types.map((t) => <option key={t} value={t}>{TYPE_LABELS[t] || t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Difficulty</label>
                <select value={selected.difficulty} onChange={(e) => handleFilterChange("difficulty", e.target.value)} className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
                  <option value="">All Levels</option>
                  {filters.difficulties.map((d) => <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Topic</label>
                <select value={selected.topic} onChange={(e) => handleFilterChange("topic", e.target.value)} className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
                  <option value="">All Topics</option>
                  {filters.topics.map((t) => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Pattern (Striver)</label>
                <select value={selected.pattern} onChange={(e) => handleFilterChange("pattern", e.target.value)} className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
                  <option value="">All Patterns</option>
                  {filters.patterns.map((t) => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Source (Curated)</label>
                <select value={selected.source} onChange={(e) => handleFilterChange("source", e.target.value)} className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
                  <option value="">All Sources</option>
                  {filters.sources.map((s) => (
                    <option key={s} value={s}>{s === "blind75" ? "Blind 75" : s === "neetcode150" ? "NeetCode 150" : s === "striver" ? "Striver A2Z" : s.charAt(0).toUpperCase() + s.slice(1)}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary text-brand-secondary mb-1">Sub Topic</label>
                <select value={selected.sub_topic} onChange={(e) => handleFilterChange("sub_topic", e.target.value)} className="w-full px-3 py-2 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white text-sm">
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
              <button key={c} onClick={() => handleFilterChange("company", selected.company === c ? "" : c)} className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${selected.company === c ? "bg-primary-600 text-text-primary" : "bg-white text-brand-secondary text-brand-muted hover:bg-surface-2"}`}>
                {c}
              </button>
            ))}
          </div>
        )}

        {/* Loading */}
        {/* Loading */}
        {loading ? (
          <QuestionCardSkeleton count={5} />
        ) : browseData?.isError ? (
          <div className="card text-center py-12">
            <div className="bg-brand-accent/10 border border-brand-accent/20 text-brand-accent px-6 py-6 rounded-lg mb-4">
              <h3 className="text-brand-accent font-medium mb-2">Couldn't load questions</h3>
              <p className="text-brand-accent/80 text-sm mb-4">Failed to fetch questions. Please check your connection.</p>
              <button
                onClick={() => refetchBrowse({ companies: selected.company, roles: selected.role, topics: selected.topics, sub_topics: selected.sub_topics, types: selected.types, difficulties: selected.difficulties, patterns: selected.patterns, sources: selected.sources })}
                className="btn-primary mt-4"
              >
                Retry
              </button>
            </div>
            <p className="text-sm text-gray-400 dark:text-brand-muted">Try adjusting your filters</p>
          </div>
        ) : filteredQuestions.length === 0 ? (
          <div className="card text-center py-12">
            <BookOpen size={48} className="mx-auto text-gray-300 dark:text-brand-secondary mb-4" />
            <p className="text-brand-muted text-brand-muted mb-2">No questions found</p>
            <p className="text-sm text-gray-400 dark:text-brand-muted">Try adjusting your filters</p>
          </div>
        ) : (
          <div className="space-y-2">
            <VirtualList
              items={filteredQuestions}
              height={Math.min(600, filteredQuestions.length * 76)}
              itemHeight={76}
              renderItem={(q, index) => {
                const isSolved = solvedStatuses[q.id];
                const companyList = Array.isArray(q.company) ? q.company : [q.company].filter(Boolean);
                const rank = (page - 1) * 80 + index + 1;
                const gk = topicGroup(q.topic);
                return (
                  <div
                    className={`group flex items-center gap-3 rounded-2xl border px-4 py-3 transition-all cursor-pointer ${
                      isSolved
                        ? "border-emerald-200 bg-emerald-50/70 dark:border-emerald-800/50 dark:bg-emerald-900/5"
                        : "border-brand-primary/10 bg-surface-card hover:border-brand-sky/30 hover:shadow-sm dark:border-gray-800 bg-surface-base dark:hover:border-brand-sky/50"
                    }`}
                    onClick={() => handlePracticeClick(q.id)}
                  >
                    <div className="flex w-12 shrink-0 flex-col items-center justify-center text-center">
                      <span className="text-[10px] font-mono uppercase tracking-[0.22em] text-gray-400">#{rank}</span>
                      <div className="mt-1">
                        {isSolved ? (
                          <CheckCircle size={18} className="text-emerald-500" />
                        ) : (
                          <div className="h-4 w-4 rounded-full border-2 border-brand-primary/20 border-brand-primary/15 group-hover:border-brand-sky transition-colors" />
                        )}
                      </div>
                    </div>

                    <div className="shrink-0">
                      <Emblem
                        question={q}
                        difficulty={q.difficulty}
                        size="xs"
                        animated={false}
                        glow={false}
                      />
                    </div>

                    {/* Question Info */}
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="truncate text-sm font-semibold text-text-primary md:text-base">{q.question || q.question_title}</span>
                      </div>
                      <div className="mt-1 flex flex-wrap items-center gap-2">
                        <span className={`rounded px-1.5 py-0.5 text-[10px] ${DIFFICULTY_COLORS[q.difficulty] || ""}`}>
                          {q.difficulty}
                        </span>
                        {companyList.slice(0, 2).map((co) => (
                          <span key={co} className="rounded-full bg-blue-50 px-1.5 py-0.5 text-[10px] text-blue-600 dark:bg-blue-900/20 dark:text-blue-400">
                            {co}
                          </span>
                        ))}
                        <span className="text-[10px] text-gray-400">{q.topic}{q.sub_topic ? ` · ${q.sub_topic}` : ""}</span>
                        {q.type === "coding" && (
                          <span className={`rounded-full px-1.5 py-0.5 text-[10px] font-medium ${GROUP_META[gk].tag}`}>
                            {GROUP_META[gk].label}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Stats — mobile: acceptance-only condensed line; desktop: full row */}
                    <div className="flex min-w-[44px] max-w-[120px] shrink-0 items-center justify-end md:max-w-none md:mr-2 md:justify-start md:gap-4">
                      <div className="flex items-center gap-1 md:hidden">
                        {renderAcceptanceBar(q)}
                      </div>
                      <div className="hidden min-w-[44px] items-center gap-1 text-[10px] text-gray-400 md:flex">
                        <ThumbsUp size={10} />
                        <span className="tabular-nums">{q.upvotes || 0}</span>
                      </div>
                      <span className={`hidden min-w-[56px] rounded px-1.5 py-0.5 text-center text-[10px] md:inline-block ${TYPE_COLORS[q.type] || ""}`}>
                        {TYPE_LABELS[q.type] || q.type}
                      </span>
                    </div>

                    {/* Arrow */}
                    <ArrowRight size={14} className="shrink-0 text-gray-300 transition-colors group-hover:text-brand-sky" />
                  </div>
                );
              }}
            />
          </div>
        )}

        {/* Pagination (LeetCode-style numbered) */}
        {pages > 1 && (
          <div className="flex items-center justify-center gap-1 mt-8">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="p-2 rounded-lg text-brand-muted hover:bg-surface-2 disabled:opacity-30"
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
                   className={`h-9 w-8 rounded-lg text-xs font-medium transition-colors ${
                     page === pageNum
                       ? "bg-primary-600 text-text-primary"
                       : "text-brand-muted hover:bg-surface-2"
                   }`}
                >
                  {pageNum}
                </button>
              );
            })}
            <button
              onClick={() => setPage(Math.min(pages, page + 1))}
              disabled={page === pages}
              className="p-2 rounded-lg text-brand-muted hover:bg-surface-2 disabled:opacity-30"
            >
              <ChevronRight size={16} />
            </button>
            <span className="ml-3 text-xs text-brand-muted">{total} problems</span>
          </div>
        )}

        {/* Free Tier Usage */}
        {!isPro && (
          <div className="mt-8 card">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-brand-secondary text-brand-muted">Free Practice: {questionsPracticed}/{FREE_LIMIT} questions used</span>
              <Link to="/pricing" className="text-sm text-primary-600 hover:text-primary-700 font-medium">Upgrade to Pro →</Link>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-surface-2">
              <div className={`h-full rounded-full transition-all ${reachedFreeLimit ? "bg-red-500" : "bg-primary-500"}`} style={{ width: `${Math.min(100, (questionsPracticed / FREE_LIMIT) * 100)}%` }} />
            </div>
            {reachedFreeLimit && <p className="text-xs text-red-500 mt-2">Free limit reached. Upgrade to Pro for unlimited practice.</p>}
          </div>
        )}

        {/* Paywall Modal */}
        <AnimatePresence>
          {showPaywall && (
            <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-surface-2 backdrop-blur-sm p-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => setShowPaywall(false)}>
              <motion.div className="w-full max-w-md rounded-2xl bg-white p-8 text-center shadow-2xl" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }} onClick={(e) => e.stopPropagation()}>
                <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-2xl flex items-center justify-center mx-auto mb-4"><Lock size={32} className="text-primary-600" /></div>
                <h2 className="text-2xl font-bold mb-2 dark:text-white">Free Limit Reached</h2>
                <p className="text-brand-secondary text-brand-muted mb-6">You've used all {FREE_LIMIT} free practice questions this month. Upgrade to Pro for unlimited access to {total}+ curated questions.</p>
                <div className="bg-primary-50 dark:bg-primary-900/20 rounded-xl p-4 mb-6">
                  <div className="flex items-center justify-center gap-2 mb-2"><Zap size={18} className="text-primary-600" /><span className="font-bold text-primary-700 dark:text-primary-400">Pro — $9/mo</span></div>
                  <p className="text-sm text-brand-secondary text-brand-muted">Unlimited questions · Full solutions · Company filters · Mock tests</p>
                </div>
                <div className="flex gap-3">
                  <button onClick={() => setShowPaywall(false)} className="flex-1 rounded-lg bg-surface-2 px-4 py-3 font-medium text-brand-secondary hover:bg-surface-2">Later</button>
                  <Link to="/pricing" className="flex-1 px-4 py-3 rounded-lg bg-primary-600 text-text-primary font-medium hover:bg-primary-700 text-center" onClick={() => setShowPaywall(false)}>Upgrade to Pro</Link>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
