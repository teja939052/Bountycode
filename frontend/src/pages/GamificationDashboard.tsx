import { useState } from "react";
import { useParams } from "react-router-dom";
import { Flame, Zap, Trophy, ShieldCheck, Star, Gift, Target, Sparkles, List, Activity } from "lucide-react";
import { Link } from "react-router-dom";
import api from "../services/api";
import { GamificationWidget } from "./components/gamification/GamificationWidget";
import { StreakCard } from "./components/gamification/Streak";
import { BadgeGrid } from "./components/gamification/Badge";
import { Chest } from "./components/gamification/Chest";
import { JourneyPath } from "./components/gamification/JourneyTile";
import { Certificate } from "./components/gamification/Certificate";
import { getXPForLevel, getLevelLabel } from "./components/gamification/palette";
import { CODDY } from "./components/gamification/palette";

const MOCK_BADGES = [
  { id: "first-steps", name: "First Steps", description: "Complete your first lesson", tier: "bronze", icon: <Zap size={16} className="text-amber-500" />, earned: true },
  { id: "streak-starter", name: "Streak Starter", description: "3-day streak", tier: "bronze", icon: <Flame size={16} className="text-orange-500" />, earned: true },
  { id: "percentages-pro", name: "Percentages Pro", description: "Master percentages", tier: "silver", icon: <ShieldCheck size={16} className="text-slate-400" />, earned: false },
  { id: "array-master", name: "Array Master", description: "Master arrays", tier: "gold", icon: <Star size={16} className="text-amber-400" />, earned: false },
  { id: "code-tracer", name: "Code Tracer", description: "Trace 10 programs", tier: "silver", icon: <Target size={16} className="text-indigo-500" />, earned: false },
  { id: "quest-completer", name: "Quest Completer", description: "Complete 5 quests", tier: "gold", icon: <Star size={16} className="text-amber-400" />, earned: false },
];

const JOURNEY_TILES = [
  { id: "loops", label: "Loops", status: "done", topic: "loops" },
  { id: "arrays", label: "Arrays", status: "done", topic: "arrays" },
  { id: "nested-loops", label: "Nested Loops", status: "active", topic: "loops" },
  { id: "complexity", label: "Complexity", status: "locked", topic: "complexity" },
  { id: "linked-list", label: "Linked List", status: "locked", topic: "linked_lists" },
  { id: "trees", label: "Trees", status: "locked", topic: "trees" },
];

const TABS = [
  { id: "overview", label: "Overview", icon: <Activity size={16} /> },
  { id: "badges", label: "Badges", icon: <Star size={16} /> },
  { id: "journey", label: "Journey", icon: <Target size={16} /> },
  { id: "chests", label: "Chests", icon: <Gift size={16} /> },
];

export default function GamificationDashboard() {
  const { section } = useParams<{ section?: string }>();
  const [xp, setXp] = useState(1240);
  const [level, setLevel] = useState(5);
  const [streak, setStreak] = useState(12);
  const [league, setLeague] = useState(42);
  const [activeTab, setActiveTab] = useState(section || "overview");

  const currentLevelXP = getXPForLevel(level);
  const nextLevelXP = getXPForLevel(level + 1);
  const progress = ((xp - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100;
  const label = getLevelLabel(level);
  const levelColor = CODDY[label.color];

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-display font-bold text-ink dark:text-white">Gamification</h1>
          <p className="text-slate-500 dark:text-slate-400">Track your progress, earn badges, and level up your placement prep.</p>
        </div>
        <Link to="/blog" className="flex items-center gap-2 px-4 py-2 bg-ink dark:bg-slate-800 text-white rounded-xl hover:bg-indigo-800 dark:hover:bg-slate-700 transition font-medium">
          <Sparkles size={14} /> Read Blogs
        </Link>
      </div>

      <GamificationWidget xp={xp} level={level} streak={streak} league={league} badges={MOCK_BADGES.filter((b) => b.earned).length} />

      <div className="grid gap-6 md:grid-cols-3 lg:grid-cols-4">
        <div className="col-span-2 lg:col-span-2">
          <StreakCard days={streak} best={streak + 5} frozen={false} />
        </div>
        <div className="lg:col-span-2">
          <div className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-6 shadow-sm">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-14 h-14 rounded-2xl flex items-center justify-center font-display font-bold text-xl" style={{
                  background: `linear-gradient(135deg, ${levelColor.light}30, ${CODDY.blue.light}20)`,
                  color: levelColor.base,
                  border: `2px solid ${levelColor.base}80`,
                  boxShadow: `0 0 20px ${levelColor.base}30`,
                }}>
                  {level}
                </div>
                <div>
                  <p className="text-[10px] uppercase tracking-wider text-slate-400 font-bold">Current Level</p>
                  <p className="text-2xl font-bold text-ink dark:text-white">{level}</p>
                  <p className="text-[10px] px-2 py-[1px] rounded border mt-1" style={{
                    backgroundColor: `${levelColor.base}15`,
                    color: levelColor.base,
                    border: `1px solid ${levelColor.base}40`,
                  }}>
                    {label.label.toUpperCase()}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-[10px] uppercase tracking-wider text-slate-400 font-bold">XP to Next Level</p>
                <p className="text-xl font-bold text-ink dark:text-white">{nextLevelXP - xp}</p>
              </div>
            </div>
            <div className="h-3 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden border border-white/20 dark:border-white/10 mb-4">
              <div className="h-full rounded-full" style={{ background: `linear-gradient(90deg, ${levelColor.base}, ${CODDY.indigo.base})`, width: `${Math.min(100, progress)}%`, transition: 'width 1s ease' }} />
            </div>
            <div className="flex justify-between text-[10px] font-mono text-slate-500 dark:text-slate-400">
              <span>{currentLevelXP} XP</span>
              <span>{nextLevelXP} XP</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex gap-1 px-1">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setActiveTab(t.id)}
            className={`px-4 py-2 rounded-xl text-sm font-medium transition ${activeTab === t.id ? 'bg-ink dark:bg-slate-800 text-white shadow-md' : 'bg-white dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 border border-white/20 dark:border-white/10 hover:bg-slate-50 dark:hover:bg-slate-700/50'}`}
          >
            {t.icon}
            <span className="ml-2 hidden sm:inline">{t.label}</span>
          </button>
        ))}
      </div>

      {activeTab === "overview" && (
        <div className="grid gap-6 md:grid-cols-2">
          <div className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-6 shadow-sm">
            <h3 className="font-bold text-ink dark:text-white mb-4 flex items-center gap-2">
              <ShieldCheck size={16} className="text-success-500" /> Recent Activity
            </h3>
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center gap-3 p-3 rounded-xl bg-slate-50 dark:bg-slate-800/50 border border-white/10">
                  <div className="w-8 h-8 rounded-lg bg-blue-50 dark:bg-blue-900/30 flex items-center justify-center text-blue-500 dark:text-blue-400">
                    <Zap size={14} />
                  </div>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-ink dark:text-white">Completed Percentages lesson</p>
                    <p className="text-[10px] text-slate-500 dark:text-slate-400">2 minutes ago · +50 XP</p>
                  </div>
                  <span className="text-[10px] font-mono text-warning-500">+50 XP</span>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-6 shadow-sm">
            <h3 className="font-bold text-ink dark:text-white mb-4 flex items-center gap-2">
              <List size={16} className="text-indigo-500" /> Weekly Progress
            </h3>
            <div className="flex items-end gap-1 h-32">
              {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day, i) => (
                <div key={day} className="flex flex-col items-center gap-1">
                  <div className={`w-full rounded-t-md transition-all duration-300 ${i < 5 ? 'bg-success-500' : 'bg-slate-200 dark:bg-slate-700'}`} style={{ height: `${30 + i * 12}%` }} />
                  <span className="text-[10px] text-slate-500 dark:text-slate-400">{day}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === "badges" && (
        <div className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-6 shadow-sm">
          <h3 className="font-bold text-ink dark:text-white mb-4">Earned Badges</h3>
          <BadgeGrid badges={MOCK_BADGES} />
        </div>
      )}

      {activeTab === "journey" && (
        <div className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-6 shadow-sm">
          <h3 className="font-bold text-ink dark:text-white mb-4">Learning Path</h3>
          <JourneyPath tiles={JOURNEY_TILES} />
        </div>
      )}

      {activeTab === "chests" && (
        <div className="bg-white dark:bg-slate-900 border border-white/30 dark:border-white/10 rounded-2xl p-6 shadow-sm">
          <h3 className="font-bold text-ink dark:text-white mb-4">Reward Chests</h3>
          <div className="flex gap-4">
            {['wood', 'silver', 'gold', 'diamond'].map((type, i) => (
              <Chest key={i} type={type} opened={false} onOpen={() => {}} size="lg" />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
