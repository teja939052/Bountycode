import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  Compass,
  GraduationCap,
  Search,
  Target,
  Zap,
  AlertTriangle,
  ArrowRight,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import { useJourneyState } from "../hooks/useJourneyState";
import AcademyProfileSetup from "../components/academy/AcademyProfileSetup";
import AcademyDiagnostic from "../components/academy/AcademyDiagnostic";
import AcademyPersonalPlan from "../components/academy/AcademyPersonalPlan";
import ScrimPath from "../components/academy/ScrimPath";

type CatalogLesson = {
  slug: string;
  title: string;
  domain?: string;
  difficulty?: string;
  duration_min?: number;
};

/** Full Placement Academy home: plan, scrims, weak skills, searchable catalog. */
export function PlacementAcademyView() {
  const { data: journey, isLoading } = useJourneyState();
  const [query, setQuery] = useState("");

  const { data: lessonResult, isLoading: lessonsLoading } = useQuery({
    queryKey: ["company-lessons", "catalog"],
    queryFn: () => api.companyLessons.listLessons(),
    staleTime: 300_000,
  });

  const { data: dailyResult } = useQuery({
    queryKey: ["study", "today"],
    queryFn: () => api.journey.getToday(),
    staleTime: 30_000,
    retry: 1,
  });

  const { data: skillResult } = useQuery({
    queryKey: ["adaptive", "skills"],
    queryFn: () => api.adaptive.getSkillAssessment(),
    staleTime: 60_000,
    retry: 1,
  });

  const lessons = ((lessonResult as any)?.data ?? []) as CatalogLesson[];
  const daily = (dailyResult as any)?.data ?? dailyResult ?? {};
  const tasks = (daily?.tasks ?? daily?.plan ?? []) as Array<{ title?: string; to?: string; reason?: string }>;
  const skillPayload = (skillResult as any)?.data ?? skillResult ?? {};
  const skills = (skillPayload.skills ?? skillPayload.assessment?.skills ?? {}) as Record<
    string,
    { score?: number; total_attempts?: number }
  >;

  const weakSkills = useMemo(() => {
    return Object.entries(skills)
      .map(([id, v]) => ({ id, score: Number(v.score ?? 0), attempts: Number(v.total_attempts ?? 0) }))
      .filter((s) => s.attempts > 0 && s.score < 70)
      .sort((a, b) => a.score - b.score)
      .slice(0, 5);
  }, [skills]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return lessons;
    return lessons.filter(
      (l) =>
        l.title.toLowerCase().includes(q) ||
        l.slug.toLowerCase().includes(q) ||
        (l.domain || "").toLowerCase().includes(q),
    );
  }, [lessons, query]);

  if (isLoading) {
    return (
      <div className="flex min-h-[50vh] items-center justify-center">
        <Spinner />
      </div>
    );
  }

  return (
    <div className="space-y-6 pb-12">
      <header className="rounded-3xl border border-[#e7e2d8] bg-gradient-to-br from-white via-[#fbfaf6] to-[#f0f5ed] p-5 shadow-sm sm:p-7">
        <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.18em] text-emerald-700">
          <GraduationCap size={15} /> Bountycode Placement Academy
        </p>
        <h1 className="mt-3 text-3xl font-black tracking-tight text-slate-900 sm:text-4xl">
          Learn it. Practise it. Prove you know it.
        </h1>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">
          Coddy-style scrims for service companies. Your path follows diagnostic evidence — not a random checklist.
        </p>
        <div className="mt-4 flex flex-wrap gap-2">
          <Link to="/journey" className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-700">
            <Compass size={15} /> Journey
          </Link>
          <Link to="/skill-graph" className="inline-flex min-h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 text-sm font-semibold text-slate-700">
            <Target size={15} /> Skill map
          </Link>
          <Link to="/quiz" className="inline-flex min-h-10 items-center gap-2 rounded-xl bg-emerald-600 px-4 text-sm font-semibold text-white">
            <Zap size={15} /> Practice / mock
          </Link>
        </div>
        {journey?.company?.company_track && (
          <p className="mt-3 text-xs font-medium text-slate-500">
            Target track: <span className="text-slate-800">{String(journey.company.company_track)}</span>
          </p>
        )}
      </header>

      {tasks.length > 0 && (
        <section className="rounded-3xl border border-emerald-200 bg-emerald-50/50 p-5">
          <h2 className="text-sm font-black uppercase tracking-wide text-emerald-800">Today&apos;s missions</h2>
          <ul className="mt-3 space-y-2">
            {tasks.slice(0, 3).map((t, i) => (
              <li key={i}>
                <Link
                  to={t.to || "/academy"}
                  className="flex items-center justify-between gap-3 rounded-xl border border-emerald-100 bg-white px-3 py-2.5 text-sm font-semibold text-slate-800 hover:border-emerald-300"
                >
                  <span className="truncate">{t.title || "Continue learning"}</span>
                  <ArrowRight size={14} className="shrink-0 text-slate-400" />
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      {weakSkills.length > 0 && (
        <section className="rounded-3xl border border-amber-200 bg-amber-50/40 p-5">
          <h2 className="flex items-center gap-2 text-sm font-black uppercase tracking-wide text-amber-900">
            <AlertTriangle size={14} /> Weak skills (evidence)
          </h2>
          <div className="mt-3 flex flex-wrap gap-2">
            {weakSkills.map((s) => (
              <Link
                key={s.id}
                to={`/academy?focus=${encodeURIComponent(s.id)}`}
                className="rounded-full border border-amber-200 bg-white px-3 py-1 text-xs font-semibold text-amber-900"
              >
                {s.id.replace(/_/g, " ")} · {Math.round(s.score)}%
              </Link>
            ))}
          </div>
        </section>
      )}

      <div id="academy-profile">
        <AcademyProfileSetup />
      </div>
      <AcademyDiagnostic />
      <AcademyPersonalPlan />
      <ScrimPath />

      <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-black text-slate-900">Lesson catalog</h2>
            <p className="mt-1 text-sm text-slate-600">
              {lessonsLoading ? "Loading lessons…" : `${filtered.length} of ${lessons.length} lessons`}
            </p>
          </div>
          <label className="relative block w-full sm:w-72">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search title, domain, slug…"
              className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2 pl-9 pr-3 text-sm outline-none focus:border-emerald-400"
            />
          </label>
        </div>
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {filtered.slice(0, 40).map((lesson) => (
            <Link
              key={lesson.slug}
              to={`/learn/lesson/${lesson.slug}`}
              className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm font-semibold text-slate-800 hover:border-emerald-300 hover:bg-emerald-50/40"
            >
              <span className="block truncate">{lesson.title}</span>
              <span className="text-[11px] font-medium text-slate-500">
                {lesson.domain || lesson.slug}
                {lesson.duration_min ? ` · ${lesson.duration_min}m` : ""}
              </span>
            </Link>
          ))}
        </div>
        {filtered.length > 40 && (
          <p className="mt-3 text-xs text-slate-500">Showing first 40 matches — refine search for more.</p>
        )}
      </section>
    </div>
  );
}
