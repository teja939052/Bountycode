import { useState, useEffect, useRef } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import PracticeConsole from "../components/learning/PracticeConsole";
import { ExternalLink, Send, CheckCircle, XCircle, ArrowRight, RotateCcw, BookOpen, Terminal } from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import CelebrationOverlay from "../components/CelebrationOverlay";
import SubmitReveal from "../components/SubmitReveal";
import { Card, SectionHeader } from "../design-system/Card";
import { Button } from "../design-system/Button";

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "bg-subject-verbal/10 text-subject-verbal border border-subject-verbal/20",
  medium: "bg-subject-aptitude/10 text-subject-aptitude border border-subject-aptitude/20",
  hard: "bg-subject-boss/10 text-subject-boss border border-subject-boss/20",
  expert: "bg-subject-interview/10 text-subject-interview border border-subject-interview/20",
};

export default function PracticeMode() {
  const { questionId } = useParams();
  const navigate = useNavigate();
  const [question, setQuestion] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [answer, setAnswer] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<any>(null);
  const [showCelebration, setShowCelebration] = useState(false);
  const [showSubmitReveal, setShowSubmitReveal] = useState(false);
  const [startTime, setStartTime] = useState<number | null>(null);
  const reduced = useReducedMotion();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

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
      <div className="min-h-screen bg-canvas flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  if (!question) {
    return (
      <div className="min-h-screen bg-canvas flex items-center justify-center">
        <Card tone="default" className="text-center py-12">
          <BookOpen size={48} className="mx-auto text-text-muted mb-4" />
          <p className="text-text-muted mb-4">Question not found</p>
          <Link to="/question-bank" className="text-primary font-semibold hover:text-primary-dark">
            Back to Question Bank
          </Link>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-canvas py-6 px-3 sm:px-4">
      <div className="max-w-3xl mx-auto">
        <CelebrationOverlay show={showCelebration} type="perfect" message="Great Answer!" />

        <Link
          to="/question-bank"
          className="inline-flex items-center gap-1 text-xs font-bold text-primary hover:text-primary-dark mb-4 uppercase tracking-wider"
        >
          ← Back to Question Bank
        </Link>

        {/* Question Card */}
        <motion.div
          className="mb-4"
          initial={reduced ? {} : { opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card tone="default" interactive className="group">
            <div className="flex items-start justify-between mb-3">
              <div>
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  <span className="text-[10px] px-2 py-0.5 rounded-full border border-border/50 text-text-secondary">
                    {question.company}
                  </span>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full border border-border/50 text-text-secondary ${TYPE_COLORS[question.type] || ""}`}>
                    {question.type}
                  </span>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full border border-border/50 text-text-secondary ${DIFFICULTY_COLORS[question.difficulty] || ""}`}>
                    {question.difficulty}
                  </span>
                </div>
                <h2 className="text-lg font-black text-text">{question.question_title}</h2>
              </div>
            </div>
            <a
              href={question.question_link}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:text-primary-dark mt-2"
            >
              Open question on {question.source} <ExternalLink size={14} />
            </a>
          </Card>
        </motion.div>

        {/* Write & Run Code */}
        {!feedback && (
          <motion.div
            className="mb-4"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.05 }}
          >
            <Card pad="md" className="relative overflow-hidden">
              <div className="absolute inset-0 bg-primary/5 pointer-events-none" />
              <div className="relative z-10 flex items-center gap-2 mb-3">
                <Terminal size={16} className="text-primary" />
                <h3 className="font-bold text-text">Write & Run Code</h3>
              </div>
              <PracticeConsole
                height={280}
                title="Code Playground"
                onResult={() => {}}
              />
            </Card>
          </motion.div>
        )}

        {/* Answer Input */}
        {!feedback && (
          <motion.div
            className="mb-4"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card pad="md">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <label className="block text-xs font-bold uppercase tracking-wider text-text-muted mb-1">
                    Your Answer / Approach
                  </label>
                </div>
                <span className="text-[10px] font-mono text-text-muted">
                  {answer.length > 0 ? `${answer.length} characters` : "Be specific for better feedback"}
                </span>
              </div>
              <textarea
                ref={textareaRef}
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Write your approach, code, or answer here. Be as detailed as possible..."
                className="w-full px-3 py-2 border border-border/50 rounded-xl bg-surfaceHover focus:border-primary focus:ring-1 focus:ring-primary text-text text-sm placeholder-text-text-muted min-h-[200px] resize-y"
                rows={8}
              />
              <Button
                variant="primary"
                onClick={handleSubmit}
                disabled={!answer.trim() || submitting}
                className="w-full mt-4 text-sm font-bold shadow-primary"
              >
                {submitting ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white/40" />
                ) : (
                  <>
                    <Send size={18} />
                    Get Feedback
                  </>
                )}
              </Button>
            </Card>
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
              <div className={`text-center py-8 rounded-2xl border border-border/50 ${
                feedback.score >= 7 ? "bg-subject-verbal/10 border-subject-verbal/30" :
                feedback.score >= 4 ? "bg-subject-aptitude/10 border-subject-aptitude/30" :
                "bg-subject-boss/10 border-subject-boss/30"
              } shadow-card`}>
                <motion.p
                  className="text-5xl font-black mb-2"
                  initial={reduced ? {} : { scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ type: "spring", stiffness: 200, damping: 15 }}
                >
                  {feedback.score}/10
                </motion.p>
                <p className="text-lg font-semibold text-text">
                  {feedback.score >= 8 ? "Excellent work!" : feedback.score >= 5 ? "Good attempt!" : "Keep practicing!"}
                </p>
                {feedback.xp_gained > 0 && (
                  <p className="text-sm text-primary mt-2 font-bold">+{feedback.xp_gained} XP earned</p>
                )}
              </div>

              {/* Feedback Details */}
              <Card pad="md">
                <h3 className="font-black mb-3 text-text">AI Feedback</h3>
                <p className="text-text-secondary mb-4 leading-relaxed">{feedback.feedback}</p>

                {feedback.strengths?.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-bold text-xs uppercase tracking-wider text-subject-verbal mb-2 flex items-center gap-1">
                      <CheckCircle size={12} className="text-subject-verbal" />
                      Strengths
                    </h4>
                    <ul className="space-y-1">
                      {feedback.strengths.map((s: string, i: number) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-text-secondary">
                          <CheckCircle size={14} className="text-subject-verbal mt-0.5 shrink-0" />
                          {s}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {feedback.improvements?.length > 0 && (
                  <div className="mb-4">
                    <h4 className="font-bold text-xs uppercase tracking-wider text-subject-boss mb-2 flex items-center gap-1">
                      <XCircle size={12} className="text-subject-boss" />
                      Areas to Improve
                    </h4>
                    <ul className="space-y-1">
                      {feedback.improvements.map((s: string, i: number) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-text-secondary">
                          <XCircle size={14} className="text-subject-boss mt-0.5 shrink-0" />
                          {s}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {feedback.better_approach && (
                  <div className="bg-primary/10 border border-primary/20 rounded-xl p-4">
                    <h4 className="font-bold text-xs uppercase tracking-wider text-primary mb-2">Better Approach</h4>
                    <p className="text-sm text-text-secondary">{feedback.better_approach}</p>
                  </div>
                )}

                {feedback.explanation && (
                  <div className="bg-subject-verbal/10 border border-subject-verbal/20 rounded-xl p-4">
                    <h4 className="font-bold text-xs uppercase tracking-wider text-subject-verbal mb-2">Concept Explained</h4>
                    <p className="text-sm text-text-secondary mb-2">{feedback.explanation.approach}</p>
                    {feedback.explanation.steps?.length > 0 && (
                      <ol className="list-decimal list-inside space-y-1 mb-2 text-sm text-text-secondary">
                        {feedback.explanation.steps.map((step: string, i: number) => (
                          <li key={i}>{step}</li>
                        ))}
                      </ol>
                    )}
                    {feedback.explanation.common_mistakes?.length > 0 && (
                      <ul className="space-y-1">
                        {feedback.explanation.common_mistakes.map((m: string, i: number) => (
                          <li key={i} className="text-sm text-subject-boss">• {m}</li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </Card>

              {/* Actions */}
              <div className="flex gap-2">
                <Button variant="outline" onClick={handleTryAgain} size="md" leftIcon={<RotateCcw size={18} />}>
                  Try Again
                </Button>
                <Link
                  to="/question-bank"
                  className="flex items-center gap-2 bg-primary text-text-primary px-4 py-3 rounded-xl font-bold hover:bg-primary-dark shadow-primary transition-all"
                >
                  Next Question <ArrowRight size={18} />
                </Link>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

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
    </div>
  );
}

const TYPE_COLORS: Record<string, string> = {
  coding: "bg-subject-coding/10 text-subject-coding border border-subject-coding/20",
  aptitude: "bg-subject-aptitude/10 text-subject-aptitude border border-subject-aptitude/20",
  behavioral: "bg-subject-reasoning/10 text-subject-reasoning border border-subject-reasoning/20",
  system_design: "bg-subject-interview/10 text-subject-interview border border-subject-interview/20",
  hr: "bg-subject-reasoning/10 text-subject-reasoning border border-subject-reasoning/20",
};
