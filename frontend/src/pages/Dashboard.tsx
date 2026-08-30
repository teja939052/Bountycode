import { useMemo } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import { useDashboard } from "../hooks/useDashboard";
import {
  Flame,
  Trophy,
  ArrowRight,
  CalendarClock,
  Search,
  TrendingUp,
  Award,
  Clock,
  Target,
  Code2,
  BookOpen,
  Briefcase,
  MessageSquare,
  Lightbulb,
  BarChart3,
  CheckCircle2,
  XCircle,
} from "lucide-react";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";
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
  { to: "/compiler", icon: Lightbulb, label: "Compiler", desc: "Run code", color: "#5BA7A0" },
];

const SKILL_RINGS = [
  { key: "dsa", label: "DSA", color: "#22C55E", icon: Code2 },
  { key: "cs_fundamentals", label: "CS", color: "#4A90E2", icon: BookOpen },
  { key: "interview", label: "Interview", color: "#8B6BD9", icon: MessageSquare },
  { key: "resume", label: "Resume", color: "#EAB74D", icon: FileText },
];

const DEFAULT_MISSION = { label: "Start Today's Practice", to: "/practice", minutes: 15, xp: 50 };

function SolvedRing({ total, easy, medium, hard, size = 160 }: { total: number; easy: number; medium: number; hard: number; size?: number }) {
  const strokeWidth = 12;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const totalSolved = easy + medium + hard;
  const offset = totalSolved === 0 ? circumference : circumference * (1 - totalSolved / Math.max(total, 1));

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} stroke="#e5e7eb" strokeWidth={strokeWidth} fill="none" />
        {totalSolved > 0 && (
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="url(#solvedGradient)"
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            fill="none"
            strokeLinecap="round"
            style={{ transition: "stroke-dashoffset 700ms ease-out" }}
          />
        )}
        <defs>
          <linearGradient id="solvedGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#22C55E" />
            <stop offset="50%" stopColor="#EAB74D" />
            <stop offset="100%" stopColor="#E96A5B" />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold text-gray-900">{totalSolved}</span>
        <span className="text-[11px] text-gray-500 mt-0.5">solved</span>
      </div>
    </div>
  );
}

function timeAgo(dateStr?: string) {
  if (!dateStr) return "";
  const diff = Date.now() - new Date(dateStr).getTime();
  const m = Math.floor(diff / 60000);
  if (m < 1) return "just now";
  if (m < 60) return `${m}m ago`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h ago`;
  return `${Math.floor(h / 24)}d ago`;
}

export default function Dashboard() {
  const storeUser = useAuthStore((s) => s.user);
  const [state, setState] = useState<StudentState | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  const {
    gamification,
    questionStats,
    recentProblems,
    readinessScore,
    dailyChallenge,
    streakStatus,
    isLoading: dashboardLoading,
    isError,
    refetch,
  } = useDashboard();

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
  const solved = questionStats?.total_solved || 0;
  const easy = questionStats?.easy || 0;
  const medium = questionStats?.medium || 0;
  const hard = questionStats?.hard || 0;
  const daily = dailyChallenge;

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

  if (loading || dashboardLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mx-auto mb-3" />
          <p className="text-sm text-gray-500">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-lg font-bold text-gray-900">Failed to load dashboard</h2>
          <button onClick={() => refetch()} className="mt-4 px-5 py-2 rounded-lg bg-blue-600 text-white text-sm font-semibold">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <div className="mx-auto max-w-6xl px-4 py-6 sm:py-10">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 }} className="space-y-6">
          {/* Header + greeting */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <p className="text-sm text-gray-500">{greeting}, {firstName}</p>
              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-gray-900 mt-1">
                {readiness === null ? "Let's get started." : `You're ${readiness}% interview ready.`}
              </h1>
            </div>
            {readiness !== null && (
              <div className="shrink-0 rounded-2xl border border-gray-200 bg-white p-3 shadow-sm">
                <ReadinessRing value={readiness} size={80} />
              </div>
            )}
          </div>

          {/* Search */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search problems, topics, companies..."
              className="w-full rounded-xl border border-gray-200 bg-white py-3 pl-11 pr-4 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition-all"
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
                  className="flex flex-col items-center gap-2 rounded-xl border border-gray-200 bg-white p-4 transition-all hover:border-blue-300 hover:shadow-md hover:-translate-y-0.5"
                >
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl" style={{ backgroundColor: `${action.color}15`, color: action.color }}>
                    <action.icon size={20} />
                  </div>
                  <div className="text-center">
                    <p className="text-sm font-semibold text-gray-900">{action.label}</p>
                    <p className="text-[11px] text-gray-500">{action.desc}</p>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>

          {/* Mission card */}
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <Card className="border border-gray-200 bg-white p-5 sm:p-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                    <Target size={24} />
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">{mission.label}</h3>
                    <p className="text-sm text-gray-500 mt-1">~{mission.minutes} minutes · +{mission.xp || 50} XP</p>
                  </div>
                </div>
                <Link to={mission.to} className="w-full sm:w-auto">
                  <Button variant="primary" rightIcon={<ArrowRight size={16} />} className="w-full sm:w-auto">
                    Start
                  </Button>
                </Link>
              </div>
            </Card>
          </motion.div>

          {/* Stats + skill rings */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Skill rings */}
            <Card className="lg:col-span-2 border border-gray-200 bg-white p-5 sm:p-6">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 size={18} className="text-blue-600" />
                <h3 className="font-bold text-gray-900">Your Skills</h3>
              </div>
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
                          <circle cx={50} cy={50} r={40} stroke="#e5e7eb" strokeWidth={8} fill="none" />
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
                      <p className="text-sm font-semibold text-gray-900">{ring.label}</p>
                      <p className="text-xs text-gray-500">{Math.round(value)}%</p>
                    </motion.div>
                  );
                })}
              </div>
            </Card>

            {/* Stats */}
            <Card className="border border-gray-200 bg-white p-5 sm:p-6">
              <div className="flex items-center gap-2 mb-4">
                <Award size={18} className="text-amber-500" />
                <h3 className="font-bold text-gray-900">Overview</h3>
              </div>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-orange-50 text-orange-600">
                      <Flame size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Streak</p>
                      <p className="text-xs text-gray-500">{s.streak} days</p>
                    </div>
                  </div>
                  <span className="text-lg font-bold text-orange-600">{s.streak}</span>
                </div>
                <div className="h-px w-full bg-gray-100" />
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-green-50 text-green-600">
                      <Trophy size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Level</p>
                      <p className="text-xs text-gray-500">{s.xp.toLocaleString()} XP</p>
                    </div>
                  </div>
                  <span className="text-lg font-bold text-gray-900">Lv. {s.level}</span>
                </div>
                <div className="h-px w-full bg-gray-100" />
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-50 text-blue-600">
                      <Clock size={20} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Practice</p>
                      <p className="text-xs text-gray-500">12h this week</p>
                    </div>
                  </div>
                  <span className="text-lg font-bold text-gray-900">3.2h</span>
                </div>
              </div>
            </Card>
          </div>

          {/* Problem of the day + Recent submissions */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
            <div className="xl:col-span-2 space-y-5">
              {/* Problem of the day */}
              <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
                <Card className="border border-gray-200 bg-white p-5 sm:p-6">
                  <div className="flex items-start gap-4">
                    <div className="h-12 w-12 shrink-0 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
                      <CalendarClock size={22} />
                    </div>
                    <div className="min-w-0 flex-1">
                      <span className="text-[11px] font-semibold uppercase tracking-wide text-gray-500">Problem of the Day</span>
                      <h2 className="text-lg font-bold mt-1 text-gray-900">
                        {daily?.title || daily?.question_title || "Today's Adaptive Challenge"}
                      </h2>
                      <p className="text-sm text-gray-500 mt-1 line-clamp-2">
                        {daily?.description || "Solve today's hand-picked problem to keep your streak alive."}
                      </p>
                      <div className="flex items-center gap-3 mt-3 text-xs text-gray-500">
                        {daily?.difficulty && (
                          <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-700">
                            {daily.difficulty}
                          </span>
                        )}
                        <span>·</span>
                        <span>+{daily?.xp_reward || 80} XP</span>
                      </div>
                    </div>
                    <Link
                      to={`/question/${daily?.id || daily?.question_id || "random"}`}
                      className="ml-2 shrink-0 inline-flex items-center gap-1 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 transition-colors"
                    >
                      Solve <ArrowRight size={15} />
                    </Link>
                  </div>
                </Card>
              </motion.div>

              {/* Recent submissions */}
              <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
                <Card className="border border-gray-200 bg-white p-5 sm:p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-bold text-gray-900">Recent Submissions</h3>
                    <Link to="/question-bank" className="text-xs text-blue-600 hover:underline">
                      View all
                    </Link>
                  </div>
                  {recentProblems.length === 0 ? (
                    <div className="text-sm text-gray-500 py-6 text-center">
                      No submissions yet — solve a problem to see it here.
                    </div>
                  ) : (
                    <div className="overflow-x-auto -mx-1">
                      <table className="w-full text-sm">
                        <thead>
                          <tr className="text-[11px] uppercase tracking-wide text-gray-500 border-b border-gray-200">
                            <th className="text-left font-medium py-2 px-2">Status</th>
                            <th className="text-left font-medium py-2 px-2">Problem</th>
                            <th className="text-left font-medium py-2 px-2">Difficulty</th>
                            <th className="text-right font-medium py-2 px-2">When</th>
                          </tr>
                        </thead>
                        <tbody>
                          {recentProblems.map((p, i) => (
                            <tr key={p.question_id || i} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                              <td className="py-2.5 px-2">
                                <span className="inline-flex items-center gap-1.5 text-green-600">
                                  <CheckCircle2 size={15} /> Accepted
                                </span>
                              </td>
                              <td className="py-2.5 px-2">
                                <Link to={`/question/${p.question_id || "random"}`} className="text-gray-900 hover:text-blue-600 transition-colors">
                                  {p.title || "Problem"}
                                </Link>
                              </td>
                              <td className="py-2.5 px-2">
                                <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-700">
                                  {p.difficulty}
                                </span>
                              </td>
                              <td className="py-2.5 px-2 text-right text-gray-500 whitespace-nowrap">{timeAgo(p.completed_at || p.timestamp)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </Card>
              </motion.div>
            </div>

            {/* Right column */}
            <div className="space-y-5">
              {/* Readiness */}
              <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
                <Card className="border border-gray-200 bg-white p-5 sm:p-6">
                  <h3 className="font-bold text-gray-900 mb-3">Interview Readiness</h3>
                  <div className="flex flex-col items-center">
                    <ReadinessRing value={readiness} size={120} />
                    <p className="text-xs text-gray-500 mt-3 text-center">
                      Keep practicing to reach the <span className="text-gray-900 font-medium">Software Engineer</span> target.
                    </p>
                  </div>
                </Card>
              </motion.div>

              {/* Activity heatmap */}
              <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}>
                <Card className="border border-gray-200 bg-white p-5 sm:p-6">
                  <h3 className="font-bold text-gray-900 mb-3">Activity</h3>
                  <div className="text-xs text-gray-500 text-center py-6">
                    Activity heatmap coming soon
                  </div>
                </Card>
              </motion.div>

              {/* Skill coverage */}
              <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
                <Card className="border border-gray-200 bg-white p-5 sm:p-6">
                  <h3 className="font-bold text-gray-900 mb-3">Skill Coverage</h3>
                  <div className="space-y-3">
                    {SKILL_RINGS.map((skill, i) => {
                      const value = s.categories[skill.key] ?? 0;
                      return (
                        <div key={skill.key} className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <div className="flex h-8 w-8 items-center justify-center rounded-lg" style={{ backgroundColor: `${skill.color}15`, color: skill.color }}>
                              <skill.icon size={16} />
                            </div>
                            <span className="text-sm font-medium text-gray-900">{skill.label}</span>
                          </div>
                          <span className="text-sm font-bold text-gray-900">{Math.round(value)}%</span>
                        </div>
                      );
                    })}
                  </div>
                </Card>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
