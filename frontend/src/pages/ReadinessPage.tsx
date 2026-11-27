import { useQuery } from "@tanstack/react-query";
import { useAuthStore } from "../store/authStore";
import { useNavigate, Link } from "react-router-dom";
import api from "../services/api";
import {
  Target, ShieldCheck, Flame, Clock, Play, Brain, AlertCircle, ArrowRight,
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
      <div className="min-h-screen bg-canvas flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary mx-auto mb-3" />
          <p className="text-sm text-text-muted">Loading readiness report…</p>
        </div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="min-h-screen bg-canvas flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <AlertCircle className="mx-auto text-subject-boss mb-3" size={32} />
          <h2 className="text-lg font-bold text-text">Could not load readiness</h2>
          <p className="text-sm text-text-muted">
            Please try again or contact support if the issue persists.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="mt-4 inline-flex items-center gap-2 rounded-xl bg-surface px-4 py-2 text-sm font-semibold text-text-primary border border-border hover:bg-surfaceHover transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  const streakStatus = readinessData?.streak_status ?? { current_streak: 0 };
  const skills = readinessData?.skills ?? readinessData?.category_scores ?? {};

  return (
    <div className="min-h-screen bg-canvas text-text">
      <div className="mx-auto max-w-5xl px-4 py-6 sm:py-10">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.16em] text-primary flex items-center gap-2">
              <Target size={14} /> Readiness report
            </p>
            <h1 className="mt-1 text-2xl font-black text-text">Readiness for {target_company}</h1>
            <p className="mt-1 text-sm text-text-secondary">
              Evidence-based readiness — not just lesson completion.
            </p>
          </div>
          <Card pad="md" className="relative overflow-hidden">
            <div className="absolute inset-0 bg-primary/5 pointer-events-none" />
            <div className="relative z-10 flex items-center gap-4">
              <div className="w-24 h-24 rounded-full border border-border flex items-center justify-center shadow-card">
                <ReadinessRing value={Number(readiness)} size={60} strokeWidth={6} />
              </div>
              <div className="flex-1">
                <h3 className="text-3xl font-black text-text">
                  {Math.round(Number(readiness))}%
                </h3>
                <p className="mt-1 text-sm text-text-secondary">
                  {Math.round(Number(readiness)) >= 75
                    ? "Strong readiness — you're on track"
                    : readiness >= 50
                    ? "Building momentum — keep going"
                    : "Building foundation — focus on weak skills"}
                </p>
                <div className="mt-3 flex items-center gap-2">
                  <span className={`rounded-full px-2.5 py-0.5 text-[10px] font-bold ${
                    readiness >= 75 ? "bg-subject-verbal/10 text-subject-verbal" :
                    readiness >= 50 ? "bg-subject-aptitude/10 text-subject-aptitude" :
                    "bg-subject-boss/10 text-subject-boss"
                  }`}>
                    {readiness >= 75 ? "Ready" : readiness >= 50 ? "Developing" : "Foundational"}
                  </span>
                  {target_company && (
                    <span className="ml-2 rounded-full border border-border/50 bg-surfaceHover px-2 py-1 text-[10px] font-semibold text-text-secondary">
                      {target_company}
                    </span>
                  )}
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Today's mission */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-8">
          <Card tone="coding">
            <div className="flex flex-col sm:flex-row sm:items-center gap-4 mb-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-subject-coding flex items-center gap-2">
                  <Clock size={14} /> Today's mission
                </p>
                <h2 className="mt-1 text-lg font-black text-text">Continue today's mission</h2>
              </div>
              <Button
                variant="primary"
                asChild
                className="px-4 py-2 text-sm shadow-primary"
              >
                <Link to="/dashboard">
                  Continue today's mission <ArrowRight size={14} />
                </Link>
              </Button>
            </div>
            <div className="mt-4 flex items-center justify-between">
              <span className="text-[10px] font-bold text-text-muted">Focus on weak skills first</span>
              <span className="text-[10px] text-text-muted">{streakStatus.current_streak ?? 0}-day streak</span>
            </div>
          </Card>

          <Card tone="verbal">
            <div className="flex flex-col sm:flex-row sm:items-center gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-subject-verbal flex items-center gap-2">
                  <Brain size={14} /> Skill evidence
                </p>
                <h2 className="mt-1 text-lg font-black text-text">Weak areas</h2>
              </div>
              <Link to="/skills" className="ml-2 text-xs font-bold text-primary hover:text-primary-dark underline-offset-4">
                View full skill map <ArrowRight size={14} />
              </Link>
            </div>
            <div className="mt-4 grid grid-cols-2 gap-3">
              {Object.entries(skills).slice(0, 4).map(([skillId, skill]: [string, any]) => (
                <div key={skillId} className="p-3 rounded-xl border border-border/50 bg-surfaceHover">
                  <h4 className="text-xs font-bold text-text capitalize">{skillId.replace(/_/g, " ")}</h4>
                  <p className="text-[10px] text-text-muted">Accuracy: {skill.score ?? 0}%</p>
                  <div className="mt-2 h-1 w-full bg-border/30 rounded-full overflow-hidden">
                    <div className="h-full bg-primary" style={{ width: `${Math.min((skill.score ?? 0), 100)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Blockers */}
        {(blockers.length > 0 || gaps.length > 0) && (
          <Card tone="boss">
            <div className="flex items-start gap-3 mb-4">
              <AlertCircle className="w-5 h-5 text-subject-boss" />
              <h3 className="text-sm font-bold text-text">Blockers & gaps</h3>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {([...blockers, ...gaps]).map((item: string, i: number) => (
                <div key={i} className="flex items-start gap-2 rounded-xl border border-subject-boss/20 bg-subject-boss/5 p-3">
                  <AlertCircle className="w-4 h-4 text-subject-boss mt-0.5 shrink-0" />
                  <p className="text-sm text-text-secondary">{item}</p>
                </div>
              ))}
            </div>
          </Card>
        )}

        {/* Strengths */}
        {(strengths.length > 0) && (
          <Card tone="verbal">
            <div className="flex items-start gap-3 mb-4">
              <ShieldCheck className="w-5 h-5 text-subject-verbal" />
              <h3 className="text-sm font-bold text-text">Strong areas</h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {strengths.slice(0, 6).map((skill: string, i: number) => (
                <span key={i} className="rounded-xl border border-subject-verbal/20 bg-subject-verbal/5 px-3 py-1.5 text-[10px] font-bold text-subject-verbal">
                  {skill}
                </span>
              ))}
            </div>
          </Card>
        )}

        {/* Next action */}
        {next_action && (
          <Card tone="interview">
            <div className="flex items-start gap-3 mb-4">
              <Play className="w-5 h-5 text-primary" />
              <h3 className="text-sm font-bold text-text">Next action</h3>
            </div>
            <p className="text-sm text-text-secondary mb-4">{next_action}</p>
            <Button variant="primary" onClick={() => navigate("/dashboard")} className="w-full sm:w-auto shadow-primary">
              Start today's mission <ArrowRight size={14} />
            </Button>
          </Card>
        )}
      </div>
    </div>
  );
}
