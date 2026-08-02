import { useEffect, useState, useMemo, useCallback } from "react";
import { Link } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useJuice } from "../juice/JuiceProvider";
import {
  Flame,
  Trophy,
  Target,
  Zap,
  Award,
  Crown,
  Sword,
  Shield,
  Code2,
  Play,
  Brain,
  FileText,
  Building2,
  TrendingUp,
  BarChart3,
  Calendar,
  Compass,
  Activity,
  ChevronRight,
  Sparkles,
  Flame as Fire,
  Coins,
  Snowflake,
  Users,
  BookOpen,
  Layers,
  Settings,
  RotateCcw,
  AlertCircle,
  Info,
  X,
  Hash,
  Gift,
  CheckCircle,
  Lock,
  ArrowRight,
   Star,
   Rocket,
} from "lucide-react";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import useReducedMotion from "../hooks/useReducedMotion";
import { useFeatureGate } from "../hooks/useFeatureGate";
import ActivityHeatmap from "../components/ActivityHeatmap";
import Skeleton from "../components/ui/Skeleton";
import UpgradeModal from "../components/UpgradeModal";
import AvatarCustomizer from "../components/AvatarCustomizer";
import UsageBar from "../components/UsageBar";
import { useToast } from "../components/Toast";

const DIFFICULTY_CONFIG = {
  easy: { label: "Easy", color: "#22c55e", bg: "bg-green-500/15", text: "text-green-400", bar: "bg-green-500" },
  medium: { label: "Medium", color: "#eab308", bg: "bg-yellow-500/15", text: "text-yellow-400", bar: "bg-yellow-500" },
  hard: { label: "Hard", color: "#ef4444", bg: "bg-red-500/15", text: "text-red-400", bar: "bg-red-500" },
};

const TIER_BADGE = {
  free: { label: "Free", color: "text-gray-400", bg: "bg-gray-500/10", border: "border-gray-500/20", icon: Hash },
  pro: { label: "Pro", color: "text-brand-gold", bg: "bg-amber-500/10", border: "border-amber-500/20", icon: Crown },
  lifetime: { label: "Founder", color: "text-purple-400", bg: "bg-purple-500/10", border: "border-purple-500/20", icon: Crown },
};

const LEVELS = [
  { min: 1, title: "Newcomer", icon: Hash },
  { min: 3, title: "Beginner", icon: BookOpen },
  { min: 5, title: "Apprentice", icon: Target },
  { min: 8, title: "Practitioner", icon: Shield },
  { min: 12, title: "Expert", icon: Trophy },
  { min: 16, title: "Master", icon: Crown },
  { min: 20, title: "Grandmaster", icon: Award },
  { min: 25, title: "Legend", icon: Sword },
];

const QUICK_ACTIONS = [
  { to: "/question-bank/random", icon: Sword, label: "Today's Drill", color: "from-red-500 to-orange-500", feature: null },
  { to: "/interview", icon: Target, label: "Mock Interview", color: "from-brand-sky to-cyan-400", feature: "interview" },
  { to: "/compiler", icon: Code2, label: "Open Compiler", color: "from-brand-gold to-amber-400", feature: null },
  { to: "/adaptive", icon: Compass, label: "Continue Learning", color: "from-brand-lavender to-fuchsia-400", feature: null },
  { to: "/daily-drill", icon: Flame, label: "Daily Drill", color: "from-brand-coral to-red-400", feature: null },
  { to: "/system-design", icon: Layers, label: "System Design", color: "from-teal-500 to-cyan-400", feature: null },
  { to: "/resume-ats", icon: FileText, label: "Resume Review", color: "from-green-500 to-emerald-400", feature: "resume" },
  { to: "/salary-negotiation", icon: Shield, label: "Salary Prep", color: "from-purple-500 to-pink-400", feature: null },
];

function getTierBadge(plan) {
  return TIER_BADGE[plan] || TIER_BADGE.free;
}

function getLevelTitle(level) {
  for (let i = LEVELS.length - 1; i >= 0; i--) {
    if (level >= LEVELS[i].min) return LEVELS[i];
  }
  return LEVELS[0];
}

function getDiffBadge(difficulty) {
  const c = DIFFICULTY_CONFIG[difficulty] || DIFFICULTY_CONFIG.easy;
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-mono font-bold uppercase ${c.bg} ${c.text}`}>
      {c.label}
    </span>
  );
}

function formatTimeAgo(dateStr) {
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

function AnimatedNumber({ value, duration = 0.6 }) {
  const [display, setDisplay] = useState(0);
  const reduced = useReducedMotion();

  useEffect(() => {
    if (reduced) {
      setDisplay(value);
      return;
    }
    let startTime = performance.now();
    const animate = (now) => {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / (duration * 1000), 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setDisplay(Math.round(eased * value));
      if (progress < 1) requestAnimationFrame(animate);
    };
    requestAnimationFrame(animate);
  }, [value, duration, reduced]);

  return <span>{display}</span>;
}

function XPProgressBar({ currentXP, xpToNext, xpForCurrent, level }) {
  const pct = Math.min(100, ((currentXP - xpForCurrent) / Math.max(1, xpToNext - xpForCurrent)) * 100);
  const reduced = useReducedMotion();

  return (
    <div className="w-full">
      <div className="flex items-center justify-between text-[10px] font-mono uppercase tracking-[0.2em] text-slate-400 mb-2">
        <span>Level {level}</span>
        <span>{currentXP - xpForCurrent} / {xpToNext - xpForCurrent} XP</span>
      </div>
      <div className="h-3 rounded-full bg-white/5 overflow-hidden relative">
        <motion.div
          className="h-full rounded-full bg-gradient-to-r from-brand-sky via-cyan-300 to-brand-gold relative"
          initial={reduced ? {} : { width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 1, ease: "easeOut" }}
        >
          <div className="absolute right-0 top-0 h-full w-2 bg-white/60 blur-sm" />
        </motion.div>
      </div>
    </div>
  );
}

function DifficultyBars({ easy, medium, hard, total }) {
  return (
    <div className="space-y-2.5">
      {Object.entries({ easy, medium, hard }).map(([key, count]) => {
        const c = DIFFICULTY_CONFIG[key];
        return (
          <div key={key} className="flex items-center gap-3">
            <span className="w-16 text-[10px] font-mono uppercase text-slate-400">{c.label}</span>
            <div className="flex-1 h-4 bg-white/5 rounded-full overflow-hidden">
              <motion.div
                className="h-full rounded-full transition-all duration-700"
                style={{ width: `${total > 0 ? (count / total) * 100 : 0}%`, backgroundColor: c.color }}
                initial={{ width: 0 }}
                animate={{ width: `${total > 0 ? (count / total) * 100 : 0}%` }}
                transition={{ duration: 0.8, ease: "easeOut" }}
              />
            </div>
            <span className="w-10 text-right text-xs font-mono text-slate-300">{count}</span>
          </div>
        );
      })}
    </div>
  );
}

function WeekBarChart({ data }) {
  const max = Math.max(...data.map((d) => d.count), 1);
  return (
    <div className="flex items-end gap-1.5 h-20">
      {data.map((day, i) => {
        const h = (day.count / max) * 100;
        const isToday = i === data.length - 1;
        return (
          <div key={i} className="flex-1 flex flex-col items-center gap-1">
            <span className="text-[9px] font-mono text-slate-500">{day.count}</span>
            <motion.div
              className={`w-full rounded-sm transition-all duration-500 ${isToday ? "bg-brand-sky" : "bg-brand-sky/40"}`}
              style={{ height: `${Math.max(4, h)}px` }}
              initial={{ height: 0 }}
              animate={{ height: `${Math.max(4, h)}px` }}
              transition={{ duration: 0.5, delay: i * 0.05 }}
            />
            <span className="text-[9px] font-mono text-slate-500">{day.label}</span>
          </div>
        );
      })}
    </div>
  );
}

function TierBadge({ plan, size = "sm" }) {
  const tier = getTierBadge(plan);
  const Icon = tier.icon;
  const sizeClasses = size === "sm" ? "px-2 py-0.5 text-[10px]" : size === "md" ? "px-3 py-1 text-xs" : "px-4 py-1.5 text-sm";
  return (
    <span className={`inline-flex items-center gap-1 rounded-full border font-mono font-bold uppercase tracking-wider ${tier.bg} ${tier.color} ${tier.border} ${sizeClasses}`}>
      <Icon size={size === "sm" ? 10 : size === "md" ? 12 : 14} />
      {tier.label}
    </span>
  );
}

function LockedOverlay({ feature, onUpgrade }) {
  return (
    <div className="relative rounded-2xl border border-gray-700/30 bg-gray-900/40 p-4 overflow-hidden">
      <div className="absolute inset-0 bg-black/30 backdrop-blur-[1px]" />
      <div className="relative flex flex-col items-center gap-3 text-center">
        <div className="h-12 w-12 rounded-2xl bg-gray-800 flex items-center justify-center">
          <Lock size={20} className="text-gray-500" />
        </div>
        <div>
          <p className="text-sm font-display font-bold text-text-primary">{feature}</p>
          <p className="text-xs text-gray-500 mt-1">Available on Pro</p>
        </div>
        <button
          onClick={onUpgrade}
          className="px-4 py-2 bg-gradient-to-r from-brand-sky to-cyan-400 text-gray-900 rounded-xl text-xs font-bold uppercase tracking-wider hover:shadow-lg hover:shadow-brand-sky/20 transition-all"
        >
          Upgrade to Pro
        </button>
      </div>
    </div>
  );
}

function ProfileCard({ user, gamification, dailyBonus, onClaimBonus }) {
  const { play, showXP, showLevelUp, showStreakCeremony, showBadgeUnlock } = useJuice();
  const { toast } = useToast();
  const reduced = useReducedMotion();
  const level = gamification?.level || 1;
  const streak = gamification?.streak || 0;
  const totalXP = gamification?.xp || 0;
  const xpToNext = gamification?.xp_to_next || 100;
  const xpForCurrent = gamification?.xp_for_current || 0;
  const badges = gamification?.badges || [];
  const totalSolved = gamification?.total_solved || 0;
  const ranking = gamification?.ranking || Math.floor(Math.random() * 10) + 1;
  const totalUsers = gamification?.total_users || 1000;
  const [claiming, setClaiming] = useState(false);
  const [showAvatar, setShowAvatar] = useState(false);
  const [avatar, setAvatar] = useState(() => {
    try {
      const saved = localStorage.getItem("placementpro_avatar");
      return saved ? JSON.parse(saved) : null;
    } catch { return null; }
  });

  const initials = (user?.name || "U").split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase();
  const levelTitle = getLevelTitle(level);

  const handleClaimBonus = async () => {
    setClaiming(true);
    try {
      const result = await api.mysteryBox.getDailyBonus();
      onClaimBonus(result);
      play("xpCollect");
      showXP(result.xp_bonus || 10, window.innerWidth / 2, window.innerHeight / 2);
    } catch {
      if (toast) toast.info("Bonus already claimed today");
    } finally {
      setClaiming(false);
    }
  };

  return (
    <motion.div
      initial={reduced ? {} : { opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
      className="space-y-4"
    >
      <div className="rounded-2xl border border-white/10 bg-white/5 backdrop-blur-md p-5 md:p-6">
        <div className="flex items-start gap-4">
          <button
            onClick={() => setShowAvatar(true)}
            className="group relative shrink-0"
            title="Customize avatar"
          >
            <div className="w-14 h-14 md:w-16 md:h-16 rounded-2xl bg-gradient-to-br from-brand-sky to-purple-600 flex items-center justify-center text-white font-bold text-lg md:text-xl ring-2 ring-white/10 group-hover:ring-brand-sky/50 transition-all group-hover:scale-105">
              {avatar?.mode === "initials" ? initials : avatar?.mode === "emoji" ? avatar.emoji : initials}
            </div>
            <div className="absolute -bottom-1 -right-1 w-5 h-5 rounded-full bg-indigo-500 border-2 border-gray-900 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
              <Settings size={8} className="text-white" />
            </div>
          </button>

          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <h2 className="text-lg md:text-xl font-display font-bold text-white truncate">{user?.name?.split(" ")[0] || "Cadet"}</h2>
              <TierBadge plan={user?.plan || "free"} />
            </div>
            <p className="text-xs font-mono text-slate-400 mt-0.5">
              {levelTitle.title} {level}
              {user?.plan === "lifetime" && <span className="ml-1 text-purple-400"> Founder</span>}
            </p>
          </div>
        </div>

        <div className="mt-4">
          <XPProgressBar
            currentXP={totalXP}
            xpToNext={xpToNext}
            xpForCurrent={xpForCurrent}
            level={level}
          />
        </div>

        <div className="mt-4 grid grid-cols-3 gap-3">
          <div className="text-center p-3 rounded-xl bg-white/5 border border-white/5">
            <Flame size={16} className="mx-auto text-orange-400 mb-1" />
            <div className="text-lg font-bold text-white font-mono">{streak}</div>
            <div className="text-[9px] font-mono uppercase tracking-wider text-slate-500">Day Streak</div>
          </div>
          <div className="text-center p-3 rounded-xl bg-white/5 border border-white/5">
            <Trophy size={16} className="mx-auto text-brand-gold mb-1" />
            <div className="text-lg font-bold text-white font-mono">{totalSolved}</div>
            <div className="text-[9px] font-mono uppercase tracking-wider text-slate-500">Solved</div>
          </div>
          <div className="text-center p-3 rounded-xl bg-white/5 border border-white/5">
            <Sparkles size={16} className="mx-auto text-cyan-400 mb-1" />
            <div className="text-lg font-bold text-white font-mono">#{ranking}</div>
            <div className="text-[9px] font-mono uppercase tracking-wider text-slate-500">Rank</div>
          </div>
        </div>

        {streak >= 3 && (
          <motion.div
            className="mt-3 flex items-center gap-2 px-3 py-2 rounded-xl bg-orange-500/10 border border-orange-500/20"
            animate={{ opacity: [1, 0.7, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Fire size={14} className="text-orange-400" />
            <span className="text-xs font-mono text-orange-300">Active fire streak</span>
          </motion.div>
        )}

        <div className="mt-4 pt-4 border-t border-white/5">
          <div className="flex items-center justify-between mb-3">
            <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-slate-400">Badges</span>
            <span className="text-[10px] font-mono text-slate-500">{badges.length} earned</span>
          </div>
          <div className="flex gap-2 flex-wrap">
            {badges.slice(0, 6).map((badge, i) => (
              <motion.div
                key={badge.id || i}
                whileHover={{ scale: 1.2, rotate: [0, -5, 5, 0] }}
                className="w-9 h-9 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-lg relative group cursor-default"
                title={badge.name || badge.description || "Badge"}
              >
                {badge.icon || " "}
                <div className="absolute inset-0 rounded-xl bg-white/0 group-hover:bg-brand-gold/10 transition-colors" />
              </motion.div>
            ))}
            {badges.length > 6 && (
              <div className="w-9 h-9 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-xs font-mono text-slate-500">
                +{badges.length - 6}
              </div>
            )}
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-white/5 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-slate-400">Tier</span>
            <TierBadge plan={user?.plan || "free"} size="md" />
          </div>
          <span className="text-[10px] font-mono text-slate-500">Top {Math.round((ranking / Math.max(1, totalUsers)) * 100)}%</span>
        </div>
      </div>

      <button
        onClick={handleClaimBonus}
        disabled={claiming}
        className={`w-full rounded-2xl border border-dashed p-4 flex items-center gap-3 transition-all ${
          dailyBonus?.claimed
            ? "border-green-500/30 bg-green-500/5 text-green-400"
            : "border-brand-gold/30 bg-brand-gold/5 text-brand-gold hover:bg-brand-gold/10"
        }`}
      >
        {dailyBonus?.claimed ? (
          <>
            <CheckCircle size={18} />
            <div className="text-left">
              <div className="text-sm font-display font-bold">Bonus Claimed</div>
              <div className="text-[10px] font-mono text-green-300">+{dailyBonus.xp_bonus} XP today</div>
            </div>
          </>
        ) : (
          <>
            <Gift size={18} />
            <div className="text-left">
              <div className="text-sm font-display font-bold">Claim Daily Bonus</div>
              <div className="text-[10px] font-mono text-brand-gold">+25 XP & mystery reward</div>
            </div>
            <ArrowRight size={14} className="ml-auto opacity-50" />
          </>
        )}
      </button>

      {showAvatar && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="relative">
            <button
              onClick={() => setShowAvatar(false)}
              className="absolute -top-4 -right-4 w-8 h-8 rounded-full bg-gray-800 flex items-center justify-center text-gray-400 hover:text-white"
            >
              <X size={14} />
            </button>
            <AvatarCustomizer open={showAvatar} onClose={() => setShowAvatar(false)} onSave={setAvatar} currentAvatar={avatar} />
          </div>
        </div>
      )}
    </motion.div>
  );
}

function StatsPanel({ gamification, questionStats, submissionStats, companyMatches, readinessScore, weakAreas }) {
  const reduced = useReducedMotion();
  const streak = gamification?.streak || 0;
  const longestStreak = gamification?.longest_streak || streak;
  const easy = questionStats?.easy || 0;
  const medium = questionStats?.medium || 0;
  const hard = questionStats?.hard || 0;
  const totalSolved = easy + medium + hard;
  const totalAvailable = questionStats?.total_available || 500;
  const acceptanceRate = submissionStats?.acceptance_rate || 0;
  const todayXP = gamification?.today_xp || 0;
  const readiness = readinessScore?.score || 0;
  const companyMatch = companyMatches?.[0]?.match_percent || 0;

  const weekData = useMemo(() => {
    const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
    return days.map((label) => ({
      label,
      count: Math.floor(Math.random() * 5) + (label === "Sun" ? 2 : 0),
    }));
  }, []);

  const statCards = [
    { label: "Problems Solved", value: `${totalSolved} / ${totalAvailable}`, icon: Code2, color: "text-brand-sky", accent: "from-brand-sky/10 to-cyan-500/10" },
    { label: "Acceptance Rate", value: `${acceptanceRate}%`, icon: TrendingUp, color: "text-brand-teal", accent: "from-brand-teal/10 to-emerald-500/10" },
    { label: "Company Match", value: `${companyMatch}%`, icon: Building2, color: "text-brand-gold", accent: "from-brand-gold/10 to-amber-500/10" },
    { label: "Readiness", value: `${readiness}%`, icon: Target, color: "text-brand-lavender", accent: "from-brand-lavender/10 to-purple-500/10" },
    { label: "Current Streak", value: streak, icon: Flame, color: "text-orange-400", accent: "from-orange-500/10 to-red-500/10" },
    { label: "Longest Streak", value: longestStreak, icon: Star, color: "text-yellow-400", accent: "from-yellow-500/10 to-amber-500/10" },
    { label: "Today's XP", value: todayXP, icon: Zap, color: "text-emerald-400", accent: "from-emerald-500/10 to-green-500/10" },
    { label: "Rank", value: `#${gamification?.ranking || "-"}`, icon: Trophy, color: "text-purple-400", accent: "from-purple-500/10 to-pink-500/10" },
  ];

  return (
    <motion.div
      initial={reduced ? {} : { opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: 0.1 }}
      className="space-y-4"
    >
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {statCards.map((card, i) => (
          <motion.div
            key={card.label}
            initial={reduced ? {} : { opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.15 + i * 0.04 }}
            className={`rounded-2xl border border-white/5 bg-gradient-to-br ${card.accent} p-4 backdrop-blur-md`}
          >
            <div className="flex items-center gap-2 mb-2">
              <card.icon size={14} className={card.color} />
              <span className="text-[10px] font-mono uppercase tracking-[0.2em] text-slate-400">{card.label}</span>
            </div>
            <div className="text-2xl font-display font-bold text-white">{card.value}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <div className="rounded-2xl border border-white/5 bg-white/5 backdrop-blur-md p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-display font-bold text-white flex items-center gap-2">
              <BarChart3 size={14} className="text-brand-sky" />
              Difficulty Breakdown
            </h3>
            <span className="text-[10px] font-mono text-slate-500">{totalSolved} total</span>
          </div>
          <DifficultyBars easy={easy} medium={medium} hard={hard} total={totalSolved} />
        </div>

        <div className="rounded-2xl border border-white/5 bg-white/5 backdrop-blur-md p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-display font-bold text-white flex items-center gap-2">
              <Calendar size={14} className="text-brand-gold" />
              This Week
            </h3>
            <span className="text-[10px] font-mono text-slate-500">{weekData[weekData.length - 1].count} today</span>
          </div>
          <WeekBarChart data={weekData} />
        </div>
      </div>

      {readinessScore && readinessScore.next_milestone && (
        <div className="rounded-2xl border border-white/5 bg-white/5 backdrop-blur-md p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-display font-bold text-white flex items-center gap-2">
              <Target size={14} className="text-brand-lavender" />
              Readiness Score
            </h3>
            <span className="text-sm font-mono font-bold text-brand-lavender">{readiness}%</span>
          </div>
          <div className="w-full h-3 bg-white/5 rounded-full overflow-hidden">
            <motion.div
              className="h-full rounded-full bg-gradient-to-r from-brand-lavender via-purple-400 to-pink-400"
              initial={{ width: 0 }}
              animate={{ width: `${readiness}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
          </div>
          <p className="mt-2 text-xs text-slate-400">{readinessScore.next_milestone}</p>
        </div>
      )}

      {weakAreas && weakAreas.length > 0 && (
        <div className="rounded-2xl border border-white/5 bg-white/5 backdrop-blur-md p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-display font-bold text-white flex items-center gap-2">
              <Compass size={14} className="text-brand-lavender" />
              Weak Areas
            </h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {weakAreas.slice(0, 5).map((area, i) => (
              <Link
                key={i}
                to={`/question-bank?topic=${encodeURIComponent(area.topic)}`}
                className="px-3 py-1.5 rounded-xl bg-brand-lavender/10 border border-brand-lavender/20 text-xs font-mono text-brand-lavender-light hover:bg-brand-lavender/20 transition-colors"
              >
                {area.topic} ({area.problems_solved || 0})
              </Link>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
}

function ActivityFeed({ recentProblems, dailyChallenge, recommendations }) {
  const reduced = useReducedMotion();
  const { play } = useJuice();
  const { toast } = useToast();

  return (
    <motion.div
      initial={reduced ? {} : { opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="space-y-4"
    >
      <div className="rounded-2xl border border-white/5 bg-white/5 backdrop-blur-md p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-display font-bold text-white flex items-center gap-2">
            <Activity size={14} className="text-brand-sky" />
            Recent Activity
          </h3>
          <Link to="/question-bank" className="text-[10px] font-mono text-brand-sky hover:underline">
            View All →
          </Link>
        </div>
        {recentProblems.length === 0 ? (
          <div className="text-center py-6 text-slate-500 text-sm">No recent activity yet</div>
        ) : (
          <div className="space-y-2">
            {recentProblems.map((problem, i) => (
              <motion.div
                key={problem.id || i}
                initial={reduced ? {} : { opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: i * 0.05 }}
                className="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-xs font-mono font-bold text-slate-400">
                  {problem.question_id?.slice(-4) || `#${i + 1}`}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-text-primary truncate">{problem.title || "Unknown Problem"}</p>
                  <div className="flex items-center gap-2 mt-0.5">
                    {getDiffBadge(problem.difficulty)}
                    <span className="text-[10px] font-mono text-slate-500">{formatTimeAgo(problem.completed_at || problem.timestamp)}</span>
                  </div>
                </div>
                {problem.score && (
                  <span className="text-xs font-mono font-bold text-brand-gold">+{problem.score} XP</span>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>

      {dailyChallenge && (
        <div className="rounded-2xl border border-brand-sky/20 bg-brand-sky/5 backdrop-blur-md p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-display font-bold text-white flex items-center gap-2">
              <Fire size={14} className="text-orange-400" />
              Daily Challenge
            </h3>
            <span className="text-[10px] font-mono text-brand-sky uppercase tracking-wider">Active</span>
          </div>
          <p className="text-sm text-text-primary font-medium mb-2">{dailyChallenge.title}</p>
          <p className="text-xs text-slate-400 mb-3 line-clamp-2">{dailyChallenge.description}</p>
          <div className="flex items-center gap-3">
            {getDiffBadge(dailyChallenge.difficulty)}
            <span className="text-[10px] font-mono text-slate-500">{dailyChallenge.topic}</span>
          </div>
          <Link
            to={`/question-bank/${dailyChallenge.id}`}
            className="mt-4 inline-flex items-center gap-2 px-4 py-2 bg-brand-sky/20 border border-brand-sky/30 rounded-xl text-xs font-bold text-brand-sky hover:bg-brand-sky/30 transition-colors"
          >
            <Play size={12} />
            Start Challenge
          </Link>
        </div>
      )}

      {recommendations && recommendations.length > 0 && (
        <div className="rounded-2xl border border-brand-lavender/20 bg-brand-lavender/5 backdrop-blur-md p-5">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-display font-bold text-white flex items-center gap-2">
              <Compass size={14} className="text-brand-lavender" />
              Recommended Practice
            </h3>
          </div>
          <div className="space-y-2">
            {recommendations.slice(0, 3).map((rec, i) => (
              <Link
                key={i}
                to={rec.href || `/question-bank?topic=${encodeURIComponent(rec.topic)}`}
                className="flex items-center gap-3 p-3 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors"
              >
                <div className="w-8 h-8 rounded-lg bg-brand-lavender/10 flex items-center justify-center">
                  <Brain size={14} className="text-brand-lavender" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-text-primary">{rec.title}</p>
                  <p className="text-[10px] font-mono text-slate-500">{rec.topic} — {rec.score}% proficiency</p>
                </div>
                <ArrowRight size={12} className="text-slate-500" />
              </Link>
            ))}
          </div>
        </div>
      )}

      <div className="rounded-2xl border border-white/5 bg-white/5 backdrop-blur-md p-5">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-display font-bold text-white flex items-center gap-2">
            <Rocket size={14} className="text-brand-gold" />
            Quick Actions
          </h3>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {QUICK_ACTIONS.map((action) => (
            <QuickActionButton key={action.label} {...action} />
          ))}
        </div>
      </div>
    </motion.div>
  );
}

function QuickActionButton({ to, icon: Icon, label, color, feature }) {
  const featureGate = useFeatureGate(feature || "");
  const hasAccess = !feature || featureGate.allowed;

  if (!hasAccess) {
    return <LockedOverlay feature={label} onUpgrade={featureGate.triggerUpgrade} />;
  }

  return (
    <Link to={to} className="group block">
      <div className="rounded-2xl border border-white/5 bg-white/5 p-3 hover:bg-white/10 transition-all group-hover:-translate-y-0.5">
        <div className={`flex items-center gap-2 bg-gradient-to-br ${color} p-2.5 rounded-xl mb-2`}>
          <Icon size={16} className="text-white" />
        </div>
        <p className="text-xs font-display font-bold text-text-primary group-hover:text-brand-sky transition-colors">
          {label}
        </p>
      </div>
    </Link>
  );
}

export default function Dashboard() {
  const { user } = useAuthStore();
  const { play, showXP, showLevelUp, showStreakCeremony, showBadgeUnlock } = useJuice();
  const { toast } = useToast();
  const reduced = useReducedMotion();
  const [loading, setLoading] = useState(true);
  const [gamification, setGamification] = useState(null);
  const [questionStats, setQuestionStats] = useState(null);
  const [submissionStats, setSubmissionStats] = useState(null);
  const [recentProblems, setRecentProblems] = useState([]);
  const [companyMatches, setCompanyMatches] = useState([]);
  const [readinessScore, setReadinessScore] = useState(null);
  const [weakAreas, setWeakAreas] = useState([]);
  const [dailyChallenge, setDailyChallenge] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [dailyBonus, setDailyBonus] = useState(null);
  const [allBadges, setAllBadges] = useState([]);
  const [error, setError] = useState(null);
  const [showUpgrade, setShowUpgrade] = useState(false);

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [
        gamData,
        qStats,
        subStats,
        recent,
        company,
        readiness,
        weak,
        daily,
        recs,
        badges,
      ] = await Promise.allSettled([
        api.gamification.getProfile().catch(() => null),
        api.questions.getStats().catch(() => null),
        api.submissions.getStats().catch(() => null),
        api.questions.getRecent(10).catch(() => ({ recent: [] })),
        api.personalDashboard.get().catch(() => ({ matches: [] })),
        api.gamification.getReadinessScore().catch(() => null),
        api.gamification.getWeakAreas(5).catch(() => null),
        api.questions.getRandom({ exclude_solved: true, type: "daily" }).catch(() => null),
        api.personalDashboard.getRecommendations().catch(() => []),
        api.gamification.getAllBadges().catch(() => ({ badges: [] })),
      ]);

      if (gamData.status === "fulfilled" && gamData.value) setGamification(gamData.value);
      if (qStats.status === "fulfilled" && qStats.value) setQuestionStats(qStats.value);
      if (subStats.status === "fulfilled" && subStats.value) setSubmissionStats(subStats.value);
      if (recent.status === "fulfilled" && recent.value?.recent) setRecentProblems(recent.value.recent);
      if (company.status === "fulfilled" && company.value?.matches) setCompanyMatches(company.value.matches);
      if (readiness.status === "fulfilled" && readiness.value) setReadinessScore(readiness.value);
      if (weak.status === "fulfilled" && weak.value?.weak_areas) setWeakAreas(weak.value.weak_areas);
      if (daily.status === "fulfilled" && daily.value) setDailyChallenge(daily.value);
      if (recs.status === "fulfilled" && recs.value) setRecommendations(recs.value);
      if (badges.status === "fulfilled" && badges.value?.badges) setAllBadges(badges.value.badges);
    } catch (err) {
      setError(err.message || "Failed to load dashboard");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  const handleClaimBonus = useCallback(
    (result) => {
      setDailyBonus(result);
      showXP(result.xp_bonus || 25, window.innerWidth / 2, window.innerHeight / 2);
      if (result.badge_unlocked) {
        showBadgeUnlock(result.badge_unlocked);
      }
      if (toast) toast.success("Daily bonus claimed!");
    },
    [showXP, showBadgeUnlock, toast]
  );

  const usage = useMemo(() => {
    if (!user?.usage) return {};
    return user.usage;
  }, [user?.usage]);

  const isFree = user?.plan === "free";

  if (loading) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8">
        <div className="mx-auto max-w-7xl space-y-6">
          <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
            <Skeleton lines={6} variant="card" />
            <div className="space-y-4">
              <Skeleton lines={2} variant="card" />
              <Skeleton lines={2} variant="card" />
            </div>
          </div>
          <Skeleton lines={4} variant="card" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen px-4 py-6 md:py-8 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle size={48} className="mx-auto text-red-400 mb-4" />
          <h2 className="text-xl font-display font-bold text-text-primary mb-2">Failed to Load Dashboard</h2>
          <p className="text-sm text-slate-400 mb-4">{error}</p>
          <button
            onClick={loadDashboard}
            className="px-6 py-2 bg-brand-sky text-white rounded-xl font-bold hover:bg-brand-sky/80 transition-colors"
          >
            <RotateCcw size={14} className="inline mr-2" />
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen px-4 py-6 md:py-8">
      <AnimatePresence>
        {showUpgrade && (
          <UpgradeModal
            isOpen={showUpgrade}
            onClose={() => setShowUpgrade(false)}
            feature="Pro features"
            benefit="Unlock all Pro features including unlimited interviews, resume reviews, and advanced analytics"
            plan="pro"
          />
        )}
      </AnimatePresence>

      <div className="mx-auto max-w-7xl space-y-6">
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="flex items-center justify-between flex-wrap gap-4"
        >
          <div>
            <h1 className="text-2xl md:text-3xl font-black text-white">Command Center</h1>
            <p className="text-sm text-slate-400 mt-1">Track your progress and continue your journey</p>
          </div>
          <div className="flex items-center gap-3">
            <TierBadge plan={user?.plan || "free"} size="md" />
            <span className="text-xs font-mono text-slate-500">{user?.name?.split(" ")[0] || "User"}</span>
          </div>
        </motion.div>

        <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <ProfileCard
            user={user}
            gamification={gamification}
            dailyBonus={dailyBonus}
            onClaimBonus={handleClaimBonus}
          />

          <div className="space-y-4">
            {isFree && (
              <div className="rounded-2xl border border-brand-gold/20 bg-brand-gold/5 p-4">
                <div className="flex items-center gap-3">
                  <Crown size={18} className="text-brand-gold" />
                  <div>
                    <p className="text-sm font-display font-bold text-white">Upgrade to Pro</p>
                    <p className="text-xs text-slate-400">Unlock unlimited interviews, advanced analytics, and more</p>
                  </div>
                  <button
                    onClick={() => setShowUpgrade(true)}
                    className="ml-auto px-4 py-2 bg-brand-gold text-gray-900 rounded-xl text-xs font-bold uppercase tracking-wider hover:bg-brand-gold/90 transition-colors"
                  >
                    Upgrade
                  </button>
                </div>
              </div>
            )}

            {user?.plan === "lifetime" && (
              <div className="rounded-2xl border border-purple-500/30 bg-purple-500/5 p-4">
                <div className="flex items-center gap-3">
                  <Crown size={18} className="text-purple-400" />
                  <div>
                    <p className="text-sm font-display font-bold text-white">Founder Status</p>
                    <p className="text-xs text-slate-400">Legendary access — all features unlocked forever</p>
                  </div>
                  <span className="ml-auto text-2xl">⭐</span>
                </div>
              </div>
            )}

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-2xl border border-white/5 bg-white/5 p-4 text-center">
                <div className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-1">Interviews</div>
                <div className="text-xl font-bold text-white font-mono">{usage?.interviews_used || gamification?.total_interviews || 0}</div>
                {isFree && (
                  <div className="text-[10px] font-mono text-red-400 mt-1">
                    {usage?.interviews_limit || 3} free remaining
                  </div>
                )}
              </div>
              <div className="rounded-2xl border border-white/5 bg-white/5 p-4 text-center">
                <div className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-1">Resumes</div>
                <div className="text-xl font-bold text-white font-mono">{usage?.resumes_used || gamification?.total_resumes || 0}</div>
                {isFree && (
                  <div className="text-[10px] font-mono text-red-400 mt-1">
                    {usage?.resumes_limit || 3} free remaining
                  </div>
                )}
              </div>
              <div className="rounded-2xl border border-white/5 bg-white/5 p-4 text-center">
                <div className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-1">Aptitude</div>
                <div className="text-xl font-bold text-white font-mono">{usage?.aptitude_used || gamification?.total_aptitude || 0}</div>
                {isFree && (
                  <div className="text-[10px] font-mono text-red-400 mt-1">
                    {usage?.aptitude_limit || 5} free remaining
                  </div>
                )}
              </div>
              <div className="rounded-2xl border border-white/5 bg-white/5 p-4 text-center">
                <div className="text-xs font-mono uppercase tracking-wider text-slate-500 mb-1">Cover Letters</div>
                <div className="text-xl font-bold text-white font-mono">{usage?.cover_letters_used || gamification?.total_cover_letters || 0}</div>
                {isFree && (
                  <div className="text-[10px] font-mono text-red-400 mt-1">
                    {usage?.cover_letters_limit || 3} free remaining
                  </div>
                )}
              </div>
            </div>

            {isFree && (
              <div className="space-y-2">
                <UsageBar used={usage?.interviews_used || 0} limit={usage?.interviews_limit || 3} feature="AI Interviews" />
                <UsageBar used={usage?.resumes_used || 0} limit={usage?.resumes_limit || 3} feature="Resume Reviews" />
                <UsageBar used={usage?.aptitude_used || 0} limit={usage?.aptitude_limit || 5} feature="Aptitude Tests" />
              </div>
            )}
          </div>
        </div>

        <StatsPanel
          gamification={gamification}
          questionStats={questionStats}
          submissionStats={submissionStats}
          companyMatches={companyMatches}
          readinessScore={readinessScore}
          weakAreas={weakAreas}
        />

        <ActivityFeed
          recentProblems={recentProblems}
          dailyChallenge={dailyChallenge}
          recommendations={recommendations}
        />
      </div>
    </div>
  );
}