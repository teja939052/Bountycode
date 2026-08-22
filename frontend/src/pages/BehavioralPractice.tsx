import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { MessageSquare, ChevronRight, Star, Send, Lightbulb } from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

export default function BehavioralPractice() {
  const [categories, setCategories] = useState<string[]>([]);
  const [question, setQuestion] = useState<any>(null);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("");

  useEffect(() => {
    api.get("/api/v1/behavioral/categories").then((d: any) => {
      setCategories(d.categories || []);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const loadQuestion = async (cat?: string) => {
    setLoading(true);
    try {
      const url = cat ? `/api/v1/behavioral/question?category=${cat}` : "/api/v1/behavioral/question";
      const q = await api.get(url);
      setQuestion(q);
      setFeedback(null);
      setAnswer("");
    } catch { }
    setLoading(false);
  };

  const submitAnswer = async () => {
    if (!answer.trim() || !question) return;
    setSubmitting(true);
    try {
      const fb = await api.post("/api/v1/behavioral/feedback", {
        question_id: question.question_id,
        answer,
      });
      setFeedback(fb);
    } catch { }
    setSubmitting(false);
  };

  useEffect(() => { loadQuestion(); }, []);

  if (loading && !question) return <div className="min-h-screen flex items-center justify-center"><Spinner /></div>;

  return (
    <div className="min-h-screen px-4 py-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand-lavender/10 border border-brand-lavender/20 mb-3">
          <MessageSquare size={14} className="text-brand-lavender" />
          <span className="text-xs font-mono text-brand-lavender">BEHAVIORAL</span>
        </div>
        <h1 className="text-3xl font-display font-black text-text-primary">Behavioral Interview Practice</h1>
        <p className="text-sm text-gray-500 mt-1">Practice STAR-method answers with AI feedback</p>
      </motion.div>

      {/* Category Pills */}
      <div className="flex flex-wrap gap-2 mb-6">
        <button onClick={() => { setSelectedCategory(""); loadQuestion(); }}
          className={`px-3 py-1.5 rounded-full text-xs font-mono border transition-all ${!selectedCategory ? "bg-brand-lavender/20 border-brand-lavender/30 text-brand-lavender" : "border-white/10 text-gray-500 hover:text-gray-300"}`}>
          All
        </button>
        {categories.map(c => (
          <button key={c} onClick={() => { setSelectedCategory(c); loadQuestion(c); }}
            className={`px-3 py-1.5 rounded-full text-xs font-mono border transition-all capitalize ${selectedCategory === c ? "bg-brand-lavender/20 border-brand-lavender/30 text-brand-lavender" : "border-white/10 text-gray-500 hover:text-gray-300"}`}>
            {c.replace(/_/g, " ")}
          </button>
        ))}
      </div>

      {/* Question Card */}
      {question && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass rounded-xl p-6 mb-6">
          <div className="flex items-start gap-3 mb-4">
            <div className="w-8 h-8 rounded-lg bg-brand-lavender/10 flex items-center justify-center shrink-0">
              <MessageSquare size={16} className="text-brand-lavender" />
            </div>
            <div>
              <h3 className="text-lg font-display font-bold text-text-primary">{question.title}</h3>
              <div className="flex flex-wrap gap-2 mt-2">
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-white/5 text-gray-400 capitalize">{question.category?.replace(/_/g, " ")}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-white/5 text-gray-400">{question.difficulty}</span>
                {question.companies?.slice(0, 3).map((c: string) => (
                  <span key={c} className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-brand-sky/10 text-brand-sky">{c}</span>
                ))}
              </div>
            </div>
          </div>

          {question.tips && (
            <div className="rounded-lg bg-amber-500/5 border border-amber-500/10 p-3 mb-4">
              <div className="flex items-center gap-2 text-amber-400 text-xs font-mono mb-1">
                <Lightbulb size={12} /> Tips
              </div>
              <p className="text-sm text-gray-400">{question.tips}</p>
            </div>
          )}

          {question.star_framework && (
            <div className="rounded-lg bg-white/[0.02] border border-white/5 p-3 mb-4">
              <p className="text-[10px] font-mono text-gray-500 uppercase tracking-wider mb-2">STAR Framework</p>
              <div className="grid grid-cols-2 gap-2 text-xs text-gray-400">
                {question.star_framework.situation && <div><span className="text-brand-sky font-mono">S:</span> {question.star_framework.situation}</div>}
                {question.star_framework.task && <div><span className="text-amber-400 font-mono">T:</span> {question.star_framework.task}</div>}
                {question.star_framework.action && <div><span className="text-emerald-400 font-mono">A:</span> {question.star_framework.action}</div>}
                {question.star_framework.result && <div><span className="text-brand-lavender font-mono">R:</span> {question.star_framework.result}</div>}
              </div>
            </div>
          )}

          <textarea value={answer} onChange={e => setAnswer(e.target.value)}
            className="w-full h-40 bg-white/[0.03] border border-white/10 rounded-xl p-4 text-sm text-gray-300 font-mono resize-none focus:outline-none focus:border-brand-lavender/40 transition-colors"
            placeholder="Type your answer using the STAR method..." />

          <div className="flex justify-end mt-3">
            <button onClick={submitAnswer} disabled={!answer.trim() || submitting}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-brand-lavender/20 text-brand-lavender font-mono text-sm hover:bg-brand-lavender/30 transition-all disabled:opacity-40">
              {submitting ? "Evaluating..." : "Get Feedback"} <Send size={14} />
            </button>
          </div>
        </motion.div>
      )}

      {/* Feedback */}
      {feedback && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-xl p-6 mb-6">
          <h3 className="font-display font-bold text-text-primary mb-3 flex items-center gap-2">
            <Star size={18} className="text-amber-400" /> AI Feedback
          </h3>
          <p className="text-sm text-gray-300 mb-4 whitespace-pre-wrap">{feedback.feedback}</p>
          {feedback.strengths?.length > 0 && (
            <div className="mb-3">
              <p className="text-[10px] font-mono text-emerald-400 uppercase tracking-wider mb-2">Strengths</p>
              {feedback.strengths.map((s: string, i: number) => (
                <p key={i} className="text-sm text-gray-400 ml-2">+ {s}</p>
              ))}
            </div>
          )}
          {feedback.areas_for_improvement?.length > 0 && (
            <div>
              <p className="text-[10px] font-mono text-amber-400 uppercase tracking-wider mb-2">Areas to Improve</p>
              {feedback.areas_for_improvement.map((a: string, i: number) => (
                <p key={i} className="text-sm text-gray-400 ml-2">- {a}</p>
              ))}
            </div>
          )}
          <button onClick={() => loadQuestion(selectedCategory)}
            className="mt-4 flex items-center gap-2 text-sm font-mono text-brand-lavender hover:underline">
            Next Question <ChevronRight size={14} />
          </button>
        </motion.div>
      )}
    </div>
  );
}
