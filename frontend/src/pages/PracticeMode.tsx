import { useState, useEffect, useRef } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import PracticeConsole from "../components/learning/PracticeConsole";
import { ExternalLink, Send, CheckCircle, XCircle, ArrowRight, RotateCcw, BookOpen, Terminal } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import CelebrationOverlay from "../components/CelebrationOverlay";
import SubmitReveal from "../components/SubmitReveal";

export default function PracticeMode() {
  const { questionId } = useParams();
  const navigate = useNavigate();
  const [question, setQuestion] = useState(null);
  const [loading, setLoading] = useState(true);
  const [answer, setAnswer] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [showCelebration, setShowCelebration] = useState(false);
  const [showSubmitReveal, setShowSubmitReveal] = useState(false);
  const [startTime, setStartTime] = useState(null);
  const reduced = useReducedMotion();
  const textareaRef = useRef(null);

  useEffect(() => {
    loadQuestion();
  }, [questionId]);

  const loadQuestion = async () => {
    setLoading(true);
    try {
      const data = await api.questions.getFull(questionId);
      if (data) {
        setQuestion(data);
        setStartTime(Date.now());
      }
    } catch {} finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!answer.trim() || submitting) return;
    setSubmitting(true);
    try {
      const timeTaken = startTime ? Math.floor((Date.now() - startTime) / 1000) : null;
      const data = await api.submitQuestionAnswer(questionId, answer, timeTaken);
      setFeedback(data);
      setShowSubmitReveal(true);
      if (data.score >= 8) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 2500);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleTryAgain = () => {
    setAnswer("");
    setFeedback(null);
    setShowSubmitReveal(false);
    setStartTime(Date.now());
    textareaRef.current?.focus();
  };

  const handleNextProblem = () => {
    navigate("/question-bank");
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
      </div>
    );
  }

  if (!question) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card text-center py-12">
          <BookOpen size={48} className="mx-auto text-brand-secondary dark:text-brand-secondary mb-4" />
          <p className="text-gray-500 dark:text-gray-400 mb-4">Question not found</p>
          <Link to="/question-bank" className="text-primary-600 font-semibold hover:text-primary-700">
            Back to Question Bank
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <CelebrationOverlay show={showCelebration} type="perfect" message="Great Answer!" />

        <Link
          to="/question-bank"
          className="inline-flex items-center gap-1 text-sm text-gray-500 dark:text-gray-400 hover:text-primary-600 mb-6"
        >
          ← Back to Question Bank
        </Link>

        {/* Question Card */}
        <motion.div
          className="card mb-6"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="flex items-start justify-between mb-4">
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <span className="text-xs px-2 py-0.5 rounded-full bg-surface-card/50 bg-surface-card/50 text-brand-secondary dark:text-gray-400">
                  {question.company}
                </span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400">
                  {question.type}
                </span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  question.difficulty === "easy" ? "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400"
                  : question.difficulty === "medium" ? "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400"
                  : "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400"
                }`}>
                  {question.difficulty}
                </span>
              </div>
              <h2 className="text-xl font-bold dark:text-white">{question.question_title}</h2>
            </div>
          </div>

          <a
            href={question.question_link}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700 mt-2"
          >
            Open question on {question.source} <ExternalLink size={14} />
          </a>
        </motion.div>

        {/* Write & Run Code */}
        {!feedback && (
          <motion.div
            className="mb-6"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
          >
            <div className="flex items-center gap-2 mb-2">
              <Terminal size={16} className="text-cyber-green" />
              <h3 className="font-semibold text-brand-primary dark:text-brand-secondary">Write & Run Code</h3>
            </div>
            <PracticeConsole
              height={280}
              title="Code Playground"
              onResult={() => {}}
            />
          </motion.div>
        )}

        {/* Answer Input */}
        {!feedback && (
          <motion.div
            className="card mb-6"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <label className="block text-sm font-medium text-brand-primary dark:text-brand-secondary mb-2">
              Your Answer / Approach
            </label>
            <textarea
              ref={textareaRef}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="Write your approach, code, or answer here. Be as detailed as possible..."
              className="w-full px-4 py-3 border border-brand-primary/20 border-brand-primary/15 rounded-lg focus:ring-2 focus:ring-primary-500 bg-surface-card bg-surface-card dark:text-white min-h-[200px] resize-y"
              rows={8}
            />
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-gray-400">
                {answer.length > 0 ? `${answer.length} characters` : "Be specific for better feedback"}
              </p>
              <button
                onClick={handleSubmit}
                disabled={!answer.trim() || submitting}
                className="flex items-center gap-2 bg-primary-600 text-text-primary px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50 transition-colors"
              >
                {submitting ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
                ) : (
                  <>
                    <Send size={18} />
                    Get Feedback
                  </>
                )}
              </button>
            </div>
          </motion.div>
        )}

        {/* AI Feedback */}
        <AnimatePresence>
          {feedback && (
            <motion.div
              className="space-y-4"
              initial={reduced ? {} : { opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              {/* Score Card */}
              <div className={`card text-center py-8 ${
                feedback.score >= 7 ? "bg-gradient-to-r from-green-500 to-emerald-600" :
                feedback.score >= 4 ? "bg-gradient-to-r from-yellow-500 to-orange-500" :
                "bg-gradient-to-r from-red-500 to-pink-500"
              } text-text-primary`}>
                <motion.p
                  className="text-6xl font-bold mb-2"
                  initial={reduced ? {} : { scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 200, damping: 15 }}
                >
                  {feedback.score}/10
                </motion.p>
                <p className="text-lg">
                  {feedback.score >= 8 ? "Excellent work!" : feedback.score >= 5 ? "Good attempt!" : "Keep practicing!"}
                </p>
                {feedback.xp_gained > 0 && (
                  <p className="text-sm mt-2 text-text-primary/80">+{feedback.xp_gained} XP earned</p>
                )}
              </div>

              {/* Feedback Details */}
              <div className="card">
                <h3 className="font-bold mb-3 dark:text-white">AI Feedback</h3>
                <p className="text-brand-secondary dark:text-gray-400 mb-4">{feedback.feedback}</p>

                {feedback.strengths?.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-semibold text-sm text-green-600 dark:text-green-400 mb-2">Strengths</h4>
                    <ul className="space-y-1">
                      {feedback.strengths.map((s, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-brand-secondary dark:text-gray-400">
                          <CheckCircle size={14} className="text-green-500 mt-0.5 shrink-0" />
                          {s}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {feedback.improvements?.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-semibold text-sm text-orange-600 dark:text-orange-400 mb-2">Areas to Improve</h4>
                    <ul className="space-y-1">
                      {feedback.improvements.map((s, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-brand-secondary dark:text-gray-400">
                          <XCircle size={14} className="text-orange-500 mt-0.5 shrink-0" />
                          {s}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {feedback.better_approach && (
                  <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                    <h4 className="font-semibold text-sm text-blue-600 dark:text-blue-400 mb-2">Better Approach</h4>
                    <p className="text-sm text-brand-secondary dark:text-gray-400">{feedback.better_approach}</p>
                  </div>
                )}

                {feedback.explanation && (
                  <div className="bg-emerald-50 dark:bg-emerald-900/20 rounded-lg p-4">
                    <h4 className="font-semibold text-sm text-emerald-600 dark:text-emerald-400 mb-2">Concept Explained</h4>
                    <p className="text-sm text-brand-secondary dark:text-gray-400 mb-2">{feedback.explanation.approach}</p>
                    {feedback.explanation.steps?.length > 0 && (
                      <ol className="list-decimal list-inside space-y-1 mb-2">
                        {feedback.explanation.steps.map((step, i) => (
                          <li key={i} className="text-sm text-brand-secondary dark:text-gray-400">{step}</li>
                        ))}
                      </ol>
                    )}
                    {feedback.explanation.common_mistakes?.length > 0 && (
                      <ul className="space-y-1">
                        {feedback.explanation.common_mistakes.map((m, i) => (
                          <li key={i} className="text-sm text-red-500 dark:text-red-400">• {m}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>

              {/* Actions */}
              <div className="flex gap-3">
                <button
                  onClick={handleTryAgain}
                  className="flex items-center gap-2 bg-surface-card/50 bg-surface-card text-brand-secondary dark:text-gray-400 px-6 py-3 rounded-lg font-semibold hover:bg-surface-card/50 dark:hover:bg-gray-700 transition-colors"
                >
                  <RotateCcw size={18} />
                  Try Again
                </button>
                <Link
                  to="/question-bank"
                  className="flex items-center gap-2 bg-primary-600 text-text-primary px-6 py-3 rounded-lg font-semibold hover:bg-primary-700 transition-colors"
                >
                  Next Question
                  <ArrowRight size={18} />
                </Link>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {showSubmitReveal && feedback && (
        <SubmitReveal
          result={feedback}
          question={question}
          onClose={() => setShowSubmitReveal(false)}
          onTryAgain={handleTryAgain}
          onNext={handleNextProblem}
        />
      )}
    </div>
  );
}
