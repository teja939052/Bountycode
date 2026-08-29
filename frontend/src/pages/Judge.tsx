import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import useAuthStore from "../store/authStore";
import {
  fetchProblem,
  fetchProblemVisible,
  fetchLockState,
  checkLock,
  runFullProblem,
  staticAnalysis,
  generateHint,
  localRuntime,
  type ProblemData,
  type SubmissionResult,
  type LockState,
  type StaticAnalysisResult,
} from "../services/judgeService";

const LANGUAGES = ["python", "javascript", "cpp", "java"] as const;
type Language = (typeof LANGUAGES)[number];

export default function Judge() {
  const { problemId } = useParams<{ problemId: string }>();
  const user = useAuthStore((s) => s.user);
  const loading = useAuthStore((s) => s.loading);

  const [problem, setProblem] = useState<ProblemData | null>(null);
  const [lockState, setLockState] = useState<LockState | null>(null);
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState<Language>("python");
  const [stdin, setStdin] = useState("");
  const [result, setResult] = useState<SubmissionResult | null>(null);
  const [analysis, setAnalysis] = useState<StaticAnalysisResult | null>(null);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const currentLock = lockState?.current_lock ?? null;

  useEffect(() => {
    if (!problemId) return;
    let cancelled = false;

    Promise.all([fetchProblemVisible(problemId), fetchLockState(problemId)])
      .then(([p, ls]) => {
        if (cancelled) return;
        setProblem(p);
        setLockState(ls);
        setCode("");
        setResult(null);
      })
      .catch((err) => {
        if (!cancelled) setError((err as Error).message || "Failed to load problem");
      });

    return () => {
      cancelled = true;
    };
  }, [problemId]);

  if (loading) return <div className="p-6 text-slate-500">Loading session…</div>;

  if (!user) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-2">Lock &amp; Key Problems</h1>
        <p className="text-slate-600">Please sign in to attempt problems.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-2">Problem</h1>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  if (!problem) {
    return <div className="p-6 text-slate-500">Loading problem…</div>;
  }

  const handleCheckLock = async () => {
    if (!code.trim() || !problemId || busy) return;
    setBusy("check");
    setResult(null);
    try {
      const res = await checkLock(problemId, { code, language, stdin });
      setResult(res);
      const ls = await fetchLockState(problemId);
      setLockState(ls);
      if (ls.current_lock) {
        setCode("");
      }
    } catch (err) {
      setResult({
        success: false,
        mode: "error",
        message: (err as Error).message || "Failed to check lock",
      });
    } finally {
      setBusy(null);
    }
  };

  const handleRun = async () => {
    if (!code.trim() || !problemId || busy) return;
    setBusy("run");
    setResult(null);

    // Prefer local browser runtime when available; fall back to server.
    if (language === "python" || language === "javascript") {
      const execRes =
        language === "python"
          ? await localRuntime.executePython(code, stdin)
          : await localRuntime.executeJavaScript(code, stdin);
      if (execRes.success) {
        setResult({
          success: true,
          mode: "runtime",
          message: execRes.stdout || "Ran without output",
        });
        setBusy(null);
        return;
      }
    }

    try {
      const res = await runFullProblem(problemId, { code, language, stdin });
      setResult(res);
    } catch (err) {
      setResult({
        success: false,
        mode: "error",
        message: (err as Error).message || "Failed to run code",
      });
    } finally {
      setBusy(null);
    }
  };

  const handleAnalyze = async () => {
    if (!code.trim() || !problemId || busy) return;
    setBusy("analyze");
    try {
      const res = await staticAnalysis(problemId, { code, language });
      setAnalysis(res.analysis);
    } catch (err) {
      setError((err as Error).message || "Analysis failed");
    } finally {
      setBusy(null);
    }
  };

  const handleHint = () => {
    if (!currentLock) return;
    const { hintText } = generateHint(currentLock, code);
    setResult({
      success: false,
      mode: "hint",
      message: hintText,
      hint_text: hintText,
    });
  };

  const lockIndex = lockState
    ? lockState.unlocked_locks.length
    : 0;
  const lockCount = problem.locks.length;

  return (
    <div className="max-w-5xl mx-auto p-6">
      <div className="flex flex-wrap items-start justify-between gap-4 mb-4">
        <div>
          <h1 className="text-3xl font-bold">{problem.title}</h1>
          <p className="text-slate-500 mt-1">
            {problem.difficulty} · {problem.mode} · ~{problem.estimated_xp} XP
          </p>
          <p className="text-xs text-slate-400 mt-1">
            Goal: {problem.learning_goal} · Time {problem.time_complexity} / Space{" "}
            {problem.space_complexity}
          </p>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-4 w-64 shadow-sm">
          <h2 className="text-sm font-bold text-slate-700 mb-2">
            🔐 Progress {lockIndex}/{lockCount}
          </h2>
          <div className="flex gap-1 mb-2">
            {problem.locks.map((l, i) => (
              <div
                key={l.id}
                className={`h-2 flex-1 rounded-full ${
                  i < lockIndex
                    ? "bg-emerald-500"
                    : i === lockIndex
                      ? "bg-amber-400"
                      : "bg-slate-200"
                }`}
                title={l.label}
              />
            ))}
          </div>
          <p className="text-xs text-slate-500">
            {currentLock
              ? `Current: ${currentLock.label}`
              : "All locks unlocked — problem mastered!"}
          </p>
        </div>
      </div>

      <p className="text-slate-700 whitespace-pre-wrap mb-6">{problem.description}</p>

      {/* Lock / hint card */}
      {result && (
        <div
          className={`border rounded-xl p-4 mb-4 ${
            result.success ? "bg-emerald-50 border-emerald-200" : "bg-slate-50 border-slate-200"
          }`}
        >
          <p className="font-medium">{result.message}</p>
          {typeof result.score === "number" && (
            <p className="text-sm text-slate-600 mt-1">Score: {result.score}%</p>
          )}
          {typeof result.passed_tests === "number" && typeof result.total_tests === "number" && (
            <p className="text-sm text-slate-600 mt-1">
              Tests: {result.passed_tests}/{result.total_tests}
            </p>
          )}
          {typeof result.xp_awarded === "number" && result.xp_awarded > 0 && (
            <p className="text-sm text-emerald-600 mt-1">+{result.xp_awarded} XP</p>
          )}
          {result.lock_unlocked && (
            <p className="text-sm text-emerald-600 mt-1">
              ✓ Unlocked: {result.lock_unlocked}
            </p>
          )}
        </div>
      )}

      {/* Code editor area for coding modes */}
      {(problem.mode === "full_coding" ||
        problem.mode === "fix_the_bug" ||
        problem.mode === "oa") && (
        <div className="space-y-3 mb-4">
          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-600">Language</label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as Language)}
              className="px-2 py-1 border border-slate-300 rounded-md text-sm"
            >
              {LANGUAGES.map((l) => (
                <option key={l} value={l}>
                  {l}
                </option>
              ))}
            </select>
          </div>
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={10}
            spellCheck={false}
            placeholder="Write your solution here…"
            className="w-full font-mono text-sm p-3 border border-slate-300 rounded-xl bg-slate-950 text-slate-100 focus:outline-none focus:ring-2 focus:ring-emerald-400"
          />
          <input
            value={stdin}
            onChange={(e) => setStdin(e.target.value)}
            placeholder="Optional stdin"
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
          />
          <div className="flex flex-wrap gap-2">
            <button
              onClick={handleCheckLock}
              disabled={!code.trim() || !!busy}
              className="px-4 py-2 rounded-lg bg-emerald-600 text-white font-medium disabled:opacity-50 hover:bg-emerald-700"
            >
              {busy === "check" ? "Checking…" : "Check Lock"}
            </button>
            <button
              onClick={handleRun}
              disabled={!code.trim() || !!busy}
              className="px-4 py-2 rounded-lg bg-blue-600 text-white font-medium disabled:opacity-50 hover:bg-blue-700"
            >
              {busy === "run" ? "Running…" : "Run"}
            </button>
            <button
              onClick={handleAnalyze}
              disabled={!code.trim() || !!busy}
              className="px-4 py-2 rounded-lg bg-slate-600 text-white font-medium disabled:opacity-50 hover:bg-slate-700"
            >
              {busy === "analyze" ? "Analyzing…" : "Analyze"}
            </button>
            <button
              onClick={handleHint}
              className="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 font-medium hover:bg-slate-100"
            >
              💡 Hint
            </button>
          </div>
        </div>
      )}

      {/* Non-coding modes: allow submitting a text answer to the lock */}
      {(problem.mode === "predict" ||
        problem.mode === "arrange" ||
        problem.mode === "fill_the_lock") && (
        <div className="space-y-3 mb-4">
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={3}
            placeholder={
              currentLock ? `Answer for: ${currentLock.label}…` : "Answer…"
            }
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"
          />
          <button
            onClick={handleCheckLock}
            disabled={!code.trim() || !!busy}
            className="px-4 py-2 rounded-lg bg-emerald-600 text-white font-medium disabled:opacity-50 hover:bg-emerald-700"
          >
            {busy === "check" ? "Checking…" : "Submit Answer"}
          </button>
        </div>
      )}

      {/* Static analysis output */}
      {analysis && (
        <div className="border border-slate-200 rounded-xl p-4 mb-4 bg-white">
          <h3 className="font-bold text-slate-700 mb-2">Static Analysis</h3>
          <p className="text-sm text-slate-600">
            Syntax {analysis.ast_valid ? "valid ✓" : "invalid ✗"}
          </p>
          {analysis.complexity_hint && (
            <p className="text-sm text-slate-600">Hint: {analysis.complexity_hint}</p>
          )}
          {analysis.errors.length > 0 && (
            <ul className="text-sm text-red-600 mt-1 list-disc list-inside">
              {analysis.errors.map((e, i) => (
                <li key={i}>{e}</li>
              ))}
            </ul>
          )}
          {analysis.functions.length > 0 && (
            <p className="text-sm text-slate-600 mt-1">
              Functions: {analysis.functions.map((f) => (typeof f === "string" ? f : f.name)).join(", ")}
            </p>
          )}
        </div>
      )}

      {analysis === null && (
        <button
          onClick={handleAnalyze}
          disabled={!code.trim() || !!busy}
          className="px-3 py-1.5 rounded-md border border-slate-300 text-slate-700 text-sm hover:bg-slate-100"
        >
          Run static analysis
        </button>
      )}
    </div>
  );
}
