import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import useReducedMotion from "../hooks/useReducedMotion";
import DailyReward from "../components/DailyReward";
import {
  Code2, Sword, Trophy, Bot, Route, Target,
  BookOpen, Flame, Zap, Sparkles, ChevronRight,
  Star, Compass, GraduationCap, Layers, Shield,
  Brain, Puzzle, BarChart3, Clock, TrendingUp,
  CheckCircle2, ArrowRight, Play, Gamepad2,
  Lightbulb, Rocket, Medal, Crown, Gem,
} from "lucide-react";

const QUICK_STATS = [
  { label: "XP", icon: Zap, color: "text-amber-700", bg: "bg-amber-100" },
  { label: "Streak", icon: Flame, color: "text-orange-600", bg: "bg-orange-100" },
  { label: "Solved", icon: CheckCircle2, color: "text-emerald-700", bg: "bg-emerald-100" },
  { label: "Level", icon: Crown, color: "text-purple-600", bg: "bg-purple-100" },
];

const QUICK_ACTIONS = [
  { to: "/daily-challenge", icon: Flame, label: "Daily Challenge", desc: "Solve today's problem", color: "from-orange-500 to-red-500" },
  { to: "/learn", icon: BookOpen, label: "Continue Learning", desc: "Resume your last lesson", color: "from-blue-500 to-indigo-500" },
  { to: "/interview", icon: Target, label: "Mock Interview", desc: "Practice with AI interviewer", color: "from-emerald-500 to-teal-500" },
  { to: "/journeys", icon: Route, label: "Learning Journeys", desc: "Follow a curated path", color: "from-purple-500 to-pink-500" },
  { to: "/challenge-packs", icon: Sword, label: "Challenge Packs", desc: "Collect and solve cards", color: "from-amber-500 to-orange-500" },
  { to: "/ai-mentor", icon: Bot, label: "AI Mentor", desc: "Get help with code", color: "from-cyan-500 to-blue-500" },
  { to: "/tower", icon: Trophy, label: "Placement Tower", desc: "Climb the ranks", color: "from-violet-500 to-purple-500" },
  { to: "/dsa-visualizer", icon: BarChart3, label: "DSA Visualizer", desc: "Watch algorithms in action", color: "from-pink-500 to-rose-500" },
  { to: "/playground", icon: Code2, label: "Code Playground", desc: "Build and experiment", color: "from-indigo-500 to-violet-500" },
];

const DSA_DOMAINS = [
  { name: "Arrays", progress: 75, color: "from-blue-500 to-cyan-500" },
  { name: "Strings", progress: 60, color: "from-emerald-500 to-teal-500" },
  { name: "Trees", progress: 40, color: "from-amber-500 to-yellow-500" },
  { name: "DP", progress: 25, color: "from-purple-500 to-pink-500" },
  { name: "Graphs", progress: 35, color: "from-red-500 to-orange-500" },
];

const RECENT_ACTIVITY = [
  { type: "solved", problem: "Two Sum", xp: 25, time: "2h ago", color: "emerald" },
  { type: "lesson", problem: "Python Loops", xp: 10, time: "4h ago", color: "blue" },
  { type: "interview", problem: "SDE Mock", xp: 50, time: "1d ago", color: "purple" },
];

const RECENT_COLORS = {
  emerald: { chip: "bg-emerald-100 border-emerald-200", text: "text-emerald-700" },
  blue: { chip: "bg-sky-100 border-sky-200", text: "text-sky-700" },
  purple: { chip: "bg-purple-100 border-purple-200", text: "text-purple-700" },
};

export default function CommandCenter() {
  const store = useAuthStore();
  const reduced = useReducedMotion();
  const [stats, setStats] = useState({ xp: 0, streak: 0, solved: 0, level: 1 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadStats = async () => {
      try {
        const profile = await api.getProfileStats();
        setStats({
          xp: profile.xp || 0,
          streak: profile.streak || 0,
          solved: profile.total_solved || 0,
          level: profile.level || 1,
        });
      } catch {
        const g = store.user?.gamification || {};
        setStats({ xp: Number(g.xp) || 0, streak: Number(g.streak) || 0, solved: Number(g.total_solved) || 0, level: Number(g.level) || 1 });
      } finally { setLoading(false); }
    };
    loadStats();
  }, []);

  const STAT_VALUES = [stats.xp, stats.streak, stats.solved, stats.level];

  return (
    <div className="relative min-h-screen">
      <div className="max-w-6xl mx-auto px-4 py-6 pb-24 md:pb-8">
        <motion.div initial={reduced ? {} : { opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl md:text-4xl font-bold text-text-primary flex items-center gap-3">
                Command Center
                <span className="text-base px-3 py-1 rounded-full bg-[#EEF5E7] text-nature-blossom border border-nature-bark font-mono text-xs">
                  Lv.{stats.level}
                </span>
              </h1>
              <p className="text-text-muted text-sm mt-1">Your hub for coding and placement prep</p>
            </div>
            <Link to="/profile" className="hidden md:flex items-center gap-2 px-4 py-2 rounded-xl bg-[#EEF5E7] border border-nature-bark hover:border-[#7BB661]/60 text-text-secondary text-sm transition-all">
              <User className="w-4 h-4" /> Profile
            </Link>
          </div>
        </motion.div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
          {QUICK_STATS.map((stat, idx) => {
            const val = loading ? "..." : STAT_VALUES[idx];
            return (
              <motion.div key={stat.label}
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.07 }}
                className="bg-white border border-nature-leaf/20 rounded-2xl p-4 flex items-center gap-3 shadow-[0_1px_2px_rgba(31,41,55,0.04),0_10px_24px_-14px_rgba(31,41,55,0.12)]"
              >
                <div className={`p-2.5 rounded-xl ${stat.bg} ${stat.color}`}>
                  <stat.icon className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-xl font-bold text-text-primary font-mono">{val}</div>
                  <div className="text-[10px] text-text-muted font-medium uppercase tracking-wider">{stat.label}</div>
                </div>
              </motion.div>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
              <h2 className="text-sm font-semibold text-text-muted uppercase tracking-wider mb-4 flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-600" /> Quick Actions
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {QUICK_ACTIONS.map((action, idx) => (
                  <Link key={action.to} to={action.to}>
                    <motion.div
                      initial={reduced ? {} : { opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.2 + idx * 0.04 }}
                      className="group bg-white border border-nature-leaf/20 rounded-2xl p-4 shadow-[0_1px_2px_rgba(31,41,55,0.04),0_10px_24px_-14px_rgba(31,41,55,0.10)] transition-all duration-150 hover:-translate-y-0.5 hover:border-[#7BB661]/50"
                    >
                      <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${action.color} flex items-center justify-center mb-3 shadow-lg`}>
                        <action.icon className="w-5 h-5 text-text-primary" />
                      </div>
                      <h3 className="font-semibold text-sm text-text-primary group-hover:text-nature-blossom transition-colors">{action.label}</h3>
                      <p className="text-[10px] text-text-muted mt-0.5">{action.desc}</p>
                    </motion.div>
                  </Link>
                ))}
              </div>
            </motion.div>

            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
              className="bg-white border border-nature-leaf/20 rounded-2xl p-5 shadow-[0_1px_2px_rgba(31,41,55,0.04),0_10px_24px_-14px_rgba(31,41,55,0.10)]">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-text-secondary flex items-center gap-2">
                  <Brain className="w-4 h-4 text-nature-blossom" /> DSA Fingerprint
                </h2>
                <Link to="/fingerprint" className="text-xs text-nature-blossom hover:text-nature-blossom transition-colors">View all →</Link>
              </div>
              <div className="space-y-3">
                {DSA_DOMAINS.map((domain) => (
                  <div key={domain.name} className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-text-muted">{domain.name}</span>
                      <span className="font-mono text-text-muted">{domain.progress}%</span>
                    </div>
                    <div className="h-1.5 bg-[#EEF5E7] rounded-full overflow-hidden">
                      <motion.div
                        className={`h-full rounded-full bg-gradient-to-r ${domain.color}`}
                        initial={{ width: 0 }}
                        animate={{ width: `${domain.progress}%` }}
                        transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>

          <div className="space-y-5">
            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
              className="bg-white border border-nature-leaf/20 rounded-2xl p-5 shadow-[0_1px_2px_rgba(31,41,55,0.04),0_10px_24px_-14px_rgba(31,41,55,0.10)]">
              <h3 className="text-sm font-semibold text-text-secondary mb-4 flex items-center gap-2">
                <Clock className="w-4 h-4 text-nature-blossom" /> Today's Progress
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs text-text-muted">
                  <span>Daily goal</span>
                  <span className="font-mono text-text-muted">0/5</span>
                </div>
                <div className="h-2 bg-[#EEF5E7] rounded-full overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: "0%" }}
                    className="h-full rounded-full bg-gradient-to-r from-[#4F8F57] to-[#7BB661]" />
                </div>
                <div className="text-center text-xs text-text-muted pt-2">
                  Complete 5 activities today for a <span className="text-amber-600 font-semibold">streak bonus</span>
                </div>
              </div>
            </motion.div>

            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
              className="bg-white border border-nature-leaf/20 rounded-2xl p-5 shadow-[0_1px_2px_rgba(31,41,55,0.04),0_10px_24px_-14px_rgba(31,41,55,0.10)]">
              <DailyReward currentDay={1} claimedDays={[]} onClaim={(d) => {}} />
            </motion.div>

            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}
              className="bg-white border border-nature-leaf/20 rounded-2xl p-5 shadow-[0_1px_2px_rgba(31,41,55,0.04),0_10px_24px_-14px_rgba(31,41,55,0.10)]">
              <h3 className="text-sm font-semibold text-text-secondary mb-4 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-nature-blossom" /> Recent Activity
              </h3>
              <div className="space-y-3">
                {RECENT_ACTIVITY.map((activity, i) => {
                  const tone = RECENT_COLORS[activity.color] || RECENT_COLORS.emerald;
                  return (
                    <div key={i} className="flex items-center gap-3 text-xs">
                      <div className={`w-7 h-7 rounded-lg ${tone.chip} border flex items-center justify-center`}>
                        {activity.type === "solved" ? <CheckCircle2 className={`w-3.5 h-3.5 ${tone.text}`} /> :
                         activity.type === "lesson" ? <BookOpen className={`w-3.5 h-3.5 ${tone.text}`} /> :
                         <Target className={`w-3.5 h-3.5 ${tone.text}`} />}
                      </div>
                      <div className="flex-1 min-w-0">
                        <span className="text-text-primary truncate block">{activity.problem}</span>
                        <span className="text-text-muted font-mono">{activity.time}</span>
                      </div>
                      <span className="font-mono text-amber-600 font-medium">+{activity.xp}</span>
                    </div>
                  );
                })}
              </div>
            </motion.div>
          </div>
        </div>

        <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
          className="mt-8 bg-gradient-to-r from-[#EEF5E7]/80 via-[#FAFAF6] to-[#F5EEDD]/80 border border-nature-bark rounded-2xl p-6 text-center">
          <p className="text-sm text-text-secondary mb-3">
            <span className="font-semibold text-text-primary">Pro Tip:</span> Follow a <Link to="/journeys" className="text-nature-blossom hover:text-nature-blossom underline">Learning Journey</Link> to stay on track. Complete daily challenges to build your streak!
          </p>
          <Link to="/journeys" className="inline-flex items-center gap-2 px-5 py-2.5 bg-nature-leaf hover:bg-nature-moss text-text-primary rounded-full text-sm font-medium transition-all shadow-[0_10px_24px_-10px_rgba(79,143,87,0.5)]">
            Explore Journeys <ArrowRight className="w-4 h-4" />
          </Link>
        </motion.div>
      </div>
    </div>
  );
}

function User(props) {
  return (
    <svg {...props} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}
