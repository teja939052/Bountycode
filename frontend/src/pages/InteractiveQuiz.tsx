import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate, Link } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  XCircle,
  Clock,
  Zap,
  Target,
  Trophy,
  Flame,
  Sparkles,
  Lightbulb,
  Eye,
  EyeOff,
  ChevronRight,
  Award,
  AlertTriangle,
  Code2,
  Brain,
  Rocket,
  Timer,
  Star,
  RefreshCw,
  Play,
  Pause,
  X,
  Check,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";
import useReducedMotion from "../hooks/useReducedMotion";

const MODE_INFO = {
  practice: {
    title: "Practice Mode",
    description: "Free practice with hints and full solutions. No timer pressure.",
    icon: BookOpen,
    color: "text-blue-400",
    bg: "from-blue-500/10 to-cyan-500/5",
  },
  quiz: {
    title: "Quiz Mode",
    description: "Test yourself with hidden solutions. Multiple choice style.",
    icon: Target,
    color: "text-purple-400",
    bg: "from-purple-500/10 to-pink-500/5",
  },
  mock_interview: {
    title: "Mock Interview",
    description: "Realistic interview simulation. Timer, pressure, no hints.",
    icon: Brain,
    color: "text-amber-400",
    bg: "from-amber-500/10 to-orange-500/5",
  },
  speed_run: {
    title: "Speed Run",
    description: "Race against time. Solve fast for bonus XP.",
    icon: Rocket,
    color: "text-green-400",
    bg: "from-green-500/10 to-emerald-500/5",
  },
  boss_battle: {
    title: "Boss Battle",
    description: "Face hard problems. 2x XP rewards.",
    icon: Trophy,
    color: "text-red-400",
    bg: "from-red-500/10 to-pink-500/5",
  },
};

const DIFFICULTY_COLORS = {
  easy: { bg: "bg-green-500/10", text: "text-green-400", border: "border-green-500/30" },
  medium: { bg: "bg-yellow-500/10", text: "text-yellow-400", border: "border-yellow-500/30" },
  hard: { bg: "bg-red-500/10", text: "text-red-400", border: "border-red-500/30" },
};

function ModeCard({ mode, info, onSelect, selected }) {
  const Icon = info.icon;
  return (
    <motion.button
      whileHover={{ y: -4, scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => onSelect(mode)}
      className={`text-left p-5 rounded-2xl border transition-all ${
        selected
          ? "bg-gradient-to-br " + info.bg + " border-brand-sky/50 ring-2 ring-brand-sky/30"
          : "bg-surface-card/60 border-brand-primary/10 hover:border-brand-sky/30"
      }`}
    >
      <div className="flex items-start gap-3">
        <div className={`p-2 rounded-xl bg-surface-base/50 ${info.color}`}>
          <Icon size={24} />
        </div>
        <div className="flex-1">
          <h3 className="font-display font-bold text-base text-text-primary">{info.title}</h3>
          <p className="text-xs text-brand-secondary mt-1 leading-relaxed">{info.description}</p>
        </div>
      </div>
    </motion.button>
  );
}

function Timer({ seconds, onExpire, paused }) {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  const isLow = seconds < 60;

  useEffect(() => {
    if (paused || seconds <= 0) return;
    const id = setInterval(() => {
      if (seconds <= 1) {
        onExpire?.();
        clearInterval(id);
      }
    }, 1000);
    return () => clearInterval(id);
  }, [seconds, paused, onExpire]);

  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-xl ${
      isLow ? "bg-red-500/10 text-red-400 animate-pulse" : "bg-surface-base/50 text-text-primary"
    }`}>
      <Timer size={14} />
      <span className="font-mono text-sm font-bold">
        {String(minutes).padStart(2, "0")}:{String(secs).padStart(2, "0")}
      </span>
    </div>
  );
}

function HintCard({ hint, level, onNext, onRevealSolution }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-amber-500/5 border border-amber-500/20 rounded-2xl p-4"
    >
      <div className="flex items-start gap-3">
        <div className="p-2 rounded-lg bg-amber-500/10">
          <Lightbulb size={18} className="text-amber-400" />
        </div>
        <div className="flex-1">
          <p className="text-[10px] font-mono uppercase tracking-widest text-amber-400 mb-1">
            Hint {level}
          </p>
          <p className="text-sm text-text-primary leading-relaxed">
            {typeof hint === "string" ? hint : hint?.text || "No hint available"}
          </p>
        </div>
      </div>
      {onNext && (
        <div className="mt-3 flex gap-2">
          <button
            onClick={onNext}
            className="px-3 py-1.5 rounded-lg bg-amber-500/10 text-amber-400 text-xs font-medium hover:bg-amber-500/20 transition-colors"
          >
            Next Hint (-2 XP)
          </button>
          {onRevealSolution && (
            <button
              onClick={onRevealSolution}
              className="px-3 py-1.5 rounded-lg bg-red-500/10 text-red-400 text-xs font-medium hover:bg-red-500/20 transition-colors"
            >
              Give Up - Show Solution
            </button>
          )}
        </div>
      )}
    </motion.div>
  );
}

export default function InteractiveQuiz() {
  const navigate = useNavigate();
  const reduced = useReducedMotion();
  const [stage, setStage] = useState("setup"); // setup, playing, results
  const [mode, setMode] = useState("practice");
  const [filters, setFilters] = useState({
    topics: [],
    difficulty: null,
    company: null,
    num_questions: 5,
  });
  const [quiz, setQuiz] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [userAnswer, setUserAnswer] = useState("");
  const [hintLevel, setHintLevel] = useState(0);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [showHint, setShowHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [currentHint, setCurrentHint] = useState(null);
  const [currentResult, setCurrentResult] = useState(null);
  const [timeLeft, setTimeLeft] = useState(0);
  const [questionStartTime, setQuestionStartTime] = useState(Date.now());
  const [results, setResults] = useState(null);
  const [showCelebration, setShowCelebration] = useState(false);
  const [xpEarned, setXpEarned] = useState(0);
  const [building, setBuilding] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const timerRef = useRef(null);

  // Timer
  useEffect(() => {
    if (stage !== "playing" || !quiz || quiz.time_limit_seconds === 0) return;
    if (timerRef.current) clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timerRef.current);
          finishQuiz();
          return 0;
        }
        return t - 1;
      });
    }, 1000);
    return () => clearInterval(timerRef.current);
  }, [stage, quiz]);

  const buildQuiz = useCallback(async () => {
    setBuilding(true);
    try {
      const response = await api.quiz.buildQuiz({
        mode,
        ...filters,
        time_limit_seconds: mode === "mock_interview" ? 90 * 60 : 0,
      });
      if (response.success) {
        setQuiz(response.quiz);
        setTimeLeft(response.quiz.time_limit_seconds || 0);
        setStage("playing");
        setCurrentIndex(0);
        setAnswers([]);
        setQuestionStartTime(Date.now());
      }
    } catch (err) {
      console.error("Failed to build quiz:", err);
    } finally {
      setBuilding(false);
    }
  }, [mode, filters]);

  const submitAnswer = useCallback(async () => {
    if (submitting) return;
    setSubmitting(true);
    const timeTaken = (Date.now() - questionStartTime) / 1000;
    try {
      const response = await api.quiz.submitAnswer({
        quiz_id: quiz.quiz_id,
        question_id: quiz.questions[currentIndex].id,
        user_answer: userAnswer || "solved",
        time_taken_seconds: timeTaken,
        hints_used: hintsUsed,
      });
      if (response.success) {
        setCurrentResult(response.result);
        setXpEarned((prev) => prev + (response.result.xp_earned || 0));
        setAnswers((prev) => [...prev, response.result]);
        if (response.result.is_correct) {
          setShowCelebration(true);
        }
      }
    } catch (err) {
      console.error("Failed to submit:", err);
    } finally {
      setSubmitting(false);
    }
  }, [quiz, currentIndex, userAnswer, hintsUsed, submitting, questionStartTime]);

  const requestHint = useCallback(async () => {
    try {
      const response = await api.quiz.getHint(
        quiz.questions[currentIndex].id,
        hintLevel + 1,
        hintsUsed
      );
      if (response.success) {
        setCurrentHint(response.hint);
        setHintLevel(hintLevel + 1);
        setHintsUsed((hintsUsed) + 1);
        setShowHint(true);
      }
    } catch (err) {
      console.error("Failed to get hint:", err);
    }
  }, [quiz, currentIndex, hintLevel, hintsUsed]);

  const nextQuestion = useCallback(() => {
    if (currentIndex + 1 < quiz.questions.length) {
      setCurrentIndex(currentIndex + 1);
      setUserAnswer("");
      setHintLevel(0);
      setHintsUsed(0);
      setShowHint(false);
      setShowSolution(false);
      setCurrentResult(null);
      setCurrentHint(null);
      setQuestionStartTime(Date.now());
    } else {
      finishQuiz();
    }
  }, [currentIndex, quiz]);

  const finishQuiz = useCallback(async () => {
    if (timerRef.current) clearInterval(timerRef.current);
    const totalTime = quiz.time_limit_seconds > 0
      ? quiz.time_limit_seconds - timeLeft
      : quiz.questions.length * 15 * 60; // estimate if no timer
    try {
      const response = await api.quiz.calculateResults({
        quiz_id: quiz.quiz_id,
        questions: quiz.questions,
        answers: answers,
        total_time_seconds: totalTime,
      });
      if (response.success) {
        setResults(response.results);
        setStage("results");
      }
    } catch (err) {
      console.error("Failed to calculate results:", err);
    }
  }, [quiz, answers, timeLeft]);

  // Render
  if (stage === "setup") {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-sm text-brand-secondary hover:text-brand-sky transition-colors mb-6"
          >
            <ArrowLeft size={16} /> Back
          </button>

          <div className="bg-gradient-to-br from-brand-sky/10 via-purple-500/5 to-amber-500/5 border border-brand-primary/20 rounded-3xl p-6 sm:p-8 mb-6">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles size={18} className="text-brand-sky" />
              <span className="text-xs font-mono uppercase tracking-[0.2em] text-brand-sky">Interactive Practice</span>
            </div>
            <h1 className="font-display font-black text-2xl sm:text-3xl">Choose Your Mode</h1>
            <p className="text-sm text-brand-secondary mt-2">
              5 modes, real-time feedback, progressive hints, and XP rewards
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-6">
            {Object.entries(MODE_INFO).map(([m, info]) => (
              <ModeCard
                key={m}
                mode={m}
                info={info}
                selected={mode === m}
                onSelect={setMode}
              />
            ))}
          </div>

          <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-5 mb-6">
            <h3 className="font-display font-bold text-sm text-text-primary mb-3">Customize</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">Difficulty</label>
                <select
                  value={filters.difficulty || ""}
                  onChange={(e) => setFilters({ ...filters, difficulty: e.target.value || null })}
                  className="w-full mt-1 px-3 py-2 rounded-xl bg-surface-base border border-brand-primary/10 text-sm"
                >
                  <option value="">All</option>
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
              <div>
                <label className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">Number</label>
                <select
                  value={filters.num_questions}
                  onChange={(e) => setFilters({ ...filters, num_questions: parseInt(e.target.value) })}
                  className="w-full mt-1 px-3 py-2 rounded-xl bg-surface-base border border-brand-primary/10 text-sm"
                >
                  <option value={3}>3 questions</option>
                  <option value={5}>5 questions</option>
                  <option value={10}>10 questions</option>
                  <option value={15}>15 questions</option>
                </select>
              </div>
            </div>
          </div>

          <button
            onClick={buildQuiz}
            disabled={building}
            className="w-full py-4 rounded-2xl bg-gradient-to-r from-brand-sky to-purple-500 text-white font-bold text-base hover:from-brand-sky/90 hover:to-purple-500/90 transition-all disabled:opacity-50"
          >
            {building ? <Spinner size={20} /> : (
              <span className="flex items-center justify-center gap-2">
                <Play size={20} /> Start {MODE_INFO[mode].title}
              </span>
            )}
          </button>
        </div>
      </div>
    );
  }

  if (stage === "results" && results) {
    return (
      <div className="min-h-screen bg-surface-base text-text-primary">
        <div className="max-w-3xl mx-auto px-4 py-8">
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-gradient-to-br from-amber-500/10 to-yellow-500/5 border border-amber-500/20 rounded-3xl p-8 text-center"
          >
            <Trophy size={48} className="mx-auto text-amber-400 mb-3" />
            <h1 className="font-display font-black text-3xl text-text-primary">
              {results.passed ? "Quiz Complete!" : "Keep Practicing!"}
            </h1>
            <p className="text-sm text-brand-secondary mt-2">Your Performance</p>

            <div className="mt-6 text-6xl font-black text-amber-400">{results.grade}</div>
            <p className="text-2xl font-bold text-text-primary mt-2">
              {results.score_percentage}% Score
            </p>

            <div className="grid grid-cols-3 gap-3 mt-6">
              <div className="bg-surface-base/40 rounded-xl p-3">
                <div className="text-2xl font-black text-green-400">{results.correct}</div>
                <div className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">Correct</div>
              </div>
              <div className="bg-surface-base/40 rounded-xl p-3">
                <div className="text-2xl font-black text-red-400">{results.incorrect}</div>
                <div className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">Incorrect</div>
              </div>
              <div className="bg-surface-base/40 rounded-xl p-3">
                <div className="text-2xl font-black text-amber-400">+{results.total_xp}</div>
                <div className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">XP</div>
              </div>
            </div>

            {results.badge_earned && (
              <div className="mt-6 p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30">
                <div className="flex items-center justify-center gap-2">
                  <Award size={20} className="text-amber-400" />
                  <span className="font-display font-bold text-amber-400">
                    Badge Earned: {results.score_percentage >= 95 ? "Quiz Master" : "High Scorer"}
                  </span>
                </div>
              </div>
            )}

            {results.weak_areas && results.weak_areas.length > 0 && (
              <div className="mt-6 p-4 rounded-2xl bg-orange-500/10 border border-orange-500/20 text-left">
                <h3 className="font-display font-bold text-sm text-orange-400 mb-2">Areas to Improve</h3>
                <ul className="space-y-1">
                  {results.weak_areas.map((a, i) => (
                    <li key={i} className="text-xs text-text-primary">
                      • {a.topic} ({Math.round(a.success_rate * 100)}% success)
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="flex gap-2 mt-6">
              <button
                onClick={() => {
                  setStage("setup");
                  setQuiz(null);
                  setAnswers([]);
                  setResults(null);
                }}
                className="flex-1 py-3 rounded-xl bg-surface-card border border-brand-primary/20 text-text-primary font-medium text-sm hover:border-brand-sky/40 transition-colors"
              >
                <RefreshCw size={16} className="inline mr-1" /> New Quiz
              </button>
              <Link
                to="/dashboard"
                className="flex-1 py-3 rounded-xl bg-brand-sky text-white font-medium text-sm text-center hover:bg-brand-sky/90 transition-colors"
              >
                Dashboard
              </Link>
            </div>
          </motion.div>
        </div>
      </div>
    );
  }

  // Playing stage
  if (!quiz) return null;
  const currentQ = quiz.questions[currentIndex];
  const diffColors = DIFFICULTY_COLORS[currentQ.difficulty] || DIFFICULTY_COLORS.medium;

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <CelebrationOverlay
        show={showCelebration}
        type="confetti"
        title="Correct!"
        subtitle={`+${currentResult?.xp_earned || 0} XP`}
        onClose={() => setShowCelebration(false)}
      />

      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-6">
        {/* Header with progress and timer */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono text-brand-secondary">
              {currentIndex + 1} / {quiz.questions.length}
            </span>
            <span className={`px-2 py-0.5 rounded-md text-[10px] font-mono uppercase border ${diffColors.bg} ${diffColors.text} ${diffColors.border}`}>
              {currentQ.difficulty}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="flex items-center gap-1 px-2 py-1 rounded-md bg-amber-500/10 text-amber-400 text-xs font-mono">
              <Zap size={12} /> +{xpEarned} XP
            </span>
            {quiz.time_limit_seconds > 0 && (
              <Timer seconds={timeLeft} onExpire={finishQuiz} paused={false} />
            )}
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-1.5 rounded-full bg-surface-card overflow-hidden mb-6">
          <div
            className="h-full bg-gradient-to-r from-brand-sky to-purple-500 rounded-full transition-all duration-500"
            style={{ width: `${((currentIndex + 1) / quiz.questions.length) * 100}%` }}
          />
        </div>

        {/* Question card */}
        <motion.div
          key={currentIndex}
          initial={reduced ? {} : { opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-surface-card/60 border border-brand-primary/20 rounded-2xl p-5 sm:p-6 mb-4"
        >
          <div className="flex items-start justify-between gap-3 mb-3">
            <h2 className="font-display font-bold text-lg text-text-primary flex-1">
              {currentQ.title || "Problem"}
            </h2>
            <span className="text-[10px] font-mono text-brand-secondary shrink-0">
              +{currentQ.xp_reward} XP
            </span>
          </div>

          <div className="text-sm text-text-primary leading-relaxed whitespace-pre-wrap">
            {currentQ.question}
          </div>

          {/* Why this matters - practice mode only */}
          {currentQ.why_this_matters && mode === "practice" && !currentResult && (
            <details className="mt-4 p-3 rounded-xl bg-blue-500/5 border border-blue-500/10">
              <summary className="text-xs font-mono uppercase tracking-widest text-blue-400 cursor-pointer">
                Why this matters
              </summary>
              <p className="text-sm text-text-primary mt-2 leading-relaxed">
                {currentQ.why_this_matters}
              </p>
            </details>
          )}

          {/* Test cases */}
          {currentQ.test_cases && currentQ.test_cases.length > 0 && !currentResult && (
            <details className="mt-3">
              <summary className="text-xs font-mono uppercase tracking-widest text-brand-secondary cursor-pointer">
                Test cases ({currentQ.test_cases.length})
              </summary>
              <div className="mt-2 space-y-1.5">
                {currentQ.test_cases.slice(0, 3).map((tc, i) => (
                  <div key={i} className="text-[11px] font-mono text-brand-secondary bg-surface-base/40 rounded-lg p-2">
                    <span className="text-brand-sky">Input:</span> {tc.input}<br/>
                    <span className="text-green-400">Output:</span> {tc.expected}
                  </div>
                ))}
              </div>
            </details>
          )}
        </motion.div>

        {/* Hint display */}
        {showHint && currentHint && !currentResult && (
          <div className="mb-4">
            <HintCard
              hint={currentHint}
              level={hintLevel}
              onNext={hintLevel < (currentQ.hints?.length || 0) ? requestHint : null}
              onRevealSolution={mode === "practice" ? () => setShowSolution(true) : null}
            />
          </div>
        )}

        {/* Solution display (after submit or give up) */}
        {(currentResult || showSolution) && currentQ.solution && (
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className={`mb-4 rounded-2xl border p-5 ${
              currentResult?.is_correct
                ? "bg-green-500/5 border-green-500/20"
                : "bg-red-500/5 border-red-500/20"
            }`}
          >
            <div className="flex items-center gap-2 mb-3">
              {currentResult?.is_correct ? (
                <CheckCircle2 size={20} className="text-green-400" />
              ) : currentResult ? (
                <XCircle size={20} className="text-red-400" />
              ) : (
                <Lightbulb size={20} className="text-amber-400" />
              )}
              <h3 className="font-display font-bold text-sm text-text-primary">
                {currentResult?.is_correct ? "Correct!" : currentResult ? "Not quite" : "Solution"}
              </h3>
              {currentResult && (
                <span className="ml-auto px-2 py-0.5 rounded-md bg-amber-500/10 text-amber-400 text-xs font-mono">
                  +{currentResult.xp_earned} XP
                </span>
              )}
            </div>

            {currentQ.solution.code && (
              <pre className="bg-surface-base text-text-primary rounded-xl p-4 text-xs font-mono overflow-x-auto mb-3">
                <code>{currentQ.solution.code}</code>
              </pre>
            )}

            <div className="grid grid-cols-2 gap-2 text-[10px] mb-3">
              <div className="bg-surface-base/40 rounded-lg p-2">
                <span className="text-brand-secondary">Time:</span>{" "}
                <span className="font-mono text-text-primary">{currentQ.solution.time_complexity}</span>
              </div>
              <div className="bg-surface-base/40 rounded-lg p-2">
                <span className="text-brand-secondary">Space:</span>{" "}
                <span className="font-mono text-text-primary">{currentQ.solution.space_complexity}</span>
              </div>
            </div>

            {currentResult?.real_world_use && (
              <details className="mt-2">
                <summary className="text-xs font-mono text-brand-secondary cursor-pointer">
                  Real-world use
                </summary>
                <p className="text-sm text-text-primary mt-1">{currentResult.real_world_use}</p>
              </details>
            )}

            {currentResult?.common_mistakes && (
              <details className="mt-2">
                <summary className="text-xs font-mono text-orange-400 cursor-pointer">
                  Common mistakes
                </summary>
                <p className="text-sm text-text-primary mt-1 whitespace-pre-wrap">
                  {currentResult.common_mistakes}
                </p>
              </details>
            )}
          </motion.div>
        )}

        {/* Action buttons */}
        <div className="flex gap-2">
          {!currentResult && !showSolution ? (
            <>
              {mode === "practice" && currentQ.hints?.length > 0 && !showHint && (
                <button
                  onClick={requestHint}
                  className="flex-1 py-3 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-400 font-medium text-sm hover:bg-amber-500/20 transition-colors"
                >
                  <Lightbulb size={16} className="inline mr-1" /> Get Hint
                </button>
              )}
              <button
                onClick={submitAnswer}
                disabled={submitting}
                className="flex-[2] py-3 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 text-white font-bold text-sm hover:from-green-400 hover:to-emerald-400 transition-all disabled:opacity-50"
              >
                {submitting ? <Spinner size={16} /> : (
                  <span className="flex items-center justify-center gap-2">
                    <Check size={16} /> Submit Answer
                  </span>
                )}
              </button>
            </>
          ) : (
            <button
              onClick={nextQuestion}
              className="w-full py-3 rounded-xl bg-gradient-to-r from-brand-sky to-purple-500 text-white font-bold text-sm hover:from-brand-sky/90 hover:to-purple-500/90 transition-all"
            >
              {currentIndex + 1 < quiz.questions.length ? (
                <span className="flex items-center justify-center gap-2">
                  Next Question <ArrowRight size={16} />
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <Trophy size={16} /> See Results
                </span>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
