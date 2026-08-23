import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import useReducedMotion from "../hooks/useReducedMotion";
import { Target, Calendar, ArrowRight, AlertCircle, RotateCw } from "lucide-react";
import { useToast } from "../components/Toast";

interface StudentStats {
  readiness?: number;
  level?: number;
  xp?: number;
  streak?: number;
  total_solved?: number;
  next_mission?: {
    label: string;
    to: string;
    minutes: number;
    xp?: number;
    description?: string;
  } | null;
  skill_scores?: Record<string, number>;
  weekly_improvement?: number;
  [key: string]: unknown;
}

function formatTimeAgo(dateStr: string) {
  if (!dateStr) return "";
  const now = new Date();
  const then = new Date(dateStr);
  const diffMs = now.getTime() - then.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "Just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  const diffDay = Math.floor(diffHr / 24);
  if (diffDay < 7) return `${diffDay}d ago`;
  return then.toLocaleDateString();
}

export default function StudentDashboard() {
  const { user } = useAuthStore();
  const reduced = useReducedMotion();
  const toast = useToast();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<StudentStats | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    (async () => {
      setLoading(true);
      try {
        const data = await api.getProfileStats().catch(() => null);
        if (!active) return;
        setStats(data || null);
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : "Failed to load");
        }
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  const greeting = (() => {
    const h = new Date().getHours();
    if (h < 5) return "Good evening";
    if (h < 12) return "Good morning";
    if (h < 18) return "Good afternoon";
    return "Good evening";
  })();

  const firstName = user?.name?.split(" ")[0] || "there";
  const readiness = stats?.readiness ?? 0;
  const mission = stats?.next_mission || {
    label: "Continue Your Preparation",
    to: "/prepare",
    minutes: 0,
    xp: 0,
    description: "Pick up where you left off.",
  };

  const weeklyImprovement = stats?.weekly_improvement ?? Math.max(1, Math.round(readiness / 12));

  const SKILL_DISPLAY = [
    { key: "dsa", label: "DSA" },
    { key: "cs_fundamentals", label: "CS" },
    { key: "interview", label: "Interview" },
    { key: "resume", label: "Resume" },
  ];

  if (loading) {
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
    <div className="min-h-screen px-4 py-6 md:py-8 page-surface">
      <div className="mx-auto max-w-5xl space-y-8">
        {/* Header — Q: Where am I? */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="flex items-center justify-between"
        >
          <div>
            <h1 className="text-2xl md:text-3xl font-black text-text-primary">
              {greeting}, {firstName}
            </h1>
            <p className="text-sm text-text-muted mt-1">
              SDE · {readiness}% ready
            </p>
          </div>
          <Link to="/career" className="text-text-muted hover:text-primary transition-colors">
            <span className="text-xl">🔔</span>
          </Link>
        </motion.div>

        {/* Next Mission — Q: What should I do now? */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.45, delay: 0.1 }}
        >
          <Link to={mission.to}>
            <div className="block rounded-[16px] p-6 bg-white border border-border shadow-card transition-all duration-300 hover:border-primary/20 hover:shadow-elevated">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-[10px] bg-primary-soft flex items-center justify-center text-2xl shrink-0">
                  ⚔
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 text-xs font-mono uppercase tracking-wider text-primary">
                    <Target size={14} /> Your next mission
                  </div>
                  <p className="mt-2 text-xl font-bold text-text-primary sm:text-2xl">
                    {mission.label}
                  </p>
                  {mission.description && (
                    <p className="mt-1 text-sm text-text-muted">
                      {mission.description}
                    </p>
                  )}
                  <div className="mt-3 flex items-center gap-4 text-xs text-text-muted">
                    {mission.minutes > 0 && <span>~{mission.minutes} min</span>}
                    {mission.xp && <span className="text-primary font-medium">+{mission.xp} XP</span>}
                  </div>
                </div>
                <div className="ml-4 text-text-muted">
                  <ArrowRight size={20} />
                </div>
              </div>
            </div>
          </Link>
        </motion.div>

        {/* Readiness + Skill Breakdown — am I improving? */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="rounded-[16px] p-6 bg-white border border-border shadow-card"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-text-primary">Your Readiness</h2>
            <span className="text-sm font-medium text-primary">+{weeklyImprovement}% this week</span>
          </div>

          <div className="mb-4">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-3xl font-black stat-numeral text-text-primary">{readiness}%</span>
              <span className="text-sm text-text-muted">Target: Software Engineer</span>
            </div>
            <div className="h-2 rounded-full bg-border overflow-hidden">
              <div
                className="h-full rounded-full bg-primary transition-all duration-500 ease-out"
                style={{ width: `${readiness}%` }}
              />
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center">
            {SKILL_DISPLAY.map((skill) => {
              const score = stats?.skill_scores?.[skill.key] ?? readiness;
              return (
                <div key={skill.key}>
                  <div className="text-xs text-text-muted mb-1">{skill.label}</div>
                  <div className="text-lg font-bold stat-numeral text-text-primary">{score}%</div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* Your Journey */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="rounded-[16px] p-6 bg-white border border-border shadow-card"
        >
          <h2 className="text-lg font-bold text-text-primary mb-4">Your Journey</h2>
          <div className="flex items-center justify-center">
            <div className="flex items-center gap-4 text-center">
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center text-xl mb-1">
                  🌱
                </div>
                <span className="text-xs text-text-muted">Foundations</span>
                <span className="text-xs font-bold text-primary">✓</span>
              </div>
              <div className="w-12 h-px bg-border"></div>
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center text-xl mb-1">
                  ⚔
                </div>
                <span className="text-xs text-text-muted">Problem Solver</span>
                <span className="text-xs font-bold text-primary">72%</span>
              </div>
              <div className="w-12 h-px bg-border"></div>
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-[10px] bg-surface-2 border border-border flex items-center justify-center text-xl mb-1">
                  🔒
                </div>
                <span className="text-xs text-text-muted">Builder</span>
                <span className="text-xs text-text-muted">Locked</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* This Week */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="rounded-[16px] p-6 bg-white border border-border shadow-card"
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
