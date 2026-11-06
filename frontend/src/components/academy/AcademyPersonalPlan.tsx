import { useQuery } from "@tanstack/react-query";
import { ArrowRight, BookOpen, CalendarDays, Clock, Target } from "lucide-react";
import { Link } from "react-router-dom";
import api from "../../services/api";

export default function AcademyPersonalPlan() {
  const { data, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ["academy", "plan"],
    queryFn: () => api.academy.getPlan(),
    staleTime: 60_000,
    retry: false,
  });
  if (isLoading) return (
    <section aria-label="Loading personalized plan" className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="h-3 w-40 animate-pulse rounded bg-slate-100" />
      <div className="mt-3 h-6 w-3/4 animate-pulse rounded bg-slate-100" />
      <div className="mt-5 space-y-3">
        <div className="h-16 animate-pulse rounded-2xl bg-slate-50" />
        <div className="h-16 animate-pulse rounded-2xl bg-slate-50" />
      </div>
    </section>
  );
  if (error) return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
      <p className="font-bold text-slate-900">Your learning plan could not load</p>
      <p className="mt-1 text-sm text-slate-600">Your progress is safe. Try again, or open the Academy to review your profile and diagnostic.</p>
      <div className="mt-3 flex flex-wrap gap-3">
        <button type="button" onClick={() => void refetch()} disabled={isFetching} className="inline-flex items-center gap-2 rounded-xl bg-emerald-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60">{isFetching ? "Retrying…" : "Try again"}</button>
        <Link to="/academy#academy-profile" className="inline-flex items-center gap-2 text-sm font-semibold text-emerald-700">Open Academy <ArrowRight size={14}/></Link>
      </div>
    </section>
  );
  const plan = (data as any)?.plan;
  if (!plan) return null;
  const nextTask = (plan.daily_tasks || []).find((task: any) => task.lesson_slug);
  const nextSkill = (plan.curriculum || []).find((skill: any) => skill.lesson_slug);
  const continueHref = nextTask?.lesson_slug
    ? `/learn/lesson/${nextTask.lesson_slug}`
    : nextSkill?.lesson_slug
      ? `/learn/lesson/${nextSkill.lesson_slug}`
      : "/academy#academy-profile";
  const continueTitle = nextTask?.title || nextSkill?.title || "Set up your learning profile";
  const continueReason = nextTask?.reason || nextSkill?.reason || "Choose your target role and companies, then complete your diagnostic to build a plan.";
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="mb-5 flex flex-col gap-3 rounded-2xl border border-emerald-200 bg-emerald-50/70 p-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <p className="text-xs font-bold uppercase tracking-[0.14em] text-emerald-800">Your next best action</p>
          <p className="mt-1 text-lg font-black text-slate-900">{continueTitle}</p>
          <p className="mt-1 text-sm leading-5 text-slate-600">{continueReason}</p>
          {nextTask?.estimated_minutes && <p className="mt-2 text-xs font-semibold text-slate-500">{nextTask.estimated_minutes} minutes · Based on your learning evidence</p>}
        </div>
        <Link to={continueHref} className="inline-flex min-h-11 shrink-0 items-center justify-center gap-2 rounded-xl bg-emerald-700 px-5 py-3 text-sm font-bold text-white transition hover:bg-emerald-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-700">
          {nextTask || nextSkill ? "Continue learning" : "Build my learning plan"} <ArrowRight size={16}/>
        </Link>
      </div>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-emerald-700"><CalendarDays size={14}/> Your personalized plan</p>
          <h2 className="mt-2 text-xl font-black text-slate-900">A daily path towards {String(plan.target_role || "your goal").replaceAll("_", " ")}</h2>
          <p className="mt-1 text-sm text-slate-600">{plan.personalization_note}</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700"><Clock className="mr-1 inline" size={13}/>{plan.daily_minutes} min/day</span>
      </div>
      {plan.overall_mastery && (
        <div className="mt-4 flex flex-wrap gap-2">
          <span className="rounded-full bg-emerald-50 px-3 py-1.5 text-xs font-semibold text-emerald-800">Current mastery: {plan.overall_mastery}</span>
          {typeof plan.overall_accuracy === "number" && <span className="rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700">Practice accuracy: {plan.overall_accuracy}%</span>}
        </div>
      )}
      {plan.curriculum?.length > 0 && (
        <div className="mt-5">
          <div className="mb-2 flex items-center justify-between gap-2">
            <p className="text-sm font-bold text-slate-800">Skill snapshot</p>
            <span className="text-xs text-slate-500">Lowest-priority gaps first</span>
          </div>
          <div className="grid gap-2 sm:grid-cols-2">
            {plan.curriculum.slice(0, 4).map((skill: any, index: number) => {
              const score = typeof skill.effective_score === "number"
                ? Math.max(0, Math.min(100, Math.round(skill.effective_score)))
                : null;
              const content = (
                <>
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-sm font-semibold text-slate-800">{skill.title}</span>
                    <span className="shrink-0 text-xs font-bold text-slate-600">{score === null ? "Not assessed" : `${score}%`}</span>
                  </div>
                  <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full rounded-full bg-emerald-600" style={{ width: `${score ?? 0}%` }} />
                  </div>
                  <p className="mt-1 text-xs text-slate-500">{String(skill.skill_level || "not assessed").replaceAll("_", " ")}</p>
                </>
              );
              return skill.lesson_slug ? (
                <Link key={skill.domain || index} to={`/learn/lesson/${skill.lesson_slug}`} className="rounded-xl border border-slate-200 p-3 transition hover:border-emerald-400 hover:bg-emerald-50/40">
                  {content}
                </Link>
              ) : (
                <div key={skill.domain || index} className="rounded-xl border border-slate-200 p-3">
                  {content}
                </div>
              );
            })}
          </div>
        </div>
      )}
      {plan.daily_tasks?.length ? (
        <div className="mt-5 space-y-3">
          {plan.daily_tasks.map((task: any, index: number) => (
            <div key={task.id || `${task.domain || task.title || "task"}-${index}`} className="flex items-start gap-3 rounded-2xl border border-slate-100 p-3">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-50 text-sm font-black text-emerald-800">{index + 1}</span>
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2"><p className="font-semibold text-slate-900">{task.title}</p>{task.priority === "high" && <span className="rounded-full bg-amber-50 px-2 py-0.5 text-[10px] font-bold uppercase text-amber-800">Priority</span>}</div>
                <p className="mt-1 text-sm text-slate-600">{task.reason}</p>
                <p className="mt-1 text-xs text-slate-500">{Number.isFinite(Number(task.estimated_minutes)) ? `${Number(task.estimated_minutes)} min` : "Practice"} · {String(task.skill_level || "recommended").replaceAll("_", " ")}{task.effective_score !== null && task.effective_score !== undefined ? ` · ${task.effective_score}% evidence` : ""}</p>
              </div>
              {task.lesson_slug && <Link to={`/learn/lesson/${task.lesson_slug}`} aria-label={`Open ${task.title} lesson`} className="rounded-lg p-2 text-emerald-700 hover:bg-emerald-50"><BookOpen size={17}/></Link>}
            </div>
          ))}
        </div>
      ) : <p className="mt-4 text-sm text-slate-600">Complete your diagnostic to generate your first set of tasks.</p>}
      {plan.study_routine?.length > 0 && (
        <div className="mt-5 rounded-2xl bg-slate-50 p-4">
          <p className="text-sm font-bold text-slate-800">A simple study rhythm</p>
          <p className="mt-1 text-xs text-slate-500">A repeatable structure for your available study time.</p>
          <div className="mt-3 grid gap-2 sm:grid-cols-2">
            {plan.study_routine.map((step: any, index: number) => (
              <div key={step.label || index} className="flex items-center justify-between gap-3 rounded-xl bg-white px-3 py-2.5">
                <span className="text-sm text-slate-700">{step.label}</span>
                <span className="shrink-0 text-xs font-bold text-slate-500">{Number(step.minutes) || 0} min</span>
              </div>
            ))}
          </div>
        </div>
      )}
      {Number(plan.revision?.due_count || 0) > 0 && (
        <div className="mt-5 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-4">
          <div>
            <p className="font-semibold text-amber-950">{plan.revision.due_count} spaced-repetition reviews due</p>
            <p className="mt-1 text-sm text-amber-900/80">Revisit previously solved problems so the concepts stay fresh.</p>
          </div>
          <Link to="/quiz" className="rounded-xl bg-white px-4 py-2 text-sm font-bold text-amber-900">Practice now</Link>
        </div>
      )}
      {plan.company_preparation?.length > 0 && (
        <div className="mt-5">
          <p className="mb-2 text-sm font-bold text-slate-800">Your selected company tracks</p>
          <div className="grid gap-2 sm:grid-cols-2">
            {plan.company_preparation.map((track: any) => (
              <Link key={track.id} to={`/tracks/${track.company_id}`} className="rounded-xl border border-slate-200 p-3 transition hover:border-emerald-400 hover:bg-emerald-50/40">
                <p className="font-semibold text-slate-900">{track.name}</p>
                <p className="mt-1 line-clamp-2 text-xs text-slate-500">{track.description}</p>
              </Link>
            ))}
          </div>
        </div>
      )}
      <div className="mt-5 flex flex-wrap items-center justify-between gap-3 border-t border-slate-100 pt-4">
        <p className="text-xs text-slate-500">Companies: {(plan.target_companies || []).join(", ") || "Choose your target companies in your profile"}</p>
        <span className="inline-flex items-center gap-1 text-xs font-semibold text-slate-500"><Target size={13}/> Skill evidence, not guesswork</span>
      </div>
    </section>
  );
}
