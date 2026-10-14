// @ts-nocheck
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  User,
  Flame,
  Trophy,
  ArrowRight,
  Crown,
  Zap,
  Shield,
  BookOpen,
  Code2,
  Stethoscope,
  LayoutTemplate,
  PenLine,
  BarChart3,
  MessageSquare,
  Lock,
  CheckCircle2,
  XCircle,
  Timer,
  Target,
  Rocket,
} from "lucide-react";
import { motion } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import { ProgressBar } from "../design-system/components/ProgressBar";

const FADE_UP = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.35 },
};

const STAGGER = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.3 },
};

const tierConfig = {
  free: {
    label: "Cadet",
    accent: "bg-gray-500",
    textAccent: "text-gray-400",
    border: "border-gray-500/30",
    glow: "",
    icon: Shield,
  },
  pro: {
    label: "Commander",
    accent: "bg-cyber-blue",
    textAccent: "text-cyber-blue",
    border: "border-cyber-blue/40",
    glow: "shadow-[0_0_40px_-12px_rgba(56,189,248,0.35)]",
    icon: Crown,
  },
  lifetime: {
    label: "Admiral",
    accent: "bg-purple-500",
    textAccent: "text-purple-400",
    border: "border-purple-500/40",
    glow: "shadow-[0_0_40px_-12px_rgba(168,85,247,0.35)]",
    icon: Crown,
  },
  trial: {
    label: "Pro Trial",
    accent: "bg-emerald-500",
    textAccent: "text-emerald-400",
    border: "border-emerald-500/40",
    glow: "shadow-[0_0_40px_-12px_rgba(16,185,129,0.35)]",
    icon: Zap,
  },
};

function daysLeftText(days) {
  if (days === null || days === undefined) return null;
  if (days <= 0) return "Expired";
  if (days < 1) return "Less than 1 day";
  if (days === 1) return "1 day left";
  return `${Math.round(days)} days left`;
}

function usageBar(used, limit) {
  if (!limit || limit === "unlimited") return null;
  const safeLimit = Number(limit);
  const safeUsed = Math.min(Number(used || 0), safeLimit);
  const pct = Math.round((safeUsed / safeLimit) * 100);
  return { used: safeUsed, limit: safeLimit, pct };
}

function usageColor(pct) {
  if (pct >= 90) return "warning";
  if (pct >= 70) return "info";
  return "success";
}

export default function Profile() {
  const { user } = useAuthStore();
  const [profile, setProfile] = useState(null);
  const [features, setFeatures] = useState(null);
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Prep target editor. `/company-select` was the intended home for this but was
  // never implemented; the write path (gamification/profile/target-company) has
  // always existed, so the editor lives here instead.
  const [companies, setCompanies] = useState<string[]>([]);
  const [targetCompany, setTargetCompany] = useState("");
  const [savingTarget, setSavingTarget] = useState(false);
  const [targetMsg, setTargetMsg] = useState<{ tone: "ok" | "err"; text: string } | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const res = await api.companyMocks?.getCompanies?.();
        if (alive) setCompanies(Array.isArray(res?.companies) ? res.companies : []);
      } catch {
        // The list is a convenience only — free text is always accepted.
      }
    })();
    return () => { alive = false; };
  }, []);

  // Seed the field once the profile lands, without clobbering live edits.
  useEffect(() => {
    const current = profile?.user?.target_company;
    if (current && !targetCompany) setTargetCompany(current);
  }, [profile, targetCompany]);

  const saveTargetCompany = async () => {
    const company = targetCompany.trim();
    if (!company) {
      setTargetMsg({ tone: "err", text: "Pick a company first." });
      return;
    }
    setSavingTarget(true);
    setTargetMsg(null);
    try {
      const res = await api.gamification.setTargetCompany(company);
      const saved = res?.target_company || company;
      setTargetCompany(saved);
      // Re-read the profile and the auth user so the campaign, today's plan and
      // readiness all pick up the new target without a manual reload.
      const fresh = await api.account?.getProfile?.();
      if (fresh) setProfile((prev) => ({ ...(prev || {}), ...fresh }));
      await useAuthStore.getState().loadUser();
      setTargetMsg({ tone: "ok", text: `Target set to ${saved}.` });
    } catch (err) {
      setTargetMsg({ tone: "err", text: err?.message || "Could not save your target." });
    } finally {
      setSavingTarget(false);
    }
  };

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const [p, f, pl] = await Promise.all([
          api.account?.getProfile?.(),
          api.account?.getFeatures?.(),
          api.account?.getPlan?.(),
        ]);
        if (!alive) return;
        setProfile(p || null);
        setFeatures(f || null);
        setPlan(pl || null);
      } catch (err) {
        if (alive) setError(err.message || "Failed to load profile");
      } finally {
        if (alive) setLoading(false);
      }
    })();
    return () => { alive = false; };
  }, []);

  const planKey = plan?.plan || user?.plan || "free";
  const tier = profile?.user?.tier || plan?.tier || "free";
  const cfg = tierConfig[tier] || tierConfig.free;
  const TierIcon = cfg.icon;
  const isPro = tier === "pro" || tier === "lifetime";
  const daysRemaining = profile?.plan?.days_remaining ?? plan?.days_remaining ?? null;
  const isTrial = profile?.plan?.is_trial || false;
  const planName = profile?.plan?.name || cfg.label;
  const planDesc = profile?.plan?.desc || "";
  const highlights = profile?.plan?.highlights || [];
  const upgradeRecommended = profile?.upgrade_recommended || false;
  const upgradeMessage = profile?.upgrade_message || "";

  const usageItems = profile?.usage
    ? [
        { id: "interviews", label: "AI Interviews", used: profile.usage.interviews_used, limit: profile.usage.interviews_limit, icon: MessageSquare },
        { id: "resumes", label: "Resume Reviews", used: profile.usage.resumes_used, limit: profile.usage.resumes_limit, icon: FileTextIcon },
        { id: "aptitude", label: "Aptitude Tests", used: profile.usage.aptitude_used, limit: profile.usage.aptitude_limit, icon: Target },
        { id: "company_mocks", label: "Company Mocks", used: profile.usage.company_mocks_used, limit: profile.usage.company_mocks_limit, icon: Building2 },
        { id: "predictions", label: "Predictions", used: profile.usage.predictions_used, limit: profile.usage.predictions_limit, icon: BarChart3 },
        { id: "question_bank", label: "Question Bank", used: profile.usage.question_bank_used, limit: profile.usage.question_bank_limit, icon: BookOpen },
      ]
    : [];

  const featureItems = features?.features || [];
  const categories = Array.from(new Set(featureItems.map((f) => f.category).filter(Boolean)));

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 pb-24 md:pb-8">
      <div className="mx-auto max-w-5xl space-y-6">
        {error && (
          <motion.div {...FADE_UP} className="rounded-xl border border-cyber-red/30 bg-cyber-red/10 px-4 py-3 text-sm text-cyber-red font-mono">
            {error}
          </motion.div>
        )}

        {loading ? (
          <div className="grid gap-4 md:grid-cols-2">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-40 rounded-2xl border border-border bg-white/60 animate-pulse" />
            ))}
          </div>
        ) : (
          <>
            {/* Hero profile card */}
            <motion.div {...FADE_UP} className={`rounded-2xl border ${cfg.border} bg-white p-6 shadow-card ${cfg.glow}`}>
              <div className="flex flex-col md:flex-row md:items-center gap-4">
                <div className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl ${cfg.accent} text-space-void`}>
                  <User size={22} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <h1 className="font-display text-2xl font-black text-text-primary">{profile?.user?.name || user?.name || "Cadet"}</h1>
                    <span className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-[10px] font-mono uppercase tracking-widest ${cfg.accent} ${cfg.textAccent}`}>
                      <TierIcon size={10} />
                      {planName}
                    </span>
                    {isTrial && (
                      <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2.5 py-1 text-[10px] font-mono text-emerald-400 border border-emerald-500/30">
                        <Zap size={10} /> Trial
                      </span>
                    )}
                  </div>
                  <p className="mt-1 text-xs text-text-muted font-mono">{profile?.user?.email || user?.email}</p>
                  <div className="mt-2 flex flex-wrap items-center gap-3 text-[11px] font-mono text-text-secondary">
                    <span className="flex items-center gap-1"><Target size={12} /> {profile?.user?.target_role || "Role"}</span>
                    <span className="flex items-center gap-1"><Building2 size={12} /> {profile?.user?.target_company || "Target company"}</span>
                    {daysRemaining !== null && daysRemaining !== undefined && (
                      <span className={`flex items-center gap-1 ${daysRemaining <= 2 ? "text-amber-400" : ""}`}>
                        <Timer size={12} /> {daysLeftText(daysRemaining)}
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex flex-col gap-2 md:text-right">
                  {upgradeRecommended && (
                    <Link to="/pricing" className="btn-primary text-xs inline-flex items-center justify-center gap-2">
                      Upgrade <ArrowRight size={12} />
                    </Link>
                  )}
                  <Link to="/settings" className="btn-secondary text-xs inline-flex items-center justify-center">Settings</Link>
                </div>
              </div>

              {highlights.length > 0 && (
                <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {highlights.slice(0, 6).map((h) => (
                    <span key={h} className="flex items-start gap-2 text-xs text-text-secondary">
                      <CheckCircle2 size={12} className="mt-0.5 text-cyber-green shrink-0" />
                      <span>{h}</span>
                    </span>
                  ))}
                </div>
              )}

              {upgradeRecommended && upgradeMessage && (
                <p className="mt-3 text-xs text-text-muted font-mono">{upgradeMessage}</p>
              )}
            </motion.div>

            {/* Prep target */}
            <motion.section {...FADE_UP} className="rounded-2xl border border-border bg-white p-6 shadow-card">
              <div className="mb-4 flex items-center gap-2">
                <Target size={16} className="text-primary" />
                <h2 className="font-display text-lg font-black text-text-primary">Prep target</h2>
                <span className="text-[10px] font-mono text-text-muted uppercase tracking-widest">Drives your plan</span>
              </div>

              <p className="text-xs text-text-secondary">
                Your target company decides which patterns, mocks and interview prep BountyCode
                serves you.
              </p>

              <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center">
                <input
                  list="bountycode-companies"
                  value={targetCompany}
                  onChange={(e) => { setTargetCompany(e.target.value); setTargetMsg(null); }}
                  placeholder="e.g. TCS"
                  aria-label="Target company"
                  className="min-h-[44px] w-full rounded-xl border border-black/10 bg-white px-3 text-sm text-text-primary outline-none focus:border-primary sm:max-w-xs"
                />
                <datalist id="bountycode-companies">
                  {companies.map((c) => <option key={c} value={c} />)}
                </datalist>
                <button
                  onClick={saveTargetCompany}
                  disabled={savingTarget}
                  className="btn-primary text-sm inline-flex min-h-[44px] items-center justify-center disabled:opacity-50"
                >
                  {savingTarget ? "Saving..." : "Save target"}
                </button>
              </div>

              {targetMsg && (
                <p className={`mt-2 text-xs font-mono ${targetMsg.tone === "ok" ? "text-cyber-green" : "text-red-600"}`}>
                  {targetMsg.text}
                </p>
              )}

              {!profile?.user?.target_company && !targetMsg && (
                <p className="mt-2 text-xs font-mono text-amber-600">
                  No target set - your plan falls back to generic prep.
                </p>
              )}
            </motion.section>

            {/* Usage grid */}
            {usageItems.length > 0 && (
              <motion.section {...FADE_UP} className="rounded-2xl border border-border bg-white p-6 shadow-card">
                <div className="mb-4 flex items-center gap-2">
                  <BarChart3 size={16} className="text-primary" />
                  <h2 className="font-display text-lg font-black text-text-primary">Usage</h2>
                  <span className="text-[10px] font-mono text-text-muted uppercase tracking-widest">Monthly</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {usageItems.map((item) => {
                    const bar = usageBar(item.used, item.limit);
                    const ItemIcon = item.icon;
                    return (
                      <div key={item.id} className="rounded-xl border border-black/5 bg-surface-2 p-4">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-space-panel border border-space-border text-text-secondary">
                              <ItemIcon size={14} />
                            </div>
                            <div>
                              <p className="text-xs font-medium text-text-primary">{item.label}</p>
                              <p className="text-[10px] font-mono text-text-muted">
                                {bar ? `${item.used} / ${item.limit}` : "Unlimited"}
                              </p>
                            </div>
                          </div>
                          {bar && (
                            <span className="text-[10px] font-mono text-text-muted">{bar.pct}%</span>
                          )}
                        </div>
                        {bar && (
                          <div className="mt-3">
                            <ProgressBar value={bar.used} max={bar.limit} size="sm" color={usageColor(bar.pct)} showLabel />
                          </div>
                        )}
                        {!bar && (
                          <div className="mt-3">
                            <span className="inline-flex items-center gap-1 rounded-full bg-cyber-green/10 px-2 py-1 text-[10px] font-mono text-cyber-green border border-cyber-green/20">
                              <CheckCircle2 size={10} /> Unlimited
                            </span>
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </motion.section>
            )}

            {/* Features grid */}
            {featureItems.length > 0 && (
              <motion.section {...FADE_UP} className="rounded-2xl border border-border bg-white p-6 shadow-card">
                <div className="mb-4 flex items-center gap-2">
                  <Rocket size={16} className="text-primary" />
                  <h2 className="font-display text-lg font-black text-text-primary">Features</h2>
                  <span className="text-[10px] font-mono text-text-muted uppercase tracking-widest">Access by tier</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {featureItems.map((feature) => {
                    const available = feature.available !== false;
                    const proRequired = feature.pro_required === true;
                    const limits = feature.limits || {};
                    const currentLimit = limits[planKey] || limits[tier] || limits.free || "—";
                    return (
                      <div key={feature.id} className={`rounded-xl border p-4 ${available ? "border-black/5 bg-surface-2" : "border-amber-500/20 bg-amber-500/5"}`}>
                        <div className="flex items-start justify-between gap-2">
                          <div>
                            <p className="text-xs font-medium text-text-primary">{feature.name}</p>
                            <p className="text-[11px] font-mono text-text-muted mt-1 line-clamp-2">{feature.description}</p>
                          </div>
                          {available ? (
                            <CheckCircle2 size={14} className="text-cyber-green shrink-0 mt-0.5" />
                          ) : (
                            <Lock size={14} className="text-amber-400 shrink-0 mt-0.5" />
                          )}
                        </div>
                        <div className="mt-3 flex items-center justify-between">
                          <span className={`text-[10px] font-mono ${available ? "text-text-secondary" : "text-amber-400"}`}>
                            {String(currentLimit)}
                          </span>
                          {!available && (
                            <Link to="/pricing" className="text-[10px] font-mono text-cyber-blue hover:underline inline-flex items-center gap-1">
                              Upgrade <ArrowRight size={10} />
                            </Link>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </motion.section>
            )}

            {/* Quick links */}
            <motion.div {...FADE_UP} className="rounded-2xl border border-border bg-white p-5 shadow-card flex flex-wrap gap-2">
              <Link to="/history" className="btn-secondary text-xs">History</Link>
              <Link to="/settings" className="btn-secondary text-xs">Settings</Link>
              <Link to="/leaderboard" className="btn-secondary text-xs">Leaderboard</Link>
              <Link to="/pricing" className="btn-primary text-xs inline-flex items-center gap-2">
                {isPro ? "Manage Plan" : "Upgrade"} <ArrowRight size={12} />
              </Link>
            </motion.div>
          </>
        )}
      </div>
    </div>
  );
}

function FileTextIcon(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
      <polyline points="10 9 9 9 8 9" />
    </svg>
  );
}

function Building2(props) {
  return (
    <svg viewBox="0 0 24 24" width="1em" height="1em" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z" />
      <path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2" />
      <path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2" />
      <path d="M10 12h4" />
      <path d="M10 16h4" />
      <path d="M10 8h4" />
    </svg>
  );
}
