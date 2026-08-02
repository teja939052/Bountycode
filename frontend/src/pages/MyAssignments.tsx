import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  ClipboardList, Calendar, Award, Send, CheckCircle2, Clock,
  FileText, X, BookOpen, Loader2
} from "lucide-react";
import { assignmentsApi } from "../services/api/adminContent";
import Spinner from "../components/ui/Spinner";

const inputCls = "w-full px-3.5 py-2.5 rounded-xl bg-slate-950/60 border border-white/10 text-sm text-text-primary placeholder-gray-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 transition-all";

function formatDate(value) {
  if (!value) return "—";
  const d = new Date(value);
  if (isNaN(d.getTime())) return value;
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" }) +
    " " + d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

function StatusBadge({ status }) {
  const config = {
    pending: { label: "Pending", cls: "bg-amber-500/10 text-amber-400 border-amber-500/30", icon: Clock },
    submitted: { label: "Submitted", cls: "bg-sky-500/10 text-sky-400 border-sky-500/30", icon: Send },
    graded: { label: "Graded", cls: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30", icon: CheckCircle2 },
  };
  const c = config[status] || config.pending;
  const Icon = c.icon;
  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-mono uppercase tracking-[0.15em] border ${c.cls}`}>
      <Icon size={11} />
      {c.label}
    </span>
  );
}

export default function MyAssignments() {
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [drafts, setDrafts] = useState<any>({});
  const [submitting, setSubmitting] = useState({});
  const [expanded, setExpanded] = useState({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await assignmentsApi.list();
      setAssignments(data.assignments || []);
      setDrafts(prev => {
        const next = { ...prev };
        (data.assignments || []).forEach(a => {
          if (next[a.id] === undefined) next[a.id] = a.answer_text || "";
        });
        return next;
      });
    } catch (e) {
      setError(e.message || "Failed to load assignments");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleSubmit = async (assignment) => {
    const answer = (drafts[assignment.id] || "").trim();
    if (!answer) {
      setError("Please write an answer before submitting");
      return;
    }
    setSubmitting(prev => ({ ...prev, [assignment.id]: true }));
    setError("");
    setSuccess("");
    try {
      await assignmentsApi.submit(assignment.id, answer);
      setSuccess(`Submitted "${assignment.title}"`);
      await load();
    } catch (e) {
      setError(e.message || "Failed to submit assignment");
    } finally {
      setSubmitting(prev => ({ ...prev, [assignment.id]: false }));
    }
  };

  const isOverdue = (a) => a.due_date && new Date(a.due_date) < new Date() && a.submission_status === "pending";

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 mb-3">
          <ClipboardList size={14} className="text-indigo-400" />
          <span className="text-xs font-mono text-indigo-400">MY ASSIGNMENTS</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Assignments</h1>
        <p className="mt-2 text-sm text-gray-400">Complete your homework tasks and track teacher feedback.</p>
      </motion.div>

      {(error || success) && (
        <div className={`mb-6 px-4 py-3 rounded-xl border text-sm font-mono flex items-center justify-between ${
          error ? "bg-red-500/10 border-red-500/20 text-red-300" : "bg-emerald-500/10 border-emerald-500/20 text-emerald-300"
        }`}>
          <span>{error || success}</span>
          <button onClick={() => { setError(""); setSuccess(""); }} className="opacity-70 hover:opacity-100">
            <X size={14} />
          </button>
        </div>
      )}

      {loading ? (
        <div className="flex justify-center py-20"><Spinner /></div>
      ) : assignments.length === 0 ? (
        <div className="glass rounded-xl p-16 text-center text-gray-500 font-mono text-sm">
          No assignments assigned to you yet. Check back soon!
        </div>
      ) : (
        <div className="space-y-4">
          {assignments.map((a, i) => {
            const status = a.submission_status || "pending";
            const overdue = isOverdue(a);
            return (
              <motion.div
                key={a.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: Math.min(i * 0.05, 0.4) }}
                className="glass rounded-xl overflow-hidden">
                <div className="p-5">
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20">
                          <FileText size={14} className="text-indigo-400" />
                        </span>
                        <h3 className="font-display font-bold text-text-primary">{a.title}</h3>
                        <StatusBadge status={status} />
                        {overdue && (
                          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono border bg-red-500/10 text-red-400 border-red-500/30">
                            Overdue
                          </span>
                        )}
                      </div>
                      {a.description && (
                        <p className="mt-2 text-sm text-gray-400 whitespace-pre-wrap">{a.description}</p>
                      )}
                      <div className="mt-3 flex flex-wrap gap-4 text-xs font-mono text-gray-500">
                        <span className="flex items-center gap-1.5">
                          <Calendar size={12} className="text-sky-400" />
                          Due {formatDate(a.due_date)}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Award size={12} className="text-amber-400" />
                          Max score {a.max_score}
                        </span>
                        {a.content_title && (
                          <span className="flex items-center gap-1.5">
                            <BookOpen size={12} className="text-indigo-400" />
                            {a.content_title}
                          </span>
                        )}
                        {status !== "pending" && (
                          <span className="flex items-center gap-1.5">
                            <Clock size={12} className="text-gray-500" />
                            Submitted {formatDate(a.submitted_at)}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {status === "graded" && (
                    <div className="mt-4 flex items-start gap-4 flex-wrap rounded-xl bg-slate-950/40 border border-white/10 p-4">
                      <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30">
                        <Award size={15} className="text-emerald-400" />
                        <span className="text-lg font-bold text-emerald-400">{a.score}</span>
                        <span className="text-[10px] font-mono text-gray-500">/ {a.max_score}</span>
                      </div>
                      <div className="flex-1 min-w-[200px]">
                        <p className="text-[10px] font-mono uppercase tracking-[0.2em] text-gray-500 mb-1">Teacher Feedback</p>
                        <p className="text-sm text-gray-300 whitespace-pre-wrap">{a.feedback || "No feedback provided."}</p>
                        {a.graded_at && (
                          <p className="mt-2 text-[10px] font-mono text-gray-600">Graded {formatDate(a.graded_at)}</p>
                        )}
                      </div>
                    </div>
                  )}

                  {status !== "graded" && (
                    <div className="mt-4">
                      <div className="flex items-center justify-between mb-2">
                        <button
                          onClick={() => setExpanded(prev => ({ ...prev, [a.id]: !prev[a.id] }))}
                          className="text-xs font-mono text-indigo-400 hover:text-indigo-300 transition-all">
                          {expanded[a.id] ? "Hide" : "Show"} answer form
                        </button>
                      </div>
                      <AnimatePresence>
                        {expanded[a.id] && (
                          <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: "auto" }}
                            exit={{ opacity: 0, height: 0 }}
                            className="overflow-hidden">
                            <textarea
                               rows={5}
                              value={drafts[a.id] || ""}
                              onChange={e => setDrafts(prev => ({ ...prev, [a.id]: e.target.value }))}
                              placeholder="Write your answer here..."
                              className={`${inputCls} resize-none`}
                            />
                            <div className="mt-3 flex justify-end">
                              <button
                                onClick={() => handleSubmit(a)}
                                disabled={submitting[a.id]}
                                className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-500/90 hover:bg-indigo-500 text-white text-sm font-semibold transition-all disabled:opacity-50">
                                {submitting[a.id] ? <Loader2 size={15} className="animate-spin" /> : <Send size={15} />}
                                {status === "submitted" ? "Resubmit" : "Submit Answer"}
                              </button>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>
                    </div>
                  )}

                  {status === "submitted" && (
                    <div className="mt-4 rounded-xl bg-slate-950/40 border border-white/10 p-3">
                      <p className="text-[10px] font-mono uppercase tracking-[0.2em] text-gray-500 mb-1">Your Answer</p>
                      <p className="text-sm text-gray-300 whitespace-pre-wrap line-clamp-4">{a.answer_text || ""}</p>
                    </div>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      )}
    </div>
  );
}
