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

/** SVG boss emblem — replaces emoji icons from remote data. */
function BossEmblem({ size = 72 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" aria-hidden="true" className="mx-auto">
      <path
        d="M32 6l20 8v14c0 12-8 22-20 30C20 50 12 40 12 28V14l20-8z"
        fill="#FDEDEC"
        stroke="#E96A5B"
        strokeWidth="3"
        strokeLinejoin="round"
      />
      <path d="M24 26l16 12M40 26L24 38M32 22v20" stroke="#E96A5B" strokeWidth="3" strokeLinecap="round" />
    </svg>
  );
}

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
      <div className="min-h-screen page-surface px-4 py-8 max-w-3xl mx-auto">
        <Skeleton className="h-10 w-64 mb-3 bg-border" />
        <Skeleton className="h-40 w-full rounded-2xl bg-border" />
      </div>
    );
  }

  if (!boss) {
    return (
      <div className="min-h-screen page-surface flex items-center justify-center">
        <div className="rounded-2xl border border-red/20 bg-red-soft px-4 py-3 text-sm text-red">
          {error || "Boss not found."}
        </div>
      </div>
    );
  }

  if (!boss.unlocked) {
    return (
      <div className="min-h-screen page-surface flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <div className="mb-4"><BossEmblem /></div>
          <h2 className="text-2xl font-display font-black text-text-primary mb-2">{boss.name}</h2>
          <p className="text-text-muted text-sm mb-4">Reach Level {boss.unlock_level} to unlock this boss.</p>
          <button onClick={() => navigate("/journey")} className="px-4 py-2 rounded-xl bg-surface-2 text-text-primary text-sm border border-border hover:bg-primary-soft transition-all">
            Back to Career RPG
          </button>
        </div>
      </div>
    );
  }

  if (phase === "intro") {
    return (
      <div className="min-h-screen page-surface px-4 py-8 max-w-3xl mx-auto">
        <button onClick={() => navigate("/journey")} className="flex items-center gap-2 text-text-muted hover:text-primary text-sm mb-6 transition-all">
          <ArrowLeft className="w-4 h-4" /> Back to Career RPG
        </button>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
          className="rounded-3xl border border-red/20 bg-red-soft p-6 sm:p-8 text-center">
          <div className="mb-4"><BossEmblem /></div>
          <h1 className="text-3xl font-display font-black text-text-primary mb-2">{boss.name}</h1>
          <p className="text-text-muted text-sm mb-6">{boss.challenges?.length || 0} challenges await. Score {boss.pass_score}%+ to defeat.</p>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-8">
            {(boss.challenges || []).map((ch: any, i: number) => {
              const Icon = CHALLENGE_ICONS[ch.type] || Target;
              return (
                <div key={i} className="rounded-xl border border-border bg-white p-3 text-center shadow-card">
                  <Icon className="w-5 h-5 mx-auto mb-1" style={{ color: DIFFICULTY_COLORS[ch.difficulty] || "#999" }} />
                  <p className="text-[10px] text-text-primary font-medium truncate">{ch.title}</p>
                  <p className="text-[9px] font-mono mt-1" style={{ color: DIFFICULTY_COLORS[ch.difficulty] }}>{ch.difficulty}</p>
                  <p className="text-[9px] font-mono text-text-muted">{ch.xp} XP</p>
                </div>
              );
            })}
          </div>

          <button onClick={() => setPhase("fight")}
            className="px-8 py-3 rounded-xl bg-coral text-white font-bold text-sm hover:brightness-105 transition-all">
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
      <div className="min-h-screen page-surface px-4 py-8 max-w-3xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <button onClick={() => navigate("/journey")} className="flex items-center gap-2 text-text-muted hover:text-primary text-sm transition-all">
            <ArrowLeft className="w-4 h-4" /> Flee
          </button>
          <div className="flex items-center gap-3 text-xs font-mono text-text-muted">
            <span>{currentChallenge + 1}/{boss.challenges.length}</span>
            <Swords className="w-4 h-4 text-coral" />
          </div>
        </div>

        {/* Progress */}
        <div className="flex gap-1 mb-6">
          {boss.challenges.map((_: any, i: number) => {
            const r = challengeResults[i];
            return (
              <div key={i} className={`h-1.5 flex-1 rounded-full transition-all ${
                r ? (r.passed ? "bg-primary" : "bg-red") : (i === currentChallenge ? "bg-text-primary" : "bg-border")
              }`} />
            );
          })}
        </div>

        <AnimatePresence mode="wait">
          <motion.div key={currentChallenge} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}
            className="rounded-2xl border border-border bg-white p-6 shadow-card">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${DIFFICULTY_COLORS[ch.difficulty]}22`, border: `1px solid ${DIFFICULTY_COLORS[ch.difficulty]}44` }}>
                <Icon className="w-5 h-5" style={{ color: DIFFICULTY_COLORS[ch.difficulty] }} />
              </div>
              <div>
                <h3 className="text-sm font-bold text-text-primary">{ch.title}</h3>
                <p className="text-[10px] font-mono" style={{ color: DIFFICULTY_COLORS[ch.difficulty] }}>{ch.difficulty} · {ch.xp} XP</p>
              </div>
            </div>

            <p className="text-xs text-text-muted mb-4">Write your solution or approach below. Press Submit when ready.</p>

            <textarea
              value={answers[currentChallenge] || ""}
              onChange={(e) => handleAnswer(currentChallenge, e.target.value)}
              placeholder="Type your answer here..."
              className="w-full h-40 bg-surface-2 border border-border rounded-xl p-4 text-sm text-text-primary placeholder-text-muted font-mono resize-none focus:outline-none focus:border-primary transition-all"
              disabled={!!result}
            />

            {result && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className={`mt-4 p-3 rounded-xl border text-sm font-mono ${result.passed ? "border-primary/30 bg-primary-soft text-primary-dark" : "border-red/30 bg-red-soft text-red"}`}>
                Score: {result.score}% {result.passed ? "· Passed" : "· Failed"}
              </motion.div>
            )}

            <div className="flex items-center gap-3 mt-4">
              {!result ? (
                <>
                  <button onClick={() => simulateChallenge(currentChallenge)}
                    className="flex-1 px-4 py-2.5 rounded-xl bg-primary text-text-primary text-sm font-medium hover:bg-primary-dark transition-all">
                    Submit
                  </button>
                  <button onClick={skipChallenge}
                    className="px-4 py-2.5 rounded-xl bg-surface-2 text-text-muted text-sm border border-border hover:text-primary transition-all">
                    <SkipForward className="w-4 h-4" />
                  </button>
                </>
              ) : (
                <button onClick={nextChallenge}
                  className="flex-1 px-4 py-2.5 rounded-xl bg-primary text-text-primary text-sm font-medium hover:bg-primary-dark transition-all">
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
      <div className="min-h-screen page-surface px-4 py-8 max-w-3xl mx-auto flex items-center justify-center">
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
          className={`rounded-3xl border p-8 text-center max-w-md w-full ${won ? "border-primary/30 bg-primary-soft" : "border-red/20 bg-red-soft"}`}>
          <div className="mb-4 flex justify-center">
            {won ? (
              <div className="treasure-seal h-20 w-20">
                <Trophy size={36} />
              </div>
            ) : (
              <BossEmblem size={80} />
            )}
          </div>
          <h2 className="text-2xl font-display font-black text-text-primary mb-2">
            {won ? "Boss Defeated!" : "Defeated..."}
          </h2>
          <p className="text-text-muted text-sm mb-4">{boss.name}</p>

          <div className="grid grid-cols-2 gap-3 mb-6">
            <div className="rounded-xl border border-border bg-white p-3 shadow-card">
              <p className="text-xl font-bold text-text-primary">{finalResult?.avgScore || 0}%</p>
              <p className="text-[10px] font-mono text-text-muted">Your Score</p>
            </div>
            <div className="rounded-xl border border-border bg-white p-3 shadow-card">
              <p className="text-xl font-bold text-text-primary">{boss.pass_score}%</p>
              <p className="text-[10px] font-mono text-text-muted">Required</p>
            </div>
          </div>

          {won && finalResult?.xp_earned > 0 && (
            <div className="mb-4 p-3 rounded-xl border border-primary/30 bg-primary-soft">
              <p className="text-sm font-mono text-primary-dark">+{finalResult.xp_earned} XP earned</p>
              {finalResult.badge_earned && (
                <p className="text-xs font-mono text-gold mt-1">Badge: {finalResult.badge_earned}</p>
              )}
            </div>
          )}

          <div className="flex gap-3">
            <button onClick={() => navigate("/journey")}
              className="flex-1 px-4 py-2.5 rounded-xl bg-surface-2 text-text-primary text-sm border border-border hover:bg-primary-soft transition-all">
              Back to RPG
            </button>
            {!won && (
              <button onClick={() => { setPhase("intro"); setCurrentChallenge(0); setAnswers({}); setChallengeResults({}); setFinalResult(null); }}
                className="flex-1 px-4 py-2.5 rounded-xl bg-surface-2 text-text-muted text-sm border border-border hover:text-primary transition-all">
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
