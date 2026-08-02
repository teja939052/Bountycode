import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft, ThumbsUp, Eye, Share2, Trash2, Star, MessageSquare,
  User, Code2, Loader2, Check, Calendar, Hash,
} from "lucide-react";
import { showcaseApi } from "../services/api/showcase.ts";
import useAuthStore from "../store/authStore";
import Skeleton from "../components/ui/Skeleton";

function StarRating({ value, onChange, size = "w-6 h-6", disabled = false }: any) {
  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3, 4, 5].map(n => (
        <button
          key={n}
          type="button"
          disabled={disabled}
          onClick={() => onChange && onChange(n)}
          className={`${disabled ? "cursor-default" : "cursor-pointer hover:scale-125"} transition-transform`}
        >
          <Star
            className={`${size} ${
              n <= value ? "text-amber-400 fill-amber-400" : "text-slate-600"
            }`}
          />
        </button>
      ))}
    </div>
  );
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

export default function ShowcaseDetail() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [liked, setLiked] = useState(false);
  const [comment, setComment] = useState("");
  const [rating, setRating] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [copied, setCopied] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const loadProject = useCallback(async () => {
    setLoading(true);
    try {
      const data = await showcaseApi.getById(projectId);
      setProject(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => { loadProject(); }, [loadProject]);

  const handleLike = async () => {
    if (!user) {
      navigate("/login");
      return;
    }
    if (liked) return;
    try {
      const result = await showcaseApi.like(projectId);
      setProject(prev => ({ ...prev, likes: result.likes }));
      setLiked(true);
    } catch (e) {
      setError(e.message);
    }
  };

  const handleReview = async () => {
    if (!user) {
      navigate("/login");
      return;
    }
    if (!comment.trim() || rating < 1) return;
    setSubmitting(true);
    try {
      const review = await showcaseApi.addReview(projectId, comment, rating);
      setProject(prev => ({
        ...prev,
        reviews: [...(prev.reviews || []), review],
        review_count: (prev.review_count || 0) + 1,
      }));
      setComment("");
      setRating(0);
    } catch (e) {
      setError(e.message);
    } finally {
      setSubmitting(false);
    }
  };

  const handleShare = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      setCopied(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm("Delete this project permanently?")) return;
    setDeleting(true);
    try {
      await showcaseApi.remove(projectId);
      navigate("/showcase");
    } catch (e) {
      setError(e.message);
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Skeleton className="h-8 w-1/3 mb-4" />
        <Skeleton className="h-64 w-full mb-6" />
        <Skeleton className="h-32 w-full" />
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center text-center px-4">
        <Code2 className="w-16 h-16 text-slate-600 mb-4" />
        <h3 className="text-lg font-semibold text-slate-300 mb-2">{error || "Project not found"}</h3>
        <button
          onClick={() => navigate("/showcase")}
          className="mt-4 flex items-center gap-2 px-4 py-2 rounded-xl border border-white/10 bg-white/5 text-sm text-slate-300 hover:border-emerald-500/40"
        >
          <ArrowLeft className="w-4 h-4" /> Back to gallery
        </button>
      </div>
    );
  }

  const isAuthor = user && String(project.author_id) === String(user.id);

  return (
    <div className="min-h-screen">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-10">
        <button
          onClick={() => navigate("/showcase")}
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-emerald-300 transition-colors mb-6"
        >
          <ArrowLeft className="w-4 h-4" /> Back to gallery
        </button>

        {error && (
          <div className="mb-6 rounded-xl border border-rose-500/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-300">
            {error}
          </div>
        )}

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="rounded-2xl border border-white/10 bg-white/5 p-6 mb-6"
        >
          <div className="flex items-start justify-between gap-4 mb-3">
            <h1 className="text-2xl sm:text-3xl font-display font-bold text-white">{project.title}</h1>
            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={handleShare}
                className="p-2.5 rounded-xl border border-white/10 bg-white/5 text-slate-400 hover:text-emerald-300 hover:border-emerald-500/40 transition-all"
                title="Copy link"
              >
                {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Share2 className="w-4 h-4" />}
              </button>
              {isAuthor && (
                <button
                  onClick={handleDelete}
                  disabled={deleting}
                  className="p-2.5 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-400 hover:bg-rose-500/20 transition-all"
                  title="Delete project"
                >
                  {deleting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Trash2 className="w-4 h-4" />}
                </button>
              )}
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 mb-4">
            <span className="flex items-center gap-1.5">
              <User className="w-3.5 h-3.5" /> {project.author_name}
            </span>
            <span className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5" /> {formatDate(project.created_at)}
            </span>
            <span className="flex items-center gap-1.5">
              <Eye className="w-3.5 h-3.5" /> {project.views || 0} views
            </span>
          </div>

          <p className="text-sm text-slate-300 leading-relaxed mb-4">{project.description}</p>

          <div className="flex flex-wrap items-center gap-2 mb-5">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border border-emerald-500/30 bg-emerald-500/10 text-emerald-400">
              {project.language}
            </span>
            {project.tags.map(tag => (
              <span key={tag} className="flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-mono font-medium border border-indigo-500/30 bg-indigo-500/10 text-indigo-400">
                <Hash className="w-2.5 h-2.5" /> {tag}
              </span>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleLike}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-medium transition-all ${
                liked
                  ? "border-emerald-500/50 bg-emerald-500/15 text-emerald-300"
                  : "border-white/10 bg-white/5 text-slate-300 hover:border-emerald-500/40 hover:text-emerald-300"
              }`}
            >
              <ThumbsUp className={`w-4 h-4 ${liked ? "fill-emerald-400" : ""}`} />
              {project.likes || 0} {liked ? "Liked" : "Like"}
            </button>
            <span className="flex items-center gap-2 text-sm text-slate-500">
              <MessageSquare className="w-4 h-4" />
              {(project.review_count || (project.reviews || []).length)} reviews
            </span>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
          className="rounded-2xl border border-white/10 bg-white/5 overflow-hidden mb-6"
        >
          <div className="flex items-center justify-between px-6 py-3 border-b border-white/10 bg-white/[0.03]">
            <span className="text-xs font-mono uppercase tracking-wider text-slate-500">Code</span>
            <span className="text-xs font-mono text-slate-500">{project.language}</span>
          </div>
          <pre className="p-6 text-sm leading-relaxed font-mono text-emerald-200 bg-black/40 overflow-x-auto whitespace-pre">
            {project.code}
          </pre>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="rounded-2xl border border-white/10 bg-white/5 p-6"
        >
          <h2 className="text-lg font-display font-semibold text-white flex items-center gap-2 mb-5">
            <MessageSquare className="w-5 h-5 text-indigo-400" />
            Peer Reviews
            <span className="text-sm font-normal text-slate-500">
              ({(project.reviews || []).length})
            </span>
          </h2>

          <div className="rounded-xl border border-white/10 bg-white/[0.03] p-4 mb-6">
            <div className="flex flex-col sm:flex-row sm:items-center gap-4">
              <div className="flex-1">
                <label className="block text-xs font-mono uppercase tracking-wider text-slate-500 mb-2">Your review</label>
                <textarea
                  value={comment}
                  onChange={e => setComment(e.target.value)}
                  placeholder="Share constructive feedback on this code..."
                  rows={3}
                  className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/20 transition-all resize-none"
                />
              </div>
              <div className="flex flex-col items-start sm:items-end gap-3 shrink-0">
                <div>
                  <label className="block text-xs font-mono uppercase tracking-wider text-slate-500 mb-1.5">Rating</label>
                  <StarRating value={rating} onChange={setRating} />
                </div>
                <button
                  onClick={handleReview}
                  disabled={submitting || !comment.trim() || rating < 1}
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-indigo-600 text-sm font-semibold text-white disabled:opacity-40 hover:from-indigo-400 hover:to-indigo-500 transition-all"
                >
                  {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Star className="w-4 h-4" />}
                  {submitting ? "Submitting..." : "Submit Review"}
                </button>
              </div>
            </div>
          </div>

          {(project.reviews || []).length === 0 ? (
            <p className="text-sm text-slate-500 text-center py-8">
              No reviews yet. Be the first to give feedback!
            </p>
          ) : (
            <div className="space-y-4">
              {project.reviews.map(review => (
                <motion.div
                  key={review.id || `${review.author_id}-${review.created_at}`}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="rounded-xl border border-white/10 bg-white/[0.03] p-4"
                >
                  <div className="flex items-center justify-between gap-3 mb-2">
                    <span className="flex items-center gap-2 text-sm font-medium text-slate-200">
                      <User className="w-4 h-4 text-indigo-400" />
                      {review.author_name}
                    </span>
                    <div className="flex items-center gap-3">
                      <StarRating value={review.rating} disabled size="w-4 h-4" />
                      <span className="text-xs text-slate-500">{formatDate(review.created_at)}</span>
                    </div>
                  </div>
                  <p className="text-sm text-slate-300 leading-relaxed">{review.comment}</p>
                </motion.div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
