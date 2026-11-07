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
  Briefcase,
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
  type?: string;
  kind?: string;
  title?: string;
  description?: string;
  reason?: string;
  estimated_minutes?: number;
  xp_reward?: number;
  question_id?: string;
  to?: string;
  label?: string;
  minutes?: number;
};

function taskHref(task: PlanTask): string {
  if (task.to) return task.to;
  if (task.question_id) return `/question/${task.question_id}`;
  if (task.type === "practice" || task.kind === "question") return "/practice";
  return "/academy";
}

function taskLabel(task: PlanTask, index: number): string {
  return task.title || task.label || `Task ${index + 1}`;
}

function taskReason(task: PlanTask): string {
  if (task.reason) return task.reason;
  if (task.description) return task.description;
  if (task.type === "practice") return "Recommended because this skill needs more evidence.";
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

  const { data: skillsRaw, isLoading: skillsLoading } = useQuery({
    queryKey: ["adaptive", "skills"],
    queryFn: () => api.adaptive.getSkillAssessment(),
    staleTime: 60_000,
    retry: 1,
  });

  const plan = (todayPlanRaw as any)?.data ?? todayPlanRaw ?? {};
  const skillsPayload = (skillsRaw as any)?.data ?? skillsRaw ?? {};
  const skills = (skillsPayload.skills ?? skillsPayload.assessment?.skills ?? {}) as Record<
    string,
    { score: number; mastery_label?: string; total_attempts?: number }
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
      });
    }
    for (const t of Array.isArray(plan.tasks) ? plan.tasks : []) if (t) collected.push(t);
    for (const t of Array.isArray(plan.practice) ? plan.practice : []) {
      if (t) collected.push({ ...t, type: t.type || "practice" });
    }
    for (const t of (Array.isArray(plan.reviews) ? plan.reviews : []).slice(0, 3)) {
      if (t) {
        collected.push({
          ...t,
          type: "review",
          title: t.title || t.question || "Review a concept",
          estimated_minutes: t.estimated_minutes ?? 5,
        });
      }
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

  const totalMinutes = useMemo(() => tasks.reduce((sum, t) => sum + taskMinutes(t), 0), [tasks]);

  const weakSkills = useMemo(() => {
    return Object.entries(skills)
      .map(([id, s]) => ({ id, ...s }))
      .filter((s) => (s.total_attempts || 0) > 0 && (s.score ?? 0) < 70)
      .sort((a, b) => (a.score ?? 0) - (b.score ?? 0))
      .slice(0, 5);
  }, [skills]);

  const readiness = readinessScore?.score ?? plan.overall_score ?? skillsPayload.overall_score ?? null;
  const streak =
    streakStatus?.current_streak ?? gamification?.streak ?? plan.streak ?? storeUser?.streak ?? 0;
  const level = gamification?.level ?? plan.level ?? storeUser?.level ?? 1;
  const rank = placementRank(Number(level));

  const greeting = useMemo(() => {
    const h = new Date().getHours();
    if (h < 12) return "Good morning";
    if (h < 18) return "Good afternoon";
    return "Good evening";
  }, []);

  const primaryHref = tasks[0] ? taskHref(tasks[0]) : "/academy";
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
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
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
                </div>
                <Link to={primaryHref} className="shrink-0">
                  <Button variant="primary" rightIcon={<Play size={16} />} className="w-full sm:w-auto min-h-11">
                    Continue learning
                  </Button>
                </Link>
              </div>
              {tasks.length === 0 ? (
                <div className="rounded-2xl border border-dashed border-slate-200 bg-white/70 p-6 text-center">
                  <Link to="/academy" className="inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white">
                    Open Academy <ArrowRight size={14} />
                  </Link>
                </div>
              ) : (
                <ol className="space-y-3">
                  {tasks.map((task, index) => {
                    const isPrimary = index === 0;
                    return (
                      <li key={`${task.type}-${task.title}-${index}`}>
                        <Link
                          to={taskHref(task)}
                          className={`group flex items-start gap-3 rounded-2xl border p-3.5 transition-all ${
                            isPrimary
                              ? "border-emerald-300 bg-white shadow-sm"
                              : "border-slate-200 bg-white/80 hover:border-emerald-200"
                          }`}
                        >
                          <div
                            className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-bold ${
                              isPrimary ? "bg-emerald-600 text-white" : "bg-slate-100 text-slate-600"
                            }`}
                          >
                            {index + 1}
                          </div>
                          <div className="min-w-0 flex-1">
                            <h3 className="font-bold text-slate-900">{taskLabel(task, index)}</h3>
                            <p className="mt-1 text-sm text-slate-600 line-clamp-2">{taskReason(task)}</p>
                            <div className="mt-2 text-xs text-slate-500 inline-flex items-center gap-1">
                              <Clock size={12} /> ~{taskMinutes(task)} min
                            </div>
                          </div>
                          <ArrowRight size={18} className="mt-1 shrink-0 text-slate-300" />
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
                <div>
                  <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.16em] text-indigo-700">
                    <Briefcase size={14} /> Service-company mock
                  </p>
                  <h2 className="mt-1 text-lg font-black text-slate-900">Measure readiness under exam conditions</h2>
                  <p className="mt-1 text-sm text-slate-600">
                    TCS / Infosys / Wipro style mocks feed the same readiness engine as your lessons.
                  </p>
                </div>
                <div className="flex flex-wrap gap-2 shrink-0">
                  <Link to="/quiz" className="inline-flex min-h-10 items-center gap-2 rounded-xl bg-indigo-700 px-4 text-sm font-semibold text-white">
                    Start company mock <ArrowRight size={15} />
                  </Link>
                  <Link to="/target" className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-700">
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
                  Mastery updates from assessments, not time spent.{" "}
                  <Link to="/academy" className="font-semibold text-emerald-700 hover:underline">
                    Go to Academy →
                  </Link>
                </div>
              ) : (
                <ul className="space-y-2">
                  {weakSkills.map((skill) => (
                    <li key={skill.id}>
                      <Link
                        to={`/academy?focus=${encodeURIComponent(skill.id)}`}
                        className="flex items-center justify-between gap-3 rounded-xl border border-slate-100 bg-slate-50/80 px-3 py-2.5 hover:border-rose-200 transition"
                      >
                        <div className="min-w-0">
                          <p className="text-sm font-semibold text-slate-900 truncate">
                            {skill.id.replace(/_/g, " ")}
                          </p>
                          <p className="text-xs text-slate-500">
                            {skill.mastery_label || "Needs work"} · {Math.round(skill.score ?? 0)}%
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
                  <div className=