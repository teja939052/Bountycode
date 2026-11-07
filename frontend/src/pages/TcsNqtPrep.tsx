import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Brain, Clock, CheckCircle2, XCircle, ArrowRight,
  Target, Trophy, ChevronRight, Filter,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";

type Pattern = {
  pattern: string;
  count: number;
  domains: string[];
  skills: string[];
};

type Question = {
  id: string;
  pattern: string;
  skill: string;
  domain: string;
  difficulty: string;
  trust_status: string;
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
  hints: string[];
  common_mistakes: string[];
  time_estimate_sec: number;
  company_relevance: Record<string, number>;
};

type AssessResult = {
  pattern: string;
  score: number;
  correct: number;
  total: number;
  passed: boolean;
  mastery_threshold: number;
  results: Array<{
    id: string;
    correct: boolean;
    your_answer: string;
    correct_answer: string;
    explanation: string;
    common_mistakes: string[];
  }>;
  message: string;
};

type Step = "patterns" | "practice" | "result";

export default function TcsNqtPrep() {
  const [step, setStep] = useState<Step>("patterns");
  const [patterns, setPatterns] = useState<Pattern[]>([]);
  const [selectedPattern, setSelectedPattern] = useState<string | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [feedback, setFeedback] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<AssessResult | null>(null);
  const [startTime, setStartTime] = useState<number | null>(null);
  const [timeTaken, setTimeTaken] = useState(0);
  const [showExplanation, setShowExplanation] = useState(false);
  const [difficulty, setDifficulty] = useState("all");

  useEffect(() => {
    loadPatterns();
  }, []);

  useEffect(() => {
    let interval: number;
    if (step === "practice" && startTime) {
      interval = window.setInterval(() => setTimeTaken(Math.floor((Date.now() - startTime) / 1000)), 1000);
    }
    return () => clearInterval(interval);
  }, [step, startTime]);

  const loadPatterns = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.tcsNqt.getPatterns();
      setPatterns(data.patterns || []);
    } catch (err: any) {
      setError(err.message || "Failed to load patterns");
    }
    setLoading(false);
  };

  const loadQuestions = async (pattern: string) => {
    setLoading(true);
    setError("");
    setSelectedPattern(pattern);
    try {
      const data = await api.tcsNqt.getPatternQuestions(pattern, {
        limit: 10,
        difficulty: difficulty === "all" ? undefined : difficulty,
      });
      setQuestions(data.questions || []);
      setCurrentQ(0);
      setAnswers({});
      setFeedback(null);
      setResult(null);
      setShowExplanation(false);
      setStartTime(Date.now());
      setTimeTaken(0);
      setStep("practice");
    } catch (err: any) {
      setError(err.message || "Failed to load questions");
    }
    setLoading(false);
  };

  const submitAnswer = (answer: string) => {
    const q = questions[currentQ];
    const qid = q.id;
    const newAnswers = { ...answers, [qid]: answer };
    setAnswers(newAnswers);

    const correctIndex = q.options.findIndex(
      (opt) => opt.toLowerCase() === q.correct_answer.toLowerCase()
    );
    const isCorrect = answer.toLowerCase() === q.correct_answer.toLowerCase();

    setFeedback({
      correct: isCorrect,
      correctAnswer: q.correct_answer,
      explanation: q.explanation,
      commonMistakes: q.common_mistakes,
      yourAnswer: answer,
    });
    setShowExplanation(true);
  };

  const nextQuestion = () => {
    if (currentQ < questions.length - 1) {
      setCurrentQ(currentQ + 1);
      setFeedback(null);
      setShowExplanation(false);
    } else {
      finishAssessment();
    }
  };

  const finishAssessment = async () => {
    setLoading(true);
    try {
      const data = await api.tcsNqt.assessPattern(
        selectedPattern || "",
        answers,
        timeTaken
      );
      setResult(data);
      setStep("result");
    } catch (err: any) {
      setError(err.message || "Failed to submit assessment");
    }
    setLoading(false);
  };

  const resetPractice = () => {
    setStep("patterns");
    setSelectedPattern(null);
    setQuestions([]);
    setCurrentQ(0);
    setAnswers({});
    setFeedback(null);
    setResult(null);
    setShowExplanation(false);
    setStartTime(null);
    setTimeTaken(0);
  };

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  const currentQuestion = questions[currentQ];

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <Link to="/" className="text-brand-secondary hover:text-brand-primary text-sm mb-4 inline-block">
            ← Back to Home
          </Link>
          <h1 className="text-3xl font-bold text-text-primary mb-2">
            TCS NQT Prep
          </h1>
          <p className="text-text-secondary">
            Master patterns for TCS NQT with interactive practice and assessment.
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400">
            {error}
          </div>
        )}

        <AnimatePresence mode="wait">
          {step === "patterns" && (
            <motion.div
              key="patterns"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {/* Stats */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
                <div className="glass rounded-xl p-4">
                  <div className="text-2xl font-bold text-cyber-blue">{patterns.length}</div>
                  <div className="text-sm text-text-secondary">Patterns</div>
                </div>
                <div className="glass rounded-xl p-4">
                  <div className="text-2xl font-bold text-cyber-green">
                    {patterns.reduce((sum, p) => sum + p.count, 0)}
                  </div>
                  <div className="text-sm text-text-secondary">Questions</div>
                </div>
                <div className="glass rounded-xl p-4">
                  <div className="text-2xl font-bold text-cyber-purple">
                    {patterns.filter(p => p.domains.includes("Quantitative Aptitude")).length}
                  </div>
                  <div className="text-sm text-text-secondary">Quant Patterns</div>
                </div>
              </div>

              {/* Filter */}
              <div className="mb-6 flex items-center gap-3">
                <Filter size={18} className="text-text-secondary" />
                <select
                  value={difficulty}
                  onChange={(e) => setDifficulty(e.target.value)}
                  className="bg-surface border border-white/10 rounded-lg px-3 py-2 text-sm text-text-primary"
                >
                  <option value="all">All Difficulties</option>
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>

              {/* Pattern Grid */}
              {loading ? (
                <div className="flex justify-center py-12">
                  <Spinner size="lg" />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {patterns.map((p, idx) => (
                    <motion.button
                      key={p.pattern}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.05 }}
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => loadQuestions(p.pattern)}
                      className="glass rounded-xl p-5 text-left hover:border-cyber-blue/30 transition-all group"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="font-semibold text-text-primary group-hover:text-cyber-blue transition-colors">
                            {p.pattern}
                          </h3>
                          <p className="text-xs text-text-secondary mt-1">
                            {p.domains.slice(0, 2).join(" • ")}
                          </p>
                        </div>
                        <ChevronRight size={18} className="text-text-secondary group-hover:text-cyber-blue transition-colors" />
                      </div>
                      <div className="flex items-center gap-4 text-xs text-text-secondary">
                        <span className="flex items-center gap-1">
                          <Target size={12} />
                          {p.count} questions
                        </span>
                        {p.skills.length > 0 && (
                          <span className="truncate">{p.skills[0]}</span>
                        )}
                      </div>
                    </motion.button>
                  ))}
                </div>
              )}
            </motion.div>
          )}

          {step === "practice" && currentQuestion && (
            <motion.div
              key="practice"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Progress */}
              <div className="glass rounded-xl p-4">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Brain size={18} className="text-cyber-blue" />
                    <span className="font-semibold text-text-primary">
                      {selectedPattern}
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-text-secondary">
                    <span className="flex items-center gap-1">
                      <Clock size={14} />
                      {formatTime(timeTaken)}
                    </span>
                    <span>
                      {currentQ + 1}/{questions.length}
                    </span>
                  </div>
                </div>
                <div className="h-2 bg-surfaceElevated rounded-full overflow-hidden">
                  <motion.div
                    className="h-full bg-cyber-blue"
                    initial={{ width: 0 }}
                    animate={{ width: `${((currentQ + 1) / questions.length) * 100}%` }}
                    transition={{ duration: 0.3 }}
                  />
                </div>
              </div>

              {/* Question */}
              <div className="glass rounded-xl p-6">
                <div className="flex items-start justify-between mb-4">
                  <span className="text-xs font-medium px-2 py-1 rounded bg-cyber-blue/10 text-cyber-blue">
                    {currentQuestion.domain}
                  </span>
                  <span className="text-xs text-text-secondary">
                    {currentQuestion.difficulty}
                  </span>
                </div>

                <h3 className="text-lg font-medium text-text-primary mb-6 leading-relaxed">
                  {currentQuestion.question}
                </h3>

                <div className="space-y-3">
                  {currentQuestion.options.map((opt, idx) => {
                    const isSelected = feedback
                      ? opt.toLowerCase() === feedback.yourAnswer?.toLowerCase()
                      : answers[currentQuestion.id]?.toLowerCase() === opt.toLowerCase();
                    const isCorrect = opt.toLowerCase() === currentQuestion.correct_answer.toLowerCase();

                    let btnClass = "w-full text-left p-4 rounded-xl border transition-all ";
                    if (showExplanation && feedback) {
                      if (isCorrect) {
                        btnClass += "border-cyber-green/50 bg-cyber-green/10 ";
                      } else if (isSelected) {
                        btnClass += "border-cyber-red/50 bg-cyber-red/10 ";
                      } else {
                        btnClass += "border-white/5 opacity-60 ";
                      }
                    } else if (isSelected) {
                      btnClass += "border-cyber-blue/50 bg-cyber-blue/10 ";
                    } else {
                      btnClass += "border-white/10 hover:border-cyber-blue/30 hover:bg-surfaceElevated ";
                    }

                    return (
                      <button
                        key={idx}
                        onClick={() => !showExplanation && submitAnswer(opt)}
                        disabled={showExplanation}
                        className={btnClass}
                      >
                        <div className="flex items-center gap-3">
                          <span className="w-8 h-8 rounded-full bg-surfaceElevated flex items-center justify-center text-sm font-mono text-text-secondary shrink-0">
                            {String.fromCharCode(65 + idx)}
                          </span>
                          <span className="text-text-primary">{opt}</span>
                          {showExplanation && isCorrect && (
                            <CheckCircle2 size={18} className="text-cyber-green ml-auto shrink-0" />
                          )}
                          {showExplanation && isSelected && !isCorrect && (
                            <XCircle size={18} className="text-cyber-red ml-auto shrink-0" />
                          )}
                        </div>
                      </button>
                    );
                  })}
                </div>

                {/* Feedback */}
                <AnimatePresence>
                  {showExplanation && feedback && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      exit={{ opacity: 0, height: 0 }}
                      className="mt-6 space-y-4"
                    >
                      <div className={`p-4 rounded-xl ${feedback.correct ? "bg-cyber-green/10 border border-cyber-green/20" : "bg-cyber-red/10 border border-cyber-red/20"}`}>
                        <div className="flex items-center gap-2 mb-2">
                          {feedback.correct ? (
                            <CheckCircle2 size={18} className="text-cyber-green" />
                          ) : (
                            <XCircle size={18} className="text-cyber-red" />
                          )}
                          <span className={`font-medium ${feedback.correct ? "text-cyber-green" : "text-cyber-red"}`}>
                            {feedback.correct ? "Correct!" : "Incorrect"}
                          </span>
                        </div>
                        {!feedback.correct && (
                          <p className="text-sm text-text-secondary">
                            Correct answer: <span className="text-cyber-green font-medium">{feedback.correctAnswer}</span>
                          </p>
                        )}
                      </div>

                      {feedback.explanation && (
                        <div className="p-4 bg-surfaceElevated/50 rounded-xl">
                          <h4 className="text-sm font-medium text-text-primary mb-2">Explanation</h4>
                          <p className="text-sm text-text-secondary whitespace-pre-wrap">{feedback.explanation}</p>
                        </div>
                      )}

                      {feedback.commonMistakes && feedback.commonMistakes.length > 0 && (
                        <div className="p-4 bg-cyber-yellow/5 border border-cyber-yellow/20 rounded-xl">
                          <h4 className="text-sm font-medium text-cyber-yellow mb-2">Common Mistakes</h4>
                          <ul className="space-y-1">
                            {feedback.commonMistakes.map((mistake: string, idx: number) => (
                              <li key={idx} className="text-sm text-text-secondary flex items-start gap-2">
                                <span className="text-cyber-yellow mt-0.5">•</span>
                                {mistake}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      <button
                        onClick={nextQuestion}
                        disabled={loading}
                        className="w-full py-3 bg-cyber-blue text-white rounded-xl font-medium hover:bg-cyber-blue/90 transition-colors disabled:opacity-50"
                      >
                        {currentQ < questions.length - 1 ? (
                          <span className="flex items-center justify-center gap-2">
                            Next Question <ArrowRight size={18} />
                          </span>
                        ) : (
                          <span className="flex items-center justify-center gap-2">
                            Finish Assessment <Trophy size={18} />
                          </span>
                        )}
                      </button>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          )}

          {step === "result" && result && (
            <motion.div
              key="result"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-6"
            >
              <div className="glass rounded-xl p-8 text-center">
                <div className={`w-20 h-20 rounded-full mx-auto mb-4 flex items-center justify-center ${result.passed ? "bg-cyber-green/10" : "bg-cyber-yellow/10"}`}>
                  <Trophy size={40} className={result.passed ? "text-cyber-green" : "text-cyber-yellow"} />
                </div>
                <h2 className="text-2xl font-bold text-text-primary mb-2">
                  {result.passed ? "Pattern Mastered!" : "Keep Practicing!"}
                </h2>
                <p className="text-text-secondary mb-6">{result.message}</p>

                <div className="grid grid-cols-3 gap-4 max-w-md mx-auto mb-6">
                  <div className="glass rounded-xl p-4">
                    <div className="text-2xl font-bold text-cyber-blue">{result.score}%</div>
                    <div className="text-xs text-text-secondary">Score</div>
                  </div>
                  <div className="glass rounded-xl p-4">
                    <div className="text-2xl font-bold text-cyber-green">{result.correct}</div>
                    <div className="text-xs text-text-secondary">Correct</div>
                  </div>
                  <div className="glass rounded-xl p-4">
                    <div className="text-2xl font-bold text-text-secondary">{result.total}</div>
                    <div className="text-xs text-text-secondary">Total</div>
                  </div>
                </div>

                <div className="flex gap-3 justify-center">
                  <button
                    onClick={resetPractice}
                    className="px-6 py-3 bg-surfaceElevated text-text-primary rounded-xl hover:bg-white/10 transition-colors"
                  >
                    Back to Patterns
                  </button>
                  <button
                    onClick={() => loadQuestions(result.pattern)}
                    disabled={loading}
                    className="px-6 py-3 bg-cyber-blue text-white rounded-xl hover:bg-cyber-blue/90 transition-colors disabled:opacity-50"
                  >
                    Practice Again
                  </button>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
