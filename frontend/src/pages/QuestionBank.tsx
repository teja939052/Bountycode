import { useState, useEffect, useMemo } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useQuestionFilters, useQuestionStats, useBrowseQuestions, useSolvedStatus, useDailyChallenge } from "../hooks/useQuestions";
import api from "../services/api";
import {
  BookOpen, Search, Filter, Hash, ExternalLink, ArrowRight, Lock, X, Zap, Plus,
  ThumbsUp, ThumbsDown, ChevronDown, ChevronLeft, ChevronRight, User, Briefcase,
  CheckCircle, Clock, TrendingUp, Target, Flame, Award, BarChart, Sparkles,
  ChevronUp, RotateCcw, Eye, Bookmark, ArrowUpDown, ArrowUp, ArrowDown, SortAsc
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import useAuthStore from "../store/authStore";
import { Emblem } from "../components/emblems";
import { GROUP_META, GROUP_ORDER, topicGroup } from "../utils/topicGroups";
import VirtualList from "../components/ui/VirtualList";
import { Card, SectionHeader } from "../design-system/Card";
import { Button } from "../design-system/Button";
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

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "bg-subject-verbal/10 text-subject-verbal border border-subject-verbal/20",
  medium: "bg-subject-aptitude/10 text-subject-aptitude border border-subject-aptitude/20",
  hard: "bg-subject-boss/10 text-subject-boss border border-subject-boss/20",
  expert: "bg-subject-interview/10 text-subject-interview border border-subject-interview/20",
};

const DIFFICULTY_DOT: Record<string, string> = {
  easy: "bg-subject-verbal",
  medium: "bg-subject-aptitude",
  hard: "bg-subject-boss",
  expert: "bg-subject-interview",
};

const TYPE_COLORS: Record<string, string> = {
  coding: "bg-subject-coding/10 text-subject-coding border border-subject-coding/20",
  aptitude: "bg-subject-aptitude/10 text-subject-aptitude border border-subject-aptitude/20",
  behavioral: "bg-subject-reasoning/10 text-subject-reasoning border border-subject-reasoning/20",
  system_design: "bg-subject-interview/10 text-subject-interview border border-subject-interview/20",
  hr: "bg-subject-reasoning/10 text-subject-reasoning border border-subject-reasoning/20",
};

const TYPE_LABELS: Record<string, string> = {
  coding: "Coding",
  aptitude: "Aptitude",
  behavioral: "Behavioral",
  system_design: "System Design",
  hr: "HR",
};

const QUICK_FILTERS = [
  { key: "all", label: "All Problems", icon: <Hash size={13} /> },
  { key: "solved", label: "Solved", icon: <CheckCircle size={13} />, color: "text-subject-verbal" },
  { key: "easy", label: "Easy", icon: <Target size={13} />, color: "text-subject-verbal" },
  { key: "medium", label: "Medium", icon: <Target size={13} />, color: "text-subject-aptitude" },
  { key: "hard", label: "Hard", icon: <Target size={13} />, color: "text-subject-boss" },
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
  const [showFilters, setShowFilters] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showSubmit, setShowSubmit] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState("");

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

  const handlePracticeClick = (questionId: string) => {
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
      const targetId = (data as any)?.id || (data as any)?.question_id || (data as any)?.problem?.id;
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
    refetchBrowse({ companies: selected.company, roles: selected.role, topics: selected.topic, sub_topics: selected.sub_topic, types: selected.type, difficulties: selected.difficulty, patterns: selected.pattern, sources: selected.source } as any);
  }, [selected, refetchFilters, refetchStats, refetchBrowse]);

  const handleFilterChange = (key: keyof QuestionFilters, value: string) => {
    setSelected((prev) => ({ ...prev, [key]: value }));
    setPage(1);
    refetchBrowse({ companies: selected.company, roles: selected.role, topics: selected.topic, sub_topics: selected.sub_topic, types: selected.type, difficulties: selected.difficulty, patterns: selected.pattern, sources: selected.source } as any);
  };

  const activeFilters = Object.values(selected).filter(Boolean).length;

  const handleQuickFilter = (filter: string) => {
    setQuickFilter(filter);
    if (filter === "all") {
      setSelected(prev => ({ ...prev, difficulty: "", search: "" }));
    } else if (filter === "solved") {
      setSelected(prev => ({ ...prev, difficulty: "" }));
    } else {
      setSelected(prev => ({ ...prev, difficulty: filter }));
    }
    setPage(1);
  };

  const handleSubmitQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const form = e.target as HTMLFormElement;
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
      refetchBrowse({ companies: selected.company, roles: selected.role, topics: selected.topic, sub_topics: selected.sub_topic, types: selected.type, difficulties: selected.difficulty, patterns: selected.pattern, sources: selected.source } as any);
    } catch {} finally {
      setSubmitting(false);
    }
  };

  const handleUpvote = async (e: React.MouseEvent, questionId: string) => {
    e.stopPropagation();
    try {
      await api.upvoteQuestion(questionId, 1);
    } catch {}
  };

  const filteredQuestions = useMemo(() => {
    let list = quickFilter === "solved"
      ? questions.filter(q => solvedMap[q.id])
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
  }, [questions, quickFilter, solvedMap, sortBy, category]);

  const difficultyDistribution = useMemo(() => {
    if (!stats?.by_difficulty) return null;
    const { easy = 0, medium = 0, hard = 0, expert = 0 } = stats.by_difficulty;
    const total = easy + medium + hard + expert;
    if (total === 0) return null;
    return { easy, medium, hard, expert, total };
  }, [stats]);

  const renderAcceptanceBar = (q: any) => {
    const rate = q.acceptance_rate;
    if (rate == null) return null;
    const barColor = rate >= 60 ? "bg-subject-verbal" : rate >= 40 ? "bg-subject-aptitude" : "bg-subject-boss";
    return (
      <div className="flex items-center gap-1.5">
        <div className="w-16 h-1.5 bg-border/30 rounded-full overflow-hidden">
          <div className={`h-full rounded-full ${barColor}`} style={{ width: `${Math.min(100, rate)}%` }} />
        </div>
        <span className="text-[10px] text-text-muted tabular-nums">{rate}%</span>
      </div>
    );
  };

  return (
    <div className="page-surface min-h-screen py-6 px-3 sm:px-4">
      <div className="mx-auto max-w-4xl lg:max-w-6xl">
        {/* Header */}
        <motion.div className="mb-6" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <Card pad="md" className="relative overflow-hidden">
            <div className="absolute inset-0 bg-primary/5 pointer-events-none" />
            <div className="relative z-10 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
              <div className="max-w-3xl">
                <div className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/10 px-3 py-1 text-[10px] font-mono uppercase tracking-[0.28em] text-primary">
                  <Sparkles size={10} />
                  LeetCode-style practice hub
                </div>
                <h1 className="mt-3 text-3xl font-black tracking-tight text-text md:text-4xl">
                  Solve better questions, faster
                </h1>
                <p className="mt-3 max-w-2xl text-sm leading-6 text-text-secondary">
                  Browse curated company questions, jump into a random solve, or filter by topic and difficulty to build real interview readiness.
                </p>
                <div className="mt-4 flex flex-wrap items-center gap-2">
                  <Button
                    variant="primary"
                    onClick={handleRandomPractice}
                    disabled={randomLoading}
                    size="md"
                    leftIcon={randomLoading ? <Zap size={14} className="animate-pulse" /> : <ArrowRight size={14} />}
                    className="text-sm font-bold shadow-primary"
                  >
                    Random solve
                  </Button>
                  <Button variant="outline" onClick={() => setShowFilters(true)} size="md" leftIcon={<Filter size={14} />}>
                    Filters
                  </Button>
                  <Button variant="gold" onClick={() => setShowSubmit(!showSubmit)} size="md" leftIcon={<Plus size={14} />}>
                    Submit question
                  </Button>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:w-[460px]">
                <Card pad="sm" tone="default" className="text-center flex flex-col items-center justify-center h-full">
                  <div className="text-2xl font-black text-text">{stats?.total_solved || 0}</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-text-muted">Solved</div>
                </Card>
                <Card pad="sm" tone="default" className="text-center flex flex-col items-center justify-center h-full">
                  <div className="text-2xl font-black text-text">{stats?.acceptance_rate || 0}%</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-text-muted">Avg acceptance</div>
                </Card>
                <Card pad="sm" tone="default" className="text-center flex flex-col items-center justify-center h-full">
                  <div className="text-2xl font-black text-text">{questions.length}</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-text-muted">Loaded</div>
                </Card>
                <Card pad="sm" tone="default" className="text-center flex flex-col items-center justify-center h-full">
                  <div className="text-2xl font-black text-text">{pages || 1}</div>
                  <div className="mt-1 text-[10px] font-mono uppercase tracking-[0.24em] text-text-muted">Pages</div>
                </Card>
              </div>
            </div>
          </Card>
        </motion.div>

        {dailyChallengeData?.problem && (
          <motion.div
            className="mb-6 overflow-hidden rounded-2xl border border-primary/20 bg-gradient-to-r from-primary via-subject-coding to-subject-verbal text-text shadow-primary-lg"
            initial={reduced ? {} : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="p-5 sm:p-6 flex flex-col lg:flex-row lg:items-center gap-4 relative z-10">
              <div className="flex items-start gap-4 flex-1 min-w-0">
                <div className="w-12 h-12 rounded-2xl bg-white/10 flex items-center justify-center shrink-0">
                  <Sparkles size={22} />
                </div>
                <div className="min-w-0">
                  <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-text-secondary">Featured today</div>
                  <h2 className="mt-1 text-xl sm:text-2xl font-black truncate">{dailyChallengeData.problem.question_title || dailyChallengeData.problem.question || "Today's Problem"}</h2>
                  <p className="mt-2 text-sm text-text-secondary">
                    {dailyChallengeData.config?.category} · {dailyChallengeData.config?.focus} · {dailyChallengeData.streak_bonus || 0} XP bonus
                  </p>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-2 lg:justify-end shrink-0">
                <span className="px-3 py-1 rounded-full bg-white/10 text-[10px] font-bold uppercase tracking-wide text-primary">
                  {dailyChallengeData.config?.difficulty || "medium"}
                </span>
                <Link to="/daily-challenge" className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-white/5 text-text font-semibold text-sm border border-white/10 hover:bg-white/10 transition-colors">
                  Open Daily Challenge
                  <ArrowRight size={14} />
                </Link>
                {dailyChallengeData.problem?.id && (
                  <Link to={`/solve/${dailyChallengeData.problem.id}`} className="inline-flex items-center gap-2 px-4 py-2 rounded-xl border border-white/20 text-text font-semibold text-sm hover:bg-white/10 transition-colors">
                    Solve Now
                  </Link>
                )}
              </div>
            </div>
          </motion.div>
        )}

        {/* Stats Summary */}
        {showStats && stats && (
          <motion.div className="mb-6" initial={reduced ? {} : { opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
            <Card pad="md">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-bold text-text flex items-center gap-2">
                  <BarChart size={14} /> Your Progress
                </h2>
                <button onClick={() => setShowStats(false)} className="text-text-muted hover:text-text">
                  <ChevronUp size={14} />
                </button>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-black text-text">{stats.total_solved || 0}</div>
                  <div className="text-[10px] text-text-muted uppercase tracking-wide">Solved</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-subject-verbal">{stats.easy_solved || 0}/{difficultyDistribution?.easy || 0}</div>
                  <div className="text-[10px] text-text-muted uppercase tracking-wide">Easy</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-subject-aptitude">{stats.medium_solved || 0}/{difficultyDistribution?.medium || 0}</div>
                  <div className="text-[10px] text-text-muted uppercase tracking-wide">Medium</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-subject-boss">{stats.hard_solved || 0}/{difficultyDistribution?.hard || 0}</div>
                  <div className="text-[10px] text-text-muted uppercase tracking-wide">Hard</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-subject-interview">{stats.expert_solved || 0}/{difficultyDistribution?.expert || 0}</div>
                  <div className="text-[10px] text-text-muted uppercase tracking-wide">Expert</div>
                </div>
              </div>
              {difficultyDistribution && (
                <div className="mt-4">
                  <div className="flex h-2 overflow-hidden rounded-full bg-surface/40">
                    {(difficultyDistribution.easy / difficultyDistribution.total * 100) > 0 && (
                      <div className="h-full bg-subject-verbal" style={{ width: `${difficultyDistribution.easy / difficultyDistribution.total * 100}%` }} />
                    )}
                    {(difficultyDistribution.medium / difficultyDistribution.total * 100) > 0 && (
                      <div className="h-full bg-subject-aptitude" style={{ width: `${difficultyDistribution.medium / difficultyDistribution.total * 100}%` }} />
                    )}
                    {(difficultyDistribution.hard / difficultyDistribution.total * 100) > 0 && (
                      <div className="h-full bg-subject-boss" style={{ width: `${difficultyDistribution.hard / difficultyDistribution.total * 100}%` }} />
                    )}
                    {(difficultyDistribution.expert / difficultyDistribution.total * 100) > 0 && (
                      <div className="h-full bg-subject-interview" style={{ width: `${difficultyDistribution.expert / difficultyDistribution.total * 100}%` }} />
                    )}
                  </div>
                </div>
              )}
            </Card>
          </motion.div>
        )}

        {showStats === false && stats && (
          <button onClick={() => setShowStats(true)} className="mb-4 text-xs text-text-muted hover:text-text flex items-center gap-1">
            <BarChart size={12} /> Show Stats
          </button>
        )}

        {/* Submit Form */}
        {showSubmit && (
          <Card pad="md" className="mb-6">
            <h2 className="text-xl font-black mb-4 text-text">Submit a Question</h2>
            {submitted && <p className="text-sm text-subject-verbal mb-2">Submitted! ID: {submitted}</p>}
            <form onSubmit={handleSubmitQuestion} className="grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Type</label>
                <select name="type" className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" required>
                  <option value="aptitude">Aptitude</option>
                  <option value="coding">Coding</option>
                  <option value="behavioral">Behavioral</option>
                  <option value="system_design">System Design</option>
                  <option value="hr">HR</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Company</label>
                <input name="company" placeholder="e.g. Google" required className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Role</label>
                <input name="role" placeholder="SDE" defaultValue="SDE" className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Difficulty</label>
                <select name="difficulty" className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                  <option value="expert">Expert</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Topic</label>
                <input name="topic" placeholder="e.g. Arrays" required className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Sub Topic</label>
                <input name="sub_topic" placeholder="e.g. Sliding Window" className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div className="md:col-span-2">
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Question</label>
                <textarea name="question" rows={3} placeholder="Enter the question text..." required className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div className="md:col-span-2">
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Options (one per line, for MCQ)</label>
                <textarea name="options" rows={3} placeholder="Option A\nOption B\nOption C\nOption D" className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Correct Answer</label>
                <input name="correct_answer" placeholder="e.g. Option A" className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div>
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Explanation</label>
                <input name="explanation" placeholder="Why this is correct..." className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div className="md:col-span-2">
                <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Hints (one per line)</label>
                <textarea name="hints" rows={2} placeholder="Hint 1\nHint 2" className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm" />
              </div>
              <div className="md:col-span-2 flex gap-2">
                <Button variant="primary" type="submit" disabled={submitting} className="text-sm font-bold shadow-primary">
                  {submitting ? "Submitting..." : "Submit Question"}
                </Button>
                <Button variant="ghost" type="button" onClick={() => setShowSubmit(false)} className="text-sm">
                  Cancel
                </Button>
              </div>
            </form>
          </Card>
        )}

        {/* Category Filters */}
        <div className="flex items-center gap-1 mb-2 overflow-x-auto pb-1">
          {CATEGORY_FILTERS.map((f) => {
            const meta = f.key === "all" ? null : GROUP_META[f.key];
            return (
              <button
                key={f.key}
                onClick={() => setCategory(f.key)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all whitespace-nowrap border ${
                  category === f.key
                    ? "bg-primary text-text-primary border-primary shadow-primary"
                    : "border-border/30 bg-surfaceHover text-text-secondary hover:bg-surfaceHover hover:border-primary/30"
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
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all whitespace-nowrap ${
                quickFilter === f.key
                  ? "bg-primary text-text-primary shadow-primary"
                  : "border border-border/30 bg-surfaceHover text-text-secondary hover:bg-surfaceHover"
              }`}
            >
              {f.icon} <span>{f.label}</span>
            </button>
          ))}
        </div>

        {/* Search + Filter + Sort */}
        <div className="flex gap-3 mb-6">
          <div className="relative flex-1">
            <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
            <input
              type="text"
              placeholder="Search questions by name, topic, or company..."
              value={selected.search}
              onChange={(e) => handleFilterChange("search", e.target.value)}
              className="w-full pl-10 pr-4 py-3 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm placeholder-text-text-muted"
            />
          </div>
          <div className="relative">
            <button
              onClick={() => setSortMenuOpen(!sortMenuOpen)}
              className="flex items-center gap-2 rounded-xl border border-border/50 bg-surfaceHover px-3 py-3 font-medium text-text-secondary transition-colors hover:border-primary/50"
            >
              <ArrowUpDown size={16} />
              <span className="text-xs hidden sm:inline">{SORT_OPTIONS.find(s => s.key === sortBy)?.label || "Sort"}</span>
              {SORT_OPTIONS.find(s => s.key === sortBy)?.icon && (
                <span className="w-1.5 h-1.5 rounded-full bg-primary" />
              )}
            </button>
            {sortMenuOpen && (
              <>
                <div className="fixed inset-0 z-30" onClick={() => setSortMenuOpen(false)} />
                <div className="absolute right-0 left-0 top-full z-40 mt-1 w-full rounded-2xl border border-border bg-surface shadow-card py-1 sm:left-auto sm:w-auto sm:min-w-[176px]">
                  {SORT_OPTIONS.map((opt) => (
                    <button
                      key={opt.key}
                      onClick={() => { setSortBy(opt.key); setSortMenuOpen(false); }}
                      className={`flex items-center justify-between gap-2 w-full px-3 py-2.5 text-xs transition-colors ${
                        sortBy === opt.key
                          ? "bg-primary/10 text-primary font-semibold border border-primary/20"
                          : "text-text-secondary hover:bg-surfaceHover hover:text-text"
                      }`}
                    >
                      <span className="flex items-center gap-1.5">{opt.icon} {opt.label}</span>
                      {sortBy === opt.key && (
                        <svg className="w-3 h-3 text-primary" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 0 1 0 1.414l-6 6a1 1 0 0 1-1.414 0l-3-3a1 1 0 1 1 1.414-1.414L10 10.586l5.293-5.293a1 1 0 0 1 1.414 0z" clipRule="evenodd" />
                        </svg>
                      )}
                    </button>
                  ))}
                </div>
              </>
            )}
          </div>
          <Button
            variant={showFilters || activeFilters > 0 ? "primary" : "outline"}
            onClick={() => setShowFilters(!showFilters)}
            size="md"
            leftIcon={<Filter size={18} />}
            className={`flex items-center gap-2 ${showFilters || activeFilters > 0 ? "" : "text-text-secondary"}`}
          >
            Filters {activeFilters > 0 && `(${activeFilters})`}
          </Button>
        </div>

        {/* Advanced Filters */}
        {showFilters && (
          <motion.div initial={reduced ? {} : { opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }}>
            <Card pad="md" className="mb-6">
              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Company</label>
                  <select value={selected.company} onChange={(e) => handleFilterChange("company", e.target.value)} className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                    <option value="">All Companies</option>
                    {filtersData.companies.map((c: string) => <option key={c} value={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Role</label>
                  <select value={selected.role} onChange={(e) => handleFilterChange("role", e.target.value)} className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                    <option value="">All Roles</option>
                    {filtersData.roles.map((r: string) => <option key={r} value={r}>{r}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Type</label>
                  <select value={selected.type} onChange={(e) => handleFilterChange("type", e.target.value)} className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                    <option value="">All Types</option>
                    {filtersData.types.map((t: string) => <option key={t} value={t}>{TYPE_LABELS[t] || t}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Difficulty</label>
                  <select value={selected.difficulty} onChange={(e) => handleFilterChange("difficulty", e.target.value)} className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                    <option value="">All Levels</option>
                    {filtersData.difficulties.map((d: string) => <option key={d} value={d}>{d.charAt(0).toUpperCase() + d.slice(1)}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Topic</label>
                  <select value={selected.topic} onChange={(e) => handleFilterChange("topic", e.target.value)} className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                    <option value="">All Topics</option>
                    {filtersData.topics.map((t: string) => <option key={t} value={t}>{t}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Pattern (Striver)</label>
                  <select value={selected.pattern} onChange={(e) => handleFilterChange("pattern", e.target.value)} className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                    <option value="">All Patterns</option>
                    {filtersData.patterns.map((t: string) => <option key={t} value={t}>{t}</option>)}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Source (Curated)</label>
                  <select value={selected.source} onChange={(e) => handleFilterChange("source", e.target.value)} className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                    <option value="">All Sources</option>
                    {filtersData.sources.map((s: string) => (
                      <option key={s} value={s}>{s === "blind75" ? "Blind 75" : s === "neetcode150" ? "NeetCode 150" : s === "striver" ? "Striver A2Z" : s.charAt(0).toUpperCase() + s.slice(1)}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">Sub Topic</label>
                  <select value={selected.sub_topic} onChange={(e) => handleFilterChange("sub_topic", e.target.value)} className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm">
                    <option value="">All Sub Topics</option>
                    {filtersData.sub_topics.map((t: string) => <option key={t} value={t}>{t}</option>)}
                  </select>
                </div>
              </div>
              {activeFilters > 0 && (
                <div className="mt-4 flex items-center gap-3">
                  <button onClick={() => setSelected({ company: "", role: "", type: "", difficulty: "", topic: "", sub_topic: "", pattern: "", source: "", search: "" })} className="text-sm text-primary font-medium flex items-center gap-1"><RotateCcw size={12} /> Clear all filters</button>
                  <span className="text-sm text-text-muted">{total} questions found</span>
                </div>
              )}
            </Card>
          </motion.div>
        )}

        {/* Company Quick Chips */}
        {!showFilters && (
          <div className="flex flex-wrap gap-2 mb-6">
            {["TCS", "Infosys", "Google", "Amazon", "Microsoft", "Meta", "Wipro", "Uber"].map((c) => (
              <button key={c} onClick={() => handleFilterChange("company", selected.company === c ? "" : c)} className={`px-3 py-1.5 rounded-xl text-sm font-medium transition-colors ${selected.company === c ? "bg-primary text-text-primary" : "border border-border/30 bg-surfaceHover text-text-secondary hover:bg-surfaceHover hover:border-primary/50"}`}>
                {c}
              </button>
            ))}
          </div>
        )}

        {/* Loading */}
        {loading ? (
          <QuestionCardSkeleton count={5} />
        ) : filteredQuestions.length === 0 ? (
          <Card tone="default" className="text-center py-12">
            <BookOpen size={48} className="mx-auto text-text-muted mb-4" />
            <p className="text-text-muted mb-2">No questions found</p>
            <p className="text-[10px] text-text-muted">Try adjusting your filters</p>
          </Card>
        ) : (
          <div className="space-y-2">
            <VirtualList
              items={filteredQuestions}
              height={Math.min(600, filteredQuestions.length * 76)}
              itemHeight={76}
              renderItem={(q: any, index: number) => {
                const isSolved = solvedMap[q.id];
                const companyList = Array.isArray(q.company) ? q.company : [q.company].filter(Boolean);
                const rank = (page - 1) * 80 + index + 1;
                const gk = topicGroup(q.topic);
                return (
                  <div
                    className={`group flex items-center gap-3 rounded-2xl border px-4 py-3 transition-all cursor-pointer ${
                      isSolved
                        ? "border-subject-verbal/30 bg-subject-verbal/5"
                        : "border-border/30 bg-surfaceHover hover:border-primary/50 hover:shadow-card-hover"
                    }`}
                    onClick={() => handlePracticeClick(q.id)}
                  >
                    <div className="flex w-12 shrink-0 flex-col items-center justify-center text-center">
                      <span className="text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted">#{rank}</span>
                      <div className="mt-1">
                        {isSolved ? (
                          <CheckCircle size={18} className="text-subject-verbal" />
                        ) : (
                          <div className="h-4 w-4 rounded-full border-2 border-border/50 group-hover:border-primary transition-colors" />
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

                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2">
                        <span className="truncate text-sm font-semibold text-text md:text-base">{q.question || q.question_title}</span>
                      </div>
                      <div className="mt-1 flex flex-wrap items-center gap-2">
                        <span className={`rounded px-1.5 py-0.5 text-[10px] ${DIFFICULTY_COLORS[q.difficulty] || ""}`}>
                          {q.difficulty}
                        </span>
                        {companyList.slice(0, 2).map((co: string) => (
                          <span key={co} className="rounded-full bg-border/50 px-1.5 py-0.5 text-[10px] font-medium text-text-secondary">
                            {co}
                          </span>
                        ))}
                        <span className="text-[10px] text-text-muted">{q.topic}{q.sub_topic ? ` · ${q.sub_topic}` : ""}</span>
                        {q.type === "coding" && (
                          <span className={`rounded-full px-1.5 py-0.5 text-[10px] font-medium ${GROUP_META[gk].tag || "bg-primary/10 text-primary"}`}>
                            {GROUP_META[gk].label}
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="flex min-w-[44px] max-w-[120px] shrink-0 items-center justify-end md:max-w-none md:mr-2 md:justify-start md:gap-4">
                      <div className="flex items-center gap-1 md:hidden">
                        {renderAcceptanceBar(q)}
                      </div>
                      <div className="hidden min-w-[44px] items-center gap-1 text-[10px] text-text-muted md:flex">
                        <ThumbsUp size={10} />
                        <span className="tabular-nums">{q.upvotes || 0}</span>
                      </div>
                      <span className={`hidden min-w-[56px] rounded px-1.5 py-0.5 text-center text-[10px] md:inline-block ${TYPE_COLORS[q.type] || ""}`}>
                        {TYPE_LABELS[q.type] || q.type}
                      </span>
                    </div>

                    <ArrowRight size={14} className="shrink-0 text-text-muted transition-colors group-hover:text-primary" />
                  </div>
                );
              }}
            />
          </div>
        )}

        {/* Pagination */}
        {pages > 1 && (
          <div className="flex items-center justify-center gap-1 mt-8">
            <button
              onClick={() => setPage(Math.max(1, page - 1))}
              disabled={page === 1}
              className="p-2 rounded-xl text-text-muted hover:bg-surfaceHover disabled:opacity-30"
            >
              <ChevronLeft size={16} />
            </button>
            {Array.from({ length: Math.min(pages, 7) }, (_, i) => {
              let pageNum: number;
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
                  className={`h-9 w-8 rounded-xl text-xs font-medium transition-colors ${
                    page === pageNum
                      ? "bg-primary text-text-primary shadow-primary"
                      : "text-text-muted hover:bg-surfaceHover"
                  }`}
                >
                  {pageNum}
                </button>
              );
            })}
            <button
              onClick={() => setPage(Math.min(pages, page + 1))}
              disabled={page === pages}
              className="p-2 rounded-xl text-text-muted hover:bg-surfaceHover disabled:opacity-30"
            >
              <ChevronRight size={16} />
            </button>
            <span className="ml-3 text-xs text-text-muted">{total} problems</span>
          </div>
        )}

        {/* Free Tier Usage */}
        {!isPro && (
          <Card tone="default" className="mt-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-text-secondary">Free Practice: {questionsPracticed}/{FREE_LIMIT} questions used</span>
              <Link to="/pricing" className="text-sm text-primary font-medium hover:text-primary-dark">Upgrade to Pro →</Link>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-surface/40">
              <div className={`h-full rounded-full transition-all ${reachedFreeLimit ? "bg-subject-boss" : "bg-primary"}`} style={{ width: `${Math.min(100, (questionsPracticed / FREE_LIMIT) * 100)}%` }} />
            </div>
            {reachedFreeLimit && <p className="text-xs text-subject-boss mt-2">Free limit reached. Upgrade to Pro for unlimited practice.</p>}
          </Card>
        )}

        {/* Paywall Modal */}
        <AnimatePresence>
          {showPaywall && (
            <motion.div className="fixed inset-0 z-50 flex items-center justify-center bg-surface/80 backdrop-blur p-4" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => setShowPaywall(false)}>
              <motion.div className="w-full max-w-md rounded-2xl bg-surface p-8 text-center shadow-modal" initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }} onClick={(e) => e.stopPropagation()}>
                <div className="w-16 h-16 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-4"><Lock size={32} className="text-primary" /></div>
                <h2 className="text-2xl font-black mb-2 text-text">Free Limit Reached</h2>
                <p className="text-text-secondary mb-6">You've used all {FREE_LIMIT} free practice questions this month. Upgrade to Pro for unlimited access to {total}+ curated questions.</p>
                <div className="bg-primary/10 rounded-xl p-4 mb-6">
                  <div className="flex items-center justify-center gap-2 mb-2"><Zap size={18} className="text-primary" /><span className="font-bold text-text">Pro — $9/mo</span></div>
                  <p className="text-[10px] text-text-muted">Unlimited questions · Full solutions · Company filters · Mock tests</p>
                </div>
                <div className="flex gap-3">
                  <button onClick={() => setShowPaywall(false)} className="flex-1 rounded-xl border border-border/50 bg-surfaceHover px-4 py-3 font-medium text-text-secondary hover:bg-surfaceHover">Later</button>
                  <Link to="/pricing" className="flex-1 px-4 py-3 rounded-xl bg-primary text-text-primary font-medium hover:bg-primary-dark text-center" onClick={() => setShowPaywall(false)}>Upgrade to Pro</Link>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
