import { useEffect, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import useReducedMotion from "../hooks/useReducedMotion";
import {
  Target,
  ArrowRight,
  Flame,
  Trophy,
  Zap,
  Star,
  Code2,
  BookOpen,
  Briefcase,
  MessageSquare,
  Lightbulb,
  BarChart3,
  RotateCw,
  AlertCircle,
  Shield,
  CheckCircle2,
} from "lucide-react";
import { useGamificationState } from "../hooks/useGamificationState";
import DiamondsBar from "../components/XPBar";
import BadgeCard from "../components/BadgeCard";

interface StudentStats {
  readiness?: number;
  level?: number;
  diamonds?: number;
  streak?: number;
  total_solved?: number;
  next_mission?: {
    label: string;
    to: string;
    minutes: number;
    diamonds?: number;
    description?: string;
  } | null;
  skill_scores?: Record<string, number>;
  weekly_improvement?: number;
  [key: string]: unknown;
}

const QUICK_ACTIONS = [
  { to: "/practice", icon: Code2, label: "Practice", desc: "DSA problems", color: "#22C55E" },
  { to: "/interview", icon: MessageSquare, label: "Interviews", desc: "Mock sessions", color: "#4A90E2" },
  { to: "/learn/c", icon: BookOpen, label: "Learn", desc: "Coding lessons", color: "#8B6BD9" },
  { to: "/company-prep", icon: Briefcase, label: "Companies", desc: "53+ guides", color: "#EAB74D" },
  { to: "/question-bank", icon: Target, label: "Problems", desc: "3000+ questions", color: "#E96A5B" },
  { to: "/compiler", icon: Lightbulb, label: "Compiler", desc: "Run code", color: "#5BA7A0" },
];

const SKILL_DISPLAY = [
  { key: "dsa", label: "DSA", color: "#22C55E", icon: Code2 },
  { key: "cs_fundamentals", label: "CS", color: "#4A90E2", icon: BookOpen },
  { key: "interview", label: "Interview", color: "#8B6BD9", icon: MessageSquare },
  { key: "resume", label: "Resume", color: "#EAB74D", icon: Briefcase },
];

export default function StudentDashboard() {
  const { user } = useAuthStore();
  const reduced = useReducedMotion();
  const [stats, setStats] = useState<StudentStats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { profile, isLoading: gamificationLoading } = useGamificationState();

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await api.getProfileStats().catch(() => null);
        if (!active) return;
        setStats(data || null);
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : "Failed to load");
        }
      }
    })();
    return () => { active = false; };
  }, []);

  const greeting = useMemo(() => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 18) return "Good afternoon";
    return "Good evening";
  }, []);

  const firstName = user?.name?.split(" ")[0] || "there";
  const readiness = stats?.readiness ?? 0;
  const mission = stats?.next_mission || {
    label: "Continue Your Preparation",
    to: "/prep-hub",
    minutes: 0,
    diamonds: 0,
    description: "Pick up where you left off.",
  };

  const weeklyImprovement = stats?.weekly_improvement ?? Math.max(1, Math.round(readiness / 12));
  const level = profile?.level ?? stats?.level ?? 1;
  const streak = profile?.streak ?? stats?.streak ?? 0;
  const badges = (profile as any)?.badges_details as any[] | undefined;
  const recentBadges = useMemo(() => badges?.slice(-6) || [], [badges]);

  if (gamificationLoading) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8 page-surface">
        <div className="mx-auto max-w-5xl space-y-8">
          <div className="h-8 w-48 bg-border rounded animate-pulse" />
          <div className="h-32 bg-white border border-border rounded-[16px] animate-pulse" />
          <div className="h-64 bg-white border border-border rounded-[16px] animate-pulse" />
          <div className="h-24 bg-white border border-border rounded-[16px] animate-pulse" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle size={48} className="mx-auto text-red-400 mb-4" />
          <h2 className="text-xl font-bold text-text-primary mb-2">Failed to Load Dashboard</h2>
          <p className="text-sm text-text-muted mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-2 rounded-[10px] bg-primary text-text-primary text-sm font-medium hover:bg-primary-dark transition-colors"
          >
            <RotateCw size={14} className="inline mr-2" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 page-surface pb-24 md:pb-8">
      <div className="mx-auto max-w-5xl space-y-6">
        {/* Player status bar */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="rounded-[16px] border border-border bg-white p-4 shadow-card"
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary-soft text-xl">
                🧑‍🚀
              </div>
              <div>
                <p className="text-sm font-bold text-text-primary">
                  {greeting}, {firstName}
                </p>
                <p className="text-xs text-text-muted">
                  SDE · Lv. {level}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {streak > 0 && (
                <div className="flex items-center gap-1 rounded-full bg-orange-50 px-2.5 py-1 text-xs font-bold text-orange-600">
                  <Flame size={14} className="fill-orange-500 text-orange-500" />
                  {streak}
                </div>
              )}
              <Link to="/tower" className="flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-bold text-amber-700">
                <Trophy size={14} />
                Tower
              </Link>
            </div>
          </div>
          <XPBar
            level={level}
            xpIntoLevel={profile?.xp_into_level}
            xpForNext={profile?.xp_level_span}
            compact
            className="mt-2"
          />
        </motion.div>

        {/* Mission card */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.45, delay: 0.1 }}
        >
          <Link to={mission.to}>
            <div className="block rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card transition-all duration-300 hover:border-primary/30 hover:shadow-elevated relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent pointer-events-none" />
              <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-start gap-4">
                  <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-primary-soft text-3xl">
                    ⚔️
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-wider text-primary">
                      <Target size={12} /> Your next mission
                    </div>
                    <p className="mt-2 text-xl font-bold text-text-primary sm:text-2xl leading-tight">
                      {mission.label}
                    </p>
                    {mission.description && (
                      <p className="mt-1 text-sm text-text-muted">
                        {mission.description}
                      </p>
                    )}
                    <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-text-muted">
                      {mission.minutes > 0 && <span className="flex items-center gap-1"><Zap size={12} />~{mission.minutes} min</span>}
                      {mission.diamonds ? (
                        <span className="flex items-center gap-1 text-primary font-semibold">
                          <Star size={12} /> +{mission.diamonds} Diamonds
                        </span>
                      ) : null}
                    </div>
                  </div>
                </div>
                <div className="shrink-0">
                  <span className="inline-flex items-center gap-1.5 rounded-full bg-primary px-5 py-2.5 text-sm font-bold text-white shadow-lg shadow-primary/30 hover:shadow-xl hover:shadow-primary/40 transition-all">
                    START
                    <ArrowRight size={14} />
                  </span>
                </div>
              </div>
            </div>
          </Link>
        </motion.div>

        {/* Readiness + skills */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <BarChart3 size={18} className="text-primary" />
              <h2 className="text-lg font-bold text-text-primary">Your Readiness</h2>
            </div>
            <span className="text-sm font-medium text-primary">+{weeklyImprovement}% this week</span>
          </div>

          <div className="mb-5">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-4xl font-black stat-numeral text-text-primary">{readiness}%</span>
              <span className="text-sm text-text-muted">Target: Software Engineer</span>
            </div>
            <div className="h-2.5 rounded-full bg-border overflow-hidden">
              <div
                className="h-full rounded-full bg-primary transition-all duration-700 ease-out"
                style={{ width: `${Math.min(100, Math.max(0, readiness))}%` }}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {SKILL_DISPLAY.map((skill, i) => {
              const score = stats?.skill_scores?.[skill.key] ?? readiness;
              return (
                <motion.div
                  key={skill.key}
                  initial={reduced ? {} : { opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.1 + i * 0.05 }}
                  className="flex flex-col items-center text-center rounded-xl border border-border p-3"
                >
                  <div className="relative mb-2">
                    <svg width={72} height={72} className="-rotate-90">
                      <circle cx={36} cy={36} r={30} stroke="#e5e7eb" strokeWidth={6} fill="none" />
                      <circle
                        cx={36}
                        cy={36}
                        r={30}
                        stroke={skill.color}
                        strokeWidth={6}
                        strokeDasharray={2 * Math.PI * 30}
                        strokeDashoffset={2 * Math.PI * 30 * (1 - Math.min(100, Math.max(0, score)) / 100)}
                        fill="none"
                        strokeLinecap="round"
                        style={{ transition: "stroke-dashoffset 700ms ease-out" }}
                      />
                    </svg>
                    <div className="absolute inset-0 flex items-center justify-center">
                      <skill.icon size={16} style={{ color: skill.color }} />
                    </div>
                  </div>
                  <p className="text-xs font-semibold text-text-primary">{skill.label}</p>
                  <p className="text-[11px] text-text-muted">{Math.round(score)}%</p>
                </motion.div>
              );
            })}
          </div>
        </motion.div>

        {/* Quick actions */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
        >
          <div className="flex items-center gap-2 mb-4">
            <Zap size={18} className="text-primary" />
            <h2 className="text-lg font-bold text-text-primary">Quick Actions</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {QUICK_ACTIONS.map((action, i) => (
              <motion.div
                key={action.to}
                initial={reduced ? {} : { opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.05 * i }}
              >
                <Link
                  to={action.to}
                  className="flex flex-col items-center gap-2 rounded-xl border border-border bg-surface p-4 transition-all hover:border-primary/30 hover:shadow-md hover:-translate-y-0.5"
                >
                  <div
                    className="flex h-10 w-10 items-center justify-center rounded-xl"
                    style={{ backgroundColor: `${action.color}15`, color: action.color }}
                  >
                    <action.icon size={20} />
                  </div>
                  <div className="text-center">
                    <p className="text-xs font-semibold text-text-primary">{action.label}</p>
                    <p className="text-[10px] text-text-muted">{action.desc}</p>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Recent achievements */}
        {recentBadges.length > 0 && (
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.35 }}
            className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Trophy size={18} className="text-amber-500" />
                <h2 className="text-lg font-bold text-text-primary">Recent Achievements</h2>
              </div>
              <Link to="/tower" className="text-xs font-medium text-primary hover:underline">
                View all
              </Link>
            </div>
            <div className="flex gap-3 overflow-x-auto pb-2 -mx-1 px-1">
              {recentBadges.map((badge) => (
                <div key={badge.id} className="shrink-0">
                  <BadgeCard
                    name={badge.name}
                    description={badge.description}
                    icon={badge.icon}
                    rarity={badge.rarity}
                    unlocked
                    compact
                  />
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Journey progress */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
        >
          <h2 className="text-lg font-bold text-text-primary mb-4">Your Journey</h2>
          <div className="flex items-center justify-center gap-2 sm:gap-4 overflow-x-auto pb-2">
            <div className="flex flex-col items-center gap-1 min-w-[64px]">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-primary-soft flex items-center justify-center text-xl sm:text-2xl">
                🌱
              </div>
              <span className="text-[10px] sm:text-xs text-text-muted">Foundations</span>
              <span className="text-[10px] font-bold text-primary">✓</span>
            </div>
            <div className="w-8 sm:w-12 h-px bg-border shrink-0" />
            <div className="flex flex-col items-center gap-1 min-w-[64px]">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-primary-soft flex items-center justify-center text-xl sm:text-2xl">
                ⚔️
              </div>
              <span className="text-[10px] sm:text-xs text-text-muted">Problem Solver</span>
              <span className="text-[10px] font-bold text-primary">72%</span>
            </div>
            <div className="w-8 sm:w-12 h-px bg-border shrink-0" />
            <div className="flex flex-col items-center gap-1 min-w-[64px]">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-surface border border-border flex items-center justify-center text-xl sm:text-2xl">
                🔒
              </div>
              <span className="text-[10px] sm:text-xs text-text-muted">Builder</span>
              <span className="text-[10px] text-text-muted">Locked</span>
            </div>
          </div>
        </motion.div>

        {/* Weekly overview */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
        >
          <h2 className="text-lg font-bold text-text-primary mb-4">This Week</h2>
          <div className="flex flex-wrap gap-6 text-sm">
            <span className="text-text-muted">
              <span className="font-medium text-text-primary">4</span> missions
            </span>
            <span className="text-text-muted">
              <span className="font-medium text-text-primary">2</span> assessments
            </span>
            <span className="text-text-muted">
              <span className="font-medium text-primary">+{weeklyImprovement}%</span> readiness
            </span>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
