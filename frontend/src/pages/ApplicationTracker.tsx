import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import {
  Plus, Trash2, ExternalLink, Calendar, Building2, Briefcase,
  ChevronDown, ChevronUp, BarChart3, X
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import AnimatedCard from "../components/motion/AnimatedCard";

const STAGE_COLORS = {
  interested: "bg-surface-card/50 dark:bg-gray-700 text-brand-primary dark:text-brand-secondary",
  applied: "bg-brand-sky/10 dark:bg-blue-900/30 text-brand-sky dark:text-blue-400",
  oa_received: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400",
  interview_scheduled: "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400",
  interview_completed: "bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400",
  offer_received: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  accepted: "bg-brand-emerald/10 dark:bg-emerald-900/30 text-brand-emerald dark:text-emerald-400",
  rejected: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400",
  withdrawn: "bg-surface-card/50 dark:bg-gray-800 text-gray-500 dark:text-brand-muted",
};

const PIPELINE_COLUMNS = [
  { key: "interested", label: "Interested" },
  { key: "applied", label: "Applied" },
  { key: "oa_received", label: "OA Received" },
  { key: "interview_scheduled", label: "Interview" },
  { key: "interview_completed", label: "Done" },
  { key: "offer_received", label: "Offer" },
  { key: "accepted", label: "Accepted" },
  { key: "rejected", label: "Rejected" },
];

export default function ApplicationTracker() {
  const [apps, setApps] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ company: "", role: "", job_url: "", notes: "" });
  const [saving, setSaving] = useState(false);
  const [expandedId, setExpandedId] = useState(null);
  const reduced = useReducedMotion();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [pipeline, statsData] = await Promise.all([
        api.getApplicationPipeline(),
        api.getApplicationStats().catch(() => null),
      ]);
      setApps(pipeline || []);
      setStats(statsData);
    } catch {} finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.createApplication(form.company, form.role, form.job_url, form.notes);
      setForm({ company: "", role: "", job_url: "", notes: "" });
      setShowForm(false);
      loadData();
    } catch {} finally {
      setSaving(false);
    }
  };

  const handleStageChange = async (appId, newStage) => {
    await api.updateApplicationStage(appId, newStage);
    loadData();
  };

  const handleDelete = async (appId) => {
    await api.deleteApplication(appId);
    loadData();
  };

  const appsByStage = PIPELINE_COLUMNS.reduce((acc, col) => {
    acc[col.key] = (apps || []).filter((a) => a.stage === col.key);
    return acc;
  }, {});

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <motion.div className="mb-8" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-xl flex items-center justify-center">
                <Briefcase size={24} className="text-indigo-600" />
              </div>
              <div>
                <h1 className="text-3xl font-bold dark:text-white">Application Tracker</h1>
                <p className="text-brand-secondary dark:text-brand-muted">Kanban board for your job applications</p>
              </div>
            </div>
            <button onClick={() => setShowForm(true)} className="btn-primary flex items-center gap-2">
              <Plus size={18} /> Add Application
            </button>
          </div>
        </motion.div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
            {[
              { label: "Total", value: stats.total_applications, color: "text-brand-secondary dark:text-brand-muted" },
              { label: "Applied", value: stats.by_stage?.applied?.count || 0, color: "text-blue-600" },
              { label: "Interview", value: (stats.by_stage?.interview_scheduled?.count || 0) + (stats.by_stage?.interview_completed?.count || 0), color: "text-purple-600" },
              { label: "Offers", value: stats.by_stage?.offer_received?.count || 0, color: "text-green-600" },
            ].map((s, i) => (
              <AnimatedCard key={s.label} delay={i * 0.05} className="card text-center">
                <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
                <p className="text-xs text-gray-500">{s.label}</p>
              </AnimatedCard>
            ))}
          </div>
        )}

        {/* Add Application Modal */}
        <AnimatePresence>
          {showForm && (
            <motion.div
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              onClick={() => setShowForm(false)}
            >
              <motion.div
                className="bg-surface-card dark:bg-gray-900 rounded-2xl p-6 max-w-md w-full"
                initial={{ scale: 0.9, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.9, opacity: 0 }}
                onClick={(e) => e.stopPropagation()}
              >
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-bold dark:text-white">New Application</h2>
                  <button onClick={() => setShowForm(false)} className="text-brand-muted hover:text-brand-secondary">
                    <X size={20} />
                  </button>
                </div>
                <form onSubmit={handleCreate} className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-brand-primary dark:text-brand-secondary mb-1">Company</label>
                    <input className="input" value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-brand-primary dark:text-brand-secondary mb-1">Role</label>
                    <input className="input" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} required />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-brand-primary dark:text-brand-secondary mb-1">Job URL</label>
                    <input className="input" value={form.job_url} onChange={(e) => setForm({ ...form, job_url: e.target.value })} />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-brand-primary dark:text-brand-secondary mb-1">Notes</label>
                    <textarea className="input" rows={3} value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
                  </div>
                  <div className="flex gap-3">
                    <button type="button" onClick={() => setShowForm(false)} className="flex-1 btn-secondary">Cancel</button>
                    <button type="submit" disabled={saving} className="flex-1 btn-primary">{saving ? "Saving..." : "Save"}</button>
                  </div>
                </form>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Kanban Board */}
        {apps.length === 0 ? (
          <div className="card text-center py-12">
            <Briefcase size={48} className="mx-auto text-brand-secondary dark:text-brand-secondary mb-4" />
            <p className="text-gray-500 dark:text-brand-muted mb-4">No applications tracked yet</p>
            <button onClick={() => setShowForm(true)} className="btn-primary">Add Your First Application</button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {PIPELINE_COLUMNS.map((col) => (
              <div key={col.key} className="min-w-[200px]">
                <div className="flex items-center gap-2 mb-3">
                  <h3 className="font-semibold text-sm dark:text-white">{col.label}</h3>
                  <span className="text-xs text-gray-500">({appsByStage[col.key]?.length || 0})</span>
                </div>
                <div className="space-y-3">
                  <AnimatePresence>
                    {appsByStage[col.key]?.map((app) => (
                      <motion.div
                        key={app.id}
                        layout
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        className="card p-4"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <h4 className="font-semibold text-sm dark:text-white">{app.company}</h4>
                            <p className="text-xs text-gray-500">{app.role}</p>
                          </div>
                          <button onClick={() => handleDelete(app.id)} className="text-brand-muted hover:text-red-500">
                            <Trash2 size={14} />
                          </button>
                        </div>

                        {app.job_url && (
                          <a href={app.job_url} target="_blank" rel="noopener noreferrer" className="text-xs text-primary-600 hover:text-primary-700 flex items-center gap-1 mb-2">
                            <ExternalLink size={12} /> View posting
                          </a>
                        )}

                        {app.notes && (
                          <p className="text-xs text-gray-500 mb-2">{app.notes}</p>
                        )}

                        <div className="flex items-center justify-between">
                          <span className="text-[10px] text-brand-muted">
                            {new Date(app.created_at).toLocaleDateString()}
                          </span>
                          <div className="relative">
                            <select
                              value={app.stage}
                              onChange={(e) => handleStageChange(app.id, e.target.value)}
                              className={`text-[10px] px-2 py-1 rounded-full border-0 font-medium ${STAGE_COLORS[app.stage] || STAGE_COLORS.interested}`}
                            >
                              {PIPELINE_COLUMNS.map((c) => (
                                <option key={c.key} value={c.key}>{c.label}</option>
                              ))}
                            </select>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
