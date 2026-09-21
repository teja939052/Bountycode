import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  BookOpen,
  Code2,
  ListChecks,
  CalendarCheck,
  Trophy,
  Flame,
  Search,
  ChevronRight,
  Rocket,
} from "lucide-react";
import Spinner from "../components/ui/Spinner";
import { useLearning } from "../hooks/useLearning";
import {
  LNav,
  LCard,
  LSectionTitle,
  Chip,
  LC,
} from "../components/leetcode/Kit";

const QUICK_START = [
  { to: "/curriculum", icon: BookOpen, title: "Structured Courses", desc: "7 languages, 105 hands-on lessons with live previews and quizzes." },
  { to: "/compiler", icon: Code2, title: "Full Compiler", desc: "8 languages, test cases and a step-by-step visualizer." },
  { to: "/question-bank", icon: ListChecks, title: "Question Bank", desc: "100+ curated interview problems by company, topic, difficulty." },
  { to: "/daily-challenge", icon: CalendarCheck, title: "Daily Challenge", desc: "Adaptive missions that change as you improve." },
];

function LanguageCard({ lang }: { lang: any }) {
  const pct = lang.progress_pct || 0;
  const inProgress = (lang.lessons_completed || 0) > 0;
  return (
    <Link to={`/learn/${lang.id}`} className="group block">
      <LCard className="h-full transition-colors hover:border-[#ffa11655]">
        <div className="flex items-start justify-between gap-3">
          <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-[#242424] text-3xl border border-[#2a2a2a]">
            {lang.icon}
          </div>
          {inProgress && (
            <span className="rounded-full bg-[#242424] px-2.5 py-0.5 text-[10px] font-medium uppercase tracking-wider text-[#9a9a9a]">
              In progress
            </span>
          )}
        </div>
        <h3 className="mt-3 text-lg font-bold">{lang.name}</h3>
        <p className="mt-1 text-sm text-[#9a9a9a] line-clamp-2 min-h-[2.5rem]">
          {lang.description}
        </p>
        <div className="mt-3 flex flex-wrap gap-2">
          <span className="rounded-full bg-[#242424] px-2.5 py-0.5 text-[10px] font-mono text-[#9a9a9a]">
            {lang.practice_lessons} practice
          </span>
          <span className="rounded-full bg-[#242424] px-2.5 py-0.5 text-[10px] font-mono text-[#9a9a9a]">
            {lang.challenge_lessons} challenges
          </span>
          <span className="rounded-full bg-[#242424] px-2.5 py-0.5 text-[10px] font-mono text-[#9a9a9a]">
            {lang.project_lessons} projects
          </span>
        </div>
        <div className="mt-4">
          <div className="flex justify-between text-[11px] font-mono text-[#9a9a9a] mb-1">
            <span>
              {lang.lessons_completed} / {lang.total_lessons} lessons
            </span>
            <span>{pct}%</span>
          </div>
          <div className="h-1.5 rounded-full bg-[#2a2a2a] overflow-hidden">
            <div
              className="h-full rounded-full bg-[#ffa116]"
              style={{ width: `${pct}%` }}
            />
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between text-[11px] text-[#9a9a9a]">
          <span className="font-mono">{lang.total_xp} Diamonds</span>
          <ChevronRight
            size={16}
            className="text-[#6b6b6b] transition-transform group-hover:translate-x-1 group-hover:text-[#ffa116]"
          />
        </div>
      </LCard>
    </Link>
  );
}

export default function LearningHub() {
  const { data, leaderboard, isLoading, isError, refetch } = useLearning();
  const [query, setQuery] = useState("");

  const languages = useMemo(() => {
    if (!data?.languages) return [];
    const q = query.trim().toLowerCase();
    return q
      ? data.languages.filter((l: any) => l.name?.toLowerCase().includes(q))
      : data.languages;
  }, [data, query]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#0f0f0f]">
        <Spinner />
      </div>
    );
  }

  if (isError || !data) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-4 bg-[#0f0f0f] text-[#9a9a9a]">
        <div className="text-sm">Failed to load learning hub</div>
        <button
          onClick={() => refetch()}
          className="px-4 py-2 rounded-lg bg-[#ffa116] text-black text-sm font-semibold"
        >
          Retry
        </button>
      </div>
    );
  }

  const totalProjects =
    data.languages?.reduce(
      (a: number, l: any) => a + (l.project_lessons || 0),
      0
    ) || 0;

  return (
    <div className="flex min-h-screen bg-[#0f0f0f] text-[#e9e9e9]">
      <LNav />

      <main className="flex-1 min-w-0 px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        {/* Hero */}
        <div className="rounded-xl border border-[#2a2a2a] bg-gradient-to-br from-[#1c1c1c] to-[#141414] p-6 md:p-8">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-2xl">
              <span className="inline-flex items-center gap-1.5 rounded-full border border-[#ffa11655] px-3 py-1 text-[11px] font-medium text-[#ffa116]">
                <BookOpen size={12} /> Learning Hub
              </span>
              <h1 className="mt-4 text-3xl font-bold tracking-tight md:text-4xl">
                Master <span className="text-[#ffa116]">13 coding campaigns</span>
              </h1>
              <p className="mt-3 text-sm text-[#9a9a9a] leading-7">
                Lessons, challenges, projects and boss battles in one progression
                loop — from C and Python to HTML, CSS, SQL, TypeScript, React and
                Node. Pick a track, climb the ladder, keep the streak alive.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
              <div className="rounded-xl bg-[#1f1f1f] px-3 py-3 text-center">
                <div className="text-xl font-bold text-[#e9e9e9]">
                  {data.total_xp}
                </div>
                <div className="mt-1 text-[10px] uppercase tracking-wider text-[#9a9a9a]">
                  Diamonds
                </div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-3 py-3 text-center">
                <div className="text-xl font-bold text-[#e9e9e9]">
                  {data.total_lessons}
                </div>
                <div className="mt-1 text-[10px] uppercase tracking-wider text-[#9a9a9a]">
                  Lessons
                </div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-3 py-3 text-center">
                <div className="text-xl font-bold text-[#ffa116]">
                  {data.streak?.streak || 0}
                </div>
                <div className="mt-1 text-[10px] uppercase tracking-wider text-[#9a9a9a]">
                  Streak
                </div>
              </div>
              <div className="rounded-xl bg-[#1f1f1f] px-3 py-3 text-center">
                <div className="text-xl font-bold text-[#e9e9e9]">
                  {totalProjects}
                </div>
                <div className="mt-1 text-[10px] uppercase tracking-wider text-[#9a9a9a]">
                  Projects
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick start */}
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {QUICK_START.map((q) => (
            <Link key={q.to} to={q.to} className="group block">
              <LCard className="h-full transition-colors hover:border-[#ffa11655]">
                <div className="inline-flex h-11 w-11 items-center justify-center rounded-xl bg-[#242424] text-[#ffa116] border border-[#2a2a2a]">
                  <q.icon size={20} />
                </div>
                <h3 className="mt-3 font-bold">{q.title}</h3>
                <p className="mt-1.5 text-sm text-[#9a9a9a] leading-6">
                  {q.desc}
                </p>
                <span className="mt-3 inline-flex items-center gap-1 text-xs font-mono text-[#ffa116]">
                  Open <ChevronRight size={12} />
                </span>
              </LCard>
            </Link>
          ))}
        </div>

        {/* Language campaigns */}
        <LCard>
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <LSectionTitle title="Language Campaigns" />
            <div className="relative">
              <Search
                size={15}
                className="absolute left-3 top-1/2 -translate-y-1/2 text-[#6b6b6b]"
              />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Filter languages…"
                className="w-full sm:w-64 rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] py-2 pl-9 pr-3 text-sm text-[#e9e9e9] placeholder:text-[#6b6b6b] focus:border-[#ffa116] focus:outline-none"
              />
            </div>
          </div>
          {languages.length === 0 ? (
            <div className="py-8 text-center text-sm text-[#6b6b6b]">
              No languages match “{query}”.
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3 mt-4">
              {languages.map((lang: any) => (
                <LanguageCard key={lang.id} lang={lang} />
              ))}
            </div>
          )}
        </LCard>

        {/* Study library + leaderboard */}
        <div className="grid grid-cols-1 lg:grid-cols-[1.3fr_0.7fr] gap-5">
          <Link to="/study" className="group block">
            <LCard className="h-full transition-colors hover:border-[#ffa11655]">
              <div className="flex items-start gap-4">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-[#ffa1161a] text-[#ffa116]">
                  <BookOpen size={22} />
                </div>
                <div>
                  <p className="text-[10px] font-mono uppercase tracking-[0.24em] text-[#ffa116]">
                    Study library
                  </p>
                  <h2 className="mt-1 text-xl font-bold">
                    In-depth guides that go deeper than W3Schools
                  </h2>
                  <p className="mt-2 text-sm text-[#9a9a9a] leading-6">
                    The why behind the syntax — theory, analogies, real code and
                    common mistakes for HTML, CSS, JS, TS, React, Node, SQL and
                    full-stack architecture.
                  </p>
                  <span className="mt-3 inline-flex items-center gap-1 text-xs font-mono text-[#ffa116]">
                    Explore articles <ChevronRight size={14} />
                  </span>
                </div>
              </div>
            </LCard>
          </Link>

          <LCard>
            <LSectionTitle
              title="Top Learners"
              icon={<Trophy size={16} className="text-[#ffa116]" />}
            />
            {!leaderboard || leaderboard.length === 0 ? (
              <div className="py-6 text-center text-sm text-[#6b6b6b]">
                Leaderboard is empty.
              </div>
            ) : (
              <div className="space-y-2">
                {leaderboard.slice(0, 5).map((entry: any, i: number) => (
                  <div
                    key={entry.user_id}
                    className="flex items-center gap-3 rounded-lg bg-[#1f1f1f] px-3 py-2"
                  >
                    <span
                      className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold ${
                        i === 0
                          ? "bg-yellow-500/20 text-yellow-400"
                          : i === 1
                          ? "bg-[#9a9a9a]/20 text-[#cfcfcf]"
                          : i === 2
                          ? "bg-orange-500/20 text-orange-400"
                          : "bg-[#2a2a2a] text-[#9a9a9a]"
                      }`}
                    >
                      {i + 1}
                    </span>
                    <span className="flex-1 truncate text-sm">
                      {entry.name}
                    </span>
                    <span className="text-xs font-mono text-[#ffa116]">
                      {entry.total_xp} Diamonds
                    </span>
                  </div>
                ))}
              </div>
            )}
          </LCard>
        </div>

        {/* Streak aura */}
        {data.streak?.streak > 0 && (
          <LCard className="flex items-center gap-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-[#ffa1161a] text-[#ffa116]">
              <Flame size={26} />
            </div>
            <div>
              <div className="text-2xl font-bold">{data.streak.streak}</div>
              <div className="text-xs uppercase tracking-[0.2em] text-[#9a9a9a]">
                days in a row
              </div>
            </div>
            <Chip icon={<Rocket size={13} className="text-[#ffa116]" />} tone="brand">
              Keep it alive
            </Chip>
          </LCard>
        )}
      </main>
    </div>
  );
}
