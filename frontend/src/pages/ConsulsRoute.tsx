import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Compass, Scale, Database } from "lucide-react";
import { MasteryBar, MentorAvatar, PageShell } from "../design-system";
import {
  bigFourApi,
  type Big4Firm,
  type CaseDetail,
  type CaseGrade,
  type CaseMeta,
  type SqlQuestion,
} from "../services/api/bigFour.ts";

type Tab = "firms" | "case" | "sql";

export default function ConsulsRoute() {
  const [tab, setTab] = useState<Tab>("firms");

  return (
    <PageShell theme="adventure">
      <div className="mx-auto max-w-4xl px-4 py-8 md:py-12">
        <header className="mb-8 flex items-center gap-4">
          <MentorAvatar size={64} mood="briefing" />
          <div>
            <p className="text-xs font-bold uppercase tracking-widest text-text-muted">
              The Consul's Trade Route
            </p>
            <h1 className="text-2xl font-extrabold text-text md:text-3xl">
              Big 4 Prep — Deloitte · PwC · EY · KPMG
            </h1>
            <p className="text-sm text-text-muted">
              Firm intel, case-study practice on the consulting framework, and
              SQL screening drills.
            </p>
          </div>
        </header>

        <nav className="mb-6 flex flex-wrap gap-2">
          {(
            [
              { key: "firms", label: "Firm Intel", icon: Compass },
              { key: "case", label: "Case Practice", icon: Scale },
              { key: "sql", label: "SQL Drill", icon: Database },
            ] as const
          ).map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setTab(key)}
              className={`flex items-center gap-1.5 rounded-full border px-3.5 py-1.5 text-sm font-bold transition-colors ${
                tab === key
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-line bg-surface text-text-muted hover:text-text"
              }`}
            >
              <Icon size={14} />
              {label}
            </button>
          ))}
        </nav>

        {tab === "firms" && <FirmsTab />}
        {tab === "case" && <CaseTab />}
        {tab === "sql" && <SqlTab />}

        <p className="mt-10 text-center text-sm text-text-muted">
          Partner-round nerves?{" "}
          <Link to="/behavioral-practice" className="font-semibold text-ocean underline">
            Behavioral practice →
          </Link>
        </p>
      </div>
    </PageShell>
  );
}

function FirmsTab() {
  const [firms, setFirms] = useState<Big4Firm[] | null>(null);

  useEffect(() => {
    bigFourApi.firms().then(r => setFirms(r.firms)).catch(() => setFirms([]));
  }, []);

  if (!firms) return <SkeletonCards />;
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {firms.map(f => (
        <article key={f.firm_id} className="bounty-card p-5">
          <h2 className="font-extrabold text-text">{f.name}</h2>
          <p className="mt-0.5 text-xs text-text-muted">{f.tagline}</p>

          <p className="mt-3 text-[11px] font-bold uppercase tracking-wider text-text-muted">
            Values they probe
          </p>
          <ul className="mt-1 space-y-0.5 text-xs text-text">
            {f.values.map(v => (
              <li key={v}>· {v}</li>
            ))}
          </ul>

          <p className="mt-3 text-[11px] font-bold uppercase tracking-wider text-text-muted">
            Round map
          </p>
          <ol className="mt-1 space-y-0.5 text-xs text-text">
            {f.rounds.map((r, i) => (
              <li key={r}>
                {i + 1}. {r}
              </li>
            ))}
          </ol>

          <p className="mt-3 text-[11px] font-bold uppercase tracking-wider text-reward">
            Captain Byte's tips
          </p>
          <ul className="mt-1 space-y-0.5 text-xs italic text-text-muted">
            {f.prep_tips.map(t => (
              <li key={t}>“{t}”</li>
            ))}
          </ul>
        </article>
      ))}
    </div>
  );
}

function CaseTab() {
  const [cases, setCases] = useState<CaseMeta[] | null>(null);
  const [active, setActive] = useState<CaseDetail | null>(null);
  const [response, setResponse] = useState("");
  const [grading, setGrading] = useState(false);
  const [grade, setGrade] = useState<CaseGrade | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    bigFourApi.cases().then(r => setCases(r.cases)).catch(() => setCases([]));
  }, []);

  async function openCase(id: string) {
    setError("");
    try {
      const r = await bigFourApi.getCase(id);
      setActive(r.case);
      setResponse("");
      setGrade(null);
    } catch {
      setError("Could not load that case.");
    }
  }

  async function submit() {
    if (!active || !response.trim()) return;
    setGrading(true);
    setError("");
    try {
      setGrade(await bigFourApi.submitCase(active.case_id, response));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Grading failed");
    } finally {
      setGrading(false);
    }
  }

  if (!active) {
    if (!cases) return <SkeletonCards />;
    return (
      <section className="grid gap-3 sm:grid-cols-2">
        {cases.map(c => (
          <button
            key={c.case_id}
            onClick={() => openCase(c.case_id)}
            className="bounty-card text-left transition-transform hover:-translate-y-0.5"
          >
            <span className="text-[10px] font-bold uppercase tracking-widest text-ocean">
              {c.firm_id}
            </span>
            <p className="mt-1 font-extrabold text-text">{c.title}</p>
            <p className="mt-2 text-xs font-semibold text-ocean">Open brief →</p>
          </button>
        ))}
      </section>
    );
  }

  const words = response.trim().split(/\s+/).filter(Boolean).length;

  return (
    <section>
      <Button variant="ghost" size="sm" onClick={() => setActive(null)}>
        ← All cases
      </Button>
      <div className="bounty-card mt-3 p-5">
        <span className="text-[10px] font-bold uppercase tracking-widest text-ocean">
          {active.firm_id}
        </span>
        <h2 className="mt-0.5 text-lg font-extrabold text-text">{active.title}</h2>
        <p className="mt-3 whitespace-pre-wrap rounded-lg border border-line bg-canvas p-3 text-sm leading-relaxed text-text">
          {active.context}
        </p>
        <p className="mt-3 text-sm font-semibold text-text">{active.task}</p>

        <textarea
          value={response}
          onChange={e => setResponse(e.target.value)}
          rows={9}
          placeholder="Structure your answer across Identify → Assess → Prioritize → Mitigate → Monitor…"
          className="mt-4 w-full rounded-lg border border-line bg-canvas p-3 text-sm leading-relaxed text-text outline-none focus:border-primary/60"
        />
        <div className="mt-2 flex items-center justify-between">
          <p className="text-xs text-text-muted">{words} words</p>
          <Button variant="gold" loading={grading} disabled={!response.trim()} onClick={submit}>
            Submit for grading
          </Button>
        </div>

        {error && (
          <p className="mt-3 rounded-lg border border-coral/30 bg-red-50 px-3 py-2 text-sm text-coral">
            {error}
          </p>
        )}

        {grade && (
          <div className="mt-5 space-y-3 border-t border-line pt-4">
            <MasteryBar
              label={`Overall ${grade.overall}/${grade.max_overall ?? 100}`}
              value={(grade.overall * 100) / Math.max(grade.max_overall ?? 100, 1)}
              tone="gold"
            />
            {grade.dimensions.map(d => (
              <div key={d.name}>
                <MasteryBar label={`${d.name} (${d.score}/20)`} value={d.score * 5} tone="ocean" />
                {d.note && <p className="mt-0.5 text-xs text-text-muted">{d.note}</p>}
              </div>
            ))}
            <p className="rounded-lg bg-mint/40 p-3 text-sm text-text">
              {grade.feedback}
            </p>
          </div>
        )}
      </div>
    </section>
  );
}

const SQL_TOPICS = ["", "Basics", "Joins", "Aggregates", "Subqueries", "Indexes", "Normalization", "Set Ops", "Transactions", "DDL vs DML", "Keys", "Window Functions", "Nulls", "Performance"];

function SqlTab() {
  const [phase, setPhase] = useState<"setup" | "drill">("setup");
  const [topic, setTopic] = useState("");
  const [questions, setQuestions] = useState<SqlQuestion[]>([]);
  const [idx, setIdx] = useState(0);
  const [picked, setPicked] = useState<string | null>(null);
  const [check, setCheck] = useState<{ correct: boolean; correct_answer: string; explanation: string } | null>(null);
  const [score, setScore] = useState(0);

  const finish = useCallback(
    async (finalScore: number, total: number) => {
      try {
        await bigFourApi.sqlComplete(finalScore, total);
      } catch {
        /* non-blocking */
      }
    },
    [],
  );

  async function begin(count: number) {
    const r = await bigFourApi.sqlQuestions(count, topic);
    setQuestions(r.questions);
    setPhase("drill");
    setIdx(0);
    setScore(0);
    setPicked(null);
    setCheck(null);
  }

  async function choose(opt: string) {
    if (check || !questions[idx]) return;
    setPicked(opt);
    try {
      const res = await bigFourApi.sqlCheck(questions[idx].id, opt);
      setCheck(res);
      if (res.correct) setScore(s => s + 1);
    } catch {
      /* stay */
    }
  }

  async function next() {
    if (idx + 1 >= questions.length) {
      await finish(score, questions.length);
      setPhase("setup");
      setQuestions([]);
      return;
    }
    setIdx(i => i + 1);
    setPicked(null);
    setCheck(null);
  }

  if (phase === "setup") {
    return (
      <section className="bounty-card mx-auto max-w-md p-6 text-center">
        <MentorAvatar size={56} mood="briefing" />
        <h2 className="mt-3 text-lg font-extrabold text-text">SQL Screening Drill</h2>
        <p className="mt-1 text-sm text-text-muted">
          The filter test before technical rounds. Instant explanations.
        </p>
        <select
          value={topic}
          onChange={e => setTopic(e.target.value)}
          className="mx-auto mt-4 block rounded-lg border border-line bg-surface px-3 py-2 text-sm text-text"
        >
          {SQL_TOPICS.map(t => (
            <option key={t} value={t}>{t || "All topics"}</option>
          ))}
        </select>
        <div className="mt-4 flex justify-center gap-3">
          <Button size="lg" onClick={() => begin(8)}>Quick · 8</Button>
          <Button variant="gold" size="lg" onClick={() => begin(15)}>Full sweep · 15</Button>
        </div>
      </section>
    );
  }

  const q = questions[idx];
  return (
    <section className="bounty-card p-5">
      <div className="mb-3 flex items-center justify-between">
        <p className="text-xs font-bold uppercase tracking-wider text-text-muted">
          Q{idx + 1}/{questions.length} · {q?.topic}
        </p>
        <p className="text-xs font-bold text-primary">{score} correct</p>
      </div>
      <p className="mb-4 whitespace-pre-wrap text-sm leading-relaxed text-text">{q?.question}</p>
      <div className="space-y-2.5">
        {(q?.options ?? []).map(opt => {
          const isPicked = picked === opt;
          const revealCorrect = check && opt === check.correct_answer;
          const cls = revealCorrect
            ? "border-primary bg-mint/60 font-semibold text-text"
            : isPicked && check
              ? "border-coral/50 bg-red-50 text-coral"
              : isPicked
                ? "border-primary/50 bg-primary/10 text-text"
                : "border-line bg-canvas text-text hover:border-primary/40";
          return (
            <button
              key={opt}
              onClick={() => choose(opt)}
              disabled={!!check}
              className={`w-full rounded-lg border px-3.5 py-2.5 text-left text-sm transition-colors ${cls}`}
            >
              {opt}
            </button>
          );
        })}
      </div>
      {check && (
        <div className="mt-4 rounded-lg bg-mint/40 p-3 text-sm text-text">
          {check.explanation}
          <div className="mt-3">
            <Button size="sm" variant="primary" onClick={next}>
              {idx + 1 >= questions.length ? "Finish drill" : "Next"}
            </Button>
          </div>
        </div>
      )}
    </section>
  );
}

function SkeletonCards() {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      {[0, 1, 2, 3].map(i => (
        <div key={i} className="h-48 animate-pulse rounded-xl bg-surface" />
      ))}
    </div>
  );
}
