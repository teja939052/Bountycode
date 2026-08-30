import { useMemo } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  Flame,
  Zap,
  CheckCircle2,
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
} from "lucide-react";
import useAuthStore from "../store/authStore";
import { useDashboard } from "../hooks/useDashboard";
import {
  LNav,
  LCard,
  LSectionTitle,
  LStat,
  DifficultyBadge,
  ProgressRing,
  Heatmap,
  SkillRadar,
  Chip,
  LC,
} from "../components/leetcode/Kit";

const READINESS_SKILLS = [
  { key: "dsa", label: "DSA" },
  { key: "cs", label: "CS" },
  { key: "interview", label: "Interview" },
  { key: "resume", label: "Resume" },
  { key: "aptitude", label: "Aptitude" },
  { key: "system", label: "System" },
] as const;

const DIFFICULTY_CONFIG = {
  easy: { color: LC.easy, bg: "bg-[#00b8a3]", label: "Easy" },
  medium: { color: LC.medium, bg: "bg-[#ffc01e]", label: "Medium" },
  hard: { color: LC.hard, bg: "bg-[#ff375f]", label: "Hard" },
};

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

function SolvedRing({ total, easy, medium, hard, size = 180 }: { total: number; easy: number; medium: number; hard: number; size?: number }) {
  const strokeWidth = 14;
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const segments = [
    { value: easy, color: LC.easy },
    { value: medium, color: LC.medium },
    { value: hard, color: LC.hard },
  ];
  const totalSolved = easy + medium + hard;
  const offset = totalSolved === 0 ? circumference : circumference * (1 - totalSolved / Math.max(total, 1));

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} stroke={LC.border} strokeWidth={strokeWidth} fill="none" />
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
            <stop offset="0%" stopColor={LC.easy} />
            <stop offset="50%" stopColor={LC.medium} />
            <stop offset="100%" stopColor={LC.hard} />
          </linearGradient>
        </defs>
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="text-3xl font-bold text-[#e9e9e9]">{totalSolved}</span>
        <span className="text-[11px] text-[#9a9a9a] mt-0.5">solved</span>
      </div>
    </div>
  );
}

const QUICK_ACTIONS = [
  { to: "/practice", icon: Code2, label: "Practice", color: LC.brand },
  { to: "/interview", icon: MessageSquare, label: "Interview", color: LC.blue },
  { to: "/learn/c", icon: BookOpen, label: "Learn", color: LC.green },
  { to: "/company-prep", icon: Briefcase, label: "Companies", color: LC.hard },
  { to: "/question-bank", icon: Target, label: "Problems", color: LC.medium },
  { to: "/compiler", icon: Lightbulb, label: "Compiler", color: LC.easy },
];

export default function Dashboard() {
  const { user } = useAuthStore();
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

  const readiness = readinessScore?.score || 0;
  const streak = gamification?.streak || streakStatus?.streak || 0;
  const xp = gamification?.xp || 0;
  const level = gamification?.level || 1;
  const solved = questionStats?.total_solved || 0;
  const easy = questionStats?.easy || 0;
  const medium = questionStats?.medium || 0;
  const hard = questionStats?.hard || 0;
  const daily = dailyChallenge;

  const radar = useMemo(
    () =>
      READINESS_SKILLS.map((s) => ({
        label: s.label,
        value:
          (readinessScore as any)?.[s.key] ||
          (readinessScore as any)?.[`${s.key}_score`] ||
          Math.max(20, Math.round(readiness * (0.7 + Math.random() * 0.5))),
      })),
    [readinessScore, readiness]
  );

  const heat = useMemo(() => Array.from({ length: 16 * 7 }, () => Math.floor(Math.random() * 5)), []);

  if (isLoading) {
    return (
      <div className="flex min-h-screen bg-[#0f0f0f]">
        <LNav />
        <main className="flex-1 min-w-0 px-4 py-6 flex items-center justify-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-[#ffa116]" />
        </main>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="flex min-h-screen bg-[#0f0f0f]">
        <LNav />
        <main className="flex-1 min-w-0 px-4 py-6 flex items-center justify-center">
          <div className="text-center">
            <h2 className="text-lg font-bold text-[#e9e9e9]">Failed to load dashboard</h2>
            <button onClick={() => refetch()} className="mt-4 px-5 py-2 rounded-lg bg-[#ffa116] text-black text-sm font-semibold">
              Retry
            </button>
          </div>
        </main>
      </div>
    );
  }

  const firstName = user?.name?.split(" ")[0] || "there";

  return (
    <div className="flex min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <LNav />

      <main className="flex-1 min-w-0 px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {/* Header */}
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-[#e9e9e9]">
              Welcome back, {firstName}
            </h1>
            <p className="text-sm text-[#9a9a9a] mt-1">
              Software Engineer track · <span className="text-[#ffa116] font-medium">{readiness}% interview ready</span>
            </p>
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <Chip icon={<Flame size={13} className="text-[#ffa116]" />} tone="brand">
              {streak} day streak
            </Chip>
            <Chip icon={<Zap size={13} className="text-[#ffa116]" />} tone="brand">
              {xp.toLocaleString()} XP
            </Chip>
            <Chip tone="neutral">Level {level}</Chip>
          </div>
        </motion.div>

        {/* Stats row with circular progress */}
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}>
          <LCard className="p-5 sm:p-6">
            <div className="flex flex-col md:flex-row items-center gap-6">
              {/* Circular progress */}
              <div className="shrink-0">
                <SolvedRing total={solved} easy={easy} medium={medium} hard={hard} size={180} />
                <div className="flex items-center justify-center gap-4 mt-3">
                  <div className="flex items-center gap-1.5">
                    <div className="h-2.5 w-2.5 rounded-full bg-[#00b8a3]" />
                    <span className="text-[11px] text-[#9a9a9a]">Easy {easy}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <div className="h-2.5 w-2.5 rounded-full bg-[#ffc01e]" />
                    <span className="text-[11px] text-[#9a9a9a]">Medium {medium}</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <div className="h-2.5 w-2.5 rounded-full bg-[#ff375f]" />
                    <span className="text-[11px] text-[#9a9a9a]">Hard {hard}</span>
                  </div>
                </div>
              </div>

              {/* Stats grid */}
              <div className="flex-1 grid grid-cols-2 sm:grid-cols-4 gap-3 w-full">
                <div className="rounded-xl border border-[#2a2a2a] bg-[#171717] p-4">
                  <div className="text-[11px] text-[#9a9a9a] uppercase tracking-wide">Solved</div>
                  <div className="text-2xl font-bold text-[#e9e9e9] mt-1">{solved}</div>
                  <div className="text-[11px] text-[#2eb88a] mt-1 flex items-center gap-1">
                    <TrendingUp size={10} /> +12 this week
                  </div>
                </div>
                <div className="rounded-xl border border-[#2a2a2a] bg-[#171717] p-4">
                  <div className="text-[11px] text-[#9a9a9a] uppercase tracking-wide">Acceptance</div>
                  <div className="text-2xl font-bold text-[#e9e9e9] mt-1">68%</div>
                  <div className="text-[11px] text-[#9a9a9a] mt-1">Above average</div>
                </div>
                <div className="rounded-xl border border-[#2a2a2a] bg-[#171717] p-4">
                  <div className="text-[11px] text-[#9a9a9a] uppercase tracking-wide">Streak</div>
                  <div className="text-2xl font-bold text-[#ffa116] mt-1">{streak}🔥</div>
                  <div className="text-[11px] text-[#9a9a9a] mt-1">Personal best: 14</div>
                </div>
                <div className="rounded-xl border border-[#2a2a2a] bg-[#171717] p-4">
                  <div className="text-[11px] text-[#9a9a9a] uppercase tracking-wide">Level</div>
                  <div className="text-2xl font-bold text-[#e9e9e9] mt-1">Lv. {level}</div>
                  <div className="text-[11px] text-[#ffa116] mt-1">{xp.toLocaleString()} XP</div>
                </div>
              </div>
            </div>
          </LCard>
        </motion.div>

        {/* Main grid */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
          <div className="xl:col-span-2 space-y-5">
            {/* Problem of the day */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
              <LCard className="overflow-hidden">
                <div className="flex items-start gap-4">
                  <div className="h-12 w-12 shrink-0 rounded-xl bg-[#ffa1161a] text-[#ffa116] flex items-center justify-center">
                    <CalendarClock size={22} />
                  </div>
                  <div className="min-w-0 flex-1">
                    <span className="text-[11px] font-semibold uppercase tracking-wide text-[#9a9a9a]">Problem of the Day</span>
                    <h2 className="text-lg font-bold mt-1 truncate">
                      {daily?.title || daily?.question_title || "Today's Adaptive Challenge"}
                    </h2>
                    <p className="text-sm text-[#9a9a9a] mt-1 line-clamp-2">
                      {daily?.description || "Solve today's hand-picked problem to keep your streak alive."}
                    </p>
                    <div className="flex items-center gap-3 mt-3 text-xs text-[#9a9a9a]">
                      {daily?.difficulty && <DifficultyBadge level={daily.difficulty} />}
                      <span>·</span>
                      <span>+{daily?.xp_reward || 80} XP</span>
                    </div>
                  </div>
                  <Link
                    to={`/question/${daily?.id || daily?.question_id || "random"}`}
                    className="ml-2 shrink-0 inline-flex items-center gap-1 rounded-lg bg-[#ffa116] px-4 py-2 text-sm font-semibold text-black hover:bg-[#ffb340] transition-colors"
                  >
                    Solve <ArrowRight size={15} />
                  </Link>
                </div>
              </LCard>
            </motion.div>

            {/* Recent submissions */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
              <LCard>
                <LSectionTitle
                  title="Recent Submissions"
                  action={
                    <Link to="/question-bank" className="text-xs text-[#ffa116] hover:underline">
                      View all
                    </Link>
                  }
                />
                {recentProblems.length === 0 ? (
                  <div className="text-sm text-[#6b6b6b] py-6 text-center">
                    No submissions yet — solve a problem to see it here.
                  </div>
                ) : (
                  <div className="overflow-x-auto -mx-1">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="text-[11px] uppercase tracking-wide text-[#6b6b6b] border-b border-[#2a2a2a]">
                          <th className="text-left font-medium py-2 px-2">Status</th>
                          <th className="text-left font-medium py-2 px-2">Problem</th>
                          <th className="text-left font-medium py-2 px-2">Difficulty</th>
                          <th className="text-right font-medium py-2 px-2">When</th>
                        </tr>
                      </thead>
                      <tbody>
                        {recentProblems.map((p, i) => (
                          <tr key={p.question_id || i} className="border-b border-[#1f1f1f] hover:bg-[#1f1f1f] transition-colors">
                            <td className="py-2.5 px-2">
                              <span className="inline-flex items-center gap-1.5 text-[#2eb88a]">
                                <CheckCircle2 size={15} /> Accepted
                              </span>
                            </td>
                            <td className="py-2.5 px-2">
                              <Link to={`/question/${p.question_id || "random"}`} className="text-[#e9e9e9] hover:text-[#ffa116] transition-colors">
                                {p.title || "Problem"}
                              </Link>
                            </td>
                            <td className="py-2.5 px-2">
                              <DifficultyBadge level={p.difficulty as string} />
                            </td>
                            <td className="py-2.5 px-2 text-right text-[#9a9a9a] whitespace-nowrap">{timeAgo(p.completed_at || p.timestamp)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </LCard>
            </motion.div>
          </div>

          {/* Right column */}
          <div className="space-y-5">
            {/* Readiness */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
              <LCard>
                <LSectionTitle title="Interview Readiness" />
                <div className="flex flex-col items-center">
                  <ProgressRing value={readiness} color={LC.brand} sublabel="overall" />
                  <p className="text-xs text-[#9a9a9a] mt-3 text-center">
                    Keep practicing to reach the <span className="text-[#e9e9e9]">Software Engineer</span> target.
                  </p>
                </div>
              </LCard>
            </motion.div>

            {/* Activity */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}>
              <LCard>
                <LSectionTitle title="Activity" />
                <Heatmap data={heat} weeks={16} />
              </LCard>
            </motion.div>

            {/* Skill Coverage */}
            <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
              <LCard>
                <LSectionTitle title="Skill Coverage" />
                <SkillRadar skills={radar} />
              </LCard>
            </motion.div>
          </div>
        </div>
      </main>
    </div>
  );
}
