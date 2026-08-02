import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Link, useNavigate } from "react-router-dom";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import {
  Flame, Trophy, Target, CheckCircle2, Circle, Star, Zap,
  ArrowRight, CalendarDays, Medal, Sparkles, BookOpen,
  Brain, MessageSquareText, Swords, Gift, Clock,
  ChevronRight, User, Gamepad2,
} from "lucide-react";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import CelebrationOverlay from "../components/CelebrationOverlay";
import useReducedMotion from "../hooks/useReducedMotion";

const DIFFICULTY_STARS = { easy: 1, medium: 2, hard: 3 };
const DIFFICULTY_COLORS = { easy: "text-green-500", medium: "text-yellow-500", hard: "text-red-500" };

const TYPE_CONFIG = {
  dsa: { icon: BookOpen, color: "bg-blue-100 text-blue-600 border-blue-200", label: "DSA" },
  aptitude: { icon: Brain, color: "bg-purple-100 text-purple-600 border-purple-200", label: "Aptitude" },
  behavioral: { icon: MessageSquareText, color: "bg-orange-100 text-orange-600 border-orange-200", label: "Behavioral" },
};

export default function DailyChallenge() {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const reduced = useReducedMotion();
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState(null);
  const [todayData, setTodayData] = useState(null);
  const [progress, setProgress] = useState(null);
  const [leaderboard, setLeaderboard] = useState(null);
  const [showEnrollModal, setShowEnrollModal] = useState(false);
  const [selectedPath, setSelectedPath] = useState("general");
  const [enrolling, setEnrolling] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);
  const [celebrationMessage, setCelebrationMessage] = useState("");
  const [completing, setCompleting] = useState(false);
  const [behavioralModal, setBehavioralModal] = useState(null);
  const [behavioralAnswer, setBehavioralAnswer] = useState("");
  const [completedQuests, setCompletedQuests] = useState(new Set());
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("today");

  useEffect(() => {
    loadAll();
  }, []);

  const loadAll = async () => {
    setLoading(true);
    setError(null);
    try {
      const [statusData, progressData, lbData] = await Promise.all([
        api.getDailyChallengeStatus().catch(() => ({ enrolled: false })),
        api.getDailyChallengeProgress().catch(() => ({ enrolled: false })),
        api.getDailyChallengeLeaderboard().catch(() => ({ leaderboard: [], user_rank: null })),
      ]);
      setStatus(statusData);
      setProgress(progressData);
      setLeaderboard(lbData);

      if (statusData.enrolled && !statusData.today_completed) {
        const today = await api.getDailyChallengeToday();
        setTodayData(today);
      } else if (statusData.enrolled && statusData.today_completed) {
        const today = await api.getDailyChallengeToday();
        setTodayData(today);
      }
    } catch (err) {
      console.error(err);
      setError("Failed to load challenge data");
    } finally {
      setLoading(false);
    }
  };

  const handleEnroll = async () => {
    setEnrolling(true);
    try {
      const data = await api.enrollDailyChallenge(selectedPath);
      setShowEnrollModal(false);
      await loadAll();
    } catch (err) {
      setError(err.message || "Failed to enroll");
    } finally {
      setEnrolling(false);
    }
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

  const handleCompleteDay = async () => {
    if (!todayData) return;
    setCompleting(true);
    try {
      const questIds = [];
      todayData.quests.forEach((q, i) => {
        if (completedQuests.has(i)) {
          questIds.push(q.question_id || q.title);
        }
      });
      const result = await api.completeDailyChallengeDay(questIds);
      setShowCelebration(true);
      setCelebrationMessage(`Day ${result.day_completed} Complete! +${result.xp_gained} XP`);
      if (result.completion_bonus) {
        setCelebrationMessage((prev) => `${prev} +${result.completion_bonus} Bonus! 🏆`);
      }
      setTimeout(() => setShowCelebration(false), 3000);
      await loadAll();
      setCompletedQuests(new Set());
    } catch (err) {
      setError(err.message || "Failed to complete day");
    } finally {
      setCompleting(false);
    }
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

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4">
        <div className="w-12 h-12 rounded-full border-4 border-brand-sky/30 border-t-brand-sky animate-spin" />
        <p className="text-text-light font-mono text-sm">Loading challenge data...</p>
      </div>
    );
  }

  if (!status?.enrolled) {
    return (
      <div className="min-h-screen py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div initial={reduced ? {} : { opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="text-center">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-br from-brand-sky via-brand-lavender to-brand-coral flex items-center justify-center mx-auto mb-6 shadow-soft-lg">
              <Gamepad2 size={40} className="text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-display font-extrabold tracking-tight text-text-primary mb-3">
              30 Days to <span className="text-brand-sky">Offer</span>
            </h1>
            <p className="text-lg text-text-light max-w-xl mx-auto mb-8">
              A Codédex-style challenge: solve DSA, aptitude, and behavioral questions daily for 30 days.
              Build habits. Crush interviews. Land your dream job.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto mb-10">
              {[
                { icon: Flame, label: "Career Streak", desc: "Daily motivation to keep going", color: "text-orange-500" },
                { icon: Trophy, label: "30-Day Journey", desc: "Structured prep from day 1 to 30", color: "text-yellow-500" },
                { icon: Medal, label: "Placement Ready", desc: "Earn the badge & certificate", color: "text-brand-sky" },
              ].map((item) => (
                <div key={item.label} className="card p-6 text-center border border-white/60">
                  <item.icon size={28} className={`mx-auto mb-3 ${item.color}`} />
                  <h3 className="font-display font-bold text-text-primary mb-1">{item.label}</h3>
                  <p className="text-sm text-text-light">{item.desc}</p>
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
                <ul className="space-y-2 text-sm text-text-light">
                  <li className="flex items-center gap-2"><CheckCircle2 size={14} className="text-green-500 shrink-0" /> 2 DSA Problems</li>
                  <li className="flex items-center gap-2"><CheckCircle2 size={14} className="text-green-500 shrink-0" /> 1 Aptitude Test</li>
                  <li className="flex items-center gap-2"><CheckCircle2 size={14} className="text-green-500 shrink-0" /> 1 Behavioral Question</li>
                </ul>
              </div>
              <div className="card p-6 border border-white/60">
                <h3 className="font-display font-bold text-text-primary mb-3 flex items-center gap-2">
                  <Gift size={18} className="text-brand-coral" /> Rewards Scaling
                </h3>
                <ul className="space-y-2 text-sm text-text-light">
                  <li className="flex items-center gap-2"><Zap size={14} className="text-yellow-500" /> Days 1-7: 100 XP/day</li>
                  <li className="flex items-center gap-2"><Zap size={14} className="text-yellow-500" /> Days 8-14: 150 XP/day</li>
                  <li className="flex items-center gap-2"><Zap size={14} className="text-yellow-500" /> Days 15-30: 200-250 XP/day</li>
                  <li className="flex items-center gap-2"><Medal size={14} className="text-brand-sky" /> Perfect 30: +500 XP + Badge</li>
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
              className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
              onClick={() => setShowEnrollModal(false)}
            >
              <motion.div
                initial={{ scale: 0.9, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 0.9, opacity: 0 }}
                className="bg-white rounded-3xl p-8 max-w-md w-full shadow-soft-lg border border-white/60"
                onClick={(e) => e.stopPropagation()}
              >
                <h2 className="text-2xl font-display font-bold text-text-primary mb-2">Choose Your Path</h2>
                <p className="text-text-light text-sm mb-6">Pick the track that matches your career goals</p>
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
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                    >
                      <div className="font-display font-bold text-text-primary">{p.label}</div>
                      <div className="text-sm text-text-light">{p.desc}</div>
                    </button>
                  ))}
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={() => setShowEnrollModal(false)}
                    className="flex-1 px-4 py-3 rounded-2xl border border-gray-200 text-text-light hover:bg-gray-50 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleEnroll}
                    disabled={enrolling}
                    className="flex-1 btn-primary py-3 rounded-2xl disabled:opacity-50"
                  >
                    {enrolling ? "Enrolling..." : "Begin Journey"}
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

      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center md:text-left md:flex md:items-center md:justify-between mb-8"
        >
          <div>
            <div className="flex items-center gap-3 mb-2 justify-center md:justify-start">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-brand-sky via-brand-lavender to-brand-coral flex items-center justify-center shadow-soft-md">
                <Gamepad2 size={24} className="text-white" />
              </div>
              <div>
                <h1 className="text-3xl md:text-4xl font-display font-extrabold tracking-tight text-text-primary">
                  30 Days to <span className="text-brand-sky">Offer</span>
                </h1>
                <p className="text-sm text-text-light font-mono">
                  Mentored by <span className="text-brand-coral font-bold">{progress?.mentor_name || status?.mentor_name}</span>
                </p>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-4 mt-4 md:mt-0 justify-center md:justify-end">
            <div className="flex items-center gap-2 bg-gradient-to-r from-orange-50 to-red-50 px-4 py-2 rounded-full border border-orange-200">
              <Flame size={18} className="text-orange-500" />
              <span className="font-display font-bold text-text-primary">{progress?.current_streak || 0}</span>
              <span className="text-xs text-text-light">day streak</span>
            </div>
            <div className="flex items-center gap-2 bg-gradient-to-r from-yellow-50 to-amber-50 px-4 py-2 rounded-full border border-yellow-200">
              <Zap size={18} className="text-yellow-500" />
              <span className="font-display font-bold text-text-primary">{progress?.total_xp || 0}</span>
              <span className="text-xs text-text-light">XP</span>
            </div>
          </div>
        </motion.div>

        {/* Day Counter Progress Bar */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="card p-5 mb-8 border border-white/60"
        >
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <CalendarDays size={18} className="text-brand-sky" />
              <span className="font-display font-bold text-text-primary">Day {dayNum} of 30</span>
            </div>
            <span className="text-sm text-text-light font-mono">{progressPct}% complete</span>
          </div>
          <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${progressPct}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
              className="h-full rounded-full bg-gradient-to-r from-brand-sky via-brand-lavender to-brand-coral"
            />
          </div>
          <div className="flex justify-between mt-2 text-xs text-text-light">
            <span>{progress?.total_days_completed || 0} days done</span>
            <span>{progress?.days_missed || 0} missed</span>
            <span>{30 - (progress?.total_days_completed || 0)} remaining</span>
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
                    ? "bg-brand-sky text-white shadow-soft-md"
                    : "bg-white border border-gray-200 text-text-light hover:border-brand-sky/30"
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
                completing={completing}
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
          <div className="fixed bottom-6 right-6 bg-error text-white px-6 py-3 rounded-2xl shadow-soft-lg text-sm">
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
      <div className="card p-10 text-center border border-white/60">
        <p className="text-text-light mb-4">No quests available for today.</p>
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
          className="bg-gradient-to-r from-brand-sky-pale via-brand-lavender-pale to-brand-coral-pale p-5 rounded-2xl mb-6 border border-white/60"
        >
          <p className="text-text-primary italic font-medium">
            "{todayData.mentor_message}"
          </p>
          <p className="text-xs text-text-light mt-2 font-mono">— {todayData.mentor_name || "Your Mentor"}</p>
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
                  done ? "border-green-300 bg-green-50/50" : "border-white/60 hover:border-brand-sky/30"
                }`}
                onClick={() => onQuestComplete(i)}
              >
                <div className="flex items-start gap-4">
                  <div className="mt-0.5">
                    {done ? (
                      <CheckCircle2 size={22} className="text-green-500" />
                    ) : (
                      <Circle size={22} className="text-gray-300" />
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
                            className={si < stars ? DIFFICULTY_COLORS[quest.difficulty] || "text-yellow-500" : "text-gray-200"}
                            fill={si < stars ? "currentColor" : "none"}
                          />
                        ))}
                      </div>
                    </div>
                    <h3 className="font-display font-bold text-text-primary truncate">{quest.title}</h3>
                  </div>
                  <div className="flex items-center gap-1 text-yellow-600 shrink-0">
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
        <div className="card p-5 border border-white/60 mb-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-text-light">Today's total XP</p>
              <p className="text-2xl font-display font-bold text-text-primary">
                {todayData.total_today_xp || 0} <span className="text-sm text-text-light font-normal">base</span>
                <span className="text-green-500"> +{todayData.daily_bonus_xp || 10} bonus</span>
              </p>
            </div>
            <button
              onClick={onCompleteDay}
              disabled={!allDone || completing}
              className={`px-8 py-4 rounded-2xl font-display font-bold text-lg transition-all ${
                allDone
                  ? "bg-gradient-to-r from-brand-sky to-brand-lavender text-white shadow-soft-md hover:shadow-soft-lg"
                  : "bg-gray-100 text-gray-300 cursor-not-allowed"
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
            <p className="text-xs text-text-light mt-3">Complete all 4 quests to finish today</p>
          )}
        </div>
      </motion.div>

      <AnimatePresence>
        {behavioralModal !== null && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
            onClick={onCloseBehavioral}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-3xl p-6 max-w-lg w-full shadow-soft-lg border border-white/60"
              onClick={(e) => e.stopPropagation()}
            >
              <h3 className="text-xl font-display font-bold text-text-primary mb-2">Behavioral Question</h3>
              <p className="text-text-light mb-4">{todayData?.quests?.[behavioralModal]?.title}</p>
              <textarea
                value={behavioralAnswer}
                onChange={(e) => setBehavioralAnswer(e.target.value)}
                placeholder="Use the STAR method: Situation, Task, Action, Result..."
                className="w-full h-40 p-4 rounded-2xl border border-gray-200 resize-none focus:border-brand-sky focus:ring-1 focus:ring-brand-sky outline-none text-sm"
              />
              <div className="flex gap-3 mt-4">
                <button onClick={onCloseBehavioral} className="flex-1 px-4 py-3 rounded-2xl border border-gray-200 text-text-light hover:bg-gray-50">
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
    return <div className="card p-10 text-center text-text-light border border-white/60">Not enrolled</div>;
  }

  return (
    <div>
      <div className="card p-6 border border-white/60 mb-6">
        <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
          <CalendarDays size={18} className="text-brand-sky" />
          30-Day Calendar
        </h3>
        <div className="grid grid-cols-6 sm:grid-cols-10 gap-1.5">
          {progress.calendar?.map((day) => {
            const colorMap = {
              completed: "bg-green-400",
              missed: "bg-red-300",
              current: "bg-brand-sky",
              future: "bg-gray-100",
            };
            return (
              <div
                key={day.day}
                title={`Day ${day.day}: ${day.status}`}
                className={`aspect-square rounded-lg flex items-center justify-center text-[10px] font-mono font-bold transition-all ${
                  colorMap[day.status] || "bg-gray-100"
                } ${
                  day.status === "current" ? "ring-2 ring-brand-sky ring-offset-1 text-white" : ""
                } ${
                  day.status === "completed" ? "text-white" : day.status === "missed" ? "text-white" : "text-text-light"
                }`}
              >
                {day.day}
              </div>
            );
          })}
        </div>
        <div className="flex gap-4 mt-4 text-xs text-text-light">
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-green-400 inline-block" /> Completed</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-red-300 inline-block" /> Missed</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-brand-sky inline-block" /> Today</span>
          <span className="flex items-center gap-1"><span className="w-3 h-3 rounded bg-gray-100 inline-block" /> Upcoming</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {[
          { label: "Days Completed", value: `${progress.total_days_completed || 0}/30` },
          { label: "Current Streak", value: `${progress.current_streak || 0} days`, color: "text-orange-500" },
          { label: "Longest Streak", value: `${progress.longest_streak || 0} days`, color: "text-brand-sky" },
          { label: "Total XP", value: `${progress.total_xp || 0}`, color: "text-yellow-500" },
          { label: "Days Missed", value: `${progress.days_missed || 0}`, color: "text-red-500" },
          { label: "Path", value: progress.chosen_path || "General" },
        ].map((stat) => (
          <div key={stat.label} className="card p-4 border border-white/60">
            <p className="text-xs text-text-light font-mono mb-1">{stat.label}</p>
            <p className={`text-xl font-display font-bold ${stat.color || "text-text-primary"}`}>{stat.value}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function LeaderboardTab({ leaderboard, reduced }) {
  const entries = leaderboard?.leaderboard || [];

  return (
    <div className="card p-6 border border-white/60">
      <h3 className="font-display font-bold text-text-primary mb-4 flex items-center gap-2">
        <Swords size={18} className="text-brand-coral" />
        Challenge Leaderboard
      </h3>
      {entries.length === 0 ? (
        <p className="text-text-light text-sm">No participants yet. Be the first!</p>
      ) : (
        <div className="space-y-2">
          {entries.map((entry, i) => (
            <div
              key={entry._id || i}
              className={`flex items-center gap-3 p-3 rounded-xl ${
                i === 0 ? "bg-yellow-50 border border-yellow-200" :
                i === 1 ? "bg-gray-50 border border-gray-200" :
                i === 2 ? "bg-orange-50 border border-orange-200" :
                "border border-gray-100"
              }`}
            >
              <span className={`w-7 h-7 rounded-full flex items-center justify-center text-sm font-bold font-mono ${
                i === 0 ? "bg-yellow-400 text-white" :
                i === 1 ? "bg-gray-400 text-white" :
                i === 2 ? "bg-orange-400 text-white" :
                "bg-gray-100 text-text-light"
              }`}>
                {i + 1}
              </span>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-text-primary truncate">{entry.user_name || "Anonymous"}</p>
                <p className="text-xs text-text-light">Day {entry.current_day || 1} · {entry.completed_days || 0}/30</p>
              </div>
              <div className="text-right">
                <p className="font-mono font-bold text-yellow-600">{entry.total_xp_earned || 0}</p>
                <p className="text-[10px] text-text-light">XP</p>
              </div>
            </div>
          ))}
        </div>
      )}
      {leaderboard?.user_rank && (
        <div className="mt-4 pt-4 border-t border-gray-100 text-center">
          <p className="text-sm text-text-light">
            Your Rank: <span className="font-bold text-brand-sky">#{leaderboard.user_rank}</span> of {leaderboard.total_participants || 0}
          </p>
        </div>
      )}
    </div>
  );
}

function MentorCard({ mentorName, todayData }) {
  return (
    <div className="card p-5 border border-white/60">
      <div className="flex items-center gap-3 mb-3">
        <div className="w-12 h-12 rounded-full bg-gradient-to-br from-brand-sky to-brand-lavender flex items-center justify-center">
          <User size={20} className="text-white" />
        </div>
        <div>
          <p className="text-xs text-text-light font-mono">Your Mentor</p>
          <p className="font-display font-bold text-text-primary">{mentorName || "Career Guru"}</p>
        </div>
      </div>
      {todayData?.mentor_message && (
        <p className="text-sm text-text-light italic">"{todayData.mentor_message}"</p>
      )}
    </div>
  );
}

function RewardsCard({ dayNum }) {
  const milestones = [
    { day: 7, label: "Week 1 Complete", xp: "700 XP" },
    { day: 14, label: "Week 2 Complete", xp: "1,750 XP" },
    { day: 21, label: "Week 3 Complete", xp: "3,150 XP" },
    { day: 30, label: "Placement Ready!", xp: "+500 Bonus + Badge" },
  ];

  return (
    <div className="card p-5 border border-white/60">
      <h3 className="font-display font-bold text-text-primary mb-3 flex items-center gap-2">
        <Gift size={16} className="text-brand-coral" /> Rewards
      </h3>
      <div className="space-y-2">
        {milestones.map((m) => {
          const unlocked = dayNum >= m.day;
          return (
            <div
              key={m.day}
              className={`flex items-center gap-2 p-2 rounded-xl text-sm ${
                unlocked ? "bg-green-50" : "bg-gray-50 opacity-60"
              }`}
            >
              {unlocked ? (
                <CheckCircle2 size={16} className="text-green-500 shrink-0" />
              ) : (
                <Clock size={16} className="text-gray-300 shrink-0" />
              )}
              <span className={`flex-1 ${unlocked ? "text-text-primary" : "text-text-light"}`}>
                Day {m.day}: {m.label}
              </span>
              <span className="text-[10px] font-mono text-text-light">{m.xp}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function StatsCard({ progress, status }) {
  return (
    <div className="card p-5 border border-white/60">
      <h3 className="font-display font-bold text-text-primary mb-3 flex items-center gap-2">
        <Medal size={16} className="text-yellow-500" /> Stats
      </h3>
      <div className="space-y-3">
        <div className="flex justify-between text-sm">
          <span className="text-text-light">Path</span>
          <span className="font-medium text-text-primary capitalize">{progress?.chosen_path || "General"}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-light">Streak</span>
          <span className="font-medium text-orange-500">{progress?.current_streak || 0} days</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-light">Longest</span>
          <span className="font-medium text-text-primary">{progress?.longest_streak || 0} days</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-light">Completion</span>
          <span className="font-medium text-green-500">{progress?.completion_percentage || 0}%</span>
        </div>
      </div>
    </div>
  );
}
