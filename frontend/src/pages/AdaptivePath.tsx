import { useEffect, useState, useMemo, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link } from "react-router-dom";
import {
  Brain, Target, Compass, TrendingUp, Clock, Zap, Award, BookOpen,
  Code2, Layers, Sparkles, Sword, Shield, ChevronRight, RotateCcw,
  CheckCircle2, AlertCircle, BarChart3, Star, Flame, Trophy, ArrowRight,
  Lightbulb, Play, RefreshCw, ChevronDown, ListOrdered,
} from "lucide-react";
import api from "../services/api";

const MASTERY_COLORS = {
  untouched: "#6B7280",
  beginner: "#EF4444",
  learning: "#F59E0B",
  practicing: "#3B82F6",
  competent: "#10B981",
  proficient: "#06B6D4",
  master: "#8B5CF6",
};

const TASK_EMOJIS = {
  lesson: "📖",
  practice: "✏️",
  problem: "💻",
  challenge: "⚔️",
  project: "🏗️",
  warmup: "🔥",
  advanced_challenge: "🏆",
  video: "🎬",
};

export default function AdaptivePath() {
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [skills, setSkills] = useState(null);
  const [weakAreas, setWeakAreas] = useState([]);
  const [dailyPlan, setDailyPlan] = useState(null);
  const [recommendations, setRecommendations] = useState(null);
  const [readiness, setReadiness] = useState(null);
  const [learningPath, setLearningPath] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedTask, setSelectedTask] = useState(null);

  const fetchAll = useCallback(async (forcePlan = false) => {
    try {
      if (forcePlan) setRefreshing(true);
      else setLoading(true);
      setError(null);

      const [skillsRes, weakRes, planRes, recsRes, readinessRes, pathRes] = await Promise.all([
        api.getSkillAssessment(),
        api.getWeakAreasAdaptive(),
        api.getDailyPlan(forcePlan),
        api.getRecommendations(),
        api.getReadinessScoreAdaptive(),
        api.getLearningPath(),
      ]);

      setSkills(skillsRes.data);
      setWeakAreas(weakRes.data || []);
      setDailyPlan(planRes.data);
      setRecommendations(recsRes.data);
      setReadiness(readinessRes.data);
      setLearningPath(pathRes.data);
    } catch (err) {
      setError(err.message || "Failed to load learning path");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  const handleCompleteTask = useCallback(async (task, index) => {
    try {
      await api.recordAdaptiveActivity({
        domain_id: task.domain_id,
        type: task.type,
        success: true,
        score_impact: task.difficulty === "hard" ? 3 : task.difficulty === "medium" ? 2 : 1,
      });
      await fetchAll(true);
    } catch (err) {
      console.error("Failed to record activity:", err);
    }
  }, [fetchAll]);

  if (loading) return <LoadingSkeleton />;
  if (error) return <ErrorState error={error} onRetry={() => fetchAll()} />;

  return (
    <div className="min-h-screen p-2 sm:p-4 md:p-6 max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-lavender to-brand-sky flex items-center justify-center shadow-lg">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Adaptive Learning Path</h1>
            <p className="text-sm text-gray-500">Personalized just for you based on your skills & progress</p>
          </div>
        </div>
        <button
          onClick={() => fetchAll(true)}
          disabled={refreshing}
          className="flex items-center gap-2 px-4 py-2 rounded-xl bg-surface-card/90 border border-brand-primary/10 text-brand-secondary hover:bg-white hover:text-white transition-all disabled:opacity-50 text-sm"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* Readiness Score Card */}
      {readiness && <ReadinessCard readiness={readiness} />}

      {/* Tab Navigation */}
      <TabNav activeTab={activeTab} onTabChange={setActiveTab} tabs={[
        { id: "overview", label: "Overview", icon: BarChart3 },
        { id: "daily", label: "Daily Plan", icon: Clock },
        { id: "skills", label: "Skills", icon: Brain },
        { id: "path", label: "Learning Path", icon: Layers },
        { id: "recommendations", label: "Recommendations", icon: Lightbulb },
      ]} />

      {activeTab === "overview" && (
        <OverviewTab
          skills={skills}
          weakAreas={weakAreas}
          dailyPlan={dailyPlan}
          readiness={readiness}
          recommendations={recommendations}
        />
      )}

      {activeTab === "daily" && (
        <DailyPlanTab
          plan={dailyPlan}
          onCompleteTask={handleCompleteTask}
          selectedTask={selectedTask}
          onSelectTask={setSelectedTask}
        />
      )}

      {activeTab === "skills" && (
        <SkillsTab skills={skills} weakAreas={weakAreas} />
      )}

      {activeTab === "path" && (
        <LearningPathTab path={learningPath} />
      )}

      {activeTab === "recommendations" && (
        <RecommendationsTab recommendations={recommendations} />
      )}
    </div>
  );
}

function ReadinessCard({ readiness }: any) {
  const levelColors = {
    "Interview Ready": "from-emerald-400 to-green-500",
    "Almost There": "from-blue-400 to-cyan-500",
    "Progressing": "from-amber-400 to-orange-500",
    "Building Foundation": "from-violet-400 to-purple-500",
    "Getting Started": "from-gray-400 to-slate-500",
  };

  const bgColor = Object.entries(levelColors).find(([key]) => readiness.readiness_level.startsWith(key.split(" ")[0]))?.[1] || "from-gray-400 to-slate-500";

  return (
    <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="rounded-2xl bg-gradient-to-r from-white/70 to-white/40 border border-brand-primary/10 p-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-6">
        <div className="relative">
          <svg className="w-24 h-24 sm:w-28 sm:h-28" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="54" fill="none" stroke="#e5e7eb" strokeWidth="8" />
            <motion.circle
              cx="60" cy="60" r="54" fill="none"
              stroke="url(#readinessGradient)"
              strokeWidth="8" strokeLinecap="round"
              strokeDasharray={`${2 * Math.PI * 54}`}
              initial={{ strokeDashoffset: 2 * Math.PI * 54 }}
              animate={{ strokeDashoffset: 2 * Math.PI * 54 * (1 - readiness.overall_readiness / 100) }}
              transition={{ duration: 1.5, ease: "easeOut" }}
              transform="rotate(-90 60 60)"
            />
            <defs>
              <linearGradient id="readinessGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#8B5CF6" />
                <stop offset="100%" stopColor="#3B82F6" />
              </linearGradient>
            </defs>
            <text x="60" y="55" textAnchor="middle" className="text-3xl font-bold fill-gray-800" fontSize="28">{Math.round(readiness.overall_readiness)}</text>
            <text x="60" y="75" textAnchor="middle" className="text-xs fill-gray-500" fontSize="10">READINESS</text>
          </svg>
        </div>
        <div className="flex-1 space-y-2">
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-white">Interview Readiness</h2>
            <span className={`px-3 py-1 rounded-full text-xs font-semibold text-white bg-gradient-to-r ${bgColor}`}>{readiness.readiness_level}</span>
          </div>
          <div className="flex flex-wrap gap-3 text-sm text-brand-secondary">
            <span>🎯 {readiness.coverage_pct}% domain coverage</span>
            <span>💪 {readiness.strong_domains_count} strong domains</span>
            <span>⚠️ {readiness.weak_areas_count} weak areas</span>
          </div>
          {readiness.category_scores && (
            <div className="flex flex-wrap gap-2 mt-2">
              {Object.entries(readiness.category_scores).filter(([, s]: any) => s > 0).map(([cat, score]: [string, any]) => (
                <span key={cat} className="px-2.5 py-1 rounded-lg bg-surface-card/90 border border-brand-primary/10 text-xs font-medium text-brand-primary">
                  {cat.charAt(0).toUpperCase() + cat.slice(1)}: {score}/100
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}

function TabNav({ activeTab, onTabChange, tabs }: any) {
  return (
    <div className="flex gap-1 p-1 rounded-2xl bg-surface-card/70 border border-brand-primary/10 overflow-x-auto">
      {tabs.map((tab) => {
        const Icon = tab.icon;
        return (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all whitespace-nowrap ${
              activeTab === tab.id
                ? "bg-surface-card shadow-lg text-white border border-brand-primary/10"
                : "text-gray-500 hover:text-brand-primary hover:bg-surface-card/70"
            }`}
          >
            <Icon className="w-4 h-4" />
            {tab.label}
          </button>
        );
      })}
    </div>
  );
}

function OverviewTab({ skills, weakAreas, dailyPlan, readiness, recommendations }: any) {
  const topWeak = (weakAreas || []).slice(0, 3);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
      {/* Today's Plan */}
      <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} className="lg:col-span-2 rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-5 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Clock className="w-5 h-5 text-brand-lavender" />
            <h3 className="font-semibold text-white">Today's Plan</h3>
          </div>
          {dailyPlan && (
            <span className="text-xs text-gray-500">{dailyPlan.total_estimated_minutes} min • {dailyPlan.task_count} tasks</span>
          )}
        </div>
        {dailyPlan?.tasks?.slice(0, 3).map((task, i) => (
          <div key={task.id || i} className="flex items-start gap-3 p-3 rounded-xl bg-surface-card/90 border border-gray-100">
            <span className="text-xl">{TASK_EMOJIS[task.type] || "📌"}</span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white">{task.title}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                  task.type === "warmup" ? "bg-amber-100 text-amber-700" :
                  task.difficulty === "easy" ? "bg-green-100 text-green-700" :
                  task.difficulty === "hard" ? "bg-red-100 text-red-700" :
                  "bg-blue-100 text-blue-700"
                }`}>{task.difficulty || task.type}</span>
                <span className="text-xs text-gray-400">{task.estimated_minutes} min</span>
                <span className="text-xs text-brand-gold">+{task.xp_reward} XP</span>
              </div>
            </div>
            <Link to={`/learn`} className="shrink-0 p-2 rounded-lg bg-brand-lavender/10 text-brand-lavender hover:bg-brand-lavender/20 transition-colors">
              <Play className="w-4 h-4" />
            </Link>
          </div>
        ))}
        <Link to="/adaptive" onClick={() => {}} className="flex items-center gap-1 text-sm text-brand-lavender font-medium hover:underline">
          View full plan <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </motion.div>

      {/* Weak Areas + Stats */}
      <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} className="space-y-4">
        {/* Weak Areas */}
        <div className="rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-5 space-y-3">
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-brand-coral" />
            <h3 className="font-semibold text-white">Weak Areas</h3>
          </div>
          {topWeak.length === 0 ? (
            <p className="text-sm text-gray-500">No weak areas detected! Keep it up 🎉</p>
          ) : (
            topWeak.map((area, i) => (
              <div key={area.domain_id || i} className="flex items-center gap-3 p-2.5 rounded-xl bg-white/50 border border-gray-100">
                <span className="text-lg">{area.emoji}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white">{area.name}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    <div className="flex-1 h-1.5 rounded-full bg-gray-200 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }} animate={{ width: `${area.score}%` }}
                        className="h-full rounded-full"
                        style={{ backgroundColor: area.color || MASTERY_COLORS[area.mastery] || "#6B7280" }}
                        transition={{ duration: 1, delay: i * 0.2 }}
                      />
                    </div>
                    <span className="text-xs font-medium text-gray-500">{area.score}%</span>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Quick Stats */}
        {readiness && (
          <div className="rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-5 space-y-3">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-emerald-500" />
              <h3 className="font-semibold text-white">Quick Stats</h3>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {[
                { label: "Overall", value: `${Math.round(skills?.overall_score || 0)}%`, color: "text-brand-lavender" },
                { label: "Accuracy", value: `${Math.round(skills?.overall_accuracy || 0)}%`, color: "text-emerald-500" },
                { label: "Attempts", value: skills?.total_attempts || 0, color: "text-blue-500" },
                { label: "Correct", value: skills?.total_correct || 0, color: "text-green-500" },
              ].map((stat) => (
                <div key={stat.label} className="p-2.5 rounded-xl bg-surface-card/90 border border-gray-100 text-center">
                  <p className={`text-lg font-bold ${stat.color}`}>{stat.value}</p>
                  <p className="text-xs text-gray-500">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </motion.div>
    </div>
  );
}

function DailyPlanTab({ plan, onCompleteTask, selectedTask, onSelectTask }: any) {
  if (!plan) return <EmptyState message="No daily plan yet. Start practicing to generate one!" />;

  return (
    <div className="space-y-4">
      {/* Plan Header */}
      <div className="rounded-2xl bg-gradient-to-r from-brand-lavender/10 to-brand-sky/10 border border-brand-primary/10 p-5">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-white">{plan.date}</h3>
            <p className="text-sm text-gray-500">Streak: {plan.streak} days • Level {plan.level} • {plan.total_estimated_minutes} minutes</p>
          </div>
          <span className="text-xs text-gray-500">{plan.task_count} tasks</span>
        </div>
        {plan.focus_areas?.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-3">
            {plan.focus_areas.map((area, i) => (
              <span key={i} className="flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-medium bg-surface-card/90 border border-brand-primary/10 text-brand-primary">
                {area.emoji} {area.name}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Tasks */}
      <div className="space-y-3">
        {plan.tasks?.map((task, i) => (
          <motion.div
            key={task.id || i}
            initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}
            className="rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-4 hover:bg-white/80 transition-colors cursor-pointer"
            onClick={() => onSelectTask(selectedTask === i ? null : i)}
          >
            <div className="flex items-start gap-4">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-xl ${
                task.type === "warmup" ? "bg-amber-100" :
                task.type === "lesson" ? "bg-blue-100" :
                task.type === "problem" ? "bg-violet-100" :
                task.type === "challenge" ? "bg-red-100" :
                task.type === "project" ? "bg-emerald-100" :
                "bg-surface-card/50"
              }`}>
                {TASK_EMOJIS[task.type] || "📌"}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-medium text-white">{task.title}</p>
                    {task.domain_id && (
                      <p className="text-xs text-gray-500 mt-0.5">{task.domain_id.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}</p>
                    )}
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                      task.difficulty === "easy" ? "bg-green-100 text-green-700" :
                      task.difficulty === "hard" ? "bg-red-100 text-red-700" :
                      "bg-blue-100 text-blue-700"
                    }`}>{task.difficulty}</span>
                  </div>
                </div>
                <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" />{task.estimated_minutes} min</span>
                  <span className="flex items-center gap-1"><Zap className="w-3 h-3 text-brand-gold" />+{task.xp_reward} XP</span>
                </div>
                {selectedTask === i && task.description && (
                  <motion.p initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="mt-2 text-sm text-brand-secondary bg-surface-base rounded-lg p-3">
                    {task.description}
                  </motion.p>
                )}
                {selectedTask === i && task.hint && (
                  <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="mt-2 p-3 rounded-lg bg-amber-50 border border-amber-200">
                    <p className="text-xs font-medium text-amber-800 flex items-center gap-1"><Lightbulb className="w-3 h-3" />Hint</p>
                    <p className="text-sm text-amber-700 mt-1">{task.hint}</p>
                  </motion.div>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function SkillsTab({ skills, weakAreas }: any) {
  if (!skills) return <EmptyState message="No skill data yet. Start practicing!" />;

  const sortedSkills = (Object.entries(skills.skills || {}) as [string, any][]).sort(([, a], [, b]) => b.score - a.score);
  const weakIds = new Set((weakAreas || []).map(w => w.domain_id));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      {/* Skill Bars */}
      <div className="rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-5">
        <h3 className="font-semibold text-white mb-4">All Skills</h3>
        <div className="space-y-3">
          {sortedSkills.map(([id, skill]) => (
            <div key={id} className="space-y-1">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-sm font-medium text-white truncate">{id.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}</span>
                  {weakIds.has(id) && <AlertCircle className="w-3.5 h-3.5 text-brand-coral shrink-0" />}
                </div>
                <span className="text-xs font-medium text-gray-500 shrink-0">{skill.score}% · {skill.mastery_label}</span>
              </div>
              <div className="h-2 rounded-full bg-gray-200 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }} animate={{ width: `${skill.score}%` }}
                  className="h-full rounded-full"
                  style={{ backgroundColor: skill.mastery_color || MASTERY_COLORS[skill.mastery] || "#6B7280" }}
                  transition={{ duration: 1 }}
                />
              </div>
              {skill.next_milestone && (
                <p className="text-xs text-gray-400">{skill.next_milestone.needed.toFixed(1)} pts to {skill.next_milestone.label}</p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Weak Areas Detail */}
      <div className="space-y-4">
        <div className="rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-5">
          <h3 className="font-semibold text-white mb-4">⚠️ Priority Weak Areas</h3>
          {(weakAreas || []).length === 0 ? (
            <p className="text-sm text-gray-500">No weak areas found!</p>
          ) : (
            <div className="space-y-3">
              {weakAreas.map((area, i) => (
                <div key={area.domain_id || i} className="p-3 rounded-xl bg-surface-card/90 border border-gray-100">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{area.emoji}</span>
                    <div>
                      <p className="text-sm font-medium text-white">{area.name}</p>
                      <p className="text-xs text-gray-500">Score: {area.score}% · {area.mastery_label} · {area.accuracy}% accuracy</p>
                    </div>
                  </div>
                  {area.reason && <p className="text-xs text-gray-500 mt-2 ml-8">{area.reason}</p>}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Mastery Legend */}
        <div className="rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-5">
          <h3 className="font-semibold text-white mb-3">Mastery Levels</h3>
          <div className="space-y-1.5">
            {["untouched", "beginner", "learning", "practicing", "competent", "proficient", "master"].map((level) => (
              <div key={level} className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: MASTERY_COLORS[level] }} />
                <span className="text-brand-primary capitalize">{level}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function LearningPathTab({ path }: any) {
  if (!path) return <EmptyState message="Generate skill data first to see your learning path." />;

  return (
    <div className="space-y-4">
      <div className="rounded-2xl bg-gradient-to-r from-brand-lavender/10 to-brand-sky/10 border border-brand-primary/10 p-5">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-white">
              {path.total_weeks}-Week Learning Path
            </h3>
            <p className="text-sm text-gray-500">{path.total_hours} hours total · Current: {path.current_level} ({path.current_score}%)</p>
          </div>
        </div>
      </div>

      <div className="relative">
        {path.weeks?.map((week, i) => (
          <motion.div
            key={week.week}
            initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}
            className="relative pl-8 pb-6 last:pb-0"
          >
            {/* Timeline line */}
            {i < path.weeks.length - 1 && (
              <div className="absolute left-[15px] top-8 bottom-0 w-0.5 bg-gradient-to-b from-brand-lavender/40 to-transparent" />
            )}
            {/* Timeline dot */}
            <div className="absolute left-2 top-1 w-7 h-7 rounded-full bg-white border-2 border-brand-lavender flex items-center justify-center">
              <span className="text-xs font-bold text-brand-lavender">{week.week}</span>
            </div>

            <div className="rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-4 hover:bg-white/80 transition-colors">
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2 min-w-0">
                  <span className="text-lg shrink-0">{week.emoji}</span>
                  <div>
                    <p className="font-semibold text-white">{week.title}</p>
                    <p className="text-xs text-gray-500">{week.goal} · ~{week.estimated_hours}h</p>
                  </div>
                </div>
                <span className={`shrink-0 px-2.5 py-1 rounded-full text-xs font-medium ${
                  week.phase === "Foundation" ? "bg-blue-100 text-blue-700" :
                  week.phase === "Development" ? "bg-violet-100 text-violet-700" :
                  week.phase === "Growth" ? "bg-emerald-100 text-emerald-700" :
                  "bg-amber-100 text-amber-700"
                }`}>{week.phase}</span>
              </div>
              <details className="mt-3">
                <summary className="text-xs text-gray-500 cursor-pointer hover:text-brand-primary">View daily plan</summary>
                <ul className="mt-2 space-y-1">
                  {week.daily_plan?.map((day, di) => (
                    <li key={di} className="flex items-center gap-2 text-xs text-brand-secondary">
                      <CheckCircle2 className="w-3 h-3 text-gray-300" />
                      {day}
                    </li>
                  ))}
                </ul>
              </details>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function RecommendationsTab({ recommendations }: any) {
  if (!recommendations) return <EmptyState message="No recommendations yet." />;

  return (
    <div className="space-y-4">
      {recommendations.career_insight && (
        <div className="rounded-2xl bg-gradient-to-r from-brand-lavender/10 to-brand-sky/10 border border-brand-primary/10 p-5">
          <div className="flex items-start gap-3">
            <Sparkles className="w-5 h-5 text-brand-gold shrink-0 mt-0.5" />
            <div>
              <p className="text-sm text-brand-primary italic">{recommendations.career_insight}</p>
              {recommendations.next_milestone && (
                <p className="text-xs text-gray-500 mt-1">Next milestone: {recommendations.next_milestone}</p>
              )}
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {recommendations.recommendations?.map((rec, i) => (
          <motion.div
            key={i} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
            className="rounded-2xl bg-surface-card/90 border border-brand-primary/10 p-5 hover:bg-white/80 transition-colors"
          >
            <div className="flex items-start gap-3">
              <div className={`w-10 h-10 rounded-xl flex items-center justify-center text-lg ${
                rec.impact === "high" ? "bg-red-100" : rec.impact === "medium" ? "bg-amber-100" : "bg-blue-100"
              }`}>
                {rec.type === "practice" ? "✏️" : rec.type === "learn" ? "📖" : rec.type === "build" ? "🏗️" : "📌"}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-2">
                  <p className="font-semibold text-white">{rec.title}</p>
                  <span className={`shrink-0 px-2 py-0.5 rounded-full text-xs font-medium ${
                    rec.impact === "high" ? "bg-red-100 text-red-700" :
                    rec.impact === "medium" ? "bg-amber-100 text-amber-700" :
                    "bg-blue-100 text-blue-700"
                  }`}>{rec.impact}</span>
                </div>
                <p className="text-sm text-brand-secondary mt-1">{rec.description}</p>
                {rec.concrete_action && (
                  <div className="mt-2 p-2.5 rounded-lg bg-surface-base border border-gray-100">
                    <p className="text-xs font-medium text-brand-primary">Action:</p>
                    <p className="text-sm text-brand-secondary">{rec.concrete_action}</p>
                  </div>
                )}
                {rec.estimated_hours && (
                  <p className="text-xs text-gray-400 mt-2">Estimated: {rec.estimated_hours}h</p>
                )}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

function LoadingSkeleton() {
  return (
    <div className="min-h-screen p-6 max-w-7xl mx-auto space-y-6">
      <div className="animate-pulse space-y-4">
        <div className="h-12 bg-gray-200 rounded-2xl w-1/3" />
        <div className="h-32 bg-gray-200 rounded-2xl" />
        <div className="grid grid-cols-3 gap-4">
          <div className="h-64 bg-gray-200 rounded-2xl" />
          <div className="h-64 bg-gray-200 rounded-2xl" />
          <div className="h-64 bg-gray-200 rounded-2xl" />
        </div>
      </div>
    </div>
  );
}

function ErrorState({ error, onRetry }: any) {
  return (
    <div className="min-h-screen p-6 max-w-7xl mx-auto">
      <div className="rounded-2xl bg-red-50 border border-red-200 p-8 text-center">
        <AlertCircle className="w-12 h-12 text-red-400 mx-auto mb-4" />
        <h3 className="text-lg font-semibold text-red-800 mb-2">Failed to load</h3>
        <p className="text-sm text-red-600 mb-4">{error}</p>
        <button onClick={onRetry} className="px-4 py-2 rounded-xl bg-red-600 text-white text-sm font-medium hover:bg-red-700 transition-colors">
          Try Again
        </button>
      </div>
    </div>
  );
}

function EmptyState({ message }: any) {
  return (
    <div className="rounded-2xl bg-surface-card/70 border border-brand-primary/10 p-8 text-center">
      <Compass className="w-12 h-12 text-gray-300 mx-auto mb-4" />
      <p className="text-gray-500">{message}</p>
    </div>
  );
}
