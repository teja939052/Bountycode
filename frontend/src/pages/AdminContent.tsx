import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BookOpen, ClipboardList, Plus, Pencil, Trash2, X, Users,
  Calendar, Award, Send, CheckCircle2, Clock, FileText, Search, Layers
} from "lucide-react";
import { adminContentApi, assignmentsApi } from "../services/api/adminContent";
import Spinner from "../components/ui/Spinner";

const CATEGORIES = ["dsa", "aptitude", "soft-skills", "system-design", "behavioral"];
const DIFFICULTIES = ["beginner", "intermediate", "advanced"];

const CATEGORY_COLORS = {
  dsa: "bg-surface-card text-nature-blossom border-nature-leaf/30",
  aptitude: "bg-sky-500/10 text-sky-400 border-sky-500/30",
  "soft-skills": "bg-amber-500/10 text-amber-400 border-amber-500/30",
  "system-design": "bg-surface-card text-nature-blossom border-nature-leaf/30",
  behavioral: "bg-rose-500/10 text-rose-400 border-rose-500/30",
};

const DIFFICULTY_COLORS = {
  beginner: "bg-brand-primary/10 text-brand-primary border-brand-primary/20",
  intermediate: "bg-amber-500/10 text-amber-400 border-amber-500/30",
  advanced: "bg-rose-500/10 text-rose-400 border-rose-500/30",
};

const inputCls = "w-full px-3.5 py-2.5 rounded-xl bg-surface-base border border-nature-leaf/20 text-sm text-text-primary placeholder-text-muted focus:outline-none focus:border-nature-leaf focus:ring-1 focus:ring-nature-leaf/30 transition-all";

function formatDate(value) {
  if (!value) return "—";
  const d = new Date(value);
  if (isNaN(d.getTime())) return value;
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" }) +
    " " + d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

function Field({ label, children }) {
  return (
    <label className="block mb-4">
      <span className="block text-xs font-mono uppercase tracking-[0.2em] text-text-muted mb-1.5">{label}</span>
      {children}
    </label>
  );
}

function Modal({ title, onClose, children, wide = false }: {
  title: string;
  onClose: () => void;
  children: React.ReactNode;
  wide?: boolean;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-surface-2 backdrop-blur-sm" onClick={onClose} />
      <motion.div
        initial={{ opacity: 0, scale: 0.96, y: 12 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
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

function StatusBadge({ status }) {
  const config = {
    pending: { label: "Pending", cls: "bg-amber-500/10 text-amber-400 border-amber-500/30", icon: Clock },
    submitted: { label: "Submitted", cls: "bg-sky-500/10 text-sky-400 border-sky-500/30", icon: Send },
    graded: { label: "Graded", cls: "bg-brand-primary/10 text-brand-primary border-brand-primary/20", icon: CheckCircle2 },
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

export default function AdminContent() {
  const [tab, setTab] = useState("content");
  const [content, setContent] = useState([]);
  const [contentLoading, setContentLoading] = useState(true);
  const [assignments, setAssignments] = useState([]);
  const [assignmentsLoading, setAssignmentsLoading] = useState(true);
  const [contentSearch, setContentSearch] = useState("");
  const [contentModal, setContentModal] = useState(null);
  const [assignmentModal, setAssignmentModal] = useState(false);
  const [activeSubmissions, setActiveSubmissions] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [submissionsLoading, setSubmissionsLoading] = useState(false);
  const [gradeDrafts, setGradeDrafts] = useState<any>({});
  const [error, setError] = useState("");

  const loadContent = useCallback(async () => {
    setContentLoading(true);
    try {
      const data = await adminContentApi.list({ limit: 100 });
      setContent(data.content || []);
    } catch (e) {
      setError(e.message || "Failed to load content modules");
    } finally {
      setContentLoading(false);
    }
  }, []);

  const loadAssignments = useCallback(async () => {
    setAssignmentsLoading(true);
    try {
      const data = await assignmentsApi.listAdmin();
      setAssignments(data.assignments || []);
    } catch (e) {
      setError(e.message || "Failed to load assignments");
    } finally {
      setAssignmentsLoading(false);
    }
  }, []);

  useEffect(() => { loadContent(); }, [loadContent]);
  useEffect(() => { loadAssignments(); }, [loadAssignments]);

  const openSubmissions = async (assignment) => {
    setActiveSubmissions(assignment);
    setSubmissions([]);
    setSubmissionsLoading(true);
    setGradeDrafts({});
    try {
      const data = await assignmentsApi.submissions(assignment.id);
      setSubmissions(data.submissions || []);
    } catch (e) {
      setError(e.message || "Failed to load submissions");
    } finally {
      setSubmissionsLoading(false);
    }
  };

  const handleContentSave = async (form) => {
    try {
      if (contentModal?.mode === "edit") {
        await adminContentApi.update(contentModal.item.id, form);
      } else {
        await adminContentApi.create(form);
      }
      setContentModal(null);
      await loadContent();
    } catch (e) {
      setError(e.message || "Failed to save content module");
    }
  };

  const handleContentDelete = async (item) => {
    if (!window.confirm(`Delete content module "${item.title}"?`)) return;
    try {
      await adminContentApi.remove(item.id);
      await loadContent();
    } catch (e) {
      setError(e.message || "Failed to delete content module");
    }
  };

  const handleAssignmentCreate = async (form) => {
    try {
      await assignmentsApi.create(form);
      setAssignmentModal(false);
      await loadAssignments();
    } catch (e) {
      setError(e.message || "Failed to create assignment");
    }
  };

  const handleGrade = async (submission) => {
    const draft = gradeDrafts[submission.id] || {};
    if (!draft.score && draft.score !== 0) {
      setError("Please enter a score before grading");
      return;
    }
    try {
      await assignmentsApi.review(activeSubmissions.id, submission.user_id, draft.score, draft.feedback || "");
      setSubmissions(prev => prev.map(s => s.id === submission.id
        ? { ...s, status: "graded", score: draft.score, feedback: draft.feedback || "", graded_at: new Date().toISOString() }
        : s));
      setGradeDrafts(prev => ({ ...prev, [submission.id]: { score: "", feedback: "" } }));
      await loadAssignments();
    } catch (e) {
      setError(e.message || "Failed to grade submission");
    }
  };

  const filteredContent = content.filter(c =>
    !contentSearch ||
    c.title?.toLowerCase().includes(contentSearch.toLowerCase()) ||
    c.category?.toLowerCase().includes(contentSearch.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-surface-base px-4 py-8 max-w-6xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="flex items-center justify-between">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-500/10 border border-red-500/20 mb-3">
              <ClipboardList size={14} className="text-red-400" />
              <span className="text-xs font-mono text-red-400">ADMIN</span>
            </div>
            <h1 className="text-3xl font-display font-black text-text-primary">Content & Assignments</h1>
          </div>
        </div>

        <div className="mt-6 flex gap-2 bg-white border border-nature-leaf/20 rounded-xl p-1.5 w-fit">
          <TabButton active={tab === "content"} onClick={() => setTab("content")} icon={BookOpen} label="Content Modules" />
          <TabButton active={tab === "assignments"} onClick={() => setTab("assignments")} icon={ClipboardList} label="Assignments" />
        </div>
      </motion.div>

      {error && (
        <div className="mb-6 px-4 py-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-500 text-sm font-mono flex items-center justify-between">
          <span>{error}</span>
          <button onClick={() => setError("")} className="text-red-500 hover:text-red-600">
            <X size={14} />
          </button>
        </div>
      )}

      {tab === "content" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <div className="flex items-center justify-between mb-5 gap-4 flex-wrap">
            <div className="relative flex-1 min-w-[220px] max-w-md">
              <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-brand-secondary" />
              <input
                value={contentSearch}
                onChange={e => setContentSearch(e.target.value)}
                placeholder="Search modules..."
                className={`${inputCls} pl-10`}
              />
            </div>
            <button
              onClick={() => setContentModal({ mode: "create" })}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-nature-leaf hover:bg-nature-moss text-text-primary text-sm font-semibold transition-all">
              <Plus size={16} />
              New Module
            </button>
          </div>

          {contentLoading ? (
            <div className="flex justify-center py-20"><Spinner /></div>
          ) : filteredContent.length === 0 ? (
            <div className="glass rounded-xl p-16 text-center text-text-muted font-mono text-sm">
              No content modules found. Create your first one!
            </div>
          ) : (
            <div className="space-y-3">
              {filteredContent.map((c, i) => (
                <motion.div
                  key={c.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: Math.min(i * 0.03, 0.3) }}
                  className="glass rounded-xl p-5 flex flex-col md:flex-row md:items-center gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 flex-wrap">
                      <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-surface-card border border-nature-leaf/30">
                        <Layers size={14} className="text-nature-blossom" />
                      </span>
                      <h3 className="font-display font-bold text-text-primary">{c.title}</h3>
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono uppercase border ${CATEGORY_COLORS[c.category] || CATEGORY_COLORS.dsa}`}>
                        {c.category}
                      </span>
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono uppercase border ${DIFFICULTY_COLORS[c.difficulty] || DIFFICULTY_COLORS.beginner}`}>
                        {c.difficulty}
                      </span>
                      <span className="text-[10px] font-mono text-text-muted">order #{c.order}</span>
                    </div>
                    <p className="mt-2 text-sm text-text-muted line-clamp-2">
                      {c.description || c.body?.slice(0, 140) || "No description"}
                    </p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setContentModal({ mode: "edit", item: c })}
                      className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-surface-card border border-nature-leaf/20 text-text-secondary text-xs font-mono hover:text-text-primary hover:border-nature-leaf/30 transition-all">
                      <Pencil size={13} />
                      Edit
                    </button>
                    <button
                      onClick={() => handleContentDelete(c)}
                      className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-surface-card border border-nature-leaf/20 text-text-secondary text-xs font-mono hover:text-red-500 hover:border-red-500/40 transition-all">
                      <Trash2 size={13} />
                      Delete
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      {tab === "assignments" && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <div className="flex items-center justify-between mb-5">
            <p className="text-sm font-mono text-text-muted">{assignments.length} assignments</p>
            <button
              onClick={() => setAssignmentModal(true)}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-nature-leaf hover:bg-nature-moss text-text-primary text-sm font-semibold transition-all">
              <Plus size={16} />
              New Assignment
            </button>
          </div>

          {assignmentsLoading ? (
            <div className="flex justify-center py-20"><Spinner /></div>
          ) : assignments.length === 0 ? (
            <div className="glass rounded-xl p-16 text-center text-text-muted font-mono text-sm">
              No assignments yet. Create one to get started!
            </div>
          ) : (
            <div className="space-y-3">
              {assignments.map((a, i) => (
                <motion.div
                  key={a.id}
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: Math.min(i * 0.03, 0.3) }}
                  className="glass rounded-xl p-5">
                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className="flex items-center justify-center w-8 h-8 rounded-lg bg-brand-primary/10 border border-nature-leaf/30">
                          <FileText size={14} className="text-brand-primary" />
                        </span>
                        <h3 className="font-display font-bold text-text-primary">{a.title}</h3>
                        {a.content_title && (
                          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono border bg-surface-card text-nature-blossom border-nature-leaf/30">
                            {a.content_title}
                          </span>
                        )}
                      </div>
                      <p className="mt-2 text-sm text-text-muted">{a.description || "No description"}</p>
                      <div className="mt-3 flex flex-wrap gap-4 text-xs font-mono text-text-muted">
                        <span className="flex items-center gap-1.5">
                          <Users size={12} className="text-nature-blossom" />
                          {a.assigned_to === "all" ? "All users" : `${a.assigned_to.length} user${a.assigned_to.length === 1 ? "" : "s"}`}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Calendar size={12} className="text-sky-400" />
                          Due {formatDate(a.due_date)}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Award size={12} className="text-amber-400" />
                          Max {a.max_score}
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Send size={12} className="text-sky-400" />
                          {a.submission_count || 0} submitted
                        </span>
                        <span className="flex items-center gap-1.5">
                          <CheckCircle2 size={12} className="text-brand-primary" />
                          {a.graded_count || 0} graded
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={() => openSubmissions(a)}
                      className="flex items-center gap-2 px-4 py-2 rounded-xl bg-surface-card border border-nature-leaf/20 text-text-secondary text-xs font-mono hover:text-text-primary hover:border-nature-leaf/30 transition-all">
                      <ClipboardList size={13} />
                      View Submissions
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      <AnimatePresence>
        {contentModal && (
          <Modal
            title={contentModal.mode === "edit" ? "Edit Content Module" : "New Content Module"}
            onClose={() => setContentModal(null)}>
            <ContentForm
              key={contentModal.mode === "edit" ? contentModal.item.id : "new"}
              initial={contentModal.mode === "edit" ? contentModal.item : null}
              onSave={handleContentSave}
              onCancel={() => setContentModal(null)}
            />
          </Modal>
        )}

        {assignmentModal && (
          <Modal title="New Assignment" onClose={() => setAssignmentModal(false)}>
            <AssignmentForm
              contentOptions={content}
              onSave={handleAssignmentCreate}
              onCancel={() => setAssignmentModal(false)}
            />
          </Modal>
        )}

        {activeSubmissions && (
          <Modal
            title={`Submissions — ${activeSubmissions.title}`}
            onClose={() => setActiveSubmissions(null)}
            wide>
            {submissionsLoading ? (
              <div className="flex justify-center py-16"><Spinner /></div>
            ) : submissions.length === 0 ? (
              <div className="text-center py-14 text-text-muted font-mono text-sm">No submissions yet.</div>
            ) : (
              <div className="space-y-4">
                {submissions.map(s => (
                  <div key={s.id} className="rounded-xl bg-surface-base border border-nature-leaf/20 p-4">
                    <div className="flex items-center justify-between gap-3 flex-wrap mb-3">
                      <div className="flex items-center gap-2 min-w-0">
                        <span className="w-7 h-7 rounded-full bg-surface-card border border-nature-leaf/30 flex items-center justify-center text-[10px] font-mono text-nature-blossom">
                          {(s.user_name || "?").charAt(0).toUpperCase()}
                        </span>
                        <div className="min-w-0">
                          <p className="text-sm font-semibold text-text-primary truncate">{s.user_name || "Unknown"}</p>
                          <p className="text-[10px] font-mono text-text-muted">{s.user_email || s.user_id}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <StatusBadge status={s.status} />
                        <span className="text-[10px] font-mono text-text-muted">submitted {formatDate(s.submitted_at)}</span>
                      </div>
                    </div>

                    <div className="rounded-lg bg-surface-card border border-[#EDEAE0] p-3 text-sm text-text-secondary whitespace-pre-wrap mb-3">
                      {s.answer_text || "(empty answer)"}
                    </div>

                    {s.status === "graded" ? (
                      <div className="flex items-start gap-4 flex-wrap">
                        <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-brand-primary/10 border border-brand-primary/20">
                          <Award size={14} className="text-brand-primary" />
                          <span className="text-sm font-bold text-brand-primary">{s.score}</span>
                          <span className="text-[10px] font-mono text-text-muted">/ {activeSubmissions.max_score}</span>
                        </div>
                        <div className="flex-1 min-w-[200px]">
                          <p className="text-[10px] font-mono uppercase tracking-[0.2em] text-text-muted mb-1">Feedback</p>
                          <p className="text-sm text-text-secondary whitespace-pre-wrap">{s.feedback || "—"}</p>
                        </div>
                      </div>
                    ) : (
                      <div className="grid md:grid-cols-[120px_1fr_auto] gap-3 items-start">
                        <div>
                          <p className="text-[10px] font-mono uppercase tracking-[0.2em] text-text-muted mb-1">Score</p>
                          <input
                            type="number"
                            min="0"
                            max={activeSubmissions.max_score}
                            value={gradeDrafts[s.id]?.score ?? ""}
                            onChange={e => setGradeDrafts(prev => ({ ...prev, [s.id]: { ...(prev[s.id] || {}), score: e.target.value } }))}
                            placeholder="0"
                            className={inputCls}
                          />
                        </div>
                        <div>
                          <p className="text-[10px] font-mono uppercase tracking-[0.2em] text-text-muted mb-1">Feedback</p>
                          <textarea
                            rows={2}
                            value={gradeDrafts[s.id]?.feedback ?? ""}
                            onChange={e => setGradeDrafts(prev => ({ ...prev, [s.id]: { ...(prev[s.id] || {}), feedback: e.target.value } }))}
                            placeholder="Write feedback for the student..."
                            className={`${inputCls} resize-none`}
                          />
                        </div>
                        <button
                          onClick={() => handleGrade(s)}
                          className="mt-6 flex items-center gap-2 px-4 py-2.5 rounded-xl bg-brand-primary/90 hover:bg-brand-primary text-text-primary text-sm font-semibold transition-all">
                          <CheckCircle2 size={15} />
                          Grade
                        </button>
                      </div>
                    )}
                  </div>
                ))}
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
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-mono transition-all ${
        active
          ? "bg-nature-leaf text-text-primary shadow-lg shadow-[#4F8F57]/20"
          : "text-text-muted hover:text-text-primary hover:bg-surface-card"
      }`}>
      <Icon size={15} />
      {label}
    </button>
  );
}

function ContentForm({ initial, onSave, onCancel }: any) {
  const [form, setForm] = useState({
    title: initial?.title || "",
    description: initial?.description || "",
    category: initial?.category || "dsa",
    difficulty: initial?.difficulty || "beginner",
    body: initial?.body || "",
    order: Number(initial?.order) ?? 0,
  });

  const set = (key, value) => setForm(prev => ({ ...prev, [key]: value }));

  return (
    <form
      onSubmit={e => { e.preventDefault(); onSave(form); }}
      className="space-y-4">
      <Field label="Title">
        <input required value={form.title} onChange={e => set("title", e.target.value)} placeholder="e.g. Arrays Deep Dive" className={inputCls} />
      </Field>
      <Field label="Description">
        <input value={form.description} onChange={e => set("description", e.target.value)} placeholder="Short summary shown in lists" className={inputCls} />
      </Field>
      <div className="grid grid-cols-2 gap-4">
        <Field label="Category">
          <select value={form.category} onChange={e => set("category", e.target.value)} className={inputCls}>
            {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
          </select>
        </Field>
        <Field label="Difficulty">
          <select value={form.difficulty} onChange={e => set("difficulty", e.target.value)} className={inputCls}>
            {DIFFICULTIES.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
        </Field>
      </div>
      <Field label="Order">
        <input
          type="number"
          value={form.order}
          onChange={e => set("order", Number(e.target.value))}
          placeholder="0"
          className={inputCls}
        />
      </Field>
      <Field label="Body">
        <textarea
          required
          rows={8}
          value={form.body}
          onChange={e => set("body", e.target.value)}
          placeholder="Full lesson content... Markdown supported"
          className={`${inputCls} resize-none font-mono text-xs leading-relaxed`}
        />
      </Field>
      <div className="flex justify-end gap-3 pt-2">
        <button type="button" onClick={onCancel} className="px-4 py-2.5 rounded-xl bg-surface-card border border-nature-leaf/20 text-text-secondary text-sm font-mono hover:text-text-primary transition-all">
          Cancel
        </button>
        <button type="submit" className="px-4 py-2.5 rounded-xl bg-nature-leaf hover:bg-nature-moss text-text-primary text-sm font-semibold transition-all">
          {initial ? "Save Changes" : "Create Module"}
        </button>
      </div>
    </form>
  );
}

function AssignmentForm({ contentOptions, onSave, onCancel }: any) {
  const [form, setForm] = useState({
    title: "",
    description: "",
    content_id: "",
    assigned_to: "",
    due_date: "",
    max_score: 100,
  });

  const [saving, setSaving] = useState(false);

  const set = (key: string, value: any) => setForm(prev => ({ ...prev, [key]: value }));

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = {
        title: form.title,
        description: form.description,
        content_id: form.content_id || null,
        assigned_to: form.assigned_to.trim().toLowerCase() === "all"
          ? "all"
          : form.assigned_to.split(/[,\s;]+/).map(s => s.trim()).filter(Boolean),
        due_date: form.due_date ? new Date(form.due_date).toISOString() : null,
        max_score: Number(form.max_score) || 100,
      };
      await onSave(payload);
    } finally {
      setSaving(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Field label="Title">
        <input required value={form.title} onChange={e => set("title", e.target.value)} placeholder="e.g. Week 1 — Arrays Assignment" className={inputCls} />
      </Field>
      <Field label="Description">
        <textarea rows={3} value={form.description} onChange={e => set("description", e.target.value)} placeholder="Instructions for the student..." className={`${inputCls} resize-none`} />
      </Field>
      <Field label="Content Module (optional)">
        <select value={form.content_id} onChange={e => set("content_id", e.target.value)} className={inputCls}>
          <option value="">None</option>
          {contentOptions.map(c => <option key={c.id} value={c.id}>{c.title}</option>)}
        </select>
      </Field>
      <Field label="Assigned To (comma-separated emails, or 'all')">
        <input value={form.assigned_to} onChange={e => set("assigned_to", e.target.value)} placeholder="student@email.com, another@email.com, ... or 'all'" className={inputCls} />
      </Field>
      <div className="grid grid-cols-2 gap-4">
        <Field label="Due Date">
          <input type="datetime-local" value={form.due_date} onChange={e => set("due_date", e.target.value)} className={inputCls} />
        </Field>
        <Field label="Max Score">
          <input type="number" min="1" value={form.max_score} onChange={e => set("max_score", Number(e.target.value))} className={inputCls} />
        </Field>
      </div>
      <div className="flex justify-end gap-3 pt-2">
        <button type="button" onClick={onCancel} className="px-4 py-2.5 rounded-xl bg-surface-card border border-nature-leaf/20 text-text-secondary text-sm font-mono hover:text-text-primary transition-all">
          Cancel
        </button>
        <button type="submit" disabled={saving} className="px-4 py-2.5 rounded-xl bg-brand-primary/90 hover:bg-brand-primary text-text-primary text-sm font-semibold transition-all disabled:opacity-50">
          {saving ? "Creating..." : "Create Assignment"}
        </button>
      </div>
    </form>
  );
}
