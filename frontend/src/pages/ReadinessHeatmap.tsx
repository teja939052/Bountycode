import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link } from "react-router-dom";
import api from "../services/api";
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
  CheckCircle2,
  Circle,
  TrendingUp,
  TrendingDown,
  Minus,
  ExternalLink,
  ShieldCheck,
  Clock,
  Activity,
  Layers,
} from "lucide-react";
import Spinner from "../components/ui/Spinner";

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
  overall_readiness: number;
  overall: number;
  readiness_level: string;
  base_score: number;
  category_scores: Record<string, number>;
  categories: Record<string, { score: number; weight: number; details?: Record<string, any> }>;
  weak_areas_count: number;
  strong_domains_count: number;
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
  stats: Record<string, any>;
  coverage_pct: number;
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
  };
  trust_policy: Record<string, number>;
  evidence: Record<string, any>;
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

function RepairLink({ skill, company }: { skill: TargetSkill; company?: string }) {
  const label = formatLabel(skill);
  const slug = label.toLowerCase().replace(/\s+/g, "-");
  const to = `/question-bank?topic=${encodeURIComponent(slug)}`;
  return (
    <Link
      to={to}
      className="inline-flex items-center gap-2 rounded-xl border border-black/5 bg-white px-3 py-2 text-xs font-mono text-text-secondary transition-all hover:border-primary/30 hover:text-primary"
    >
      <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-amber-100 text-[10px] font-bold text-amber-700">
        <Lightbulb size={12} />
      </span>
      Repair {label}
      <ExternalLink size={10} className="opacity-60" />
    </Link>
  );
}

export default function ReadinessHeatmap() {
  const [readiness, setReadiness] = useState<ReadinessResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [company, setCompany] = useState<string>("");
  const [selectedSkill, setSelectedSkill] = useState<TargetSkill | null>(null);
  const [retesting, setRetesting] = useState(false);

  const load = useMemo(() => {
    return async () => {
      setLoading(true);
      setError(null);
      try {
        const params = company ? `?company=${encodeURIComponent(company)}` : "";
        const data = await api.adaptive.getReadinessScore(company || null);
        setReadiness(data as ReadinessResponse);
        const skills = (data as ReadinessResponse).target_readiness?.skills || [];
        if (skills.length > 0 && !selectedSkill) {
          setSelectedSkill(skills[0]);
        }
      } catch (e) {
        setError(e instanceof Error ? e.message : "Failed to load readiness");
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
          <h2 className="text-xl font-bold text-text-primary mb-2">Failed to Load Readiness</h2>
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
          <p className="text-sm text-text-muted">No readiness data yet. Complete an assessment to generate your heatmap.</p>
          <Link to="/mock-oa" className="mt-4 inline-flex items-center gap-2 btn-primary text-sm">
            Take an OA <ArrowRight size={14} />
          </Link>
        </div>
      </div>
    );
  }

  const selectedStatus = selectedSkill ? skillStatus(selectedSkill.score, selectedSkill.sufficient_evidence) : "unknown";

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
              <p className="text-[10px] font-mono uppercase tracking-widest text-primary mb-1">Readiness</p>
              <h1 className="font-display text-2xl font-black text-text-primary">
                {readiness.target_readiness?.target?.company ? `${readiness.target_readiness.target.company.toUpperCase()} ` : ""}
                Preparation
              </h1>
              <p className="text-xs text-text-muted font-mono mt-1">
                Target: {readiness.target_readiness?.target?.role || "sde"}
                {readiness.target_readiness?.target?.company ? ` · ${readiness.target_readiness.target.company}` : ""}
              </p>
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
        </motion.div>

        {/* Heatmap */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-[16px] border border-border bg-white p-5 shadow-card"
        >
          <h2 className="section-header text-lg mb-4 flex items-center gap-2">
            <Activity size={20} className="text-primary" />
            Skill Heatmap
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3">
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

        {/* Detail + Company Match + Repair */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Selected Skill Detail */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
            className="lg:col-span-2 rounded-[16px] border border-border bg-white p-5 shadow-card"
          >
            {selectedSkill ? (
              <>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="section-header text-lg flex items-center gap-2">
                    <Target size={20} className="text-primary" />
                    {formatLabel(selectedSkill)}
                  </h2>
                  <span
                    className="rounded-full border px-2 py-0.5 font-mono text-[10px] uppercase tracking-widest"
                    style={{ color: statusColor(selectedStatus), borderColor: statusColor(selectedStatus) + "40" }}
                  >
                    {selectedStatus}
                  </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
                  {Object.entries(selectedSkill.components).map(([key, value]) => (
                    <div key={key} className="rounded-xl border border-black/5 bg-surface-2 p-3">
                      <p className="text-[10px] font-mono uppercase tracking-wider text-text-muted capitalize">{key}</p>
                      <p className="font-mono text-sm font-bold text-text-primary">{Math.round(value)}%</p>
                    </div>
                  ))}
                </div>

                <div className="flex flex-wrap items-center gap-2 mb-6">
                  <Link to={`/question-bank?topic=${encodeURIComponent(formatLabel(selectedSkill).toLowerCase().replace(/\s+/g, "-"))}`} className="btn-secondary text-xs inline-flex items-center gap-2">
                    <Code2 size={12} /> Practice
                  </Link>
                  <Link to="/mock-oa" className="btn-ghost text-xs inline-flex items-center gap-2">
                    <BarChart3 size={12} /> Retest
                  </Link>
                </div>

                {nextAction && nextAction.skill_id === selectedSkill.skill_id && (
                  <div className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                    <p className="font-mono text-xs text-amber-800">
                      <strong>Next action:</strong> {nextAction.reason}
                    </p>
                  </div>
                )}
              </>
            ) : (
              <p className="text-sm text-text-muted font-mono">Select a skill to view details.</p>
            )}
          </motion.div>

          {/* Company Blueprint Match */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="rounded-[16px] border border-border bg-white p-5 shadow-card"
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
                {blockers.length > 0 && (
                  <div className="mt-3 rounded-xl border border-red-200 bg-red-50 p-3">
                    <p className="font-mono text-[10px] uppercase tracking-wider text-red-700 mb-1">Blockers</p>
                    {blockers.map((b, i) => (
                      <p key={i} className="font-mono text-[11px] text-red-800">{b.reason}</p>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <p className="text-xs text-text-muted font-mono">Select a company to see blueprint match.</p>
            )}
          </motion.div>
        </div>

        {/* Recommendations / Repair Prescription */}
        {(readiness.recommendations || []).length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
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
