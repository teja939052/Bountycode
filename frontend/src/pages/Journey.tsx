import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  XCircle,
  Lock,
  Sparkles,
  Lightbulb,
  Clock,
  Zap,
  Target,
  Trophy,
  Crown,
  Map,
  Compass,
  ChevronRight,
  Play,
  Star,
  Heart,
  Flame,
  Sword,
  Shield,
  Brain,
  Rocket,
  AlertTriangle,
  Code2,
  Award,
  TrendingUp,
  Activity,
  GraduationCap,
  Eye,
  EyeOff,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import CelebrationOverlay from "../components/CelebrationOverlay";
import useReducedMotion from "../hooks/useReducedMotion";

const DIFFICULTY_COLORS = {
  easy: { bg: "bg-green-500/10", text: "text-green-400", border: "border-green-500/30" },
  medium: { bg: "bg-yellow-500/10", text: "text-yellow-400", border: "border-yellow-500/30" },
  hard: { bg: "bg-red-500/10", text: "text-red-400", border: "border-red-500/30" },
  expert: { bg: "bg-purple-500/10", text: "text-purple-400", border: "border-purple-500/30" },
};

const PROVENANCE_LABELS = {
  official: { label: "Official", color: "text-emerald-400" },
  candidate_reported: { label: "Candidate-reported", color: "text-amber-400" },
  pattern_relevant: { label: "Pattern-relevant", color: "text-blue-400" },
  canonical: { label: "Canonical", color: "text-purple-400" },
  synthetic: { label: "Synthetic", color: "text-gray-400" },
};

// Mastery Ring
function MasteryRing({ score, size = 80, label = "mastery" }) {
  const r = (size - 8) / 2;
  const c = 2 * Math.PI * r;
  const off = c - (score || 0) * c;
  const color =
    (score || 0) >= 0.7 ? "#10B981" : (score || 0) >= 0.4 ? "#F59E0B" : "#EF4444";
  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="rotate-[-90deg]">
        <circle cx={size / 2} cy={size / 2} r={r} fill="none" stroke="rgba(255,255,255,0.10)" strokeWidth={6} />
        <circle
          cx={size / 2} cy={size / 2} r={r}
          fill="none" stroke={color} strokeWidth={6}
          strokeDasharray={c} strokeDashoffset={off}
          strokeLinecap="round" className="transition-all duration-700"
        />
        <text
          x={size / 2} y={size / 2} textAnchor="middle" dominantBaseline="central"
          className="fill-text-primary text-base font-bold"
          style={{ transform: "rotate(90deg)", transformOrigin: "center" }}
        >
          {Math.round((score || 0) * 100)}%
        </text>
      </svg>
      <div className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary mt-1">{label}</div>
    </div>
  );
}

// Mission / Boss card
function MissionCard({ mission, onClick }) {
  const diff = DIFFICULTY_COLORS[mission.difficulty] || DIFFICULTY_COLORS.medium;
  return (
    <motion.button
      whileHover={mission.unlocked ? { y: -3, scale: 1.02 } : {}}
      whileTap={mission.unlocked ? { scale: 0.98 } : {}}
      onClick={() => mission.unlocked && onClick(mission)}
      disabled={!mission.unlocked}
      className={`text-left p-4 rounded-2xl border transition-all w-full ${
        !mission.unlocked
          ? "bg-surface-card/30 border-brand-primary/5 cursor-not-allowed opacity-50"
          : mission.is_boss
          ? "bg-gradient-to-br from-red-500/10 to-amber-500/5 border-red-500/30 hover:border-red-500/50"
          : "bg-surface-card/60 border-brand-primary/10 hover:border-brand-sky/40"
      }`}
    >
      <div className="flex items-start justify-between gap-2 mb-2">
        <div className="flex items-center gap-2">
          {mission.is_boss ? (
            <Crown size={16} className="text-red-400" />
          ) : (
            <Play size={14} className="text-brand-sky" />
          )}
          <span className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">
            {mission.is_boss ? "Boss" : "Mission"}
          </span>
        </div>
        {!mission.unlocked && <Lock size={14} className="text-gray-500" />}
      </div>
      <h4 className="font-display font-bold text-sm text-text-primary mb-2 leading-tight">
        {mission.name}
      </h4>
      <div className="flex items-center gap-2 flex-wrap">
        <span className={`px-1.5 py-0.5 rounded text-[9px] font-mono uppercase border ${diff.bg} ${diff.text} ${diff.border}`}>
          {mission.difficulty}
        </span>
        <span className="text-[10px] font-mono text-amber-400">+{mission.xp_reward || 0} XP</span>
      </div>
      {mission.unlocked && mission.my_mastery > 0 && (
        <div className="mt-2 h-1 rounded-full bg-surface-base overflow-hidden">
          <div
            className="h-full rounded-full"
            style={{
              width: `${mission.my_mastery * 100}%`,
              backgroundColor: mission.gate_passed ? "#10B981" : "#F59E0B",
            }}
          />
        </div>
      )}
    </motion.button>
  );
}

// Town Card (used in World view)
function TownCard({ town, onSelect }) {
  return (
    <div className="bg-surface-card/60 border border-brand-primary/10 rounded-2xl p-5">
      <div className="flex items-start gap-3 mb-4">
        <div className="text-4xl">{town.icon}</div>
        <div className="flex-1">
          <h3 className="font-display font-bold text-lg text-text-primary">{town.display_name}</h3>
          <p className="text-xs text-brand-secondary mt-1">{town.description}</p>
        </div>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        {town.mmissions ? null : (town.missions || []).map((m) => (
          <MissionCard key={m.id} mission={m} onClick={onSelect} />
        ))}
        {(town.missions || []).map((m) => (
          <MissionCard key={m.id} mission={m} onClick={onSelect} />
        ))}
      </div>
    </div>
  );
}

// World Map view
function WorldMap({ data, onSelectMission, progress }) {
  if (!data || !data.world) return null;
  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-brand-sky/10 via-purple-500/5 to-amber-500/5 border border-brand-primary/20 rounded-3xl p-6 sm:p-8">
        <div className="flex items-center gap-2 mb-3">
          <Compass size={18} className="text-brand-sky" />
          <span className="text-xs font-mono uppercase tracking-[0.2em] text-brand-sky">BountyCode Journey</span>
        </div>
        <h1 className="font-display font-black text-2xl sm:text-3xl">{data.world.display_name}</h1>
        <p className="text-sm text-brand-secondary mt-2 max-w-2xl">{data.world.description}</p>

        {progress && (
          <div className="mt-6 grid grid-cols-3 gap-3">
            <div className="bg-surface-base/40 rounded-xl p-3">
              <div className="flex items-center gap-2 mb-1">
                <Zap size={14} className="text-amber-400" />
                <span className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">Adventure</span>
              </div>
              <div className="text-xl font-black text-text-primary">{progress.xp.total} XP</div>
              <div className="text-[10px] text-brand-secondary">{progress.xp.level.title} (lvl {progress.xp.level.level})</div>
            </div>
            <div className="bg-surface-base/40 rounded-xl p-3">
              <div className="flex items-center gap-2 mb-1">
                <GraduationCap size={14} className="text-green-400" />
                <span className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">Mastery</span>
              </div>
              <div className="text-xl font-black text-text-primary">
                {progress.mastery.skills_mastered.length}/{Object.keys(progress.mastery.skills).length || 0}
              </div>
              <div className="text-[10px] text-brand-secondary">skills at gate</div>
            </div>
            <div className="bg-surface-base/40 rounded-xl p-3">
              <div className="flex items-center gap-2 mb-1">
                <Target size={14} className="text-purple-400" />
                <span className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary">Readiness</span>
              </div>
              <div className="text-xl font-black text-text-primary">{progress.readiness.score}</div>
              <div className="text-[10px] text-brand-secondary">{progress.readiness.label}</div>
            </div>
          </div>
        )}
      </div>

      <div className="space-y-4">
        {data.world.towns.map((town) => (
          <TownCard key={town.id} town={town} onSelect={onSelectMission} />
        ))}
      </div>
    </div>
  );
}

// Mission Detail (Practice)
function MissionView({ mission, onComplete, onBack }) {
  const reduced = useReducedMotion();
  const [hintLevel, setHintLevel] = useState(0);
  const [showSolution, setShowSolution] = useState(false);
  const [revealedHints, setRevealedHints] = useState([]);
  const [showConcept, setShowConcept] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);
  const [startTime] = useState(Date.now());

  const lo = mission;
  const diff = DIFFICULTY_COLORS[lo.assessment?.difficulty || "medium"];

  const requestHint = () => {
    const next = hintLevel + 1;
    if (next <= 3) {
      const hintKey = `hint_${next}`;
      setRevealedHints((prev) => [...prev, hintKey]);
      setHintLevel(next);
    }
  };

  const submit = async (passed) => {
    setSubmitting(true);
    const timeTaken = Math.round((Date.now() - startTime) / 1000);
    try {
      const response = await onComplete({
        hints_used: hintLevel,
        first_try: hintLevel === 0,
        time_taken_seconds: timeTaken,
        passed,
      });
      if (response?.success) {
        setResult(response);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-5">
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-sm text-brand-secondary hover:text-brand-sky transition-colors"
      >
        <ArrowLeft size={16} /> Back to map
      </button>

      <CelebrationOverlay
        show={!!result}
        type={result?.mastery?.gate_passed ? "levelup" : "confetti"}
        title={result?.mastery?.gate_passed ? "Mastery Gained" : "Mission Complete"}
        subtitle={`+${result?.xp?.awarded || 0} XP`}
        onClose={() => setResult(null)}
      />

      <div className="bg-surface-card/60 border border-brand-primary/20 rounded-2xl p-5 sm:p-6">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary mb-1">
              {lo.progression?.boss_variant ? "Boss Battle" : "Mission"}
            </div>
            <h2 className="font-display font-bold text-xl text-text-primary">{lo.title}</h2>
            <p className="text-xs text-brand-secondary mt-1">{lo.learning?.concept}</p>
          </div>
          <div className="flex flex-col items-end gap-1">
            <span className={`px-2 py-0.5 rounded text-[10px] font-mono uppercase border ${diff.bg} ${diff.text} ${diff.border}`}>
              {lo.assessment?.difficulty}
            </span>
            <span className="text-[10px] font-mono text-amber-400">+{lo.progression?.xp_reward} XP</span>
          </div>
        </div>

        {/* Provenance badge */}
        {lo.career?.provenance && (
          <div className="mb-4 inline-flex items-center gap-1.5 px-2 py-1 rounded-lg bg-surface-base/40">
            <span className={`text-[10px] font-mono uppercase ${PROVENANCE_LABELS[lo.career.provenance.level]?.color || "text-gray-400"}`}>
              {PROVENANCE_LABELS[lo.career.provenance.level]?.label || lo.career.provenance.level}
            </span>
            <span className="text-[10px] text-brand-secondary">— {lo.career.provenance.note?.slice(0, 70)}...</span>
          </div>
        )}

        {/* Mental model + Why this matters */}
        {showConcept && (
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-3 mb-4"
          >
            {lo.learning?.mental_model && (
              <div className="bg-blue-500/5 border border-blue-500/15 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-1.5">
                  <Brain size={14} className="text-blue-400" />
                  <span className="text-[10px] font-mono uppercase tracking-widest text-blue-400">Mental model</span>
                </div>
                <p className="text-sm text-text-primary leading-relaxed">{lo.learning.mental_model}</p>
              </div>
            )}

            {lo.learning?.why_this_matters && (
              <div className="bg-amber-500/5 border border-amber-500/15 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-1.5">
                  <Lightbulb size={14} className="text-amber-400" />
                  <span className="text-[10px] font-mono uppercase tracking-widest text-amber-400">Why this matters</span>
                </div>
                <p className="text-sm text-text-primary leading-relaxed">{lo.learning.why_this_matters}</p>
              </div>
            )}

            {lo.learning?.real_world && lo.learning.real_world.length > 0 && (
              <details className="bg-green-500/5 border border-green-500/15 rounded-xl p-4">
                <summary className="text-[10px] font-mono uppercase tracking-widest text-green-400 cursor-pointer">
                  Real-world use ({lo.learning.real_world.length})
                </summary>
                <ul className="mt-2 space-y-1.5 text-sm text-text-primary">
                  {lo.learning.real_world.map((u, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <ChevronRight size={12} className="text-green-400 mt-1 shrink-0" />
                      <span>{u}</span>
                    </li>
                  ))}
                </ul>
              </details>
            )}
          </motion.div>
        )}

        {/* Problem statement */}
        <div className="bg-surface-base/50 rounded-xl p-4 mb-4">
          <div className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary mb-2">
            Problem
          </div>
          <pre className="text-sm text-text-primary leading-relaxed whitespace-pre-wrap font-sans">
            {lo.problem}
          </pre>
        </div>

        {/* Test cases */}
        {lo.assessment?.test_cases && lo.assessment.test_cases.length > 0 && (
          <details className="mb-4">
            <summary className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary cursor-pointer mb-2">
              Test cases ({lo.assessment.test_cases.length})
            </summary>
            <div className="space-y-2 mt-2">
              {lo.assessment.test_cases.map((tc, i) => (
                <div key={i} className="bg-surface-base/40 rounded-lg p-2 text-[11px] font-mono">
                  <span className="text-brand-sky">Input:</span> {tc.input}
                  {tc.edge && <span className="ml-2 text-amber-400">[{tc.edge}]</span>}
                  <br />
                  <span className="text-green-400">Expected:</span> {tc.expected}
                </div>
              ))}
            </div>
          </details>
        )}

        {/* Hints */}
        {revealedHints.length > 0 && (
          <div className="space-y-2 mb-4">
            {revealedHints.map((key, i) => {
              const hintText = lo.assistance?.[key];
              if (!hintText) return null;
              return (
                <motion.div
                  key={key}
                  initial={reduced ? {} : { opacity: 0, x: -8 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="bg-purple-500/5 border border-purple-500/20 rounded-xl p-3"
                >
                  <div className="text-[10px] font-mono uppercase tracking-widest text-purple-400 mb-1">
                    Hint {i + 1}
                  </div>
                  <p className="text-sm text-text-primary">{hintText}</p>
                </motion.div>
              );
            })}
          </div>
        )}

        {/* Solution (revealed) */}
        {showSolution && lo.solution?.code && (
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-surface-base/50 rounded-xl p-4 mb-4"
          >
            <div className="text-[10px] font-mono uppercase tracking-widest text-green-400 mb-2">
              Solution
            </div>
            <pre className="bg-surface-base text-text-primary rounded-lg p-3 text-xs font-mono overflow-x-auto">
              <code>{lo.solution.code}</code>
            </pre>
            {lo.solution.time_complexity && (
              <div className="flex gap-3 mt-2 text-[10px]">
                <span className="text-brand-secondary">
                  Time: <span className="font-mono text-text-primary">{lo.solution.time_complexity}</span>
                </span>
                <span className="text-brand-secondary">
                  Space: <span className="font-mono text-text-primary">{lo.solution.space_complexity}</span>
                </span>
              </div>
            )}
          </motion.div>
        )}

        {/* Common mistakes */}
        {lo.assistance?.common_mistakes && lo.assistance.common_mistakes.length > 0 && (
          <details className="mb-4">
            <summary className="text-[10px] font-mono uppercase tracking-widest text-orange-400 cursor-pointer">
              Common mistakes ({lo.assistance.common_mistakes.length})
            </summary>
            <ul className="mt-2 space-y-1 text-sm text-text-primary">
              {lo.assistance.common_mistakes.map((m, i) => (
                <li key={i} className="flex items-start gap-2">
                  <AlertTriangle size={12} className="text-orange-400 mt-1 shrink-0" />
                  <span>{m}</span>
                </li>
              ))}
            </ul>
          </details>
        )}

        {/* Actions */}
        <div className="flex flex-wrap gap-2">
          {hintLevel < 3 && !showSolution && (
            <button
              onClick={requestHint}
              className="px-4 py-2 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400 text-sm font-medium hover:bg-purple-500/20 transition-colors"
            >
              <Lightbulb size={14} className="inline mr-1" />
              Get hint ({hintLevel}/3)
            </button>
          )}
          {!showSolution && (
            <button
              onClick={() => setShowSolution(true)}
              className="px-4 py-2 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm font-medium hover:bg-red-500/20 transition-colors"
            >
              <Eye size={14} className="inline mr-1" />
              Show solution
            </button>
          )}
          <div className="flex-1" />
          <button
            onClick={() => submit(false)}
            disabled={submitting}
            className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/20 text-brand-secondary text-sm font-medium hover:border-brand-sky/30 transition-colors disabled:opacity-50"
          >
            Need more practice
          </button>
          <button
            onClick={() => submit(true)}
            disabled={submitting}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-green-500 to-emerald-500 text-white text-sm font-bold hover:from-green-400 hover:to-emerald-400 transition-all disabled:opacity-50"
          >
            {submitting ? <Spinner size={14} /> : (
              <span className="flex items-center gap-1">
                <CheckCircle2 size={14} /> I solved it
              </span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

// Boss view (transfer test)
function BossView({ boss, onAttempt, onBack }) {
  const reduced = useReducedMotion();
  const [hintLevel, setHintLevel] = useState(0);
  const [startTime] = useState(Date.now());
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(null);

  const lo = boss;
  const myMastery = lo.player_mastery || 0;
  const required = lo.gate_threshold || 0.7;

  const submit = async (passed) => {
    setSubmitting(true);
    const timeTaken = Math.round((Date.now() - startTime) / 1000);
    try {
      const response = await onAttempt({
        passed,
        attempts: 1,
        hints_used: hintLevel,
        time_taken_seconds: timeTaken,
      });
      if (response?.success) setResult(response);
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-5">
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-sm text-brand-secondary hover:text-brand-sky transition-colors"
      >
        <ArrowLeft size={16} /> Back to map
      </button>

      <CelebrationOverlay
        show={!!result && result.gate_passed}
        type="levelup"
        title="Mastery Gate Passed"
        subtitle={`+${result?.xp?.awarded || 0} XP • Mastery ${(result?.mastery?.new_score * 100).toFixed(0)}%`}
        onClose={() => setResult(null)}
      />

      <div className="bg-gradient-to-br from-red-500/10 to-amber-500/5 border border-red-500/30 rounded-2xl p-5 sm:p-6">
        <div className="flex items-center gap-3 mb-4">
          <Crown size={32} className="text-red-400" />
          <div>
            <div className="text-[10px] font-mono uppercase tracking-widest text-red-400">Boss Battle</div>
            <h2 className="font-display font-black text-xl text-text-primary">{lo.title}</h2>
          </div>
        </div>

        {/* Mastery gate */}
        <div className="bg-surface-base/40 rounded-xl p-4 mb-4 flex items-center gap-4">
          <MasteryRing score={myMastery} label="your mastery" />
          <div className="flex-1">
            <h3 className="font-display font-bold text-sm text-text-primary">The Mastery Gate</h3>
            <p className="text-xs text-brand-secondary mt-1 leading-relaxed">
              This is a <strong>transfer test</strong>. The story is new, the technique is one you have
              already learned. Prove you can recognize the pattern, not just reproduce a problem.
            </p>
            <div className="mt-2 text-[10px] font-mono text-brand-secondary">
              Gate: {(required * 100).toFixed(0)}% mastery required
            </div>
          </div>
        </div>

        {/* Story */}
        {lo.learning?.mental_model && (
          <div className="bg-blue-500/5 border border-blue-500/15 rounded-xl p-4 mb-4">
            <div className="text-[10px] font-mono uppercase tracking-widest text-blue-400 mb-1">The Story</div>
            <p className="text-sm text-text-primary leading-relaxed">{lo.learning.mental_model}</p>
          </div>
        )}

        {/* Problem */}
        <div className="bg-surface-base/50 rounded-xl p-4 mb-4">
          <div className="text-[10px] font-mono uppercase tracking-widest text-brand-secondary mb-2">
            Challenge
          </div>
          <pre className="text-sm text-text-primary leading-relaxed whitespace-pre-wrap font-sans">
            {lo.problem}
          </pre>
        </div>

        {/* Hints (3 progressive) */}
        <div className="space-y-2 mb-4">
          {[1, 2, 3].slice(0, hintLevel).map((n) => {
            const hintText = lo.assistance?.[`hint_${n}`];
            if (!hintText) return null;
            return (
              <div key={n} className="bg-purple-500/5 border border-purple-500/20 rounded-xl p-3">
                <div className="text-[10px] font-mono uppercase tracking-widest text-purple-400 mb-1">
                  Hint {n}
                </div>
                <p className="text-sm text-text-primary">{hintText}</p>
              </div>
            );
          })}
        </div>

        {hintLevel < 3 && (
          <button
            onClick={() => setHintLevel(hintLevel + 1)}
            className="px-4 py-2 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-400 text-sm font-medium hover:bg-purple-500/20 transition-colors mb-4"
          >
            <Lightbulb size={14} className="inline mr-1" />
            Get hint ({hintLevel}/3)
          </button>
        )}

        <div className="flex gap-2">
          <div className="flex-1" />
          <button
            onClick={() => submit(false)}
            disabled={submitting}
            className="px-4 py-2 rounded-xl bg-surface-card border border-brand-primary/20 text-brand-secondary text-sm font-medium hover:border-brand-sky/30 transition-colors disabled:opacity-50"
          >
            Failed
          </button>
          <button
            onClick={() => submit(true)}
            disabled={submitting}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-red-500 to-amber-500 text-white text-sm font-bold hover:from-red-400 hover:to-amber-400 transition-all disabled:opacity-50"
          >
            {submitting ? <Spinner size={14} /> : (
              <span className="flex items-center gap-1">
                <Trophy size={14} /> Passed the gate
              </span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

// Main
export default function Journey() {
  const navigate = useNavigate();
  const [stage, setStage] = useState("world"); // world, mission, boss
  const [world, setWorld] = useState(null);
  const [progress, setProgress] = useState(null);
  const [activeMission, setActiveMission] = useState(null);
  const [activeBoss, setActiveBoss] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const reduced = useReducedMotion();

  const loadAll = async () => {
    setLoading(true);
    try {
      const [w, p] = await Promise.all([
        api.journey.getWorld("foundations"),
        api.journey.getProgress(),
      ]);
      setWorld(w.world);
      setProgress(p);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAll();
  }, []);

  const handleSelectMission = async (mission) => {
    try {
      const response = await api.journey.getMission(mission.id);
      if (response.success) {
        setActiveMission(response.mission);
        setStage("mission");
      }
    } catch (err) {
      if (err.response?.status === 403) {
        alert(err.response.data.detail);
      }
    }
  };

  const handleSelectBoss = async (mission) => {
    try {
      const response = await api.journey.getBoss(mission.id);
      if (response.success) {
        setActiveBoss(response.boss);
        setStage("boss");
      }
    } catch (err) {
      if (err.response?.status === 403) {
        alert(err.response.data.detail);
      }
    }
  };

  const handleMissionSelect = (mission) => {
    if (mission.is_boss) {
      handleSelectBoss(mission);
    } else {
      handleSelectMission(mission);
    }
  };

  const handleComplete = async (payload) => {
    if (!activeMission) return null;
    return await api.journey.completeMission(activeMission.progression.mission_id, payload);
  };

  const handleBossAttempt = async (payload) => {
    if (!activeBoss) return null;
    return await api.journey.attemptBoss(activeBoss.progression.mission_id, payload);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-surface-base">
        <Spinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-surface-base px-6 text-center">
        <AlertTriangle size={48} className="text-red-400 mb-3" />
        <h2 className="text-xl font-bold text-text-primary">Journey unavailable</h2>
        <p className="text-sm text-brand-secondary mt-2">{error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-surface-base text-text-primary">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        {stage === "world" && (
          <WorldMap
            data={{ world }}
            onSelectMission={handleMissionSelect}
            progress={progress}
          />
        )}

        {stage === "mission" && activeMission && (
          <MissionView
            mission={activeMission}
            onComplete={async (payload) => {
              const result = await handleComplete(payload);
              if (result?.success) {
                setProgress((p) => ({
                  ...p,
                  readiness: result.readiness,
                  xp: { ...p.xp, total: p.xp.total + (result.xp?.awarded || 0) },
                }));
                return result;
              }
              return null;
            }}
            onBack={() => {
              setStage("world");
              setActiveMission(null);
              loadAll();
            }}
          />
        )}

        {stage === "boss" && activeBoss && (
          <BossView
            boss={activeBoss}
            onAttempt={async (payload) => {
              const result = await handleBossAttempt(payload);
              if (result?.success) {
                setProgress((p) => ({
                  ...p,
                  readiness: result.readiness,
                }));
                return result;
              }
              return null;
            }}
            onBack={() => {
              setStage("world");
              setActiveBoss(null);
              loadAll();
            }}
          />
        )}
      </div>
    </div>
  );
}
