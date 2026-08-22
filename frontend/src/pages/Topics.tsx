import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import { BookOpen, ChevronRight, CheckCircle, Target, Flame, Database, Workflow, Sparkles, Briefcase, Layers } from "lucide-react";
import AnimatedCard from "../components/motion/AnimatedCard";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import useReducedMotion from "../hooks/useReducedMotion";
import { GROUP_META, GROUP_ORDER, TOPIC_DESCRIPTIONS, topicGroup } from "../utils/topicGroups";

const TOPIC_ICONS = {
  "Arrays": "01",
  "Linked Lists": "02",
  "Stacks & Queues": "03",
  "Trees": "04",
  "Graphs": "05",
  "Dynamic Programming": "06",
  "Greedy": "07",
  "Tries": "08",
  "Heaps": "09",
  "Sorting": "10",
  "Searching": "11",
  "Bit Manipulation": "12",
  "Math": "13",
  "Strings": "14",
  "Binary Search": "15",
  "Two Pointers": "16",
  "Sliding Window": "17",
  "Backtracking": "18",
  "Intervals": "19",
  "Prefix Sum": "20",
  "Monotonic Stack": "21",
  "Union Find": "22",
  "Hash Table": "23",
  "Design": "24",
  "Aptitude": "25",
  "Logical Reasoning": "26",
  "Verbal Ability": "27",
  "Coding Challenges": "28",
};

const TOPIC_COLORS = {
  "Arrays": "from-blue-500 to-cyan-500",
  "Linked Lists": "from-purple-500 to-pink-500",
  "Stacks & Queues": "from-orange-500 to-red-500",
  "Trees": "from-green-500 to-emerald-500",
  "Graphs": "from-indigo-500 to-blue-500",
  "Dynamic Programming": "from-yellow-500 to-orange-500",
  "Greedy": "from-pink-500 to-rose-500",
  "Tries": "from-teal-500 to-cyan-500",
  "Heaps": "from-violet-500 to-purple-500",
  "Sorting": "from-amber-500 to-yellow-500",
  "Searching": "from-sky-500 to-blue-500",
  "Bit Manipulation": "from-fuchsia-500 to-purple-500",
  "Math": "from-lime-500 to-green-500",
  "Strings": "from-red-500 to-pink-500",
  "Binary Search": "from-cyan-500 to-teal-500",
  "Two Pointers": "from-blue-500 to-indigo-500",
  "Sliding Window": "from-emerald-500 to-teal-500",
  "Backtracking": "from-orange-500 to-amber-500",
  "Intervals": "from-slate-500 to-gray-600",
  "Prefix Sum": "from-teal-500 to-emerald-500",
  "Monotonic Stack": "from-indigo-500 to-violet-500",
  "Union Find": "from-rose-500 to-red-500",
  "Hash Table": "from-amber-500 to-orange-500",
  "Design": "from-gray-500 to-slate-600",
  "Aptitude": "from-green-500 to-lime-500",
  "Logical Reasoning": "from-purple-500 to-fuchsia-500",
  "Verbal Ability": "from-pink-500 to-rose-500",
  "Coding Challenges": "from-cyan-500 to-blue-500",
};

function normalizeTopic(name) {
  return String(name || "").toLowerCase().replace(/[\s-]+/g, "").replace(/&/g, "");
}

export default function Topics() {
  const [topics, setTopics] = useState([]);
  const [progress, setProgress] = useState(null);
  const [topicProgress, setTopicProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeGroup, setActiveGroup] = useState("all");
  const reduced = useReducedMotion();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [topicsData, progressData, topicProgressData] = await Promise.all([
        api.questions.getTopics(),
        api.getProblemProgress(),
        api.getTopicProgress(),
      ]);
      setTopics(topicsData.topics || []);
      setProgress(progressData);
      setTopicProgress(topicProgressData?.topics || []);
    } catch (err) {
      console.error("Failed to load topics:", err);
    } finally {
      setLoading(false);
    }
  };

  const progressFor = (topicName) => {
    const norm = normalizeTopic(topicName);
    return topicProgress.find((t) => normalizeTopic(t.topic) === norm);
  };

  if (loading) {
    return (
      <div className="page-surface min-h-screen py-6 px-4">
        <div className="mx-auto max-w-6xl">
          <div className="space-y-4">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="card animate-pulse bg-white">
                <div className="mb-2 h-6 w-1/3 rounded bg-black/5" />
                <div className="h-4 w-1/2 rounded bg-black/5" />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const overallPercentage = progress
    ? Math.min(100, Math.round((progress.total_solved / (progress.total_problems || 1)) * 100))
    : 0;
  const hasTopicProgress = topicProgress.length > 0;

  const byGroup = {};
  GROUP_ORDER.forEach((key) => { byGroup[key] = []; });
  topics.forEach((topic) => {
    byGroup[topicGroup(topic.topic)].push(topic);
  });

  const visibleGroups = activeGroup === "all"
    ? GROUP_ORDER
    : GROUP_ORDER.filter((key) => key === activeGroup);

  const sectionStats = (groupTopics) => {
    const total = groupTopics.reduce((sum, t) => sum + (t.total || 0), 0);
    const solved = groupTopics.reduce((sum, t) => {
      const p = progressFor(t.topic);
      return sum + (p?.solved || 0);
    }, 0);
    return { total, solved, pct: total ? Math.round((solved / total) * 100) : 0 };
  };

  const FILTERS = [
    { key: "all", label: "All", icon: Layers },
    { key: "data_structure", label: "Data Structures", icon: Database },
    { key: "algorithm", label: "Algorithms", icon: Workflow },
    { key: "pattern", label: "Patterns", icon: Sparkles },
    { key: "career", label: "Career & Aptitude", icon: Briefcase },
  ];

  return (
    <div className="page-surface min-h-screen py-6 px-4">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <motion.div
          className="mb-6"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="mb-2 flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-[#4F8F57] to-[#7BB661]">
              <BookOpen size={24} className="text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-text-primary">DSA Practice</h1>
              <p className="text-brand-secondary">
                Organized by data structure, algorithm and pattern
              </p>
            </div>
          </div>
        </motion.div>

        {/* Overall Progress */}
        {progress && (
          <AnimatedCard className="card mb-6 bg-white">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <Target size={20} className="text-primary-600" />
                <h2 className="text-lg font-bold text-text-primary">Overall Progress</h2>
              </div>
              <div className="flex items-center gap-2">
                <Flame size={16} className="text-orange-500" />
                <span className="text-sm font-medium text-brand-secondary dark:text-gray-400">
                  {progress.total_solved}/{progress.total_problems} solved
                </span>
              </div>
            </div>
            <div className="mb-3 h-3 overflow-hidden rounded-full bg-black/5">
              <motion.div
                className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-600"
                initial={{ width: 0 }}
                animate={{ width: `${overallPercentage}%` }}
                transition={{ duration: 1, ease: "easeOut" }}
              />
            </div>
            <div className="flex items-center justify-between text-sm text-text-muted">
              <span>{overallPercentage}% complete</span>
              <span>{progress.total_problems - progress.total_solved} remaining</span>
            </div>
          </AnimatedCard>
        )}

        {/* Filter Tabs */}
        <motion.div
          className="flex flex-wrap gap-2 mb-8"
          initial={reduced ? {} : { opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
        >
          {FILTERS.map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setActiveGroup(key)}
              className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-sm font-medium transition-all border ${
                activeGroup === key
                ? "bg-primary-600 text-white border-primary-600 shadow-lg shadow-primary-600/25"
                  : "bg-white text-brand-secondary border-black/5 hover:border-primary-400"
              }`}
            >
              <Icon size={15} />
              {label}
            </button>
          ))}
        </motion.div>

        {/* Grouped Topic Sections */}
        <AnimatePresence mode="popLayout">
          {visibleGroups.map((groupKey) => {
            const groupTopics = byGroup[groupKey];
            if (!groupTopics.length) return null;
            const meta = GROUP_META[groupKey];
            const Icon = meta.icon;
            const stats = sectionStats(groupTopics);
            return (
              <motion.section
                key={groupKey}
                layout
                initial={reduced ? {} : { opacity: 0, y: 16 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                className="mb-10"
              >
                {/* Section header */}
                <div className="flex items-center gap-3 mb-5">
                  <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${meta.color} flex items-center justify-center text-white shadow-lg`}>
                    <Icon size={22} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h2 className="text-xl font-bold text-text-primary">{meta.label}</h2>
                    <p className="text-sm text-text-muted">{meta.description}</p>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-lg font-bold text-primary-600 dark:text-primary-400">{stats.pct}%</div>
                    <div className="text-xs text-text-muted">{stats.solved}/{stats.total} solved</div>
                  </div>
                </div>
                {hasTopicProgress && (
                    <div className="mb-5 h-1.5 overflow-hidden rounded-full bg-black/5">
                    <div
                      className="h-full rounded-full bg-gradient-to-r from-primary-500 to-primary-600 transition-all duration-700"
                      style={{ width: `${stats.pct}%` }}
                    />
                  </div>
                )}

                <StaggerContainer className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {groupTopics.map((topic) => {
                    const topicProgress = progressFor(topic.topic);
                    const solved = topicProgress?.solved || 0;
                    const percentage = topicProgress?.percentage || 0;
                    const colorClass = TOPIC_COLORS[topic.topic] || "from-gray-500 to-gray-600";

                    return (
                      <StaggerItem key={topic.topic}>
                        <Link to={`/problems/${encodeURIComponent(topic.topic)}`}>
                          <motion.div
                            whileHover={reduced ? {} : { y: -4, scale: 1.02 }}
                                className="card h-full cursor-pointer group bg-white"
                          >
                            <div className="flex items-start justify-between mb-3">
                              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${colorClass} flex items-center justify-center text-white font-bold text-sm`}>
                                {TOPIC_ICONS[topic.topic] || "XX"}
                              </div>
                              <ChevronRight
                                size={20}
                                className="text-gray-400 group-hover:text-primary-600 transition-colors"
                              />
                            </div>
                            <h3 className="text-lg font-bold dark:text-white mb-1">{topic.topic}</h3>
                              <p className="mb-2 text-xs leading-relaxed text-text-muted">
                              {TOPIC_DESCRIPTIONS[topic.topic] || "Practice problems"}
                            </p>
                              <p className="mb-3 text-sm text-text-muted">
                              {topic.total} problems
                            </p>

                            {/* Difficulty badges */}
                            <div className="flex gap-2 mb-3">
                              {topic.easy > 0 && (
                                <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-xs text-emerald-700">
                                  {topic.easy} Easy
                                </span>
                              )}
                              {topic.medium > 0 && (
                                <span className="rounded-full bg-amber-50 px-2 py-0.5 text-xs text-amber-700">
                                  {topic.medium} Medium
                                </span>
                              )}
                              {topic.hard > 0 && (
                                <span className="rounded-full bg-rose-50 px-2 py-0.5 text-xs text-rose-700">
                                  {topic.hard} Hard
                                </span>
                              )}
                            </div>

                            {/* Progress bar */}
                            {hasTopicProgress && (
                              <>
                                <div className="h-2 overflow-hidden rounded-full bg-black/5">
                                  <div
                                    className={`h-full rounded-full transition-all ${
                                      percentage >= 100
                                        ? "bg-green-500"
                                        : percentage >= 50
                                        ? "bg-primary-500"
                                        : "bg-primary-400"
                                    }`}
                                    style={{ width: `${percentage}%` }}
                                  />
                                </div>
                                <div className="mt-2 flex items-center justify-between text-xs text-text-muted">
                                  <span>{solved}/{topic.total} solved</span>
                                  {solved > 0 && (
                                    <span className="flex items-center gap-1">
                                      <CheckCircle size={12} className="text-green-500" />
                                      {percentage}%
                                    </span>
                                  )}
                                </div>
                              </>
                            )}
                          </motion.div>
                        </Link>
                      </StaggerItem>
                    );
                  })}
                </StaggerContainer>
              </motion.section>
            );
          })}
        </AnimatePresence>

        {topics.length === 0 && !loading && (
          <div className="card bg-white text-center py-12">
            <BookOpen size={48} className="mx-auto mb-4 text-brand-secondary" />
            <p className="text-text-muted">No topics available yet</p>
            <p className="text-sm text-text-dim">
              Run the seed script to add problems
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
