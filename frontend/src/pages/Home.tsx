import { useEffect, useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import { requestWithRetry as request } from "../services/api/request.ts";
import {
  Search,
  Code2,
  Flame,
  Trophy,
  ArrowRight,
  Target,
  BookOpen,
  Briefcase,
  MessageSquare,
  Zap,
  Star,
  FileText,
  TrendingUp,
  Award,
  Clock,
  BarChart3,
} from "lucide-react";
import { LCard, LSectionTitle } from "../components/leetcode/Kit";
import { Button } from "../design-system/Button";
import { ReadinessRing } from "../design-system/Progress";

interface StudentState {
  readiness: number | null;
  categories: Record<string, number>;
  level: number;
  streak: number;
  xp: number;
  name: string;
  next_mission?: { label: string; to: string; minutes: number; xp?: number } | null;
}

const QUICK_ACTIONS = [
  { to: "/practice", icon: Code2, label: "Practice", desc: "DSA problems", color: "#22C55E" },
  { to: "/interview", icon: MessageSquare, label: "Interviews", desc: "Mock sessions", color: "#4A90E2" },
  { to: "/learn/c", icon: BookOpen, label: "Learn", desc: "Coding lessons", color: "#8B6BD9" },
  { to: "/company-prep", icon: Briefcase, label: "Companies", desc: "53+ guides", color: "#EAB74D" },
  { to: "/question-bank", icon: Target, label: "Problems", desc: "3217+ questions", color: "#E96A5B" },
  { to: "/compiler", icon: Zap, label: "Compiler", desc: "Run code", color: "#5BA7A0" },
];

const SKILL_RINGS = [
  { key: "dsa", label: "DSA", color: "#22C55E", icon: Code2 },
  { key: "cs_fundamentals", label: "CS", color: "#4A90E2", icon: BookOpen },
  { key: "interview", label: "Interview", color: "#8B6BD9", icon: MessageSquare },
  { key: "resume", label: "Resume", color: "#EAB74D", icon: FileText },
];

const DEFAULT_MISSION = { label: "Start Today's Practice", to: "/practice", minutes: 15, xp: 50 };

export default function Home() {
  const storeUser = useAuthStore((s) => s.user);
  const [state, setState] = useState<StudentState | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const res = await request<StudentState>("/api/v1/auth/state");
        if (!active) return;
        setState({
          readiness: res?.readiness ?? null,
          categories: res?.categories || {},
          level: res?.level ?? storeUser?.level ?? 1,
          streak: res?.streak ?? storeUser?.streak ?? 0,
          xp: res?.xp ?? storeUser?.xp ?? 0,
          name: res?.name || storeUser?.name || "",
          next_mission: res?.next_mission,
        });
      } catch {
        setState({
          readiness: null,
          categories: {},
          level: storeUser?.level ?? 1,
          streak: storeUser?.streak ?? 0,
          xp: storeUser?.xp ?? 0,
          name: storeUser?.name || "",
          next_mission: null,
        });
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => { active = false; };
  }, [storeUser?.name, storeUser?.level, storeUser?.streak, storeUser?.xp]);

  const s = state ?? {
    readiness: null,
    categories: {},
    level: storeUser?.level ?? 1,
    streak: storeUser?.streak ?? 0,
    xp: storeUser?.xp ?? 0,
    name: storeUser?.name || "",
    next_mission: null,
  };

  const firstName = s.name?.split(" ")[0] || "there";
  const readiness = s.readiness;
  const mission = s.next_mission || DEFAULT_MISSION;

  const greeting = useMemo(() => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 18) return "Good afternoon";
    return "Good evening";
  }, []);

  const filteredActions = useMemo(() => {
    if (!searchQuery.trim()) return QUICK_ACTIONS;
    const q = searchQuery.toLowerCase();
    return QUICK_ACTIONS.filter((a) => a.label.toLowerCase().includes(q) || a.desc.toLowerCase().includes(q));
  }, [searchQuery]);

  return (
    <div className="min-h-screen bg-[#0a0f0d] text-[#e9e9e9]">
      <div className="mx-auto max-w-6xl px-4 py-6 sm:py-10">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="space-y-6">
          {/* Header + greeting */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <p className="text-sm text-[#9a9a9a]">{greeting}, {firstName}</p>
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-[#e9e9e9] mt-1">
                {readiness === null ? "Let's get started." : `You're ${readiness}% voyage ready.`}
              </h1>
            </div>
            {readiness !== null && (
              <div className="shrink-0 rounded-2xl border border-[#2a2a2a] bg-[#171717] p-3">
                <ReadinessRing value={readiness} size={80} />
              </div>
            )}
          </div>

          {/* Search */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-[#6b6b6b]" size={18} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search problems, topics, companies..."
              className="w-full rounded-xl border border-[#2a2a2a] bg-[#171717] py-3 pl-11 pr-4 text-sm text-[#e9e9e9] placeholder-[#6b6b6b] focus:outline-none focus:border-[#ffa116] focus:ring-1 focus:ring-[#ffa116] transition-colors"
            />
          </div>

          {/* Quick actions */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
            {filteredActions.map((action, i) => (
              <motion.div
                key={action.to}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Link
                  to={action.to}
                  className="flex flex-col items-center gap-2 rounded-xl border border-[#2a2a2a] bg-[#171717] p-4 transition-all hover:border-[#ffa116]/50 hover:bg-[#1f1f1f] hover:-translate-y-0.5"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl" style={{ backgroundColor: `${action.color}18`, color: action.color }}>
                    <action.icon size={20} />
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-semibold text-[#e9e9e9]">{action.label}</p>
                    <p className="text-[11px] text-[#9a9a9a]">{action.desc}</p>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>

          {/* Mission card */}
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <LCard className="p-5 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#ffa1161a] text-[#ffa116]">
                    <Target size={24} />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-[#e9e9e9]">{mission.label}</h3>
                    <p className="text-sm text-[#9a9a9a] mt-1">~{mission.minutes} minutes · +{mission.xp || 50} XP</p>
                  </div>
                </div>
                <Link to={mission.to} className="w-full sm:w-auto">
                  <Button variant="primary" rightIcon={<ArrowRight size={16} />} className="w-full sm:w-auto">
                    Start
                  </Button>
                </Link>
              </div>
            </LCard>
          </motion.div>

          {/* Stats + skill rings */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Skill rings */}
            <LCard className="lg:col-span-2">
              <LSectionTitle title="Your Skills" icon={<BarChart3 size={16} className="text-[#ffa116]" />} />
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                {SKILL_RINGS.map((ring, i) => {
                  const value = s.categories[ring.key] ?? 0;
                  return (
                    <motion.div
                      key={ring.key}
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ delay: 0.1 + i * 0.05 }}
                      className="flex flex-col items-center text-center"
                    >
                      <div className="relative mb-3">
                        <svg width={100} height={100} className="-rotate-90">
                          <circle cx={50} cy={50} r={40} stroke="#2a2a2a" strokeWidth={8} fill="none" />
                          <circle
                            cx={50}
                            cy={50}
                            r={40}
                            stroke={ring.color}
                            strokeWidth={8}
                            strokeDasharray={2 * Math.PI * 40}
                            strokeDashoffset={2 * Math.PI * 40 * (1 - Math.min(100, Math.max(0, value)) / 100)}
                            fill="none"
                            strokeLinecap="round"
                            style={{ transition: "stroke-dashoffset 700ms ease-out" }}
                          />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center">
                          <ring.icon size={20} style={{ color: ring.color }} />
                        </div>
                      </div>
                      <p className="text-sm font-semibold text-[#e9e9e9]">{ring.label}</p>
                      <p className="text-xs text-[#9a9a9a]">{Math.round(value)}%</p>
                    </motion.div>
                  );
                })}
              </div>
            </LCard>

            {/* Stats */}
            <LCard>
              <LSectionTitle title="Overview" icon={<Award size={16} className="text-[#ffa116]" />} />
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#ffa1161a] text-[#ffa116]">
                      <Flame size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-[#e9e9e9]">Streak</p>
                      <p className="text-xs text-[#9a9a9a]">{s.streak} days</p>
                    </div>
                  </div>
                  <span className="text-lg font-bold text-[#ffa116]">{s.streak}</span>
                </div>
                <div className="h-px w-full bg-[#2a2a2a]" />
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#2eb88a1a] text-[#2eb88a]">
                      <Trophy size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-[#e9e9e9]">Level</p>
                      <p className="text-xs text-[#9a9a9a]">{s.xp.toLocaleString()} XP</p>
                    </div>
                  </div>
                  <span className="text-lg font-bold text-[#e9e9e9]">Lv. {s.level}</span>
                </div>
                <div className="h-px w-full bg-[#2a2a2a]" />
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-[#4A90E21a] text-[#4A90E2]">
                      <Clock size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-[#e9e9e9]">Practice</p>
                      <p className="text-xs text-[#9a9a9a]">12h this week</p>
                    </div>
                  </div>
                  <span className="text-lg font-bold text-[#e9e9e9]">3.2h</span>
                </div>
              </div>
            </LCard>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
