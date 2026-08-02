import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import api from "../services/api";
import useAuthStore from "../store/authStore";
import useReducedMotion from "../hooks/useReducedMotion";
import RPGPageLayout from "../components/space/RPGPageLayout";
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
  { label: "XP", icon: Zap, color: "text-amber-400", bg: "bg-amber-500/10" },
  { label: "Streak", icon: Flame, color: "text-orange-400", bg: "bg-orange-500/10" },
  { label: "Solved", icon: CheckCircle2, color: "text-emerald-400", bg: "bg-emerald-500/10" },
  { label: "Level", icon: Crown, color: "text-purple-400", bg: "bg-purple-500/10" },
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
        // Use auth store fallback
        const g = store.user?.gamification || {};
        setStats({ xp: g.xp || 0, streak: g.streak || 0, solved: g.total_solved || 0, level: g.level || 1 });
      } finally { setLoading(false); }
    };
    loadStats();
  }, []);

  const STAT_VALUES = [stats.xp, stats.streak, stats.solved, stats.level];

  return (
    <RPGPageLayout theme="dark" gridVariant="dots" gradient="from-indigo-950/30 via-slate-950 to-purple-950/30">
      <div className="max-w-6xl mx-auto px-4 py-6 pb-24 md:pb-8">
        {/* Welcome Header */}
        <motion.div initial={reduced ? {} : { opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl md:text-4xl font-bold text-white flex items-center gap-3">
                Command Center
                <span className="text-base px-3 py-1 rounded-full bg-indigo-500/15 text-indigo-400 border border-indigo-500/30 font-mono text-xs">
                  Lv.{stats.level}
                </span>
              </h1>
              <p className="text-slate-400 text-sm mt-1">Your hub for coding and placement prep</p>
            </div>
            <Link to="/profile" className="hidden md:flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800/50 border border-slate-700/50 hover:border-slate-600/50 text-slate-300 text-sm transition-all">
              <User className="w-4 h-4" /> Profile
            </Link>
          </div>
        </motion.div>

        {/* Quick Stats Row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
          {QUICK_STATS.map((stat, idx) => {
            const val = loading ? "..." : STAT_VALUES[idx];
            return (
              <motion.div key={stat.label}
                initial={reduced ? {} : { opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.07 }}
                className="bg-slate-900/70 border border-slate-800/80 rounded-xl p-4 flex items-center gap-3 hover:border-slate-700/80 transition-colors"
              >
                <div className={`p-2.5 rounded-lg ${stat.bg} ${stat.color}`}>
                  <stat.icon className="w-5 h-5" />
                </div>
                <div>
                  <div className="text-xl font-bold text-white font-mono">{val}</div>
                  <div className="text-[10px] text-slate-500 font-medium uppercase tracking-wider">{stat.label}</div>
                </div>
              </motion.div>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Actions Grid */}
            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
              <h2 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" /> Quick Actions
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                {QUICK_ACTIONS.map((action, idx) => (
                  <Link key={action.to} to={action.to}>
                    <motion.div
                      initial={reduced ? {} : { opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.2 + idx * 0.04 }}
                      className="group bg-slate-900/60 border border-slate-800/60 rounded-xl p-4 hover:bg-slate-800/60 hover:border-slate-700/60 transition-all duration-200 hover:-translate-y-0.5"
                    >
                      <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${action.color} bg-opacity-20 flex items-center justify-center mb-3 shadow-lg`}>
                        <action.icon className="w-5 h-5 text-white" />
                      </div>
                      <h3 className="font-semibold text-sm text-white group-hover:text-indigo-300 transition-colors">{action.label}</h3>
                      <p className="text-[10px] text-slate-500 mt-0.5">{action.desc}</p>
                    </motion.div>
                  </Link>
                ))}
              </div>
            </motion.div>

            {/* DSA Skill Progress */}
            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
              className="bg-slate-900/60 border border-slate-800/60 rounded-xl p-5">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-sm font-semibold text-slate-300 flex items-center gap-2">
                  <Brain className="w-4 h-4 text-indigo-400" /> DSA Fingerprint
                </h2>
                <Link to="/fingerprint" className="text-xs text-indigo-400 hover:text-indigo-300 transition-colors">View all →</Link>
              </div>
              <div className="space-y-3">
                {DSA_DOMAINS.map((domain) => (
                  <div key={domain.name} className="space-y-1">
                    <div className="flex items-center justify-between text-xs">
                      <span className="text-slate-400">{domain.name}</span>
                      <span className="font-mono text-slate-500">{domain.progress}%</span>
                    </div>
                    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
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

          {/* Right Sidebar */}
          <div className="space-y-5">
            {/* Today's Progress */}
            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}
              className="bg-slate-900/60 border border-slate-800/60 rounded-xl p-5">
              <h3 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
                <Clock className="w-4 h-4 text-cyan-400" /> Today's Progress
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span>Daily goal</span>
                  <span className="font-mono text-slate-500">0/5</span>
                </div>
                <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                  <motion.div initial={{ width: 0 }} animate={{ width: "0%" }}
                    className="h-full rounded-full bg-gradient-to-r from-cyan-500 to-blue-500" />
                </div>
                <div className="text-center text-xs text-slate-500 pt-2">
                  Complete 5 activities today for a <span className="text-amber-400 font-semibold">streak bonus</span>
                </div>
              </div>
            </motion.div>

            {/* Daily Rewards */}
            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
              className="bg-slate-900/60 border border-slate-800/60 rounded-xl p-5">
              <DailyReward currentDay={1} claimedDays={[]} onClaim={(d) => {}} />
            </motion.div>

            {/* Recent Activity */}
            <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.35 }}
              className="bg-slate-900/60 border border-slate-800/60 rounded-xl p-5">
              <h3 className="text-sm font-semibold text-slate-300 mb-4 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" /> Recent Activity
              </h3>
              <div className="space-y-3">
                {RECENT_ACTIVITY.map((activity, i) => (
                  <div key={i} className="flex items-center gap-3 text-xs">
                    <div className={`w-7 h-7 rounded-lg bg-${activity.color}-500/10 border border-${activity.color}-500/20 flex items-center justify-center`}>
                      {activity.type === "solved" ? <CheckCircle2 className={`w-3.5 h-3.5 text-${activity.color}-400`} /> :
                       activity.type === "lesson" ? <BookOpen className={`w-3.5 h-3.5 text-${activity.color}-400`} /> :
                       <Target className={`w-3.5 h-3.5 text-${activity.color}-400`} />}
                    </div>
                    <div className="flex-1 min-w-0">
                      <span className="text-slate-300 truncate block">{activity.problem}</span>
                      <span className="text-slate-600 font-mono">{activity.time}</span>
                    </div>
                    <span className="font-mono text-amber-400 font-medium">+{activity.xp}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>

        {/* Bottom Banner */}
        <motion.div initial={reduced ? {} : { opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
          className="mt-8 bg-gradient-to-r from-indigo-600/10 via-purple-600/10 to-pink-600/10 border border-indigo-500/20 rounded-2xl p-6 text-center">
          <p className="text-sm text-slate-300 mb-3">
            🚀 <span className="font-semibold text-white">Pro Tip:</span> Follow a <Link to="/journeys" className="text-indigo-400 hover:text-indigo-300 underline">Learning Journey</Link> to stay on track. Complete daily challenges to build your streak!
          </p>
          <Link to="/journeys" className="inline-flex items-center gap-2 px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-sm font-medium transition-all shadow-lg shadow-indigo-600/20">
            Explore Journeys <ArrowRight className="w-4 h-4" />
          </Link>
        </motion.div>
      </div>
    </RPGPageLayout>
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
