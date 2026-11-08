import { useMemo } from "react";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";
import {
  Network, ArrowRight, Target, AlertTriangle, CheckCircle2,
  BookOpen, BarChart3, GraduationCap,
} from "lucide-react";
import api from "../services/api";

/** Canonical service-company skill map (mirrors backend skill_graph.json). */
const DOMAINS = [
  {
    id: "programming_fundamentals",
    name: "Programming foundations",
    color: "#22c55e",
    lessons: ["variables_basics", "conditions_basics", "loops_basics", "functions_basics", "arrays_basics", "strings_basics"],
    weightNote: "InfyTQ / NQT coding foundation",
  },
  {
    id: "quantitative_aptitude",
    name: "Quantitative aptitude",
    color: "#3b82f6",
    lessons: ["number_systems", "percentages", "profit_loss", "ratio_proportion", "averages", "time_work", "time_distance"],
    weightNote: "Highest weight in TCS NQT aptitude",
  },
  {
    id: "logical_reasoning",
    name: "Logical reasoning",
    color: "#a855f7",
    lessons: ["number_series", "coding_decoding", "blood_relations", "direction_sense", "syllogisms", "seating_arrangement"],
    weightNote: "Series, puzzles, relations",
  },
  {
    id: "verbal_ability",
    name: "Verbal ability",
    color: "#f59e0b",
    lessons: ["reading_comprehension", "error_spotting", "vocabulary_cloze", "grammar_transformations"],
    weightNote: "RC + grammar for service papers",
  },
  {
    id: "arrays_hashing",
    name: "DSA for service OA",
    color: "#ef4444",
    lessons: ["data_structures_intro", "hashing_basics", "algorithms_basics", "sorting_basics", "recursion_basics"],
    weightNote: "Pattern problems under time",
  },
] as const;

function scoreTone(score: number | null) {
  if (score == null) return { bar: "#64748b", text: "text-slate-400", label: "Not assessed" };
  if (score >= 80) return { bar: "#22c55e", text: "text-emerald-400", label: "Strong" };
  if (score >= 60) return { bar: "#3b82f6", text: "text-blue-400", label: "Developing" };
  if (score >= 35) return { bar: "#f59e0b", text: "text-amber-400", label: "Needs work" };
  return { bar: "#ef4444", text: "text-rose-400", label: "Foundation" };
}

function lessonHref(slug: string) {
  return `/learn/lesson/${slug}`;
}

export default function SkillGraph() {
  const { data: skillsRaw, isLoading: sLoad } = useQuery({
    queryKey: ["adaptive", "skills"],
    queryFn: () => api.adaptive.getSkillAssessment(),
    staleTime: 60_000,
    retry: 1,
  });
  const { data: readinessRaw } = useQuery({
    queryKey: ["readiness"],
    queryFn: () => api.readiness?.getScore?.() ?? api.gamification.getReadinessScore(),
    staleTime: 60_000,
    retry: 1,
  });
  const { data: sprintRaw } = useQuery({
    queryKey: ["sprint", "today"],
    queryFn: () => api.sprint?.getToday?.() ?? api.journey.getToday(),
    staleTime: 30_000,
    retry: 1,
  });

  const payload = (skillsRaw as any)?.data ?? skillsRaw ?? {};
  const skills = (payload.skills ?? payload.assessment?.skills ?? {}) as Record<
    string,
    { score?: number; mastery_label?: string; total_attempts?: number }
  >;

  const readiness = (readinessRaw as any)?.data ?? readinessRaw ?? {};
  const overall =
    readiness.overall_readiness ??
    readiness.score ??
    payload.overall_accuracy ??
    payload.overall_score ??
    null;

  const sprintTasks = ((sprintRaw as any)?.data?.tasks ?? (sprintRaw as any)?.tasks ?? []) as Array<{
    title?: string;
    to?: string;
    reason?: string;
  }>;

  const domainRows = useMemo(() => {
    return DOMAINS.map((d) => {
      const evidence = skills[d.id];
      const attempts = Number(evidence?.total_attempts ?? 0);
      const score = attempts > 0 ? Number(evidence?.score ?? 0) : null;
      return { ...d, score, attempts, tone: scoreTone(score) };
    }).sort((a, b) => (a.score ?? -1) - (b.score ?? -1));
  }, [skills]);

  const weak = domainRows.filter((d) => d.score != null && d.score < 70);
  const strong = domainRows.filter((d) => d.score != null && d.score >= 80);

  if (sLoad) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400">
        Building your skill map…
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-5xl px-4 py-8 space-y-6">
        <header className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div>
            <p className="text-[11px] font-bold uppercase tracking-[0.16em] text-indigo-400 flex items-center gap-2">
              <Network size={14} /> Service-company skill map
            </p>
            <h1 className="mt-1 text-2xl sm:text-3xl font-black tracking-tight">
              {overall == null
                ? "Map your placement skills"
                : `${Math.round(Number(overall))}% evidence-based readiness`}
            </h1>
            <p className="mt-1 text-sm text-slate-400 max-w-xl">
              Mastery comes from server-graded lessons and mocks — not time spent.
              Each domain links to the exact Academy lessons that build it.
            </p>
          </div>
          <div className="flex flex-wrap gap-2 shrink-0">
            <Link
              to="/academy"
              className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white"
            >
              <GraduationCap size={16} /> Open Academy
            </Link>
            <Link
              to="/quiz"
              className="inline-flex items-center gap-2 rounded-xl border border-slate-600 px-4 py-2.5 text-sm font-semibold"
            >
              Company mock
            </Link>
          </div>
        </header>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: "Domains", value: DOMAINS.length, icon: BarChart3 },
            { label: "Strong", value: strong.length, icon: CheckCircle2 },
            { label: "Need focus", value: weak.length, icon: AlertTriangle },
            { label: "Today's tasks", value: sprintTasks.length || "—", icon: Target },
          ].map((s) => (
            <div key={s.label} className="rounded-2xl border border-slate-800 bg-slate-900/80 p-4">
              <p className="text-[10px] uppercase tracking-wide text-slate-500 font-semibold flex items-center gap-1">
                <s.icon size={12} /> {s.label}
              </p>
              <p className="mt-1 text-2xl font-black">{s.value}</p>
            </div>
          ))}
        </div>

        {sprintTasks.length > 0 && (
          <section className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-5">
            <h2 className="text-sm font-bold text-emerald-300 flex items-center gap-2">
              <Target size={16} /> From today's sprint
            </h2>
            <ul className="mt-3 space-y-2">
              {sprintTasks.slice(0, 3).map((t, i) => (
                <li key={i}>
                  <Link
                    to={t.to || "/academy"}
                    className="flex items-center justify-between gap-3 rounded-xl border border-slate-700/80 bg-slate-900/60 px-3 py-2.5 hover:border-emerald-500/40 transition"
                  >
                    <span className="text-sm font-medium">{t.title || "Continue learning"}</span>
                    <ArrowRight size={14} className="text-slate-500 shrink-0" />
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        )}

        <section className="space-y-3">
          <h2 className="text-sm font-bold uppercase tracking-wide text-slate-400">Domains</h2>
          {domainRows.map((d, idx) => (
            <motion.article
              key={d.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.04 }}
              className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 sm:p-5"
            >
              <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-6">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="h-2.5 w-2.5 rounded-full shrink-0" style={{ background: d.color }} />
                    <h3 className="font-bold text-white">{d.name}</h3>
                    <span className={`text-[11px] font-semibold ${d.tone.text}`}>{d.tone.label}</span>
                  </div>
                  <p className="mt-1 text-xs text-slate-500">{d.weightNote}</p>
                  <div className="mt-3 h-2 rounded-full bg-slate-800 overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{
                        width: `${d.score == null ? 4 : Math.max(4, Math.min(100, d.score))}%`,
                        background: d.tone.bar,
                      }}
                    />
                  </div>
                  <p className="mt-1 text-[11px] text-slate-500">
                    {d.score == null
                      ? "No assessment evidence yet"
                      : `${Math.round(d.score)}% · ${d.attempts} graded attempt${d.attempts === 1 ? "" : "s"}`}
                  </p>
                </div>
                <Link
                  to={`/academy?focus=${encodeURIComponent(d.id)}`}
                  className="shrink-0 inline-flex items-center justify-center gap-2 rounded-xl bg-slate-100 px-4 py-2.5 text-sm font-semibold text-slate-900 hover:bg-white"
                >
                  Practise domain <ArrowRight size={14} />
                </Link>
              </div>

              <div className="mt-4 flex flex-wrap gap-2">
                {d.lessons.map((slug) => (
                  <Link
                    key={slug}
                    to={lessonHref(slug)}
                    className="inline-flex items-center gap-1.5 rounded-lg border border-slate-700 bg-slate-950/50 px-2.5 py-1.5 text-[11px] font-medium text-slate-300 hover:border-slate-500 hover:text-white"
                  >
                    <BookOpen size={12} className="opacity-60" />
                    {slug.replace(/_/g, " ")}
                  </Link>
                ))}
              </div>
            </motion.article>
          ))}
        </section>

        <footer className="rounded-2xl border border-slate-800 bg-slate-900/50 p-4 text-center text-sm text-slate-400">
          Weak domains rise to the top of today's sprint automatically.{" "}
          <Link to="/dashboard" className="font-semibold text-emerald-400 hover:underline">
            Open daily plan
          </Link>
        </footer>
      </div>
    </div>
  );
}
