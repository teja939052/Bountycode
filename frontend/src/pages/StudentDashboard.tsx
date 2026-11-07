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
  Lightbulb,
  BarChart3,
  RotateCw,
  AlertCircle,
  Shield,
  CheckCircle2,
  Building2,
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

interface DailyMissionProblem {
  id: string;
  question_title?: string;
  statement?: string;
  difficulty?: string;
  topics?: string[];
  domain?: string;
  type?: string;
}

interface DailyMission {
  date: string;
  mission_type?: string;
  target_company?: string;
  problems: DailyMissionProblem[];
  problem_count: number;
  estimated_minutes: number;
  already_completed: boolean;
  diamonds_reward?: number;
}

interface ReadinessBreakdown {
  overall_readiness: number;
  domain_scores: Record<string, number>;
  per_company_scores: Record<string, any>;
  target_company?: string;
  blockers: string[];
  next_focus: string;
  readiness_level: string;
}

const QUICK_ACTIONS = [
  { to: "/practice", icon: Code2, label: "Practice", desc: "DSA problems", color: "#22C55E" },
  { to: "/interview", icon: Briefcase, label: "Interviews", desc: "Mock sessions", color: "#4A90E2" },
  { to: "/learn/c", icon: BookOpen, label: "Learn", desc: "Coding lessons", color: "#8B6BD9" },
  { to: "/company-prep", icon: Briefcase, label: "Companies", desc: "53+ guides", color: "#EAB74D" },
  { to: "/question-bank", icon: Target, label: "Problems", desc: "Curated bank", color: "#E96A5B" },
  { to: "/compiler", icon: Lightbulb, label: "Compiler", desc: "Run code", color: "#5BA7A0" },
];

const SKILL_DISPLAY = [
  { key: "aptitude", label: "Aptitude", color: "#D946EF", icon: BarChart3 },
  { key: "verbal", label: "Verbal", color: "#10B981", icon: BookOpen },
  { key: "coding", label: "Coding", color: "#22C55E", icon: Code2 },
  { key: "dsa", label: "DSA", color: "#4A90E2", icon: Code2 },
  { key: "interview", label: "Interview", color: "#8B6BD9", icon: Briefcase },
  { key: "cs_fundamentals", label: "CS", color: "#EAB74D", icon: BookOpen },
];

export default function StudentDashboard() {
  const { user } = useAuthStore();
  const reduced = useReducedMotion();
  const [stats, setStats] = useState<StudentStats | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dailyMission, setDailyMission] = useState<DailyMission | null>(null);
  const [readiness, setReadiness] = useState<ReadinessBreakdown | null>(null);
  const [missionLoading, setMissionLoading] = useState(false);
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

  useEffect(() => {
    let active = true;
    (async () => {
      setMissionLoading(true);
      try {
        const res = await fetch("/api/v1/daily/challenge", { credentials: "include" });
        const data = await res.json().catch(() => null);
        if (active && data) setDailyMission(data);
      } catch {
        // ignore
      } finally {
        if (active) setMissionLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await api.adaptive.getReadinessScore(null);
        if (active && data?.data) {
          const d = data.data;
          setReadiness({
            overall_readiness: d.overall_readiness ?? d.overall ?? 0,
            domain_scores: d.category_scores ?? d.domain_scores ?? d.categories ?? {},
            per_company_scores: d.company_specific ? { [d.company_specific.company]: d.company_specific.score } : {},
            target_company: d.target_readiness?.target?.company,
            blockers: d.target_readiness?.blockers?.map((b: any) => b.skill_id || b) || [],
            next_focus: d.target_readiness?.next_action?.skill_id || d.next_focus || "aptitude",
            readiness_level: d.readiness_level || "",
          });
        }
      } catch {
        // ignore
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
  const readinessScore = readiness?.overall_readiness ?? stats?.readiness ?? 0;
  const domainScores = readiness?.domain_scores ?? stats?.skill_scores ?? {};
  const targetCompany = readiness?.target_company || dailyMission?.target_company || "general";
  const diamonds = profile?.diamonds ?? stats?.diamonds ?? 0;
  const streak = profile?.streak ?? stats?.streak ?? 0;
  const level = profile?.level ?? stats?.level ?? 1;
  const blockers = readiness?.blockers || [];
  const nextFocus = readiness?.next_focus || "aptitude";
  const readinessLevel = readiness?.readiness_level || "Getting Started";

  const mission = dailyMission || stats?.next_mission || {
    label: "Start Your Daily Mission",
    to: "/practice",
    minutes: 30,
    description: "Complete your daily contract to earn Proof and Bounty.",
  };

  const weeklyImprovement = stats?.weekly_improvement ?? Math.max(1, Math.round(readinessScore / 12));
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
                  Target: {targetCompany.toUpperCase()} • Level {level} • {readinessLevel}
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-bold text-amber-700 border border-amber-200">
                <Shield size={14} /> {diamonds} Diamonds
              </span>
              <span className="inline-flex items-center gap-1.5 rounded-full bg-sky-50 px-2.5 py-1 text-xs font-bold text-sky-700 border border-sky-200">
                <Zap size={14} /> {diamonds} Diamonds
              </span>
              {streak > 0 && (
                <span className="inline-flex items-center gap-1.5 rounded-full bg-orange-50 px-2.5 py-1 text-xs font-bold text-orange-700">
                  <Flame size={14} className="fill-orange-500 text-orange-500" /> {streak}d
                </span>
              )}
              <Link to="/tower" className="flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-bold text-amber-700">
                <Trophy size={14} />
                Tower
              </Link>
            </div>
          </div>
          <div className="mt-2 flex items-center gap-3">
            <div className="h-2 flex-1 rounded-full bg-border overflow-hidden">
              <div
                className="h-full rounded-full bg-primary transition-all duration-700 ease-out"
                style={{ width: `${Math.min(100, Math.max(0, readinessScore))}%` }}
              />
            </div>
            <span className="text-xs font-bold text-text-primary">{Math.round(readinessScore)}%</span>
          </div>
        </motion.div>

        {/* Today's Contract */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.45, delay: 0.1 }}
        >
          <Link to={mission.to || "/practice"}>
            <div className="block rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card transition-all duration-300 hover:border-primary/30 hover:shadow-elevated relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent pointer-events-none" />
              <div className="relative flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-start gap-4">
                  <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl bg-primary-soft text-3xl">
                    ⚔️
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-wider text-primary">
                      <Target size={12} /> Today&apos;s Contract
                      {dailyMission?.target_company && (
                        <span className="rounded-full bg-nature-blossom/10 px-2 py-0.5 text-[10px] font-bold text-nature-blossom">
                          {dailyMission.target_company.toUpperCase()}
                        </span>
                      )}
                    </div>
                    <p className="mt-2 text-xl font-bold text-text-primary sm:text-2xl leading-tight">
                      {mission.label || "Daily Mission"}
                    </p>
                    {(mission as any)?.description && (
                      <p className="mt-1 text-sm text-text-muted">
                        {(mission as any).description}
                      </p>
                    )}
                    {dailyMission?.problems?.length > 0 && (
                      <div className="mt-3 flex flex-wrap gap-2">
                        {dailyMission.problems.map((p, idx) => (
                          <span key={idx} className="inline-flex items-center gap-1 rounded-full border border-border bg-surface px-2.5 py-1 text-[11px] font-mono text-text-secondary">
                            <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                            {p.domain || p.topic || `Problem ${idx + 1}`}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-text-muted">
                      <span>~{mission.minutes || dailyMission?.estimated_minutes || 30} min</span>
                       <span className="text-primary font-semibold">+{dailyMission?.diamonds_reward || 20} Diamonds</span>
                       <span className="text-sky-600 font-semibold">+{dailyMission?.diamonds_reward || 10} Diamonds</span>
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

        {/* Company Tracks */}
        <CompanyTracksSection />

        {/* Company Readiness */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <BarChart3 size={18} className="text-primary" />
              <h2 className="text-lg font-bold text-text-primary">
                {targetCompany.toUpperCase()} Readiness
              </h2>
            </div>
            <span className="text-sm font-medium text-primary">+{weeklyImprovement}% this week</span>
          </div>

          <div className="mb-4">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="text-4xl font-black stat-numeral text-text-primary">{Math.round(readinessScore)}%</span>
              <span className="text-sm text-text-muted">{readinessLevel || "In Progress"}</span>
            </div>
            <div className="h-2.5 rounded-full bg-border overflow-hidden">
              <div
                className="h-full rounded-full bg-primary transition-all duration-700 ease-out"
                style={{ width: `${Math.min(100, Math.max(0, readinessScore))}%` }}
              />
            </div>
          </div>

          {blockers.length > 0 && (
            <div className="mb-4 rounded-xl border border-red-200 bg-red-50 p-4">
              <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-red-700 mb-2">
                <AlertCircle size={14} /> Blockers
              </div>
              <div className="flex flex-wrap gap-2">
                {blockers.map((b) => (
                  <span key={b} className="inline-flex items-center gap-1 rounded-full bg-red-100 px-2.5 py-1 text-xs font-medium text-red-800">
                    <span className="h-1.5 w-1.5 rounded-full bg-red-500" />
                    {b.replace(/_/g, " ")}
                  </span>
                ))}
              </div>
              <p className="mt-2 text-xs text-red-700">
                Focus area: <span className="font-bold">{nextFocus.replace(/_/g, " ")}</span>
              </p>
            </div>
          )}

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {SKILL_DISPLAY.map((skill, i) => {
              const score = domainScores[skill.key] ?? 0;
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

        {/* Journey Progress */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
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
              <span className="text-[10px] font-bold text-primary">{Math.round(readinessScore)}%</span>
            </div>
            <div className="w-8 sm:w-12 h-px bg-border shrink-0" />
            <div className="flex flex-col items-center gap-1 min-w-[64px]">
              <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-surface border border-border flex items-center justify-center text-xl sm:text-2xl">
                🔒
              </div>
              <span className="text-[10px] sm:text-xs text-text-muted">Ready</span>
              <span className="text-[10px] text-text-muted">{Math.round(readinessScore)}%</span>
            </div>
          </div>
        </motion.div>

        {/* Weekly overview */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
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

        {/* Weekly overview */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
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

        <CompanyTracksSection />
      </div>
    </div>
  );
}

function CompanyTracksSection() {
  const { user } = useAuthStore();
  const reduced = useReducedMotion();
  const [tracks, setTracks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await api.companyTracks.listCompanies();
        if (active) setTracks(data.tracks || []);
      } catch {
        // ignore
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  if (loading) {
    return (
      <motion.div
        initial={reduced ? {} : { opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
      >
        <h2 className="text-lg font-bold text-text-primary mb-4">Your Companies</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-32 bg-border rounded-xl animate-pulse" />
          ))}
        </div>
      </motion.div>
    );
  }

  if (!tracks.length) return null;

  return (
    <motion.div
      initial={reduced ? {} : { opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Building2 size={18} className="text-primary" />
          <h2 className="text-lg font-bold text-text-primary">Your Companies</h2>
        </div>
        <Link to="/company-tracks" className="text-sm text-primary hover:underline">
          View all
        </Link>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {tracks.map((track, i) => (
          <motion.div
            key={track.id}
            initial={reduced ? {} : { opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <Link
              to={`/tracks/${track.id}`}
              className="block rounded-xl border border-border p-4 hover:border-primary/30 hover:shadow-md transition-all"
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="text-2xl">{track.icon}</span>
                <div>
                  <p className="text-sm font-bold text-text-primary">{track.name}</p>
                  <p className="text-[10px] text-text-muted">{track.duration_minutes} min • {track.difficulty}</p>
                </div>
              </div>
              <div className="flex items-center justify-between text-xs">
                <span className="text-text-muted">{track.total_modules} modules</span>
                <span className={`font-bold ${track.enrolled ? "text-primary" : "text-text-muted"}`}>
                  {track.enrolled ? `${track.progress_pct}%` : "Not started"}
                </span>
              </div>
              {track.enrolled && (
                <div className="mt-2 h-1.5 rounded-full bg-border overflow-hidden">
                  <div
                    className="h-full rounded-full bg-primary transition-all duration-500"
                    style={{ width: `${Math.min(100, Math.max(0, track.progress_pct))}%` }}
                  />
                </div>
              )}
            </Link>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
