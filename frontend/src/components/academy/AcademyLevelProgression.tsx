import {
  ArrowRight,
  Check,
  CheckCircle2,
  Clock3,
  Flag,
  Gauge,
  LockKeyhole,
  Play,
  ShieldCheck,
  Sparkles,
  Trophy,
} from "lucide-react";
import { Link } from "react-router-dom";

type Level = {
  id: number;
  title: string;
  focus: string;
  unlock?: string;
  status: "complete" | "current" | "locked" | string;
};

type Props = {
  plan: any;
  mockCompany: string;
};

const levelColors = [
  { tint: "from-slate-700 to-slate-900", soft: "bg-slate-50", border: "border-slate-200", text: "text-slate-800" },
  { tint: "from-emerald-600 to-teal-700", soft: "bg-emerald-50", border: "border-emerald-200", text: "text-emerald-800" },
  { tint: "from-sky-600 to-indigo-700", soft: "bg-sky-50", border: "border-sky-200", text: "text-sky-800" },
  { tint: "from-indigo-600 to-violet-700", soft: "bg-indigo-50", border: "border-indigo-200", text: "text-indigo-800" },
  { tint: "from-violet-600 to-fuchsia-700", soft: "bg-violet-50", border: "border-violet-200", text: "text-violet-800" },
  { tint: "from-amber-500 to-orange-600", soft: "bg-amber-50", border: "border-amber-200", text: "text-amber-800" },
];

const levelProof = [
  "Set your target and finish the diagnostic",
  "Reach reliable fundamentals across the core skill bank",
  "Solve varied DSA, SQL and debugging tasks",
  "Pass mixed transfer checks with fewer repeated errors",
  "Complete timed practice with stable speed and accuracy",
  "Explain projects and handle communication practice",
];

function ProgressRing({ value }: { value: number }) {
  const safe = Math.max(0, Math.min(100, value));
  return (
    <div className="relative h-14 w-14 shrink-0" aria-label={`${safe}% campaign progress`}>
      <svg viewBox="0 0 36 36" className="h-14 w-14 -rotate-90">
        <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#e2e8f0" strokeWidth="3" />
        <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#4f46e5" strokeWidth="3" strokeDasharray={`${safe}, 100`} strokeLinecap="round" />
      </svg>
      <span className="absolute inset-0 flex items-center justify-center text-[11px] font-black text-indigo-800">{safe}%</span>
    </div>
  );
}

export default function AcademyLevelProgression({ plan, mockCompany }: Props) {
  const levels: Level[] = Array.isArray(plan.level_path) ? plan.level_path : [];
  const currentIndex = Math.max(0, Math.min(levels.length - 1, Number(plan.current_level || 0)));
  const current = levels[currentIndex];
  const overall = typeof plan.overall_accuracy === "number" ? Math.round(plan.overall_accuracy) : typeof plan.overall_diagnostic_score === "number" ? Math.round(plan.overall_diagnostic_score) : null;
  const campaignProgress = levels.length ? Math.round(((currentIndex + (overall === null ? 0 : Math.min(overall, 100) / 100)) / levels.length) * 100) : 0;
  const nextTask = Array.isArray(plan.daily_tasks) ? plan.daily_tasks[0] : null;
  const nextHref = nextTask?.lesson_slug ? `/learn/lesson/${nextTask.lesson_slug}` : "/academy#academy-diagnostic";
  const continueHref = currentIndex >= 3 ? `/mock-oa?company=${encodeURIComponent(mockCompany)}` : nextHref;
  const readiness = plan.assessment_readiness?.stage || "diagnostic";

  if (!levels.length) return null;

  return (
    <div className="mt-5 overflow-hidden rounded-[1.75rem] border border-indigo-200 bg-gradient-to-br from-indigo-50 via-white to-slate-50 shadow-sm">
      <div className="border-b border-indigo-100 px-4 py-5 sm:px-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="rounded-2xl bg-indigo-700 p-3 text-white shadow-lg shadow-indigo-200"><Trophy size={20} /></div>
            <div>
              <p className="flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.18em] text-indigo-700"><Sparkles size={13} /> Service-company campaign</p>
              <h3 className="mt-1 text-lg font-black text-slate-950">Your path to assessment-ready</h3>
              <p className="mt-1 max-w-xl text-xs leading-5 text-slate-600">Levels reward demonstrated skill, not time spent. XP and streaks can make practice fun, but mastery evidence unlocks the next stage.</p>
            </div>
          </div>
          <ProgressRing value={campaignProgress} />
        </div>

        <div className="mt-5 grid gap-2 sm:grid-cols-3">
          <div className="rounded-2xl border border-white/80 bg-white/80 p-3"><p className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wide text-slate-500"><Flag size={12} /> Current mission</p><p className="mt-1 text-sm font-black capitalize text-slate-900">{current?.title || "Orientation"}</p></div>
          <div className="rounded-2xl border border-white/80 bg-white/80 p-3"><p className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wide text-slate-500"><Gauge size={12} /> Evidence</p><p className="mt-1 text-sm font-black capitalize text-slate-900">{overall === null ? "Diagnostic pending" : `${overall}% overall accuracy`}</p></div>
          <div className="rounded-2xl border border-white/80 bg-white/80 p-3"><p className="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wide text-slate-500"><Clock3 size={12} /> Readiness mode</p><p className="mt-1 text-sm font-black capitalize text-slate-900">{String(readiness).replaceAll("_", " ")}</p></div>
        </div>
      </div>

      <div className="px-4 py-5 sm:px-6">
        <div className="relative">
          <div className="absolute left-7 right-7 top-7 hidden h-1 rounded-full bg-slate-200 sm:block" />
          <div className="absolute left-7 top-7 hidden h-1 rounded-full bg-gradient-to-r from-emerald-500 via-indigo-500 to-violet-500 transition-all sm:block" style={{ width: `${levels.length > 1 ? (currentIndex / (levels.length - 1)) * 100 : 0}%` }} />
          <div className="grid gap-3 sm:grid-cols-6">
            {levels.map((level, index) => {
              const isCurrent = index === currentIndex || level.status === "current";
              const isComplete = level.status === "complete" || index < currentIndex;
              const isLocked = !isComplete && !isCurrent;
              const color = levelColors[index % levelColors.length];
              const cardClass = isCurrent ? `${color.soft} ${color.border} shadow-lg shadow-indigo-100/60` : isComplete ? "border-emerald-200 bg-emerald-50/70" : "border-slate-200 bg-white/70";
              return (
                <div key={level.id} className={`relative rounded-2xl border p-3 transition ${cardClass}`}>
                  <div className="relative z-10 mx-auto flex h-9 w-9 items-center justify-center rounded-xl border-4 border-white bg-slate-200 text-xs font-black text-slate-600 shadow-sm">
                    {isComplete ? <Check size={16} className="text-emerald-700" /> : isLocked ? <LockKeyhole size={14} className="text-slate-400" /> : <span className={`bg-gradient-to-br ${color.tint} bg-clip-text text-transparent`}>L{index + 1}</span>}
                  </div>
                  <p className="mt-3 text-center text-[10px] font-black uppercase tracking-wide text-slate-500">Level {index + 1}</p>
                  <p className="mt-1 text-center text-xs font-black text-slate-900">{level.title}</p>
                  <p className="mt-1 line-clamp-3 text-center text-[10px] leading-4 text-slate-500">{level.focus}</p>
                  <div className="mt-3 text-center">{isComplete ? <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-700"><CheckCircle2 size={12} /> Evidence earned</span> : isCurrent ? <span className="inline-flex items-center gap-1 rounded-full bg-white px-2 py-1 text-[10px] font-black text-indigo-700 shadow-sm"><Play size={10} fill="currentColor" /> Play now</span> : <span className="text-[10px] font-semibold text-slate-400">Locked</span>}</div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="mt-5 grid gap-4 lg:grid-cols-[1fr_auto]">
          <div className="rounded-2xl border border-indigo-100 bg-white/80 p-4">
            <div className="flex items-start gap-3"><div className="rounded-xl bg-indigo-100 p-2 text-indigo-700"><ShieldCheck size={16} /></div><div><p className="text-xs font-black uppercase tracking-wide text-indigo-800">What unlocks the next level?</p><p className="mt-1 text-sm font-semibold text-slate-900">{levelProof[currentIndex] || current?.unlock || "Complete the next evidence check"}</p><p className="mt-1 text-xs leading-5 text-slate-500">The engine uses accuracy, varied questions, recency and timed performance. A single lucky score does not unlock a stage.</p></div></div>
          </div>
          <Link to={continueHref} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-2xl bg-indigo-700 px-5 py-3 text-sm font-black text-white shadow-lg shadow-indigo-200 transition hover:-translate-y-0.5 hover:bg-indigo-800">{currentIndex >= 3 ? "Run a timed mock" : `Continue Level ${currentIndex + 1}`} <ArrowRight size={16} /></Link>
        </div>

        <p className="mt-4 text-[11px] leading-5 text-slate-500">Target track: <span className="font-bold text-slate-700">{plan.assessment_track_label || "Service-company core"}</span>. Employer mock timing remains edition-specific; verify the official invitation before treating a simulation as an exact replica.</p>
      </div>
    </div>
  );
}
