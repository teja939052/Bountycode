import { useState, useEffect, useRef } from "react";
import { useParams, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import {
  Building2, Lock, ArrowRight, CheckCircle, XCircle,
  Clock, Trophy, AlertTriangle, Zap, ArrowLeft, RotateCcw, Target
} from "lucide-react";
import useReducedMotion from "../hooks/useReducedMotion";
import AnimatedCard from "../components/motion/AnimatedCard";

const TIER_COLORS = {
  FAANG: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 border-red-200 dark:border-red-800",
  Product: "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400 border-purple-200 dark:border-purple-800",
  Services: "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 border-blue-200 dark:border-blue-800",
  Startup: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 border-green-200 dark:border-green-800",
};

const TYPE_COLORS = {
  aptitude: "bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-400",
  coding: "bg-emerald-100 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-400",
  behavioral: "bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400",
  system_design: "bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400",
};

export default function CompanyMocks() {
  const { testId } = useParams();
  const [companies, setCompanies] = useState([]);
  const [activeTest, setActiveTest] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);
  const [history, setHistory] = useState([]);
  const reduced = useReducedMotion();
  const timerRef = useRef(null);

  const isPro = false; // will be set from user store in real impl

  useEffect(() => {
    if (testId) {
      loadTestState(testId);
    } else {
      loadCompanies();
      loadHistory();
    }
    return () => clearInterval(timerRef.current);
  }, [testId]);

  const loadCompanies = async () => {
    setLoading(true);
    try {
      const data = await api.getMockCompanies();
      setCompanies(data.companies || []);
    } catch {} finally {
      setLoading(false);
    }
  };

  const loadHistory = async () => {
    try {
      const data = await api.getMockHistory();
      setHistory(data.tests || []);
    } catch {}
  };

  const loadTestState = async (id) => {
    setLoading(true);
    try {
      const data = await api.getMockHistory();
      const found = (data.tests || []).find((t) => t.test_id === id);
      if (found && found.status === "completed") {
        setResult(found);
      } else {
        // Try to reconstruct from localStorage or start fresh
        setActiveTest(null);
      }
    } catch {} finally {
      setLoading(false);
    }
  };

  const handleStart = async (companyId) => {
    setLoading(true);
    try {
      const data = await api.startMockTest(companyId);
      setActiveTest(data);
      setAnswers({});
      setResult(null);
      setTimeLeft(data.duration_minutes * 60);
      startTimer(data.duration_minutes * 60);
    } catch (err) {
      if (err.message?.includes("Pro-only") || err.message?.includes("limit")) {
        alert(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const startTimer = (seconds) => {
    clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setTimeLeft((t) => {
        if (t <= 1) {
          clearInterval(timerRef.current);
          handleComplete(true);
          return 0;
        }
        return t - 1;
      });
    }, 1000);
  };

  const handleAnswer = (index, value) => {
    setAnswers((prev) => ({ ...prev, [index]: value }));
  };

  const handleComplete = async (auto = false) => {
    clearInterval(timerRef.current);
    setSubmitting(true);
    try {
      const data = await api.completeMockTest(activeTest.test_id, answers);
      setResult(data);
      setActiveTest(null);
      loadHistory();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const formatTime = (s) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  // Result view
  if (result) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <Link to="/company-mocks" className="inline-flex items-center gap-1 text-sm text-brand-muted hover:text-primary-600 mb-6">
            <ArrowLeft size={16} /> All Mock Tests
          </Link>

          <AnimatedCard className="card mb-6">
            <div className="text-center mb-6">
              <h2 className="text-2xl font-bold dark:text-white">{result.company} Mock Test</h2>
              <p className="text-brand-muted">{result.paper_name}</p>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="text-center">
                <p className="text-3xl font-bold text-primary-600">{result.percentage}%</p>
                <p className="text-sm text-brand-muted">Score</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold">{result.score}/{result.total}</p>
                <p className="text-sm text-brand-muted">Correct</p>
              </div>
              <div className="text-center">
                <p className={`text-3xl font-bold ${result.passed ? "text-green-600" : "text-red-600"}`}>
                  {result.passed ? "PASSED" : "FAILED"}
                </p>
                <p className="text-sm text-brand-muted">Passing: {result.passing_score}%</p>
              </div>
            </div>

            {result.section_scores && Object.keys(result.section_scores).length > 0 && (
              <div className="mb-6">
                <h3 className="font-bold mb-3 dark:text-white">Section Breakdown</h3>
                <div className="space-y-2">
                  {Object.entries(result.section_scores).map(([section, s]: [string, any]) => (
                    <div key={section} className="flex items-center justify-between bg-surface-base dark:bg-gray-700/50 rounded-lg px-4 py-2">
                      <span className="capitalize text-sm font-medium dark:text-white">{section}</span>
                      <span className="text-sm text-brand-secondary dark:text-gray-400">
                        {s.correct}/{s.total} ({s.percentage}%)
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {result.weak_topics && result.weak_topics.length > 0 && (
              <div className="mb-6">
                <h3 className="font-bold mb-3 flex items-center gap-2 dark:text-white">
                  <AlertTriangle size={18} className="text-orange-500" />
                  Weak Topics
                </h3>
                <div className="flex flex-wrap gap-2">
                  {result.weak_topics.map((w, i) => (
                    <span key={i} className="px-3 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-400 rounded-full text-sm">
                      {w.topic} ({w.accuracy}%)
                    </span>
                  ))}
                </div>
              </div>
            )}

            {result.gap_analysis && (
              <div className="bg-primary-50 dark:bg-primary-900/20 rounded-xl p-6">
                <h3 className="font-bold mb-3 flex items-center gap-2 dark:text-white">
                  <Target size={18} className="text-primary-600" />
                  Gap Analysis
                </h3>
                <p className="text-sm text-brand-secondary dark:text-gray-400 mb-4">{result.gap_analysis.headline}</p>
                {result.gap_analysis.actions?.length > 0 && (
                  <div className="space-y-3">
                    {result.gap_analysis.actions.slice(0, 3).map((action, i) => (
                      <div key={i} className="bg-surface-card bg-surface-card rounded-lg p-4 border border-brand-primary/10 dark:border-brand-primary/10">
                        <div className="flex items-center justify-between mb-1">
                          <span className="font-semibold text-sm dark:text-white">{action.skill.replace("_", " ").toUpperCase()}</span>
                          <span className={`text-xs px-2 py-0.5 rounded-full ${
                            action.priority === "critical" ? "bg-red-100 text-red-700" :
                            action.priority === "high" ? "bg-orange-100 text-orange-700" :
                            "bg-yellow-100 text-yellow-700"
                          }`}>{action.priority}</span>
                        </div>
                        <p className="text-sm text-brand-secondary dark:text-gray-400 mb-2">{action.action}</p>
                        <div className="flex items-center gap-4 text-xs text-brand-muted">
                          <span>From {action.from_probability}% → {action.to_probability}%</span>
                          <span>+{action.projected_boost_pct}% boost</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </AnimatedCard>

          <div className="flex gap-3">
            <Link to="/company-mocks" className="flex-1 btn-secondary text-center">Back to Tests</Link>
            <Link to="/predictor" className="flex-1 btn-primary text-center">View Full Predictor</Link>
          </div>
        </div>
      </div>
    );
  }

  // Active test view
  if (activeTest) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <Link to="/company-mocks" className="text-sm text-brand-muted hover:text-primary-600">Exit Test</Link>
            <div className="flex items-center gap-2 bg-surface-card/50 bg-surface-card px-4 py-2 rounded-lg">
              <Clock size={18} className="text-brand-muted" />
              <span className={`font-mono font-bold ${timeLeft < 60 ? "text-red-600" : "text-brand-primary dark:text-gray-300"}`}>
                {formatTime(timeLeft)}
              </span>
            </div>
          </div>

          <AnimatedCard className="card mb-6">
            <h2 className="text-xl font-bold dark:text-white mb-1">{activeTest.company} — {activeTest.paper_name}</h2>
            <p className="text-sm text-brand-muted">Question {Object.keys(answers).filter(k => answers[k]?.trim()).length} of {activeTest.total_questions} answered</p>
          </AnimatedCard>

          <div className="space-y-4">
            <AnimatePresence>
              {activeTest.questions?.map((q, idx) => (
                <motion.div
                  key={q.question_id || idx}
                  className="card"
                  initial={reduced ? {} : { opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.03 }}
                >
                  <div className="flex items-start gap-3 mb-3">
                    <span className="text-sm font-bold text-gray-400 mt-0.5">Q{idx + 1}.</span>
                    <div>
                      <div className="flex flex-wrap gap-2 mb-2">
                        <span className={`text-xs px-2 py-0.5 rounded-full ${TYPE_COLORS[q.type] || ""}`}>{q.type}</span>
                        <span className="text-xs px-2 py-0.5 rounded-full bg-surface-card/50 dark:bg-gray-700 text-brand-secondary dark:text-gray-400">{q.difficulty}</span>
                      </div>
                      <p className="font-medium dark:text-white">{q.question_title}</p>
                    </div>
                  </div>

                  {q.type === "aptitude" && q.options?.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 ml-8">
                      {q.options.map((opt, oi) => (
                        <button
                          key={oi}
                          onClick={() => handleAnswer(idx, opt)}
                          className={`text-left px-4 py-3 rounded-lg border-2 transition-colors text-sm ${
                            answers[idx] === opt
                              ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400"
                              : "border-brand-primary/10 dark:border-brand-primary/10 hover:border-brand-primary/20 dark:text-gray-300"
                          }`}
                        >
                          {opt}
                        </button>
                      ))}
                    </div>
                  ) : (
                    <textarea
                      value={answers[idx] || ""}
                      onChange={(e) => handleAnswer(idx, e.target.value)}
                      placeholder="Write your answer..."
                      className="w-full ml-8 px-4 py-3 border border-brand-primary/20 border-brand-primary/15 rounded-lg bg-surface-card bg-surface-card dark:text-white min-h-[100px] resize-y text-sm"
                    />
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
          </div>

          <div className="mt-8 flex gap-3">
            <button
              onClick={() => handleComplete(false)}
              disabled={submitting}
              className="flex-1 btn-primary flex items-center justify-center gap-2"
            >
              {submitting ? "Submitting..." : <><CheckCircle size={18} /> Submit Test</>}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Company list view
  return (
    <div className="min-h-screen py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <motion.div className="mb-8" initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center gap-3 mb-2">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center">
              <Building2 size={24} className="text-blue-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold dark:text-white">Company Mock Tests</h1>
              <p className="text-brand-secondary dark:text-gray-400">Timed papers that mirror real campus drives</p>
            </div>
          </div>
        </motion.div>

        {loading ? (
          <div className="space-y-3">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="card animate-pulse">
                <div className="h-4 bg-surface-card/50 dark:bg-gray-700 rounded w-1/2 mb-2" />
                <div className="h-3 bg-surface-card/50 dark:bg-gray-700 rounded w-1/3" />
              </div>
            ))}
          </div>
        ) : (
          <div className="grid md:grid-cols-2 gap-4">
            {companies.map((co) => (
              <motion.div
                key={co.id}
                className={`card border-2 transition-all ${co.locked ? "opacity-70" : "hover:border-primary-300 dark:hover:border-primary-700"}`}
                initial={reduced ? {} : { opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-bold text-lg dark:text-white">{co.name}</h3>
                    <p className="text-sm text-brand-muted">{co.paper_name}</p>
                  </div>
                  {co.locked && <Lock size={20} className="text-gray-400" />}
                </div>

                <div className="flex flex-wrap gap-2 mb-3">
                  <span className={`text-xs px-2 py-1 rounded-full border ${TIER_COLORS[co.tier] || "bg-surface-card/50 text-brand-secondary"}`}>
                    {co.tier}
                  </span>
                  <span className="text-xs px-2 py-1 rounded-full bg-surface-card/50 dark:bg-gray-700 text-brand-secondary dark:text-gray-400">
                    {co.duration_minutes} min
                  </span>
                  <span className="text-xs px-2 py-1 rounded-full bg-surface-card/50 dark:bg-gray-700 text-brand-secondary dark:text-gray-400">
                    {co.question_count} questions
                  </span>
                  <span className="text-xs px-2 py-1 rounded-full bg-surface-card/50 dark:bg-gray-700 text-brand-secondary dark:text-gray-400">
                    Pass: {co.passing_score}%
                  </span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-xs text-gray-400">{co.bank_size} questions in bank</span>
                  {co.locked ? (
                    <span className="text-xs text-brand-muted font-medium">Pro-only</span>
                  ) : (
                    <button onClick={() => handleStart(co.id)} className="btn-primary text-sm py-2">
                      Start Mock
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {history.length > 0 && (
          <div className="mt-10">
            <h3 className="font-bold mb-4 dark:text-white">Recent Mocks</h3>
            <div className="space-y-2">
              {history.slice(0, 5).map((h) => (
                <Link key={h.test_id} to={`/company-mocks/${h.test_id}`} className="block card hover:border-primary-300 transition-colors">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-semibold dark:text-white">{h.company}</p>
                      <p className="text-xs text-brand-muted">{h.paper_name} · {new Date(h.completed_at).toLocaleDateString()}</p>
                    </div>
                    <div className="text-right">
                      <p className={`font-bold ${h.passed ? "text-green-600" : "text-red-600"}`}>{h.percentage}%</p>
                      <p className="text-xs text-gray-400">{h.score}/{h.total}</p>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
