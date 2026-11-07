import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import {
  ShieldCheck,
  Check,
  X,
  RefreshCw,
  ThumbsUp,
  ThumbsDown,
  ChevronLeft,
  ChevronRight,
  ChevronDown,
} from "lucide-react";

interface MemoryRow {
  id: string;
  exam: string;
  exam_name: string;
  section: string;
  topic: string;
  question_text: string;
  format: "mcq" | "code" | "verbal";
  options: string[];
  known_answer: string;
  notes: string;
  status: string;
  report_count: number;
  created_at: string;
  updated_at: string;
  reporters?: string[];
}

const FILTERS = [
  { id: "verified_crowd", label: "Ready to promote" },
  { id: "new", label: "New (1+ report)" },
  { id: "approved", label: "Approved" },
  { id: "dismissed", label: "Dismissed" },
  { id: "", label: "All" },
];

const STATUS_STYLE: Record<string, string> = {
  new: "bg-surface-2 text-text-secondary border-black/10",
  verified_crowd: "bg-emerald-50 text-emerald-700 border-emerald-200",
  approved: "bg-cyber-blue/10 text-cyber-blue border-cyber-blue/30",
  dismissed: "bg-red-50 text-red-500 border-red-200",
};

interface PromoteState {
  correctIndex?: string;
  correctAnswer: string;
  reasoning: string;
  type: string;
}

const emptyPromote: PromoteState = { correctIndex: "", correctAnswer: "", reasoning: "", type: "mcq" };

export default function AdminExamReview() {
  const [status, setStatus] = useState("verified_crowd");
  const [exam, setExam] = useState("");
  const [rows, setRows] = useState<MemoryRow[]>([]);
  const [threshold, setThreshold] = useState(5);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [acting, setActing] = useState<string | null>(null);
  const [error, setError] = useState("");
  const [note, setNote] = useState("");
  const [exams, setExams] = useState<{ id: string; name: string }[]>([]);
  const [selected, setSelected] = useState<MemoryRow | null>(null);
  const [promote, setPromote] = useState<PromoteState>(emptyPromote);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [list, cfg] = await Promise.all([
        api.examMemories.adminList(status || undefined, exam || undefined, page, 50),
        api.examMemories.config(),
      ]);
      setRows(list.memories || []);
      setTotal(list.total || 0);
      setPages(list.pages || 1);
      setThreshold(list.threshold || cfg.verify_threshold || 5);
      setExams(cfg.exams || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load review queue");
    } finally {
      setLoading(false);
    }
  }, [status, exam, page]);

  useEffect(() => {
    load();
  }, [load]);

  const reset = () => {
    setStatus("verified_crowd");
    setExam("");
    setPage(1);
    load();
  };

  const openRow = (row: MemoryRow) => {
    setSelected(row);
    setPromote(emptyPromote);
    setNote("");
  };

  const doPromote = async (row: MemoryRow) => {
    if (!promote.reasoning.trim()) {
      setError("Reasoning is required to promote an item into the bank.");
      return;
    }
    setActing(row.id);
    setError("");
    try {
      const body: Record<string, unknown> = {
        reasoning: promote.reasoning.trim(),
        type: promote.type || row.format || "mcq",
        correct_answer: promote.correctAnswer.trim() || undefined,
      };
      if (promote.correctIndex !== "") body.correct_index = Number(promote.correctIndex);
      const res = (await api.examMemories.promote(row.id, body as Parameters<typeof api.examMemories.promote>[1])) as {
        status: string;
        note: string;
      };
      setNote(`${res.status} — ${res.note}`);
      setSelected(null);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Promotion failed");
    } finally {
      setActing(null);
    }
  };

  const doDismiss = async (row: MemoryRow) => {
    setActing(row.id);
    setError("");
    try {
      const res = (await api.examMemories.dismiss(row.id, note.trim() || "Not quality / not an original question")) as {
        status: string;
      };
      setNote(`${res.status} — dismissed`);
      setSelected(null);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Dismiss failed");
    } finally {
      setActing(null);
    }
  };

  return (
    <div className="page-surface min-h-screen py-10 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div className="mb-8" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <span className="section-subheader block mb-2">Admin · Content Trust</span>
              <h1 className="section-header text-2xl flex items-center gap-2">
                <ShieldCheck className="text-nature-blossom" size={26} /> Exam Memory Review
              </h1>
              <p className="font-mono text-xs text-text-muted mt-1">
                Promote crowdsourced recollections into the live bank. Auto-promotion: {threshold} reports. A verified human answer + reasoning is required.
              </p>
            </div>
            <button onClick={reset} className="btn-ghost text-xs flex items-center gap-1">
              <RefreshCw size={14} /> Reset filters
            </button>
          </div>
        </motion.div>

        {error && (
          <div className="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-center font-mono text-sm text-red-600">
            {error}
          </div>
        )}
        {note && (
          <div className="mb-5 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-center font-mono text-sm text-emerald-700">
            {note}
          </div>
        )}

        <div className="flex flex-wrap gap-2 mb-6">
          {FILTERS.map((f) => (
            <button
              key={f.id || "all"}
              onClick={() => { setStatus(f.id); setPage(1); }}
              className={`rounded-full border px-3.5 py-1.5 font-mono text-xs transition-colors ${
                status === f.id
                  ? "border-nature-blossom bg-blossom-50 text-nature-blossom font-bold"
                  : "border-black/10 bg-white text-text-muted hover:border-nature-blossom/50"
              }`}
            >
              {f.label}
            </button>
          ))}
          <select
            value={exam}
            onChange={(e) => { setExam(e.target.value); setPage(1); }}
            className="field w-auto ml-auto"
          >
            <option value="">All exams</option>
            {exams.map((e) => (
              <option key={e.id} value={e.id}>{e.name}</option>
            ))}
          </select>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        ) : rows.length === 0 ? (
          <div className="card rounded-3xl py-16 text-center">
            <p className="font-mono text-sm text-text-muted">
              No items in this queue. New memories appear here as students submit them.
            </p>
          </div>
        ) : (
          <>
            <div className="space-y-3">
              {rows.map((row) => (
                <div
                  key={row.id}
                  className="card rounded-2xl p-4 flex flex-col sm:flex-row sm:items-center gap-3 cursor-pointer hover:border-nature-blossom/50 transition-colors"
                  onClick={() => openRow(row)}
                >
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-center gap-2 mb-1">
                      <span className="font-mono text-[10px] uppercase tracking-wider text-nature-blossom">
                        {row.exam_name || row.exam} · {row.section}
                      </span>
                      {row.topic && (
                        <span className="rounded-full bg-surface-2 px-2 py-0.5 font-mono text-[9px] text-text-secondary">
                          {row.topic}
                        </span>
                      )}
                      <span className={`rounded-full border px-2 py-0.5 font-mono text-[9px] ${STATUS_STYLE[row.status] || STATUS_STYLE.new}`}>
                        {row.status.replace(/_/g, " ")}
                      </span>
                    </div>
                    <p className="text-sm text-text-primary line-clamp-2 leading-relaxed">{row.question_text}</p>
                    <p className="font-mono text-[10px] text-text-muted mt-1">
                      {row.report_count}/{threshold} reports · {row.format} · {new Date(row.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <button className="btn-ghost shrink-0 text-xs">
                    Review <ChevronDown size={14} className="inline" />
                  </button>
                </div>
              ))}
            </div>

            {pages > 1 && (
              <div className="flex items-center justify-center gap-3 mt-6">
                <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)} className="btn-ghost disabled:opacity-30">
                  <ChevronLeft size={16} /> Prev
                </button>
                <span className="font-mono text-xs text-text-muted">Page {page} / {pages} · {total} items</span>
                <button disabled={page >= pages} onClick={() => setPage((p) => p + 1)} className="btn-ghost disabled:opacity-30">
                  Next <ChevronRight size={16} />
                </button>
              </div>
            )}
          </>
        )}

        <AnimatePresence>
          {selected && (
            <motion.div
              className="fixed inset-0 z-50 flex items-center justify-center bg-space-void/50 p-4 backdrop-blur-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => !acting && setSelected(null)}
            >
              <motion.div
                className="card rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto"
                initial={{ scale: 0.96, y: 12 }}
                animate={{ scale: 1, y: 0 }}
                exit={{ scale: 0.96, y: 12 }}
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex items-start justify-between gap-4 mb-3">
                  <div>
                    <h3 className="font-display font-bold text-text-primary text-sm">
                      {selected.exam_name || selected.exam} · {selected.section}
                    </h3>
                    <p className="font-mono text-[10px] text-text-muted mt-0.5">
                      {selected.report_count}/{threshold} reports · {selected.format} · {selected.status.replace(/_/g, " ")}
                    </p>
                  </div>
                  <button onClick={() => !acting && setSelected(null)} className="text-text-muted hover:text-text-primary">
                    <X size={18} />
                  </button>
                </div>

                <div className="rounded-xl border border-black/5 bg-white p-4 mb-4">
                  <p className="text-sm leading-relaxed text-text-primary">{selected.question_text}</p>
                </div>

                {selected.options.length > 0 && (
                  <div className="mb-4 space-y-1.5">
                    {selected.options.map((opt, i) => (
                      <div key={i} className="rounded-lg border border-black/5 bg-white px-3 py-2 font-mono text-xs text-text-secondary">
                        {String.fromCharCode(65 + i)}. {opt}
                      </div>
                    ))}
                  </div>
                )}

                {selected.known_answer && (
                  <p className="mb-4 font-mono text-xs text-text-secondary">
                    <span className="text-text-muted">Student answer: </span>
                    {selected.known_answer}
                  </p>
                )}
                {selected.notes && (
                  <p className="mb-4 font-mono text-xs text-text-muted">Notes: {selected.notes}</p>
                )}

                <div className="border-t border-black/5 pt-4">
                  <h4 className="font-display font-bold text-text-primary text-xs mb-3">Promote into the bank</h4>
                  <div className="grid sm:grid-cols-2 gap-3 mb-3">
                    <label className="block">
                      <span className="label-text">Type (if coding/verbal)</span>
                      <select
                        value={promote.type}
                        onChange={(e) => setPromote((p) => ({ ...p, type: e.target.value }))}
                        className="field"
                      >
                        <option value="mcq">mcq</option>
                        <option value="text">text</option>
                        <option value="code">code</option>
                      </select>
                    </label>
                    {selected.format === "mcq" && (
                      <label className="block">
                        <span className="label-text">Correct option index</span>
                        <input
                          type="number"
                          min={0}
                          max={Math.max(selected.options.length - 1, 0)}
                          value={promote.correctIndex}
                          onChange={(e) => setPromote((p) => ({ ...p, correctIndex: e.target.value }))}
                          placeholder="0-based index e.g. 2"
                          className="field"
                        />
                      </label>
                    )}
                  </div>
                  <label className="block mb-3">
                    <span className="label-text">Verified answer / expected output</span>
                    <textarea
                      value={promote.correctAnswer}
                      onChange={(e) => setPromote((p) => ({ ...p, correctAnswer: e.target.value }))}
                      rows={2}
                      placeholder="The correct answer, verified independently — not just reported."
                      className="field resize-y"
                    />
                  </label>
                  <label className="block mb-4">
                    <span className="label-text">Reasoning (why is this correct + quality gate?)</span>
                    <textarea
                      value={promote.reasoning}
                      onChange={(e) => setPromote((p) => ({ ...p, reasoning: e.target.value }))}
                      rows={3}
                      placeholder="Independent verification reasoning, source, or analysis. Required."
                      className="field resize-y"
                    />
                  </label>
                  <div className="flex gap-3">
                    <button
                      onClick={() => doPromote(selected)}
                      disabled={acting === selected.id}
                      className="btn-primary flex-1 flex items-center justify-center gap-2 text-sm disabled:opacity-50"
                    >
                      {acting === selected.id ? <Spinner size="sm" className="text-space-void" /> : <><ThumbsUp size={15} /> Approve & promote</>}
                    </button>
                    <button
                      onClick={() => doDismiss(selected)}
                      disabled={acting === selected.id}
                      className="btn-ghost flex items-center gap-2 text-sm text-red-500 hover:text-red-600 disabled:opacity-50"
                    >
                      <ThumbsDown size={15} /> Dismiss
                    </button>
                  </div>
                  <div className="mt-3 flex items-center gap-2 font-mono text-[10px] text-text-muted">
                    <Check size={12} className="text-emerald-500" />
                    Approved items write to exam_memory_approved.json with trust_status "reviewed" and are served after restart.
                  </div>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}