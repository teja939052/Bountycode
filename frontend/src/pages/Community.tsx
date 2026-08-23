import { useState, useEffect, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link } from "react-router-dom";
import {
  Heart,
  MessageCircle,
  Trash2,
  Send,
  ChevronDown,
  ChevronUp,
  Clock,
  Award,
  Flame,
  CheckCircle,
  Code2,
  Loader2,
  Users,
  BookOpen,
  Trophy,
  Crown,
  Star,
  Target,
  Globe,
   Trees,
   Gift,
   Play,
   Medal,
 } from "lucide-react";
import api from "../services/api";

const TIME_AGO_CONFIG = { day: "day", hour: "hr", minute: "min", second: "sec" };

function timeAgo(dateStr) {
  const diff = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
  if (diff < 60) return `${diff}s`;
  if (diff < 3600) return `${Math.floor(diff / 60)}m`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`;
  return `${Math.floor(diff / 86400)}d`;
}

function PostSkeleton() {
  return (
    <div className="bg-white border border-nature-leaf/20 rounded-2xl p-5 shadow-sm animate-pulse">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded-full bg-[#E5E0D3]" />
        <div className="flex-1">
          <div className="h-4 bg-[#E5E0D3] rounded w-28 mb-1" />
          <div className="h-3 bg-[#E5E0D3] rounded w-16" />
        </div>
      </div>
      <div className="h-4 bg-[#E5E0D3] rounded w-3/4 mb-2" />
      <div className="h-4 bg-[#E5E0D3] rounded w-1/2" />
    </div>
  );
}

function TypeBadge({ type }) {
  const config = {
    achievement: { label: "Achievement", icon: Award, color: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
    streak: { label: "Streak", icon: Flame, color: "bg-orange-500/20 text-orange-400 border-orange-500/30" },
    solve: { label: "Solve", icon: CheckCircle, color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
    post: { label: "Post", icon: MessageCircle, color: "bg-nature-bark text-nature-blossom border-nature-leaf/30" },
  };
  const c = config[type] || config.post;
  const Icon = c.icon;
  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium border ${c.color}`}>
      <Icon size={12} />
      {c.label}
    </span>
  );
}

export default function Community() {
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [newContent, setNewContent] = useState("");
  const [newType, setNewType] = useState("post");
  const [newCode, setNewCode] = useState("");
  const [newLanguage, setNewLanguage] = useState("");
  const [posting, setPosting] = useState(false);
  const [showCodeField, setShowCodeField] = useState(false);
  const [expandedComments, setExpandedComments] = useState({});
  const [commentTexts, setCommentTexts] = useState({});
  const [submittingComment, setSubmittingComment] = useState({});
  const [error, setError] = useState("");
  const [currentUserId, setCurrentUserId] = useState("");
  const feedRef = useRef(null);

  useEffect(() => {
    api.getMe().then(u => setCurrentUserId(u.id)).catch(() => {});
  }, []);

  const fetchPosts = useCallback(async (p = 1, append = false) => {
    if (!append) setLoading(true);
    else setLoadingMore(true);
    try {
      const data = await api.getFeedPosts(p, 20);
      setPosts(prev => append ? [...prev, ...data.posts] : data.posts);
      setTotalPages(data.pages);
      setPage(p);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, []);

  useEffect(() => { fetchPosts(); }, [fetchPosts]);

  const handleCreatePost = async () => {
    if (!newContent.trim()) return;
    setPosting(true);
    try {
      const post = await api.createFeedPost({
        content: newContent,
        type: newType,
        code: showCodeField ? newCode || null : null,
        language: showCodeField ? newLanguage || null : null,
      });
      setPosts(prev => [post, ...prev]);
      setNewContent("");
      setNewCode("");
      setNewLanguage("");
      setShowCodeField(false);
      setNewType("post");
    } catch (e) {
      setError(e.message);
    } finally {
      setPosting(false);
    }
  };

  const handleLike = async (postId) => {
    try {
      const data = await api.likeFeedPost(postId);
      setPosts(prev => prev.map(p =>
        p.id === postId ? { ...p, likes: data.likes, liked: data.liked } : p
      ));
    } catch (e) {
      // ignore
    }
  };

  const handleDelete = async (postId) => {
    try {
      await api.deleteFeedPost(postId);
      setPosts(prev => prev.filter(p => p.id !== postId));
    } catch (e) {
      setError(e.message);
    }
  };

  const handleComment = async (postId) => {
    const text = commentTexts[postId];
    if (!text?.trim()) return;
    setSubmittingComment(prev => ({ ...prev, [postId]: true }));
    try {
      const data = await api.addFeedComment(postId, text);
      setPosts(prev => prev.map(p =>
        p.id === postId ? { ...p, comments: [...(p.comments || []), data.comment] } : p
      ));
      setCommentTexts(prev => ({ ...prev, [postId]: "" }));
    } catch (e) {
      setError(e.message);
    } finally {
      setSubmittingComment(prev => ({ ...prev, [postId]: false }));
    }
  };

  const toggleComments = (postId) => {
    setExpandedComments(prev => ({ ...prev, [postId]: !prev[postId] }));
  };

  const loadMore = () => {
    if (page < totalPages && !loadingMore) {
      fetchPosts(page + 1, true);
    }
  };

  return (
    <div className="min-h-screen bg-surface-base">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">Community</h1>
          <p className="text-text-muted">Connect, share, and learn with fellow students</p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-6">
          {[
            { to: "/study-groups", icon: Users, label: "Study Groups", color: "bg-brand-teal/10 text-brand-teal border-brand-teal/20" },
            { to: "/tower", icon: Trophy, label: "Leaderboard", color: "bg-brand-gold/10 text-brand-gold border-brand-gold/20" },
            { to: "/daily-challenge", icon: Target, label: "Daily Challenge", color: "bg-brand-coral/10 text-brand-coral border-brand-coral/20" },
            { to: "/question-bank", icon: BookOpen, label: "Practice", color: "bg-brand-lavender/10 text-brand-lavender border-brand-lavender/20" },
          ].map((nav) => (
            <Link key={nav.label} to={nav.to} className={`flex items-center gap-2 rounded-xl border p-3 hover:bg-white border-border/50 transition-colors ${nav.color}`}>
              <nav.icon size={16} />
              <span className="text-xs font-bold">{nav.label}</span>
            </Link>
          ))}
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
            {error}
            <button onClick={() => setError("")} className="float-right text-red-400 hover:text-red-300">&times;</button>
          </div>
        )}

        <div className="bg-white border border-nature-leaf/20 rounded-2xl p-5 shadow-sm mb-6">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-nature-bark flex items-center justify-center text-nature-blossom font-bold">
              {currentUserId ? "U" : "?"}
            </div>
            <select
              value={newType}
              onChange={e => setNewType(e.target.value)}
              className="bg-white border border-nature-leaf/20 rounded-lg px-3 py-1.5 text-sm text-text-secondary"
            >
              <option value="post">Post</option>
              <option value="achievement">Achievement</option>
              <option value="streak">Streak</option>
              <option value="solve">Solve</option>
            </select>
          </div>
          <textarea
            value={newContent}
            onChange={e => setNewContent(e.target.value)}
            placeholder="Share something with the community..."
            rows={3}
            className="w-full bg-white border border-nature-leaf/20 rounded-xl p-3 text-text-primary placeholder-text-muted resize-none focus:outline-none focus:border-nature-leaf transition-colors"
          />
          <div className="flex items-center justify-between mt-3">
            <button
              onClick={() => setShowCodeField(!showCodeField)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-colors ${showCodeField ? 'bg-nature-bark text-nature-blossom' : 'text-text-muted hover:text-text-secondary'}`}
            >
              <Code2 size={16} />
              Add Code
            </button>
            <button
              onClick={handleCreatePost}
              disabled={posting || !newContent.trim()}
              className="px-5 py-2 bg-nature-leaf hover:bg-nature-moss disabled:bg-[#E5E0D3] disabled:text-text-muted text-text-primary rounded-xl text-sm font-medium transition-colors flex items-center gap-2"
            >
              {posting ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
              Post
            </button>
          </div>
          <AnimatePresence>
            {showCodeField && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="overflow-hidden mt-3"
              >
                <div className="flex gap-2 mb-2">
                  <input
                    value={newLanguage}
                    onChange={e => setNewLanguage(e.target.value)}
                    placeholder="Language (e.g. python)"
                    className="flex-1 bg-white border border-nature-leaf/20 rounded-lg px-3 py-1.5 text-sm text-text-secondary placeholder-text-muted"
                  />
                </div>
                <textarea
                  value={newCode}
                  onChange={e => setNewCode(e.target.value)}
                  placeholder="Paste your code here..."
                  rows={5}
                  className="w-full bg-[#101623] border border-[#1F2937] rounded-xl p-3 text-sm font-mono text-[#6EE7A8] placeholder-[#4B5563] resize-none focus:outline-none focus:border-[#7BB661]"
                />
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map(i => <PostSkeleton key={i} />)}
          </div>
        ) : posts.length === 0 ? (
          <div className="text-center py-16 text-text-muted">
            <MessageCircle size={48} className="mx-auto mb-4 opacity-50" />
            <p className="text-lg font-medium mb-1">No posts yet</p>
            <p className="text-sm">Be the first to share something!</p>
          </div>
        ) : (
          <div className="space-y-4" ref={feedRef}>
            {posts.map(post => {
              const isLiked = post.liked || post.liked_by?.includes(currentUserId);
              const commentCount = post.comments?.length || 0;
              return (
                <motion.div
                  key={post.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white border border-nature-leaf/20 rounded-2xl p-5 shadow-sm"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#4F8F57] to-[#7BB661] flex items-center justify-center text-text-primary font-bold text-sm shadow-lg">
                        {post.user_avatar || post.user_name?.[0] || "?"}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-text-primary">{post.user_name}</span>
                          <TypeBadge type={post.type} />
                        </div>
                        <div className="flex items-center gap-1 text-xs text-text-muted mt-0.5">
                          <Clock size={10} />
                          {timeAgo(post.created_at)} ago
                        </div>
                      </div>
                    </div>
                    {post.user_id === currentUserId && (
                      <button
                        onClick={() => handleDelete(post.id)}
                        className="p-1.5 text-text-muted hover:text-red-500 hover:bg-red-500/10 rounded-lg transition-colors"
                      >
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>

                  <p className="text-text-secondary text-sm leading-relaxed mb-3 whitespace-pre-wrap">{post.content}</p>

                  {post.code && (
                    <div className="mb-3 bg-[#101623] rounded-xl border border-[#1F2937] overflow-hidden">
                      {post.language && (
                        <div className="px-4 py-1.5 bg-[#161D2E] border-b border-[#1F2937] text-xs text-text-muted font-mono">
                          {post.language}
                        </div>
                      )}
                      <pre className="p-4 text-sm font-mono text-[#6EE7A8] overflow-x-auto whitespace-pre-wrap">
                        {post.code}
                      </pre>
                    </div>
                  )}

                  <div className="flex items-center gap-4 pt-2 border-t border-[#EDEAE0]">
                    <button
                      onClick={() => handleLike(post.id)}
                      className={`flex items-center gap-1.5 text-sm transition-all ${
                        isLiked ? "text-red-500" : "text-text-muted hover:text-red-500"
                      }`}
                    >
                      <motion.div
                        whileTap={{ scale: 1.3 }}
                        className="flex items-center gap-1"
                      >
                        <Heart size={16} fill={isLiked ? "currentColor" : "none"} />
                        <span>{post.likes || 0}</span>
                      </motion.div>
                    </button>
                    <button
                      onClick={() => toggleComments(post.id)}
                      className="flex items-center gap-1.5 text-sm text-text-muted hover:text-nature-blossom transition-colors"
                    >
                      <MessageCircle size={16} />
                      <span>{commentCount}</span>
                      {expandedComments[post.id] ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                    </button>
                  </div>

                  <AnimatePresence>
                    {expandedComments[post.id] && (
                      <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                      >
                        <div className="mt-3 pt-3 border-t border-[#EDEAE0] space-y-3">
                          {(post.comments || []).map((c, i) => (
                            <div key={c.id || i} className="flex gap-2 pl-2">
                              <div className="w-7 h-7 rounded-full bg-[#E5E0D3] flex items-center justify-center text-text-muted text-xs font-bold shrink-0 mt-0.5">
                                {c.user_name?.[0] || "?"}
                              </div>
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2">
                                  <span className="text-xs font-semibold text-text-secondary">{c.user_name}</span>
                                  <span className="text-[10px] text-text-muted">{timeAgo(c.created_at)} ago</span>
                                </div>
                                <p className="text-sm text-text-secondary mt-0.5">{c.content}</p>
                              </div>
                            </div>
                          ))}
                          <div className="flex gap-2 pt-1">
                            <div className="w-7 h-7 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 text-xs font-bold shrink-0">
                              {currentUserId ? "U" : "?"}
                            </div>
                            <div className="flex-1 flex gap-2">
                              <input
                                value={commentTexts[post.id] || ""}
                                onChange={e => setCommentTexts(prev => ({ ...prev, [post.id]: e.target.value }))}
                                onKeyDown={e => e.key === "Enter" && handleComment(post.id)}
                                placeholder="Write a comment..."
                                className="flex-1 bg-white border border-nature-leaf/20 rounded-lg px-3 py-2 text-sm text-text-secondary placeholder-text-muted focus:outline-none focus:border-nature-leaf"
                              />
                              <button
                                onClick={() => handleComment(post.id)}
                                disabled={submittingComment[post.id] || !commentTexts[post.id]?.trim()}
                                className="p-2 bg-nature-leaf hover:bg-nature-moss disabled:bg-[#E5E0D3] disabled:text-text-muted text-text-primary rounded-lg transition-colors"
                              >
                                {submittingComment[post.id] ? (
                                  <Loader2 size={14} className="animate-spin" />
                                ) : (
                                  <Send size={14} />
                                )}
                              </button>
                            </div>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              );
            })}

            {page < totalPages && (
              <div className="text-center pt-4">
                <button
                  onClick={loadMore}
                  disabled={loadingMore}
                  className="px-6 py-2.5 bg-white hover:bg-surface-card text-text-secondary rounded-xl text-sm font-medium transition-colors border border-nature-leaf/20 inline-flex items-center gap-2"
                >
                  {loadingMore ? (
                    <Loader2 size={16} className="animate-spin" />
                  ) : (
                    <ChevronDown size={16} />
                  )}
                  Load More
                </button>
              </div>
            )}
          </div>
        )}

        <div className="mt-8 rounded-2xl border border-nature-leaf/20 bg-white p-5 shadow-sm">
          <h3 className="text-sm font-bold text-text-primary mb-4">More Community Features</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {[
              { to: "/tower", icon: Trophy, label: "Leaderboard", color: "text-brand-gold" },
              { to: "/study-groups", icon: Users, label: "Study Groups", color: "text-brand-teal" },
              { to: "/daily-challenge", icon: Target, label: "Daily Challenge", color: "text-brand-coral" },
              { to: "/battles", icon: Crown, label: "1v1 Battles", color: "text-brand-amber" },
              { to: "/question-bank", icon: BookOpen, label: "Question Bank", color: "text-brand-lavender" },
              { to: "/interview", icon: Play, label: "Mock Interviews", color: "text-brand-sky" },
              { to: "/rank", icon: Medal, label: "Rank System", color: "text-brand-gold" },
              { to: "/problem-of-the-day", icon: Sparkles, label: "Problem of the Day", color: "text-brand-coral" },
              { to: "/world", icon: Globe, label: "World Map", color: "text-brand-emerald" },
              { to: "/tower", icon: Trees, label: "Forest Journey", color: "text-brand-teal" },
              { to: "/referral", icon: Gift, label: "Refer & Earn", color: "text-brand-coral" },
              { to: "/campus-wars", icon: Users, label: "Campus Wars", color: "text-brand-sky" },
            ].map((feature) => (
              <Link key={feature.label} to={feature.to} className="flex items-center gap-2 rounded-xl border border-nature-leaf/20 p-3 hover:bg-surface-card transition-colors">
                <feature.icon size={16} className={feature.color} />
                <span className="text-xs font-bold text-text-secondary">{feature.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
