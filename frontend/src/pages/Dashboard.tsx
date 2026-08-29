import { useMemo } from "react";
import { Link } from "react-router-dom";
import { Flame, Zap, CheckCircle2, ArrowRight, CalendarClock } from "lucide-react";
import useAuthStore from "../store/authStore";
import { useDashboard } from "../hooks/useDashboard";
import PageSkeleton from "../components/PageSkeleton";
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

  const heat = useMemo(
    () => Array.from({ length: 16 * 7 }, () => Math.floor(Math.random() * 5)),
    []
  );

  if (isLoading) return <PageSkeleton />;

  if (isError) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0f0f0f]">
        <div className="text-center">
          <h2 className="text-lg font-bold text-[#e9e9e9]">
            Failed to load dashboard
          </h2>
          <button
            onClick={() => refetch()}
            className="mt-4 px-5 py-2 rounded-lg bg-[#ffa116] text-black text-sm font-semibold"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const daily = dailyChallenge;
  const firstName = user?.name?.split(" ")[0] || "there";

  return (
    <div className="flex min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <LNav />

      <main className="flex-1 min-w-0 px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {/* Header */}
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              Welcome back, {firstName}
            </h1>
            <p className="text-sm text-[#9a9a9a] mt-1">
              Software Engineer track ·{" "}
              <span className="text-[#ffa116] font-medium">
                {readiness}% interview ready
              </span>
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Chip icon={<Flame size={13} className="text-[#ffa116]" />} tone="brand">
              {streak} day streak
            </Chip>
            <Chip icon={<Zap size={13} className="text-[#ffa116]" />} tone="brand">
              {xp} XP
            </Chip>
            <Chip tone="neutral">Level {level}</Chip>
          </div>
        </div>

        {/* Stat row */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <LStat label="Problems Solved" value={solved} accent={LC.green} />
          <LStat
            label="Easy"
            value={questionStats?.easy || 0}
            accent={LC.easy}
          />
          <LStat
            label="Medium"
            value={questionStats?.medium || 0}
            accent={LC.medium}
          />
          <LStat
            label="Hard"
            value={questionStats?.hard || 0}
            accent={LC.hard}
          />
        </div>

        {/* Main grid */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-5">
          {/* Left: problem of the day + recent */}
          <div className="xl:col-span-2 space-y-5">
            {/* Problem of the day */}
            <LCard className="overflow-hidden">
              <div className="flex items-start gap-4">
                <div className="h-12 w-12 shrink-0 rounded-xl bg-[#ffa1161a] text-[#ffa116] flex items-center justify-center">
                  <CalendarClock size={22} />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-semibold uppercase tracking-wide text-[#9a9a9a]">
                      Problem of the Day
                    </span>
                  </div>
                  <h2 className="text-lg font-bold mt-1 truncate">
                    {daily?.title ||
                      daily?.question_title ||
                      "Today's Adaptive Challenge"}
                  </h2>
                  <p className="text-sm text-[#9a9a9a] mt-1 line-clamp-2">
                    {daily?.description ||
                      "Solve today's hand-picked problem to keep your streak alive."}
                  </p>
                  <div className="flex items-center gap-3 mt-3 text-xs text-[#9a9a9a]">
                    {daily?.difficulty && (
                      <DifficultyBadge level={daily.difficulty} />
                    )}
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

            {/* Recent submissions */}
            <LCard>
              <LSectionTitle
                title="Recent Submissions"
                action={
                  <Link
                    to="/question-bank"
                    className="text-xs text-[#ffa116] hover:underline"
                  >
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
                        <tr
                          key={p.question_id || i}
                          className="border-b border-[#1f1f1f] hover:bg-[#1f1f1f] transition-colors"
                        >
                          <td className="py-2.5 px-2">
                            <span className="inline-flex items-center gap-1.5 text-[#2eb88a]">
                              <CheckCircle2 size={15} /> Accepted
                            </span>
                          </td>
                          <td className="py-2.5 px-2">
                            <Link
                              to={`/question/${p.question_id || "random"}`}
                              className="text-[#e9e9e9] hover:text-[#ffa116] transition-colors"
                            >
                              {p.title || "Problem"}
                            </Link>
                          </td>
                          <td className="py-2.5 px-2">
                            <DifficultyBadge level={p.difficulty as string} />
                          </td>
                          <td className="py-2.5 px-2 text-right text-[#9a9a9a] whitespace-nowrap">
                            {timeAgo(p.completed_at || p.timestamp)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </LCard>
          </div>

          {/* Right: readiness + heatmap + radar */}
          <div className="space-y-5">
            <LCard>
              <LSectionTitle title="Interview Readiness" />
              <div className="flex flex-col items-center">
                <ProgressRing
                  value={readiness}
                  color={LC.brand}
                  sublabel="overall"
                />
                <p className="text-xs text-[#9a9a9a] mt-3 text-center">
                  Keep practicing to reach the{" "}
                  <span className="text-[#e9e9e9]">Software Engineer</span>{" "}
                  target.
                </p>
              </div>
            </LCard>

            <LCard>
              <LSectionTitle title="Activity" />
              <Heatmap data={heat} weeks={16} />
            </LCard>

            <LCard>
              <LSectionTitle title="Skill Coverage" />
              <SkillRadar skills={radar} />
            </LCard>
          </div>
        </div>
      </main>
    </div>
  );
}
