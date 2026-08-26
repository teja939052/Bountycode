import { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import ActivityHeatmap from "../components/ActivityHeatmap";
import PredictorGauge from "../components/PredictorGauge";
import CelebrationOverlay from "../components/CelebrationOverlay";
import StreakFreezeModal from "../components/StreakFreezeModal";
import {
  Flame, Trophy, Target, TrendingUp, Zap, Award, BookOpen,
  Code2, Brain, FileText, BarChart3, ChevronRight,
  CheckCircle, Star, Calendar, Rocket, Shield, Crown, Gem,
  Hash, Percent, Building2, Sparkles, Layers, Sword,
  Users, Coins, Timer, Activity, ArrowRight,
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

const cardCls = "bg-white border-border/90 border border-black/10 rounded-xl p-4 sm:p-5 shadow-sm";

function humanize(str) {
  return (str || "")
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function formatDate(iso) {
  if (!iso) return "";
  try {
    const d = new Date(iso);
    if (isNaN(d.getTime())) return "";
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
  } catch {
    return "";
  }
}

function mapAction(action) {
  if (!action) return "/question-bank";
  const m = action.match(/^\/problems\/(.+)$/);
  if (m) return `/question-bank?topic=${encodeURIComponent(m[1])}`;
  return action;
}

function Bar({ value = 0, color = "bg-cyber-blue" }) {
  return (
    <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
      <div
        className={`h-full rounded-full transition-all duration-500 ${color}`}
        style={{ width: `${Math.min(100, Math.max(0, value || 0))}%` }}
      />
    </div>
  );
}

function SectionHeader({ icon, title, subtitle, action }: { icon?: React.ReactNode; title?: React.ReactNode; subtitle?: React.ReactNode; action?: React.ReactNode }) {
  return (
    <div className="flex items-center justify-between mb-4">
      <div className="min-w-0">
        <h2 className="text-sm font-semibold text-gray-300 flex items-center gap-2">
          {icon} {title}
        </h2>
        {subtitle && <p className="text-[10px] text-gray-500 mt-0.5">{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

function DiffChip({ difficulty }) {
  const map = {
    easy: "bg-green-500/10 text-green-400 border-green-500/20",
    medium: "bg-yellow-500/10 text-yellow-400 border-yellow-500/20",
    hard: "bg-red-500/10 text-red-400 border-red-500/20",
  };
  return (
    <span className={`px-2 py-0.5 rounded-full text-[10px] border ${map[difficulty] || "bg-gray-700/40 text-gray-400 border-gray-600/30"}`}>
      {difficulty || "unknown"}
    </span>
  );
}

export default function PersonalDashboard() {
  const { user } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [showAllBadges, setShowAllBadges] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const [freezeOpen, setFreezeOpen] = useState(false);

  // Core progress
  const [overview, setOverview] = useState(null);
  const [heatmap, setHeatmap] = useState(null);
  const [streak, setStreak] = useState(null);
  const [topicProgress, setTopicProgress] = useState([]);
  const [dailyGoalProgress, setDailyGoalProgress] = useState(null);
  const [weeklyGoal, setWeeklyGoal] = useState(null);

  // Gamification
  const [gamProfile, setGamProfile] = useState(null);
  const [startup, setStartup] = useState(null);
  const [league, setLeague] = useState(null);
  const [badges, setBadges] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [skillGraph, setSkillGraph] = useState(null);
  const [weakSkills, setWeakSkills] = useState([]);
  const [gamReadiness, setGamReadiness] = useState(null);

  // Profile / career
  const [profileStats, setProfileStats] = useState(null);
  const [profileReadiness, setProfileReadiness] = useState(null);
  const [companyMatches, setCompanyMatches] = useState(null);

  // Slower endpoints (loaded in phase 2)
  const [tower, setTower] = useState(null);
  const [plan, setPlan] = useState(null);
  const [pd, setPd] = useState(null);
  const [analyticsOverview, setAnalyticsOverview] = useState(null);

  useEffect(() => {
    loadAll();
  }, []);

  const loadAll = async () => {
    setLoading(true);
    try {
      // Phase 1 — fast endpoints so the page renders instantly
      const fast = await Promise.allSettled([
        api.getProgressOverview(),
        api.getHeatmap(),
        api.getStreak(),
        api.getTopicProgress(),
        api.getWeeklyGoal(),
        api.get("/api/v1/progress/daily-goal"),
        api.gamification.getProfile(),
        api.gamification.getAllBadges(),
        api.gamification.getLeaderboard(10),
        api.gamification.getStartupState(),
        api.gamification.getLeague(),
        api.gamification.getSkillGraph(),
        api.gamification.getWeakAreas(5),
        api.gamification.getReadinessScore(),
        api.getProfileStats(),
        api.get("/api/v1/profile/readiness-score"),
      ]);

      if (fast[0]?.status === "fulfilled") setOverview(fast[0].value);
      if (fast[1]?.status === "fulfilled") setHeatmap(fast[1].value);
      if (fast[2]?.status === "fulfilled") setStreak(fast[2].value);
      if (fast[3]?.status === "fulfilled") setTopicProgress(fast[3].value?.topics || []);
      if (fast[4]?.status === "fulfilled") setWeeklyGoal(fast[4].value);
      if (fast[5]?.status === "fulfilled") setDailyGoalProgress(fast[5].value);
      if (fast[6]?.status === "fulfilled") setGamProfile(fast[6].value);
      if (fast[7]?.status === "fulfilled") setBadges(fast[7].value?.badges || []);
      if (fast[8]?.status === "fulfilled") setLeaderboard(fast[8].value || []);
      if (fast[9]?.status === "fulfilled") setStartup(fast[9].value);
      if (fast[10]?.status === "fulfilled") setLeague(fast[10].value);
      if (fast[11]?.status === "fulfilled") setSkillGraph(fast[11].value);
      if (fast[12]?.status === "fulfilled") setWeakSkills(fast[12].value || []);
      if (fast[13]?.status === "fulfilled") setGamReadiness(fast[13].value);
      if (fast[14]?.status === "fulfilled") setProfileStats(fast[14].value);
      if (fast[15]?.status === "fulfilled") setProfileReadiness(fast[15].value);
    } catch {} finally {
      setLoading(false);
    }

    // Phase 2 — heavier aggregations; populate as they arrive
    try {
      const slow = await Promise.allSettled([
        api.gamification.getTower(),
        api.adaptive.getDailyPlan(),
        api.personalDashboard.get(),
        api.analytics.getOverview(),
        api.get("/api/v1/profile/company-matches"),
      ]);
      if (slow[0]?.status === "fulfilled") setTower(slow[0].value);
      if (slow[1]?.status === "fulfilled") setPlan(slow[1].value);
      if (slow[2]?.status === "fulfilled") setPd(slow[2].value);
      if (slow[3]?.status === "fulfilled") setAnalyticsOverview(slow[3].value);
      if (slow[4]?.status === "fulfilled") setCompanyMatches(slow[4].value);
    } catch {}
  };

  // ─── Derived values ───
  const firstName = user?.name?.split(" ")[0] || user?.email?.split("@")[0] || "Coder";
  const planBadge = profileStats?.plan || user?.plan || "free";

  const level = gamProfile?.level ?? startup?.level ?? profileStats?.level ?? 1;
  const xp = gamProfile?.xp ?? startup?.xp ?? profileStats?.xp ?? 0;
  const titleEmoji = startup?.title_emoji || gamProfile?.title_emoji || getLevelTitle(level).icon;
  const title = startup?.title || gamProfile?.title || getLevelTitle(level).title;
  const xpBase = gamProfile?.xp_for_current_level || 0;
  const xpSpan = gamProfile?.xp_to_next_level || 100;
  const xpPct = Math.min(100, Math.max(0, ((xp - xpBase) / Math.max(xpSpan, 1)) * 100));

  const curStreak = gamProfile?.streak ?? startup?.streak ?? streak?.current_streak ?? 0;
  const longestStreak = gamProfile?.longest_streak ?? startup?.longest_streak ?? streak?.longest_streak ?? 0;
  const coins = gamProfile?.coins ?? tower?.coins ?? 0;
  const stars = gamProfile?.stars_total ?? tower?.stars_total ?? 0;
  const streakFreezes = gamProfile?.streak_freezes ?? startup?.streak_freezes ?? 0;

  const earnedBadgeIds = useMemo(() => {
    const raw = gamProfile?.badges || [];
    return raw.filter((b) => typeof b === "string");
  }, [gamProfile]);
  const earnedBadgeDetails = gamProfile?.badges_details || [];
  const earnedBadgeCount = earnedBadgeDetails.length || earnedBadgeIds.length;
  const totalBadges = badges.length || 20;

  const readinessScore = useMemo(() => {
    const s = profileReadiness?.score ?? Math.round((gamReadiness?.overall ?? 0) * 10);
    if (s) return Math.min(100, Math.max(0, s));
    return pd?.readiness_score ?? 0;
  }, [profileReadiness, gamReadiness, pd]);

  const skillList = useMemo(() => {
    const src = profileStats?.skills || analyticsOverview?.skill_categories || skillGraph?.categories || {};
    return Object.entries(src)
      .map(([key, v]) => {
        const meta = (v && typeof v === "object" ? v : null) as { score?: number; name?: string } | null;
        const score = meta?.score ?? (typeof v === "number" ? v : 0);
        return { key, name: (meta?.name || humanize(key)), score: Math.round(score * 10) / 10 };
      })
      .sort((a, b) => b.score - a.score);
  }, [profileStats, analyticsOverview, skillGraph]);

  const topTopics = useMemo(() => {
    return [...topicProgress].sort((a, b) => b.percentage - a.percentage).slice(0, 5);
  }, [topicProgress]);

  const weakTopics = useMemo(() => {
    return [...topicProgress].sort((a, b) => a.percentage - b.percentage).filter((t) => t.percentage < 60).slice(0, 3);
  }, [topicProgress]);

  const planData = plan?.data || null;
  const planTasks = planData?.tasks || [];
  const planFocus = planData?.focus_areas || [];

  const pdRecs = pd?.recommendations || [];
  const pdActivity = pd?.recent_activity || [];
  const weakAreasPd = pd?.weak_areas || [];

  const readinessRecs = gamReadiness?.recommendations || [];

  const leaderTier = league?.tier || (startup?.league && startup.league.tier) || null;
  const leaderRank = league?.rank || (startup?.league && startup.league.rank) || null;
  const leaderOf = league?.of || (startup?.league && startup.league.of) || null;
  const weeklyXp = league?.weekly_xp ?? (startup?.league && startup.league.weekly_xp) ?? 0;

  const dailyGoalCount = dailyGoalProgress?.solved_today ?? gamProfile?.daily_goal_count ?? 0;
  const dailyGoalTarget = dailyGoalProgress?.daily_goal ?? gamProfile?.daily_goal_target ?? 2;
  const dailyGoalPct = dailyGoalProgress?.percentage ?? Math.min(100, (dailyGoalCount / Math.max(dailyGoalTarget, 1)) * 100);
  const dailyGoalMet = dailyGoalProgress?.goal_met || gamProfile?.daily_goal_completed || dailyGoalCount >= dailyGoalTarget;

  const towerBossLevel = tower?.boss_level ?? gamProfile?.boss_level ?? null;
  const bossesDefeated = tower?.bosses_defeated || [];
  const nextBossLevel = ((Math.floor(level / 10) + 1) * 10) <= 100 ? ((Math.floor(level / 10) + 1) * 10) : null;
  const hasBossAvailable = towerBossLevel && !bossesDefeated.includes(towerBossLevel);

  if (loading) {
    return (
      <div className="page-surface min-h-screen py-12 px-4">
        <div className="max-w-6xl mx-auto space-y-4">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="h-32 bg-white border-border/80 rounded-xl animate-pulse border border-black/5 shadow-sm" />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="page-surface min-h-screen py-6 sm:py-8 px-4">
      <div className="max-w-6xl mx-auto space-y-4 sm:space-y-6">
        <CelebrationOverlay show={showCelebration} type="levelup" message="Level Up!" onClose={() => setShowCelebration(false)} />
        <StreakFreezeModal open={freezeOpen} onClose={() => setFreezeOpen(false)} />

        {/* ── Header ── */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between">
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-text-primary">Command Center</h1>
            <p className="text-xs sm:text-sm text-brand-muted">Your progress, plan, and power-ups in one place</p>
          </div>
          <div className="text-right">
            <span className="text-[10px] text-brand-muted font-mono hidden sm:block">Welcome back,</span>
            <span className="text-xs sm:text-sm font-medium text-text-primary capitalize">{firstName}</span>
            <span className={`ml-2 inline-block px-2 py-0.5 rounded-full text-[10px] font-medium capitalize ${
              planBadge === "pro" || planBadge === "lifetime"
                ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                : "bg-surface-2 text-brand-secondary border border-black/10"
            }`}>
              {planBadge}
            </span>
          </div>
        </motion.div>

        {/* ── Hero Level Card ── */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}
          className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 rounded-2xl p-4 sm:p-6 text-text-primary relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSI+PHBhdGggZD0iTTM2IDM0djItSDJ2LTJoMzRtMC00SDJ2MmgzNHptMC00SDJ2MmgzNHptMC00SDJ2MmgzNHoiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-30" />
          <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center gap-3 sm:gap-4">
              <div className="w-12 h-12 sm:w-16 sm:h-16 bg-white border-border/20 rounded-2xl flex items-center justify-center shrink-0">
                <span className="text-xl sm:text-2xl font-bold">{level}</span>
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-lg sm:text-xl">{titleEmoji}</span>
                  <span className="text-base sm:text-lg font-bold truncate">{title}</span>
                </div>
                <div className="text-xs sm:text-sm text-text-primary/70 mt-0.5">
                  {xp.toLocaleString()} XP · {xpSpan > 0 ? `${xpSpan.toLocaleString()} XP to Level ${level + 1}` : "Max level"}
                </div>
                <div className="w-32 sm:w-48 h-1.5 bg-white border-border/20 rounded-full mt-2 overflow-hidden">
                  <div className="h-full bg-white rounded-full transition-all duration-500" style={{ width: `${xpPct}%` }} />
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3 sm:gap-5 text-center shrink-0 flex-wrap">
              <div>
                <div className="text-lg sm:text-2xl font-bold flex items-center gap-1"><Flame size={18} />{curStreak}</div>
                <div className="text-[10px] sm:text-xs text-text-primary/60">Streak</div>
              </div>
              <div>
                <div className="text-lg sm:text-2xl font-bold flex items-center gap-1"><Coins size={16} />{coins}</div>
                <div className="text-[10px] sm:text-xs text-text-primary/60">Coins</div>
              </div>
              <div>
                <div className="text-lg sm:text-2xl font-bold flex items-center gap-1"><Star size={16} />{stars}</div>
                <div className="text-[10px] sm:text-xs text-text-primary/60">Stars</div>
              </div>
              <div>
                <div className="text-lg sm:text-2xl font-bold flex items-center gap-1"><SnowIcon />{streakFreezes}</div>
                <div className="text-[10px] sm:text-xs text-text-primary/60">Freezes</div>
              </div>
            </div>
          </div>
          {streakFreezes > 0 && (
            <button onClick={() => setFreezeOpen(true)} className="relative mt-3 text-[10px] sm:text-xs underline underline-offset-2 opacity-80 hover:opacity-100">
              Manage streak freeze →
            </button>
          )}
        </motion.div>

        {/* ── Readiness + Skills + Companies ── */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className={cardCls}>
            <SectionHeader icon={<Brain size={14} />} title="Interview Readiness" subtitle={profileReadiness?.next_milestone || "Overall readiness across all domains"} />
            <div className="flex flex-col items-center">
              <PredictorGauge probability={Math.round(readinessScore)} size={200} />
              <div className="w-full grid grid-cols-2 gap-2 mt-3">
                {(profileReadiness?.breakdown && Object.entries(profileReadiness.breakdown)) || (gamReadiness?.categories && Object.entries(gamReadiness.categories)) ? (
                  Object.entries(profileReadiness?.breakdown || gamReadiness?.categories || {}).slice(0, 4).map(([key, val]) => (
                    <div key={key} className="text-center">
                      <div className="text-xs font-bold text-text-primary">{Math.round((Number(val) || 0) * 10) / 10}</div>
                      <div className="text-[9px] text-brand-muted uppercase tracking-wide">{humanize(key)}</div>
                    </div>
                  ))
                ) : null}
              </div>
            </div>
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }} className={cardCls}>
            <SectionHeader icon={<BarChart3 size={14} />} title="Skill Overview" subtitle="Score per skill domain (out of 10)" />
            <div className="space-y-3">
              {skillList.length === 0 && <p className="text-xs text-brand-muted text-center py-6">Complete activities to build your skill graph.</p>}
              {skillList.slice(0, 5).map((s) => (
                <div key={s.key} className="flex items-center gap-3">
                  <div className="w-24 sm:w-28 text-xs text-gray-400 truncate shrink-0">{s.name}</div>
                  <div className="flex-1"><Bar value={(s.score / 10) * 100} color={s.score >= 7 ? "bg-green-500" : s.score >= 4 ? "bg-yellow-500" : "bg-red-500"} /></div>
                  <div className="w-8 text-right text-[10px] text-brand-muted shrink-0">{s.score}</div>
                </div>
              ))}
            </div>
            {readinessRecs.length > 0 && (
              <div className="mt-4 pt-3 border-t border-black/10 space-y-1.5">
                {readinessRecs.slice(0, 3).map((r, i) => (
                  <p key={i} className="text-[10px] text-gray-400">• {r}</p>
                ))}
              </div>
            )}
          </motion.div>

          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className={cardCls}>
            <SectionHeader icon={<Building2 size={14} />} title="Company Matches" subtitle="How close you are to target companies" />
            {!companyMatches?.matches || companyMatches.matches.length === 0 ? (
              <p className="text-xs text-brand-muted text-center py-6">Add target companies in onboarding to see matches.</p>
            ) : (
              <div className="space-y-3">
                {companyMatches.matches.slice(0, 3).map((m, i) => (
                  <Link key={i} to="/company-prep" className="block group">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs font-medium text-text-primary group-hover:text-cyber-blue transition-colors">{m.company}</span>
                      <span className="text-[10px] text-brand-muted">{m.match_percent}%</span>
                    </div>
                    <Bar value={m.match_percent} color={m.match_percent >= 70 ? "bg-green-500" : m.match_percent >= 40 ? "bg-yellow-500" : "bg-red-500"} />
                  </Link>
                ))}
              </div>
            )}
            {companyMatches?.matches?.length > 0 && (
              <p className="text-[10px] text-brand-muted mt-3 line-clamp-2">{companyMatches.matches[0].missing_skills?.join(" · ")}</p>
            )}
          </motion.div>
        </div>

        {/* ── Stat Cards ── */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
          {[
            { label: "Solved", value: overview?.total_solved || pd?.total_solved || 0, icon: <CheckCircle size={18} />, color: "text-green-400", bg: "bg-green-500/10" },
            { label: "Acceptance", value: `${overview?.acceptance_rate || 0}%`, icon: <Percent size={18} />, color: "text-blue-400", bg: "bg-blue-500/10" },
            { label: "Submissions", value: overview?.total_submissions || 0, icon: <Code2 size={18} />, color: "text-purple-400", bg: "bg-purple-500/10" },
            { label: "Badges", value: `${earnedBadgeCount}/${totalBadges}`, icon: <Award size={18} />, color: "text-orange-400", bg: "bg-orange-500/10" },
          ].map((stat, i) => (
            <motion.div key={stat.label} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 + i * 0.05 }}
              className={`${cardCls} text-center`}
            >
              <div className={`inline-flex p-2 rounded-lg ${stat.bg} ${stat.color} mb-2`}>{stat.icon}</div>
              <div className="text-lg sm:text-xl font-bold text-text-primary">{stat.value}</div>
              <div className="text-[10px] text-brand-muted uppercase tracking-wide">{stat.label}</div>
            </motion.div>
          ))}
        </div>

        {/* ── Main two-column grid ── */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-3 sm:gap-4">
          {/* Left column */}
          <div className="lg:col-span-3 space-y-3 sm:space-y-4">
            {/* Daily Plan */}
            {planTasks.length > 0 && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className={cardCls}>
                <SectionHeader
                  icon={<Target size={14} />}
                  title="Today's Plan"
                  subtitle={`${planData?.task_count || 0} tasks · ${planData?.total_estimated_minutes || 0} min · ${planData?.overall_mastery_label || ""}`}
                  action={<span className="text-[10px] text-brand-muted font-mono">{planData?.date}</span>}
                />
                {planFocus.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-3">
                    {planFocus.map((f, i) => (
                      <span key={i} className="px-2.5 py-1 rounded-full text-[10px] bg-surface-2 border border-black/10 text-brand-secondary" style={{ color: f.color }}>
                        {f.emoji} {f.name} · {f.score}/10 · {f.mastery_label}
                      </span>
                    ))}
                  </div>
                )}
                <div className="space-y-2">
                  {planTasks.slice(0, 4).map((t, i) => (
                    <div key={t.id || i} className="flex items-center gap-3 p-2.5 rounded-lg bg-surface-2 border border-black/5">
                      <span className="text-lg shrink-0">{t.emoji || "📘"}</span>
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-medium text-text-primary truncate">{t.title}</div>
                        <div className="text-[10px] text-gray-500 flex items-center gap-2 mt-0.5">
                          <span className="flex items-center gap-1"><Timer size={10} />{t.estimated_minutes}m</span>
                          <span className="flex items-center gap-1"><Zap size={10} className="text-amber-400" />{t.xp_reward} XP</span>
                          {t.difficulty && <DiffChip difficulty={t.difficulty} />}
                        </div>
                      </div>
                      <Link to="/question-bank" className="shrink-0 text-cyber-blue hover:text-cyber-blue/80"><ChevronRight size={16} /></Link>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Recommendations */}
            {(pdRecs.length > 0 || weakTopics.length > 0) && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }} className={cardCls}>
                <SectionHeader icon={<Sparkles size={14} />} title="Recommendations" subtitle="Personalized based on your recent performance" />
                <div className="space-y-2">
                  {pdRecs.map((r, i) => (
                    <Link key={i} to={mapAction(r.action)} className="flex items-start gap-3 p-2.5 rounded-lg hover:bg-surface-2 transition-colors group">
                      <span className={`mt-0.5 w-1.5 h-1.5 rounded-full shrink-0 ${
                        r.priority === "high" ? "bg-red-500" : r.priority === "medium" ? "bg-yellow-500" : "bg-green-500"
                      }`} />
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-medium text-text-primary">{r.title}</div>
                        <div className="text-[10px] text-gray-500 mt-0.5 line-clamp-2">{r.description}</div>
                      </div>
                      <ChevronRight size={14} className="shrink-0 text-gray-600 group-hover:text-cyber-blue" />
                    </Link>
                  ))}
                </div>
                {weakTopics.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-black/10 flex flex-wrap gap-2">
                    {weakTopics.map((t, i) => (
                      <Link key={i} to={`/question-bank?topic=${encodeURIComponent(t.topic)}`}
                        className="px-3 py-1.5 bg-red-500/10 border border-red-500/20 rounded-full text-xs text-red-400 hover:bg-red-500/20 transition-colors"
                      >
                        {t.topic} ({t.percentage}%)
                      </Link>
                    ))}
                  </div>
                )}
              </motion.div>
            )}

            {/* Recent Activity */}
            {pdActivity.length > 0 && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className={cardCls}>
                <SectionHeader icon={<Activity size={14} />} title="Recent Activity" subtitle="Your latest solved problems" />
                <div className="space-y-2">
                  {pdActivity.slice(0, 5).map((a, i) => (
                    <div key={i} className="flex items-center gap-3 p-2.5 rounded-lg hover:bg-surface-2 transition-colors">
                      <span className={`shrink-0 ${a.is_correct ? "text-green-400" : "text-red-400"}`}>
                        {a.is_correct ? <CheckCircle size={14} /> : <FileText size={14} />}
                      </span>
                      <div className="flex-1 min-w-0">
                        <div className="text-xs font-medium text-text-primary truncate">{a.question_title}</div>
                        <div className="text-[10px] text-gray-500">{a.topic} · {formatDate(a.created_at)}</div>
                      </div>
                      <DiffChip difficulty={a.difficulty} />
                      {typeof a.score === "number" && <span className="text-[10px] text-gray-500 shrink-0">{a.score}%</span>}
                    </div>
                  ))}
                </div>
              </motion.div>
            )}

            {/* Weak skills */}
            {weakSkills.length > 0 && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }} className={cardCls}>
                <SectionHeader icon={<TrendingUp size={14} />} title="Weak Skills" subtitle="Lowest-scoring skills — drill these next" />
                <div className="flex flex-wrap gap-2">
                  {weakSkills.map((w, i) => (
                    <Link key={i} to={`/question-bank?topic=${encodeURIComponent(w.category || w.skill)}`}
                      className="px-3 py-1.5 bg-red-500/10 border border-red-500/20 rounded-full text-xs text-red-400 hover:bg-red-500/20 transition-colors"
                    >
                      {w.category_name || humanize(w.category)} · {humanize(w.skill)} ({w.score}/10)
                    </Link>
                  ))}
                </div>
              </motion.div>
            )}
          </div>

          {/* Right column */}
          <div className="lg:col-span-2 space-y-3 sm:space-y-4">
            {/* League */}
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }} className={cardCls}>
              <SectionHeader
                icon={<Trophy size={14} />}
                title="Weekly League"
                subtitle={leaderRank && leaderOf ? `Ranked #${leaderRank} of ${leaderOf} this week` : "Compete for XP to climb tiers"}
              />
              {leaderTier ? (
                <div>
                  <div className="flex items-center gap-3">
                    <span className="text-3xl">{leaderTier.icon}</span>
                    <div>
                      <div className="text-sm font-bold text-text-primary" style={{ color: leaderTier.color }}>{leaderTier.name}</div>
                      <div className="text-[10px] text-gray-500">{weeklyXp} XP this week</div>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-3">
                    {league?.promoted_next_week && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] bg-green-500/10 text-green-400 border border-green-500/20">⬆ Promoting</span>
                    )}
                    {league?.relegated_next_week && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] bg-red-500/10 text-red-400 border border-red-500/20">⬇ Relegating</span>
                    )}
                    <Link to="/rank" className="px-2 py-0.5 rounded-full text-[10px] bg-cyber-blue/10 text-cyber-blue border border-cyber-blue/20 hover:bg-cyber-blue/20 transition-colors">
                      Rank ladder →
                    </Link>
                  </div>
                </div>
              ) : (
                <p className="text-xs text-gray-500">Earn XP to enter the weekly league ladder.</p>
              )}
            </motion.div>

            {/* Tower */}
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className={cardCls}>
              <SectionHeader icon={<Sword size={14} />} title="The Tower" subtitle="Climb floors and defeat bosses every 10 levels" />
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm font-bold text-text-primary">Floor {Math.floor(level / 10)} · Level {level}</div>
                  <div className="text-[10px] text-gray-500 mt-0.5">
                    {hasBossAvailable
                      ? `Boss battle available at Level ${towerBossLevel}!`
                      : nextBossLevel
                        ? `Next boss at Level ${nextBossLevel}`
                        : "All bosses defeated — max level!"}
                  </div>
                  {bossesDefeated.length > 0 && (
                    <div className="text-[10px] text-amber-400 mt-1">💀 {bossesDefeated.length} boss{bossesDefeated.length === 1 ? "" : "es"} defeated</div>
                  )}
                </div>
                <Link to="/tower" className="shrink-0 px-3 py-2 rounded-lg bg-cyber-blue/10 border border-cyber-blue/20 text-cyber-blue text-xs font-medium hover:bg-cyber-blue/20 transition-colors flex items-center gap-1">
                  Enter <ArrowRight size={12} />
                </Link>
              </div>
            </motion.div>

            {/* Daily + Weekly goals */}
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.45 }} className={cardCls}>
              <SectionHeader icon={<Target size={14} />} title="Goals" subtitle="Build consistency, one problem at a time" />
              <div className="space-y-4">
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs text-gray-300 flex items-center gap-1"><Calendar size={12} /> Daily</span>
                    <span className="text-[10px] text-gray-500 font-mono">{dailyGoalCount}/{dailyGoalTarget}</span>
                  </div>
                  <Bar value={dailyGoalPct} color={dailyGoalMet ? "bg-green-500" : "bg-blue-500"} />
                  {dailyGoalMet && (
                    <div className="flex items-center gap-1 mt-1.5 text-[10px] text-green-400"><CheckCircle size={11} /> Goal met!</div>
                  )}
                </div>
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-xs text-gray-300 flex items-center gap-1"><Calendar size={12} /> Weekly</span>
                    <span className="text-[10px] text-gray-500 font-mono">{weeklyGoal?.solved_this_week || 0}/{weeklyGoal?.weekly_goal || 7}</span>
                  </div>
                  <Bar value={weeklyGoal?.percentage || 0} color={weeklyGoal?.goal_met ? "bg-green-500" : "bg-yellow-500"} />
                  {weeklyGoal?.goal_met && (
                    <div className="flex items-center gap-1 mt-1.5 text-[10px] text-green-400"><CheckCircle size={11} /> Weekly goal crushed!</div>
                  )}
                </div>
              </div>
            </motion.div>

            {/* Difficulty breakdown */}
            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }} className={cardCls}>
              <SectionHeader icon={<Layers size={14} />} title="Difficulty Breakdown" />
              <div className="grid grid-cols-3 gap-2">
                {[
                  { key: "easy", label: "Easy", color: "text-green-400", bg: "bg-green-500/15" },
                  { key: "medium", label: "Medium", color: "text-yellow-400", bg: "bg-yellow-500/15" },
                  { key: "hard", label: "Hard", color: "text-red-400", bg: "bg-red-500/15" },
                ].map((d) => {
                  const solved = overview?.difficulty_breakdown?.[d.key] || 0;
                  return (
                    <div key={d.key} className={`rounded-xl p-3 text-center ${d.bg}`}>
                      <div className={`text-lg sm:text-xl font-bold ${d.color}`}>{solved}</div>
                      <div className="text-[9px] text-gray-400 uppercase tracking-wide">{d.label}</div>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          </div>
        </div>

        {/* ── Heatmap ── */}
        {heatmap && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}
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
                  {[0, 1, 2, 3, 4].map((l) => (
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

        {/* ── Topic Progress ── */}
        {topTopics.length > 0 && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.55 }} className={cardCls}>
            <SectionHeader icon={<BookOpen size={14} />} title="Topic Progress" subtitle="Solve coverage across DSA topics" />
            <div className="space-y-3">
              {topTopics.map((t, i) => (
                <div key={t.topic || i} className="flex items-center gap-3">
                  <div className="w-24 sm:w-32 text-xs text-gray-400 truncate shrink-0">{t.topic}</div>
                  <div className="flex-1">
                    <Bar value={t.percentage} color={t.percentage >= 80 ? "bg-green-500" : t.percentage >= 50 ? "bg-yellow-500" : "bg-red-500"} />
                  </div>
                  <div className="w-16 text-right text-[10px] text-gray-500 shrink-0">
                    {t.solved}/{t.total} <span className="text-gray-600">({t.percentage}%)</span>
                  </div>
                </div>
              ))}
            </div>
            {weakAreasPd.length > 0 && (
              <div className="mt-4 pt-4 border-t border-black/10">
                <h3 className="text-xs font-medium text-red-400 mb-2 flex items-center gap-1">
                  <TrendingUp size={12} /> Weak Areas — Practice These
                </h3>
                <div className="flex flex-wrap gap-2">
                  {weakAreasPd.slice(0, 3).map((t, i) => (
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

        {/* ── Badges ── */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className={cardCls}>
          <SectionHeader
            icon={<Award size={14} />}
            title={`Badges (${earnedBadgeCount}/${totalBadges})`}
            action={
              <button onClick={() => setShowAllBadges(!showAllBadges)} className="text-xs text-cyber-blue hover:text-cyber-blue/80">
                {showAllBadges ? "Show Less" : "View All"}
              </button>
            }
          />
          {earnedBadgeDetails.length === 0 && earnedBadgeIds.length === 0 ? (
            <div className="text-center py-6 text-gray-500">
              <Award size={32} className="mx-auto mb-2 opacity-50" />
              <p className="text-xs">Complete activities to earn badges!</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2 sm:gap-3">
              {(showAllBadges ? badges : earnedBadgeDetails.length > 0 ? earnedBadgeDetails.slice(0, 10) : earnedBadgeDetails)
                .filter(Boolean)
                .slice(0, showAllBadges ? 30 : 10)
                .map((badge, i) => {
                  const isEarned = earnedBadgeIds.includes(badge.id) || earnedBadgeDetails.some((b) => b.id === badge.id);
                  return (
                    <motion.div
                      key={badge.id || i}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: i * 0.03 }}
                      className={`relative p-3 rounded-xl border text-center cursor-default group ${
                        isEarned ? "bg-white border-black/10" : "bg-surface-2 border-black/5 opacity-50"
                      }`}
                    >
                      <div className="text-2xl mb-1">{badge.icon}</div>
                      <div className="text-[10px] font-medium text-gray-300">{badge.name}</div>
                      <div className="text-[9px] text-gray-500 mt-0.5 line-clamp-2">{badge.description}</div>
                    </motion.div>
                  );
                })}
            </div>
          )}
        </motion.div>

        {/* ── Leaderboard ── */}
        {leaderboard.length > 0 && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.65 }} className={cardCls}>
            <SectionHeader icon={<Trophy size={14} />} title="Leaderboard" subtitle="Top performers this week" />
            <div className="space-y-2">
              {leaderboard.slice(0, 5).map((entry, i) => {
                const isMe = entry.user_id === user?.id;
                return (
                  <div key={i} className={`flex items-center gap-3 p-2.5 rounded-lg ${isMe ? "bg-cyber-blue/10 border border-cyber-blue/20" : "hover:bg-surface-2"}`}>
                    <div className={`w-6 text-center text-xs font-bold ${i === 0 ? "text-yellow-400" : i === 1 ? "text-gray-400" : i === 2 ? "text-amber-500" : "text-gray-500"}`}>
                      {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${i + 1}`}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-xs font-medium text-text-primary truncate">{isMe ? "You" : `User ${entry.user_id?.slice(-4)}`}</div>
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

        {/* ── Quick Actions ── */}
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }} className={cardCls}>
          <SectionHeader icon={<Rocket size={14} />} title="Quick Actions" subtitle="Jump straight into any feature" />
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3">
            {[
              { to: "/question-bank", label: "Practice", icon: <Code2 size={18} />, color: "from-blue-500 to-cyan-500" },
              { to: "/interview", label: "Interview", icon: <Target size={18} />, color: "from-green-500 to-emerald-500" },
              { to: "/daily-challenge", label: "Daily Challenge", icon: <Calendar size={18} />, color: "from-orange-500 to-red-500" },
              { to: "/tower", label: "The Tower", icon: <Sword size={18} />, color: "from-purple-500 to-pink-500" },
              { to: "/battles", label: "1v1 Battles", icon: <Users size={18} />, color: "from-yellow-500 to-amber-500" },
              { to: "/company-prep", label: "Company Prep", icon: <Building2 size={18} />, color: "from-indigo-500 to-blue-500" },
              { to: "/scrims", label: "Scrims", icon: <PlayIcon size={18} />, color: "from-teal-500 to-cyan-500" },
              { to: "/learn", label: "Learning Hub", icon: <BookOpen size={18} />, color: "from-pink-500 to-rose-500" },
            ].map((link, i) => (
              <Link key={i} to={link.to}
                className="group p-4 bg-white border-border/90 border border-black/10 rounded-xl hover:border-black/15 hover:bg-surface-2 transition-all shadow-sm"
              >
                <div className={`inline-flex p-2 rounded-lg bg-gradient-to-br ${link.color} text-text-primary mb-2 group-hover:scale-110 transition-transform`}>
                  {link.icon}
                </div>
                <div className="text-xs sm:text-sm font-medium text-text-primary">{link.label}</div>
              </Link>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}

function SnowIcon() {
  return <Shield size={16} />;
}

function PlayIcon({ size = 18 }: { size?: number }) {
  return <Rocket size={size} />;
}
