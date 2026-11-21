import { useQuery } from "@tanstack/react-query";
import { useAuthStore } from "../store/authStore";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import {
  Target, ShieldCheck, Flame, Clock, Play,
} from "lucide-react";
import { Button } from "../design-system/Button";
import { Card } from "../design-system/Card";
import { ReadinessRing } from "../design-system/Progress";

export default function ReadinessPage() {
  const storeUser = useAuthStore((s) => s.user);
  const navigate = useNavigate();
  const { data: readinessData, isLoading, isError } = useQuery({
    queryKey: ["readiness"],
    queryFn: () =>
      api.gamification.getCompanyReadiness(),
    staleTime: 5 * 60 * 1000,
    retry: 1,
  });

  const readiness = readinessData?.readiness_score ?? readinessData?.score ?? readinessData?.overall_readiness ?? 0;
  const categories = readinessData?.category_scores ?? readinessData?.categories ?? {};
  const blockers = readinessData?.blockers ?? readinessData?.gaps ?? [];
  const strengths = readinessData?.strong_skills ?? readinessData?.strengths ?? [];
  const gaps = readinessData?.gaps ?? readinessData?.blockers ?? [];
  const next_action = readinessData?.next_action ?? readinessData?.next_action_skill ?? "";
  const target_company = readinessData?.target_company ?? storeUser?.target_company ?? "Not set";

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-brand-sky mx-auto mb-3" />
          <p className="text-sm text-slate-500">Loading readiness report…</p>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <AlertCircle className="mx-auto text-rose-500 mb-3" size={32} />
          <h2 className="text-lg font-bold text-slate-900">Could not load readiness</h2>
          <p className="text-sm text-slate-600">
            Please try again or contact support if the issue persists.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 inline-flex items-center gap-2 rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white"
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="mx-auto max-w-5xl px-4 py-6 sm:py-10">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-brand-sky flex items-center gap-2">
              <Target size={14} /> Readiness report
            </p>
            <h1 className="mt-1 text-2xl font-black text-slate-900">Readiness for {target_company}</h1>
            <p className="mt-1 text-sm text-slate-600">
              Evidence-based readiness — not just lesson completion.
            </p>
          </div>
          <div className="rounded-2xl border border-emerald-200 bg-white p-4 sm:p-5 shadow-sm">
            <div className="flex items-center gap-4">
              <div className="w-24 h-24 rounded-full border border-emerald-100 flex items-center justify-center shadow-sm">
                <ReadinessRing value={Number(readiness)} size={60} />
              </div>
              <div className="flex-1">
                <h3 className="text-3xl font-black text-slate-900">
                  {Math.round(Number(readiness))}%
                </h3>
                <p className="mt-1 text-sm text-slate-600">
                  {Math.round(Number(readiness)) >= 75
                    ? "Strong readiness — you're on track"
                    : readiness >= 50
                    ? "Building momentum — keep going"
                    : "Building foundation — focus on weak skills"}
                </p>
                <div className="mt-3 flex items-center gap-2">
                  <span className="rounded-full px-2.5 py-0.5 text-[10px] font-bold"
                    className={readiness >= 75 ? "bg-emerald-100 text-emerald-700" : readiness >= 50 ? "bg-amber-100 text-amber-700" : "bg-rose-100 text-rose-700"}>
                    {readiness >= 75 ? "Ready" : readiness >= 50 ? "Developing" : "Foundational"}
                  </span>
                  {target_company && (
                    <span className="ml-2 rounded-full border border-slate-200 bg-white px-2 py-1 text-[10px] font-semibold text-slate-700">
                      {target_company}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Today's mission */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <Card>
              <div className="flex flex-col sm:flex-row sm:items-center gap-4 mb-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.16em] text-brand-sky flex items-center gap-2">
                    <Clock size={14} /> Today's mission
                  </p>
                  <h2 className="mt-1 text-lg font-bold text-slate-900">Continue today's mission</h2>
                </div>
                <Button variant="primary" className="px-4 py-2 text-sm" asChild>
                  <Link to="/dashboard">
                    Continue today's mission <ArrowRight size={14} />
                  </Link>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between">
                <span className="text-xs font-bold text-slate-500">Focus on weak skills first</span>
                <span className="text-xs text-slate-400">{streakStatus?.current_streak ?? 0}-day habit</span>
              </div>
            </div>
          </Card>

          <Card>
            <div className="flex flex-col sm:flex-row sm:items-center gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-blue-700 flex items-center gap-2">
                  <Brain size={14} /> Skill evidence
                </p>
                <h2 className="mt-1 text-lg font-bold text-slate-900">Weak areas</h2>
              </div>
              <Link to="/skills" className="ml-2 text-sm text-brand-sky font-semibold hover:underline">
                View full skill map <ArrowRight size={14} />
              </div>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-3">
              {Object.entries(skills).slice(0, 4).map(([skillId, skill]) => (
                <div key={skillId} className="p-3 rounded-lg border border-white/50 bg-white/50">
                  <h4 className="text-xs font-bold text-slate-900 capitalize">{skillId.replace(/_/g, " ")}</h4>
                  <p className="text-[10px] text-slate-500">Accuracy: {skill.score ?? 0}%</p>
                  <div className="mt-2 h-1 w-full bg-slate-200 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500" style={{ width: `${Math.min((skill.score ?? 0), 100)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Blockers */}
        {(blockers.length > 0 || gaps.length > 0) && (
          <Card className="border border-rose-100 bg-rose-50 p-6 sm:p-8 shadow-sm">
            <div className="flex items-start gap-3 mb-4">
              <AlertCircle className="w-5 h-5 text-rose-600" />
              <h3 className="text-sm font-bold text-slate-900">Blockers & gaps</h3>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {([...blockers, ...gaps]).map((item: string, i: number) => (
                <div key={i} className="flex items-start gap-2 rounded-lg border border-rose-200 bg-rose-50 p-3">
                  <AlertCircle className="w-4 h-4 text-rose-500 mt-0.5 shrink-0" />
                  <p className="text-sm text-slate-800">{item}</p>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Strengths */}
        {(strengths.length > 0) && (
          <Card className="border border-emerald-100 bg-green-50 p-6 sm:p-8 shadow-sm">
            <div className="flex items-start gap-3 mb-4">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              <h3 className="text-sm font-bold text-slate-900">Strong areas</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {strengths.slice(0, 6).map((skill: string, i: number) => (
                <span key={i} className="rounded-lg border border-emerald-200 bg-white px-3 py-1.5 text-xs font-bold text-emerald-700">
                  {skill}
                </span>
              ))}
            </div>
          </Card>
        )}

        {/* Next action */}
        {next_action && (
          <Card className="border border-blue-100 bg-blue-50 p-6 sm:p-8 shadow-sm">
            <div className="flex items-start gap-3 mb-4">
              <Play className="w-5 h-5 text-blue-600" />
              <h3 className="text-sm font-bold text-slate-900">Next action</h3>
            </div>
            <p className="text-sm text-slate-800 mb-4">{next_action}</p>
            <Button variant="primary" onClick={() => navigate("/dashboard")} className="w-full sm:w-auto">
              Start today's mission <ArrowRight size={14} />
            </Button>
          </Card>
        )}
      </div>
    </div>
  );
}

import { useNavigate, Link, ArrowRight } from "react-router-dom";
import { AlertCircle } from "lucide-react";