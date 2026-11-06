import { useQuery } from "@tanstack/react-query";
import { ArrowRight, BookOpen, CalendarDays, Clock, Target } from "lucide-react";
import { Link } from "react-router-dom";
import api from "../../services/api";

export default function AcademyPersonalPlan() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["academy", "plan"],
    queryFn: () => api.academy.getPlan(),
    staleTime: 60_000,
    retry: false,
  });
  if (isLoading) return null;
  if (error) return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5">
      <p className="font-bold text-slate-900">Your personalized plan is waiting</p>
      <p className="mt-1 text-sm text-slate-600">Save your learning profile first. Complete the diagnostic to make the plan evidence-based.</p>
      <Link to="#academy-profile" className="mt-3 inline-flex items-center gap-2 text-sm font-semibold text-emerald-700">Set up profile <ArrowRight size={14}/></Link>
    </section>
  );
  const plan = (data as any)?.plan;
  if (!plan) return null;
  return (
    <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-emerald-700"><CalendarDays size={14}/> Your personalized plan</p>
          <h2 className="mt-2 text-xl font-black text-slate-900">A daily path towards {String(plan.target_role || "your goal").replaceAll("_", " ")}</h2>
          <p className="mt-1 text-sm text-slate-600">{plan.personalization_note}</p>
        </div>
        <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700"><Clock className="mr-1 inline" size={13}/>{plan.daily_minutes} min/day</span>
      </div>
      {plan.daily_tasks?.length ? (
        <div className="mt-5 space-y-3">
          {plan.daily_tasks.map((task: any, index: number) => (
            <div key={task.domain} className="flex items-start gap-3 rounded-2xl border border-slate-100 p-3">
              <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-50 text-sm font-black text-emerald-800">{index + 1}</span>
              <div className="min-w-0 flex-1">
                <div className="flex flex-wrap items-center gap-2"><p className="font-semibold text-slate-900">{task.title}</p>{task.priority === "high" && <span className="rounded-full bg-amber-50 px-2 py-0.5 text-[10px] font-bold uppercase text-amber-800">Priority</span>}</div>
                <p className="mt-1 text-sm text-slate-600">{task.reason}</p>
                <p className="mt-1 text-xs text-slate-500">{task.estimated_minutes} min · {String(task.skill_level).replaceAll("_", " ")}</p>
              </div>
              {task.lesson_slug && <Link to={`/learn/lesson/${task.lesson_slug}`} aria-label={`Open ${task.title} lesson`} className="rounded-lg p-2 text-emerald-700 hover:bg-emerald-50"><BookOpen size={17}/></Link>}
            </div>
          ))}
        </div>
      ) : <p className="mt-4 text-sm text-slate-600">Complete your diagnostic to generate your first set of tasks.</p>}
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
