import { useQuery } from "@tanstack/react-query";
import { ArrowRight, BookOpen, Building2, Target } from "lucide-react";
import { Link } from "react-router-dom";
import api from "../../services/api";

const stateStyles: Record<string, string> = {
  foundation_needed: "bg-amber-50 text-amber-800",
  beginner: "bg-orange-50 text-orange-800",
  developing: "bg-blue-50 text-blue-800",
  strong: "bg-emerald-50 text-emerald-800",
  not_assessed: "bg-slate-100 text-slate-600",
};

export default function AcademyPersonalPlan() {
  const { data, isLoading, error, refetch, isFetching } = useQuery({
    queryKey: ["academy", "plan"],
    queryFn: () => api.academy.getPlan(),
    staleTime: 60_000,
    retry: false,
  });

  if (isLoading) {
    return (
      <section aria-label="Loading learning roadmap" className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div className="h-3 w-40 animate-pulse rounded bg-slate-100" />
        <div className="mt-3 h-6 w-3/4 animate-pulse rounded bg-slate-100" />
        <div className="mt-5 grid gap-3 sm:grid-cols-2">
          <div className="h-24 animate-pulse rounded-2xl bg-slate-50" />
          <div className="h-24 animate-pulse rounded-2xl bg-slate-50" />
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section aria-label="Learning roadmap unavailable" className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
        <p className="font-bold text-slate-900">Your learning roadmap could not load</p>
        <p className="mt-1 text-sm text-slate-600">Your saved progress is safe. Retry the roadmap or review your learner profile.</p>
        <div className="mt-3 flex flex-wrap gap-3">
          <button
            type="button"
            onClick={() => void refetch()}
            disabled={isFetching}
            className="inline-flex min-h-10 items-center gap-2 rounded-xl bg-emerald-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-60"
          >
            {isFetching ? "Retrying…" : "Try again"}
          </button>
          <Link to="/academy#academy-profile" className="inline-flex items-center gap-2 text-sm font-semibold text-emerald-700">
            Review profile <ArrowRight size={14} />
          </Link>
        </div>
      </section>
    );
  }

  const plan = (data as any)?.plan;
  if (!plan) return null;

  const curriculum = Array.isArray(plan.curriculum) ? plan.curriculum : [];
  const companyPreparation = Array.isArray(plan.company_preparation) ? plan.company_preparation : [];
  const targetCompanies = Array.isArray(plan.target_companies) ? plan.target_companies : [];
  const roleLabel = String(plan.target_role || "your goal").replaceAll("_", " ");
  const mockCompany = targetCompanies.find((company: string) => ["tcs", "infosys", "wipro", "cognizant"].includes(company)) || "general";

  return (
    <section aria-label="Your learning roadmap" className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-emerald-700">
            <Target size={14} /> Learning roadmap
          </p>
          <h2 className="mt-2 text-xl font-black text-slate-900">
            Skills to build for {roleLabel}
          </h2>
          <p className="mt-1 max-w-2xl text-sm leading-6 text-slate-600">
            {plan.personalization_note || "Your longer-term priorities are based on your profile and available assessment signals."}
          </p>
          {plan.learning_strategy && (
            <div className="mt-3 max-w-2xl rounded-xl border border-slate-200 bg-slate-50 p-3">
              <p className="text-[10px] font-bold uppercase tracking-wider text-emerald-700">Your study approach</p>
              <p className="mt-1 text-sm leading-5 text-slate-700">{plan.learning_strategy}</p>
              <p className="mt-2 text-xs text-slate-500">
                Level: {String(plan.experience_level || "absolute_beginner").replaceAll("_", " ")}
                {" · "}Language: {String(plan.preferred_language || "cpp").toUpperCase()}
                {" · "}Style: {String(plan.learning_preference || "mixed").replaceAll("_", " ")}
              </p>
            </div>
          )}
        </div>
        <Link
          to="/academy#academy-profile"
          className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 transition hover:border-emerald-400 hover:bg-emerald-50"
        >
          Edit goals <ArrowRight size={14} />
        </Link>
      </div>

      {Array.isArray(plan.level_path) && plan.level_path.length > 0 && (
        <div className="mt-5 rounded-2xl border border-indigo-200 bg-indigo-50/50 p-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-indigo-700">Your placement campaign</p>
              <p className="mt-1 text-sm font-bold text-slate-900">Level {Number(plan.current_level || 0) + 1}: {plan.level_path[Number(plan.current_level || 0)]?.title || "Orientation"}</p>
              <p className="mt-1 text-xs text-slate-600">{plan.assessment_track_label || "Service-company core"} · {plan.level_path[Number(plan.current_level || 0)]?.focus}</p>
            </div>
            <Link to={`/mock-oa?company=${encodeURIComponent(mockCompany)}`} className="inline-flex min-h-9 items-center gap-2 rounded-xl bg-indigo-700 px-3 py-2 text-xs font-bold text-white hover:bg-indigo-800">Try a mock <ArrowRight size={13} /></Link>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-1.5 sm:grid-cols-6">
            {plan.level_path.map((level: any) => (
              <div key={level.id} className={`rounded-xl border px-2 py-2 ${level.status === "current" ? "border-indigo-500 bg-white shadow-sm" : level.status === "complete" ? "border-emerald-200 bg-emerald-50" : "border-slate-200 bg-white/60"}`}>
                <p className="text-[10px] font-black uppercase tracking-wide text-slate-500">L{Number(level.id) + 1}</p>
                <p className="mt-1 truncate text-[11px] font-bold text-slate-800">{level.title}</p>
                <p className="mt-1 text-[10px] text-slate-500">{level.status === "complete" ? "Complete" : level.status === "current" ? "Now" : "Next"}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {plan.assessment_blueprint && (
        <div className="mt-4 rounded-2xl border border-amber-200 bg-amber-50/60 p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-amber-800">Assessment blueprint</p>
              <p className="mt-1 text-sm font-bold text-slate-900">{plan.assessment_blueprint.source_label}</p>
              <p className="mt-1 text-xs text-slate-600">{plan.assessment_blueprint.sections?.join(" · ")}</p>
            </div>
            <div className="text-right">
              <p className="text-sm font-black text-slate-900">{plan.assessment_blueprint.duration_minutes ? `${plan.assessment_blueprint.duration_minutes} min` : "Invitation-specific"}</p>
              <p className="text-[10px] font-semibold uppercase tracking-wide text-amber-800">{plan.assessment_blueprint.confidence}</p>
            </div>
          </div>
          <p className="mt-3 text-xs leading-5 text-amber-900">{plan.assessment_blueprint.notice}</p>
          <div className="mt-3 flex flex-wrap items-center justify-between gap-2 border-t border-amber-200/80 pt-3 text-xs">
            <span className="font-semibold text-slate-700">This week: {plan.weekly_minutes || plan.daily_minutes * 5} focused minutes</span>
            {plan.assessment_blueprint.source_url && <a href={plan.assessment_blueprint.source_url} target="_blank" rel="noreferrer" className="font-bold text-amber-900 underline">Read source</a>}
          </div>
          {plan.assessment_readiness?.action && <p className="mt-2 text-xs font-semibold text-indigo-800">Next readiness step: {plan.assessment_readiness.action}</p>}
        </div>
      )}

      {curriculum.length > 0 ? (
        <div className="mt-5">
          <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm font-bold text-slate-800">Learning priorities</p>
            <span className="text-xs text-slate-500">Prerequisites are considered in the ordering</span>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            {curriculum.slice(0, 6).map((skill: any, index: number) => {
              const state = String(skill.skill_level || "not_assessed");
              const baselineScore = typeof skill.diagnostic_score === "number"
                ? Math.max(0, Math.min(100, Math.round(skill.diagnostic_score)))
                : null;
              const stateLabel = state.replaceAll("_", " ");
              const card = (
                <>
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <p className="font-semibold text-slate-900">{skill.title || String(skill.domain || "Skill").replaceAll("_", " ")}</p>
                    <span className={`rounded-full px-2.5 py-1 text-[10px] font-bold capitalize ${stateStyles[state] || stateStyles.not_assessed}`}>
                      {stateLabel}
                    </span>
                  </div>
                  <p className="mt-2 text-sm leading-5 text-slate-600">{skill.reason || "Continue building this skill through lessons and practice."}</p>
                  {baselineScore !== null && (
                    <p className="mt-2 text-xs font-semibold text-slate-500">Baseline assessment: {baselineScore}%</p>
                  )}
                  {skill.prerequisite_status === "needs_foundation" && (
                    <p className="mt-2 text-xs font-semibold text-amber-700">A prerequisite needs attention first</p>
                  )}
                  {skill.lesson_slug && (
                    <p className="mt-3 inline-flex items-center gap-1 text-xs font-bold text-emerald-700">
                      <BookOpen size={13} /> Open lesson <ArrowRight size={13} />
                    </p>
                  )}
                </>
              );
              return skill.lesson_slug ? (
                <Link
                  key={skill.domain || index}
                  to={`/learn/lesson/${skill.lesson_slug}`}
                  className="rounded-2xl border border-slate-200 p-4 transition hover:border-emerald-400 hover:bg-emerald-50/40 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-emerald-700"
                >
                  {card}
                </Link>
              ) : (
                <div key={skill.domain || index} className="rounded-2xl border border-slate-200 p-4">
                  {card}
                </div>
              );
            })}
          </div>
          {curriculum.length > 6 && (
            <p className="mt-3 text-xs text-slate-500">Showing the first six priorities. Your full curriculum remains available in the Academy.</p>
          )}
        </div>
      ) : (
        <div className="mt-5 rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-5">
          <p className="font-semibold text-slate-900">Your roadmap is not ready yet</p>
          <p className="mt-1 text-sm text-slate-600">Complete your learner profile and baseline diagnostic to create a useful starting point.</p>
          <Link to="/academy#academy-profile" className="mt-3 inline-flex items-center gap-2 text-sm font-bold text-emerald-700">
            Set up your profile <ArrowRight size={14} />
          </Link>
        </div>
      )}

      {companyPreparation.length > 0 && (
        <div className="mt-6 border-t border-slate-100 pt-5">
          <p className="mb-3 flex items-center gap-2 text-sm font-bold text-slate-800">
            <Building2 size={15} /> Selected company tracks
          </p>
          <div className="grid gap-2 sm:grid-cols-2">
            {companyPreparation.map((track: any) => (
              <Link
                key={track.id}
                to={`/tracks/${track.company_id}`}
                className="rounded-xl border border-slate-200 p-3 transition hover:border-emerald-400 hover:bg-emerald-50/40"
              >
                <p className="font-semibold text-slate-900">{track.name}</p>
                <p className="mt-1 line-clamp-2 text-xs text-slate-500">{track.description}</p>
              </Link>
            ))}
          </div>
        </div>
      )}

      <div className="mt-5 flex flex-wrap items-center justify-between gap-2 border-t border-slate-100 pt-4">
        <p className="text-xs text-slate-500">
          Companies: {targetCompanies.join(", ") || "Choose target companies in your profile"}
        </p>
        <p className="text-xs text-slate-500">This is a roadmap, not your daily task queue.</p>
      </div>
    </section>
  );
}
