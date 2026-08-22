import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Eye, ThumbsUp, User, Code2, Plus, X, Loader2, Search,
  ChevronLeft, ChevronRight, MessageSquare, Sparkles, Hash,
} from "lucide-react";
import { showcaseApi } from "../services/api/showcase.ts";
import useAuthStore from "../store/authStore";
import Skeleton from "../components/ui/Skeleton";

const LANGUAGES = ["python", "javascript", "typescript", "java", "cpp", "c", "go", "rust", "sql", "html"];

const LANGUAGE_COLORS = {
  python: "border-brand-primary/20 bg-brand-primary/10 text-brand-primary",
  javascript: "border-amber-500/30 bg-amber-500/10 text-amber-400",
  typescript: "border-sky-500/30 bg-sky-500/10 text-sky-400",
  java: "border-orange-500/30 bg-orange-500/10 text-orange-400",
  cpp: "border-brand-primary/20 bg-brand-primary/10 text-brand-primary",
  c: "border-violet-500/30 bg-violet-500/10 text-violet-400",
  go: "border-brand-primary/20 bg-brand-secondary/10 text-brand-secondary",
  rust: "border-rose-500/30 bg-rose-500/10 text-rose-400",
  sql: "border-fuchsia-500/30 bg-fuchsia-500/10 text-fuchsia-400",
  html: "border-red-500/30 bg-red-500/10 text-red-400",
};

function languageColor(lang) {
  return LANGUAGE_COLORS[lang] || "border-indigo-500/30 bg-indigo-500/10 text-indigo-400";
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

export default function Showcase() {
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const [projects, setProjects] = useState([]);
  const [tags, setTags] = useState([]);
  const [activeTag, setActiveTag] = useState("");
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [showPublish, setShowPublish] = useState(false);
  const [publishing, setPublishing] = useState(false);
  const [form, setForm] = useState({
    title: "", description: "", language: "python", tags: "", code: "",
  });
  const [error, setError] = useState("");

  const loadProjects = useCallback(async () => {
    setLoading(true);
    try {
      const data = await showcaseApi.browse({ tag: activeTag, page, limit: 12 });
      setProjects(data.projects || []);
      setTotal(data.total || 0);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [activeTag, page]);

  useEffect(() => { loadProjects(); }, [loadProjects]);

  useEffect(() => {
    showcaseApi.getTags().then(data => setTags(data.tags || [])).catch(() => {});
  }, []);

  useEffect(() => { setPage(1); }, [activeTag]);

  const openPublish = () => {
    if (!user) {
      navigate("/login");
      return;
    }
    setShowPublish(true);
  };

  const handlePublish = async () => {
    setPublishing(true);
    try {
      const parsedTags = form.tags.split(",").map(t => t.trim()).filter(Boolean);
      const project = await showcaseApi.publish({
        title: form.title,
        description: form.description,
        language: form.language,
        tags: parsedTags,
        code: form.code,
      });
      setShowPublish(false);
      setForm({ title: "", description: "", language: "python", tags: "", code: "" });
      navigate(`/showcase/${project.id}`);
    } catch (e) {
      setError(e.message);
    } finally {
      setPublishing(false);
    }
  };

  const totalPages = Math.ceil(total / 12);

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-display font-bold text-white flex items-center gap-3">
              <Code2 className="w-8 h-8 text-brand-primary" />
              Project Showcase
            </h1>
            <p className="text-brand-muted mt-1">
              Share your code snippets, get peer reviews, and level up.
            </p>
          </div>
          <button
            onClick={openPublish}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500/20 to-indigo-500/20 border border-emerald-500/40 text-brand-primary text-sm font-medium hover:border-emerald-400/70 hover:bg-brand-primary/10 transition-all"
          >
            <Plus className="w-4 h-4" />
            Publish Project
          </button>
        </div>

        <AnimatePresence>
          {tags.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="flex flex-wrap items-center gap-2 mb-8"
            >
              <Hash className="w-4 h-4 text-brand-muted" />
              <button
                onClick={() => setActiveTag("")}
                className={`px-3 py-1 rounded-full text-xs font-mono border transition-all ${
                  activeTag === ""
                    ? "border-emerald-500/50 bg-emerald-500/15 text-brand-primary"
                    : "border-brand-primary/10 bg-surface-card/30 text-brand-muted hover:text-slate-200"
                }`}
              >
                All
              </button>
              {tags.map(tag => (
                <button
                  key={tag}
                  onClick={() => setActiveTag(tag === activeTag ? "" : tag)}
                  className={`px-3 py-1 rounded-full text-xs font-mono border transition-all ${
                    activeTag === tag
                      ? "border-emerald-500/50 bg-emerald-500/15 text-brand-primary"
                      : "border-brand-primary/10 bg-surface-card/30 text-brand-muted hover:text-slate-200"
                  }`}
                >
                  {tag}
                </button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {error && (
          <div className="mb-6 rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
            {error}
          </div>
        )}

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
            {Array.from({ length: 6 }).map((_, i) => (
              <div key={i} className="rounded-2xl border border-brand-primary/10 bg-surface-card/30 p-5">
                <Skeleton className="h-4 w-3/4 mb-3" />
                <Skeleton className="h-3 w-full mb-2" />
                <Skeleton className="h-3 w-2/3 mb-4" />
                <Skeleton className="h-24 w-full mb-4" />
                <div className="flex gap-2">
                  <Skeleton className="h-5 w-16 rounded-full" />
                  <Skeleton className="h-5 w-14 rounded-full" />
                </div>
              </div>
            ))}
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-20">
            <Search className="w-16 h-16 mx-auto text-slate-600 mb-4" />
            <h3 className="text-lg font-semibold text-brand-secondary mb-2">No projects found</h3>
            <p className="text-brand-muted text-sm">Be the first to publish a project for this tag.</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {projects.map((project, idx) => (
                <motion.button
                  key={project.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                  onClick={() => navigate(`/showcase/${project.id}`)}
                  className="group relative text-left rounded-2xl border border-brand-primary/10 bg-surface-card/30 p-5 hover:border-emerald-500/40 hover:bg-white/[0.07] transition-all duration-300"
                >
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <h3 className="text-base font-semibold text-slate-100 group-hover:text-brand-primary transition-colors line-clamp-1">
                      {project.title}
                    </h3>
                    <span className={`shrink-0 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border ${languageColor(project.language)}`}>
                      {project.language}
                    </span>
                  </div>

                  <p className="text-xs text-brand-muted line-clamp-2 mb-3 leading-relaxed">
                    {project.description}
                  </p>

                  <pre className="text-[11px] leading-relaxed font-mono text-brand-muted bg-black/30 border border-brand-primary/10 rounded-lg p-3 mb-4 line-clamp-5 overflow-hidden whitespace-pre-wrap">
                    {project.code_preview || "// no preview"}
                  </pre>

                  <div className="flex flex-wrap items-center gap-2 mb-4">
                    {project.tags.slice(0, 3).map(tag => (
                      <span key={tag} className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border border-indigo-500/30 bg-indigo-500/10 text-indigo-400">
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div className="flex items-center gap-4 text-xs text-brand-muted">
                    <span className="flex items-center gap-1.5">
                      <User className="w-3.5 h-3.5" />
                      {project.author_name}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Eye className="w-3.5 h-3.5" />
                      {project.views || 0}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <ThumbsUp className="w-3.5 h-3.5" />
                      {project.likes || 0}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <MessageSquare className="w-3.5 h-3.5" />
                      {project.review_count || 0}
                    </span>
                  </div>
                </motion.button>
              ))}
            </div>

            {totalPages > 1 && (
              <div className="flex items-center justify-center gap-3 mt-10">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage(p => p - 1)}
                  className="flex items-center gap-1 px-4 py-2 rounded-xl border border-brand-primary/10 bg-surface-card/30 text-sm text-brand-secondary disabled:opacity-40 hover:border-emerald-500/40 transition-all"
                >
                  <ChevronLeft className="w-4 h-4" /> Prev
                </button>
                <span className="text-sm text-brand-muted">
                  Page {page} of {totalPages}
                </span>
                <button
                  disabled={page >= totalPages}
                  onClick={() => setPage(p => p + 1)}
                  className="flex items-center gap-1 px-4 py-2 rounded-xl border border-brand-primary/10 bg-surface-card/30 text-sm text-brand-secondary disabled:opacity-40 hover:border-emerald-500/40 transition-all"
                >
                  Next <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            )}
          </>
        )}
      </div>

      <AnimatePresence>
        {showPublish && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4"
            onClick={() => setShowPublish(false)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              onClick={e => e.stopPropagation()}
              className="rounded-3xl border border-brand-primary/10 bg-slate-900 p-6 sm:p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-display font-bold text-white flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-brand-primary" />
                  Publish Project
                </h2>
                <button
                  onClick={() => setShowPublish(false)}
                  className="p-2 rounded-lg text-brand-muted hover:text-slate-200 hover:bg-surface-card/30"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-brand-muted mb-1.5">Title</label>
                  <input
                    type="text"
                    value={form.title}
                    onChange={e => setForm({ ...form, title: e.target.value })}
                    placeholder="e.g. Real-time chat with WebSockets"
                    className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-2.5 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all"
                  />
                </div>

                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-brand-muted mb-1.5">Description</label>
                  <textarea
                    value={form.description}
                    onChange={e => setForm({ ...form, description: e.target.value })}
                    placeholder="What does this project do?"
                    rows={2}
                    className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-2.5 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all resize-none"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-mono uppercase tracking-wider text-brand-muted mb-1.5">Language</label>
                    <select
                      value={form.language}
                      onChange={e => setForm({ ...form, language: e.target.value })}
                      className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-2.5 text-sm text-slate-200 focus:outline-none focus:border-emerald-500/50"
                    >
                      {LANGUAGES.map(l => <option key={l} value={l}>{l}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-mono uppercase tracking-wider text-brand-muted mb-1.5">Tags (comma-separated)</label>
                    <input
                      type="text"
                      value={form.tags}
                      onChange={e => setForm({ ...form, tags: e.target.value })}
                      placeholder="react, websockets, realtime"
                      className="w-full rounded-xl border border-brand-primary/10 bg-surface-card/30 px-4 py-2.5 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-brand-muted mb-1.5">Code</label>
                  <textarea
                    value={form.code}
                    onChange={e => setForm({ ...form, code: e.target.value })}
                    placeholder="Paste your code snippet..."
                    rows={10}
                    className="w-full rounded-xl border border-brand-primary/10 bg-black/30 px-4 py-3 text-sm font-mono text-emerald-200 placeholder-slate-600 focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all resize-y"
                  />
                </div>

                {error && (
                  <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
                    {error}
                  </div>
                )}

                <div className="flex justify-end gap-3 pt-2">
                  <button
                    onClick={() => setShowPublish(false)}
                    className="px-5 py-2.5 rounded-xl border border-brand-primary/10 bg-surface-card/30 text-sm font-medium text-brand-secondary hover:text-slate-100 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handlePublish}
                    disabled={publishing || !form.title.trim() || !form.code.trim()}
                    className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-emerald-600 text-sm font-semibold text-slate-950 disabled:opacity-40 hover:from-emerald-400 hover:to-emerald-500 transition-all"
                  >
                    {publishing ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                    {publishing ? "Publishing..." : "Publish"}
                  </button>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
