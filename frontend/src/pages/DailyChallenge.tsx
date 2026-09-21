import { useState, useEffect, useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link } from "react-router-dom";
import useAuthStore from "../store/authStore";
import { useDailyChallenge } from "../hooks/useDailyChallenge";
import {
  Flame, Trophy, Target, CheckCircle2, Circle, Star, Zap,
  ArrowRight, CalendarDays, Medal, Sparkles, BookOpen,
  Brain, MessageSquareText, Swords, Gift, Clock,
  ChevronRight, User, Gamepad2,
} from "lucide-react";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import CelebrationOverlay from "../components/CelebrationOverlay";
import StreakFreezeModal from "../components/StreakFreezeModal";
import { getLevelForXP } from "../components/XPBar";
import useReducedMotion from "../hooks/useReducedMotion";
import confetti from "canvas-confetti";

const DIFFICULTY_STARS = { easy: 1, medium: 2, hard: 3 };
const DIFFICULTY_COLORS = { easy: "text-green-500", medium: "text-yellow-500", hard: "text-red-500" };

const TYPE_CONFIG = {
  dsa: { icon: BookOpen, color: "bg-blue-100 text-blue-600 border-blue-200", label: "DSA" },
  aptitude: { icon: Brain, color: "bg-purple-100 text-purple-600 border-purple-200", label: "Aptitude" },
  behavioral: { icon: MessageSquareText, color: "bg-orange-100 text-orange-600 border-orange-200", label: "Behavioral" },
};

function formatCountdown(ms) {
  if (!ms || ms <= 0) return "0h 0m";
  const totalMinutes = Math.max(0, Math.floor(ms / 60000));
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return `${h}h ${m}m`;
}

export default function DailyChallenge() {
  const { user } = useAuthStore();
  const reduced = useReducedMotion();
  const { status, progress, leaderboard, today: todayData, enrollMutation, completeDayMutation, isLoading, isError, refetch } = useDailyChallenge();

  const [showEnrollModal, setShowEnrollModal] = useState(false);
  const [selectedPath, setSelectedPath] = useState("general");
  const [showCelebration, setShowCelebration] = useState(false);
  const [celebrationMessage, setCelebrationMessage] = useState("");
  const [behavioralModal, setBehavioralModal] = useState(null);
  const [behavioralAnswer, setBehavioralAnswer] = useState("");
  const [completedQuests, setCompletedQuests] = useState(new Set());
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("today");
  const [showMilestone, setShowMilestone] = useState(false);
  const [milestoneRewards, setMilestoneRewards] = useState(null);
  const [showFreezeModal, setShowFreezeModal] = useState(false);
  const [now, setNow] = useState(Date.now());

  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, []);

  const resetTime = useMemo(() => {
    const d = new Date();
    d.setHours(24, 0, 0, 0);
    return d.getTime();
  }, []);

  const handleEnroll = () => {
    enrollMutation.mutate(selectedPath, {
      onSuccess: () => {
        setShowEnrollModal(false);
      },
      onError: (err) => {
        setError(err.message || "Failed to enroll");
      },
    });
  };

  const handleQuestComplete = (questIndex) => {
    const quest = todayData?.quests?.[questIndex];
    if (!quest) return;

    if (quest.type === "behavioral") {
      setBehavioralModal(questIndex);
      return;
    }

    setCompletedQuests((prev) => {
      const next = new Set(prev);
      if (next.has(questIndex)) next.delete(questIndex);
      else next.add(questIndex);
      return next;
    });
  };

  const handleBehavioralSubmit = () => {
    if (!behavioralAnswer.trim()) return;
    const idx = behavioralModal;
    setCompletedQuests((prev) => new Set([...prev, idx]));
    setBehavioralModal(null);
    setBehavioralAnswer("");
  };

  const handleCompleteDay = () => {
    if (!todayData) return;
    const questIds = [];
    todayData.quests.forEach((q, i) => {
      if (completedQuests.has(i)) {
        questIds.push(q.question_id || q.title);
      }
    });
    completeDayMutation.mutate(questIds, {
      onSuccess: (result) => {
        setShowCelebration(true);
        setCelebrationMessage(`Day ${result.day_completed} Complete! +${result.xp_gained} Diamonds`);
        if (result.completion_bonus) {
          setCelebrationMessage((prev) => `${prev} +${result.completion_bonus} Bonus! 🏆`);
        }

        const earned = (result.xp_gained || 0) + (result.completion_bonus || 0);
        const curTotal = progress?.total_xp || 0;
        const curStreak = progress?.current_streak || 0;

        window.dispatchEvent(
          new CustomEvent("diamonds-gained", { detail: { diamonds: earned, streak: result.new_streak || curStreak + 1 } }),
        );

        const milestone = result.milestone;
        if (milestone && Object.keys(milestone).length > 0) {
          const days = Object.keys(milestone).map(Number);
          const day = Math.max(...days);
          setMilestoneRewards({ day, reward: milestone[day], newStreak: result.new_streak || curStreak + 1 });
          setShowMilestone(true);
        }

        const prevLevel = getLevelForXP(curTotal);
        const nextLevel = getLevelForXP(curTotal + earned);
        if (nextLevel > prevLevel) {
          setTimeout(() => {
            window.dispatchEvent(
              new CustomEvent("celebrate", {
                detail: { type: "levelup", title: String(nextLevel) },
              }),
            );
          }, 1000);
        }

        setTimeout(() => setShowCelebration(false), 3000);
        setCompletedQuests(new Set());
      },
      onError: (err) => {
        setError(err.message || "Failed to complete day");
      },
    });
  };

  const allQuestTypesCompleted = () => {
    if (!todayData?.quests) return false;
    const types = new Set(todayData.quests.map((q) => q.type));
    const covered = new Set();
    todayData.quests.forEach((q, i) => {
      if (completedQuests.has(i)) covered.add(q.type);
    });
    return types.size === covered.size;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4">
        <div className="w-12 h-12 rounded-full border-4 border-brand-sky/30 border-t-brand-sky animate-spin" />
        <p className="text-brand-secondary font-mono text-sm">Loading challenge data...</p>
      </div>
    );
  }

  if (!status?.enrolled) {
    return (
      <div className="min-h-screen py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={reduced ? {} : { opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="text-center">
            <div className="w-20 h-20 rounded-2xl bg-accent-primary flex items-center justify-center mx-auto mb-6 shadow-lg">
              <Gamepad2 size={40} className="text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-display font-extrabold tracking-tight text-primary mb-3">
              30 Days to <span className="text-accent-secondary">Offer</span>
            </h1>
            <p className="text-lg text-secondary max-w-xl mx-auto mb-8">
              A Codédex-style challenge: solve DSA, aptitude, and behavioral questions daily for 30 days.
              Build habits. Crush interviews. Land your dream job.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto mb-10">
              {[
                { icon: Flame, label: "Career Streak", desc: "Daily motivation to keep going", color: "text-orange-500" },
                { icon: Trophy, label: "30-Day Journey", desc: "Structured prep from day 1 to 30", color: "text-accent-warm" },
                { icon: Medal, label: "Placement Ready", desc: "Earn the badge & certificate", color: "text-accent-secondary" },
              ].map((item) => (
                <div key={item.label} className="card p-6 text-center border border-default">
                  <item.icon size={28} className={`mx-auto mb-3 ${item.color}`} />
                  <h3 className="font-display font-bold text-primary mb-1">{item.label}</h3>
                  <p className="text-sm text-secondary">{item.desc}</p>
                </div>
              ))}
            </div>
            <button
              onClick={() => setShowEnrollModal(true)}
              className="btn-primary text-lg px-10 py-4 rounded-2xl inline-flex items-center gap-3"
            >
              <Sparkles size={20} />
              Start the Challenge
            </button>

            <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto text-left">
              <div className="card p-6 border border-white/60">
                <h3 className="font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                  <Target size={18} className="text-brand-sky" /> Daily Quests
                </h3>
                <ul className="space-y-2 text-sm text-brand-secondary">
                  <li className="flex items-center gap-2"><CheckCircle2 size={14} className="text-green-500 shrink-0" /> 2 DSA Problems</li>
                  <li className="flex items-center gap-2"><CheckCircle2 size={14} className="text-green-500 shrink-0" /> 1 Aptitude Test</li>
                  <li className="flex items-center gap-2"><CheckCircle2 size={14} className="text-green-500 shrink-0" /> 1 Behavioral Question</li>
                </ul>
              </div>
              <div className="card p-6 border border-white/60">
                <h3 className="font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                  <Gift size={18} className="text-brand-coral" /> Rewards Scaling
                </h3>
                <ul className="space-y-2 text-sm text-brand-secondary">
                  <li className="flex items-center gap-2"><Zap size={14} className="text-yellow-500" /> Days 1-7: 100 Diamonds/day</li>
                  <li className="flex items-center gap-2"><Zap size={14} className="text-yellow-500" /> Days 8-14: 150 Diamonds/day</li>
                  <li className="flex items-center gap-2"><Zap size={14} className="text-yellow-500" /> Days 15-30: 200-250 Diamonds/day</li>
                  <li className="flex items-center gap-2"><Medal size={14} className="text-brand-sky" /> Perfect 30: +500 Diamonds + Badge</li>
                </ul>
              </div>
            </div>
          </motion.div>
        </div>

        <AnimatePresence>
          {showEnrollModal && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 z-50 flex items-center justify-center bg-surface-2 border-border backdrop-blur-sm p-4"
              onClick={() => setShowEnrollModal(false)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-surface-card rounded-3xl p-8 max-w-md w-full shadow-soft-lg border border-white/60"
                onClick={(e) => e.stopPropagation()}
              >
                <h2 className="text-2xl font-display font-bold text-text-primary mb-2">Choose Your Path</h2>
                <p className="text-brand-secondary text-sm mb-6">Pick the track that matches your career goals</p>
                <div className="space-y-3 mb-6">
                  {[
                    { id: "swe", label: "Software Engineer", desc: "Generalist SWE prep" },
                    { id: "sde", label: "SDE (Product)", desc: "Product-based companies" },
                    { id: "data-scientist", label: "Data Scientist", desc: "ML & analytics roles" },
                    { id: "general", label: "General", desc: "Mixed placement prep" },
                  ].map((p) => (
                    <button
                      key={p.id}
                      onClick={() => setSelectedPath(p.id)}
                      className={`w-full text-left p-4 rounded-2xl border-2 transition-all ${
                        selectedPath === p.id
                          ? "border-brand-sky bg-brand-sky-pale"
                          : "border-brand-primary/10 hover:border-gray-300"
                      }`}
                    >
                      <div className="font-display font-bold text-text-primary">{p.label}</div>
                      <div className="text-sm text-brand-secondary">{p.desc}</div>
                    </button>
                  ))}
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={() => setShowEnrollModal(false)}
                    className="flex-1 px-4 py-3 rounded-2xl border border-brand-primary/10 text-brand-secondary hover:bg-surface-card transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleEnroll}
                    disabled={enrollMutation.isPending}
                    className="flex-1 btn-primary py-3 rounded-2xl disabled:opacity-50"
                  >
                    {enrollMutation.isPending ? "Enrolling..." : "Begin Journey"}
                  </button>
                </div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
  }

  // Enrolled state
  const dayNum = todayData?.day || status?.current_day || 1;
  const progressPct = progress?.completion_percentage || 0;

  return (
    <div className="min-h-screen py-8 px-4 md:px-6">
      <CelebrationOverlay show={showCelebration} type="confetti" title={celebrationMessage} subtitle="Keep going!" />

      <AnimatePresence>
        {showMilestone && milestoneRewards && (
          <StreakMilestoneModal rewards={milestoneRewards} onClose={() => setShowMilestone(false)} />
        )}
        <StreakFreezeModal open={showFreezeModal} onClose={() => setShowFreezeModal(false)} />
      </AnimatePresence>

      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center md:text-left md:flex md:items-center md:justify-between mb-8"
        >
          <div>
            <div className="flex items-center gap-3 mb-2 justify-center md:justify-start">
              <motion.div
                className="w-12 h-12 rounded-2xl bg-accent-primary flex items-center justify-center shadow-md"
                animate={{ scale: [1, 1.1, 1] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              >
                <Gamepad2 size={24} className="text-white" />
              </motion.div>
              <div>
                <h1 className="text-3xl md:text-4xl font-display font-extrabold tracking-tight text-primary">
                  30 Days to <span className="text-accent-secondary">Offer</span>
                </h1>
                <p className="text-sm text-secondary font-mono">
                  Mentored by <span className="text-accent-warm font-bold">{progress?.mentor_name || status?.mentor_name}</span>
                </p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4 mt-4 md:mt-0 justify-center md:justify-end">
            <motion.button
              onClick={() => setShowFreezeModal(true)}
              title="Streak protection — buy a freeze"
              className="flex items-center gap-2 bg-accent-warm/10 px-4 py-2 rounded-full border border-accent-warm/20 hover:border-accent-warm/30 transition-colors"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
            >
              <Flame size={18} className="text-orange-500" />
              <span className="font-display font-bold text-primary">{progress?.current_streak || 0}</span>
              <span className="text-xs text-secondary">day streak</span>
            </motion.button>
            <motion.div
              className="flex items-center gap-2 bg-accent-warm/10 px-4 py-2 rounded-full border border-accent-warm/20"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut", delay: 0.3 }}
            >
              <Zap size={18} className="text-accent-warm" />
              <span className="font-display font-bold text-primary">{progress?.total_xp || 0}</span>
              <span className="text-xs text-secondary">Diamonds</span>
            </motion.div>
          </div>
        </motion.div>

        {/* Day Counter Progress */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-5 mb-8"
        >
          <div className="flex flex-col sm:flex-row items-center gap-5">
            <div className="relative inline-flex items-center justify-center shrink-0">
              <svg width="96" height="96" viewBox="0 0 96 96" className="drop-shadow-lg">
                <circle cx="48" cy="48" r="40" fill="none" stroke="currentColor" strokeWidth="5" className="text-black/5 dark:text-white/10" />
                <motion.circle
                  cx="48" cy="48" r="40"
                  fill="none"
                  stroke="var(--accent-primary)"
                  strokeWidth="5"
                  strokeLinecap="round"
                  className="progress-ring-circle"
                  strokeDasharray={2 * Math.PI * 40}
                  animate={{ strokeDashoffset: 2 * Math.PI * 40 * (1 - Math.min(progressPct, 100) / 100) }}
                  transition={{ duration: 1.1, ease: 'easeOut' }}
                  style={{ filter: 'drop-shadow(0 0 8px rgba(88,204,2,0.35))' }}
                />
              </svg>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-2xl font-black font-display text-primary">{dayNum}</span>
                <span className="text-[9px] font-mono text-muted uppercase tracking-wider">of 30</span>
              </div>
            </div>

            <div className="flex-1 w-full text-center sm:text-left">
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <CalendarDays size={18} className="text-accent-primary" />
                  <span className="font-display font-bold text-primary">Daily Progress</span>
                </div>
                <div className="flex items-center gap-1.5 text-xs font-mono text-muted">
                  <Clock size={12} />
                  <span>Resets in {formatCountdown(resetTime - now)}</span>
                </div>
              </div>
              <div className="w-full h-2.5 bg-black/5 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${progressPct}%` }}
                  transition={{ duration: 1, ease: "easeOut" }}
                  className="h-full rounded-full bg-accent-primary relative"
                >
                  <div className="absolute inset-0 overflow-hidden rounded-full">
                    <div className="absolute inset-0 holo-shimmer opacity-50" style={{ animationDuration: '2.2s' }} />
                  </div>
                </motion.div>
              </div>
              <div className="flex justify-between mt-2 text-xs text-secondary">
                <span>{progress?.total_days_completed || 0} days done</span>
                <span>{progress?.days_missed || 0} missed</span>
                <span>{30 - (progress?.total_days_completed || 0)} remaining</span>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6">
          {[
            { id: "today", label: "Today's Quest", icon: Target },
            { id: "progress", label: "Progress", icon: CalendarDays },
            { id: "leaderboard", label: "Leaderboard", icon: Swords },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-5 py-3 rounded-2xl font-medium text-sm transition-all ${
                  activeTab === tab.id
                    ? "bg-accent-primary text-white shadow-md"
                    : "bg-card border border-default text-secondary hover:border-accent-primary/30"
                }`}
              >
                <Icon size={16} />
                {tab.label}
              </button>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            {activeTab === "today" && (
              <TodayQuestTab
                todayData={todayData}
                dayNum={dayNum}
                completedQuests={completedQuests}
                onQuestComplete={handleQuestComplete}
                onCompleteDay={handleCompleteDay}
                allDone={allQuestTypesCompleted()}
                completing={completeDayMutation.isPending}
                behavioralModal={behavioralModal}
                behavioralAnswer={behavioralAnswer}
                setBehavioralAnswer={setBehavioralAnswer}
                onBehavioralSubmit={handleBehavioralSubmit}
                onCloseBehavioral={() => { setBehavioralModal(null); setBehavioralAnswer(""); }}
                reduced={reduced}
              />
            )}

            {activeTab === "progress" && (
              <ProgressTab progress={progress} reduced={reduced} />
            )}

            {activeTab === "leaderboard" && (
              <LeaderboardTab leaderboard={leaderboard} reduced={reduced} />
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-4">
            <MentorCard mentorName={progress?.mentor_name || status?.mentor_name} todayData={todayData} />
            <RewardsCard dayNum={dayNum} />
            <StatsCard progress={progress} status={status} />
          </div>
        </div>

        {error && (
          <div className="fixed bottom-6 right-6 bg-red-500 text-white px-6 py-3 rounded-2xl shadow-lg text-sm">
            {error}
            <button onClick={() => setError(null)} className="ml-3 text-white/70 hover:text-white">✕</button>
          </div>
        )}
      </div>
    </div>
  );
}

function TodayQuestTab({
  todayData, dayNum, completedQuests, onQuestComplete,
  onCompleteDay, allDone, completing,
  behavioralModal, behavioralAnswer, setBehavioralAnswer,
  onBehavioralSubmit, onCloseBehavioral, reduced,
}) {
  if (!todayData) {
    return (
      <div className="card p-10 text-center border border-default">
        <p className="text-secondary mb-4">No quests available for today.</p>
        <button onClick={() => window.location.reload()} className="btn-primary inline-flex items-center gap-2">
          <ArrowRight size={16} /> Refresh
        </button>
      </div>
    );
  }

  return (
    <div>
      {todayData.mentor_message && (
        <motion.div
          initial={reduced ? {} : { opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-accent-primary/5 border border-accent-primary/10 p-5 rounded-2xl mb-6"
        >
          <p className="text-primary italic font-medium">
            "{todayData.mentor_message}"
          </p>
          <p className="text-xs text-secondary mt-2 font-mono">— {todayData.mentor_name || "Your Mentor"}</p>
        </motion.div>
      )}

      <StaggerContainer className="space-y-4">
        {todayData.quests?.map((quest, i) => {
          const typeCfg = TYPE_CONFIG[quest.type] || TYPE_CONFIG.dsa;
          const Icon = typeCfg.icon;
          const stars = DIFFICULTY_STARS[quest.difficulty] || 2;
          const done = completedQuests.has(i);

          return (
            <StaggerItem key={i}>
              <motion.div
                whileHover={reduced ? {} : { scale: 1.01 }}
                className={`card p-5 border-2 cursor-pointer transition-all ${
                  done ? "border-accent-primary bg-accent-primary/5" : "border-default hover:border-accent-primary/30"
                }`}
                onClick={() => onQuestComplete(i)}
              >
                <div className="flex items-start gap-4">
                  <div className="mt-0.5">
                    {done ? (
                      <CheckCircle2 size={22} className="text-accent-primary" />
                    ) : (
                      <Circle size={22} className="text-muted" />
                    )}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1 flex-wrap">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium border ${typeCfg.color}`}>
                        <Icon size={12} />
                        {typeCfg.label}
                      </span>
                      <div className="flex items-center gap-0.5">
                        {Array.from({ length: 3 }).map((_, si) => (
                          <Star
                            key={si}
                            size={12}
                            className={si < stars ? DIFFICULTY_COLORS[quest.difficulty] || "text-accent-warm" : "text-muted"}
                            fill={si < stars ? "currentColor" : "none"}
                          />
                        ))}
                      </div>
                    </div>
                    <h3 className="font-display font-bold text-primary truncate">{quest.title}</h3>
                  </div>
                  <div className="flex items-center gap-1 text-accent-warm shrink-0">
                    <Zap size={14} />
                    <span className="font-mono font-bold text-sm">{quest.points}</span>
                  </div>
                </div>
              </motion.div>
            </StaggerItem>
          );
        })}
      </StaggerContainer>

      <motion.div
        initial={reduced ? {} : { opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mt-6"
      >
        <div className="card p-5 border border-default mb-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-secondary">Today's total Diamonds</p>
              <p className="text-2xl font-display font-bold text-primary">
                {todayData.total_today_xp || 0} <span className="text-sm text-secondary font-normal">base</span>
                <span className="text-accent-primary"> +{todayData.daily_bonus_xp || 10} bonus</span>
              </p>
            </div>
            <button
              onClick={onCompleteDay}
              disabled={!allDone || completing}
              className={`px-8 py-4 rounded-2xl font-display font-bold text-lg transition-all ${
                allDone
                  ? "bg-accent-primary text-white shadow-lg hover:shadow-xl"
                  : "bg-card text-muted cursor-not-allowed"
              }`}
            >
              {completing ? (
                <span className="flex items-center gap-2">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Completing...
                </span>
              ) : (
                "Complete Day"
              )}
            </button>
          </div>
          {!allDone && (
            <p className="text-xs text-secondary mt-3">Complete all 4 quests to finish today</p>
          )}
        </div>
      </motion.div>

      <AnimatePresence>
        {behavioralModal !== null && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-surface border-border backdrop-blur-sm p-4"
            onClick={onCloseBehavioral}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-card rounded-3xl p-6 max-w-lg w-full shadow-lg border border-default"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-xl font-display font-bold text-primary mb-2">Behavioral Question</h3>
              <p className="text-secondary mb-4">{todayData?.quests?.[behavioralModal]?.title}</p>
              <textarea
                value={behavioralAnswer}
                onChange={(e) => setBehavioralAnswer(e.target.value)}
                placeholder="Use the STAR method: Situation, Task, Action, Result..."
                className="w-full h-40 p-4 rounded-2xl border border-default resize-none focus:border-accent-primary focus:ring-1 focus:ring-accent-primary outline-none text-sm bg-surface"
              />
              <div className="flex gap-3 mt-4">
                <button onClick={onCloseBehavioral} className="flex-1 px-4 py-3 rounded-2xl border border-default text-secondary hover:bg-surface">
                  Cancel
                </button>
                <button
                  onClick={onBehavioralSubmit}
                  disabled={!behavioralAnswer.trim()}
                  className="flex-1 btn-primary py-3 rounded-2xl disabled:opacity-50"
                >
                  Submit Answer
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

function ProgressTab({ progress, reduced }) {
  if (!progress?.enrolled) {
    return <div className="card p-10 text-center text-secondary border border-default">Not enrolled</div>;
  }

  return (
    <div>
      <div className="card p-6 border border-default mb-6">
        <h3 className="font-display font-bold text-primary mb-4 flex items-center gap-2">
          <CalendarDays size={18} className="text-accent-primary" />
          30-Day Calendar
        </h3>
        <div className="grid grid-cols-6 sm:grid-cols-10 gap-1.5">
          {progress.calendar?.map((day) => {
            const colorMap = {
              completed: "bg-accent-primary",
              missed: "bg-red-400",
              current: "bg-accent-secondary",
              future: "bg-card",
            };
            return (
              <div
                key={day.day}
                title={`Day ${day.day}: ${day.status}`}
                className={`aspect-square rounded-lg flex items-center justify-center text-[10px] font-mono font-bold transition-all ${
                  colorMap[day.status] || "bg-card"
                } ${
                  day.status === "current" ? "ring-2 ring-accent-secondary ring-offset-1 text-primary" : ""
                } ${
                  day.status === "completed" ? "text-white" : day.status === "missed" ? "text-white" : "text-muted"
                }`}
              >
                {day.day}
              </div>
            );
          })}
        </div>
        <div className="flex gap-4 mt-4 text-xs text-secondary">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-accent-primary inline-block" /> Completed</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-red-400 inline-block" /> Missed</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-accent-secondary inline-block" /> Today</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-card inline-block" /> Upcoming</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {[
          { label: "Days Completed", value: `${progress.total_days_completed || 0}/30` },
          { label: "Current Streak", value: `${progress.current_streak || 0} days`, color: "text-orange-500" },
          { label: "Longest Streak", value: `${progress.longest_streak || 0} days`, color: "text-accent-secondary" },
          { label: "Total Diamonds", value: `${progress.total_xp || 0}`, color: "text-accent-warm" },
          { label: "Days Missed", value: `${progress.days_missed || 0}`, color: "text-red-500" },
          { label: "Path", value: progress.chosen_path || "General" },
        ].map((stat) => (
          <div key={stat.label} className="card p-4 border border-default">
            <p className="text-xs text-secondary font-mono mb-1">{stat.label}</p>
            <p className={`text-xl font-display font-bold ${stat.color || "text-primary"}`}>{stat.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function LeaderboardTab({ leaderboard, reduced }) {
  const entries = leaderboard?.leaderboard || [];

  return (
    <div className="card p-6 border border-default">
      <h3 className="font-display font-bold text-primary mb-4 flex items-center gap-2">
        <Swords size={18} className="text-accent-coral" />
        Challenge Leaderboard
      </h3>
      {entries.length === 0 ? (
        <p className="text-secondary text-sm">No participants yet. Be the first!</p>
      ) : (
        <div className="space-y-2">
          {entries.map((entry, i) => (
            <div
              key={entry._id || i}
              className={`flex items-center gap-3 p-3 rounded-xl border ${
                i === 0 ? "bg-accent-warm/10 border-accent-warm/20" :
                i === 1 ? "bg-card border-default" :
                i === 2 ? "bg-accent-warm/5 border-accent-warm/10" :
                "border-default"
              }`}
            >
              <span className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold font-mono ${
                i === 0 ? "bg-accent-warm text-white" :
                i === 1 ? "bg-gray-400 text-white" :
                i === 2 ? "bg-orange-400 text-white" :
                "bg-card text-muted"
              }`}>
                {i + 1}
              </span>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-primary truncate">{entry.user_name || "Anonymous"}</p>
                <p className="text-xs text-secondary">Day {entry.current_day || 1} · {entry.completed_days || 0}/30</p>
              </div>
              <div className="text-right">
                <p className="font-mono font-bold text-accent-warm">{entry.total_xp_earned || 0}</p>
                <p className="text-[10px] text-secondary">Diamonds</p>
              </div>
            </div>
          ))}
        </div>
      )}
      {leaderboard?.user_rank && (
        <div className="mt-4 pt-4 border-t border-default text-center">
          <p className="text-sm text-secondary">
            Your Rank: <span className="font-bold text-accent-primary">#{leaderboard.user_rank}</span> of {leaderboard.total_participants || 0}
          </p>
        </div>
      )}
    </div>
  );
}

function MentorCard({ mentorName, todayData }) {
  return (
    <div className="card p-5 border border-default">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-12 h-12 rounded-full bg-accent-primary flex items-center justify-center">
          <User size={20} className="text-white" />
        </div>
        <div>
          <p className="text-xs text-secondary font-mono">Your Mentor</p>
          <p className="font-display font-bold text-primary">{mentorName || "Career Guru"}</p>
        </div>
      </div>
      {todayData?.mentor_message && (
        <p className="text-sm text-secondary italic">"{todayData.mentor_message}"</p>
      )}
    </div>
  );
}

function RewardsCard({ dayNum }) {
  const milestones = [
    { day: 7, label: "Week 1 Complete", diamonds: "700 Diamonds" },
    { day: 14, label: "Week 2 Complete", diamonds: "1,750 Diamonds" },
    { day: 21, label: "Week 3 Complete", diamonds: "3,150 Diamonds" },
    { day: 30, label: "Placement Ready!", diamonds: "+500 Bonus + Badge" },
  ];

  return (
    <div className="card p-5 border border-default">
      <h3 className="font-display font-bold text-primary mb-3 flex items-center gap-2">
        <Gift size={16} className="text-accent-coral" /> Rewards
      </h3>
      <div className="space-y-2">
        {milestones.map((m) => {
          const unlocked = dayNum >= m.day;
          return (
            <div
              key={m.day}
              className={`flex items-center gap-2 p-2 rounded-xl text-sm ${
                unlocked ? "bg-accent-primary/5" : "bg-card opacity-60"
              }`}
            >
              {unlocked ? (
                <CheckCircle2 size={16} className="text-accent-primary shrink-0" />
              ) : (
                <Clock size={16} className="text-muted shrink-0" />
              )}
              <span className={`flex-1 ${unlocked ? "text-primary" : "text-secondary"}`}>
                Day {m.day}: {m.label}
              </span>
              <span className="text-[10px] font-mono text-secondary">{m.diamonds}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function StatsCard({ progress, status }) {
  return (
    <div className="card p-5 border border-default">
      <h3 className="font-display font-bold text-primary mb-3 flex items-center gap-2">
        <Medal size={16} className="text-accent-warm" /> Stats
      </h3>
      <div className="space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-secondary">Path</span>
          <span className="font-medium text-primary capitalize">{progress?.chosen_path || "General"}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-secondary">Streak</span>
          <span className="font-medium text-orange-500">{progress?.current_streak || 0} days</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-secondary">Longest</span>
          <span className="font-medium text-primary">{progress?.longest_streak || 0} days</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-secondary">Completion</span>
          <span className="font-medium text-accent-primary">{progress?.completion_percentage || 0}%</span>
        </div>
      </div>
    </div>
  );
}

const MILESTONE_ITEM_LABELS = {
  coins: { label: "Coins", icon: "🪙", color: "text-yellow-600" },
  streak_freezes: { label: "Streak Freezes", icon: "❄️", color: "text-sky-500" },
  double_xp: { label: "Double Diamonds", icon: "⚡", color: "text-purple-500" },
  skip_boss: { label: "Skip Boss", icon: "🛡️", color: "text-red-500" },
};

function StreakMilestoneModal({ rewards, onClose }) {
  const { day, reward, newStreak } = rewards;
  const items = reward?.items || {};
  const entries = Object.entries(items);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center bg-surface border-border backdrop-blur-sm p-4"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.85, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.85, opacity: 0 }}
        className="relative bg-card rounded-3xl p-8 max-w-sm w-full shadow-lg border border-default text-center overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="absolute -top-16 left-1/2 -translate-x-1/2 w-40 h-40 rounded-full bg-accent-warm/20 blur-2xl" />

        <div className="relative">
          <motion.div
            initial={{ rotate: -12, scale: 0.6, opacity: 0 }}
            animate={{ rotate: 0, scale: 1, opacity: 1 }}
            transition={{ type: "spring", stiffness: 260, damping: 16, delay: 0.1 }}
            className="w-24 h-24 mx-auto mb-4 rounded-3xl bg-accent-warm flex items-center justify-center shadow-lg text-5xl"
          >
            {reward?.emoji || "🎁"}
          </motion.div>

          <div className="text-[10px] font-mono uppercase tracking-[0.25em] text-accent-warm mb-1">
            Streak Milestone · Day {day}
          </div>
          <h3 className="text-2xl font-display font-extrabold text-primary mb-1">{reward?.title}</h3>
          <p className="text-sm text-secondary mb-5">
            🔥 {newStreak}-day streak! Your chest is full of real rewards.
          </p>

          <div className="grid grid-cols-2 gap-2 mb-6">
            {entries.map(([key, value]) => {
              const cfg = MILESTONE_ITEM_LABELS[key] || { label: key, icon: "🎁", color: "text-primary" };
              return (
                <div key={key} className="rounded-2xl border border-accent-warm/20 bg-accent-warm/5 p-3">
                  <div className="text-xl mb-0.5">{cfg.icon}</div>
                  <div className={`font-display font-bold text-lg ${cfg.color}`}>+{Number(value) || 0}</div>
                  <div className="text-[10px] font-mono text-secondary">{cfg.label}</div>
                </div>
              );
            })}
          </div>

          <button
            onClick={onClose}
            className="w-full px-4 py-3 rounded-2xl bg-accent-warm text-white font-display font-bold text-sm shadow-md hover:shadow-lg transition-shadow"
          >
            Claim & keep going
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
}
