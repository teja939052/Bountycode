import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";
import { motion } from "framer-motion";
import { Brain, Clock, CheckCircle, XCircle, ArrowRight } from "lucide-react";

const CATEGORIES = [
  { id: "quantitative", name: "Quantitative", icon: "🔢", desc: "Math, Percentages, Time & Work", color: "text-cyber-blue" },
  { id: "logical", name: "Logical Reasoning", icon: "🧠", desc: "Patterns, Sequences, Deductions", color: "text-cyber-purple" },
  { id: "verbal", name: "Verbal Ability", icon: "📝", desc: "Grammar, Vocabulary, Comprehension", color: "text-cyber-green" },
  { id: "technical", name: "Technical MCQs", icon: "💻", desc: "Programming, CS Fundamentals", color: "text-cyber-orange" },
  { id: "data-interpretation", name: "Data Interpretation", icon: "📊", desc: "Charts, Graphs, Tables", color: "text-cyber-yellow" },
];

const DIFFICULTIES = [
  { id: "easy", name: "Easy", color: "text-cyber-green bg-cyber-green/10 border border-cyber-green/20" },
  { id: "medium", name: "Medium", color: "text-cyber-yellow bg-cyber-yellow/10 border border-cyber-yellow/20" },
  { id: "hard", name: "Hard", color: "text-cyber-red bg-cyber-red/10 border border-cyber-red/20" },
];

export default function AptitudeTest() {
  const [step, setStep] = useState("select");
  const [category, setCategory] = useState("");
  const [difficulty, setDifficulty] = useState("medium");
  const [testId, setTestId] = useState("");
  const [questions, setQuestions] = useState([]);
  const [currentQ, setCurrentQ] = useState(0);
  const [answers, setAnswers] = useState({});
  const [answerFeedback, setAnswerFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [timeTaken, setTimeTaken] = useState(0);
  const [startTime, setStartTime] = useState(null);
  const [showCelebration, setShowCelebration] = useState(false);

  useEffect(() => {
    let interval;
    if (step === "test" && startTime) {
      interval = setInterval(() => setTimeTaken(Math.floor((Date.now() - startTime) / 1000)), 1000);
    }
    return () => clearInterval(interval);
  }, [step, startTime]);

  const startTest = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.startAptitudeTest(category, difficulty, 10);
      setTestId(data.test_id);
      setQuestions(data.questions);
      setCurrentQ(0);
      setAnswers({});
      setStartTime(Date.now());
      setTimeTaken(0);
      setStep("test");
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const submitAnswer = async (answer) => {
    setLoading(true);
    setError("");
    try {
      const data = await api.submitAptitudeAnswer(testId, currentQ, answer);
      setAnswers({ ...answers, [currentQ]: answer });
      setAnswerFeedback(data);
      setTimeout(() => {
        setAnswerFeedback(null);
        if (currentQ < questions.length - 1) {
          setCurrentQ(currentQ + 1);
        } else {
          completeTest();
        }
      }, 2000);
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const completeTest = async () => {
    setLoading(true);
    try {
      const data = await api.completeAptitudeTest(testId, timeTaken);
      setResult(data);
      setStep("results");
      if (data.percentage >= 80) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 3000);
      }
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const formatTime = (s) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  // SELECT SCREEN
  if (step === "select") {
    return (
      <div className="min-h-screen py-12 px-4">
        <CelebrationOverlay show={showCelebration} type="perfect" message="System Diagnostics Clear!" />
        <div className="max-w-4xl mx-auto">
          <motion.div
            className="text-center mb-10"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <span className="section-subheader mb-3 block">System Diagnostics</span>
            <h1 className="section-header text-3xl mb-2">
              <Brain className="text-cyber-purple inline mr-2" size={28} />
              Aptitude <span className="text-cyber-purple">Diagnostics</span>
            </h1>
            <p className="text-gray-500 font-mono text-sm">
              Campus placement prep with AI-generated questions
            </p>
          </motion.div>

          {error && (
            <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">{error}</div>
          )}

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
            {CATEGORIES.map((cat, i) => (
              <motion.button
                key={cat.id}
                onClick={() => setCategory(cat.id)}
                className={`card text-left transition-all border-2 ${
                  category === cat.id ? "border-cyber-purple bg-cyber-purple/10" : "border-transparent hover:border-space-border"
                }`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <span className="text-3xl mb-2 block">{cat.icon}</span>
                <h3 className={`font-display font-bold ${cat.color}`}>{cat.name}</h3>
                <p className="text-xs font-mono text-gray-500 mt-1">{cat.desc}</p>
              </motion.button>
            ))}
          </div>

          {category && (
            <div className="card">
              <h3 className="font-display font-bold text-white text-sm mb-4">Threat Level</h3>
              <div className="flex gap-3 mb-6">
                {DIFFICULTIES.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => setDifficulty(d.id)}
                    className={`px-4 py-2 rounded-lg font-mono text-xs transition-colors ${difficulty === d.id ? d.color : "bg-space-panel border border-space-border text-gray-500"}`}
                  >
                    {d.name}
                  </button>
                ))}
              </div>
              <div className="flex items-center justify-between">
                <p className="text-xs font-mono text-gray-500">10 questions • ~10 minutes</p>
                <button onClick={startTest} disabled={loading} className="btn-primary flex items-center gap-2">
                  {loading ? <Spinner size="sm" className="text-space-void" /> : "Initiate Diagnostics"}
                  <ArrowRight size={16} />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // TEST SCREEN
  if (step === "test" && questions.length > 0) {
    const q = questions[currentQ];
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-3xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <span className="text-xs font-mono text-gray-400">Query {currentQ + 1} / {questions.length}</span>
            <div className="flex items-center gap-2 text-sm font-mono text-gray-400">
              <Clock size={14} /> {formatTime(timeTaken)}
            </div>
          </div>

          <div className="w-full bg-space-panel rounded-full h-1.5 mb-8 border border-space-border">
            <div className="bg-gradient-to-r from-cyber-purple to-cyber-blue h-1.5 rounded-full transition-all duration-300" style={{ width: `${((currentQ + 1) / questions.length) * 100}%` }} />
          </div>

          {answerFeedback && (
            <motion.div
              className={`card mb-6 ${answerFeedback.is_correct ? "border-cyber-green/20 bg-cyber-green/5" : "border-cyber-red/20 bg-cyber-red/5"}`}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <div className="flex items-center gap-2 mb-2">
                {answerFeedback.is_correct ? (
                  <CheckCircle className="text-cyber-green" size={20} />
                ) : (
                  <XCircle className="text-cyber-red" size={20} />
                )}
                <span className={`font-display font-bold ${answerFeedback.is_correct ? "text-cyber-green" : "text-cyber-red"}`}>
                  {answerFeedback.is_correct ? "Correct!" : "Incorrect"}
                </span>
              </div>
              <p className="text-xs font-mono text-gray-400">{answerFeedback.explanation}</p>
            </motion.div>
          )}

          <div className="card mb-6">
            <p className="font-display font-bold text-white text-lg mb-6">{q.question}</p>
            <div className="space-y-3">
              {q.options.map((option, idx) => (
                <button
                  key={idx}
                  onClick={() => submitAnswer(idx)}
                  disabled={loading || answerFeedback !== null}
                  className={`w-full text-left p-4 rounded-lg border-2 transition-all font-mono text-sm ${
                    answers[currentQ] === idx
                      ? "border-cyber-purple bg-cyber-purple/10 text-white"
                      : "border-space-border hover:border-gray-500 text-gray-400 hover:text-white"
                  } ${answerFeedback !== null ? "cursor-not-allowed opacity-70" : ""}`}
                >
                  <span className="font-bold text-cyber-blue">{String.fromCharCode(65 + idx)}.</span> {option}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // RESULTS SCREEN
  if (step === "results" && result) {
    return (
      <div className="min-h-screen py-12 px-4">
        <CelebrationOverlay show={showCelebration} type="perfect" message="Diagnostics Passed!" />
        <div className="max-w-4xl mx-auto">
          <div className="card mb-8 text-center">
            <span className="section-subheader mb-3 block">Diagnostics Complete</span>
            <div className={`w-32 h-32 rounded-full flex items-center justify-center text-4xl font-display font-black mx-auto border-2 ${
              result.percentage >= 80 ? "text-cyber-green bg-cyber-green/10 border-cyber-green/30" :
              result.percentage >= 50 ? "text-cyber-yellow bg-cyber-yellow/10 border-cyber-yellow/30" :
              "text-cyber-red bg-cyber-red/10 border-cyber-red/30"
            }`}>
              {result.percentage}%
            </div>
            <p className="text-gray-500 font-mono text-sm mt-3">
              {result.score}/{result.total_questions} correct
            </p>
            <p className="text-xs font-mono text-gray-600 mt-1">Time: {formatTime(result.time_taken)}</p>
          </div>

          <div className="grid sm:grid-cols-2 gap-4 mb-6">
            {result.weak_areas?.length > 0 && (
              <div className="card border-cyber-red/20">
                <h3 className="font-display font-bold text-cyber-red text-sm mb-2">⚠ Weak Sectors</h3>
                <div className="flex flex-wrap gap-2">
                  {result.weak_areas.map((area, i) => (
                    <span key={i} className="px-3 py-1 bg-cyber-red/10 border border-cyber-red/20 text-cyber-red rounded-full text-[10px] font-mono">{area}</span>
                  ))}
                </div>
              </div>
            )}
            {result.strong_areas?.length > 0 && (
              <div className="card border-cyber-green/20">
                <h3 className="font-display font-bold text-cyber-green text-sm mb-2">✅ Strong Sectors</h3>
                <div className="flex flex-wrap gap-2">
                  {result.strong_areas.map((area, i) => (
                    <span key={i} className="px-3 py-1 bg-cyber-green/10 border border-cyber-green/20 text-cyber-green rounded-full text-[10px] font-mono">{area}</span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="space-y-4">
            {result.questions?.map((q, i) => (
              <div key={i} className="card">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="font-display font-bold text-white text-sm">Q{i + 1}: {q.question}</h3>
                  {q.is_correct ? (
                    <CheckCircle className="text-cyber-green shrink-0" size={18} />
                  ) : (
                    <XCircle className="text-cyber-red shrink-0" size={18} />
                  )}
                </div>
                <div className="text-xs font-mono space-y-1">
                  <p className="text-gray-400">Your answer: {q.options[q.your_answer] || "Not answered"}</p>
                  {!q.is_correct && <p className="text-cyber-green">Correct: {q.options[q.correct_answer]}</p>}
                  <p className="text-gray-600 italic">{q.explanation}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="flex gap-4 mt-8">
            <button onClick={() => { setStep("select"); setResult(null); }} className="flex-1 btn-primary text-center">
              Run Diagnostics Again
            </button>
            <Link to="/dashboard" className="flex-1 btn-secondary text-center">Command Deck</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Spinner size="lg" />
    </div>
  );
}
