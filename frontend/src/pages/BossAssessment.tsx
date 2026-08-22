import { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Swords, Shield, Zap, Clock, CheckCircle2, XCircle, Lock,
  ArrowLeft, Trophy, Target, Flame, Loader2, SkipForward,
} from "lucide-react";
import { rpgApi } from "../services/api/rpg";
import { useJuice } from "../juice/JuiceProvider";
import Skeleton from "../components/ui/Skeleton";

const CHALLENGE_ICONS: Record<string, any> = {
  solve: Target,
  debug: Shield,
  predict: Zap,
  timed: Clock,
  interview: Swords,
};

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "#22C55E",
  medium: "#F59E0B",
  hard: "#EF4444",
  expert: "#A855F7",
};

export default function BossAssessment() {
  const { bossId } = useParams<{ bossId: string }>();
  const navigate = useNavigate();
  const { showXP, play } = useJuice();

  const [boss, setBoss] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [phase, setPhase] = useState<"intro" | "fight" | "result">("intro");
  const [currentChallenge, setCurrentChallenge] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [challengeResults, setChallengeResults] = useState<Record<number, { score: number; passed: boolean }>>({});
  const [submitting, setSubmitting] = useState(false);
  const [finalResult, setFinalResult] = useState<any>(null);

  const loadBoss = useCallback(async () => {
    if (!bossId) return;
    setLoading(true);
    try {
      const d = await rpgApi.bossDetail(bossId);
      setBoss(d);
    } catch (e: any) {
      setError(e.message || "Boss not found");
    } finally {
      setLoading(false);
    }
  }, [bossId]);

  useEffect(() => { loadBoss(); }, [loadBoss]);

  const handleAnswer = (challengeIdx: number, value: string) => {
    setAnswers((prev) => ({ ...prev, [challengeIdx]: value }));
  };

  const simulateChallenge = (challengeIdx: number) => {
    const answer = answers[challengeIdx] || "";
    const hasInput = answer.trim().length > 0;
    const score = hasInput ? Math.floor(Math.random() * 40) + 60 : Math.floor(Math.random() * 30) + 10;
    setChallengeResults((prev) => ({ ...prev, [challengeIdx]: { score, passed: score >= 60 } }));
  };

  const nextChallenge = () => {
    if (!boss) return;
    if (currentChallenge < boss.challenges.length - 1) {
      setCurrentChallenge((c) => c + 1);
    } else {
      finishFight();
    }
  };

  const skipChallenge = () => {
    if (!boss) return;
    setChallengeResults((prev) => ({ ...prev, [currentChallenge]: { score: 0, passed: false } }));
    nextChallenge();
  };

  const finishFight = async () => {
    if (!boss) return;
    setSubmitting(true);
    const totalScore = Object.values(challengeResults).reduce((sum, r) => sum + r.score, 0);
    const count = Object.keys(challengeResults).length || 1;
    const avgScore = Math.round(totalScore / count);
    try {
      const res = await rpgApi.challengeBoss(boss.id, avgScore);
      setFinalResult({ ...res, avgScore });
      setPhase("result");
      if (res.defeated) {
        play("levelUp");
        showXP(res.xp_earned, window.innerWidth / 2, window.innerHeight / 2);
      }
    } catch {
      setFinalResult({ defeated: false, avgScore, xp_earned: 0, pass_score: boss.pass_score });
      setPhase("result");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black px-4 py-8 max-w-3xl mx-auto">
        <Skeleton className="h-10 w-64 mb-3 bg-white/5" />
        <Skeleton className="h-40 w-full rounded-2xl bg-white/5" />
      </div>
    );
  }

  if (!boss) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="rounded-2xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400">
          {error || "Boss not found."}
        </div>
      </div>
    );
  }

  if (!boss.unlocked) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <div className="text-6xl mb-4">{boss.icon}</div>
          <h2 className="text-2xl font-display font-black text-white mb-2">{boss.name}</h2>
          <p className="text-gray-400 text-sm mb-4">Reach Level {boss.unlock_level} to unlock this boss.</p>
          <button onClick={() => navigate("/journey")} className="px-4 py-2 rounded-xl bg-white/10 text-white text-sm border border-white/10 hover:bg-white/15 transition-all">
            Back to Career RPG
          </button>
        </div>
      </div>
    );
  }

  if (phase === "intro") {
    return (
      <div className="min-h-screen bg-black px-4 py-8 max-w-3xl mx-auto">
        <button onClick={() => navigate("/journey")} className="flex items-center gap-2 text-gray-400 hover:text-white text-sm mb-6 transition-all">
          <ArrowLeft className="w-4 h-4" /> Back to Career RPG
        </button>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="rounded-3xl border border-red-500/20 bg-gradient-to-br from-red-500/10 to-transparent p-6 sm:p-8 text-center">
          <div className="text-6xl mb-4">{boss.icon}</div>
          <h1 className="text-3xl font-display font-black text-white mb-2">{boss.name}</h1>
          <p className="text-gray-400 text-sm mb-6">{boss.challenges?.length || 0} challenges await. Score {boss.pass_score}%+ to defeat.</p>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-8">
            {(boss.challenges || []).map((ch: any, i: number) => {
              const Icon = CHALLENGE_ICONS[ch.type] || Target;
              return (
                <div key={i} className="rounded-xl border border-white/10 bg-white/5 p-3 text-center">
                  <Icon className="w-5 h-5 mx-auto mb-1" style={{ color: DIFFICULTY_COLORS[ch.difficulty] || "#999" }} />
                  <p className="text-[10px] text-white font-medium truncate">{ch.title}</p>
                  <p className="text-[9px] font-mono mt-1" style={{ color: DIFFICULTY_COLORS[ch.difficulty] }}>{ch.difficulty}</p>
                  <p className="text-[9px] font-mono text-gray-500">{ch.xp} XP</p>
                </div>
              );
            })}
          </div>

          <button onClick={() => setPhase("fight")}
            className="px-8 py-3 rounded-xl bg-gradient-to-r from-red-600 to-orange-500 text-white font-bold text-sm hover:brightness-110 transition-all">
            <Swords className="w-4 h-4 inline mr-2" /> Enter Battle
          </button>
        </motion.div>
      </div>
    );
  }

  if (phase === "fight") {
    const ch = boss.challenges[currentChallenge];
    const result = challengeResults[currentChallenge];
    const Icon = CHALLENGE_ICONS[ch.type] || Target;

    return (
      <div className="min-h-screen bg-black px-4 py-8 max-w-3xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <button onClick={() => navigate("/journey")} className="flex items-center gap-2 text-gray-400 hover:text-white text-sm transition-all">
            <ArrowLeft className="w-4 h-4" /> Flee
          </button>
          <div className="flex items-center gap-3 text-xs font-mono text-gray-500">
            <span>{currentChallenge + 1}/{boss.challenges.length}</span>
            <span>{boss.icon}</span>
          </div>
        </div>

        {/* Progress */}
        <div className="flex gap-1 mb-6">
          {boss.challenges.map((_: any, i: number) => {
            const r = challengeResults[i];
            return (
              <div key={i} className={`h-1.5 flex-1 rounded-full transition-all ${
                r ? (r.passed ? "bg-green-500" : "bg-red-500") : (i === currentChallenge ? "bg-white" : "bg-white/10")
              }`} />
            );
          })}
        </div>

        <AnimatePresence mode="wait">
          <motion.div key={currentChallenge} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}
            className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${DIFFICULTY_COLORS[ch.difficulty]}22`, border: `1px solid ${DIFFICULTY_COLORS[ch.difficulty]}44` }}>
                <Icon className="w-5 h-5" style={{ color: DIFFICULTY_COLORS[ch.difficulty] }} />
              </div>
              <div>
                <h3 className="text-sm font-bold text-white">{ch.title}</h3>
                <p className="text-[10px] font-mono" style={{ color: DIFFICULTY_COLORS[ch.difficulty] }}>{ch.difficulty} · {ch.xp} XP</p>
              </div>
            </div>

            <p className="text-xs text-gray-400 mb-4">Write your solution or approach below. Press Submit when ready.</p>

            <textarea
              value={answers[currentChallenge] || ""}
              onChange={(e) => handleAnswer(currentChallenge, e.target.value)}
              placeholder="Type your answer here..."
              className="w-full h-40 bg-black/40 border border-white/10 rounded-xl p-4 text-sm text-white placeholder-gray-600 font-mono resize-none focus:outline-none focus:border-white/25 transition-all"
              disabled={!!result}
            />

            {result && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className={`mt-4 p-3 rounded-xl border text-sm font-mono ${result.passed ? "border-green-500/30 bg-green-500/10 text-green-400" : "border-red-500/30 bg-red-500/10 text-red-400"}`}>
                Score: {result.score}% {result.passed ? "· Passed" : "· Failed"}
              </motion.div>
            )}

            <div className="flex items-center gap-3 mt-4">
              {!result ? (
                <>
                  <button onClick={() => simulateChallenge(currentChallenge)}
                    className="flex-1 px-4 py-2.5 rounded-xl bg-white/10 text-white text-sm font-medium border border-white/10 hover:bg-white/15 transition-all">
                    Submit
                  </button>
                  <button onClick={skipChallenge}
                    className="px-4 py-2.5 rounded-xl bg-white/5 text-gray-400 text-sm border border-white/5 hover:text-white transition-all">
                    <SkipForward className="w-4 h-4" />
                  </button>
                </>
              ) : (
                <button onClick={nextChallenge}
                  className="flex-1 px-4 py-2.5 rounded-xl bg-white/10 text-white text-sm font-medium border border-white/10 hover:bg-white/15 transition-all">
                  {currentChallenge < boss.challenges.length - 1 ? "Next Challenge" : "View Results"}
                </button>
              )}
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    );
  }

  if (phase === "result") {
    const won = finalResult?.defeated;
    return (
      <div className="min-h-screen bg-black px-4 py-8 max-w-3xl mx-auto flex items-center justify-center">
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
          className={`rounded-3xl border p-8 text-center max-w-md w-full ${won ? "border-green-500/30 bg-green-500/10" : "border-red-500/30 bg-red-500/10"}`}>
          <div className="text-6xl mb-4">{won ? "🏆" : boss.icon}</div>
          <h2 className="text-2xl font-display font-black text-white mb-2">
            {won ? "Boss Defeated!" : "Defeated..."}
          </h2>
          <p className="text-gray-400 text-sm mb-4">{boss.name}</p>

          <div className="grid grid-cols-2 gap-3 mb-6">
            <div className="rounded-xl border border-white/10 bg-white/5 p-3">
              <p className="text-xl font-bold text-white">{finalResult?.avgScore || 0}%</p>
              <p className="text-[10px] font-mono text-gray-500">Your Score</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-white/5 p-3">
              <p className="text-xl font-bold text-white">{boss.pass_score}%</p>
              <p className="text-[10px] font-mono text-gray-500">Required</p>
            </div>
          </div>

          {won && finalResult?.xp_earned > 0 && (
            <div className="mb-4 p-3 rounded-xl border border-green-500/30 bg-green-500/10">
              <p className="text-sm font-mono text-green-400">+{finalResult.xp_earned} XP earned</p>
              {finalResult.badge_earned && (
                <p className="text-xs font-mono text-amber-400 mt-1">Badge: {finalResult.badge_earned}</p>
              )}
            </div>
          )}

          <div className="flex gap-3">
            <button onClick={() => navigate("/journey")}
              className="flex-1 px-4 py-2.5 rounded-xl bg-white/10 text-white text-sm border border-white/10 hover:bg-white/15 transition-all">
              Back to RPG
            </button>
            {!won && (
              <button onClick={() => { setPhase("intro"); setCurrentChallenge(0); setAnswers({}); setChallengeResults({}); setFinalResult(null); }}
                className="flex-1 px-4 py-2.5 rounded-xl bg-white/5 text-gray-400 text-sm border border-white/5 hover:text-white transition-all">
                Try Again
              </button>
            )}
          </div>
        </motion.div>
      </div>
    );
  }

  return null;
}
