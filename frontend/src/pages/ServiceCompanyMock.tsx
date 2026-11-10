import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  ArrowLeft,
  Building2,
  CheckCircle2,
  Loader2,
  Target,
  Timer,
  XCircle,
  Zap,
} from "lucide-react";
import api from "../services/api";

const COMPANIES = [
  { key: "tcs", label: "TCS NQT" },
  { key: "infosys", label: "Infosys" },
  { key: "wipro", label: "Wipro NLTH" },
  { key: "cognizant", label: "Cognizant GenC" },
  { key: "accenture", label: "Accenture" },
] as const;

type Question = {
  id: string;
  order: number;
  section?: string;
  section_label?: string;
  topic?: string;
  difficulty?: string;
  prompt: string;
  options: string[];
  time_sec_target?: number;
};

/**
 * Timed service-company OA mock.
 * Questions sampled by company ontology weights; graded only on the server.
 */
export default function ServiceCompanyMock() {
  const [company, setCompany] = useState("tcs");
  const [count, setCount] = useState(15);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [meta, setMeta] = useState<any>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [idx, setIdx] = useState(0);
  const [startedAt, setStartedAt] = useState<number>(0);
  const [result, setResult] = useState<any>(null);
  const [bankTotal, setBankTotal] = useState<number | null>(null);

  useEffect(() => {
    api.serviceOa
      .bankStats()
      .then((res: any) => setBankTotal(res?.data?.total ?? null))
      .catch(() => {});
  }, []);

  const start = async () => {
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res: any = await api.serviceOa.startMock({
        company,
        question_count: count,
      });
      const data = res?.data;
      if (!data?.session_id) throw new Error("Could not start mock");
      setSessionId(data.session_id);
      setMeta(data);
      setQuestions(data.questions || []);
      setAnswers({});
      setIdx(0);
      setStartedAt(Date.now());
    } catch (e: any) {
      setError(e?.message || "Failed to start mock");
    } finally {
      setLoading(false);
    }
  };

  const submit = async () => {
    if (!sessionId) return;
    setLoading(true);
    setError("");
    try {
      const res: any = await api.serviceOa.gradeMock({
        session_id: sessionId,
        answers,
        time_spent_sec: Math.max(0, Math.floor((Date.now() - startedAt) / 1000)),
      });
      setResult(res?.data);
      setSessionId(null);
    } catch (e: any) {
      setError(e?.message || "Grading failed");
    } finally {
      setLoading(false);
    }
  };

  const q = questions[idx];
  const answered = useMemo(() => Object.keys(answers).length, [answers]);

  if (result) {
    return (
      <div className="mx-auto max-w-2xl space-y-6 px-4 py-8">
        <Link to="/academy" className="inline-flex items-center gap-1 text-sm text-slate-500">
          <ArrowLeft size={14} /> Academy
        </Link>
        <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h1 className="text-2xl font-black text-slate-900">Mock result</h1>
          <p className="mt-1 text-sm text-slate-600">{result.message}</p>
          <p className="mt-4 text-4xl font-black text-emerald-700">{result.score_pct}%</p>
          <p className="text-sm text-slate-500">
            {result.correct}/{result.total} correct · band: {result.band}
          </p>
          <div className="mt-6 space-y-2">
            {Object.entries(result.section_scores || {}).map(([k, v]: any) => (
              <div key={k} className="flex items-center justify-between rounded-xl border border-slate-100 px-3 py-2 text-sm">
                <span className="font-semibold text-slate-800">{v.label || k}</span>
                <span className="text-slate-600">
                  {v.correct}/{v.total} · {v.score_pct}%
                </span>
              </div>
            ))}
          </div>
          {result.weak_topics?.length > 0 && (
            <div className="mt-6">
              <h2 className="text-sm font-bold uppercase tracking-wide text-amber-800">Weak topics</h2>
              <div className="mt-2 flex flex-wrap gap-2">
                {result.weak_topics.map((t: any) => (
                  <Link
                    key={t.topic}
                    to={`/academy?focus=${encodeURIComponent(t.topic)}`}
                    className="rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-900"
                  >
                    {String(t.topic).replace(/_/g, " ")} · {t.score_pct}%
                  </Link>
                ))}
              </div>
            </div>
          )}
          <button
            type="button"
            onClick={() => {
              setResult(null);
              setQuestions([]);
            }}
            className="mt-6 w-full rounded-xl bg-emerald-600 py-3 text-sm font-bold text-white"
          >
            Take another mock
          </button>
        </div>
      </div>
    );
  }

  if (!questions.length) {
    return (
      <div className="mx-auto max-w-xl space-y-6 px-4 py-8">
        <Link to="/academy" className="inline-flex items-center gap-1 text-sm text-slate-500">
          <ArrowLeft size={14} /> Academy
        </Link>
        <header className="rounded-3xl border border-slate-200 bg-gradient-to-br from-white to-emerald-50/40 p-6 shadow-sm">
          <p className="flex items-center gap-2 text-[11px] font-bold uppercase tracking-wider text-emerald-700">
            <Building2 size={14} /> Service company OA
          </p>
          <h1 className="mt-2 text-2xl font-black text-slate-900">Company-weighted mock</h1>
          <p className="mt-2 text-sm text-slate-600">
            Questions sampled from the service OA bank using each company&apos;s section weights
            (TCS NQT, Infosys, Wipro, Cognizant, Accenture). Answers graded on the server.
          </p>
          {bankTotal != null && (
            <p className="mt-2 text-xs font-medium text-slate-500">{bankTotal} items in problem bank</p>
          )}
        </header>

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm space-y-4">
          <label className="block text-sm font-semibold text-slate-800">
            Company
            <select
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              className="mt-1 w-full rounded-xl border border-slate-200 bg-slate-50 px-3 py-2 text-sm"
            >
              {COMPANIES.map((c) => (
                <option key={c.key} value={c.key}>
                  {c.label}
                </option>
              ))}
            </select>
          </label>
          <label className="block text-sm font-semibold text-slate-800">
            Questions ({count})
            <input
              type="range"
              min={8}
              max={30}
              value={count}
              onChange={(e) => setCount(Number(e.target.value))}
              className="mt-2 w-full"
            />
          </label>
          {error && (
            <p className="rounded-lg border border-rose-200 bg-rose-50 p-2 text-xs text-rose-700">{error}</p>
          )}
          <button
            type="button"
            disabled={loading}
            onClick={() => void start()}
            className="inline-flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-600 py-3 text-sm font-bold text-white disabled:opacity-50"
          >
            {loading ? <Loader2 className="animate-spin" size={16} /> : <Zap size={16} />}
            Start mock
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-6">
      <div className="mb-4 flex items-center justify-between gap-3 text-xs text-slate-500">
        <span className="font-semibold text-slate-700">{meta?.company_name}</span>
        <span className="inline-flex items-center gap-1">
          <Timer size={12} /> ~{meta?.duration_min} min · {answered}/{questions.length} answered
        </span>
      </div>
      <div className="mb-4 h-1.5 rounded-full bg-slate-200">
        <div
          className="h-full rounded-full bg-emerald-500 transition-all"
          style={{ width: `${((idx + 1) / questions.length) * 100}%` }}
        />
      </div>

      {q && (
        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
          <p className="text-[11px] font-bold uppercase tracking-wide text-emerald-700">
            {q.section_label || q.section} · {q.topic?.replace(/_/g, " ")}
          </p>
          <h2 className="mt-2 text-lg font-bold text-slate-900">
            {q.order}. {q.prompt}
          </h2>
          <div className="mt-4 space-y-2">
            {q.options.map((opt, oi) => {
              const selected = answers[q.id] === oi;
              return (
                <button
                  key={oi}
                  type="button"
                  onClick={() => setAnswers((prev) => ({ ...prev, [q.id]: oi }))}
                  className={`w-full rounded-xl border px-3 py-2.5 text-left text-sm transition ${
                    selected
                      ? "border-emerald-500 bg-emerald-50 font-semibold text-emerald-900"
                      : "border-slate-200 hover:border-slate-400"
                  }`}
                >
                  {opt}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {error && (
        <p className="mt-3 rounded-lg border border-rose-200 bg-rose-50 p-2 text-xs text-rose-700">{error}</p>
      )}

      <div className="mt-6 flex items-center justify-between gap-3">
        <button
          type="button"
          disabled={idx === 0}
          onClick={() => setIdx((i) => Math.max(0, i - 1))}
          className="rounded-xl border border-slate-200 px-4 py-2 text-sm disabled:opacity-40"
        >
          Back
        </button>
        {idx < questions.length - 1 ? (
          <button
            type="button"
            onClick={() => setIdx((i) => i + 1)}
            className="rounded-xl bg-slate-900 px-4 py-2 text-sm font-semibold text-white"
          >
            Next
          </button>
        ) : (
          <button
            type="button"
            disabled={loading}
            onClick={() => void submit()}
            className="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-4 py-2 text-sm font-bold text-white disabled:opacity-50"
          >
            {loading ? <Loader2 className="animate-spin" size={14} /> : <Target size={14} />}
            Submit mock
          </button>
        )}
      </div>
      <p className="mt-4 text-center text-[11px] text-slate-500">
        Server-graded. Hints are not available in timed mocks — use Academy scrims to learn.
      </p>
    </div>
  );
}
