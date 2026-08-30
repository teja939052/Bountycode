import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import useAuthStore from "../store/authStore";
import {
  Flame,
  Trophy,
  ArrowLeft,
  CheckCircle2,
  XCircle,
  Lightbulb,
  RotateCcw,
  Play,
  Zap,
} from "lucide-react";
import CelebrationOverlay from "../components/CelebrationOverlay";
import AnimatedCard from "../components/motion/AnimatedCard";
import useReducedMotion from "../hooks/useReducedMotion";
import { requestWithRetry } from "../services/api/request.ts";

const DIFFICULTY_COLORS = {
  easy: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  medium: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400",
  hard: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400",
};

const LANGUAGES = [
  { value: "python", label: "Python" },
  { value: "javascript", label: "JavaScript" },
  { value: "java", label: "Java" },
  { value: "cpp", label: "C++" },
  { value: "c", label: "C" },
];

export default function ProblemOfTheDay() {
  const store = useAuthStore();
  const reduced = useReducedMotion();
  const [challenge, setChallenge] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showCelebration, setShowCelebration] = useState(false);
  const [activeTab, setActiveTab] = useState("problem");
  const [selectedLanguage, setSelectedLanguage] = useState("python");
  const [userCode, setUserCode] = useState("");
  const [codeRunning, setCodeRunning] = useState(false);
  const [runResult, setRunResult] = useState(null);
  const [revealedHints, setRevealedHints] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => { loadChallenge(); }, []);

  const loadChallenge = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    setUserCode("");
    setRunResult(null);
    setRevealedHints(0);
    try {
      const data = await requestWithRetry<{ problem: any; config: any; xp_reward: number; streak_bonus: number; already_completed: boolean }>("/api/v1/daily-problem/today");
      setChallenge(data);
    } catch {
      setError("Failed to load today's challenge.");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!challenge?.problem) return;
    setSubmitting(true);
    setError(null);
    try {
      const data = await requestWithRetry<{ all_passed: boolean; passed_count: number; total_cases: number; xp_gained: number; streak_bonus: number; time_taken: number }>("/api/v1/daily-problem/submit", {
        method: "POST",
        body: JSON.stringify({ problem_id: challenge.problem.id, code: userCode, language: selectedLanguage }),
      });
      setResult(data);
      if (data.all_passed) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 3000);
      }
    } catch {
      setError("Submission failed.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleRun = async () => {
    if (!userCode.trim()) return;
    setCodeRunning(true);
    try {
      const data = await requestWithRetry<{ success: boolean; stdout?: string; error?: string }>("/api/v1/compiler/execute", {
        method: "POST",
        body: JSON.stringify({ code: userCode, language: selectedLanguage, stdin: "", timeout: 10 }),
      });
      setRunResult(data);
    } catch {
      // silent
    } finally {
      setCodeRunning(false);
    }
  };

  const revealNextHint = () => {
    if (challenge?.problem?.hints && revealedHints < challenge.problem.hints.length) {
      setRevealedHints((n) => n + 1);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600 mx-auto mb-3" />
          <p className="text-sm text-gray-500">Loading today&apos;s challenge...</p>
        </div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-3">{error}</p>
          <button onClick={loadChallenge} className="text-sm text-primary-600 hover:underline">Try again</button>
        </div>
      </div>
    );
  }
  if (!challenge) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-brand-muted">No challenge available today.</p>
      </div>
    );
  }

  const problem = challenge.problem;
  const league = challenge.user_league || { name: "Bronze", emoji: "🥉" };
  const user = store.user;

  return (
    <div className="min-h-screen py-4 px-3 sm:py-6 sm:px-4 max-w-7xl mx-auto">
      <CelebrationOverlay show={showCelebration} type="perfect" message="Daily Challenge Solved!" onClose={() => setShowCelebration(false)} />

      {/* Header */}
      <motion.div
        initial={reduced ? {} : { opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-4 sm:mb-6"
      >
        <Link to="/" className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 mb-3 transition-colors">
          <ArrowLeft size={16} />
          Back to home
        </Link>
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="h-10 w-10 sm:h-12 sm:w-12 rounded-xl bg-orange-100 dark:bg-orange-900/30 border border-orange-300 dark:border-orange-800 flex items-center justify-center text-xl sm:text-2xl">
              {league.emoji}
            </div>
            <div className="absolute -bottom-1 -right-1 h-4 w-4 rounded-full bg-orange-500 flex items-center justify-center">
              <Flame size={8} className="text-white" />
            </div>
          </div>
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-text-primary dark:text-white">Problem of the Day</h1>
            <p className="text-xs sm:text-sm text-brand-muted dark:text-gray-400">
              {challenge.config?.category} · {challenge.config?.difficulty} · {challenge.config?.focus || "Daily challenge"}
            </p>
          </div>
        </div>
      </motion.div>

      {/* Main layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 sm:gap-6">
        {/* Left column — problem + code */}
        <div className="lg:col-span-8 space-y-4 sm:space-y-6">
          {/* League card */}
          <AnimatedCard className="card">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-orange-50 dark:bg-orange-900/20 flex items-center justify-center text-xl">
                {league.emoji}
              </div>
              <div className="flex-1">
                <div className="font-bold text-orange-700 dark:text-orange-400 text-sm uppercase tracking-wide">{league.name} League</div>
                <div className="text-xs text-brand-muted dark:text-gray-400">
                  {challenge.already_completed ? "Completed today!" : `+${challenge.streak_bonus || 50} XP bonus for daily streak`}
                </div>
              </div>
              {!challenge.already_completed && (
                <div className="hidden sm:flex items-center gap-1 rounded-lg bg-orange-50 dark:bg-orange-900/20 px-3 py-1.5">
                  <Zap size={14} className="text-orange-500" />
                  <span className="text-xs font-bold text-orange-700 dark:text-orange-400">+{challenge.xp_reward || 50} XP</span>
                </div>
              )}
            </div>
          </AnimatedCard>

          {/* Tabs */}
          <div className="flex items-center gap-1 bg-surface-card/50 p-1 rounded-xl border border-brand-primary/10 dark:border-gray-700">
            {[
              { key: "problem", label: "Problem", icon: FileText },
              { key: "code", label: "Code", icon: Code2 },
              { key: "leaderboard", label: "Leaderboard", icon: Trophy },
            ].map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-lg text-xs sm:text-sm font-medium transition-all ${
                  activeTab === tab.key
                    ? "bg-white dark:bg-gray-800 text-text-primary dark:text-white shadow-sm"
                    : "text-brand-muted dark:text-gray-400 hover:text-text-primary dark:hover:text-gray-200"
                }`}
              >
                <tab.icon size={14} />
                <span className="hidden sm:inline">{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Problem tab */}
          {activeTab === "problem" && problem && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <AnimatedCard className="card">
                <div className="flex items-center gap-3 mb-4">
                  <h2 className="text-lg sm:text-xl font-bold text-text-primary dark:text-white flex-1">{problem.question_title}</h2>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${DIFFICULTY_COLORS[problem.difficulty] || DIFFICULTY_COLORS.medium}`}>
                    {problem.difficulty?.charAt(0).toUpperCase() + problem.difficulty?.slice(1)}
                  </span>
                </div>
                <div className="flex flex-wrap gap-2 mb-4">
                  {(problem.topics || []).map((t, i) => (
                    <span key={i} className="px-2 py-1 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg text-xs font-mono border border-primary-100 dark:border-primary-800">
                      {t}
                    </span>
                  ))}
                </div>
                <div className="prose prose-sm dark:prose-invert max-w-none text-brand-primary dark:text-gray-300 leading-relaxed">
                  <div className="whitespace-pre-wrap text-sm sm:text-base">{problem.statement}</div>
                </div>
                {problem.constraints && problem.constraints.length > 0 && (
                  <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                    <h4 className="text-xs font-bold text-blue-700 dark:text-blue-400 mb-2 uppercase tracking-wide">Constraints</h4>
                    <ul className="text-xs text-blue-600 dark:text-blue-300 space-y-1">
                      {problem.constraints.map((c, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <span className="text-blue-400 mt-0.5">•</span>
                          <span>{c}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {problem.examples && problem.examples.length > 0 && (
                  <div className="mt-4 space-y-3">
                    <h3 className="font-semibold text-text-primary dark:text-white text-sm flex items-center gap-2">
                      <Code2 size={16} />
                      Examples
                    </h3>
                    {problem.examples.map((ex, i) => (
                      <div key={i} className="bg-surface-card/50 rounded-lg p-4 border border-brand-primary/10 dark:border-gray-700">
                        <div className="text-xs font-mono text-brand-muted mb-1">Input: {ex.input || "N/A"}</div>
                        <div className="text-sm font-mono text-green-700 dark:text-green-400 mb-1">Output: {ex.output || "N/A"}</div>
                        {ex.explanation && <div className="text-xs text-brand-muted mt-2 italic">{ex.explanation}</div>}
                      </div>
                    ))}
                  </div>
                )}
                {problem.hints && problem.hints.length > 0 && (
                  <div className="mt-4 space-y-2">
                    <button
                      onClick={revealNextHint}
                      disabled={revealedHints >= problem.hints.length}
                      className="flex items-center gap-2 px-3 py-2 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 text-amber-700 dark:text-amber-400 text-xs font-medium hover:bg-amber-100 dark:hover:bg-amber-900/30 transition-colors disabled:opacity-50"
                    >
                      <Lightbulb size={14} />
                      {revealedHints >= problem.hints.length ? "All hints revealed" : `Reveal hint ${revealedHints + 1} of ${problem.hints.length}`}
                    </button>
                    {revealedHints > 0 && (
                      <motion.div
                        initial={{ opacity: 0, y: 8 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="p-3 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800"
                      >
                        {problem.hints.slice(0, revealedHints).map((hint, i) => (
                          <div key={i} className="flex items-start gap-2 text-xs text-amber-800 dark:text-amber-300">
                            <span className="text-amber-500 mt-0.5">💡</span>
                            <span>{hint}</span>
                          </div>
                        ))}
                      </motion.div>
                    )}
                  </div>
                )}
                {challenge.already_completed && (
                  <div className="mt-4 flex items-center gap-2 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
                    <CheckCircle2 size={16} className="text-green-600" />
                    <span className="text-sm text-green-700 dark:text-green-400 font-medium">Already completed today! Come back tomorrow for a new challenge.</span>
                  </div>
                )}
              </AnimatedCard>
            </motion.div>
          )}

          {/* Code tab */}
          {activeTab === "code" && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <AnimatedCard className="card">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center gap-2">
                    <Flame size={18} className="text-primary-600" />
                    <h2 className="text-lg font-bold text-text-primary dark:text-white">Code Editor</h2>
                  </div>
                  <div className="flex items-center gap-2">
                    <select
                      value={selectedLanguage}
                      onChange={(e) => setSelectedLanguage(e.target.value)}
                      className="px-3 py-1.5 bg-surface-card border border-brand-primary/10 dark:border-gray-600 rounded-lg text-sm text-brand-primary dark:text-gray-200 focus:outline-none focus:border-primary-500"
                    >
                      {LANGUAGES.map((lang) => (
                        <option key={lang.value} value={lang.value}>{lang.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Code editor */}
                <div className="relative rounded-xl overflow-hidden border border-gray-300 dark:border-gray-600 bg-gray-900">
                  <div className="flex items-center justify-between px-4 py-2 bg-gray-800 border-b border-gray-700">
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1.5">
                        <div className="h-3 w-3 rounded-full bg-red-500/80" />
                        <div className="h-3 w-3 rounded-full bg-yellow-500/80" />
                        <div className="h-3 w-3 rounded-full bg-green-500/80" />
                      </div>
                      <span className="text-xs text-gray-400 ml-2">solution.{selectedLanguage === "cpp" ? "cpp" : selectedLanguage === "javascript" ? "js" : selectedLanguage}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={handleRun}
                        disabled={codeRunning || !userCode.trim()}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-700 hover:bg-gray-600 disabled:opacity-50 text-white text-xs font-medium rounded-lg transition-colors"
                      >
                        <Play size={12} />
                        {codeRunning ? "Running..." : "Run"}
                      </button>
                      <button
                        onClick={handleSubmit}
                        disabled={submitting || !userCode.trim() || challenge.already_completed}
                        className="flex items-center gap-1.5 px-4 py-1.5 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-white text-xs font-bold rounded-lg transition-colors"
                      >
                        <Zap size={12} />
                        {submitting ? "Submitting..." : "Submit"}
                      </button>
                    </div>
                  </div>
                  <textarea
                    value={userCode}
                    onChange={(e) => setUserCode(e.target.value)}
                    placeholder={`// Write your ${selectedLanguage} solution here...`}
                    className="w-full h-64 sm:h-80 p-4 bg-gray-900 text-green-400 font-mono text-sm leading-relaxed resize-none focus:outline-none"
                    spellCheck={false}
                    disabled={challenge.already_completed}
                  />
                </div>

                {/* Run result */}
                {runResult && (
                  <motion.div
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-3 p-4 bg-surface-card/50 rounded-xl border border-brand-primary/10 dark:border-gray-700"
                  >
                    <div className="flex items-center gap-2 mb-2">
                      {runResult.success ? (
                        <CheckCircle2 size={18} className="text-green-500" />
                      ) : (
                        <XCircle size={18} className="text-red-500" />
                      )}
                      <span className="font-bold text-sm">{runResult.success ? "Execution Success" : "Execution Failed"}</span>
                    </div>
                    {runResult.stdout && (
                      <div className="p-3 bg-gray-900 rounded-lg font-mono text-xs text-green-400 whitespace-pre-wrap">{runResult.stdout}</div>
                    )}
                    {runResult.error && (
                      <div className="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg font-mono text-xs text-red-600 dark:text-red-400 mt-2">{runResult.error}</div>
                    )}
                  </motion.div>
                )}

                {/* Submit result */}
                {result && (
                  <motion.div
                    initial={{ opacity: 0, y: 8, scale: 0.98 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    transition={{ type: "spring", stiffness: 200, damping: 20 }}
                    className="mt-4 p-5 bg-surface-card/50 rounded-xl border border-brand-primary/10 dark:border-gray-700"
                  >
                    <div className="flex items-center gap-3 mb-4">
                      {result.all_passed ? (
                        <div className="h-10 w-10 rounded-full bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                          <CheckCircle2 size={24} className="text-green-600" />
                        </div>
                      ) : (
                        <div className="h-10 w-10 rounded-full bg-yellow-100 dark:bg-yellow-900/30 flex items-center justify-center">
                          <XCircle size={24} className="text-yellow-600" />
                        </div>
                      )}
                      <div>
                        <p className="font-bold text-lg">{result.all_passed ? "All Test Cases Passed!" : `${result.passed_count || 0}/${result.total_cases || 0} Test Cases Passed`}</p>
                        <p className="text-xs text-brand-muted">{result.all_passed ? "Perfect solution!" : "Keep trying — you got this!"}</p>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="text-center p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                        <div className="text-xl font-bold text-primary-600">+{result.xp_gained || 0}</div>
                        <div className="text-[10px] text-brand-muted uppercase tracking-wide mt-1">XP Gained</div>
                      </div>
                      <div className="text-center p-3 bg-green-50 dark:bg-green-900/20 rounded-lg">
                        <div className="text-xl font-bold text-green-600">+{result.streak_bonus || 0}</div>
                        <div className="text-[10px] text-brand-muted uppercase tracking-wide mt-1">Streak Bonus</div>
                      </div>
                      <div className="text-center p-3 bg-amber-50 dark:bg-amber-900/20 rounded-lg">
                        <div className="text-xl font-bold text-amber-600">{(result.time_taken || 0).toFixed(1)}s</div>
                        <div className="text-[10px] text-brand-muted uppercase tracking-wide mt-1">Time</div>
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatedCard>
            </motion.div>
          )}

          {/* Leaderboard tab */}
          {activeTab === "leaderboard" && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <AnimatedCard className="card">
                <h2 className="text-lg font-bold text-text-primary dark:text-white mb-4 flex items-center gap-2">
                  <Trophy size={20} className="text-amber-500" />
                  Today&apos;s Leaderboard
                </h2>
                {!challenge.leaderboard || challenge.leaderboard.length === 0 ? (
                  <div className="text-center py-12">
                    <Trophy size={48} className="mx-auto mb-3 text-gray-300 dark:text-gray-600" />
                    <p className="text-sm text-brand-muted">No submissions yet. Be the first to solve!</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {challenge.leaderboard.map((entry, i) => (
                      <motion.div
                        key={i}
                        initial={{ opacity: 0, x: -12 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.05 }}
                        className="flex items-center gap-3 p-3 rounded-xl bg-surface-card/50 border border-brand-primary/5 dark:border-gray-700 hover:border-brand-primary/20 transition-colors"
                      >
                        <span className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold ${
                          i === 0 ? "bg-yellow-100 text-yellow-700" :
                          i === 1 ? "bg-gray-100 text-gray-600" :
                          i === 2 ? "bg-orange-100 text-orange-700" :
                          "bg-surface-card text-brand-muted"
                        }`}>
                          {i + 1}
                        </span>
                        <span className="flex-1 font-medium text-sm text-text-primary dark:text-white">{entry.user_name}</span>
                        <span className="text-xs text-brand-muted font-mono">{(entry.time_taken || 0).toFixed(1)}s</span>
                      </motion.div>
                    ))}
                  </div>
                )}
              </AnimatedCard>
            </motion.div>
          )}
        </div>

        {/* Right sidebar */}
        <div className="lg:col-span-4 space-y-4 sm:space-y-6">
          {/* Daily bonus */}
          {!challenge.already_completed && (
            <AnimatedCard className="card border-2 border-primary-200 dark:border-primary-800 bg-gradient-to-br from-primary-50 to-white dark:from-primary-900/20 dark:to-gray-800">
              <div className="text-center">
                <div className="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/30">
                  <Trophy size={28} className="text-primary-600" />
                </div>
                <h3 className="font-bold text-text-primary dark:text-white mb-1">Daily Bonus</h3>
                <p className="text-xs text-brand-muted dark:text-gray-400 mb-4">Solve today for +{challenge.streak_bonus || 50} bonus XP</p>
                <button
                  onClick={() => setActiveTab("code")}
                  className="w-full py-2.5 bg-primary-600 hover:bg-primary-700 text-white text-sm font-bold rounded-xl transition-colors shadow-sm"
                >
                  Start Coding
                </button>
              </div>
            </AnimatedCard>
          )}

          {/* User stats */}
          <AnimatedCard className="card">
            <h3 className="font-bold text-text-primary dark:text-white mb-4 flex items-center gap-2">
              <Flame size={16} className="text-orange-500" />
              Your Stats
            </h3>
            <div className="space-y-3">
              {[
                { label: "Streak", value: `${user?.streak || 0} days`, color: "text-orange-600" },
                { label: "XP", value: `${user?.xp || 0}`, color: "text-primary-600" },
                { label: "Level", value: `${user?.level || 1}`, color: "text-amber-600" },
              ].map((stat) => (
                <div key={stat.label} className="flex items-center justify-between p-2.5 rounded-lg bg-surface-card/50 border border-brand-primary/5 dark:border-gray-700">
                  <span className="text-xs text-brand-muted uppercase tracking-wide">{stat.label}</span>
                  <span className={`font-bold text-sm ${stat.color}`}>{stat.value}</span>
                </div>
              ))}
            </div>
          </AnimatedCard>

          {/* Tips */}
          <AnimatedCard className="card bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 border-blue-200 dark:border-blue-800">
            <div className="flex items-start gap-3">
              <div className="text-2xl">💡</div>
              <div>
                <h4 className="font-bold text-blue-900 dark:text-blue-100 text-sm mb-1">Pro Tip</h4>
                <p className="text-xs text-blue-700 dark:text-blue-300 leading-relaxed">
                  Solve the daily problem before midnight to maintain your streak! Consistency beats intensity.
                </p>
              </div>
            </div>
          </AnimatedCard>
        </div>
      </div>
    </div>
  );
}

