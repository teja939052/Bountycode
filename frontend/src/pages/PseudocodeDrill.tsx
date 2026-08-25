import { useEffect, useMemo, useRef, useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Terminal,
  XCircle,
} from "lucide-react";
import { MasteryBar, MentorAvatar, PageShell } from "../design-system";
import { Button } from "../design-system/Button";
import { pseudocodeApi } from "../services/api/pseudocode";
import type {
  CheckResult,
  PseudocodeQuestion,
} from "../services/api/pseudocode";

type Phase = "setup" | "drill" | "done";

interface AnswerState {
  selected: string | null;
  result: CheckResult | null;
}

export default function PseudocodeDrill() {
  const [phase, setPhase] = useState<Phase>("setup");
  const [meta, setMeta] = useState<{ total: number; topics: Record<string, number> } | null>(
    null,
  );
  const [topic, setTopic] = useState("");
  const [count, setCount] = useState(10);

  const [questions, setQuestions] = useState<PseudocodeQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<number, AnswerState>>({});
  const [current, setCurrent] = useState(0);
  const [loading, setLoading] = useState(false);
  const [checking, setChecking] = useState(false);
  const [error, setError] = useState("");

  const [summary, setSummary] = useState<{
    accuracy: number;
    xp_gained: number;
    message: string;
  } | null>(null);

  const codeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    pseudocodeApi
      .meta()
      .then(setMeta)
      .catch(() => {});
  }, []);

  async function startDrill() {
    setLoading(true);
    setError("");
    try {
      const res = await pseudocodeApi.getQuestions(count, topic || undefined);
      setQuestions(res.questions);
      setAnswers({});
      setCurrent(0);
      setSummary(null);
      setPhase("drill");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load questions");
    } finally {
      setLoading(false);
    }
  }

  async function choose(option: string) {
    const q = questions[current];
    if (!q || answers[current]?.result) return;
    setChecking(true);
    try {
      const result = await pseudocodeApi.check(q.id, option);
      setAnswers(prev => ({ ...prev, [current]: { selected: option, result } }));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Check failed");
    } finally {
      setChecking(false);
    }
  }

  async function finishDrill() {
    const answered = Object.values(answers).filter(a => a.result);
    const correct = answered.filter(a => a.result?.is_correct).length;
    try {
      const res = await pseudocodeApi.complete(correct, answered.length || 1);
      setSummary(res);
    } catch {
      setSummary({
        accuracy: Math.round((correct / Math.max(answered.length, 1)) * 100),
        xp_gained: 0,
        message: "Drill finished (stats log failed — accuracy still shown).",
      });
    }
    setPhase("done");
  }

  const stats = useMemo(() => {
    const answered = Object.values(answers).filter(a => a.result);
    return {
      correct: answered.filter(a => a.result?.is_correct).length,
      answered: answered.length,
    };
  }, [answers]);

  // ---------- setup ----------
  if (phase === "setup") {
    return (
      <PageShell theme="focus">
        <div className="mx-auto max-w-3xl px-4 py-8 md:py-12">
          <header className="mb-10 flex items-center gap-4">
            <MentorAvatar size={64} mood="briefing" />
            <div>
              <p className="text-xs font-bold uppercase tracking-widest text-text-muted">
                Infosys-style drills
              </p>
              <h1 className="text-2xl font-extrabold text-text md:text-3xl">
                Pseudocode Dry-Run
              </h1>
              <p className="text-sm text-text-muted">
                No compiler. Trace it in your head — exactly like the real screen.
              </p>
            </div>
          </header>

          <section className="bounty-card mb-6 p-5">
            <p className="mb-3 text-xs font-bold uppercase tracking-wider text-text-muted">
              Topics {meta ? `(${meta.total} questions)` : ""}
            </p>
            <div className="flex flex-wrap gap-1.5">
              <button
                onClick={() => setTopic("")}
                className={`rounded-full border px-3 py-1 text-xs font-semibold ${
                  !topic
                    ? "border-primary bg-primary text-white"
                    : "border-line bg-surface text-text-muted hover:text-text"
                }`}
              >
                All topics
              </button>
              {meta &&
                Object.entries(meta.topics).map(([t, n]) => (
                  <button
                    key={t}
                    onClick={() => setTopic(t)}
                    className={`rounded-full border px-3 py-1 text-xs font-semibold ${
                      topic === t
                        ? "border-primary bg-primary text-white"
                        : "border-line bg-surface text-text-muted hover:text-text"
                    }`}
                  >
                    {t} · {n}
                  </button>
                ))}
            </div>

            <p className="mb-2 mt-4 text-xs font-bold uppercase tracking-wider text-text-muted">
              Drill length
            </p>
            <div className="flex gap-1.5">
              {[5, 10, 15].map(c => (
                <button
                  key={c}
                  onClick={() => setCount(c)}
                  className={`rounded-lg border px-4 py-1.5 text-sm font-bold ${
                    count === c
                      ? "border-primary bg-mint/60 text-text"
                      : "border-line bg-surface text-text-muted hover:text-text"
                  }`}
                >
                  {c}
                </button>
              ))}
            </div>
          </section>

          {error && (
            <p className="mb-4 rounded-lg border border-coral/30 bg-red-50 px-3 py-2 text-sm text-coral">
              {error}
            </p>
          )}

          <div className="flex items-center gap-3">
            <Button size="lg" loading={loading} onClick={startDrill}>
              <Terminal size={16} /> Start dry run
            </Button>
            <Link to="/mass-recruiter">
              <Button variant="ghost" size="lg">
                Full exams instead
              </Button>
            </Link>
          </div>
        </div>
      </PageShell>
    );
  }

  // ---------- done ----------
  if (phase === "done") {
    return (
      <PageShell theme="celebration">
        <div className="mx-auto max-w-3xl px-4 py-8 md:py-12">
          <header className="mb-8 flex flex-col items-center text-center">
            <MentorAvatar size={72} mood={summary && summary.accuracy >= 60 ? "proud" : "encouraging"} />
            <h1 className="mt-4 text-2xl font-extrabold text-text">Dry run complete</h1>
            <p className="text-sm text-text-muted">{summary?.message}</p>
            {!!summary?.xp_gained && (
              <p className="mt-1 text-sm font-bold text-reward">+{summary.xp_gained} XP</p>
            )}
          </header>

          <section className="bounty-card mb-6 p-5">
            <MasteryBar
              label="Accuracy"
              value={summary?.accuracy ?? 0}
              tone={(summary?.accuracy ?? 0) >= 60 ? "primary" : "coral"}
            />
            <p className="mt-3 text-xs text-text-muted">
              {stats.correct}/{stats.answered} traced correctly.
            </p>
          </section>

          {/* review mistakes */}
          {Object.entries(answers).some(([, a]) => a.result && !a.result.is_correct) && (
            <section className="mb-6 rounded-xl border border-coral/25 bg-red-50 p-4">
              <h2 className="mb-2 text-xs font-bold uppercase tracking-widest text-coral">
                Review these traces
              </h2>
              <ul className="space-y-2 text-sm">
                {Object.entries(answers)
                  .filter(([, a]) => a.result && !a.result.is_correct)
                  .map(([idx, a]) => (
                    <li key={idx} className="text-text">
                      Q{Number(idx) + 1} ({questions[Number(idx)]?.sub_category}):{" "}
                      <span className="font-semibold">answer is {a.result?.correct_answer}</span> —{" "}
                      {a.result?.explanation}
                    </li>
                  ))}
              </ul>
            </section>
          )}

          <div className="flex flex-wrap items-center justify-center gap-3">
            <Button
              size="lg"
              onClick={() => {
                setPhase("setup");
                setQuestions([]);
                setAnswers({});
              }}
            >
              Run another drill
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

  // ---------- drill ----------
  const q = questions[current];
  const state = answers[current];
  const locked = !!state?.result;

  return (
    <PageShell theme="focus">
      <div className="mx-auto max-w-3xl px-4 py-6 md:py-10">
        <header className="mb-4 flex items-center justify-between border-b border-line pb-3">
          <div className="flex items-center gap-3">
            <MentorAvatar size={40} mood="serious" />
            <div>
              <h1 className="text-sm font-extrabold text-text">Pseudocode Dry-Run</h1>
              <p className="text-xs text-text-muted">
                Q{current + 1}/{questions.length} · {q?.sub_category} ·{" "}
                {stats.correct}/{stats.answered} correct
              </p>
            </div>
          </div>
        </header>

        {/* progress dots */}
        <div className="mb-4 flex flex-wrap gap-1.5">
          {questions.map((_, i) => {
            const a = answers[i];
            return (
              <button
                key={i}
                onClick={() => setCurrent(i)}
                aria-label={`Go to question ${i + 1}`}
                className={`h-2.5 w-6 rounded-full transition-colors ${
                  i === current
                    ? "bg-ocean"
                    : a?.result?.is_correct
                      ? "bg-primary"
                      : a?.result
                        ? "bg-coral"
                        : "bg-mint"
                }`}
              />
            );
          })}
        </div>

        <div ref={codeRef} className="rounded-xl border border-line bg-surface p-5">
          <pre className="overflow-x-auto whitespace-pre-wrap rounded-lg border border-line bg-canvas p-4 font-mono text-[13px] leading-relaxed text-text">
            {q?.question}
          </pre>

          <div className="mt-4 space-y-2.5">
            {(q?.options ?? []).map(opt => {
              const picked = state?.selected === opt;
              const revealed = state?.result;
              const isRight = revealed && opt === revealed.correct_answer;
              const isWrongPick = revealed && picked && !revealed.is_correct;
              return (
                <button
                  key={opt}
                  disabled={locked || checking}
                  onClick={() => choose(opt)}
                  className={`w-full rounded-lg border px-3.5 py-2.5 text-left font-mono text-sm transition-colors disabled:cursor-default ${
                    isRight
                      ? "border-primary bg-mint/50 font-semibold text-text"
                      : isWrongPick
                        ? "border-coral bg-red-50 text-text"
                        : picked
                          ? "border-ocean/50 bg-canvas font-semibold text-text"
                          : "border-line bg-canvas text-text hover:border-primary/40 disabled:hover:border-line"
                  }`}
                >
                  {opt}
                  {isRight && <CheckCircle2 size={15} className="ml-2 inline text-primary" />}
                  {isWrongPick && <XCircle size={15} className="ml-2 inline text-coral" />}
                </button>
              );
            })}
          </div>

          {state?.result && (
            <div
              className={`mt-4 rounded-lg border p-3 text-sm leading-relaxed ${
                state.result.is_correct
                  ? "border-primary/30 bg-mint/30 text-text"
                  : "border-coral/30 bg-red-50 text-text"
              }`}
            >
              <span className="mr-1 font-bold">
                {state.result.is_correct ? "Clean trace." : "Off course."}
              </span>
              {state.result.explanation}
            </div>
          )}

          {error && (
            <p className="mt-3 rounded-lg border border-coral/30 bg-red-50 px-3 py-2 text-sm text-coral">
              {error}
            </p>
          )}
        </div>

        <div className="mt-4 flex items-center justify-between">
          <Button
            variant="outline"
            disabled={current === 0}
            onClick={() => setCurrent(i => Math.max(0, i - 1))}
          >
            <ArrowLeft size={14} /> Prev
          </Button>
          {current < questions.length - 1 ? (
            <Button
              variant="primary"
              disabled={!locked}
              title={locked ? undefined : "Answer first"}
              onClick={() => setCurrent(i => Math.min(questions.length - 1, i + 1))}
            >
              Next <ArrowRight size={14} />
            </Button>
          ) : (
            <Button variant="gold" onClick={finishDrill}>
              Finish &amp; Log
            </Button>
          )}
        </div>
      </div>
    </PageShell>
  );
}
