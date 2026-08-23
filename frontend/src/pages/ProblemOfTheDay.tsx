import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import { Flame, Trophy, ArrowLeft, CheckCircle2, XCircle, RotateCcw } from "lucide-react";
import CelebrationOverlay from "../components/CelebrationOverlay";
import AnimatedCard from "../components/motion/AnimatedCard";
import useReducedMotion from "../hooks/useReducedMotion";

const DIFFICULTY_COLORS = {
  easy: "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400",
  medium: "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400",
  hard: "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400",
};

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

  useEffect(() => { loadChallenge(); }, []);

  const loadChallenge = async () => {
    setLoading(true); setError(null); setResult(null); setUserCode(""); setRunResult(null);
    try {
      const data = await api.getDailyChallenge();
      setChallenge(data);
    } catch (err) { setError("Failed to load today challenge."); }
    finally { setLoading(false); }
  };

  const handleSubmit = async () => {
    if (!challenge?.problem) return;
    setSubmitting(true); setError(null);
    try {
      const data = await api.submitDailyChallenge(challenge.problem.id, userCode, selectedLanguage);
      setResult(data);
      if (data.all_passed) { setShowCelebration(true); setTimeout(() => setShowCelebration(false), 3000); }
    } catch (err) { setError("Submission failed."); }
    finally { setSubmitting(false); }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center"><div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" /></div>;
  if (error) return <div className="min-h-screen flex items-center justify-center"><p className="text-red-500">{error}</p></div>;
  if (!challenge) return <div className="min-h-screen flex items-center justify-center"><p className="text-brand-muted">No challenge available.</p></div>;

  const problem = challenge.problem;
  const league = challenge.user_league;
  const user = store.user;

  return (
    <div className="min-h-screen py-6 px-4 max-w-6xl mx-auto">
      <CelebrationOverlay show={showCelebration} type="perfect" message="Daily Challenge Solved!" onClose={() => setShowCelebration(false)} />
      <motion.div initial={reduced ? {} : { opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <ArrowLeft size={20} className="text-gray-400" />
          <Flame size={28} className="text-orange-500" />
          <h1 className="text-2xl font-bold text-text-primary dark:text-white">Problem of the Day</h1>
        </div>
        <p className="text-brand-muted dark:text-gray-400 text-sm ml-11">
          Daily Coding Challenge - {challenge.config?.category} - {challenge.config?.difficulty}
        </p>
      </motion.div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <AnimatedCard className="card">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-xl bg-orange-100 dark:bg-orange-900/30 border border-orange-300 dark:border-orange-800 flex items-center justify-center"><span className="text-2xl">{league.emoji}</span></div>
              <div><div className="font-bold text-orange-700 dark:text-orange-400 text-sm uppercase">{league.name} League</div><div className="text-xs text-brand-muted dark:text-gray-400">{challenge.streak_bonus} XP bonus daily</div></div>
            </div>
          </AnimatedCard>
          <div className="flex items-center gap-1 bg-surface-card/50 bg-surface-card p-1 rounded-xl">
            {["problem","code","leaderboard"].map((tab) => (
              <button key={tab} onClick={() => setActiveTab(tab)} className={"flex-1 py-2 px-4 rounded-lg text-xs font-medium transition-colors " + (activeTab === tab ? "bg-white bg-surface-card/50 text-text-primary dark:text-white shadow-sm" : "text-brand-muted dark:text-gray-400")}>
                {tab === "problem" ? "Problem" : tab === "code" ? "Code" : "Leaderboard"}
              </button>
            ))}
          </div>
          {activeTab === "problem" && problem && (
            <AnimatedCard className="card">
              <div className="flex items-center gap-3 mb-4">
                <h2 className="text-xl font-bold text-text-primary dark:text-white flex-1">{problem.question_title}</h2>
                <span className={"px-3 py-1 rounded-full text-xs font-medium " + (DIFFICULTY_COLORS[problem.difficulty] || DIFFICULTY_COLORS.medium)}>{problem.difficulty?.charAt(0).toUpperCase() + problem.difficulty?.slice(1)}</span>
              </div>
              {(problem.topics||[]).map((t,i) => <span key={i} className="px-2 py-0.5 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded text-xs font-mono mr-1">{t}</span>)}
              <div className="prose prose-sm dark:prose-invert max-w-none text-brand-primary dark:text-gray-300 leading-relaxed mt-4">{problem.statement}</div>
              {problem.examples?.length > 0 && (<div className="mt-4 space-y-3"><h3 className="font-semibold text-text-primary dark:text-white text-sm">Examples</h3>{problem.examples.map((ex,i) => (<div key={i} className="bg-surface-base bg-surface-card/50 rounded-lg p-3 border border-brand-primary/10 dark:border-gray-700"><div className="text-xs font-mono text-brand-muted mb-1">Input: {ex.input || "N/A"}</div><div className="text-sm font-mono text-green-700 dark:text-green-400 mb-1">Output: {ex.output || "N/A"}</div>{ex.explanation && <div className="text-xs text-brand-muted mt-2">{ex.explanation}</div>}</div>))}</div>)}
              {challenge.already_completed && (<div className="mt-4 flex items-center gap-2 p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800"><CheckCircle2 size={16} className="text-green-600" /><span className="text-sm text-green-700 dark:text-green-400 font-medium">Already completed today!</span></div>)}
            </AnimatedCard>
          )}
          {activeTab === "code" && (
            <AnimatedCard className="card">
              <div className="flex items-center gap-2 mb-4"><Flame size={16} className="text-primary-600" /><h2 className="text-lg font-bold text-text-primary dark:text-white">Code Editor</h2></div>
              <div className="flex items-center gap-2 mb-3">
                <select value={selectedLanguage} onChange={(e) => setSelectedLanguage(e.target.value)} className="px-3 py-1.5 bg-surface-base bg-surface-card border border-brand-primary/10 dark:border-gray-600 rounded-lg text-sm text-brand-primary dark:text-gray-200">
                  <option value="python">Python</option><option value="javascript">JavaScript</option><option value="java">Java</option><option value="cpp">C++</option><option value="c">C</option>
                </select>
                <button onClick={async () => { if(!userCode.trim()) return; setCodeRunning(true); try { const d = await api.executeCompilerCode({code:userCode,language:selectedLanguage,stdin:"",timeout:10}); setRunResult(d); } catch(e) {} setCodeRunning(false); }} className="flex items-center gap-1.5 px-3 py-1.5 bg-brand-emerald hover:bg-green-700 text-text-primary text-sm font-medium rounded-lg">Run</button>
                <button onClick={handleSubmit} disabled={submitting||!userCode.trim()} className="flex items-center gap-1.5 px-3 py-1.5 bg-primary-600 hover:bg-primary-700 disabled:opacity-50 text-text-primary text-sm font-medium rounded-lg">Submit</button>
              </div>
              <textarea value={userCode} onChange={(e) => setUserCode(e.target.value)} placeholder="// Write your solution here..." className="w-full h-48 p-3 bg-gray-900 text-green-400 font-mono text-sm rounded-lg border border-gray-300 dark:border-gray-600 focus:outline-none focus:border-primary-500 resize-none" spellCheck={false} />
              {runResult && (<div className="mt-3 p-3 bg-surface-base bg-surface-card/50 rounded-lg font-mono text-xs">{runResult.success ? <span className="text-green-600">Success</span> : <span className="text-red-600">{runResult.error || "Failed"}</span>}</div>)}
              {result && (<div className="mt-4 p-4 bg-surface-base bg-surface-card/50 rounded-lg border border-brand-primary/10 dark:border-gray-700"><div className="flex items-center gap-2 mb-3">{result.all_passed ? <CheckCircle2 size={20} className="text-green-500" /> : <XCircle size={20} className="text-yellow-500" />}<span className="font-bold">{result.all_passed ? "All Passed!" : result.passed_count + "/" + result.total_cases}</span></div><div className="grid grid-cols-3 gap-3 text-center"><div><div className="text-lg font-bold text-primary-600">+{result.xp_gained}</div><div className="text-xs text-brand-muted">XP</div></div><div><div className="text-lg font-bold text-green-600">+{result.streak_bonus}</div><div className="text-xs text-brand-muted">Bonus</div></div><div><div className="text-lg font-bold text-brand-primary">{(result.time_taken||0).toFixed(1)}s</div><div className="text-xs text-brand-muted">Time</div></div></div></div>)}
            </AnimatedCard>
          )}
          {activeTab === "leaderboard" && challenge.leaderboard && (
            <AnimatedCard className="card">
              <h2 className="text-lg font-bold text-text-primary dark:text-white mb-4">Leaderboard</h2>
              {challenge.leaderboard.length === 0 ? (
                <p className="text-brand-muted text-sm text-center py-8">No submissions yet.</p>
              ) : (
                <div className="space-y-2">
                  {challenge.leaderboard.map((entry, i) => (
                    <div key={i} className="flex items-center gap-3 p-2 rounded-lg bg-surface-base bg-surface-card/50">
                      <span className={"w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold " + (i===0?"bg-yellow-100 text-yellow-700":i===1?"bg-surface-card/50 text-brand-primary":i===2?"bg-orange-100 text-orange-700":"bg-surface-card/50 text-brand-muted")}>{i + 1}</span>
                      <span className="flex-1 font-medium text-sm text-text-primary dark:text-white">{entry.user_name}</span>
                      <span className="text-xs text-brand-muted font-mono">{(entry.time_taken || 0).toFixed(1)}s</span>
                    </div>
                  ))}
                </div>
              )}
            </AnimatedCard>
          )}
        </div>
        <div className="space-y-6">
          <AnimatedCard className="card"><h3 className="font-bold text-text-primary dark:text-white mb-3">Your Stats</h3><div className="space-y-3"><div className="flex justify-between"><span className="text-sm text-brand-muted">Streak</span><span className="font-bold text-sm text-text-primary dark:text-white">{user?.streak || 0} days</span></div><div className="flex justify-between"><span className="text-sm text-brand-muted">XP</span><span className="font-bold text-sm text-primary-600">{user?.xp || 0}</span></div><div className="flex justify-between"><span className="text-sm text-brand-muted">Level</span><span className="font-bold text-sm text-text-primary dark:text-white">{user?.level || 1}</span></div></div></AnimatedCard>
          {!challenge.already_completed && (<AnimatedCard className="card border-2 border-primary-200 dark:border-primary-800"><div className="text-center"><Trophy size={28} className="mx-auto mb-2 text-primary-500" /><h3 className="font-bold text-text-primary dark:text-white mb-1">Daily Bonus</h3><p className="text-xs text-brand-muted dark:text-gray-400 mb-3">Solve today for +{challenge.streak_bonus} bonus XP</p><button onClick={() => setActiveTab("code")} className="w-full py-2 bg-primary-600 hover:bg-primary-700 text-text-primary text-sm font-medium rounded-lg transition-colors">Start Challenge</button></div></AnimatedCard>)}
        </div>
      </div>
    </div>
  );
}
