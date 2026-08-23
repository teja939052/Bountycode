import { useState, useEffect, useCallback } from "react";
import { peerReviewApi } from "../services/api/peerReview.ts";
import {
  FileCode2, Plus, Inbox, Handshake, Loader2, Send, Star,
  ClipboardCheck, Code2, Users,
} from "lucide-react";

const TABS = [
  { key: "submit", label: "Submit Code", icon: Plus },
  { key: "my", label: "My Submissions", icon: Inbox },
  { key: "queue", label: "Review Queue", icon: Handshake },
];

const STATUS_BADGE = {
  pending: "bg-amber-100 text-amber-700",
  claimed: "bg-sky-100 text-sky-700",
  reviewed: "bg-green-100 text-green-700",
};

export default function PeerReview() {
  const [tab, setTab] = useState("submit");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [myItems, setMyItems] = useState([]);
  const [queue, setQueue] = useState([]);

  const [form, setForm] = useState({ title: "", language: "python", code: "", description: "" });
  const [saving, setSaving] = useState(false);

  const [claimed, setClaimed] = useState(null);
  const [review, setReview] = useState({ comments: "", rating: 3, strengths: "", improvements: "" });
  const [submitting, setSubmitting] = useState(false);

  const loadMy = useCallback(async () => {
    try {
      const res = await peerReviewApi.my();
      setMyItems(res.items || []);
    } catch {
      // ignore
    }
  }, []);

  const loadQueue = useCallback(async () => {
    try {
      const res = await peerReviewApi.queue(20);
      setQueue(res.items || []);
    } catch {
      // ignore
    }
  }, []);

  const loadAll = useCallback(async () => {
    setLoading(true);
    await Promise.all([loadMy(), loadQueue()]);
    setLoading(false);
  }, [loadMy, loadQueue]);

  useEffect(() => {
    loadAll();
  }, [loadAll]);

  const handleSubmit = async () => {
    if (!form.title.trim() || form.code.trim().length < 10) return;
    setSaving(true);
    setError("");
    try {
      await peerReviewApi.submit({
        title: form.title,
        language: form.language,
        code: form.code,
        description: form.description,
      });
      setForm({ title: "", language: "python", code: "", description: "" });
      setTab("my");
      loadAll();
    } catch (e) {
      setError(e.message || "Could not submit code");
    } finally {
      setSaving(false);
    }
  };

  const handleClaim = async (item) => {
    setError("");
    try {
      await peerReviewApi.claim(item.id);
      setClaimed(item);
      setReview({ comments: "", rating: 3, strengths: "", improvements: "" });
      loadQueue();
    } catch (e) {
      setError(e.message || "Could not claim item");
    }
  };

  const handleSubmitReview = async () => {
    if (!claimed || review.comments.trim().length < 10) return;
    setSubmitting(true);
    setError("");
    try {
      await peerReviewApi.review(claimed.id, {
        comments: review.comments,
        rating: review.rating,
        strengths: review.strengths,
        improvements: review.improvements,
      });
      setClaimed(null);
      setTab("my");
      loadAll();
    } catch (e) {
      setError(e.message || "Could not submit review");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-display font-extrabold text-text-primary flex items-center gap-3">
          <FileCode2 className="text-brand-coral" size={32} />
          Peer Code Review
        </h1>
        <p className="text-text-light mt-1">
          Share your code, get honest reviews from fellow candidates, and sharpen your eye reviewing theirs
        </p>
      </div>

      {error && (
        <div className="mb-6 p-3 rounded-xl border border-red-200 bg-red-50 text-red-600 text-sm">{error}</div>
      )}

      <div className="flex gap-2 mb-6 flex-wrap">
        {TABS.map((t) => {
          const Icon = t.icon;
          return (
            <button
              key={t.key}
              onClick={() => { setTab(t.key); if (t.key === "queue") loadQueue(); }}
              className={`px-4 py-2 rounded-xl text-sm font-semibold flex items-center gap-2 transition-colors ${
                tab === t.key ? "bg-brand-sky text-text-primary shadow-sm" : "bg-white border-border/80 border border-white/60 text-text-light hover:text-text-primary"
              }`}
            >
              <Icon size={16} /> {t.label}
              {t.key === "queue" && queue.filter((i) => i.status === "pending").length > 0 && (
                <span className="px-1.5 py-0.5 rounded-full bg-red-500 text-text-primary text-[10px] font-bold">
                  {queue.filter((i) => i.status === "pending").length}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {tab === "submit" && (
        <div className="grid lg:grid-cols-2 gap-6">
          <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80 space-y-3 h-fit">
            <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
              <Code2 size={18} className="text-brand-sky" /> New Review Request
            </h2>
            <input
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              placeholder="Title — e.g. Two Sum with O(1) lookups"
              className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
            />
            <select
              value={form.language}
              onChange={(e) => setForm({ ...form, language: e.target.value })}
              className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
            >
              {["python", "javascript", "typescript", "java", "cpp", "go", "rust", "other"].map((l) => (
                <option key={l} value={l}>{l}</option>
              ))}
            </select>
            <textarea
              value={form.code}
              onChange={(e) => setForm({ ...form, code: e.target.value })}
              placeholder="Paste your code (min 10 characters)"
              rows={12}
              className="w-full p-3 rounded-xl border border-white/60 bg-[#0f172a] text-emerald-200 font-mono text-xs resize-none"
            />
            <textarea
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              placeholder="What do you want reviewed? (approach, edge cases, style…)"
              rows={2}
              className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm resize-none"
            />
            <button
              onClick={handleSubmit}
              disabled={saving || !form.title.trim() || form.code.trim().length < 10}
              className="w-full btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {saving ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />} Submit for Review
            </button>
          </div>
          <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80 text-sm text-text-light space-y-2 h-fit">
            <h3 className="text-base font-bold text-text-primary mb-2">How it works</h3>
            <p>1. Submit a snippet — reviewers will rate clarity, correctness and style on 1–5.</p>
            <p>2. Claim items from the queue to review others. You can never review your own code.</p>
            <p>3. Every item can receive multiple independent reviews — the more you review, the more your own code gets seen.</p>
            <p>4. Feedback is peer-written, instant, and free — no AI involved.</p>
          </div>
        </div>
      )}

      {tab === "my" && (
        <div className="space-y-4">
          {loading ? (
            <div className="flex justify-center py-12"><Loader2 size={28} className="animate-spin text-brand-sky" /></div>
          ) : myItems.length === 0 ? (
            <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80 text-text-light text-sm">
              You haven't submitted any code for review yet.
            </div>
          ) : (
            myItems.map((item) => (
              <div key={item.id} className="p-5 rounded-2xl border border-white/60 bg-white border-border/80">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-text-primary">{item.title}</span>
                    <span className="text-xs text-text-light">{item.language}</span>
                  </div>
                  <span className={`px-2 py-1 rounded-lg text-xs font-semibold ${STATUS_BADGE[item.status] || "bg-gray-100 text-gray-700"}`}>
                    {item.status}
                  </span>
                </div>
                {item.avg_rating != null && (
                  <div className="flex items-center gap-1 text-sm mb-2">
                    <Star size={14} className="fill-amber-400 text-amber-400" />
                    <span className="font-bold text-text-primary">{item.avg_rating}</span>
                    <span className="text-xs text-text-light">/ 5 · {item.reviews_count} review{item.reviews_count === 1 ? "" : "s"}</span>
                  </div>
                )}
                {(item.reviews || []).length > 0 ? (
                  <div className="space-y-3 mt-3">
                    {(item.reviews || []).map((r) => (
                      <div key={r.id} className="p-3 rounded-xl border border-white/60 bg-white border-border/60">
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-xs font-semibold text-text-primary">{r.reviewer_name}</span>
                          <span className="text-xs flex items-center gap-1">
                            {Array.from({ length: r.rating }, (_, i) => <Star key={i} size={12} className="fill-amber-400 text-amber-400" />)}
                          </span>
                        </div>
                        <p className="text-sm text-text-secondary">{r.comments}</p>
                        {r.strengths && (
                          <p className="mt-2 text-xs text-green-700"><span className="font-semibold">Strengths:</span> {r.strengths}</p>
                        )}
                        {r.improvements && (
                          <p className="mt-1 text-xs text-amber-700"><span className="font-semibold">Improve:</span> {r.improvements}</p>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="mt-3 text-xs text-text-light">No reviews yet — pending in the queue.</p>
                )}
              </div>
            ))
          )}
        </div>
      )}

      {tab === "queue" && (
        <div className="grid lg:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
              <Handshake size={18} className="text-brand-lavender" /> Available for review
            </h2>
            {loading ? (
              <div className="flex justify-center py-12"><Loader2 size={28} className="animate-spin text-brand-sky" /></div>
            ) : queue.length === 0 ? (
              <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80 text-text-light text-sm">
                Queue is empty — check back soon or submit your own code.
              </div>
            ) : (
              queue.map((item) => (
                <div key={item.id} className="p-4 rounded-2xl border border-white/60 bg-white border-border/80">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-text-primary">{item.title}</span>
                      <span className="text-xs text-text-light">{item.language}</span>
                    </div>
                    <span className={`px-2 py-1 rounded-lg text-xs font-semibold ${STATUS_BADGE[item.status] || "bg-gray-100 text-gray-700"}`}>
                      {item.status}
                    </span>
                  </div>
                  <div className="text-xs text-text-light mb-1">by {item.user_name}</div>
                  <pre className="p-2 rounded-lg bg-[#0f172a] text-emerald-200 font-mono text-[10px] max-h-24 overflow-hidden whitespace-pre-wrap">
                    {item.code.slice(0, 500)}{item.code.length > 500 ? "…" : ""}
                  </pre>
                  <button
                    onClick={() => handleClaim(item)}
                    disabled={item.status === "claimed"}
                    className="mt-3 w-full py-2 rounded-xl border border-brand-sky text-brand-sky text-sm font-semibold hover:bg-brand-sky hover:text-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <ClipboardCheck size={15} className="inline mr-1" /> Claim & Review
                  </button>
                </div>
              ))
            )}
          </div>

          <div className="p-6 rounded-2xl border border-white/60 bg-white border-border/80 h-fit sticky top-24">
            {!claimed ? (
              <div className="text-center py-10 text-text-light text-sm flex flex-col items-center gap-3">
                <Users size={36} className="text-brand-sky" />
                Claim an item from the queue to start reviewing.
              </div>
            ) : (
              <div className="space-y-3">
                <h2 className="text-lg font-bold text-text-primary flex items-center gap-2">
                  <Star size={18} className="text-amber-400" /> Review: {claimed.title}
                </h2>
                <pre className="p-3 rounded-xl bg-[#0f172a] text-emerald-200 font-mono text-xs max-h-40 overflow-auto whitespace-pre-wrap">
                  {claimed.code}
                </pre>
                <div className="flex items-center gap-1">
                  <span className="text-sm text-text-light mr-1">Rating:</span>
                  {[1, 2, 3, 4, 5].map((n) => (
                    <button key={n} onClick={() => setReview({ ...review, rating: n })}>
                      <Star
                        size={22}
                        className={n <= review.rating ? "fill-amber-400 text-amber-400" : "text-gray-300"}
                      />
                    </button>
                  ))}
                </div>
                <textarea
                  value={review.comments}
                  onChange={(e) => setReview({ ...review, comments: e.target.value })}
                  placeholder="Your feedback (min 10 characters) — what works, what's risky, edge cases…"
                  rows={4}
                  className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm resize-none"
                />
                <input
                  value={review.strengths}
                  onChange={(e) => setReview({ ...review, strengths: e.target.value })}
                  placeholder="Strengths (optional)"
                  className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
                />
                <input
                  value={review.improvements}
                  onChange={(e) => setReview({ ...review, improvements: e.target.value })}
                  placeholder="Suggested improvements (optional)"
                  className="w-full p-2.5 rounded-xl border border-white/60 bg-white text-sm"
                />
                <button
                  onClick={handleSubmitReview}
                  disabled={submitting || review.comments.trim().length < 10}
                  className="w-full btn-primary py-3 flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {submitting ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />} Submit Review
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
