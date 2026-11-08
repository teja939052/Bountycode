import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowRight,
  BookOpen,
  Brain,
  Building2,
  CheckCircle2,
  Clock,
  Compass,
  GraduationCap,
  Search,
  ShieldCheck,
  Target,
  TrendingUp,
  Zap,
} from "lucide-react";
import api from "../services/api";
import Spinner from "../components/ui/Spinner";
import { useJourneyState } from "../hooks/useJourneyState";
import AcademyProfileSetup from "../components/academy/AcademyProfileSetup";
import AcademyDiagnostic from "../components/academy/AcademyDiagnostic";
import AcademyPersonalPlan from "../components/academy/AcademyPersonalPlan";
import ScrimPath from "../components/academy/ScrimPath";

/** Minimal resilient Academy view while full catalog hydrates. */
export function PlacementAcademyView() {
  const { data: journey, isLoading } = useJourneyState();
  const { data: lessonResult, isLoading: lessonsLoading } = useQuery({
    queryKey: ["company-lessons", "catalog"],
    queryFn: () => api.companyLessons.listLessons(),
    staleTime: 300_000,
  });
  const lessons = ((lessonResult as any)?.data ?? []) as Array<{ slug: string; title: string; domain?: string }>;

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
          Coddy-style scrims, diagnostic, and evidence-based practice for service-company placement.
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
      </header>

      <div id="academy-profile">
        <AcademyProfileSetup />
      </div>
      <AcademyDiagnostic />
      <AcademyPersonalPlan />
      <ScrimPath />

      <section className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
        <h2 className="text-lg font-black text-slate-900">Lesson catalog</h2>
        <p className="mt-1 text-sm text-slate-600">
          {lessonsLoading ? "Loading lessons…" : `${lessons.length} lessons available`}
        </p>
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          {lessons.slice(0, 24).map((lesson) => (
            <Link
              key={lesson.slug}
              to={`/learn/lesson/${lesson.slug}`}
              className="rounded-xl border border-slate-200 px-3 py-2.5 text-sm font-semibold text-slate-800 hover:border-emerald-300 hover:bg-emerald-50/40"
            >
              <span className="block truncate">{lesson.title}</span>
              <span className="text-[11px] font-medium text-slate-500">{lesson.domain || lesson.slug}</span>
            </Link>
          ))}
        </div>
        {lessons.length > 24 && (
          <p className="mt-3 text-xs text-slate-500">Showing first 24 — open a scrim track above for ordered paths.</p>
        )}
      </section>
    </div>
  );
}
