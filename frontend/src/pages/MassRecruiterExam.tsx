import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import {
  AlarmClock,
  ArrowLeft,
  ArrowRight,
  Bookmark,
  CheckCircle2,
  FileStack,
  FlagTriangleRight,
} from "lucide-react";
import { MasteryBar, MentorAvatar, PageShell, ReadinessRing } from "../design-system";
import { Button } from "../design-system/Button";
import { massRecruiterApi } from "../services/api/massRecruiter";
import type {
  ExamBlueprint,
  ExamQuestion,
  ExamResult,
  ExamStart,
} from "../services/api/massRecruiter";

type Phase = "picker" | "runner" | "results";

export default function MassRecruiterExam() {
  const [phase, setPhase] = useState<Phase>("picker");
  const [exams, setExams] = useState<ExamBlueprint[]>([]);
  const [loadingList, setLoadingList] = useState(true);

  const [exam, setExam] = useState<ExamStart | null>(null);
  const [answers, setAnswers] = useState<Record<number, string | null>>({});
  const [marked, setMarked] = useState<Set<number>>(new Set());
  const [current, setCurrent] = useState(0);
  const [secondsLeft, setSecondsLeft] = useState(0);
  const [saving, setSaving] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const [result, setResult] = useState<ExamResult | null>(null);
  const submitRef = useRef<() => void>(() => {});

  useEffect(() => {
    massRecruiterApi
      .listExams()
      .then(r => setExams(r.exams))
      .catch(() => setError("Could not load exam list"))
      .finally(() => setLoadingList(false));
  }, []);

  const handleSubmit = useCallback(async () => {
    if (!exam || submitting) return;
    setSubmitting(true);
    setError("");
    try {
      const res = await massRecruiterApi.complete(exam.test_id);
      setResult(res);
      setPhase("results");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not submit exam");
    } finally {
      setSubmitting(false);
    }
  }, [exam, submitting]);

  submitRef.current = handleSubmit;

  useEffect(() => {
    if (phase !== "runner" || !exam) return;
    const endMs = new Date(exam.ends_at).getTime();
    const tick = () => {
      const left = Math.max(0, Math.floor((endMs - Date.now()) / 1000));
      setSecondsLeft(left);
      if (left === 0) {
        submitRef.current();
      }
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [phase, exam]);

  async function startExam(bp: ExamBlueprint) {
    setError("");
    try {
      const started = await massRecruiterApi.start(bp.exam_id);
      setExam(started);
      setAnswers({});
      setMarked(new Set());
      setCurrent(0);
      setResult(null);
      setPhase("runner");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not start the exam");
    }
  }

  function persistAnswer(idx: number, value: string | null, isMarked: boolean) {
    if (!exam) return;
    // fire-and-forget save; grading happens server-side on complete
    massRecruiterApi.saveAnswer(exam.test_id, idx, value, isMarked).catch(() => {});
  }

  function chooseOption(option: string) {
    if (!exam) return;
    const next = { ...answers, [current]: answers[current] === option ? null : option };
    setAnswers(next);
    persistAnswer(current, next[current], marked.has(current));
  }

  function toggleMark() {
    if (!exam) return;
    const next = new Set(marked);
    if (next.has(current)) next.delete(current);
    else next.add(current);
    setMarked(next);
    persistAnswer(current, answers[current] ?? null, next.has(current));
  }

  const activeSection = useMemo(() => {
    if (!exam) return null;
    return (
      exam.sections.find(
        s => current >= s.start_index && current <= s.end_index,
      ) ?? null
    );
  }, [exam, current]);

  const answeredCount = useMemo(
    () => Object.values(answers).filter(v => v !== null && v !== undefined).length,
    [answers],
  );

  const timerLabel = useMemo(() => {
    const m = Math.floor(secondsLeft / 60);
    const s = secondsLeft % 60;
    return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
  }, [secondsLeft]);

  if (phase === "picker") {
    return (
      <PageShell theme="focus">
        <div className="mx-auto max-w-3xl px-4 py-8 md:py-12">
          <header className="mb-10 flex items-center gap-4">
            <MentorAvatar size={64} mood="briefing" />
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-text-muted">
                Navigational tests
              </p>
              <h1 className="text-2xl font-extrabold text-text md:text-3xl">
                Mass Recruiter Exams
              </h1>
              <p className="text-sm text-text-muted">
                Full sectioned papers — real timing, real cutoffs, no hints mid-exam.
              </p>
            </div>
          </header>

          {error && (
            <p className="mb-4 rounded-lg border border-coral/30 bg-red-50 px-3 py-2 text-sm text-coral">
              {error}
            </p>
          )}

          {loadingList ? (
            <div className="grid gap-4 sm:grid-cols-2">
              {[0, 1, 2, 3].map(i => (
                <div key={i} className="h-40 animate-pulse rounded-xl bg-surface" />
              ))}
            </div>
          ) : (
            <section className="grid gap-4 sm:grid-cols-2">
              {exams.map(bp => (
                <button
                  key={bp.exam_id}
                  onClick={() => startExam(bp)}
                  className="rounded-xl border-2 border-line bg-surface p-4 text-left transition-colors hover:border-primary/50"
                >
                  <div className="mb-1 flex items-center justify-between">
                    <span className="font-extrabold text-text">{bp.name}</span>
                    {bp.locked ? (
                      <span className="rounded bg-reward/10 px-1.5 py-0.5 text-[10px] font-bold uppercase text-reward">
                        Locked
                      </span>
                    ) : (
                      <FileStack size={16} className="text-text-muted" />
                    )}
                  </div>
                  <p className="text-sm text-text-muted">{bp.description}</p>
                  <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-xs font-semibold text-ocean">
                    <span>{bp.total_questions} questions</span>
                    <span>{bp.total_minutes} min</span>
                    <span>
                      {bp.negative_marks > 0
                        ? `-${bp.negative_marks} per wrong`
                        : "no negative"}
                    </span>
                    <span>cutoff {bp.cutoff_pct}%</span>
                  </div>
                  <ul className="mt-2 space-y-0.5 text-xs text-text-muted">
                    {bp.sections.map(s => (
                      <li key={s.name}>
                        · {s.name}: {s.questions}q / {s.minutes}m
                      </li>
                    ))}
                  </ul>
                </button>
              ))}
            </section>
          )}

          <p className="mt-8 text-center text-sm text-text-muted">
            Infosys screen coming up?{" "}
            <Link to="/pseudocode" className="font-semibold text-ocean underline">
              Pseudocode dry-run drills →
            </Link>
            {" · "}
            <Link to="/consuls-route" className="font-semibold text-ocean underline">
              Big 4 Consul's Route →
            </Link>
          </p>
        </div>
      </PageShell>
    );
  }

  if (phase === "runner" && exam) {
    const q: ExamQuestion | undefined = exam.questions[current];
    const lowTime = secondsLeft <= 120;
    const locked = !!exam.locked;
    const isSpecial = !!q?.special;

    function goNext() {
      if (!exam) return;
      if (locked && !(answers[current] ?? "").trim()) {
        if (
          !window.confirm(
            "This paper is LOCKED — once you leave, you cannot come back to this question. Leave it unanswered?",
          )
        )
          return;
      }
      setCurrent(c => Math.min(exam.total_questions - 1, c + 1));
    }

    return (
      <PageShell theme="focus">
        <div className="mx-auto max-w-5xl px-4 py-6">
          <header className="mb-4 flex flex-wrap items-center justify-between gap-3 border-b border-line pb-3">
            <div className="flex items-center gap-3">
              <MentorAvatar size={40} mood="serious" />
              <div>
                <h1 className="text-sm font-extrabold text-text">{exam.exam_name}</h1>
                <p className="text-xs text-text-muted">
                  {answeredCount}/{exam.total_questions} answered
                  {activeSection ? ` · ${activeSection.name}` : ""}
                  {locked && (
                    <span className="ml-2 rounded bg-reward/10 px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-reward">
                      Locked · no going back
                    </span>
                  )}
                </p>
              </div>
            </div>
            <div
              className={`flex items-center gap-2 rounded-lg border px-3 py-1.5 font-mono text-sm font-bold ${
                lowTime
                  ? "border-coral/40 bg-red-50 text-coral"
                  : "border-line bg-surface text-text"
              }`}
              aria-live={lowTime ? "assertive" : "off"}
            >
              <AlarmClock size={15} className={lowTime ? "text-coral" : "text-text-muted"} />
              {timerLabel}
            </div>
          </header>

          {/* question palette (hidden on locked papers, like the real NQT) */}
          <div className="mb-4 flex gap-4">
            {!locked && (
              <div className="hidden w-56 shrink-0 sm:block">
                <div className="max-h-[60vh] overflow-y-auto rounded-xl border border-line bg-surface p-3">
                  {exam.sections.map(sec => (
                    <div key={sec.name} className="mb-3 last:mb-0">
                      <p className="mb-1.5 text-[11px] font-bold uppercase tracking-wider text-text-muted">
                        {sec.name}
                      </p>
                      <div className="grid grid-cols-5 gap-1.5">
                        {Array.from({ length: sec.count }, (_, i) => {
                          const idx = sec.start_index + i;
                          const state =
                            idx === current
                              ? "border-primary ring-2 ring-primary/30 bg-mint/60 text-text"
                              : answers[idx]
                                ? "border-primary/40 bg-primary/10 text-primary"
                                : marked.has(idx)
                                  ? "border-reward/50 bg-reward/10 text-reward"
                                  : "border-line bg-canvas text-text-muted hover:border-primary/40";
                          return (
                            <button
                              key={idx}
                              onClick={() => setCurrent(idx)}
                              aria-label={`Question ${idx + 1}`}
                              className={`h-8 rounded-md border text-xs font-bold ${state}`}
                            >
                              {idx + 1}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* current question */}
            <div className="min-w-0 flex-1">
              <div className="rounded-xl border border-line bg-surface p-5">
                <div className="mb-3 flex items-center justify-between">
                  <p className="text-xs font-bold uppercase tracking-wider text-text-muted">
                    Q{current + 1}
                    {q?.sub_category ? ` · ${q.sub_category}` : ""}
                    {q?.special === "email" && " · type your email below"}
                    {q?.special === "coding" && " · write your solution below"}
                  </p>
                  {!locked && (
                    <button
                      onClick={toggleMark}
                      className={`flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-semibold ${
                        marked.has(current)
                          ? "border-reward/50 bg-reward/10 text-reward"
                          : "border-line text-text-muted hover:text-text"
                      }`}
                    >
                      <Bookmark size={13} />
                      {marked.has(current) ? "Marked" : "Mark for review"}
                    </button>
                  )}
                </div>
                <p className="mb-5 whitespace-pre-wrap text-sm leading-relaxed text-text">
                  {q?.question}
                </p>
                {isSpecial ? (
                  <div>
                    <textarea
                      value={answers[current] ?? ""}
                      onChange={e =>
                        setAnswers(a => ({ ...a, [current]: e.target.value }))
                      }
                      onBlur={() =>
                        persistAnswer(
                          current,
                          answers[current] ?? "",
                          marked.has(current),
                        )
                      }
                      rows={q?.special === "coding" ? 16 : 9}
                      spellCheck={q?.special !== "coding"}
                      placeholder={
                        q?.special === "email"
                          ? "Subject line, greeting, body, sign-off…"
                          : "// Write your solution (any language or pseudocode)"
                      }
                      className={`w-full rounded-lg border border-line bg-canvas p-3 text-sm leading-relaxed text-text outline-none focus:border-primary/60 ${
                        q?.special === "coding" ? "font-mono" : ""
                      }`}
                    />
                    {q?.special === "email" && (
                      <p className="mt-1.5 text-xs text-text-muted">
                        {(answers[current] ?? "").trim().split(/\s+/).filter(Boolean).length} words — aim for 120–180.
                      </p>
                    )}
                  </div>
                ) : (
                  <div className="space-y-2.5">
                    {(q?.options ?? []).map(opt => {
                      const selected = answers[current] === opt;
                      return (
                        <button
                          key={opt}
                          onClick={() => chooseOption(opt)}
                          className={`w-full rounded-lg border px-3.5 py-2.5 text-left text-sm transition-colors ${
                            selected
                              ? "border-primary bg-mint/60 font-semibold text-text"
                              : "border-line bg-canvas text-text hover:border-primary/40"
                          }`}
                        >
                          {opt}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>

              <div className="mt-4 flex items-center justify-between">
                {locked ? (
                  <span className="text-xs font-semibold text-text-muted">
                    Forward only — answered screens are sealed.
                  </span>
                ) : (
                  <Button
                    variant="outline"
                    disabled={current === 0}
                    onClick={() => setCurrent(c => Math.max(0, c - 1))}
                  >
                    <ArrowLeft size={14} /> Prev
                  </Button>
                )}
                {current < exam.total_questions - 1 ? (
                  <Button variant="primary" onClick={goNext}>
                    Next <ArrowRight size={14} />
                  </Button>
                ) : (
                  <Button variant="gold" loading={submitting} onClick={handleSubmit}>
                    <FlagTriangleRight size={14} /> Submit Exam
                  </Button>
                )}
              </div>

              {error && (
                <p className="mt-3 rounded-lg border border-coral/30 bg-red-50 px-3 py-2 text-sm text-coral">
                  {error}
                </p>
              )}
            </div>
          </div>

          <footer className="border-t border-line pt-3 text-center">
            <Button variant="danger" size="sm" loading={submitting} onClick={handleSubmit}>
              End &amp; Submit ({exam.total_questions - answeredCount} unanswered)
            </Button>
          </footer>
        </div>
      </PageShell>
    );
  }

  // results
  const stats = result?.section_stats ?? {};

  return (
    <PageShell theme="celebration">
      <div className="mx-auto max-w-3xl px-4 py-8 md:py-12">
        <header className="mb-8 flex flex-col items-center text-center">
          <ReadinessRing value={result?.score ?? 0} size={132} label="Score %" />
          <span
            className={`mt-3 inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-sm font-bold ${
              result?.passed_cutoff
                ? "border-primary/40 bg-mint/50 text-primary"
                : "border-coral/40 bg-red-50 text-coral"
            }`}
          >
            <CheckCircle2 size={15} />
            {result?.passed_cutoff
              ? `Cleared the ${result.cutoff_pct}% cutoff`
              : `Below the ${result.cutoff_pct}% cutoff`}
          </span>
          <h1 className="mt-2 text-2xl font-extrabold text-text">{result?.exam_name}</h1>
          <p className="text-sm text-text-muted">{result?.message}</p>
        </header>

        <section className="bounty-card mb-6 grid grid-cols-2 gap-4 p-5 sm:grid-cols-4">
          <Stat label="Correct" value={result?.correct_answers ?? 0} tone="text-primary" />
          <Stat label="Wrong" value={result?.wrong_answers ?? 0} tone="text-coral" />
          <Stat label="Skipped" value={result?.skipped_answers ?? 0} tone="text-text-muted" />
          <Stat
            label={`Net${result && result.negative_marks > 0 ? ` (-${result.negative_marks}/w)` : ""}`}
            value={result?.net_score ?? 0}
            tone="text-ocean"
          />
        </section>

        {Object.keys(stats).length > 0 && (
          <section className="bounty-card mb-6 space-y-3 p-5">
            <h2 className="text-xs font-bold uppercase tracking-widest text-text-muted">
              Section breakdown
            </h2>
            {Object.entries(stats).map(([name, s]) => (
              <MasteryBar
                key={name}
                label={`${name} (${s.correct}/${s.total})`}
                value={(s.correct / Math.max(s.total, 1)) * 100}
                tone="ocean"
              />
            ))}
          </section>
        )}

        {result?.subjective && Object.keys(result.subjective).length > 0 && (
          <section className="bounty-card mb-6 space-y-4 p-5">
            <h2 className="text-xs font-bold uppercase tracking-widest text-text-muted">
              Graded tasks (AI evaluated)
            </h2>
            {Object.entries(result.subjective).map(([name, group]) => (
              <div key={name}>
                <MasteryBar
                  label={`${name} — avg ${group.avg_score}/100`}
                  value={group.avg_score}
                  tone="gold"
                />
                <ul className="mt-1.5 space-y-1">
                  {group.items.map(item => (
                    <li key={item.label} className="text-xs text-text-muted">
                      <span className="font-bold text-text">{item.label}:</span>{" "}
                      {item.score}/100 — {item.feedback}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </section>
        )}

        {!!result?.weak_areas?.length && (
          <section className="mb-6 rounded-xl border border-coral/25 bg-red-50 p-4">
            <h2 className="mb-2 text-xs font-bold uppercase tracking-widest text-coral">
              Drill these before the real drive
            </h2>
            <div className="flex flex-wrap gap-2">
              {result.weak_areas.map(w => (
                <span
                  key={w.category}
                  className="rounded-full border border-coral/30 bg-surface px-2.5 py-1 text-xs font-semibold text-text"
                >
                  {w.category} · {Math.round(w.accuracy)}%
                </span>
              ))}
            </div>
          </section>
        )}

        {!!result?.xp_earned && (
          <p className="mb-6 text-center text-sm font-bold text-reward">
            +{result.xp_earned} XP earned
          </p>
        )}

        <div className="flex flex-wrap items-center justify-center gap-3">
          <Button
            size="lg"
            onClick={() => {
              setPhase("picker");
              setExam(null);
              setResult(null);
            }}
          >
            Run Another Exam
          </Button>
          <Link to="/home">
            <Button variant="ghost" size="lg">
              Back to Home
            </Button>
          </Link>
        </div>
      </div>
    </PageShell>
  );
}

function Stat({
  label,
  value,
  tone,
}: {
  label: string;
  value: number | string;
  tone: string;
}) {
  return (
    <div className="text-center">
      <p className={`text-xl font-extrabold ${tone}`}>{value}</p>
      <p className="text-xs font-medium text-text-muted">{label}</p>
    </div>
  );
}
