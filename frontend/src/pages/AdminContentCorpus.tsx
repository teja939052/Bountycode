import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BookOpen, Search, RefreshCw, Play, FileText,
  AlertTriangle, CheckCircle2, Clock, X, ChevronRight, Loader2, FlaskConical
} from "lucide-react";
import { corpusApi, type CorpusSummary, type CorpusConcept, type ConceptDetail, type GenerationQueueItem } from "../services/api/adminContent";
import Spinner from "../components/ui/Spinner";

type Tab = "concepts" | "queue" | "validate";

const DOMAINS = ["cs", "databases", "devops", "placement", "programming", "web"];
const STATUS_OPTIONS = ["seeded", "AUTO_SCAFFOLDED", "enriched", "verified"];
const CONTENT_TYPES = ["lesson", "exercise", "quiz", "assessment", "debug_challenge"];

const STATUS_COLORS: Record<string, string> = {
  seeded: "bg-gray-500/10 text-gray-400 border-gray-500/30",
  AUTO_SCAFFOLDED: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  enriched: "bg-sky-500/10 text-sky-400 border-sky-500/30",
  verified: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
};

const DOMAIN_COLORS: Record<string, string> = {
  cs: "bg-brand-primary/10 text-brand-primary border-brand-primary/20",
  databases: "bg-sky-500/10 text-sky-400 border-sky-500/30",
  devops: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  placement: "bg-rose-500/10 text-rose-400 border-rose-500/30",
  programming: "bg-brand-lavender/10 text-brand-lavender border-brand-lavender/20",
  web: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
};

const inputCls = "w-full px-3.5 py-2.5 rounded-xl bg-surface-base border border-nature-leaf/20 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-nature-leaf focus:ring-1 focus:ring-nature-leaf/30 transition-all";

function formatCount(value: number | undefined) {
  if (typeof value !== "number") return "—";
  return value.toLocaleString();
}

export default function AdminContentCorpus() {
  const [tab, setTab] = useState<Tab>("concepts");
  const [summary, setSummary] = useState<CorpusSummary | null>(null);
  const [concepts, setConcepts] = useState<CorpusConcept[]>([]);
  const [conceptsLoading, setConceptsLoading] = useState(false);
  const [conceptCount, setConceptCount] = useState(0);
  const [queue, setQueue] = useState<GenerationQueueItem[]>([]);
  const [queueLoading, setQueueLoading] = useState(false);
  const [queueCount, setQueueCount] = useState(0);
  const [validation, setValidation] = useState<{ valid: boolean; issues: Array<{ concept_id?: string; message: string }> } | null>(null);
  const [validateLoading, setValidateLoading] = useState(false);
  const [activeConcept, setActiveConcept] = useState<ConceptDetail | null>(null);
  const [conceptLoading, setConceptLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [generateResult, setGenerateResult] = useState<any>(null);

  const [search, setSearch] = useState("");
  const [domainFilter, setDomainFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [contentTypeFilter, setContentTypeFilter] = useState("");
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [error, setError] = useState("");

  const loadSummary = useCallback(async () => {
    try {
      const data = await corpusApi.summary();
      setSummary(data);
    } catch (e: any) {
      setError(e?.message || "Failed to load corpus summary");
    }
  }, []);

  const loadConcepts = useCallback(async () => {
    setConceptsLoading(true);
    try {
      const params: Record<string, string> = {};
      if (domainFilter) params.domain = domainFilter;
      if (statusFilter) params.language = statusFilter;
      const data = await corpusApi.concepts(params);
      setConcepts(data.concepts || []);
      setConceptCount(data.count || 0);
    } catch (e: any) {
      setError(e?.message || "Failed to load concepts");
    } finally {
      setConceptsLoading(false);
    }
  }, [domainFilter, statusFilter]);

  const loadQueue = useCallback(async () => {
    setQueueLoading(true);
    try {
      const params: Record<string, string> = {};
      if (domainFilter) params.domain = domainFilter;
      if (contentTypeFilter) params.language = contentTypeFilter;
      const data = await corpusApi.queue(params, 50);
      setQueue(data.queue || []);
      setQueueCount(data.count || 0);
    } catch (e: any) {
      setError(e?.message || "Failed to load generation queue");
    } finally {
      setQueueLoading(false);
    }
  }, [domainFilter, contentTypeFilter]);

  const loadValidation = useCallback(async () => {
    setValidateLoading(true);
    try {
      const data = await corpusApi.validate();
      setValidation(data);
    } catch (e: any) {
      setError(e?.message || "Failed to validate corpus");
    } finally {
      setValidateLoading(false);
    }
  }, []);

  const openConcept = async (conceptId: string) => {
    setConceptLoading(true);
    setActiveConcept(null);
    try {
      const data = await corpusApi.concept(conceptId);
      setActiveConcept(data.concept as ConceptDetail);
    } catch (e: any) {
      setError(e?.message || "Failed to load concept");
    } finally {
      setConceptLoading(false);
    }
  };

  const handleGenerate = async () => {
    if (selectedIds.size === 0) {
      setError("Select at least one concept to generate");
      return;
    }
    setGenerating(true);
    setGenerateResult(null);
    try {
      const types = contentTypeFilter ? contentTypeFilter.split(",").map(s => s.trim()).filter(Boolean) : undefined;
      const report = await corpusApi.generate(Array.from(selectedIds), types, "dry_run");
      setGenerateResult(report);
      await loadQueue();
      await loadSummary();
    } catch (e: any) {
      setError(e?.message || "Generation failed");
    } finally {
      setGenerating(false);
    }
  };

  const toggleSelect = (id: string) => {
    setSelectedIds(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  };

  const selectAll = () => {
    const filtered = getFilteredConcepts();
    if (selectedIds.size === filtered.length && filtered.length > 0) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(filtered.map(c => c.concept_id)));
    }
  };

  const getFilteredConcepts = () => {
    let result = concepts;
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(c => c.title?.toLowerCase().includes(q) || c.concept_id?.toLowerCase().includes(q) || c.description?.toLowerCase().includes(q));
    }
    return result;
  };

  useEffect(() => { loadSummary(); }, [loadSummary]);
  useEffect(() => { if (tab === "concepts") loadConcepts(); }, [tab, loadConcepts]);
  useEffect(() => { if (tab === "queue") loadQueue(); }, [tab, loadQueue]);
  useEffect(() => { if (tab === "validate") loadValidation(); }, [tab, loadValidation]);

  const filteredConcepts = getFilteredConcepts();

  return (
    <div className="min-h-screen bg-surface-base px-4 py-8 max-w-7xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-500/10 border border-red-500/20 mb-3">
              <BookOpen size={14} className="text-red-400" />
              <span className="text-xs font-mono text-red-400">ADMIN</span>
            </div>
            <h1 className="text-3xl font-display font-black text-text-primary">Knowledge Corpus</h1>
            <p className="text-sm text-text-muted font-mono mt-1">Manage concepts, generation queue, and content verification</p>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={() => { loadSummary(); loadConcepts(); loadQueue(); }}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-surface-card border border-nature-leaf/20 text-text-secondary text-sm font-mono hover:text-text-primary hover:border-nature-leaf/30 transition-all">
              <RefreshCw size={14} />
              Refresh
            </button>
          </div>
        </div>

        <div className="mt-6 flex gap-2 bg-white border border-nature-leaf/20 rounded-xl p-1.5 w-fit flex-wrap">
          <TabButton active={tab === "concepts"} onClick={() => setTab("concepts")} icon={BookOpen} label={`Concepts${conceptCount ? ` (${conceptCount})` : ""}`} />
          <TabButton active={tab === "queue"} onClick={() => setTab("queue")} icon={Clock} label={`Queue${queueCount ? ` (${queueCount})` : ""}`} />
          <TabButton active={tab === "validate"} onClick={() => setTab("validate")} icon={AlertTriangle} label="Validate" />
        </div>
      </motion.div>

      {error && (
        <div className="mb-6 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-500 text-sm font-mono flex items-center justify-between">
          <span>{error}</span>
          <button onClick={() => setError("")} className="text-red-500 hover:text-red-600"><X size={14} /></button>
        </div>
      )}

      {/* Summary */}
      {summary && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          <StatCard icon={BookOpen} label="Concepts" value={formatCount(summary.total_concepts)} sub={`${Object.keys(summary.domains || {}).length} domains`} color="text-brand-primary" />
          <StatCard icon={CheckCircle2} label="Verified" value={formatCount(summary.status_counts?.verified || 0)} sub={`${summary.status_counts?.AUTO_SCAFFOLDED || 0} scaffolded`} color="text-emerald-400" />
          <StatCard icon={AlertTriangle} label="Issues" value={formatCount(summary.validation?.issues?.length || 0)} sub={summary.validation?.valid ? "Corpus valid" : "Has issues"} color={summary.validation?.valid ? "text-emerald-400" : "text-amber-400"} />
          <StatCard icon={FileText} label="Categories" value={formatCount(Object.keys(summary.categories || {}).length)} sub={`${Object.keys(summary.status_counts || {}).length} statuses`} color="text-brand-sky" />
        </motion.div>
      )}

      {/* Concepts Tab */}
      {tab === "concepts" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
            <div className="flex flex-1 min-w-[220px] gap-3 flex-wrap">
              <div className="relative flex-1 min-w-[180px] max-w-md">
                <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-brand-secondary" />
                <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search concepts..." className={`${inputCls} pl-10`} />
              </div>
              <select value={domainFilter} onChange={e => setDomainFilter(e.target.value)} className={`${inputCls} max-w-[160px]`}>
                <option value="">All domains</option>
                {DOMAINS.map(d => <option key={d} value={d}>{d}</option>)}
              </select>
              <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)} className={`${inputCls} max-w-[180px]`}>
                <option value="">All statuses</option>
                {STATUS_OPTIONS.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div className="flex items-center gap-2">
              <button onClick={selectAll} className="px-3 py-2 rounded-lg bg-surface-card border border-nature-leaf/20 text-text-secondary text-xs font-mono hover:text-text-primary transition-all">
                {selectedIds.size === filteredConcepts.length && filteredConcepts.length > 0 ? "Deselect All" : "Select All"}
              </button>
              <button onClick={handleGenerate} disabled={generating || selectedIds.size === 0} className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-nature-leaf hover:bg-nature-moss text-text-primary text-sm font-semibold transition-all disabled:opacity-50">
                {generating ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />}
                {generating ? "Generating..." : `Generate (${selectedIds.size})`}
              </button>
            </div>
          </div>

          {conceptsLoading ? (
            <div className="flex justify-center py-20"><Spinner /></div>
          ) : filteredConcepts.length === 0 ? (
            <div className="glass rounded-xl p-16 text-center text-text-muted font-mono text-sm">No concepts match your filters.</div>
          ) : (
            <div className="space-y-2">
              {filteredConcepts.map((c, i) => (
                <motion.div key={c.concept_id} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: Math.min(i * 0.02, 0.3) }}
                  className="glass rounded-xl p-4 flex items-center gap-4">
                  <button onClick={() => toggleSelect(c.concept_id)} className={`shrink-0 w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all ${selectedIds.has(c.concept_id) ? "bg-nature-leaf border-nature-leaf" : "border-nature-leaf/30 hover:border-nature-leaf/60"}`}>
                    {selectedIds.has(c.concept_id) && <CheckCircle2 size={12} className="text-white" />}
                  </button>
                  <div className="flex-1 min-w-0 cursor-pointer" onClick={() => openConcept(c.concept_id)}>
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-display font-bold text-text-primary text-sm">{c.title}</h3>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono uppercase border ${DOMAIN_COLORS[c.domain] || DOMAIN_COLORS.cs}`}>{c.domain}</span>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono uppercase border ${STATUS_COLORS[c.content_status] || STATUS_COLORS.seeded}`}>{c.content_status}</span>
                      <span className="text-[10px] font-mono text-text-muted">{c.category}</span>
                    </div>
                    {c.description && <p className="mt-1 text-xs text-text-muted line-clamp-1">{c.description}</p>}
                  </div>
                  <button onClick={() => openConcept(c.concept_id)} className="shrink-0 p-2 rounded-lg text-text-muted hover:text-text-primary hover:bg-surface-card transition-all">
                    <ChevronRight size={16} />
                  </button>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      {/* Queue Tab */}
      {tab === "queue" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
            <p className="text-sm font-mono text-text-muted">{queueCount} items in generation queue</p>
            <div className="flex items-center gap-2">
              <select value={contentTypeFilter} onChange={e => { setContentTypeFilter(e.target.value); loadQueue(); }} className={`${inputCls} max-w-[180px]`}>
                <option value="">All types</option>
                {CONTENT_TYPES.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
              <button onClick={loadQueue} className="px-3 py-2 rounded-lg bg-surface-card border border-nature-leaf/20 text-text-secondary text-xs font-mono hover:text-text-primary transition-all">
                <RefreshCw size={14} />
              </button>
            </div>
          </div>

          {queueLoading ? (
            <div className="flex justify-center py-20"><Spinner /></div>
          ) : queue.length === 0 ? (
            <div className="glass rounded-xl p-16 text-center text-text-muted font-mono text-sm">Queue is empty. Select concepts and generate content.</div>
          ) : (
            <div className="space-y-2">
              {queue.map((item, i) => (
                <motion.div key={item.concept_id} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: Math.min(i * 0.02, 0.3) }}
                  className="glass rounded-xl p-4 flex items-center gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="font-display font-bold text-text-primary text-sm">{item.title}</h3>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono uppercase border ${DOMAIN_COLORS[item.domain] || DOMAIN_COLORS.cs}`}>{item.domain}</span>
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono uppercase border ${STATUS_COLORS[item.content_status] || STATUS_COLORS.seeded}`}>{item.content_status}</span>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-2">
                      {(item.missing_types || []).map(t => (
                        <span key={t} className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20">{t}</span>
                      ))}
                    </div>
                  </div>
                  <button onClick={() => { setSelectedIds(new Set([item.concept_id])); setTab("concepts"); }} className="shrink-0 px-3 py-2 rounded-lg bg-surface-card border border-nature-leaf/20 text-text-secondary text-xs font-mono hover:text-text-primary transition-all">
                    Generate
                  </button>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      {/* Validate Tab */}
      {tab === "validate" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1}} className="space-y-4">
          <div className="flex items-center justify-between">
            <p className="text-sm font-mono text-text-muted">Run corpus validation to detect schema issues and orphaned prerequisites</p>
            <button onClick={loadValidation} disabled={validateLoading} className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-nature-leaf hover:bg-nature-moss text-text-primary text-sm font-semibold transition-all disabled:opacity-50">
              {validateLoading ? <Loader2 size={14} className="animate-spin" /> : <RefreshCw size={14} />}
              {validateLoading ? "Validating..." : "Re-run Validation"}
            </button>
          </div>

          {validation && (
            <div className="glass rounded-xl p-6">
              <div className="flex items-center gap-3 mb-4">
                {validation.valid ? (
                  <CheckCircle2 size={20} className="text-emerald-400" />
                ) : (
                  <AlertTriangle size={20} className="text-amber-400" />
                )}
                <h3 className="font-display font-bold text-text-primary">
                  {validation.valid ? "Corpus is valid" : `${(validation.issues || []).length} issue(s) found`}
                </h3>
              </div>

              {(validation.issues || []).length === 0 ? (
                <p className="text-sm text-text-muted font-mono">No validation issues found.</p>
              ) : (
                <div className="space-y-2 max-h-96 overflow-y-auto">
                  {(validation.issues || []).map((issue, i) => (
                    <div key={i} className="rounded-lg bg-surface-base border border-nature-leaf/20 p-3 flex items-start gap-3">
                      <AlertTriangle size={14} className="text-amber-400 mt-0.5 shrink-0" />
                      <div>
                        {issue.concept_id && <span className="text-[10px] font-mono text-text-muted">{issue.concept_id}</span>}
                        <p className="text-sm text-text-secondary">{issue.message}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </motion.div>
      )}

      {/* Generate Modal */}
      <AnimatePresence>
        {(generateResult || generating) && (
          <Modal title="Generation Result" onClose={() => setGenerateResult(null)} wide>
            {generating ? (
              <div className="flex flex-col items-center justify-center py-12 gap-3">
                <Loader2 size={32} className="text-brand-primary animate-spin" />
                <p className="text-sm font-mono text-text-muted">Generating content in dry_run mode...</p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono uppercase border bg-amber-500/10 text-amber-400 border-amber-500/30`}>
                    Dry Run
                  </span>
                  <span className="text-xs font-mono text-text-muted">concept: {String(generateResult?.concept_id || "")}</span>
                </div>

                {generateResult?.generated && Object.keys(generateResult.generated).length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-emerald-400 mb-2">Generated</h4>
                    <div className="space-y-1">
                      {Object.entries(generateResult.generated as Record<string, unknown>).map(([key, val]) => (
                        <div key={key} className="rounded-lg bg-emerald-500/5 border border-emerald-500/10 p-3 flex items-center gap-2">
                          <CheckCircle2 size={12} className="text-emerald-400" />
                          <span className="text-xs font-mono text-text-primary">{key}</span>
                          <span className="text-[10px] font-mono text-text-muted ml-auto">{typeof val === "object" ? JSON.stringify(val).slice(0, 60) : String(val)}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {generateResult?.skipped && Object.keys(generateResult.skipped).length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-amber-400 mb-2">Skipped</h4>
                    <div className="space-y-1">
                      {Object.entries(generateResult.skipped as Record<string, string>).map(([key, reason]) => (
                        <div key={key} className="rounded-lg bg-amber-500/5 border border-amber-500/10 p-3 flex items-center gap-2">
                          <Clock size={12} className="text-amber-400" />
                          <span className="text-xs font-mono text-text-primary">{key}</span>
                          <span className="text-[10px] font-mono text-text-muted ml-auto">{reason}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {generateResult?.validation && !generateResult.validation.valid && (
                  <div className="rounded-lg bg-red-500/5 border border-red-500/10 p-3">
                    <h4 className="text-xs font-mono uppercase tracking-wider text-red-400 mb-2">Validation Issues</h4>
                    <div className="space-y-1">
                      {(generateResult.validation.issues || []).map((issue: any, idx: number) => (
                        <p key={idx} className="text-xs font-mono text-red-400">{issue.message || JSON.stringify(issue)}</p>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </Modal>
        )}
      </AnimatePresence>

      {/* Concept Detail Modal */}
      <AnimatePresence>
        {activeConcept && (
          <Modal title={activeConcept.title} onClose={() => setActiveConcept(null)} wide>
            {conceptLoading ? (
              <div className="flex justify-center py-12"><Spinner /></div>
            ) : (
              <div className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono uppercase border ${DOMAIN_COLORS[activeConcept.domain] || DOMAIN_COLORS.cs}`}>{activeConcept.domain}</span>
                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-mono uppercase border ${STATUS_COLORS[activeConcept.content_status] || STATUS_COLORS.seeded}`}>{activeConcept.content_status}</span>
                  <span className="px-2.5 py-1 rounded-full text-[10px] font-mono bg-surface-card border border-nature-leaf/20 text-text-secondary">{activeConcept.category}</span>
                  {activeConcept.difficulty && <span className="px-2.5 py-1 rounded-full text-[10px] font-mono bg-surface-card border border-nature-leaf/20 text-text-secondary">{activeConcept.difficulty}</span>}
                </div>

                {activeConcept.description && <p className="text-sm text-text-secondary">{activeConcept.description}</p>}

                {activeConcept.prerequisites && activeConcept.prerequisites.length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-text-muted mb-2">Prerequisites</h4>
                    <div className="flex flex-wrap gap-2">
                      {activeConcept.prerequisites.map(p => (
                        <span key={p} className="px-2 py-1 rounded-lg bg-surface-card border border-nature-leaf/20 text-[10px] font-mono text-text-secondary">{p}</span>
                      ))}
                    </div>
                  </div>
                )}

                {activeConcept.worked_examples && activeConcept.worked_examples.length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-text-muted mb-2">Worked Examples</h4>
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                      {(activeConcept.worked_examples as any[]).map((ex, i) => (
                        <div key={i} className="rounded-lg bg-surface-base border border-nature-leaf/20 p-3">
                          <p className="text-xs font-mono text-text-secondary whitespace-pre-wrap">{typeof ex === "string" ? ex : JSON.stringify(ex, null, 2)}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeConcept.misconceptions && activeConcept.misconceptions.length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-text-muted mb-2">Misconceptions</h4>
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                      {(activeConcept.misconceptions as any[]).map((m, i) => (
                        <div key={i} className="rounded-lg bg-amber-500/5 border border-amber-500/10 p-3">
                          <p className="text-xs font-mono text-amber-400">{typeof m === "string" ? m : JSON.stringify(m, null, 2)}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {activeConcept.transfer_targets && activeConcept.transfer_targets.length > 0 && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-text-muted mb-2">Transfer Targets</h4>
                    <div className="flex flex-wrap gap-2">
                      {(activeConcept.transfer_targets as string[]).map(t => (
                        <span key={t} className="px-2 py-1 rounded-lg bg-sky-500/5 border border-sky-500/10 text-[10px] font-mono text-sky-400">{t}</span>
                      ))}
                    </div>
                  </div>
                )}

                {activeConcept.verification && (activeConcept.verification as any) && (
                  <div>
                    <h4 className="text-xs font-mono uppercase tracking-wider text-text-muted mb-2">Verification</h4>
                    <pre className="text-[10px] font-mono text-text-secondary bg-surface-base border border-nature-leaf/20 rounded-lg p-3 overflow-x-auto">
                      {JSON.stringify(activeConcept.verification, null, 2)}
                    </pre>
                  </div>
                )}

                <div className="flex justify-end pt-2">
                  <button onClick={() => { setSelectedIds(new Set([activeConcept.concept_id])); setActiveConcept(null); setTab("queue"); }} className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-nature-leaf hover:bg-nature-moss text-text-primary text-sm font-semibold transition-all">
                    <FlaskConical size={14} />
                    Generate Content
                  </button>
                </div>
              </div>
            )}
          </Modal>
        )}
      </AnimatePresence>
    </div>
  );
}

function TabButton({ active, onClick, icon: Icon, label }: any) {
  return (
    <button onClick={onClick} className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-mono transition-all ${active ? "bg-nature-leaf text-text-primary shadow-lg shadow-[#4F8F57]/20" : "text-text-muted hover:text-text-primary hover:bg-surface-card"}`}>
      <Icon size={15} />
      {label}
    </button>
  );
}

function StatCard({ icon: Icon, label, value, sub, color = "text-brand-sky", delay = 0 }: any) {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay }} className="glass rounded-xl p-4">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-lg bg-white border-border shadow-card flex items-center justify-center shrink-0">
          <Icon size={18} className={color} />
        </div>
        <div className="min-w-0">
          <p className="text-[10px] font-mono text-gray-500 uppercase tracking-wider">{label}</p>
          <p className={`text-xl font-display font-black ${color}`}>{value}</p>
          {sub && <p className="text-[10px] font-mono text-gray-600 truncate">{sub}</p>}
        </div>
      </div>
    </motion.div>
  );
}

function Modal({ title, onClose, children, wide = false }: { title: string; onClose: () => void; children: React.ReactNode; wide?: boolean }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-surface-2 backdrop-blur-sm" onClick={onClose} />
      <motion.div initial={{ opacity: 0, scale: 0.96, y: 12 }} animate={{ opacity: 1, scale: 1, y: 0 }}
        className={`relative w-full ${wide ? "max-w-3xl" : "max-w-xl"} max-h-[90vh] overflow-y-auto rounded-2xl bg-white border border-nature-leaf/20 shadow-2xl`}>
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#EDEAE0] sticky top-0 bg-white rounded-t-2xl z-10">
          <h3 className="font-display font-bold text-text-primary">{title}</h3>
          <button onClick={onClose} className="p-1.5 rounded-lg text-text-muted hover:text-text-primary hover:bg-surface-card transition-all" aria-label="Close">
            <X size={18} />
          </button>
        </div>
        <div className="p-6">{children}</div>
      </motion.div>
    </div>
  );
}
