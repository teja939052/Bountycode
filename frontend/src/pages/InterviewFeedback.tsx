import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { interviewFeedbackApi } from "../services/api/interviewFeedback.ts";
import { Star, Send, MessageSquare, Award, BarChart3 } from "lucide-react";

const RATINGS = [
  { id: "clarity", label: "Clarity", desc: "How clearly they communicated" },
  { id: "depth", label: "Depth", desc: "How deep their answers were" },
  { id: "confidence", label: "Confidence", desc: "How confident they appeared" },
  { id: "relevance", label: "Relevance", desc: "How relevant their responses were" },
  { id: "problem_solving", label: "Problem-Solving", desc: "Their approach to solving problems" },
];

const StarRating = ({ value, onChange, readOnly = false }) => {
  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5].map((n) => (
        <button
          key={n}
          type="button"
          onClick={() => !readOnly && onChange(n)}
          disabled={readOnly}
          className={readOnly ? "cursor-default" : "hover:scale-110 transition-transform"}
        >
          <Star
            className={`h-5 w-5 ${
              n <= value
                ? "fill-amber-400 text-amber-400"
                : "text-slate-600"
            }`}
          />
        </button>
      ))}
    </div>
  );
};

export default function InterviewFeedback({ interviewId, onSubmitSuccess }) {
  const [scores, setScores] = useState({
    clarity: 0, depth: 0, confidence: 0, relevance: 0, problem_solving: 0,
  });
  const [comment, setComment] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (interviewId) {
      interviewFeedbackApi.get(interviewId)
        .then(setFeedback)
        .catch((e) => setError(e.message || "Load failed"));
    }
  }, [interviewId]);

  const handleRating = (category, value) => {
    setScores((prev) => ({ ...prev, [category]: value }));
  };

  const handleSubmit = async () => {
    const total = Object.values(scores).reduce((a, b) => a + b, 0);
    if (total < 5) {
      setError("Please rate all categories");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await interviewFeedbackApi.submit(interviewId, scores, comment);
      setSubmitted(true);
      if (onSubmitSuccess) onSubmitSuccess();
    } catch (e) {
      setError(e.message || "Submit failed");
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="flex flex-col items-center justify-center py-12 text-center"
      >
        <div className="mb-6 rounded-full bg-green-500/20 p-4">
          <Award className="h-12 w-12 text-green-400" />
        </div>
        <h3 className="text-2xl font-bold text-slate-200">Feedback Submitted!</h3>
        <p className="text-slate-400 mt-2 mb-2">
          Your peer review helps them improve.
        </p>
        <p className="text-amber-400 text-sm">
          +25 XP bonus for participating.
        </p>
      </motion.div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-200 flex items-center gap-2">
          <MessageSquare className="h-6 w-6 text-indigo-400" />
          Peer Interview Feedback
        </h2>
        <p className="text-slate-400 text-sm mt-1">
          Rate your peer across 5 key categories.
        </p>
      </div>

      {feedback && feedback.average_scores && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-slate-800/40 border border-slate-700 rounded-xl p-4 mb-6"
        >
          <div className="flex items-center gap-2 mb-3">
            <BarChart3 className="h-5 w-5 text-indigo-400" />
            <span className="font-bold text-slate-200">Average Scores</span>
          </div>
          <div className="grid grid-cols-2 gap-3">
            {RATINGS.map(({ id, label }) => (
              <div key={id} className="flex justify-between">
                <span className="text-sm text-slate-400">{label}</span>
                <span className="text-sm font-bold text-amber-300">
                  {feedback.average_scores[id] || 0}/5
                </span>
              </div>
            ))}
          </div>
          <div className="mt-3 pt-3 border-t border-slate-700">
            <span className="text-sm text-slate-400">Overall: </span>
            <span className="font-bold text-xl text-indigo-300">{feedback.overall_score}/5</span>
            <span className="text-xs text-slate-500 ml-2">({feedback.feedback_count} reviews)</span>
          </div>
        </motion.div>
      )}

      <div className="space-y-6">
        {RATINGS.map(({ id, label, desc }) => (
          <motion.div
            key={id}
            className="bg-slate-900/40 border border-slate-800 rounded-xl p-4"
          >
            <div className="flex justify-between items-center mb-1">
              <span className="font-medium text-slate-200">{label}</span>
              <span className="text-xs text-slate-500">{desc}</span>
            </div>
            <StarRating
              value={scores[id]}
              onChange={(v) => handleRating(id, v)}
            />
          </motion.div>
        ))}
      </div>

      <div className="mt-6">
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Any additional feedback? (optional)"
          rows={3}
          maxLength={500}
          className="w-full rounded-xl border border-slate-700 bg-slate-800/40 px-4 py-3 text-sm text-slate-100 placeholder-slate-500 resize-none focus:border-indigo-500 focus:outline-none"
        />
      </div>

      {error && (
        <p className="text-amber-400 text-sm mt-4">{error}</p>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading || Object.values(scores).some((v) => v === 0)}
        className="mt-6 w-full rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white shadow hover:bg-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
      >
        {loading ? (
          <>
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
            Submitting...
          </>
        ) : (
          <>
            <Send className="h-4 w-4" />
            Submit Feedback
          </>
        )}
      </button>
    </div>
  );
}
