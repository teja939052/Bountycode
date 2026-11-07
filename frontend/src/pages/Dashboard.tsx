import { useMemo } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import useAuthStore from "../store/authStore";
import { useDashboard } from "../hooks/useDashboard";
import api from "../services/api";
import {
  Flame,
  Trophy,
  ArrowRight,
  Clock,
  Target,
  Code2,
  BookOpen,
  Briefcase,
  MessageSquare,
  BarChart3,
  CheckCircle2,
  GraduationCap,
  RefreshCw,
  AlertCircle,
  Play,
} from "lucide-react";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";
import { ReadinessRing } from "../design-system/Progress";
import { placementRank } from "../lib/placementRank";

type PlanTask = {
  id?: string;
  type?: string;
  kind?: string;
  title?: string;
  description?: string;
  reason?: string;
  estimated_minutes?: number;
  xp_reward?: number;
  domain_id?: string;
  skill?: string;
  question_id?: string;
  to?: string;
  label?: string;
  minutes?: number;
  difficulty?: string;
  mastery_label?: string;
  emoji?: string;
};

function taskHref(task: PlanTask): string {
  if (task.to) return task.to;
  if (task.question_id) return `/question/${task.question_id}`;
  if (task.type === "next_mission" || task.kind === "lesson") return "/academy";
  if (task.type === "practice" || task.kind === "question") return "/practice";
  if (task.type === "review" || task.kind === "srs") return "/academy";
  if (task.type === "company_mission" || task.type === "company_focus") return "/academy";
  return "/academy";
}

function taskLabel(task: PlanTask, index: number): string {
  return task.title || task.label || `Task ${index + 1}`;
}

function taskReason(task: PlanTask): string {
  if (task.reason) return task.reason;
  if (task.description) return task.description;
  if (task.type === "next_mission") return "Next curriculum step on your learning path.";
  if (task.type === "practice" || task.kind === "weak_area") return "Recommended because this skill needs more evidence.";
  if (task.type === "review") return "Due for spaced repetition so you keep what you learned.";
  if (task.type === "company_mission" || task.type === "company_focus") return "Aligned to your target company track.";
  return "Part of today's personalized plan.";
}

function taskMinutes(task: PlanTask): number {
  return Number(task.estimated_minutes ?? task.minutes ?? 12) || 12;
}

export default function Dashboard() {
  const storeUser = useAuthStore((s) => s.user);
  const firstName = (storeUser?.name || "there").split(" ")[0];

  const {
    gamification,
    readinessScore,
    streakStatus,
    isLoading: dashboardLoading,
    isError,
    refetch,
  } = useDashboard();

  const {
    data: todayPlanRaw,
    isLoading: planLoading,
    isError: planError,
    refetch: refetchPlan,
  } = useQuery({
    queryKey: ["study", "today"],
    queryFn: () => api.journey.getToday(),
    staleTime: 30_000,
    retry: 1,
  });

  const {
    data: skillsRaw,
    isLoading: skillsLoading,
  } = useQuery({
    queryKey: ["adaptive", "skills"],
    queryFn: () => api.adaptive.getSkillAssessment(),
    staleTime: 60_000,
    retry: 1,
  });

  const plan = (todayPlanRaw as any)?.data ?? todayPlanRaw ?? {};
  const skillsPayload = (skillsRaw as any)?.data ?? skillsRaw ?? {};
  const skills = (skillsPayload.skills ?? skillsPayload.assessment?.skills ?? {}) as Record<
    string,
    { score: number; mastery?: string; mastery_label?: string; accuracy?: number; total_attempts?: number }
  >;

  const tasks: PlanTask[] = useMemo(() => {
    const collected: PlanTask[] = [];
    const companyMission = plan.company_mission || plan.company_focus;
    if (companyMission) {
      collected.push({
        ...companyMission,
        type: companyMission.type || "company_mission",
        title: companyMission.title || companyMission.label || "Company preparation",
      });
    }
    const next = plan.next || plan.next_mission;
    if (next) {
      collected.push({
        ...next,
        type: next.type || "next_mission",
        title: next.title || next.level?.title || next.label || "Continue your learning path",
        estimated_minutes: next.estimated_minutes ?? next.minutes ?? 15,
        xp_reward: next.xp_reward ?? next.xp ?? 40,
      });
    }
    const fromTasks = Array.isArray(plan.tasks) ? plan.tasks : [];
    for (const t of fromTasks) {
      if (!t) continue;
      collected.push(t);
    }
    const practice = Array.isArray(plan.practice) ? plan.practice : [];
    for (const t of practice) {
      if (!t) continue;
      collected.push({ ...t, type: t.type || "practice" });
    }
    const reviews = Array.isArray(plan.reviews) ? plan.reviews : [];
    for (const t of reviews.slice(0, 3)) {
      if (!t) continue;
      collected.push({
        ...t,
        type: "review",
        title: t.title || t.question || "Review a concept",
        estimated_minutes: t.estimated_minutes ?? 5,
      });
    }
    const seen = new Set<string>();
    return collected
      .filter((t) => {
        const key = `${t.type || ""}:${t.title || t.label || t.question_id || ""}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      })
      .slice(0, 8);
  }, [plan]);

  const totalMinutes = useMemo(
    () => tasks.reduce((sum, t) => sum + taskMinutes(t), 0),
    [tasks],
  );

  const weakSkills = useMemo(() => {
    return Object.entries(skills)
      .map(([id, s]) => ({ id, ...s }))
      .filter((s) => (s.total_attempts || 0) > 0 && (s.score ?? 0) < 70)
      .sort((a, b) => (a.score ?? 0) - (b.score ?? 0))
      .slice(0, 5);
  }, [skills]);

  const readiness =
    readinessScore?.score ??
    plan.overall_score ??
    skillsPayload.overall_score ??
    null;

  const streak =
    streakStatus?.current_streak ??
    gamification?.streak ??
    plan.streak ??
    storeUser?.streak ??
    0;
  const level = gamification?.level ?? plan.level ?? storeUser?.level ?? 1;
  const rank = placementRank(Number(level));

  const greeting = useMemo(() => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 18) return "Good afternoon";
    return "Good evening";
  }, []);

  const primaryTask = tasks[0];
  const primaryHref = primaryTask ? taskHref(primaryTask) : "/academy";
  const loading = dashboardLoading || planLoading || skillsLoading;

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-emerald-600 mx-auto mb-3" />
          <p className="text-sm text-slate-500">Building your plan for today…</p>
        </div>
      </div>
    );
  }

  if (isError && planError) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <AlertCircle className="mx-auto text-rose-500 mb-3" size={32} />
          <h2 className="text-lg font-bold text-slate-900">Could not load your dashboard</h2>
          <p className="text-sm text-slate-500 mt-2">
            Check your connection and try again. Your progress is safe.
          </p>
          <button
            onClick={() => {
              void refetch();
              void refetchPlan();
            }}
            className="mt-4 inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-900 text-white text-sm font-semibold"
          >
            <RefreshCw size={16} /> Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-5xl px-4 py-6 sm:py-10">
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35 }}
          className="space-y-6"
        >
          <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <p className="text-sm text-slate-500">
                {greeting}, {firstName}
              </p>
              <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-slate-900 mt-1">
                {readiness == null
                  ? "Your placement journey starts here."
                  : `You are ${Math.round(Number(readiness))}% placement-ready.`}
              </h1>
              <p className="mt-1 text-sm text-slate-600">
                Follow today's plan. Progress is measured by evidence — not coins, XP, or time spent.
              </p>
            </div>
            <div className="flex items-center gap-3 shrink-0">
              {readiness != null && (
                <div className="rounded-2xl border border-slate-200 bg-white p-3 shadow-sm">
                  <ReadinessRing value={Number(readiness)} size={72} />
                </div>
              )}
              <div className="hidden sm:flex flex-col gap-1 text-right text-xs text-slate-500">
                <span className="inline-flex items-center justify-end gap-1 font-semibold text-orange-600">
                  <Flame size={14} /> {streak} day habit
                </span>
                <span className="font-semibold text-slate-800">{rank.title}</span>
                <span className="text-[11px] text-slate-500">{rank.blurb}</span>
              </div>
            </div>
          </header>

          <section aria-label="Today's learning plan">
            <Card className="border border-emerald-200/80 bg-gradient-to-br from-white via-[#fbfaf6] to-emerald-50/40 p-5 sm:p-6 shadow-sm">
              <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4 mb-5">
                <div>
                  <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.16em] text-emerald-700">
                    <GraduationCap size={14} /> Today's learning plan
                  </p>
                  <h2 className="mt-1 text-xl font-black text-slate-900">
                    {tasks.length
                      ? `${tasks.length} focused task${tasks.length === 1 ? "" : "s"} · ~${totalMinutes} min`
                      : "Your next step is ready"}
                  </h2>
                  <p className="mt-1 text-sm text-slate-600">
                    Learn the concept, practise it, then prove you know it. Weak skills and company targets drive the order.
                  </p>
                </div>
                <Link to={primaryHref} className="shrink-0">
                  <Button variant="primary" rightIcon={<Play size={16} />} className="w-full sm:w-auto min-h-11">
                    Continue learning
                  </Button>
                </Link>
              </div>

              {tasks.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-slate-200 bg-white/70 p-6 text-center">
                  <p className="text-sm font-medium text-slate-800">No open tasks yet</p>
                  <p className="mt-1 text-sm text-slate-500">
                    Open the Academy to set your level and target companies, or start a foundational lesson.
                  </p>
                  <div className="mt-4 flex flex-wrap justify-center gap-2">
                    <Link
                      to="/academy"
                      className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white"
                    >
                      Open Academy <ArrowRight size={14} />
                    </Link>
                    <Link
                      to="/target"
                      className="inline-flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700"
                    >
                      Set target companies
                    </Link>
                  </div>
                </div>
              ) : (
                <ol className="space-y-3">
                  {tasks.map((task, index) => {
                    const href = taskHref(task);
                    const minutes = taskMinutes(task);
                    const isPrimary = index === 0;
                    return (
                      <li key={`${task.type}-${task.title}-${index}`}>
                        <Link
                          to={href}
                          className={`group flex items-start gap-3 rounded-2xl border p-3.5 transition-all ${
                            isPrimary
                              ? "border-emerald-300 bg-white shadow-sm"
                              : "border-slate-200 bg-white/80 hover:border-emerald-200 hover:bg-white"
                          }`}
                        >
                          <div
                            className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-bold ${
                              isPrimary
                                ? "bg-emerald-600 text-white"
                                : "bg-slate-100 text-slate-600"
                            }`}
                          >
                            {index + 1}
                          </div>
                          <div className="min-w-0 flex-1">
                            <div className="flex flex-wrap items-center gap-2">
                              <h3 className="font-bold text-slate-900 group-hover:text-emerald-800">
                                {taskLabel(task, index)}
                              </h3>
                              {task.type && (
                                <span className="rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-slate-600">
                                  {String(task.type).replace(/_/g, " ")}
                                </span>
                              )}
                            </div>
                            <p className="mt-1 text-sm text-slate-600 line-clamp-2">{taskReason(task)}</p>
                            <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-slate-500">
                              <span className="inline-flex items-center gap-1">
                                <Clock size={12} /> ~{minutes} min
                              </span>
                            </div>
                          </div>
                          <ArrowRight
                            size={18}
                            className="mt-1 shrink-0 text-slate-300 transition group-hover:text-emerald-600"
                          />
                        </Link>
                      </li>
                    );
                  })}
                </ol>
              )}
            </Card>
          </section>

          <section aria-label="Company mock assessment">
            <Card className="border border-indigo-200/80 bg-gradient-to-br from-white via-indigo-50/30 to-white p-5 sm:p-6 shadow-sm">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div className="min-w-0">
                  <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.16em] text-indigo-700">
                    <Briefcase size={14} /> Service-company mock
                  </p>
                  <h2 className="mt-1 text-lg font-black text-slate-900">
                    Measure placement readiness under exam conditions
                  </h2>
                  <p className="mt-1 text-sm text-slate-600">
                    Take a TCS / Infosys / Wipro style mock. Scores feed the same readiness engine as your lessons.
                  </p>
                </div>
                <div className="flex flex-wrap gap-2 shrink-0">
                  <Link
                    to="/quiz"
                    className="inline-flex min-h-10 items-center gap-2 rounded-xl bg-indigo-700 px-4 text-sm font-semibold text-white"
                  >
                    Start company mock <ArrowRight size={15} />
                  </Link>
                  <Link
                    to="/target"
                    className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-700"
                  >
                    Choose target
                  </Link>
                </div>
              </div>
            </Card>
          </section>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            <Card className="lg:col-span-2 border border-slate-200 bg-white p-5 sm:p-6">
              <div className="flex items-center gap-2 mb-4">
                <BarChart3 size={18} className="text-rose-500" />
                <h3 className="font-bold text-slate-900">Skills that need attention</h3>
              </div>
              {weakSkills.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-200 bg-slate-50 p-5 text-sm text-slate-600">
                  {Object.keys(skills).length === 0
                    ? "Complete a diagnostic or a few lessons so we can measure your strengths and gaps."
                    : "No weak skills with enough evidence yet. Keep practising — mastery updates from assessments, not time spent."}
                  <div className="mt-3">
                    <Link to="/academy" className="text-sm font-semibold text-emerald-700 hover:underline">
                      Go to Academy →
                    </Link>
                  </div>
                </div>
              ) : (
                <ul className="space-y-2">
                  {weakSkills.map((skill) => (
                    <li key={skill.id}>
                      <Link
                        to={`/academy?focus=${encodeURIComponent(skill.id)}`}
                        className="flex items-center justify-between gap-3 rounded-xl border border-slate-100 bg-slate-50/80 px-3 py-2.5 hover:border-rose-200 hover:bg-rose-50/40 transition"
                      >
                        <div className="min-w-0">
                          <p className="text-sm font-semibold text-slate-900 truncate">
                            {skill.id.replace(/_/g, " ")}
                          </p>
                          <p className="text-xs text-slate-500">
                            {skill.mastery_label || "Needs work"} · {Math.round(skill.score ?? 0)}% ·{" "}
                            {skill.total_attempts || 0} attempts
                          </p>
                        </div>
                        <span className="shrink-0 text-xs font-semibold text-rose-700">Practise →</span>
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </Card>

            <Card className="border border-slate-200 bg-white p-5 sm:p-6">
              <div className="flex items-center gap-2 mb-4">
                <Trophy size={18} className="text-amber-500" />
                <h3 className="font-bold text-slate-900">Progress support</h3>
              </div>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-full bg-orange-50 text-orange-600">
                      <Flame size={18} />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-slate-900">Habit streak</p>
                      <p className="text-xs text-slate-500">Consistency, not perfection</p>
                    </div>
                  </div>
                  <span className="text-lg font-black text-slate-900">{streak}</span>
                </div>
                <div className="flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="flex h-9 w-9 items-center justify-center rounded-full bg-emerald-50 text-emerald-600">
                      <Target size={18} />
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-slate-900">Placement rank</p>
                      <p className="text-xs text-slate-500 truncate">{rank.blurb}</p>
                    </div>
                  </div>
                  <span className="text-sm font-black text-slate-900 text-right shrink-0">{rank.title}</span>
                </div>
                {readiness != null && (
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-50 text-indigo-600">
                        <CheckCircle2 size={18} />
                      </div>
                      <div>
                        <p className=