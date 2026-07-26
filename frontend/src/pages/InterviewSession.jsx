import { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useLocation, useNavigate, Link } from "react-router-dom";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";
import XPPopup from "../components/XPPopup";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import {
  Clock, Target, TrendingUp, MessageSquare,
  AlertCircle, CheckCircle2, ArrowRight, RotateCcw,
} from "lucide-react";

const REACTIONS = {
  fire: { emoji: "🔥", label: "Crushing it!", color: "text-cyber-orange" },
  thumbsup: { emoji: "👍", label: "Solid answer!", color: "text-cyber-blue" },
  muscle: { emoji: "💪", label: "Good effort!", color: "text-cyber-green" },
  memo: { emoji: "📝", label: "Keep refining", color: "text-cyber-yellow" },
  star: { emoji: "⭐", label: "Exceptional!", color: "text-cyber-yellow" },
  thinking: { emoji: "🤔", label: "Think deeper", color: "text-cyber-purple" },
};

const DIFFICULTY_COLORS = {
  easy: "text-cyber-green bg-cyber-green/10 border border-cyber-green/20",
  medium: "text-cyber-yellow bg-cyber-yellow/10 border border-cyber-yellow/20",
  hard: "text-cyber-red bg-cyber-red/10 border border-cyber-red/20",
};

const COMPANY_COLORS = {
  google: "from-blue-500 to-green-500",
  amazon: "from-orange-400 to-yellow-500",
  meta: "from-blue-600 to-indigo-600",
  microsoft: "from-green-500 to-blue-500",
  tcs: "from-blue-700 to-blue-900",
  infosys: "from-blue-500 to-purple-600",
  wipro: "from-blue-600 to-cyan-500",
  uber: "from-black to-gray-700",
  general: "from-gray-500 to-gray-700",
};

export default function InterviewSession() {
  const { interviewId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const reduced = useReducedMotion();

  const initialState = location.state || {};
  const [question, setQuestion] = useState(initialState.question || "");
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState(null);
  const [score, setScore] = useState(0);
  const [questionCount, setQuestionCount] = useState(1);
  const [totalQuestions] = useState(initialState.totalQuestions || 10);
  const [loading, setLoading] = useState(false);
  const [finished, setFinished] = useState(false);
  const [result, setResult] = useState(null);
  const [tips, setTips] = useState(initialState.tips || "");
  const [difficulty, setDifficulty] = useState(initialState.difficulty || "medium");
  const [company, setCompany] = useState(initialState.company || "general");
  const [companyStyle, setCompanyStyle] = useState(initialState.companyStyle || "");
  const [isFollowUp, setIsFollowUp] = useState(false);
  const [reaction, setReaction] = useState(null);
  const [showReaction, setShowReaction] = useState(false);
  const [timer, setTimer] = useState(0);
  const [showCelebration, setShowCelebration] = useState(false);
  const [xpData, setXpData] = useState(null);
  const [showXP, setShowXP] = useState(false);
  const [error, setError] = useState("");
  const [initialized, setInitialized] = useState(!!initialState.question);

  const timerRef = useRef(null);
  const answerStartTime = useRef(Date.now());

  useEffect(() => {
    timerRef.current = setInterval(() => setTimer((p) => p + 1), 1000);
    return () => clearInterval(timerRef.current);
  }, []);

  useEffect(() => {
    if (!initialState.question && interviewId) {
      const loadInterview = async () => {
        try {
          const data = await api.get(`/api/interview/${interviewId}/result`);
          if (data.questions?.length > 0 && (data.total_questions >= 10 || data.questions.length >= 10)) {
            setResult(data);
            setFinished(true);
          }
          setInitialized(true);
        } catch {
          setError("Could not load interview.");
          setInitialized(true);
        }
      };
      loadInterview();
    } else {
      setInitialized(true);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [interviewId, initialState.question]);

  const triggerReaction = useCallback((type) => {
    if (!type || !REACTIONS[type]) return;
    setReaction(REACTIONS[type]);
    setShowReaction(true);
    setTimeout(() => setShowReaction(false), 2500);
  }, []);

  const submitAnswer = useCallback(async () => {
    if (!answer.trim() || loading) return;
    setLoading(true);
    setError("");
    const timeTaken = Math.round((Date.now() - answerStartTime.current) / 1000);
    answerStartTime.current = Date.now();

    try {
      const data = await api.post("/api/interview/answer", {
        interview_id: interviewId, question, answer, time_taken: timeTaken, is_follow_up: isFollowUp,
      });

      setFeedback(data.feedback);
      setScore(data.current_score);
      setReaction(null);
      triggerReaction(data.reaction);

      if (data.finished) {
        const resultData = await api.get(`/api/interview/${interviewId}/result`);
        setResult(resultData);
        setFinished(true);
        clearInterval(timerRef.current);
        if (data.xp_gained) {
          setXpData({ xpGained: data.xp_gained, level: data.level, streak: data.streak, newBadges: data.new_badges || [] });
          setShowXP(true);
        }
        if (data.current_score >= 7) {
          setShowCelebration(true);
          setTimeout(() => setShowCelebration(false), 3000);
        }
      } else {
        setQuestion(data.next_question);
        setTips(data.next_tips || "");
        setDifficulty(data.next_difficulty || difficulty);
        setIsFollowUp(data.is_follow_up || false);
        setQuestionCount(data.questions_answered + 1);
        setAnswer("");
        setFeedback(null);
        setReaction(null);
      }
    } catch (err) {
      setError(err.message || "Failed to submit answer.");
    } finally {
      setLoading(false);
    }
  }, [answer, loading, interviewId, question, isFollowUp, difficulty, triggerReaction]);

  const handleKeyDown = useCallback((e) => {
    if (e.key === "Enter" && e.ctrlKey) submitAnswer();
  }, [submitAnswer]);

  const formatTime = (s) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  const getScoreColor = (s) => {
    if (s >= 8) return "text-cyber-green bg-cyber-green/10 border-cyber-green/30";
    if (s >= 6) return "text-cyber-blue bg-cyber-blue/10 border-cyber-blue/30";
    if (s >= 4) return "text-cyber-yellow bg-cyber-yellow/10 border-cyber-yellow/30";
    return "text-cyber-red bg-cyber-red/10 border-cyber-red/30";
  };

  if (!initialized) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spinner size="lg" />
      </div>
    );
  }

  // RESULTS SCREEN
  if (finished && result) {
    return (
      <div className="min-h-screen py-12 px-4">
        <CelebrationOverlay show={showCelebration} type="perfect" message="Outstanding Performance!" />
        <XPPopup show={showXP} {...xpData} onClose={() => setShowXP(false)} />
        <div className="max-w-4xl mx-auto">
          <motion.div
            className="card mb-8 text-center"
            initial={reduced ? {} : { opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
          >
            <span className="section-subheader mb-3 block">Mission Complete</span>
            <h1 className="section-header text-3xl mb-2">Engagement <span className="text-cyber-blue">Terminated</span></h1>
            <p className="text-gray-500 font-mono text-sm mb-6">
              {result.job_role} — {result.company === "general" ? "General" : result.company?.charAt(0).toUpperCase() + result.company?.slice(1)}
            </p>

            <div className={`w-32 h-32 rounded-full flex items-center justify-center text-4xl font-display font-black mx-auto border-2 ${getScoreColor(result.overall_score)}`}>
              {result.overall_score}
            </div>
            <p className="text-gray-500 font-mono text-xs mt-3">Overall Score / 10</p>

            {result.score_breakdown && Object.keys(result.score_breakdown).length > 0 && (
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6">
                {Object.entries(result.score_breakdown).map(([key, val]) => (
                  <div key={key} className="bg-space-panel border border-space-border rounded-lg p-3">
                    <p className="text-2xl font-display font-bold text-white">{val}</p>
                    <p className="text-xs font-mono text-gray-500 capitalize">{key.replace("_", " ")}</p>
                  </div>
                ))}
              </div>
            )}

            {result.readiness_score !== undefined && (
              <div className="mt-6 inline-flex items-center gap-2 bg-cyber-blue/10 border border-cyber-blue/20 px-4 py-2 rounded-full">
                <Target size={14} className="text-cyber-blue" />
                <span className="font-mono text-sm text-cyber-blue">Readiness: {result.readiness_score}%</span>
              </div>
            )}
          </motion.div>

          <div className="grid sm:grid-cols-2 gap-4 mb-8">
            {result.strength_areas?.length > 0 && (
              <div className="card border-cyber-green/20 bg-cyber-green/5">
                <h3 className="font-display font-bold text-cyber-green text-sm mb-2 flex items-center gap-2">
                  <CheckCircle2 size={16} /> Strengths
                </h3>
                <ul className="space-y-1">
                  {result.strength_areas.map((s, i) => (
                    <li key={i} className="text-xs font-mono text-gray-400">{s}</li>
                  ))}
                </ul>
              </div>
            )}
            {result.improvement_areas?.length > 0 && (
              <div className="card border-cyber-orange/20 bg-cyber-orange/5">
                <h3 className="font-display font-bold text-cyber-orange text-sm mb-2 flex items-center gap-2">
                  <AlertCircle size={16} /> Areas to Improve
                </h3>
                <ul className="space-y-1">
                  {result.improvement_areas.map((s, i) => (
                    <li key={i} className="text-xs font-mono text-gray-400">{s}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {result.difficulty_progression?.length > 1 && (
            <div className="card mb-8">
              <h3 className="font-display font-bold text-white text-sm mb-3 flex items-center gap-2">
                <TrendingUp size={16} className="text-cyber-blue" /> Difficulty Trajectory
              </h3>
              <div className="flex items-center gap-2 flex-wrap">
                {result.difficulty_progression.map((d, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-mono ${DIFFICULTY_COLORS[d] || DIFFICULTY_COLORS.medium}`}>{d}</span>
                    {i < result.difficulty_progression.length - 1 && <ArrowRight size={12} className="text-gray-600" />}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="space-y-4 mb-8">
            {result.questions?.map((q, i) => (
              <motion.div
                key={i}
                className="card"
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <div className="flex items-start justify-between mb-3">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      {q.is_follow_up && (
                        <span className="text-[10px] bg-cyber-purple/20 text-cyber-purple px-2 py-0.5 rounded-full font-mono">Follow-up</span>
                      )}
                      <span className={`text-[10px] px-2 py-0.5 rounded-full font-mono ${DIFFICULTY_COLORS[q.difficulty] || ""}`}>{q.difficulty}</span>
                    </div>
                    <h3 className="font-display font-bold text-white text-sm">Q{i + 1}: {q.question}</h3>
                  </div>
                  <span className={`text-sm font-display font-bold px-3 py-1 rounded-full shrink-0 border ${getScoreColor(q.score)}`}>{q.score}/10</span>
                </div>
                <p className="text-gray-500 font-mono text-xs mb-3">Your answer: {q.answer}</p>

                {q.feedback && (
                  <div className="bg-space-panel border border-space-border rounded-lg p-4 text-xs space-y-2 font-mono">
                    {q.feedback.strengths?.length > 0 && (
                      <div><span className="text-cyber-green">Strengths: </span><span className="text-gray-400">{q.feedback.strengths.join(", ")}</span></div>
                    )}
                    {q.feedback.improvements?.length > 0 && (
                      <div><span className="text-cyber-orange">Improve: </span><span className="text-gray-400">{q.feedback.improvements.join(", ")}</span></div>
                    )}
                    {q.feedback.better_answer && (
                      <details className="mt-2">
                        <summary className="text-gray-400 cursor-pointer hover:text-white">See improved answer</summary>
                        <p className="text-gray-400 mt-2 bg-space-void p-3 rounded-lg border border-space-border">{q.feedback.better_answer}</p>
                      </details>
                    )}
                  </div>
                )}
              </motion.div>
            ))}
          </div>

          <div className="flex gap-4">
            <Link to="/interview" className="flex-1 btn-primary text-center flex items-center justify-center gap-2">
              <RotateCcw size={16} /> Engage Again
            </Link>
            <Link to="/dashboard" className="flex-1 btn-secondary text-center">Command Deck</Link>
          </div>
        </div>
      </div>
    );
  }

  // LIVE INTERVIEW SCREEN
  return (
    <div className="min-h-screen py-12 px-4">
      <CelebrationOverlay show={showCelebration} type="confetti" message="Great Interview!" />
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${COMPANY_COLORS[company] || COMPANY_COLORS.general} flex items-center justify-center text-white text-xs font-bold`}>
              {company?.charAt(0).toUpperCase()}
            </div>
            <div>
              <span className="text-sm font-display font-bold text-white">
                Q{questionCount} / {totalQuestions}
              </span>
              {isFollowUp && (
                <span className="ml-2 text-[10px] bg-cyber-purple/20 text-cyber-purple px-2 py-0.5 rounded-full font-mono">Follow-up</span>
              )}
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className={`text-[10px] px-2 py-1 rounded-full font-mono ${DIFFICULTY_COLORS[difficulty] || DIFFICULTY_COLORS.medium}`}>{difficulty}</span>
            <div className="flex items-center gap-1 text-sm font-mono text-gray-400">
              <Clock size={12} /> {formatTime(timer)}
            </div>
            <div className="flex items-center gap-1 text-sm font-display font-bold text-cyber-blue">
              <TrendingUp size={12} /> {score > 0 ? score.toFixed(1) : "-"}/10
            </div>
          </div>
        </div>

        {/* Progress */}
        <div className="w-full bg-space-panel rounded-full h-1.5 mb-8 border border-space-border">
          <motion.div
            className="bg-gradient-to-r from-cyber-blue to-cyber-purple h-1.5 rounded-full"
            initial={reduced ? { width: `${((questionCount - 1) / totalQuestions) * 100}%` } : { width: 0 }}
            animate={{ width: `${(questionCount / totalQuestions) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>

        {companyStyle && questionCount === 1 && (
          <motion.div
            className="card mb-6 border-cyber-blue/20 bg-cyber-blue/5 text-sm"
            initial={reduced ? {} : { opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <p className="text-cyber-blue font-mono text-xs">
              <strong>{company?.charAt(0).toUpperCase() + company?.slice(1)} Style:</strong> {companyStyle}
            </p>
          </motion.div>
        )}

        {error && (
          <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-4 text-center font-mono text-xs">{error}</div>
        )}

        {/* Floating Reaction */}
        <AnimatePresence>
          {showReaction && reaction && (
            <motion.div
              className="fixed top-24 right-8 z-40 bg-space-panel border border-space-border rounded-2xl shadow-xl px-6 py-4 flex items-center gap-3"
              initial={reduced ? {} : { opacity: 0, x: 50, scale: 0.8 }}
              animate={{ opacity: 1, x: 0, scale: 1 }}
              exit={reduced ? { opacity: 0 } : { opacity: 0, x: 50, scale: 0.8 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              <span className="text-4xl">{reaction.emoji}</span>
              <div>
                <p className={`font-display font-bold ${reaction.color}`}>{reaction.label}</p>
                <p className="text-xs font-mono text-gray-500">Score: {score.toFixed(1)}/10</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Feedback */}
        <AnimatePresence>
          {feedback && (
            <motion.div
              className="card mb-6 border-cyber-green/20 bg-cyber-green/5"
              initial={reduced ? {} : { opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
            >
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">{REACTIONS[feedback.reaction]?.emoji || (feedback.score >= 7 ? "🎉" : feedback.score >= 5 ? "👍" : "💪")}</span>
                <span className="font-display font-bold text-cyber-green">Score: {feedback.score}/10</span>
                {feedback.breakdown && Object.keys(feedback.breakdown).length > 0 && (
                  <div className="flex gap-2 ml-auto">
                    {Object.entries(feedback.breakdown).map(([k, v]) => (
                      <span key={k} className="text-[10px] bg-space-panel border border-space-border px-2 py-1 rounded-full font-mono text-gray-400">{k.replace("_", " ")}: {v}</span>
                    ))}
                  </div>
                )}
              </div>
              {feedback.strengths?.slice(0, 2).map((s, i) => (
                <p key={i} className="text-cyber-green text-xs font-mono mb-1">✅ {s}</p>
              ))}
              {feedback.improvements?.slice(0, 2).map((s, i) => (
                <p key={i} className="text-cyber-orange text-xs font-mono">💡 {s}</p>
              ))}
              {feedback.better_answer && (
                <details className="mt-3">
                  <summary className="text-xs font-mono text-gray-400 cursor-pointer hover:text-white">See improved answer</summary>
                  <p className="text-xs font-mono text-gray-400 mt-2 bg-space-void p-3 rounded-lg border border-space-border">{feedback.better_answer}</p>
                </details>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Question */}
        <motion.div
          className="card mb-6"
          key={question}
          initial={reduced ? {} : { opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ type: "spring", stiffness: 200, damping: 20 }}
        >
          <div className="flex items-center gap-2 mb-2">
            <MessageSquare size={14} className="text-cyber-blue" />
            <span className="text-[10px] uppercase tracking-widest font-mono text-gray-500">
              {isFollowUp ? "Follow-up" : "Interview Query"}
            </span>
          </div>
          <p className="font-display font-bold text-white text-lg">{question}</p>
          {tips && (
            <p className="text-xs font-mono text-gray-500 mt-2 italic">💡 Hint: {tips}</p>
          )}
        </motion.div>

        {/* Answer Input */}
        <textarea
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          onKeyDown={handleKeyDown}
          className="input min-h-[180px] resize-y mb-4 font-mono text-sm"
          placeholder={
            isFollowUp ? "Follow-up answer — dig deeper..." :
            company === "amazon" ? "STAR method: Situation, Task, Action, Result..." :
            "Type your answer here — be specific with examples..."
          }
        />

        <button
          onClick={submitAnswer}
          disabled={loading || !answer.trim()}
          className="w-full btn-primary text-center flex items-center justify-center gap-2"
        >
          {loading ? (
            <><Spinner size="sm" className="text-space-void" /> Transmitting...</>
          ) : (
            <>Transmit Answer <ArrowRight size={16} /></>
          )}
        </button>

        <p className="text-[10px] font-mono text-gray-600 text-center mt-3">Ctrl+Enter to submit</p>
      </div>
    </div>
  );
}
