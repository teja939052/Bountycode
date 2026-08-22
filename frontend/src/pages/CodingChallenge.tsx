import { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";
import XPPopup from "../components/XPPopup";
import { HyperdriveStatus } from "../components/space";
import { motion, AnimatePresence } from "framer-motion";
import useReducedMotion from "../hooks/useReducedMotion";
import {
  Code, Clock, CheckCircle, XCircle, AlertTriangle,
  Lightbulb, Brain, Building2, ArrowRight, RotateCcw,
} from "lucide-react";

const DIFFICULTIES = [
  { id: "easy", name: "Easy", color: "text-cyber-green bg-cyber-green/10 border border-cyber-green/20" },
  { id: "medium", name: "Medium", color: "text-cyber-yellow bg-cyber-yellow/10 border border-cyber-yellow/20" },
  { id: "hard", name: "Hard", color: "text-cyber-red bg-cyber-red/10 border border-cyber-red/20" },
];

const COMPANY_COLORS = {
  google: "from-blue-500 to-green-500",
  amazon: "from-orange-400 to-yellow-500",
  meta: "from-blue-600 to-indigo-600",
  microsoft: "from-green-500 to-blue-500",
  tcs: "from-blue-700 to-blue-900",
  infosys: "from-blue-500 to-purple-600",
  wipro: "from-blue-600 to-cyan-500",
  uber: "from-black to-gray-700",
};

const COMPANIES = [
  { id: "google", name: "Google", focus: "Algorithms, DP, Graphs" },
  { id: "amazon", name: "Amazon", focus: "Arrays, Trees, Hashing" },
  { id: "meta", name: "Meta", focus: "Graphs, DP, Strings" },
  { id: "microsoft", name: "Microsoft", focus: "Arrays, Trees, Recursion" },
  { id: "tcs", name: "TCS", focus: "Basic Programming" },
  { id: "uber", name: "Uber", focus: "Real-time Systems" },
];

export default function CodingChallenge() {
  const [step, setStep] = useState("select");
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("arrays");
  const [difficulty, setDifficulty] = useState("medium");
  const [language, setLanguage] = useState("python");
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("SDE");
  const [challenge, setChallenge] = useState(null);
  const [challengeId, setChallengeId] = useState("");
  const [code, setCode] = useState("");
  const [timer, setTimer] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [testResults, setTestResults] = useState(null);
  const [score, setScore] = useState(0);
  const [interviewerEval, setInterviewerEval] = useState(null);
  const [hints, setHints] = useState([]);
  const [hintLevel, setHintLevel] = useState(0);
  const [showCelebration, setShowCelebration] = useState(false);
  const [xpData, setXpData] = useState(null);
  const [showXP, setShowXP] = useState(false);
  const [hyperdriveState, setHyperdriveState] = useState("idle");
  const timerRef = useRef(null);
  const reduced = useReducedMotion();

  useEffect(() => {
    const loadTopics = async () => {
      try {
        const data = await api.getCodingTopics();
        setTopics(data.topics);
      } catch (err) {
        setError(err.message);
      }
    };
    loadTopics();
  }, []);

  useEffect(() => {
    if (step === "coding") {
      timerRef.current = setInterval(() => setTimer((p) => p + 1), 1000);
    }
    return () => clearInterval(timerRef.current);
  }, [step]);

  const startChallenge = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await api.startCodingChallengeV2(difficulty, selectedTopic, language, company, role);
      setChallenge(data.challenge || data);
      setChallengeId(data.challenge_id);
      setTimer(0);
      setHints([]);
      setHintLevel(0);
      setHyperdriveState("idle");
      setStep("coding");
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const submitCode = async () => {
    setLoading(true);
    setError("");
    setHyperdriveState("compiling");
    setTimeout(() => setHyperdriveState("running"), 1000);
    try {
      const result = await api.submitCodingAnswer(challengeId, code, timer);
      setTestResults(result.test_results);
      setScore(result.score || 0);
      setInterviewerEval(result.interviewer_eval);
      setHyperdriveState(result.score >= 80 ? "success" : result.score > 0 ? "partial" : "failed");

      if (result.xp_gained) {
        setXpData({ xpGained: result.xp_gained, level: result.level, streak: result.streak, newBadges: result.new_badges || [] });
        setShowXP(true);
      }
      if (result.score >= 80) {
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 3000);
      }
      const solution = await api.getCodingSolution(challengeId);
      setChallenge({ ...challenge, ...solution });
      setStep("review");
    } catch (err) {
      setError(err.message);
      setHyperdriveState("error");
    }
    setLoading(false);
  };

  const requestHint = async () => {
    const nextLevel = hintLevel + 1;
    if (nextLevel > 3) return;
    try {
      const data = await api.getCodingHint(challengeId, nextLevel);
      setHints((prev) => [...prev, { level: nextLevel, text: data.hint }]);
      setHintLevel(nextLevel);
    } catch (err) {
      console.error(err);
    }
  };

  const requestInterviewerReview = async () => {
    setLoading(true);
    try {
      const evalResult = await api.getInterviewerReview(challengeId, code, language);
      setInterviewerEval(evalResult);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const formatTime = (s) => `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, "0")}`;

  // SELECT SCREEN
  if (step === "select") {
    return (
      <div className="min-h-screen py-12 px-4">
        <CelebrationOverlay show={showCelebration} type="perfect" title="Hyperdrive Engaged!" onClose={() => setShowCelebration(false)} />
        <XPPopup show={showXP} {...xpData} onClose={() => setShowXP(false)} />
        <div className="max-w-4xl mx-auto">
          <motion.div
            className="text-center mb-10"
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <span className="section-subheader mb-3 block">Hyperdrive Training</span>
            <h1 className="section-header text-3xl mb-2">
              <Code className="text-cyber-green inline mr-2" size={28} />
              Coding <span className="text-cyber-green">Challenges</span>
            </h1>
            <p className="text-brand-dim font-mono text-sm">
              Company-specific problems with live AI feedback
            </p>
          </motion.div>

          {error && (
            <div className="bg-cyber-red/10 border border-cyber-red/20 text-cyber-red px-4 py-3 rounded-lg mb-6 text-center font-mono text-sm">{error}</div>
          )}

          {/* Company Selection */}
          <div className="card mb-6">
            <h3 className="font-display font-bold text-text-primary text-sm mb-4 flex items-center gap-2">
              <Building2 size={16} className="text-cyber-blue" /> Company Style
            </h3>
            <div className="grid sm:grid-cols-3 gap-3">
              <button
                onClick={() => setCompany("")}
                className={`p-3 rounded-lg text-left transition-all border-2 ${
                  !company ? "border-brand-primary/30 bg-brand-primary/10" : "border-brand-primary/20 hover:border-brand-primary/40"
                }`}
              >
                <p className="font-display font-bold text-text-primary text-sm">General</p>
                <p className="text-xs font-mono text-brand-dim">No company focus</p>
              </button>
              {COMPANIES.map((c) => (
                <button
                  key={c.id}
                  onClick={() => setCompany(c.id)}
                  className={`p-3 rounded-lg text-left transition-all border-2 ${
                    company === c.id ? "border-brand-primary bg-brand-primary/10" : "border-brand-primary/20 hover:border-brand-primary/40"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <div className={`w-6 h-6 rounded bg-gradient-to-br ${COMPANY_COLORS[c.id]} flex items-center justify-center text-white text-xs font-bold`}>{c.name[0]}</div>
                    <p className="font-display font-bold text-text-primary text-sm">{c.name}</p>
                  </div>
                  <p className="text-xs font-mono text-brand-dim mt-1">{c.focus}</p>
                </button>
              ))}
            </div>
          </div>

          <div className="card mb-6">
            <h3 className="font-display font-bold text-text-primary text-sm mb-4">Select Topic</h3>
            <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-3">
              {topics.map((topic) => (
                <button
                  key={topic.id}
                  onClick={() => setSelectedTopic(topic.id)}
                  className={`p-3 rounded-lg text-left transition-all border-2 ${
                    selectedTopic === topic.id ? "border-brand-primary bg-brand-primary/10" : "border-brand-primary/20 hover:border-brand-primary/40"
                  }`}
                >
                  <p className="font-mono text-xs text-text-primary">{topic.name}</p>
                </button>
              ))}
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-6 mb-6">
            <div className="card">
              <h3 className="font-display font-bold text-text-primary text-sm mb-4">Difficulty</h3>
              <div className="flex gap-3">
                {DIFFICULTIES.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => setDifficulty(d.id)}
                    className={`px-4 py-2 rounded-lg font-mono text-xs transition-colors ${difficulty === d.id ? d.color : "bg-surface-card border border-brand-primary/20 text-brand-dim"}`}
                  >
                    {d.name}
                  </button>
                ))}
              </div>
            </div>

            <div className="card">
              <h3 className="font-display font-bold text-text-primary text-sm mb-4">Language</h3>
              <div className="flex gap-3">
                {["python", "javascript", "java", "cpp"].map((lang) => (
                  <button
                    key={lang}
                    onClick={() => setLanguage(lang)}
                    className={`px-4 py-2 rounded-lg font-mono text-xs capitalize transition-colors ${
                      language === lang ? "bg-brand-emerald text-white" : "bg-surface-card border border-brand-primary/20 text-brand-dim"
                    }`}
                  >
                    {lang}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button onClick={startChallenge} disabled={loading} className="w-full btn-primary flex items-center justify-center gap-2">
            {loading ? <Spinner size="sm" className="text-space-void" /> : null}
            Engage Hyperdrive
            {!loading && <ArrowRight size={16} />}
          </button>
        </div>
      </div>
    );
  }

  // CODING SCREEN
  if (step === "coding" && challenge) {
    return (
      <div className="min-h-screen py-12 px-4">
        <CelebrationOverlay show={showCelebration} type="perfect" title="All Tests Passed!" onClose={() => setShowCelebration(false)} />
        <XPPopup show={showXP} {...xpData} onClose={() => setShowXP(false)} />
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <h2 className="font-display font-bold text-text-primary text-lg">{challenge.title}</h2>
              {company && (
                <span className={`px-3 py-1 rounded-full text-[10px] font-mono bg-gradient-to-r ${COMPANY_COLORS[company]} text-white`}>{company}</span>
              )}
            </div>
            <div className="flex items-center gap-4">
              <HyperdriveStatus status={hyperdriveState} testResults={{ time: formatTime(timer) }} />
              <span className={`px-3 py-1 rounded-full text-[10px] font-mono ${DIFFICULTIES.find(d => d.id === difficulty)?.color || ""}`}>{difficulty}</span>
            </div>
          </div>

          <div className="grid lg:grid-cols-2 gap-6">
            {/* Problem Description */}
            <div className="card">
              <h3 className="font-display font-bold text-text-primary text-sm mb-3">Mission Brief</h3>
              <p className="text-brand-secondary font-mono text-xs whitespace-pre-wrap mb-4">{challenge.description}</p>

              {challenge.examples?.length > 0 && (
                <div className="mb-4">
                  <p className="font-display font-bold text-brand-primary text-xs mb-2">Test Cases:</p>
                  {challenge.examples.map((ex, i) => (
                    <div key={i} className="bg-surface-card border border-brand-primary/10 rounded-lg p-3 mb-2 font-mono text-xs">
                      <p><span className="text-brand-sky">Input:</span> <span className="text-brand-secondary">{typeof ex === 'object' ? ex.input : ex}</span></p>
                      {ex.output && <p><span className="text-brand-emerald">Output:</span> <span className="text-brand-secondary">{ex.output}</span></p>}
                      {ex.explanation && <p className="text-brand-dim"><span className="text-brand-gold">Why:</span> {ex.explanation}</p>}
                    </div>
                  ))}
                </div>
              )}

              {challenge.constraints?.length > 0 && (
                <div className="mb-4">
                  <p className="font-display font-bold text-brand-primary text-xs mb-2">Constraints:</p>
                  <ul className="text-xs font-mono text-brand-dim">
                    {challenge.constraints.map((c, i) => <li key={i}>• {c}</li>)}
                  </ul>
                </div>
              )}

              {/* Progressive Hints */}
              <div className="border-t border-brand-primary/10 pt-4 mt-4">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-display font-bold text-brand-primary text-sm flex items-center gap-2">
                    <Lightbulb size={14} className="text-brand-gold" /> Navigation Beacons
                    {hintLevel > 0 && <span className="text-[10px] font-mono text-brand-dim">({hintLevel}/3)</span>}
                  </h3>
                  {hintLevel < 3 && (
                    <button onClick={requestHint} className="text-xs font-mono text-brand-gold hover:underline flex items-center gap-1">
                      <Lightbulb size={12} /> Beacon {hintLevel + 1}
                    </button>
                  )}
                </div>
                <AnimatePresence>
                  {hints.map((h, i) => (
                    <motion.div
                      key={i}
                      initial={reduced ? {} : { opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: "auto" }}
                      className="bg-brand-gold/5 border border-brand-gold/20 rounded-lg p-3 mb-2 text-xs font-mono"
                    >
                      <span className="text-brand-gold font-bold">Level {h.level}: </span>
                      <span className="text-brand-secondary">{h.text}</span>
                    </motion.div>
                  ))}
                </AnimatePresence>
                {hintLevel === 0 && (
                  <p className="text-xs font-mono text-brand-dim italic">Stuck? Request navigation beacons for progressive hints.</p>
                )}
              </div>
            </div>

            {/* Code Editor */}
            <div className="card">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-display font-bold text-brand-primary text-sm">Solution Module</h3>
                <span className="text-[10px] font-mono text-brand-dim uppercase">{language}</span>
              </div>
              <textarea
                className="w-full h-96 font-mono text-xs p-4 border border-brand-primary/10 rounded-lg resize-none focus:ring-2 focus:ring-brand-emerald/50 focus:border-brand-emerald/50 bg-surface-card text-brand-secondary"
                placeholder={`// ${language} solution...`}
                value={code}
                onChange={(e) => setCode(e.target.value)}
              />
              <div className="flex gap-4 mt-4">
                <button
                  onClick={submitCode}
                  disabled={!code.trim() || loading}
                  className="flex-1 btn-primary flex items-center justify-center gap-2"
                >
                  {loading ? <Spinner size="sm" className="text-space-void" /> : null}
                  Transmit Solution
                </button>
                <Link to="/coding" className="btn-ghost">New Challenge</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // REVIEW SCREEN
  if (step === "review" && challenge) {
    return (
      <div className="min-h-screen py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="card mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="font-display font-bold text-text-primary text-lg">{challenge.title}</h2>
                {company && <span className="text-xs font-mono text-gray-500">{company} style</span>}
              </div>
              <div className="text-center">
                <p className={`text-3xl font-display font-black ${score >= 80 ? "text-cyber-green" : score > 0 ? "text-cyber-yellow" : "text-gray-500"}`}>{score}%</p>
                <p className="text-[10px] font-mono text-gray-500">Time: {formatTime(timer)}</p>
              </div>
            </div>
            {testResults && (
              <div className="mt-4 flex items-center gap-4">
                <p className="text-xs font-mono text-gray-400">{testResults.summary}</p>
                {score >= 80 && <span className="text-cyber-green text-xs font-mono">✅ Hyperdrive Engaged!</span>}
              </div>
            )}
          </div>

          {testResults?.results?.length > 0 && (
            <div className="card mb-6">
              <h3 className="font-display font-bold text-text-primary text-sm mb-3">Test Case Diagnostics</h3>
              <div className="space-y-2">
                {testResults.results.map((tc) => (
                  <div key={tc.test_case_index} className={`rounded-lg p-3 text-xs font-mono ${tc.passed ? "bg-cyber-green/5 border border-cyber-green/20" : "bg-cyber-red/5 border border-cyber-red/20"}`}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="font-display font-bold text-text-primary">TC-{tc.test_case_index}</span>
                      {tc.passed ? <CheckCircle size={14} className="text-cyber-green" /> : <XCircle size={14} className="text-cyber-red" />}
                    </div>
                    {!tc.is_hidden && (
                      <div className="text-gray-400 space-y-0.5">
                        <p><span className="text-cyber-blue">In:</span> {tc.input}</p>
                        <p><span className="text-cyber-green">Expected:</span> {tc.expected}</p>
                        {!tc.passed && <p className="text-cyber-red"><span className="text-cyber-red">Got:</span> {tc.actual}</p>}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {interviewerEval && (
            <div className="card mb-6">
              <h3 className="font-display font-bold text-text-primary text-sm mb-3 flex items-center gap-2">
                <Brain size={16} className="text-cyber-purple" /> AI Interviewer Assessment
              </h3>
              <div className="flex items-center gap-4 mb-4">
                <div className={`px-3 py-1 rounded-full text-xs font-mono font-bold ${interviewerEval.would_pass ? "bg-cyber-green/20 text-cyber-green" : "bg-cyber-red/20 text-cyber-red"}`}>
                  {interviewerEval.would_pass ? "PASS" : "NEEDS WORK"}
                </div>
                <span className="text-sm font-display font-bold text-text-primary">Score: {interviewerEval.score}/10</span>
              </div>
              <div className="grid sm:grid-cols-2 gap-3 mb-4">
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                  <p className="text-[10px] font-mono text-gray-500 mb-1">Time Complexity</p>
                  <p className="font-mono text-xs text-text-primary">{interviewerEval.time_complexity}</p>
                </div>
                <div className="bg-gray-50 border border-gray-200 rounded-lg p-3">
                  <p className="text-[10px] font-mono text-gray-500 mb-1">Space Complexity</p>
                  <p className="font-mono text-xs text-text-primary">{interviewerEval.space_complexity}</p>
                </div>
              </div>
              <p className="text-gray-400 font-mono text-xs mb-3">{interviewerEval.feedback}</p>
              {interviewerEval.strengths?.length > 0 && (
                <div className="mb-2">
                  <p className="text-xs font-mono text-cyber-green mb-1">Strengths:</p>
                  {interviewerEval.strengths.map((s, i) => <p key={i} className="text-xs font-mono text-gray-400">✅ {s}</p>)}
                </div>
              )}
              {interviewerEval.improvements?.length > 0 && (
                <div>
                  <p className="text-xs font-mono text-cyber-orange mb-1">Improve:</p>
                  {interviewerEval.improvements.map((s, i) => <p key={i} className="text-xs font-mono text-gray-400">💡 {s}</p>)}
                </div>
              )}
            </div>
          )}

          {!interviewerEval && (
            <div className="card mb-6">
              <button onClick={requestInterviewerReview} disabled={loading} className="w-full flex items-center justify-center gap-2 p-4 text-cyber-purple hover:bg-cyber-purple/10 rounded-lg transition-colors font-mono text-xs">
                <Brain size={16} />
                {loading ? "Analyzing..." : "Request AI Interviewer Assessment"}
              </button>
            </div>
          )}

          {challenge.solution_approach && (
            <div className="card mb-6 border-cyber-blue/20 bg-cyber-blue/5">
              <h3 className="font-display font-bold text-text-primary text-sm mb-2 flex items-center gap-2">
                <Lightbulb size={14} className="text-cyber-blue" /> Optimal Solution
              </h3>
              <p className="text-xs font-mono text-gray-400">{challenge.solution_approach}</p>
            </div>
          )}

          {challenge.follow_up && (
            <div className="card mb-6 border-cyber-yellow/20 bg-cyber-yellow/5">
              <h3 className="font-display font-bold text-text-primary text-sm mb-2 flex items-center gap-2">
                <AlertTriangle size={14} className="text-cyber-yellow" /> Follow-up Mission
              </h3>
              <p className="text-xs font-mono text-gray-400">{challenge.follow_up}</p>
            </div>
          )}

          <div className="flex gap-4">
            <Link to="/coding" className="flex-1 btn-primary text-center flex items-center justify-center gap-2">
              <RotateCcw size={16} /> New Challenge
            </Link>
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
