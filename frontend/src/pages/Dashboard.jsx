import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import api from "../services/api";
import { Bot, FileText, Target, Brain, Layers, Building2, Code, BarChart3, Flame, Trophy, Users, TrendingUp, Zap, GraduationCap, Lock, User, Briefcase, Snowflake, CheckCircle2, Sparkles, BookOpen, Sword, Shield, Rocket, Compass } from "lucide-react";
import SkillRadar from "../components/SkillRadar";
import StaggerContainer, { StaggerItem } from "../components/motion/StaggerContainer";
import AnimatedNumber from "../components/motion/AnimatedNumber";
import useReducedMotion from "../hooks/useReducedMotion";
import { DailyGoal, StreakFreeze } from "../components/tower";
import UsageBar from "../components/UsageBar";

const features = [
  { title: "Daily Drill", desc: "5 quick questions to keep your streak alive", icon: Flame, color: "bg-cyber-amber/10 text-cyber-amber border-cyber-amber/20", link: "/daily-drill", highlight: true },
  { title: "AI Interview", desc: "Mock interviews with real-time feedback", icon: Bot, color: "bg-cyber-blue/10 text-cyber-blue border-cyber-blue/20", link: "/interview" },
  { title: "System Design", desc: "Practice system design interviews", icon: Layers, color: "bg-cyber-purple/10 text-cyber-purple border-cyber-purple/20", link: "/system-design" },
  { title: "Coding", desc: "Timed coding problems with hyperdrive", icon: Code, color: "bg-cyber-green/10 text-cyber-green border-cyber-green/20", link: "/coding" },
  { title: "Company Intel", desc: "FAANG guides & behavioral Qs", icon: Building2, color: "bg-cyan-500/10 text-cyan-400 border-cyan-400/20", link: "/company-prep" },
  { title: "Hull Builder", desc: "Create ATS-optimized resumes", icon: FileText, color: "bg-cyber-green/10 text-emerald-400 border-emerald-400/20", link: "/resume" },
  { title: "Hull Scanner", desc: "Match resume to job descriptions", icon: Target, color: "bg-cyber-amber/10 text-cyber-amber border-cyber-amber/20", link: "/ats" },
  { title: "Aptitude Tests", desc: "Quant, logical, verbal MCQs", icon: Brain, color: "bg-fuchsia-500/10 text-fuchsia-400 border-fuchsia-400/20", link: "/aptitude" },
];

const quickLinks = [
  { to: "/daily-drill", icon: Flame, label: "Drill", color: "text-cyber-amber border-cyber-amber/20 hover:bg-cyber-amber/5" },
  { to: "/tower", icon: Trophy, label: "Tower", color: "text-cyber-purple border-cyber-purple/20 hover:bg-cyber-purple/5" },
  { to: "/problems", icon: Code, label: "Practice", color: "text-cyber-blue border-cyber-blue/20 hover:bg-cyber-blue/5" },
  { to: "/leaderboard", icon: Trophy, label: "Ranks", color: "text-cyber-green border-cyber-green/20 hover:bg-cyber-green/5" },
  { to: "/predictor", icon: TrendingUp, label: "Predictor", color: "text-teal-400 border-teal-400/20 hover:bg-teal-400/5" },
  { to: "/company-mocks", icon: Building2, label: "Mocks", color: "text-blue-400 border-blue-400/20 hover:bg-blue-400/5" },
  { to: "/resume", icon: FileText, label: "Resume", color: "text-emerald-400 border-emerald-400/20 hover:bg-emerald-400/5" },
  { to: "/ats", icon: Target, label: "ATS", color: "text-cyber-amber border-cyber-amber/20 hover:bg-cyber-amber/5" },
];

export default function Dashboard() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState({ interviews: 0, resumes: 0, aptitude: 0, questions: 0, coding: 0 });
  const [gamification, setGamification] = useState(null);
  const [weakAreas, setWeakAreas] = useState([]);
  const [loading, setLoading] = useState(true);
  const reduced = useReducedMotion();

  useEffect(() => {
    const loadStats = async () => {
      setLoading(true);
      try {
        const [interviewData, resumeData, aptitudeData, gamData, weakData] = await Promise.all([
          api.get("/api/interview/history").catch(() => ({ interviews: [] })),
          api.get("/api/resume/history").catch(() => ({ resumes: [] })),
          api.get("/api/aptitude/history").catch(() => ({ tests: [] })),
          api.getTower().catch(() => null),
          api.get("/api/gamification/skills/weak").catch(() => null),
        ]);
        setStats({
          interviews: interviewData.interviews.length,
          resumes: resumeData.resumes.length,
          aptitude: aptitudeData.tests.length,
          questions: 0,
          coding: 0,
        });
        setGamification(gamData);
        if (weakData && weakData.weak_areas) {
          setWeakAreas(weakData.weak_areas);
        }
      } catch {
      } finally {
        setLoading(false);
      }
    };
    loadStats();
  }, []);

  const usage = user?.usage || {};
  const isPremium = user?.plan === "pro" || user?.plan === "lifetime";
  const level = gamification?.level || 1;
  const streak = gamification?.streak || 0;
  const xp = gamification?.xp || 0;
  const xpToNext = gamification?.xp_to_next || 100;
  const xpForCurrent = gamification?.xp_for_current || 0;
  const dailyGoalCount = gamification?.daily_goal_count || 0;
  const dailyGoalTarget = gamification?.daily_goal_target || 5;
  const dailyGoalCompleted = gamification?.daily_goal_completed || false;
  const streakFreezes = gamification?.streak_freezes || 0;
  const coins = gamification?.coins || 0;
  const boss = gamification?.current_boss;

  const xpPct = Math.min(100, ((xp - xpForCurrent) / (xpToNext - xpForCurrent || 1)) * 100);

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-5xl mx-auto">

        {/* ═══ HERO STRIP — Coddy Style ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="mb-8"
        >
          <div className="flex items-center gap-2 mb-1">
            <span className="status-online" />
            <span className="text-[10px] font-mono text-cyber-blue/70 tracking-widest uppercase">
              Command Deck Online
            </span>
          </div>
          <h1 className="text-2xl md:text-3xl font-display font-black text-white">
            Welcome back, <span className="text-cyber-blue">{user?.name?.split(" ")[0] || "Cadet"}</span>
          </h1>
        </motion.div>

        {/* ═══ TOP STATS BAR — Streak / Level / XP ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="glass rounded-2xl p-5 mb-6"
        >
          <div className="grid grid-cols-3 gap-4 mb-4">
            {/* Streak */}
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 mb-1">
                <Flame size={20} className={`${streak > 0 ? 'text-orange-400 streak-fire' : 'text-gray-500'}`} />
                <span className="text-2xl font-display font-black text-white">{streak}</span>
              </div>
              <span className="text-[10px] font-mono text-gray-500 uppercase tracking-wider">Day Streak</span>
            </div>

            {/* Level */}
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 mb-1">
                <Trophy size={20} className="text-cyber-purple" />
                <span className="text-2xl font-display font-black text-white">{level}</span>
              </div>
              <span className="text-[10px] font-mono text-gray-500 uppercase tracking-wider">Level</span>
            </div>

            {/* XP Today */}
            <div className="text-center">
              <div className="flex items-center justify-center gap-1 mb-1">
                <Zap size={20} className="text-green-400" />
                <span className="text-2xl font-display font-black text-green-400">{xp}</span>
              </div>
              <span className="text-[10px] font-mono text-gray-500 uppercase tracking-wider">Total XP</span>
            </div>
          </div>

          {/* XP Progress Bar */}
          <div className="mb-3">
            <div className="flex justify-between text-xs font-mono mb-1">
              <span className="text-gray-500">Level {level}</span>
              <span className="text-gray-500">{xp - xpForCurrent}/{xpToNext - xpForCurrent} XP</span>
            </div>
            <div className="w-full h-2 bg-space-void rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-cyber-blue to-cyan-400 rounded-full"
                initial={{ width: 0 }}
                animate={{ width: `${xpPct}%` }}
                transition={{ duration: 1, ease: 'easeOut' }}
              />
            </div>
          </div>

          {/* Coins + Streak Freezes */}
          <div className="flex items-center justify-between text-xs font-mono">
            <div className="flex items-center gap-3">
              <span className="text-yellow-400">🪙 {coins} coins</span>
              <span className="text-blue-400 flex items-center gap-1">
                <Snowflake size={12} /> {streakFreezes} freeze{streakFreezes !== 1 ? 's' : ''}
              </span>
            </div>
            {streak > 0 && (
              <span className="text-gray-500">
                {streak >= 30 ? '5x' : streak >= 14 ? '3x' : streak >= 7 ? '2x' : streak >= 3 ? '1.5x' : '1x'} XP multiplier
              </span>
            )}
          </div>
        </motion.div>

        {/* ═══ DAILY GOAL + STREAK FREEZE ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="grid md:grid-cols-2 gap-4 mb-6"
        >
          <DailyGoal />
          <StreakFreeze streakFreezes={streakFreezes} coins={coins} />
        </motion.div>

        {/* ═══ BOSS ALERT ═══ */}
        {boss && !dailyGoalCompleted && (
          <motion.div
            initial={reduced ? {} : { opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="glass border border-amber-500/30 rounded-2xl p-5 mb-6 text-center"
          >
            <span className="text-4xl mb-2 block">{boss.emoji}</span>
            <h3 className="font-display font-bold text-white text-lg mb-1">
              Boss Battle Available!
            </h3>
            <p className="text-gray-400 text-sm font-mono mb-3">
              {boss.name} awaits at Level {gamification?.boss_level}
            </p>
            <Link to="/tower" className="btn-primary text-sm inline-block">
              Enter Battle
            </Link>
          </motion.div>
        )}

        {/* ═══ TODAY'S MISSION — Dynamic ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mb-6"
        >
          <div className="flex items-center gap-2 mb-4">
            <Sword size={18} className="text-cyber-amber" />
            <h2 className="font-display font-bold text-white text-lg uppercase tracking-wider">
              Today's Mission
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-3">
            {/* Mission 1: Solve a Problem */}
            <Link to="/problems" className="block">
              <div className="glass rounded-xl p-4 hover:border-cyber-blue/30 transition-all group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-cyber-blue/10 flex items-center justify-center">
                    <Code size={20} className="text-cyber-blue" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-display font-bold text-sm text-white group-hover:text-cyber-blue transition-colors">
                      Solve 1 Problem
                    </p>
                    <p className="text-xs font-mono text-gray-500">+15 XP</p>
                  </div>
                  {stats.questions > 0 && (
                    <CheckCircle2 size={16} className="text-green-400 shrink-0" />
                  )}
                </div>
              </div>
            </Link>

            {/* Mission 2: Daily Drill */}
            <Link to="/daily-drill" className="block">
              <div className="glass rounded-xl p-4 hover:border-cyber-amber/30 transition-all group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-cyber-amber/10 flex items-center justify-center">
                    <Flame size={20} className="text-cyber-amber" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-display font-bold text-sm text-white group-hover:text-cyber-amber transition-colors">
                      5-Min Daily Drill
                    </p>
                    <p className="text-xs font-mono text-gray-500">+10 XP</p>
                  </div>
                  {stats.aptitude >= 5 && (
                    <CheckCircle2 size={16} className="text-green-400 shrink-0" />
                  )}
                </div>
              </div>
            </Link>

            {/* Mission 3: Weak Area Practice — Dynamic */}
            {weakAreas.length > 0 ? (
              <Link to={`/problems?topic=${encodeURIComponent(weakAreas[0].topic)}`} className="block">
                <div className="glass rounded-xl p-4 hover:border-cyber-purple/30 transition-all group border border-cyber-purple/20">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-cyber-purple/10 flex items-center justify-center">
                      <Compass size={20} className="text-cyber-purple" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-display font-bold text-sm text-white group-hover:text-cyber-purple transition-colors">
                        Drill: {weakAreas[0].topic}
                      </p>
                      <p className="text-xs font-mono text-gray-500">Weak area — +20 XP</p>
                    </div>
                    <Sparkles size={16} className="text-cyber-purple shrink-0" />
                  </div>
                </div>
              </Link>
            ) : (
              <Link to="/interview" className="block">
                <div className="glass rounded-xl p-4 hover:border-cyber-purple/30 transition-all group">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-cyber-purple/10 flex items-center justify-center">
                      <Bot size={20} className="text-cyber-purple" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-display font-bold text-sm text-white group-hover:text-cyber-purple transition-colors">
                        Complete Interview
                      </p>
                      <p className="text-xs font-mono text-gray-500">+30 XP</p>
                    </div>
                    {stats.interviews >= 3 && (
                      <CheckCircle2 size={16} className="text-green-400 shrink-0" />
                    )}
                  </div>
                </div>
              </Link>
            )}
          </div>
        </motion.div>

        {/* ═══ QUICK ACTIONS ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mb-6"
        >
          <div className="flex flex-wrap gap-2">
            {quickLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-mono text-xs border transition-all duration-200 ${link.color}`}
              >
                <link.icon size={12} /> {link.label}
              </Link>
            ))}
          </div>
        </motion.div>

        {/* ═══ SKILL RADAR ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.45 }}
          className="mb-6"
        >
          <SkillRadar />
        </motion.div>

        {/* ═══ USAGE BAR (Free Tier) ═══ */}
        {!isPremium && (
          <motion.div
            initial={reduced ? {} : { opacity: 0 }}
            animate={{ opacity: 1 }}
            className="glass rounded-xl p-5 mb-6"
          >
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-display font-bold text-sm text-gray-300 uppercase tracking-wider flex items-center gap-2">
                <Zap size={14} className="text-cyber-amber" /> Monthly Clearance
              </h3>
              <Link to="/pricing?selected=pro" className="text-xs text-cyber-blue hover:text-cyber-blue/80 font-mono">
                Upgrade →
              </Link>
            </div>
            <div className="grid md:grid-cols-2 gap-3">
              <UsageBar used={user?.interviews_used || 0} limit={user?.interviews_limit || 5} feature="AI Interviews" />
              <UsageBar used={user?.resumes_used || 0} limit={user?.resumes_limit || 3} feature="Resume Reviews" />
              <UsageBar used={user?.aptitude_used || 0} limit={user?.aptitude_limit || 5} feature="Aptitude Tests" />
              <UsageBar used={user?.cover_letters_used || 0} limit={user?.cover_letters_limit || 3} feature="Cover Letters" />
            </div>
          </motion.div>
        )}

        {/* ═══ ALL FEATURES — Compact Grid ═══ */}
        <motion.div
          initial={reduced ? {} : { opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="mb-6"
        >
          <h2 className="font-display font-bold text-white text-lg uppercase tracking-wider mb-4">
            All Tools
          </h2>
          <StaggerContainer className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {features.map((f) => (
              <StaggerItem key={f.title}>
                <Link to={f.link} className="block">
                  <motion.div
                    whileHover={reduced ? {} : { y: -2 }}
                    className="glass rounded-xl p-4 group h-full hover:border-cyber-blue/20 transition-all"
                  >
                    <div className={`w-9 h-9 rounded-lg border flex items-center justify-center mb-2 ${f.color}`}>
                      <f.icon size={18} />
                    </div>
                    <h3 className="font-display font-bold text-white text-xs group-hover:text-cyber-blue transition-colors">
                      {f.title}
                    </h3>
                    <p className="text-gray-500 font-mono text-[10px] mt-0.5">{f.desc}</p>
                  </motion.div>
                </Link>
              </StaggerItem>
            ))}
          </StaggerContainer>
        </motion.div>

        {/* ═══ UPGRADE CTA ═══ */}
        {!isPremium && (
          <motion.div
            initial={reduced ? {} : { opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="card-glow flex flex-col md:flex-row items-center justify-between gap-4 mb-8"
          >
            <div>
              <h3 className="text-lg font-display font-bold text-white mb-1">Upgrade to <span className="text-cyber-blue">Commander</span></h3>
              <p className="text-gray-400 font-mono text-sm">
                Unlimited missions, hulls, diagnostics. Full clearance.
              </p>
            </div>
            <Link to="/pricing" className="btn-primary text-sm shrink-0">
              View Clearance Levels
            </Link>
          </motion.div>
        )}
      </div>
    </div>
  );
}
