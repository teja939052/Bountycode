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
  Zap,
  BarChart3,
  RotateCw,
  AlertCircle,
  BookOpen,
  Code2,
  Briefcase,
  Trophy,
  Shield,
} from "lucide-react";
import { useGamificationState } from "../hooks/useGamificationState";

interface DailyMission {
  date: string;
  mission_type?: string;
  target_company?: string;
  problems: Array<{
    id: string;
    question_title?: string;
    statement?: string;
    difficulty?: string;
    topics?: string[];
    domain?: string;
    type?: string;
  }>;
  problem_count: number;
  estimated_minutes: number;
  already_completed: boolean;
  diamonds_reward?: number;
  readiness?: number;
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

const SKILL_DISPLAY = [
  { key: "aptitude", label: "Aptitude", color: "#D946EF", icon: BarChart3 },
  { key: "verbal", label: "Verbal", color: "#10B981", icon: BookOpen },
  { key: "coding", label: "Coding", color: "#22C55E", icon: Code2 },
  { key: "dsa", label: "DSA", color: "#4A90E2", icon: Code2 },
  { key: "interview", label: "Interview", color: "#8B6BD9", icon: Briefcase },
  { key: "cs_fundamentals", label: "CS", color: "#EAB74D", icon: BookOpen },
];

const QUICK_ACTIONS = [
  { to: "/learn", icon: BookOpen, label: "Learn", desc: "Patterns & lessons", color: "#8B6BD9" },
  { to: "/practice", icon: Code2, label: "Practice", desc: "Timed drills", color: "#22C55E" },
  { to: "/company-mocks", icon: Briefcase, label: "Assess", desc: "Mock OAs", color: "#4A90E2" },
  { to: "/readiness", icon: BarChart3, label: "Progress", desc: "Readiness & evidence", color: "#EAB74D" },
];

export default function PrepHub() {
  const { user } = useAuthStore();
  const reduced = useReducedMotion();
  const [dailyMission, setDailyMission] = useState<DailyMission | null>(null);
  const [readiness, setReadiness] = useState<ReadinessBreakdown | null>(null);
  const [missionLoading, setMissionLoading] = useState(false);
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const { profile, isLoading: gamificationLoading } = useGamificationState();

  useEffect(() => {
    let active = true;
    (async () => {
      setMissionLoading(true);
      try {
        const [missionRes, readinessRes, companiesRes] = await Promise.all([
          fetch("/api/v1/daily/challenge", { credentials: "include" }).then(r => r.ok ? r.json() : null).catch(() => null),
          api.adaptive.getReadinessScore(null).catch(() => null),
          fetch('/api/v1/indian-placement/companies', { credentials: 'include' }).then(r => r.ok ? r.json() : null).catch(() => null),
        ]);
        if (active) {
          setDailyMission(missionRes);
          if (readinessRes?.data) {
            const d = readinessRes.data;
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
          if (companiesRes?.companies) {
            setCompanies(companiesRes.companies);
          }
        }
      } catch {
        // ignore
      } finally {
        if (active) setMissionLoading(false);
      }
    })();
    return () => { active = false; };
  }, []);

  const firstName = user?.name?.split(" ")[0] || "there";
  const readinessScore = readiness?.overall_readiness ?? 0;
  const domainScores = readiness?.domain_scores ?? {};
  const targetCompany = readiness?.target_company || dailyMission?.target_company || "general";
  const diamonds = profile?.diamonds ?? 0;
  const streak = profile?.streak ?? 0;
  const level = profile?.level ?? 1;
  const blockers = readiness?.blockers || [];
  const nextFocus = readiness?.next_focus || "aptitude";
  const readinessLevel = readiness?.readiness_level || "Getting Started";

  const mission = dailyMission || {
    label: "Start Your Daily Mission",
    to: "/practice",
    estimated_minutes: 30,
    description: "Complete your daily contract to earn Proof and Bounty.",
  };

  if (gamificationLoading) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8 page-surface">
        <div className="mx-auto max-w-5xl space-y-8">
          <div className="h-8 w-48 bg-border rounded animate-pulse" />
          <div className="h-32 bg-white border border-border rounded-[16px] animate-pulse" />
          <div className="h-64 bg-white border border-border rounded-[16px] animate-pulse" />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 page-surface pb-24 md:pb-8">
      <div className="mx-auto max-w-5xl space-y-6">
        {/* Company selector + status */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="rounded-[16px] border border-border bg-white p-4 shadow-card"
        >
          <div className="flex items-center justify-between mb-3">
            <div>
              <p className="text-xs font-mono uppercase tracking-wider text-text-muted mb-1">Target</p>
              <div className="flex items-center gap-2">
                <select
                  value={targetCompany}
                  onChange={(e) => setSelectedCompany(e.target.value)}
                  className="text-sm font-bold text-text-primary bg-surface border border-border rounded-lg px-3 py-1.5"
                >
                  <option value="general">General Placement</option>
                  {companies.map((c: any) => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
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
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="h-2 flex-1 rounded-full bg-border overflow-hidden">
              <div
                className="h-full rounded-full bg-primary transition-all duration-700 ease-out"
                style={{ width: `${Math.min(100, Math.max(0, readinessScore))}%` }}
              />
            </div>
            <span className="text-xs font-bold text-text-primary">{Math.round(readinessScore)}%</span>
          </div>
          <p className="text-[11px] text-text-muted mt-1">
            {readinessLevel || "In Progress"} • Level {level}
          </p>
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
                      <span>~{mission.estimated_minutes || dailyMission?.estimated_minutes || 30} min</span>
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

        {/* Company Readiness + Blockers */}
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
            <span className="text-sm font-medium text-primary">+{Math.max(1, Math.round(readinessScore / 12))}% this week</span>
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

        {/* Quick Actions */}
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
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
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

        {/* Company shortcuts */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="rounded-[16px] p-5 sm:p-6 bg-white border border-border shadow-card"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Trophy size={18} className="text-primary" />
              <h2 className="text-lg font-bold text-text-primary">Companies</h2>
            </div>
            <Link to="/indian-placement" className="text-xs font-medium text-primary hover:underline">View all</Link>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {companies.slice(0, 6).map((co: any) => (
              <Link
                key={co.id}
                to={`/indian-placement?focus=${encodeURIComponent(co.id)}`}
                className="flex flex-col items-center gap-2 rounded-xl border border-border bg-surface p-4 transition-all hover:border-primary/30 hover:shadow-md"
              >
                <span className="text-2xl">{co.icon || "🏢"}</span>
                <span className="text-xs font-bold text-text-primary text-center">{co.name}</span>
                <span className="text-[10px] font-mono text-text-muted">{co.package || ""}</span>
              </Link>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
