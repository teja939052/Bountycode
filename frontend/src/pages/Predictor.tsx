import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import { TrendingUp, Target, Brain, ChevronDown, BarChart3, Zap, Building2, Flame, CheckCircle, XCircle, Hourglass, Trash2 } from "lucide-react";
import AnimatedCard from "../components/motion/AnimatedCard";
import PredictorGauge from "../components/PredictorGauge";
import useReducedMotion from "../hooks/useReducedMotion";

const OUTCOME_META: Record<string, { label: string; icon: any; color: string }> = {
  offered: { label: "Offered", icon: CheckCircle, color: "text-emerald-500" },
  rejected: { label: "Rejected", icon: XCircle, color: "text-red-500" },
  in_process: { label: "In process", icon: Hourglass, color: "text-amber-500" },
};

const FACTOR_VERDICT_STYLE: Record<string, string> = {
  strong: "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300",
  on_track: "bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300",
  gap: "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300",
  critical: "bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300",
};

export default function Predictor() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [role, setRole] = useState("SDE");
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [companiesLoading, setCompaniesLoading] = useState(true);
  const [history, setHistory] = useState([]);
  const [practiceResult, setPracticeResult] = useState(null);
  const [practicing, setPracticing] = useState(false);
  const [outcomes, setOutcomes] = useState<any[]>([]);
  const [outcomeStats, setOutcomeStats] = useState<any>(null);
  const [outcomeForm, setOutcomeForm] = useState({ outcome: "offered", notes: "" });
  const [savingOutcome, setSavingOutcome] = useState(false);
  const [timeToOffer, setTimeToOffer] = useState<any>(null);
  const [timeToOfferLoading, setTimeToOfferLoading] = useState(false);
  const reduced = useReducedMotion();

  useEffect(() => {
    const load = async () => {
      try {
        const data = await api.getSupportedCompanies();
        setCompanies(data.companies || data || []);
      } catch {} finally {
        setCompaniesLoading(false);
      }
      try {
        const h = await api.getPredictionHistory();
        setHistory(h.predictions || h || []);
      } catch {}
      try {
        const o = await api.getOutcomes();
        setOutcomes(o.outcomes || []);
      } catch {}
      try {
        const s = await api.getOutcomeStats();
        setOutcomeStats(s);
      } catch {}
    };
    load();
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    if (!selectedCompany) return;
    setLoading(true);
    try {
      const data = await api.predictOffer(selectedCompany, role);
      setPrediction(data);
    } catch {} finally {
      setLoading(false);
    }
  };

  const handleTimeToOffer = async () => {
    const target = selectedCompany || prediction?.target_company || prediction?.company;
    if (!target) return;
    setTimeToOfferLoading(true);
    try {
      const data = await api.timeToOffer(target, role);
      setTimeToOffer(data);
    } catch {} finally {
      setTimeToOfferLoading(false);
    }
  };

  const handlePracticeForRole = async () => {
    if (!selectedCompany) return;
    setPracticing(true);
    setPracticeResult(null);
    try {
      const data = await api.createPracticeSession({ company: selectedCompany, role });
      setPracticeResult(data);
    } catch {} finally {
      setPracticing(false);
    }
  };

  const handleRecordOutcome = async (e: any) => {
    e.preventDefault();
    if (!prediction) return;
    setSavingOutcome(true);
    try {
      const company = selectedCompany || prediction.company || prediction.target_company;
      const res = await api.recordOutcome({
        company,
        role,
        predicted_probability: probability,
        factors: prediction.factors,
        confidence_band: prediction.confidence_band,
        outcome: outcomeForm.outcome,
        notes: outcomeForm.notes || null,
      });
      setOutcomes((prev) => [
        { id: res.outcome_id, company: res.company, role: res.role, outcome: res.outcome, predicted_probability: res.predicted_probability, notes: outcomeForm.notes },
        ...prev,
      ]);
      setOutcomeForm({ outcome: "offered", notes: "" });
    } catch {} finally {
      setSavingOutcome(false);
    }
  };

  const handleDeleteOutcome = async (id: string) => {
    try {
      await api.deleteOutcome(id);
      setOutcomes((prev) => prev.filter((o) => o.id !== id));
    } catch {}
  };

  const probability = prediction?.probability || prediction?.placement_probability || 0;

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-10"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="w-16 h-16 bg-emerald-100 dark:bg-emerald-900/30 rounded-full flex items-center justify-center mx-auto mb-4">
            <TrendingUp size={32} className="text-emerald-600" />
          </div>
          <h1 className="text-3xl font-bold dark:text-white">Placement Predictor</h1>
          <p className="text-brand-secondary dark:text-gray-400 mt-2">Predict your offer based on skills and company tier</p>
        </motion.div>

        <AnimatedCard className="card mb-8">
          <form onSubmit={handlePredict}>
            <div className="grid md:grid-cols-2 gap-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-brand-primary dark:text-gray-300 mb-1">Company</label>
                <div className="relative">
                  <Building2 size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                  <select
                    value={selectedCompany}
                    onChange={(e) => setSelectedCompany(e.target.value)}
                    className="w-full pl-10 pr-10 py-3 border border-brand-primary/20 border-brand-primary/15 rounded-lg focus:ring-2 focus:ring-primary-500 appearance-none bg-surface-card bg-surface-card dark:text-white"
                    required
                  >
                    <option value="">{companiesLoading ? "Loading..." : "Select company"}</option>
                    {companies.map((c) => (
                      <option key={c.name || c} value={c.name || c}>{c.name || c}</option>
                    ))}
                  </select>
                  <ChevronDown size={18} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none" />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-brand-primary dark:text-gray-300 mb-1">Role</label>
                <div className="relative">
                  <Target size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                  <input
                    type="text"
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                    placeholder="e.g., SDE, Data Scientist"
                    className="w-full pl-10 pr-4 py-3 border border-brand-primary/20 border-brand-primary/15 rounded-lg focus:ring-2 focus:ring-primary-500 bg-surface-card bg-surface-card dark:text-white"
                  />
                </div>
              </div>
            </div>
            <button
              type="submit"
              disabled={loading || !selectedCompany}
              className="w-full bg-primary-600 text-white py-3 rounded-lg font-bold hover:bg-primary-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
            >
              {loading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
              ) : (
                <>
                  <Zap size={18} />
                  Predict My Offer
                </>
              )}
            </button>
          </form>
        </AnimatedCard>

        {/* Results with Gauge */}
        <AnimatePresence>
          {prediction && (
            <motion.div
              className="space-y-6"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
               {/* Probability Gauge */}
               {probability > 0 && (
                <AnimatedCard className="card flex justify-center">
                  <PredictorGauge probability={probability} band={prediction.confidence_band} />
                </AnimatedCard>
              )}

              {prediction.what_it_means && (
                <AnimatedCard className="card">
                  <h3 className="font-bold mb-2 flex items-center gap-2">
                    <Brain size={20} className="text-primary-600" />
                    What this means
                  </h3>
                  <p className="text-sm text-brand-secondary dark:text-gray-300 leading-relaxed">
                    {prediction.what_it_means}
                  </p>
                  {prediction.confidence_band?.note && (
                    <p className="text-xs text-brand-muted dark:text-gray-500 mt-2">
                      {prediction.confidence_band.note}
                    </p>
                  )}
                </AnimatedCard>
              )}

              {prediction.factors?.length > 0 && (
                <AnimatedCard className="card">
                  <h3 className="font-bold mb-4 flex items-center gap-2">
                    <BarChart3 size={20} className="text-primary-600" />
                    Why {probability}% — factor by factor
                  </h3>
                  {prediction.role_profile && (
                    <p className="text-xs text-brand-muted dark:text-gray-500 mb-4">
                      Weights tuned for <span className="font-semibold text-primary-600">{prediction.role_profile}</span>
                      {prediction.role ? ` (${prediction.role})` : ""} — DSA carries more weight for SDEs, behavioral for PMs.
                    </p>
                  )}
                  <div className="space-y-4">
                    {prediction.factors.map((f: any) => (
                      <div key={f.key} className="border border-brand-primary/10 rounded-lg p-3">
                        <div className="flex items-center justify-between mb-1.5 gap-2 flex-wrap">
                          <div className="flex items-center gap-2 min-w-0">
                            <span className="font-semibold text-sm dark:text-white">{f.label}</span>
                            <span className={`text-[10px] font-bold uppercase px-1.5 py-0.5 rounded ${FACTOR_VERDICT_STYLE[f.verdict] || FACTOR_VERDICT_STYLE.gap}`}>
                              {f.verdict.replace("_", " ")}
                            </span>
                          </div>
                          <span className="text-sm font-bold text-primary-600">{f.score}<span className="text-xs text-brand-muted">/100</span></span>
                        </div>
                        <div className="w-full bg-surface-card/50 dark:bg-gray-700 rounded-full h-2 overflow-hidden mb-1.5">
                          <motion.div
                            className={`h-2 rounded-full ${f.verdict === "critical" ? "bg-red-500" : f.verdict === "gap" ? "bg-amber-500" : f.verdict === "on_track" ? "bg-sky-500" : "bg-emerald-500"}`}
                            initial={reduced ? { width: `${f.score}%` } : { width: 0 }}
                            whileInView={{ width: `${f.score}%` }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.7 }}
                          />
                        </div>
                        <p className="text-xs text-brand-secondary dark:text-gray-400 mb-1">
                          {f.message} Weight {Math.round(f.weight * 100)}% · {f.contribution_pct}% of your score
                        </p>
                        <p className="text-xs text-brand-muted dark:text-gray-500">
                          Fix: {f.how_to_improve}
                        </p>
                      </div>
                    ))}
                  </div>
                </AnimatedCard>
              )}

              <div className="card bg-gradient-to-r from-primary-600 to-primary-700 text-white">
                <div className="text-center">
                  <p className="text-primary-100 mb-1">Predicted CTC</p>
                  <p className="text-5xl font-bold mb-2">
                    ₹{(prediction.predicted_ctc || prediction.salary || 0).toLocaleString("en-IN")}
                  </p>
                  <p className="text-primary-200 text-sm">
                    {prediction.range_min && prediction.range_max
                      ? `Range: ₹${prediction.range_min.toLocaleString("en-IN")} — ₹${prediction.range_max.toLocaleString("en-IN")}`
                      : "Based on your skills and company tier"}
                  </p>
                </div>
              </div>

              {prediction.skill_scores && (
                <AnimatedCard className="card">
                  <h3 className="font-bold mb-4 flex items-center gap-2">
                    <Brain size={20} className="text-primary-600" />
                    Skill Assessment
                  </h3>
                  <div className="space-y-3">
                    {Object.entries(prediction.skill_scores).map(([skill, score]: [string, any], i) => (
                      <div key={skill}>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="capitalize text-brand-secondary dark:text-gray-400">{skill.replace(/_/g, " ")}</span>
                          <span className="font-medium dark:text-white">{score}/100</span>
                        </div>
                        <div className="w-full bg-surface-card/50 dark:bg-gray-700 rounded-full h-2 overflow-hidden">
                          <motion.div
                             className={`h-2 rounded-full ${Number(score) >= 80 ? "bg-green-500" : Number(score) >= 50 ? "bg-yellow-500" : "bg-red-500"}`}
                             initial={reduced ? { width: `${Number(score)}%` } : { width: 0 }}
                             whileInView={{ width: `${Number(score)}%` }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.6, delay: i * 0.1 }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </AnimatedCard>
              )}

              {!practiceResult && (
                <div className="text-center">
                  <button
                    onClick={handlePracticeForRole}
                    disabled={practicing || !selectedCompany}
                    className="btn-primary inline-flex items-center gap-2"
                  >
                    {practicing ? (
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                    ) : (
                      <><Flame size={18} /> Practice for This Role</>
                    )}
                  </button>
                </div>
              )}
              {practiceResult && (
                <AnimatedCard className="card bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 border border-emerald-200 dark:border-emerald-800">
                  <h3 className="font-bold mb-2 dark:text-white">Practice Session Ready</h3>
                  <p className="text-sm text-brand-secondary dark:text-gray-400 mb-3">
                    {practiceResult.company} · {practiceResult.role}
                  </p>
                  <div className="flex flex-wrap gap-4 text-sm text-brand-primary dark:text-gray-300 mb-4">
                    <span>Coding: {practiceResult.coding?.length || 0}</span>
                    <span>Behavioral: {practiceResult.behavioral?.length || 0}</span>
                    <span>System Design: {practiceResult.system_design?.length || 0}</span>
                  </div>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-brand-secondary dark:text-gray-400">Probability: {practiceResult.probability_before}% → {practiceResult.probability_after_target}%</span>
                  </div>
                </AnimatedCard>
              )}

              {prediction.next_best_moves?.length > 0 && (
                <AnimatedCard className="card">
                  <h3 className="font-bold mb-3 flex items-center gap-2">
                    <Zap size={20} className="text-primary-600" />
                    Your best moves
                  </h3>
                  <div className="space-y-3">
                    {prediction.next_best_moves.map((move: any, i: number) => (
                      <div key={move.id || i} className="flex items-start gap-3">
                        <div className="w-7 h-7 rounded-full bg-primary-100 dark:bg-primary-900/40 text-primary-700 dark:text-primary-300 text-xs font-bold flex items-center justify-center shrink-0 mt-0.5">
                          {i + 1}
                        </div>
                        <div className="min-w-0">
                          <p className="text-sm font-semibold dark:text-white">{move.title}</p>
                          <p className="text-xs text-brand-secondary dark:text-gray-400 mt-0.5">{move.description}</p>
                          <div className="flex flex-wrap gap-2 mt-1.5 text-[11px]">
                            <span className="px-2 py-0.5 bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 rounded-full font-semibold">
                              +{move.projected_gain}%
                            </span>
                            <span className="px-2 py-0.5 bg-surface-card/70 dark:bg-gray-700 text-brand-secondary dark:text-gray-300 rounded-full">
                              {move.effort} effort
                            </span>
                            {move.time_estimate && (
                              <span className="px-2 py-0.5 bg-surface-card/70 dark:bg-gray-700 text-brand-secondary dark:text-gray-300 rounded-full">
                                {move.time_estimate}
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </AnimatedCard>
              )}

              {prediction.tips && (
                <AnimatedCard className="card">
                  <h3 className="font-bold mb-3">Tips to Improve</h3>
                  <ul className="space-y-2">
                    {(Array.isArray(prediction.tips) ? prediction.tips : [prediction.tips]).map((tip, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-brand-secondary dark:text-gray-400">
                        <span className="text-primary-600 mt-0.5">•</span>
                        {tip}
                      </li>
                    ))}
                  </ul>
                </AnimatedCard>
              )}

              {/* Outcome tracking — how the model learns */}
              <AnimatedCard className="card border border-primary-500/20">
                <h3 className="font-bold mb-1 flex items-center gap-2">
                  <Target size={20} className="text-primary-600" />
                  What actually happened?
                </h3>
                <p className="text-xs text-brand-muted dark:text-gray-500 mb-4">
                  Reporting real outcomes teaches the predictor — the more data, the sharper your next number.
                </p>
                <form onSubmit={handleRecordOutcome} className="flex flex-wrap items-center gap-3">
                  <div className="flex rounded-lg overflow-hidden border border-brand-primary/20">
                    {Object.entries(OUTCOME_META).map(([key, meta]) => (
                      <button
                        key={key}
                        type="button"
                        onClick={() => setOutcomeForm((f) => ({ ...f, outcome: key }))}
                        className={`px-3 py-2 text-sm font-medium flex items-center gap-1.5 transition-colors ${
                          outcomeForm.outcome === key
                            ? "bg-primary-600 text-white"
                            : "bg-surface-card dark:bg-gray-800 text-brand-secondary dark:text-gray-300 hover:bg-primary-100 dark:hover:bg-gray-700"
                        }`}
                      >
                        <meta.icon size={14} />
                        {meta.label}
                      </button>
                    ))}
                  </div>
                  <input
                    value={outcomeForm.notes}
                    onChange={(e) => setOutcomeForm((f) => ({ ...f, notes: e.target.value }))}
                    placeholder="Optional note (e.g. round, date)"
                    className="flex-1 min-w-[180px] px-3 py-2 text-sm border border-brand-primary/20 rounded-lg bg-surface-card dark:bg-gray-800 dark:text-white focus:ring-2 focus:ring-primary-500"
                  />
                  <button
                    type="submit"
                    disabled={savingOutcome}
                    className="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-bold hover:bg-primary-700 disabled:opacity-50 transition-colors"
                  >
                    {savingOutcome ? "Saving..." : "Log outcome"}
                  </button>
                </form>

                {outcomes.length > 0 && (
                  <div className="mt-4 space-y-2">
                    {outcomes.slice(0, 5).map((o) => {
                      const meta = OUTCOME_META[o.outcome] || OUTCOME_META.in_process;
                      return (
                        <div key={o.id} className="flex items-center justify-between gap-2 text-sm bg-surface-card/50 dark:bg-gray-800/60 rounded-lg px-3 py-2">
                          <div className="flex items-center gap-2 min-w-0">
                            <meta.icon size={15} className={meta.color} />
                            <span className="font-semibold capitalize dark:text-white truncate">{o.company}</span>
                            {o.predicted_probability != null && (
                              <span className="text-xs text-brand-muted dark:text-gray-500">predicted {o.predicted_probability}%</span>
                            )}
                            {o.notes && <span className="text-xs text-brand-secondary dark:text-gray-400 truncate">· {o.notes}</span>}
                          </div>
                          <button
                            onClick={() => handleDeleteOutcome(o.id)}
                            className="text-brand-muted hover:text-red-500 transition-colors shrink-0"
                            aria-label="Delete outcome"
                          >
                            <Trash2 size={14} />
                          </button>
                        </div>
                      );
                    })}
                  </div>
                )}
              </AnimatedCard>

              {/* Calibration curve — does the predictor hold up? */}
              {outcomeStats && (
                <AnimatedCard className="card">
                  <h3 className="font-bold mb-1 flex items-center gap-2">
                    <BarChart3 size={20} className="text-primary-600" />
                    Calibration — is the number trustworthy?
                  </h3>
                  <p className="text-xs text-brand-muted dark:text-gray-500 mb-4">
                    {outcomeStats.decided || 0} outcomes decided so far
                    {(outcomeStats.decided || 0) < 20
                      ? ` — warming up, need ${20 - (outcomeStats.decided || 0)} more for a useful curve.`
                      : "."}
                  </p>

                  <div className="flex gap-8 mb-5 text-sm">
                    <div>
                      <p className="text-2xl font-bold text-primary-600">
                        {outcomeStats.offered_rate != null ? `${outcomeStats.offered_rate}%` : "—"}
                      </p>
                      <p className="text-xs text-brand-muted">Actual offer rate</p>
                    </div>
                    <div>
                      <p className="text-2xl font-bold dark:text-white">{outcomeStats.offered ?? 0}</p>
                      <p className="text-xs text-brand-muted">Offers</p>
                    </div>
                    <div>
                      <p className="text-2xl font-bold dark:text-white">{outcomeStats.in_process ?? 0}</p>
                      <p className="text-xs text-brand-muted">In process</p>
                    </div>
                  </div>

                  {outcomeStats.calibration?.length > 0 ? (
                    <div className="space-y-3">
                      {outcomeStats.calibration.map((c: any) => {
                        const nums = (c.band || "").replace("%", "").split("-").map(Number).filter((n: number) => !isNaN(n));
                        const mid = nums.length === 2 ? Math.round((nums[0] + nums[1]) / 2) : null;
                        return (
                          <div key={c.band}>
                            <div className="flex justify-between text-xs mb-1">
                              <span className="text-brand-secondary dark:text-gray-400">Predicted {c.band}</span>
                              <span className="dark:text-white">
                                Actual {c.actual_offer_rate}% · {c.count} {c.count === 1 ? "outcome" : "outcomes"}
                              </span>
                            </div>
                            <div className="flex items-center gap-2">
                              <div className="flex-1 bg-surface-card/50 dark:bg-gray-700 rounded-full h-2.5 overflow-hidden">
                                <motion.div
                                  className="h-2.5 rounded-full bg-primary-600"
                                  initial={reduced ? { width: `${c.actual_offer_rate}%` } : { width: 0 }}
                                  whileInView={{ width: `${c.actual_offer_rate}%` }}
                                  viewport={{ once: true }}
                                  transition={{ duration: 0.8 }}
                                />
                              </div>
                              {mid != null && (
                                <span className="text-[10px] text-brand-muted w-12 text-right whitespace-nowrap">
                                  target ~{mid}%
                                </span>
                              )}
                            </div>
                          </div>
                        );
                      })}
                      <p className="text-xs text-brand-muted dark:text-gray-500 mt-2">
                        When the predictor is honest, each actual bar lands near its target mark.
                      </p>
                    </div>
                  ) : (
                    <p className="text-xs text-brand-muted dark:text-gray-500">
                      Keep logging outcomes after interviews — once 20 are decided, the predicted-vs-actual curve appears here.
                    </p>
                  )}
                </AnimatedCard>
              )}

              {/* Time-to-offer — when will you get an offer? */}
              <AnimatedCard className="card">
                <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
                  <div>
                    <h3 className="font-bold flex items-center gap-2">
                      <Hourglass size={20} className="text-primary-600" />
                      When will you get an offer?
                    </h3>
                    <p className="text-xs text-brand-muted dark:text-gray-500 mt-0.5">
                      For {prediction?.target_company || "this company"} · transparent math, not a magic date
                    </p>
                  </div>
                  <button
                    onClick={handleTimeToOffer}
                    disabled={timeToOfferLoading}
                    className="px-4 py-2 rounded-lg bg-primary-600 text-white text-sm font-bold hover:bg-primary-700 disabled:opacity-50 transition-colors"
                  >
                    {timeToOfferLoading ? "Estimating..." : timeToOffer ? "Re-estimate" : "Estimate"}
                  </button>
                </div>

                {timeToOffer && (
                  <div className="space-y-4">
                    <div className="flex items-end gap-2">
                      <p className="text-5xl font-black text-primary-600">{timeToOffer.weeks_estimate}</p>
                      <div className="pb-1">
                        <p className="text-sm font-bold dark:text-white">weeks to offer</p>
                        <p className="text-xs text-brand-muted dark:text-gray-500">{timeToOffer.range}</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-3 text-center">
                      <div className="bg-surface-card/50 dark:bg-gray-800/60 rounded-lg px-2 py-2">
                        <p className="text-lg font-bold dark:text-white">{timeToOffer.process_time_weeks}</p>
                        <p className="text-[10px] uppercase tracking-wide text-brand-muted">process</p>
                      </div>
                      <div className="bg-surface-card/50 dark:bg-gray-800/60 rounded-lg px-2 py-2">
                        <p className="text-lg font-bold dark:text-white">{timeToOffer.prep_weeks}</p>
                        <p className="text-[10px] uppercase tracking-wide text-brand-muted">prep weeks</p>
                      </div>
                      <div className="bg-surface-card/50 dark:bg-gray-800/60 rounded-lg px-2 py-2">
                        <p className="text-lg font-bold dark:text-white">{timeToOffer.velocity}</p>
                        <p className="text-[10px] uppercase tracking-wide text-brand-muted">pts/wk velocity</p>
                      </div>
                    </div>

                    {timeToOffer.gaps?.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-wide text-brand-muted mb-2">Biggest gaps to close</p>
                        <div className="flex flex-wrap gap-2">
                          {timeToOffer.gaps.map((g: any) => (
                            <span key={g.skill} className="text-xs bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300 rounded-full px-3 py-1">
                              {g.label} +{g.gap} pts
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    <div className="space-y-1.5">
                      {timeToOffer.accelerants?.map((a: string, i: number) => (
                        <p key={i} className="text-xs text-brand-secondary dark:text-gray-400 flex gap-2">
                          <Zap size={13} className="text-amber-500 shrink-0 mt-0.5" />
                          {a}
                        </p>
                      ))}
                    </div>

                    <p className="text-[11px] text-brand-muted dark:text-gray-500">{timeToOffer.data_note}</p>
                  </div>
                )}
              </AnimatedCard>
            </motion.div>
          )}
        </AnimatePresence>

        {history.length > 0 && (
          <div className="mt-8">
            <h3 className="font-bold mb-4 dark:text-white">Past Predictions</h3>
            <div className="space-y-2">
              {history.slice(0, 5).map((p, i) => (
                <AnimatedCard key={i} className="card flex items-center justify-between py-3">
                  <div>
                    <p className="font-semibold dark:text-white">{p.company}</p>
                    <p className="text-sm text-brand-muted">{p.role}</p>
                  </div>
                  <p className="font-bold text-primary-600">₹{(p.predicted_ctc || p.salary || 0).toLocaleString("en-IN")}</p>
                </AnimatedCard>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
