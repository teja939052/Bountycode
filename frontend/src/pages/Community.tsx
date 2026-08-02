import { useState, useEffect, useCallback, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
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
    <div className="bg-gray-800/50 backdrop-blur border border-gray-700/50 rounded-xl p-5 animate-pulse">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-10 h-10 rounded-full bg-gray-700" />
        <div className="flex-1">
          <div className="h-4 bg-gray-700 rounded w-28 mb-1" />
          <div className="h-3 bg-gray-700 rounded w-16" />
        </div>
      </div>
      <div className="h-4 bg-gray-700 rounded w-3/4 mb-2" />
      <div className="h-4 bg-gray-700 rounded w-1/2" />
    </div>
  );
}

function TypeBadge({ type }) {
  const config = {
    achievement: { label: "Achievement", icon: Award, color: "bg-amber-500/20 text-amber-400 border-amber-500/30" },
    streak: { label: "Streak", icon: Flame, color: "bg-orange-500/20 text-orange-400 border-orange-500/30" },
    solve: { label: "Solve", icon: CheckCircle, color: "bg-emerald-500/20 text-emerald-400 border-emerald-500/30" },
    post: { label: "Post", icon: MessageCircle, color: "bg-indigo-500/20 text-indigo-400 border-indigo-500/30" },
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
    <div className="min-h-screen bg-gray-900">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-100 mb-2">Community Feed</h1>
          <p className="text-gray-400">Share your progress, tips, and achievements with fellow students</p>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
            {error}
            <button onClick={() => setError("")} className="float-right text-red-400 hover:text-red-300">&times;</button>
          </div>
        )}

        <div className="bg-gray-800/50 backdrop-blur border border-gray-700/50 rounded-xl p-5 mb-6">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center text-indigo-400 font-bold">
              {currentUserId ? "U" : "?"}
            </div>
            <select
              value={newType}
              onChange={e => setNewType(e.target.value)}
              className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-sm text-gray-200"
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
            className="w-full bg-gray-700/50 border border-gray-600 rounded-xl p-3 text-gray-100 placeholder-gray-500 resize-none focus:outline-none focus:border-indigo-500 transition-colors"
          />
          <div className="flex items-center justify-between mt-3">
            <button
              onClick={() => setShowCodeField(!showCodeField)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-colors ${showCodeField ? 'bg-indigo-500/20 text-indigo-400' : 'text-gray-400 hover:text-gray-300'}`}
            >
              <Code2 size={16} />
              Add Code
            </button>
            <button
              onClick={handleCreatePost}
              disabled={posting || !newContent.trim()}
              className="px-5 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-xl text-sm font-medium transition-colors flex items-center gap-2"
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
                    className="flex-1 bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-sm text-gray-200 placeholder-gray-500"
                  />
                </div>
                <textarea
                  value={newCode}
                  onChange={e => setNewCode(e.target.value)}
                  placeholder="Paste your code here..."
                  rows={5}
                  className="w-full bg-gray-900 border border-gray-700 rounded-xl p-3 text-sm font-mono text-emerald-400 placeholder-gray-600 resize-none focus:outline-none focus:border-indigo-500"
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
          <div className="text-center py-16 text-gray-500">
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
                  className="bg-gray-800/50 backdrop-blur border border-gray-700/50 rounded-xl p-5"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm shadow-lg">
                        {post.user_avatar || post.user_name?.[0] || "?"}
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-gray-100">{post.user_name}</span>
                          <TypeBadge type={post.type} />
                        </div>
                        <div className="flex items-center gap-1 text-xs text-gray-500 mt-0.5">
                          <Clock size={10} />
                          {timeAgo(post.created_at)} ago
                        </div>
                      </div>
                    </div>
                    {post.user_id === currentUserId && (
                      <button
                        onClick={() => handleDelete(post.id)}
                        className="p-1.5 text-gray-500 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                      >
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>

                  <p className="text-gray-200 text-sm leading-relaxed mb-3 whitespace-pre-wrap">{post.content}</p>

                  {post.code && (
                    <div className="mb-3 bg-gray-900 rounded-xl border border-gray-700 overflow-hidden">
                      {post.language && (
                        <div className="px-4 py-1.5 bg-gray-800 border-b border-gray-700 text-xs text-gray-400 font-mono">
                          {post.language}
                        </div>
                      )}
                      <pre className="p-4 text-sm font-mono text-emerald-400 overflow-x-auto whitespace-pre-wrap">
                        {post.code}
                      </pre>
                    </div>
                  )}

                  <div className="flex items-center gap-4 pt-2 border-t border-gray-700/50">
                    <button
                      onClick={() => handleLike(post.id)}
                      className={`flex items-center gap-1.5 text-sm transition-all ${
                        isLiked ? "text-red-400" : "text-gray-500 hover:text-red-400"
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
                      className="flex items-center gap-1.5 text-sm text-gray-500 hover:text-indigo-400 transition-colors"
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
                        <div className="mt-3 pt-3 border-t border-gray-700/30 space-y-3">
                          {(post.comments || []).map((c, i) => (
                            <div key={c.id || i} className="flex gap-2 pl-2">
                              <div className="w-7 h-7 rounded-full bg-gray-700 flex items-center justify-center text-gray-300 text-xs font-bold shrink-0 mt-0.5">
                                {c.user_name?.[0] || "?"}
                              </div>
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center gap-2">
                                  <span className="text-xs font-semibold text-gray-300">{c.user_name}</span>
                                  <span className="text-[10px] text-gray-600">{timeAgo(c.created_at)} ago</span>
                                </div>
                                <p className="text-sm text-gray-400 mt-0.5">{c.content}</p>
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
                                className="flex-1 bg-gray-700/50 border border-gray-600 rounded-lg px-3 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-indigo-500"
                              />
                              <button
                                onClick={() => handleComment(post.id)}
                                disabled={submittingComment[post.id] || !commentTexts[post.id]?.trim()}
                                className="p-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 disabled:text-gray-500 text-white rounded-lg transition-colors"
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
                  className="px-6 py-2.5 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-xl text-sm font-medium transition-colors border border-gray-700/50 inline-flex items-center gap-2"
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
      </div>
    </div>
  );
}
