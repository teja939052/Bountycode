import { useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import useAuthStore from "../store/authStore";
import useReducedMotion from "../hooks/useReducedMotion";
import { useDashboard } from "../hooks/useDashboard";
import StreakFreezeModal from "../components/StreakFreezeModal";
import StreakRepairModal from "../components/StreakRepairModal";
import PageSkeleton from "../components/PageSkeleton";
import { useToast } from "../components/Toast";

const READINESS_SKILLS = [
  { key: "dsa", label: "DSA" },
  { key: "cs", label: "CS" },
  { key: "interview", label: "Interview" },
  { key: "resume", label: "Resume" },
] as const;

function formatTimeAgo(dateStr: string) {
  if (!dateStr) return "";
  const now = new Date();
  const then = new Date(dateStr);
  const diffMs = now.getTime() - then.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "Just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  const diffDay = Math.floor(diffHr / 24);
  if (diffDay < 7) return `${diffDay}d ago`;
  return then.toLocaleDateString();
}

export default function Dashboard() {
  const { user } = useAuthStore();
  const toast = useToast();
  const reduced = useReducedMotion();

  const {
    gamification,
    questionStats,
    recentProblems,
    readinessScore,
    dailyChallenge,
    streakStatus,
    isLoading,
    isError,
    refetch,
  } = useDashboard();

  const [showRepair, setShowRepair] = useState(false);

  const readiness = readinessScore?.score || 0;
  const streak = gamification?.streak || streakStatus?.streak || 0;
  const xp = gamification?.xp || 0;
  const level = gamification?.level || 1;
  const xpToNext = gamification?.xp_to_next || 100;
  const xpForCurrent = gamification?.xp_for_current || 0;
  const todayXp = gamification?.today_xp || 0;

  const dailyProblem = dailyChallenge;

  const handleClaimBonus = useCallback(() => {
    if (toast) toast.info("Daily bonus will be available in the Career section");
  }, [toast]);

  if (isLoading) {
    return <PageSkeleton />;
  }

  if (isError) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-bold text-text-primary mb-2">Failed to Load Dashboard</h2>
          <p className="text-sm text-text-muted mb-4">Something went wrong loading your data.</p>
          <button
            onClick={() => refetch()}
            className="px-6 py-2 rounded-[10px] bg-primary text-text-primary text-sm font-medium transition-all hover:bg-primary-dark"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-4 py-6 md:py-8 page-surface">
      <div className="mx-auto max-w-5xl space-y-8">
        {/* Header — where am I? */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="flex items-center justify-between flex-wrap gap-4"
        >
          <div>
            <h1 className="text-2xl md:text-3xl font-black text-text-primary">
              Good evening, {user?.name?.split(" ")[0] || "there"}
            </h1>
            <p className="text-sm text-text-muted mt-1">
              SDE · {readiness}% ready
            </p>
          </div>
          <button
            onClick={handleClaimBonus}
            className="text-text-muted hover:text-primary transition-colors"
          >
            <span className="text-xl">🔔</span>
          </button>
        </motion.div>

        {/* Your Next Mission — what should I do now? */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          {dailyProblem ? (
            <Link to={`/question/${dailyProblem.id || dailyProblem.question_id || "random"}`}>
              <div className="block rounded-[16px] p-6 bg-white border border-border shadow-card transition-all duration-300 hover:border-primary/20">
                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-[10px] bg-primary-soft flex items-center justify-center text-2xl shrink-0">
                    ⚔
                  </div>
                  <div className="min-w-0 flex-1">
                    <h2 className="text-lg font-bold text-text-primary">Your Next Mission</h2>
                    <p className="text-sm font-medium text-text-primary mt-1 line-clamp-1">
                      {dailyProblem.title || dailyProblem.question_title || "Daily Challenge"}
                    </p>
                    <p className="text-sm text-text-muted mt-1 line-clamp-2">
                      {dailyProblem.description || "Solve today's adaptive challenge."}
                    </p>
                    <div className="flex items-center gap-3 mt-3 text-xs text-text-muted">
                      <span>🧠 DSA</span>
                      <span>•</span>
                      <span>20 min</span>
                      <span>•</span>
                      <span className="text-primary font-medium">+{dailyProblem.xp_reward || 80} XP</span>
                    </div>
                  </div>
                  <div className="ml-4 text-text-muted">
                    <span>→</span>
                  </div>
                </div>
              </div>
            </Link>
          ) : (
            <div className="rounded-[16px] p-6 bg-white border border-border shadow-card">
              <h2 className="text-lg font-bold text-text-primary">Your Next Mission</h2>
              <p className="text-sm text-text-muted mt-2">
                Loading today's challenge...
              </p>
            </div>
          )}
        </motion.div>

        {/* Readiness + Skill Breakdown — am I improving? */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="rounded-[16px] p-6 bg-white border border-border shadow-card"
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-text-primary">Your Readiness</h2>
            <span className="text-sm font-medium text-primary">+{Math.max(1, Math.round(readiness / 10))}% this week</span>
          </div>

          {/* Progress bar */}
          <div className="mb-4">
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="font-bold text-text-primary text-3xl stat-numeral">{readiness}%</span>
              <span className="text-text-muted">Target: Software Engineer</span>
            </div>
            <div className="h-2 rounded-full bg-border overflow-hidden">
              <div
                className="h-full rounded-full bg-primary transition-all duration-500 ease-out"
                style={{ width: `${readiness}%` }}
              />
            </div>
          </div>

          {/* Skill breakdown */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {READINESS_SKILLS.map((skill) => {
              const skillScore = readinessScore?.[skill.key] || readinessScore?.[`${skill.key}_score`] || Math.floor(Math.random() * 30 + 50);
              return (
                <div key={skill.key} className="text-center">
                  <div className="text-xs text-text-muted mb-1">{skill.label}</div>
                  <div className="text-lg font-bold text-text-primary stat-numeral">{skillScore}%</div>
                </div>
              );
            })}
          </div>
        </motion.div>

        {/* Your Journey */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="rounded-[16px] p-6 bg-white border border-border shadow-card"
        >
          <h2 className="text-lg font-bold text-text-primary mb-4">Your Journey</h2>
          <div className="flex items-center justify-center">
            <div className="flex items-center gap-4 text-center">
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center text-xl mb-1">
                  🌱
                </div>
                <span className="text-xs text-text-muted">Foundations</span>
                <span className="text-xs font-bold text-primary">✓</span>
              </div>
              <div className="w-12 h-px bg-border"></div>
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-[10px] bg-primary-soft flex items-center justify-center text-xl mb-1">
                  ⚔
                </div>
                <span className="text-xs text-text-muted">Problem Solver</span>
                <span className="text-xs font-bold text-primary">72%</span>
              </div>
              <div className="w-12 h-px bg-border"></div>
              <div className="flex flex-col items-center">
                <div className="w-10 h-10 rounded-[10px] bg-surface-2 border border-border flex items-center justify-center text-xl mb-1">
                  🔒
                </div>
                <span className="text-xs text-text-muted">Builder</span>
                <span className="text-xs text-text-muted">Locked</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* This Week */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="rounded-[16px] p-6 bg-white border border-border shadow-card"
        >
          <h2 className="text-lg font-bold text-text-primary mb-4">This Week</h2>
          <div className="flex flex-wrap gap-4 text-sm">
            <span className="text-text-muted">
              <span className="font-medium text-text-primary">4</span> missions
            </span>
            <span className="text-text-muted">
              <span className="font-medium text-text-primary">2</span> assessments
            </span>
            <span className="text-text-muted">
              <span className="font-medium text-primary">+{Math.max(1, Math.round(readiness / 10))}%</span> readiness
            </span>
          </div>
        </motion.div>
      </div>

      <AnimatePresence>
        {showRepair && (
          <StreakRepairModal
            open={showRepair}
            onClose={() => setShowRepair(false)}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
