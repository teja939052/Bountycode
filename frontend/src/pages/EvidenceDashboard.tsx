import { useEffect, useState, useMemo } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import api from "../services/api";
import {
  Target,
  ArrowRight,
  Lightbulb,
  Activity,
  TrendingUp,
  TrendingDown,
  Minus,
  ExternalLink,
  Layers,
  Briefcase,
  ShieldCheck,
  AlertCircle,
  RotateCw,
  Star,
  Code2,
  BarChart3,
} from "lucide-react";
import ActivityHeatmap from "../components/ActivityHeatmap";

type SkillStatus = "strong" | "developing" | "weak" | "unknown";

type TargetSkill = {
  skill_id: string;
  label: string;
  score: number;
  weight: number;
  critical: boolean;
  threshold: number;
  sufficient_evidence: boolean;
  high_stakes: boolean;
  components: Record<string, number>;
  last_evidence_at?: string;
};

type ReadinessResponse = {
  overall_readiness?: number;
  overall?: number;
  readiness_level?: string;
  coverage_pct?: number;
  target_readiness?: {
    target: { role: string; company?: string };
    score: number;
    coverage: number;
    status: string;
    skills: TargetSkill[];
    strengths: string[];
    gaps: string[];
    blockers: Array<{ skill_id: string; score: number; threshold: number; reason: string }>;
    evidence: Record<string, number>;
    freshness_pct: number;
    next_action?: { type: string; skill_id: string; reason: string };
    coverage_message?: string;
    target_weights?: Record<string, number>;
  };
  company_specific?: {
    company: string;
    score: number;
    match: {
      match_level: string;
      gaps: Array<{ area: string; required: number; current: number; gap: number }>;
      strengths: Array<{ area: string; required: number; current: number }>;
    };
  };
  recommendations: Array<{ category: string; current_score: number; priority: string; message: string }>;
};

type HeatmapDay = {
  date: string;
  total: number;
  solves?: number;
  submissions?: number;
};

type PerformanceResponse = {
  heatmap?: HeatmapDay[];
  biggest_weakness?: {
    pattern_id: string;
    label: string;
    score: number;
    attempts: number;
    success_rate: number;
  };
  why?: {
    pattern_id: string;
    label: string;
    top_failure: string;
    percentages: Record<string, number>;
  };
  improvement?: {
    pattern_id: string;
    label: string;
    trend: "improving" | "stable" | "declining";
    slope: number;
    recent_avg: number;
    older_avg: number;
  };
  failure_mix?: Record<string, number>;
  target?: {
    role: string;
    company?: string;
    score: number;
    coverage: number;
    gaps: string[];
    blockers: Array<{ skill_id: string; score: number; threshold: number; reason: string }>;
  };
  records?: {
    longest_streak?: number;
    fastest_solve_ms?: number;
    hardest_cleared?: { label: string; score: number };
  };
  next?: {
    type: string;
    skill_id?: string;
    reason: string;
  };
  generated_at?: string;
};

const LEVEL_COLORS: Record<string, string> = {
  strong: "#22c55e",
  developing: "#f59e0b",
  weak: "#ef4444",
  unknown: "#9ca3af",
};

function skillStatus(score: number, sufficient: boolean): SkillStatus {
  if (!sufficient || score === 0) return "unknown";
  if (score >= 75) return "strong";
  if (score >= 55) return "developing";
  return "weak";
}

function statusColor(status: SkillStatus) {
  return LEVEL_COLORS[status] || LEVEL_COLORS.unknown;
}

function formatLabel(skill: TargetSkill): string {
  return skill.label || skill.skill_id.split(".").pop() || skill.skill_id;
}

export default function EvidenceDashboard() {
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null);
  const [performance, setPerformance] = useState<PerformanceResponse | null>(null);
  const [heatmap, setHeatmap] = useState<HeatmapDay[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [company, setCompany] = useState<string>("");
  const [selectedSkill, setSelectedSkill] = useState<TargetSkill | null>(null);

  const load = useMemo(() => {
    return async () => {
      setLoading(true);
      setError(null);
      try {
      const [readinessData, performanceData, activityData] = await Promise.all([
          api.adaptive.getReadinessScore(company || null),
          api.evidence.getMyPerformance("sde", company || null),
          api.progress.getHeatmap(),
        ]);
        setReadiness(readinessData as unknown as ReadinessResponse);
        setPerformance(performanceData as unknown as PerformanceResponse);
        setHeatmap((activityData as any)?.heatmap || []);
        const skills = (readinessData as unknown as ReadinessResponse).target_readiness?.skills || [];
        if (skills.length > 0 && !selectedSkill) {
          setSelectedSkill(skills[0]);
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load evidence dashboard");
      } finally {
        setLoading(false);
      }
    };
  }, [company, selectedSkill]);

  useEffect(() => {
    load();
  }, [load]);

  const skills = readiness?.target_readiness?.skills || [];
  const coverage = readiness?.coverage_pct ?? readiness?.target_readiness?.coverage ?? 0;
  const overall = readiness?.overall_readiness ?? readiness?.overall ?? 0;
  const level = readiness?.readiness_level || "";
  const companyData = readiness?.company_specific;
  const nextAction = readiness?.target_readiness?.next_action;
  const blockers = readiness?.target_readiness?.blockers || [];
  const coverageMessage = readiness?.target_readiness?.coverage_message;
  const targetWeights = readiness?.target_readiness?.target_weights || {};
  const failureWhy = performance?.why;
  const improvement = performance?.improvement;
  const failureMix = performance?.failure_mix || {};

  const selectedStatus = selectedSkill ? skillStatus(selectedSkill.score, selectedSkill.sufficient_evidence) : "unknown";

  if (loading) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8 page-surface">
        <div className="mx-auto max-w-5xl space-y-6">
          <div className="h-8 w-48 bg-border rounded animate-pulse" />
          <div className="h-64 bg-white border border-border rounded-[16px] animate-pulse" />
          <div className="h-48 bg-white border border-border rounded-[16px] animate-pulse" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle size={48} className="mx-auto text-red-400 mb-4" />
          <h2 className="text-xl font-bold text-text-primary mb-2">Failed to Load Evidence</h2>
          <p className="text-sm text-text-muted mb-4">{error}</p>
          <button onClick={load} className="px-6 py-2 rounded-[10px] bg-primary text-text-primary text-sm font-medium hover:bg-primary-dark transition-colors">
            <RotateCw size={14} className="inline mr-2" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!readiness) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8 flex items-center justify-center">
        <div className="text-center">
          <p className="text-sm text-text-muted">No evidence data yet. Complete an assessment to generate your dashboard.</p>
          <Link to="/mock-oa" className="mt-4 inline-flex items-center gap-2 btn-primary text-sm">
            Take an OA <ArrowRight size={14} />
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 page-surface pb-24 md:pb-8">
      <div className="mx-auto max-w-5xl space-y-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-[16px] border border-border bg-white p-5 shadow-card"
        >
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <p className="text-[10px] font-mono uppercase tracking-widest text-primary mb-1">Evidence Dashboard</p>
              <h1 className="font-display text-2xl font-black text-text-primary">
                {readiness.target_readiness?.target?.company ? `${readiness.target_readiness.target.company.toUpperCase()} ` : ""}
                Preparation
              </h1>
              <p className="text-xs text-text-muted font-mono mt-1">
                Target: {readiness.target_readiness?.target?.role || "sde"}
                {readiness.target_readiness?.target?.company ? ` · ${readiness.target_readiness.target.company}` : ""}
              </p>
              {coverageMessage && (
                <p className="text-xs text-text-secondary font-mono mt-1">{coverageMessage}</p>
              )}
            </div>
            <div className="flex items-center gap-3">
              <select
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                className="rounded-xl border border-black/10 bg-surface-2 px-3 py-2 text-xs font-mono text-text-secondary focus:border-primary/40 focus:outline-none"
              >
                <option value="">General</option>
                <option value="tcs">TCS</option>
                <option value="infosys">Infosys</option>
                <option value="wipro">Wipro</option>
                <option value="google">Google</option>
                <option value="amazon">Amazon</option>
                <option value="microsoft">Microsoft</option>
                <option value="meta">Meta</option>
              </select>
              <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border border-border bg-surface-2">
                <div className="text-center">
                  <p className="font-display text-xl font-black" style={{ color: overall >= 75 ? "#22c55e" : overall >= 55 ? "#f59e0b" : "#ef4444" }}>
                    {Math.round(overall)}%
                  </p>
                  <p className="font-mono text-[9px] text-text-muted uppercase tracking-wider">ready</p>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-4 grid grid-cols-3 gap-3">
            <div className="rounded-xl border border-black/5 bg-surface-2 p-3">
              <p className="text-[10px] font-mono uppercase tracking-wider text-text-muted">Coverage</p>
              <p className="font-display text-lg font-black text-text-primary">{Math.round(coverage)}%</p>
            </div>
            <div className="rounded-xl border border-black/5 bg-surface-2 p-3">
              <p className="text-[10px] font-mono uppercase tracking-wider text-text-muted">Level</p>
              <p className="font-display text-lg font-black text-text-primary">{level}</p>
            </div>
            <div className="rounded-xl border border-black/5 bg-surface-2 p-3">
              <p className="text-[10px] font-mono uppercase tracking-wider text-text-muted">Evidence</p>
              <p className="font-display text-lg font-black text-text-primary">
                {readiness.target_readiness?.evidence ? Object.values(readiness.target_readiness.evidence).reduce((a: any, b: any) => a + (typeof b === 'number' ? b : 0), 0) : 0}
              </p>
            </div>
          </div>

          {nextAction && (
            <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4">
              <p className="font-mono text-xs text-amber-800">
                <strong>Next action:</strong> {nextAction.reason}
              </p>
            </div>
          )}
        </motion.div>

        {/* Activity Heatmap */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
          className="rounded-[16px] border border-border bg-white p-5 shadow-card"
        >
          <h2 className="section-header text-lg mb-4 flex items-center gap-2">
            <Activity size={20} className="text-primary" />
            Activity Heatmap
          </h2>
          {heatmap.length > 0 ? (
            <ActivityHeatmap data={heatmap as any} />
          ) : (
            <p className="text-sm text-text-muted font-mono">No activity data yet. Start solving problems to see your heatmap.</p>
          )}
          {heatmap.length > 0 && (
            <div className="mt-3 flex items-center gap-4 text-xs text-text-muted font-mono">
              <span>Less</span>
              <div className="flex gap-1">
                <div className="w-3 h-3 rounded-sm bg-gray-800" />
                <div className="w-3 h-3 rounded-sm bg-green-900" />
                <div className="w-3 h-3 rounded-sm bg-green-700" />
                <div className="w-3 h-3 rounded-sm bg-green-500" />
                <div className="w-3 h-3 rounded-sm bg-green-400" />
              </div>
              <span>More</span>
            </div>
          )}
        </motion.div>

        {/* Skill Heatmap + Detail + Company Match */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Skill Heatmap */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="lg:col-span-2 rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            <h2 className="section-header text-lg mb-4 flex items-center gap-2">
              <Target size={20} className="text-primary" />
              Skill Heatmap
            </h2>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
              {skills.map((skill) => {
                const status = skillStatus(skill.score, skill.sufficient_evidence);
                const color = statusColor(status);
                return (
                  <button
                    key={skill.skill_id}
                    onClick={() => setSelectedSkill(skill)}
                    className={`rounded-2xl border p-3 text-left transition-all ${
                      selectedSkill?.skill_id === skill.skill_id
                        ? "border-primary/40 shadow-elevated"
                        : "border-black/5 hover:border-primary/20"
                    }`}
                    style={{ backgroundColor: color + "10" }}
                  >
                    <div className="flex items-center justify-between mb-1">
                      <p className="font-display text-xs font-bold text-text-primary line-clamp-2">{formatLabel(skill)}</p>
                      {skill.critical && <Star size={10} className="text-amber-500 fill-amber-500 shrink-0" />}
                    </div>
                    <p className="font-mono text-lg font-black" style={{ color }}>
                      {Math.round(skill.score)}%
                    </p>
                    <p className="font-mono text-[10px] text-text-muted mt-0.5 capitalize">{status}</p>
                  </button>
                );
              })}
            </div>
          </motion.div>

          {/* Selected Skill Detail */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            <h3 className="font-display text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
              <Layers size={16} className="text-primary" />
              Skill Detail
            </h3>
            {selectedSkill ? (
              <div className="space-y-3">
                <div>
                  <p className="font-display text-xs font-bold text-text-primary">{formatLabel(selectedSkill)}</p>
                  <p className="font-mono text-2xl font-black" style={{ color: statusColor(selectedStatus) }}>
                    {Math.round(selectedSkill.score)}%
                  </p>
                  <p className="font-mono text-[10px] text-text-muted capitalize">{selectedStatus}</p>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(selectedSkill.components).map(([key, value]) => (
                    <div key={key} className="rounded-lg border border-black/5 bg-surface-2 p-2">
                      <p className="text-[10px] font-mono uppercase tracking-wider text-text-muted capitalize">{key}</p>
                      <p className="font-mono text-sm font-bold text-text-primary">{Math.round(value)}%</p>
                    </div>
                  ))}
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <Link to={`/question-bank?topic=${encodeURIComponent(formatLabel(selectedSkill).toLowerCase().replace(/\s+/g, "-"))}`} className="btn-secondary text-xs inline-flex items-center gap-2">
                    <Code2 size={12} /> Practice
                  </Link>
                  <Link to="/mock-oa" className="btn-ghost text-xs inline-flex items-center gap-2">
                    <BarChart3 size={12} /> Retest
                  </Link>
                </div>
              </div>
            ) : (
              <p className="text-sm text-text-muted font-mono">Select a skill to view details.</p>
            )}
          </motion.div>
        </div>

        {/* Failure Breakdown + Improvement */}
        <div className="grid gap-6 lg:grid-cols-2">
          {/* Failure Breakdown */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            <h3 className="font-display text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
              <AlertCircle size={16} className="text-red-500" />
              Why You Fail
            </h3>
            {failureWhy ? (
              <div className="space-y-3">
                <div>
                  <p className="font-mono text-xs text-text-muted">Biggest weakness</p>
                  <p className="font-display text-sm font-bold text-text-primary">{failureWhy.label || failureWhy.pattern_id}</p>
                </div>
                <div>
                  <p className="font-mono text-xs text-text-muted mb-1">Failure mix</p>
                  <div className="space-y-1">
                    {Object.entries(failureMix).map(([reason, pct]) => (
                      <div key={reason} className="flex items-center justify-between">
                        <span className="font-mono text-[11px] text-text-secondary capitalize">{reason}</span>
                        <span className="font-mono text-[11px] font-bold text-text-primary">{Math.round(pct as number)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-sm text-text-muted font-mono">Complete more problems to see failure patterns.</p>
            )}
          </motion.div>

          {/* Improvement Trend */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.25 }}
            className="rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            <h3 className="font-display text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
              <TrendingUp size={16} className="text-primary" />
              Improvement Trend
            </h3>
            {improvement ? (
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  {improvement.trend === "improving" && <TrendingUp size={16} className="text-green-500" />}
                  {improvement.trend === "declining" && <TrendingDown size={16} className="text-red-500" />}
                  {improvement.trend === "stable" && <Minus size={16} className="text-amber-500" />}
                  <span className="font-mono text-xs text-text-muted capitalize">{improvement.trend}</span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-xl border border-black/5 bg-surface-2 p-3">
                    <p className="text-[10px] font-mono uppercase tracking-wider text-text-muted">Recent avg</p>
                    <p className="font-mono text-sm font-bold text-text-primary">{Math.round(improvement.recent_avg)}%</p>
                  </div>
                  <div className="rounded-xl border border-black/5 bg-surface-2 p-3">
                    <p className="text-[10px] font-mono uppercase tracking-wider text-text-muted">Older avg</p>
                    <p className="font-mono text-sm font-bold text-text-primary">{Math.round(improvement.older_avg)}%</p>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-sm text-text-muted font-mono">Solve more problems to see your trend.</p>
            )}
          </motion.div>
        </div>

        {/* Company Match + Blockers */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Company Blueprint Match */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="lg:col-span-2 rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            <h3 className="font-display text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
              <Briefcase size={16} className="text-primary" />
              Company Match
            </h3>
            {companyData ? (
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-xs text-text-muted">{companyData.company.toUpperCase()}</span>
                  <span className="font-mono text-sm font-bold" style={{ color: companyData.score >= 70 ? "#22c55e" : "#ef4444" }}>
                    {Math.round(companyData.score)}%
                  </span>
                </div>
                <div className="space-y-2">
                  {(companyData.match.gaps || []).slice(0, 5).map((g, i) => (
                    <div key={i} className="flex items-center justify-between rounded-lg border border-red-100 bg-red-50 px-2 py-1.5">
                      <span className="font-mono text-[11px] text-text-secondary capitalize">{g.area}</span>
                      <span className="font-mono text-[11px] text-red-600">-{Math.round(g.gap)}</span>
                    </div>
                  ))}
                  {(companyData.match.strengths || []).slice(0, 5).map((s, i) => (
                    <div key={i} className="flex items-center justify-between rounded-lg border border-emerald-100 bg-emerald-50 px-2 py-1.5">
                      <span className="font-mono text-[11px] text-text-secondary capitalize">{s.area}</span>
                      <span className="font-mono text-[11px] text-emerald-600">+{Math.round(s.current - s.required)}</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <p className="text-xs text-text-muted font-mono">Select a company to see blueprint match.</p>
            )}
          </motion.div>

          {/* Blockers */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.35 }}
            className="rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            <h3 className="font-display text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
              <ShieldCheck size={16} className="text-red-500" />
              Blockers
            </h3>
            {blockers.length > 0 ? (
              <div className="space-y-2">
                {blockers.map((b, i) => (
                  <div key={i} className="rounded-xl border border-red-200 bg-red-50 p-3">
                    <p className="font-mono text-[11px] text-red-800">{b.reason}</p>
                    <p className="font-mono text-[10px] text-red-600 mt-1">
                      {b.skill_id}: {Math.round(b.score)}% / {Math.round(b.threshold)}%
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-text-muted font-mono">No blockers. Keep it up!</p>
            )}
          </motion.div>
        </div>

        {/* Target Weights */}
        {Object.keys(targetWeights).length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            <h3 className="font-display text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
              <Layers size={16} className="text-primary" />
              Target Weights
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
              {Object.entries(targetWeights).map(([skill, weight]) => (
                <div key={skill} className="flex items-center justify-between rounded-xl border border-black/5 bg-surface-2 px-3 py-2">
                  <span className="font-mono text-[11px] text-text-secondary capitalize">{skill.replace(/^role:/, "")}</span>
                  <span className="font-mono text-[11px] font-bold text-text-primary">{Math.round(weight * 100)}%</span>
                </div>
              ))}
            </div>
          </motion.div>
        )}

        {/* Recommendations */}
        {(readiness.recommendations || []).length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.45 }}
            className="rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            <h3 className="font-display text-sm font-bold text-text-primary mb-3 flex items-center gap-2">
              <Lightbulb size={16} className="text-amber-500" />
              Repair Prescription
            </h3>
            <div className="grid gap-2 sm:grid-cols-2">
              {readiness.recommendations.slice(0, 6).map((rec, i) => (
                <Link
                  key={i}
                  to={`/question-bank?topic=${encodeURIComponent(rec.category.toLowerCase().replace(/\s+/g, "-"))}`}
                  className="flex items-center gap-2 rounded-xl border border-black/5 bg-surface-2 px-3 py-2.5 text-xs font-mono text-text-secondary transition-all hover:border-primary/30 hover:text-primary"
                >
                  <span className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-[10px] font-bold ${
                    rec.priority === "high" ? "bg-red-100 text-red-700" :
                    rec.priority === "medium" ? "bg-amber-100 text-amber-700" :
                    "bg-emerald-100 text-emerald-700"
                  }`}>
                    {rec.priority === "high" ? "!" : rec.priority === "medium" ? "~" : "✓"}
                  </span>
                  {rec.message}
                  <ExternalLink size={10} className="ml-auto opacity-60" />
                </Link>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
}
