import { useMemo, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { Link } from "react-router-dom";
import { useAuthStore } from "../store/authStore";
import api from "../services/api";
import {
  Flame, ArrowRight, Clock, Briefcase, BarChart3,
  GraduationCap, RefreshCw, AlertCircle, Play, CheckCircle2,
  Rocket, Brain, ShieldCheck, Target, Calendar, BookOpen,
} from "lucide-react";
import { Button } from "../design-system/Button";
import { Card, SectionHeader } from "../design-system/Card";
import { ReadinessRing } from "../design-system/Progress";
import { placementRank } from "../lib/placementRank";
import { journeyApi } from "../services/api/journey";
import { missionApi } from "../services/api/missions";

type PlanTask = {
  type?: string; kind?: string; title?: string; description?: string;
  reason?: string; estimated_minutes?: number; question_id?: string;
  to?: string; label?: string; minutes?: number;
  mission_id?: string;
};

function taskHref(t: PlanTask): string {
  if (t.to) return t.to;
  if (t.question_id) return `/question/${t.question_id}`;
  if (t.type === "practice" || t.kind === "question") return "/practice";
  if (t.type === "repair") return `/repair/${t.mission_id || ""}`;
  if (t.type === "retest") return `/retest/${t.mission_id || ""}`;
  if (t.type === "lesson" || t.type === "lesson_complete") return `/lessons/${t.question_id || ""}`;
  return "/academy";
}
function taskLabel(t: PlanTask, i: number) {
  return t.title || t.label || `Task ${i + 1}`;
}
function taskReason(t: PlanTask) {
  if (t.reason) return t.reason;
  if (t.description) return t.description;
  if (t.type === "practice") return "This skill needs more evidence.";
  if (t.type === "review") return "Due for spaced repetition.";
  if (t.type === "repair") return "Repair mission — fix the gap before retesting.";
  if (t.type === "retest") return "Retest to confirm mastery.";
  if (t.type === "company_mission" || t.type === "company_focus") return "Aligned to your target company.";
  return "Part of today's personalized plan.";
}
function taskMinutes(t: PlanTask) {
  return Number(t.estimated_minutes ?? t.minutes ?? 12) || 12;
}

export default function Dashboard() {
  const storeUser = useAuthStore((s) => s.user);
  const { gamification, readinessScore, streakStatus, isLoading: dLoad } = useDashboard();
  const { data: todayPlanRaw, isLoading: pLoad, isError: pErr, refetch: refetchPlan } = useQuery({
    queryKey: ["study", "today"],
    queryFn: () => journeyApi.getToday(),
    staleTime: 30_000,
    retry: 1,
  });
  const { data: skillsRaw, isLoading: sLoad } = useQuery({
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
    const out: PlanTask[] = [];
    const cm = plan.company_mission || plan.company_focus;
    if (cm) out.push({ ...cm, type: cm.type || "company_mission", title: cm.title || cm.label || "Company preparation" });
    const next = plan.next || plan.next_mission;
    if (next) {
      out.push({
        ...next,
        type: next.type || "next_mission",
        title: next.title || next.level?.title || next.label || "Continue learning",
        estimated_minutes: next.estimated_minutes ?? next.minutes ?? 15,
      });
    }
    for (const t of Array.isArray(plan.tasks) ? plan.tasks : []) if (t) out.push(t);
    for (const t of Array.isArray(plan.practice) ? plan.practice : []) if (t) out.push({ ...t, type: t.type || "practice" });
    for (const t of (Array.isArray(plan.reviews) ? plan.reviews : []).slice(0, 3)) {
      if (t) out.push({ ...t, type: "review", title: t.title || t.question || "Review", estimated_minutes: t.estimated_minutes ?? 5 });
    }
    const seen = new Set<string>();
    return out
      .filter((t) => {
        const k = `${t.type}:${t.title || t.label || t.question_id}`;
        if (seen.has(k)) return false;
        seen.add(k);
        return true;
      })
      .slice(0, 8);
  }, [plan]);

  const totalMinutes = useMemo(() => tasks.reduce((s, t) => s + (Number(t.estimated_minutes ?? t.minutes ?? 12) || 12), 0), [tasks]);
  const weakSkills = useMemo(
    () =>
      Object.entries(skills)
        .map(([id, s]) => ({ id, ...s }))
        .filter((s) => (s.total_attempts || 0) > 0 && (s.score ?? 0) < 70)
        .sort((a, b) => (a.score ?? 0) - (b.score ?? 0))
        .slice(0, 5),
    [skills],
  );

  const readiness = readinessScore?.score ?? plan.overall_score ?? skillsPayload.overall_score ?? null;
  const streak = streakStatus?.current_streak ?? gamification?.streak ?? plan.streak ?? storeUser?.streak ?? 0;
  const level = gamification?.level ?? plan.level ?? storeUser?.level ?? 1;
  const rank = placementRank(Number(level));

  // Sort tasks: repair first, then lesson, then review, then practice
  const sortedTasks = useMemo(() => {
    const priority: Record<string, number> = { repair: 0, lesson: 1, retest: 1, practice: 2, mock: 3, review: 3 };
    return [...tasks].sort((a, b) => (priority[a.type ?? "practice"] ?? 5) - (priority[b.type ?? "practice"] ?? 5));
  }, [tasks]);

  const loading = dLoad || pLoad || sLoad;
  const primaryTask = sortedTasks[0];

  if (loading) {
    return (
      <div className="min-h-screen bg-canvas flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary mx-auto mb-3" />
          <p className="text-sm text-text-muted">Building your plan for today…</p>
        </div>
      </div>
    );
  }

  if (pErr) {
    return (
      <div className="min-h-screen bg-canvas flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <AlertCircle className="mx-auto text-subject-boss mb-3" size={32} />
          <h2 className="text-lg font-bold text-text">Could not load your dashboard</h2>
          <button
            onClick={() => { void refetchPlan(); }}
            className="mt-4 inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-surface text-primary text-sm font-semibold border border-border"
          >
            <RefreshCw size={16} /> Retry
          </button>
        </div>
      </div>
    );
  }

  const firstName = (storeUser?.name || "there").split(" ")[0];
  const greeting = (() => {
    const h = new Date().getHours();
    return h < 12 ? "Good morning" : h < 18 ? "Good afternoon" : "Good evening";
  })();

  return (
    <div className="min-h-screen bg-canvas text-text">
      <div className="mx-auto max-w-5xl px-4 py-6 sm:py-10">
        {/* ===== GREETING + READINESS ===== */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <p className="text-sm text-text-muted">
              {greeting}, {firstName}
            </p>
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight mt-1">
              Today's mission
            </h1>
            <p className="mt-1 text-sm text-text-secondary">
              Build one skill at a time. Every action is evidence toward readiness.
            </p>
          </div>
          <div className="flex items-center gap-3 shrink-0">
            <Card tone="default" pad="sm" className="w-24 h-24 flex items-center justify-center shrink-0">
              <ReadinessRing value={Number(readiness ?? 0)} size={48} strokeWidth={6} />
            </Card>
            <div className="flex flex-col gap-1 text-right text-xs">
              <span className="inline-flex items-center justify-end gap-1 font-semibold text-subject-coding">
                <Flame size={14} /> {streak} day streak
              </span>
              <span className="font-semibold text-text-primary">{rank.title}</span>
            </div>
          </div>
        </div>

        {/* ===== TODAY'S MISSION - ONE PRIMARY ACTION ===== */}
        <Card tone="default" interactive className="mb-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-[0.16em] text-primary mb-1">
                <Rocket size={14} /> Today's mission
              </div>
              <h2 className="text-xl font-black text-text">
                {sortedTasks.length > 0
                  ? sortedTasks[0].title || sortedTasks[0].label || "Continue learning"
                  : "All caught up — take a break or explore"}
              </h2>
              <p className="mt-1 text-sm text-text-secondary">
                {sortedTasks[0]?.reason || sortedTasks[0]?.description || "You're all caught up for today."}
                <span className="ml-2 text-xs text-primary font-semibold">
                  {totalMinutes > 0 ? `~${totalMinutes} min` : ""}
                </span>
              </p>
            </div>
            <div className="flex gap-2 sm:flex-col w-full sm:w-auto">
              {sortedTasks.length > 0 ? (
                <Button
                  variant="primary"
                  onClick={() => {
                    const t = sortedTasks[0];
                    if (t.to) window.location.href = t.to;
                    else if (t.question_id) window.location.href = `/question/${t.question_id}`;
                    else if (t.type === "practice" || t.kind === "question") window.location.href = "/practice";
                    else if (t.type === "repair") window.location.href = `/repair/${t.mission_id || ""}`;
                    else if (t.type === "retest") window.location.href = `/retest/${t.mission_id || ""}`;
                    else if (t.type === "lesson" || t.type === "lesson_complete") window.location.href = `/lessons/${t.question_id || ""}`;
                    else window.location.href = "/academy";
                  }}
                  className="w-full sm:w-auto min-h-11 px-6 py-3 text-lg font-bold"
                >
                  {sortedTasks[0].type === "repair" ? "Start repair mission" : sortedTasks[0].type === "retest" ? "Start retest" : "Continue today's mission"}
                  <ArrowRight size={16} className="ml-2" />
                </Button>
              ) : (
                <Button variant="outline" asChild className="w-full sm:w-auto min-h-11 px-6 py-3 text-lg font-semibold">
                  <Link to="/academy" className="flex items-center gap-2">
                    Explore academy <ArrowRight size={16} />
                  </Link>
                </Button>
              )}
            </div>
          </div>
          {sortedTasks.length > 0 && (
            <div className="mt-4 flex flex-col sm:flex-row gap-3 sm:items-end">
              {sortedTasks.slice(1, 4).map((t, i) => (
                <Link
                  key={t.question_id || t.title || i}
                  to={taskHref(t)}
                  className="flex items-center gap-2 px-3 py-2 rounded-xl border border-border bg-surface-hover text-sm font-medium text-text-secondary hover:bg-surface-hover hover:border-primary/30 transition-all"
                >
                  <ArrowRight size={14} className="text-text-muted" />
                  <span>{t.title || t.label}</span>
                  <span className="ml-auto text-[10px] text-text-muted">{taskMinutes(t)} min</span>
                </Link>
              ))}
              {sortedTasks.length > 4 && (
                <div className="px-3 py-2 flex items-center text-[10px] font-bold text-text-muted uppercase tracking-wider">
                  +{sortedTasks.length - 4} more
                </div>
              )}
            </div>
          )}
        </Card>

        {/* ===== QUICK ACTIONS ===== */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {/* Weak skills quick repair */}
          {weakSkills.length > 0 && (
            <Card tone="aptitude" interactive className="group">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div>
                  <p className="text-xs font-bold uppercase tracking-[0.16em] text-subject-aptitude flex items-center gap-2">
                    <AlertCircle size={14} /> Repair weak skills
                  </p>
                  <h3 className="mt-1 text-sm font-semibold text-text">
                    Focus on {weakSkills[0].id.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())}
                  </h3>
                  <p className="mt-0.5 text-xs text-subject-aptitude">
                    Accuracy: {(weakSkills[0].score ?? 0)}% — repair recommended
                  </p>
                </div>
                <Link
                  to="/practice"
                  className="inline-flex items-center gap-2 rounded-xl bg-subject-aptitude px-3 py-2 text-[11px] font-bold text-text-inverse hover:bg-amber-500 transition-all"
                >
                  Start practice <ArrowRight size={14} />
                </Link>
              </div>
            </Card>
          )}

          <Card tone="coding" interactive className="group">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-subject-coding flex items-center gap-2">
                  <Target size={14} /> Readiness checkpoint
                </p>
                <h3 className="mt-1 text-sm font-semibold text-text">
                  {Math.round(readiness ?? 0)}% readiness
                </h3>
                <p className="mt-0.5 text-xs text-subject-coding">
                  Evidence-based — not just lesson completion
                </p>
              </div>
              <Link
                to="/readiness"
                className="inline-flex items-center gap-2 rounded-xl bg-subject-coding px-3 py-2 text-[11px] font-bold text-text-inverse hover:bg-cyan-500 transition-all"
              >
                View report <ArrowRight size={14} />
              </Link>
            </div>
          </Card>

          <Card tone="interview" interactive className="group">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.16em] text-subject-interview flex items-center gap-2">
                  <BookOpen size={14} /> Next lesson
                </p>
                <h3 className="mt-1 text-sm font-semibold text-text">
                  Continue curriculum
                </h3>
                <p className="mt-0.5 text-xs text-subject-interview">
                  Mastery through practice, not just watching
                </p>
              </div>
              <Link
                to="/academy"
                className="inline-flex items-center gap-2 rounded-xl bg-subject-interview px-3 py-2 text-[11px] font-bold text-text-inverse hover:bg-violet-600 transition-all"
              >
                Browse lessons <ArrowRight size={14} />
              </Link>
            </div>
          </Card>
        </div>

        {/* ===== SKILL HEATMAP (small) ===== */}
        <div className="mt-8">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-bold text-text">Skill evidence</h3>
            <Link to="/skills" className="text-xs font-bold text-primary hover:text-primary-dark underline-offset-4">
              View full skill graph <ArrowRight size={14} />
            </Link>
          </div>
          <div className="grid grid-cols-5 gap-2">
            {Object.entries(skills).slice(0, 5).map(([id, s]) => (
              <div key={id} className="flex flex-col items-center gap-2 p-3 rounded-xl bg-surface border border-border shadow-card">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center mb-1 text-xs font-bold"
                  style={{
                    backgroundColor: (s.score ?? 0) >= 70 ? "rgba(34, 197, 94, 0.15)" : (s.score ?? 0) >= 40 ? "rgba(245, 158, 11, 0.15)" : "rgba(239, 68, 68, 0.15)",
                    color: (s.score ?? 0) >= 70 ? "#22C55E" : (s.score ?? 0) >= 40 ? "#F59E0B" : "#EF4444",
                  }}
                >
                  {(s.score ?? 0) >= 70 ? "✓" : (s.score ?? 0) >= 40 ? "⚡" : "●"}
                </div>
                <span className="text-xs font-semibold text-text truncate" title={id}>{id.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase())}</span>
                <span className="text-[10px] text-text-muted">{s.score ?? 0}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
