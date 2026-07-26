import { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import ActivityHeatmap from "../components/ActivityHeatmap";
import CelebrationOverlay from "../components/CelebrationOverlay";
import {
  Flame, Trophy, Target, TrendingUp, Zap, Award, BookOpen,
  Code2, Brain, FileText, BarChart3, Clock, ChevronRight,
  CheckCircle, Star, Calendar, Rocket, Shield, Crown, Gem,
  Hash, Medal, Percent, Building2
} from "lucide-react";

const BADGE_ICONS = {
  interview: <Target size={16} />,
  resume: <FileText size={16} />,
  aptitude: <Brain size={16} />,
  coding: <Code2 size={16} />,
  streak: <Flame size={16} />,
  company: <Trophy size={16} />,
  system_design: <BarChart3 size={16} />,
};

const BADGE_COLORS = {
  interview: "from-blue-500 to-cyan-500",
  resume: "from-green-500 to-emerald-500",
  aptitude: "from-purple-500 to-pink-500",
  coding: "from-orange-500 to-red-500",
  streak: "from-yellow-500 to-amber-500",
  company: "from-indigo-500 to-blue-500",
  system_design: "from-teal-500 to-cyan-500",
};

const LEVEL_TITLES = [
  { min: 1, title: "Newcomer", icon: <Hash size={14} /> },
  { min: 3, title: "Beginner", icon: <BookOpen size={14} /> },
  { min: 5, title: "Apprentice", icon: <Target size={14} /> },
  { min: 8, title: "Practitioner", icon: <Shield size={14} /> },
  { min: 12, title: "Expert", icon: <Trophy size={14} /> },
  { min: 16, title: "Master", icon: <Crown size={14} /> },
  { min: 20, title: "Grandmaster", icon: <Gem size={14} /> },
  { min: 25, title: "Legend", icon: <Rocket size={14} /> },
];

function getLevelTitle(level) {
  for (let i = LEVEL_TITLES.length - 1; i >= 0; i--) {
    if (level >= LEVEL_TITLES[i].min) return LEVEL_TITLES[i];
  }
  return LEVEL_TITLES[0];
}

const cardCls = "bg-gray-900/40 border border-gray-700/30 rounded-xl p-4 sm:p-5";

export default function PersonalDashboard() {
  const { user } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState(null);
  const [heatmap, setHeatmap] = useState(null);
  const [streak, setStreak] = useState(null);
  const [topicProgress, setTopicProgress] = useState([]);
  const [dailyGoal, setDailyGoal] = useState(null);
  const [weeklyGoal, setWeeklyGoal] = useState(null);
  const [gamProfile, setGamProfile] = useState(null);
  const [badges, setBadges] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [showAllBadges, setShowAllBadges] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);

  useEffect(() => {
    loadAll();
  }, []);

  const loadAll = async () => {
    setLoading(true);
    try {
      const results = await Promise.allSettled([
        api.getProgressOverview(),
        api.getHeatmap(365),
        api.getStreak(),
        api.getTopicProgress(),
        api.getDailyGoal(),
        api.getWeeklyGoal(),
        api.getGamificationProfile(),
        api.getAllBadges(),
        api.getLeaderboard(10),
      ]);

      if (results[0].status === "fulfilled") setOverview(results[0].value);
      if (results[1].status === "fulfilled") setHeatmap(results[1].value);
      if (results[2].status === "fulfilled") setStreak(results[2].value);
      if (results[3].status === "fulfilled") setTopicProgress(results[3].value?.topics || []);
      if (results[4].status === "fulfilled") setDailyGoal(results[4].value);
      if (results[5].status === "fulfilled") setWeeklyGoal(results[5].value);
      if (results[6].status === "fulfilled") setGamProfile(results[6].value);
      if (results[7].status === "fulfilled") setBadges(results[7].value?.badges || []);
      if (results[8].status === "fulfilled") setLeaderboard(results[8].value || []);
    } catch {} finally {
      setLoading(false);
    }
  };

  const levelTitle = getLevelTitle(gamProfile?.level || 1);
  const earnedBadges = gamProfile?.badges || [];
  const totalBadges = badges.length || 20;
  const earnedBadgeCount = earnedBadges.length;
  const allEarnedBadges = badges.filter(b => earnedBadges.includes(b.id));

  const topTopics = useMemo(() => {
    return [...topicProgress].sort((a, b) => b.percentage - a.percentage).slice(0, 5);
  }, [topicProgress]);

  const weakTopics = useMemo(() => {
    return [...topicProgress].sort((a, b) => a.percentage - b.percentage).filter(t => t.percentage < 60).slice(0, 3);
  }, [topicProgress]);

  if (loading) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-6xl mx-auto space-y-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-32 bg-gray-800/40 rounded-xl animate-pulse border border-gray-700/20" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-4 sm:space-y-6">
        <CelebrationOverlay show={showCelebration} type="levelup" message="Level Up!" onClose={() => setShowCelebration(false)} />

        {/* Header */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between">
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-white">Your Dashboard</h1>
            <p className="text-xs sm:text-sm text-gray-500">Track your progress and achievements</p>
          </div>
          <div className="text-right">
            <span className="text-[10px] text-gray-500 font-mono hidden sm:block">Welcome back,</span>
            <span className="text-xs sm:text-sm font-medium text-white">{user?.name || user?.email || "Coder"}</span>
          </div>
        </motion.div>

        {/* Level Card */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}
          className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl p-4 sm:p-6 text-white relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDM0djItSDJ2LTJoMzRtMC00SDJ2MmgzNHptMC00SDJ2MmgzNHptMC00SDJ2MmgzNHoiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-30" />
          <div className="relative flex items-center justify-between">
            <div className="flex items-center gap-3 sm:gap-4">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-white/20 rounded-2xl flex items-center justify-center backdrop-blur-sm shrink-0">
                <span className="text-xl sm:text-2xl font-bold">{gamProfile?.level || 1}</span>
              </div>
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <span className="text-base sm:text-lg font-bold truncate">{levelTitle.title}</span>
                  <span className="text-white/60 shrink-0">{levelTitle.icon}</span>
                </div>
                <div className="text-xs sm:text-sm text-white/70 mt-0.5">
                  {gamProfile?.xp || 0} XP
                </div>
                <div className="w-32 sm:w-48 h-1.5 bg-white/20 rounded-full mt-2 overflow-hidden">
                  <div
                    className="h-full bg-white rounded-full transition-all duration-500"
                    style={{ width: `${Math.min(100, ((gamProfile?.xp || 0) % ((gamProfile?.level || 1) ** 2 * 100)) / ((gamProfile?.level || 1) ** 2 * 100) * 100)}%` }}
                  />
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3 sm:gap-6 text-center shrink-0">
              <div>
                <div className="text-lg sm:text-2xl font-bold flex items-center gap-1"><Flame size={18} />{streak?.current_streak || 0}</div>
                <div className="text-[10px] sm:text-xs text-white/60">Streak</div>
              </div>
              <div>
                <div className="text-lg sm:text-2xl font-bold">{overview?.total_solved || 0}</div>
                <div className="text-[10px] sm:text-xs text-white/60">Solved</div>
              </div>
              <div>
                <div className="text-lg sm:text-2xl font-bold">{earnedBadgeCount}/{totalBadges}</div>
                <div className="text-[10px] sm:text-xs text-white/60">Badges</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Daily + Weekly Goals */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
            className={cardCls}
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-semibold text-gray-300 flex items-center gap-2">
                <Target size={14} /> Daily Goal
              </span>
              <span className="text-xs text-gray-500 font-mono">{dailyGoal?.solved_today || 0}/{dailyGoal?.daily_goal || 2}</span>
            </div>
            <div className="h-2.5 bg-gray-800 rounded-full overflow-hidden">
              <div className={`h-full rounded-full transition-all duration-500 ${dailyGoal?.goal_met ? "bg-green-500" : "bg-blue-500"}`}
                style={{ width: `${Math.min(100, dailyGoal?.percentage || 0)}%` }} />
            </div>
            {dailyGoal?.goal_met && (
              <div className="flex items-center gap-1 mt-2 text-xs text-green-400">
                <CheckCircle size={12} /> Goal met! Great job.
              </div>
            )}
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}
            className={cardCls}
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-semibold text-gray-300 flex items-center gap-2">
                <Calendar size={14} /> Weekly Goal
              </span>
              <span className="text-xs text-gray-500 font-mono">{weeklyGoal?.solved_this_week || 0}/{weeklyGoal?.weekly_goal || 7}</span>
            </div>
            <div className="h-2.5 bg-gray-800 rounded-full overflow-hidden">
              <div className={`h-full rounded-full transition-all duration-500 ${weeklyGoal?.goal_met ? "bg-green-500" : "bg-yellow-500"}`}
                style={{ width: `${Math.min(100, weeklyGoal?.percentage || 0)}%` }} />
            </div>
            {weeklyGoal?.goal_met && (
              <div className="flex items-center gap-1 mt-2 text-xs text-green-400">
                <CheckCircle size={12} /> Weekly goal crushed!
              </div>
            )}
          </motion.div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
          {[
            { label: "Solved", value: overview?.total_solved || 0, icon: <CheckCircle size={18} />, color: "text-green-400", bg: "bg-green-500/10" },
            { label: "Acceptance", value: `${overview?.acceptance_rate || 0}%`, icon: <Percent size={18} />, color: "text-blue-400", bg: "bg-blue-500/10" },
            { label: "Submissions", value: overview?.total_submissions || 0, icon: <Code2 size={18} />, color: "text-purple-400", bg: "bg-purple-500/10" },
            { label: "Streak", value: `${streak?.current_streak || 0}d`, icon: <Flame size={18} />, color: "text-orange-400", bg: "bg-orange-500/10" },
          ].map((stat, i) => (
            <motion.div key={stat.label} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 + i * 0.05 }}
              className={`${cardCls} text-center`}
            >
              <div className={`inline-flex p-2 rounded-lg ${stat.bg} ${stat.color} mb-2`}>{stat.icon}</div>
              <div className="text-lg sm:text-xl font-bold text-white">{stat.value}</div>
              <div className="text-[10px] text-gray-500 uppercase tracking-wide">{stat.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Difficulty Breakdown */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
          className={cardCls}
        >
          <h2 className="text-sm font-semibold text-gray-300 mb-4">Difficulty Breakdown</h2>
          <div className="grid grid-cols-3 gap-3 sm:gap-4">
            {[
              { key: "easy", label: "Easy", color: "text-green-400", bg: "bg-green-500/15" },
              { key: "medium", label: "Medium", color: "text-yellow-400", bg: "bg-yellow-500/15" },
              { key: "hard", label: "Hard", color: "text-red-400", bg: "bg-red-500/15" },
            ].map((d) => {
              const solved = overview?.difficulty_breakdown?.[d.key] || 0;
              return (
                <div key={d.key} className={`rounded-xl p-3 sm:p-4 ${d.bg}`}>
                  <div className="text-center">
                    <div className={`text-xl sm:text-2xl font-bold ${d.color}`}>{solved}</div>
                    <div className="text-[10px] text-gray-400 uppercase tracking-wide">{d.label}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* Heatmap */}
        {heatmap && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}
            className={`${cardCls} overflow-x-auto`}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-gray-300 flex items-center gap-2">
                <BarChart3 size={14} /> Activity Heatmap
              </h2>
              <div className="flex items-center gap-2 text-[10px] text-gray-500">
                <span>{heatmap.active_days} active days</span>
                <div className="hidden sm:flex items-center gap-1">
                  <span>Less</span>
                  {[0, 1, 2, 3, 4].map(l => (
                    <div key={l} className={`w-2.5 h-2.5 rounded-sm ${
                      l === 0 ? "bg-gray-700" :
                      l === 1 ? "bg-green-900" :
                      l === 2 ? "bg-green-700" :
                      l === 3 ? "bg-green-500" :
                      "bg-green-300"
                    }`} />
                  ))}
                  <span>More</span>
                </div>
              </div>
            </div>
            <ActivityHeatmap data={heatmap.heatmap} />
          </motion.div>
        )}

        {/* Badges */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
          className={cardCls}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-300 flex items-center gap-2">
              <Award size={14} /> Badges ({earnedBadgeCount}/{totalBadges})
            </h2>
            <button onClick={() => setShowAllBadges(!showAllBadges)} className="text-xs text-cyber-blue hover:text-cyber-blue/80">
              {showAllBadges ? "Show Less" : "View All"}
            </button>
          </div>

          {allEarnedBadges.length === 0 ? (
            <div className="text-center py-6 text-gray-500">
              <Award size={32} className="mx-auto mb-2 opacity-50" />
              <p className="text-xs">Complete activities to earn badges!</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 sm:gap-3">
              {(showAllBadges ? allEarnedBadges : allEarnedBadges.slice(0, 10)).map((badge, i) => (
                <motion.div
                  key={badge.id || i}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: i * 0.03 }}
                  className="relative p-3 rounded-xl border text-center group cursor-default bg-gray-800/40 border-gray-700/30"
                >
                  <div className="text-2xl mb-1">{badge.icon}</div>
                  <div className="text-[10px] font-medium text-gray-300">{badge.name}</div>
                  <div className="text-[9px] text-gray-500 mt-0.5">{badge.description}</div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>

        {/* Topic Progress */}
        {topTopics.length > 0 && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }}
            className={cardCls}
          >
            <h2 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
              <BookOpen size={14} /> Topic Progress
            </h2>
            <div className="space-y-3">
              {topTopics.map((t, i) => (
                <div key={t.topic || i} className="flex items-center gap-3">
                  <div className="w-24 sm:w-32 text-xs text-gray-400 truncate shrink-0">{t.topic}</div>
                  <div className="flex-1 h-2 bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        t.percentage >= 80 ? "bg-green-500" :
                        t.percentage >= 50 ? "bg-yellow-500" : "bg-red-500"
                      }`}
                      style={{ width: `${t.percentage}%` }}
                    />
                  </div>
                  <div className="w-16 text-right text-[10px] text-gray-500 shrink-0">
                    {t.solved}/{t.total} <span className="text-gray-600">({t.percentage}%)</span>
                  </div>
                </div>
              ))}
            </div>

            {weakTopics.length > 0 && (
              <div className="mt-4 pt-4 border-t border-gray-700/30">
                <h3 className="text-xs font-medium text-red-400 mb-2 flex items-center gap-1">
                  <TrendingUp size={12} /> Weak Areas — Practice These
                </h3>
                <div className="flex flex-wrap gap-2">
                  {weakTopics.map((t, i) => (
                    <Link key={i} to={`/question-bank?topic=${encodeURIComponent(t.topic)}`}
                      className="px-3 py-1.5 bg-red-500/10 border border-red-500/20 rounded-full text-xs text-red-400 hover:bg-red-500/20 transition-colors"
                    >
                      {t.topic} ({t.percentage}%)
                    </Link>
                  ))}
                </div>
              </div>
            )}
          </motion.div>
        )}

        {/* Leaderboard */}
        {leaderboard.length > 0 && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}
            className={cardCls}
          >
            <h2 className="text-sm font-semibold text-gray-300 mb-4 flex items-center gap-2">
              <Trophy size={14} /> Leaderboard
            </h2>
            <div className="space-y-2">
              {leaderboard.slice(0, 5).map((entry, i) => {
                const isMe = entry.user_id === user?.id;
                return (
                  <div key={i} className={`flex items-center gap-3 p-2.5 rounded-lg ${isMe ? "bg-cyber-blue/10 border border-cyber-blue/20" : "hover:bg-gray-800/40"}`}>
                    <div className={`w-6 text-center text-xs font-bold ${i === 0 ? "text-yellow-400" : i === 1 ? "text-gray-400" : i === 2 ? "text-amber-500" : "text-gray-500"}`}>
                      {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${i + 1}`}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-xs font-medium text-white truncate">{isMe ? "You" : `User ${entry.user_id?.slice(-4)}`}</div>
                      <div className="text-[10px] text-gray-500">Level {entry.level} · {entry.streak}d streak</div>
                    </div>
                    <div className="text-right shrink-0">
                      <div className="text-xs font-bold text-cyber-blue">{entry.xp} XP</div>
                      <div className="text-[10px] text-gray-500">{entry.badges_count} badges</div>
                    </div>
                  </div>
                );
              })}
            </div>
            <Link to="/leaderboard" className="block text-center text-xs text-cyber-blue hover:text-cyber-blue/80 mt-3">
              View Full Leaderboard →
            </Link>
          </motion.div>
        )}

        {/* Quick Links */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.55 }}
          className="grid grid-cols-2 sm:grid-cols-3 gap-3"
        >
          {[
            { to: "/question-bank", label: "Practice", icon: <Code2 size={18} />, color: "from-blue-500 to-cyan-500" },
            { to: "/interview", label: "Interview", icon: <Target size={18} />, color: "from-green-500 to-emerald-500" },
            { to: "/indian-placement", label: "Placement Prep", icon: <Building2 size={18} />, color: "from-orange-500 to-red-500" },
            { to: "/cards", label: "Cards", icon: <Gem size={18} />, color: "from-purple-500 to-pink-500" },
            { to: "/leaderboard", label: "Leaderboard", icon: <Trophy size={18} />, color: "from-yellow-500 to-amber-500" },
            { to: "/company-prep", label: "Company Prep", icon: <Building2 size={18} />, color: "from-indigo-500 to-blue-500" },
          ].map((link, i) => (
            <Link key={i} to={link.to}
              className="group p-4 bg-gray-900/40 border border-gray-700/30 rounded-xl hover:border-gray-600/40 hover:bg-gray-800/40 transition-all"
            >
              <div className={`inline-flex p-2 rounded-lg bg-gradient-to-br ${link.color} text-white mb-2 group-hover:scale-110 transition-transform`}>
                {link.icon}
              </div>
              <div className="text-sm font-medium text-white">{link.label}</div>
            </Link>
          ))}
        </motion.div>
      </div>
    </div>
  );
}
