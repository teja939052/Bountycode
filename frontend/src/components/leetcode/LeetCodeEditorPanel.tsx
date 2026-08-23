import { useCallback, useEffect, useMemo, useState } from "react";
import Editor from "@monaco-editor/react";
import { motion } from "framer-motion";
import { CheckCircle2, Copy, Play, RotateCcw, Send, Terminal, Timer, XCircle } from "lucide-react";
import api from "../../services/api";
import useReducedMotion from "../../hooks/useReducedMotion";

const LANGUAGES = [
  { id: "python", label: "Python" },
  { id: "cpp", label: "C++" },
  { id: "java", label: "Java" },
  { id: "javascript", label: "JavaScript" },
  { id: "typescript", label: "TypeScript" },
  { id: "go", label: "Go" },
  { id: "rust", label: "Rust" },
];

const DEFAULT_CODE: Record<string, string> = {
  python: `def solution(nums, target):\n    # Write your solution here\n    pass`,
  cpp: `class Solution {\npublic:\n    // Write your solution here\n};`,
  java: `class Solution {\n    // Write your solution here\n}`,
  javascript: `function solution(nums, target) {\n  // Write your solution here\n}`,
  typescript: `function solution(nums: number[], target: number): any {\n  // Write your solution here\n}`,
  go: `package main\n\nfunc main() {\n  // Write your solution here\n}`,
  rust: `fn main() {\n    // Write your solution here\n}`,
};

function cacheKey(problemId: string, language: string) {
  return `pp_solve_code_${problemId}_${language}`;
}

function loadCachedCode(problemId: string, language: string) {
  try {
    const raw = localStorage.getItem(cacheKey(problemId, language));
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (parsed?.code && Date.now() - parsed.ts < 7 * 86400000) return parsed.code;
  } catch {}
  return null;
}

function saveCachedCode(problemId: string, language: string, code: string) {
  try {
    localStorage.setItem(cacheKey(problemId, language), JSON.stringify({ code, ts: Date.now() }));
  } catch {}
}

function getDefaultLanguage(problem: any) {
  const text = JSON.stringify(problem || {}).toLowerCase();
  if (text.includes("javascript") || text.includes("js")) return "javascript";
  return "python";
}

function formatMemory(bytes: number | null | undefined) {
  if (!bytes) return "0 MB";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function summarizeVerdict(result: any) {
  if (!result) return { label: "Ready", tone: "text-brand-muted", detail: "Run samples or submit your solution" };
  if (result.solved || result.all_passed) {
    return { label: "Accepted", tone: "text-emerald-600", detail: result.summary || "All checks passed" };
  }
  if (result.results?.some((r: any) => !r.passed)) {
    return { label: "Wrong Answer", tone: "text-brand-coral", detail: result.summary || "Some tests failed" };
  }
  if (result.stderr || result.error) {
    return { label: "Error", tone: "text-brand-coral", detail: result.error || result.stderr || "Execution failed" };
  }
  return { label: "Done", tone: "text-brand-secondary", detail: result.summary || "" };
}

type Props = {
  problemId: string;
  problem?: any;
  className?: string;
  onSolved?: (result: any) => void;
};

export default function LeetCodeEditorPanel({ problemId, problem, className = "", onSolved }: Props) {
  const reduced = useReducedMotion();
  const [language, setLanguage] = useState(() => getDefaultLanguage(problem));
  const [code, setCode] = useState(() => loadCachedCode(problemId, getDefaultLanguage(problem)) || DEFAULT_CODE[getDefaultLanguage(problem)]);
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>("");
  const [mode, setMode] = useState<"sample" | "result" | "submissions">("sample");

  const samples = useMemo(() => {
    const visible = Array.isArray(problem?.visible_test_cases) ? problem.visible_test_cases : [];
    if (visible.length) return visible.slice(0, 4).map((tc: any, index: number) => ({
      id: index + 1,
      input: tc.input || tc.stdin || "",
      expected: tc.expected || tc.expected_output || "",
    }));
    const examples = Array.isArray(problem?.examples) ? problem.examples : [];
    return examples.slice(0, 3).map((ex: any, index: number) => ({
      id: index + 1,
      input: ex.input || ex.input_text || "",
      expected: ex.output || ex.output_text || "",
    }));
  }, [problem]);

  useEffect(() => {
    const nextLanguage = getDefaultLanguage(problem);
    setLanguage(nextLanguage);
    const cached = loadCachedCode(problemId, nextLanguage);
    setCode(cached || DEFAULT_CODE[nextLanguage] || DEFAULT_CODE.python);
    setResult(null);
    setError("");
    setMode("sample");
  }, [problemId, problem]);

  useEffect(() => {
    saveCachedCode(problemId, language, code);
  }, [problemId, language, code]);

  const handleReset = () => {
    const fallback = DEFAULT_CODE[language] || DEFAULT_CODE.python;
    setCode(loadCachedCode(problemId, language) || fallback);
    setResult(null);
    setError("");
  };

  const handleCopy = async () => {
    await navigator.clipboard?.writeText(code);
  };

  const runSamples = useCallback(async () => {
    setRunning(true);
    setError("");
    try {
      if (samples.length > 0) {
        const data = await api.executeCompilerTestCases({
          code,
          language,
          test_cases: samples.map((s) => ({ input: s.input, expected: s.expected })),
          timeout: 10,
        });
        setResult({ kind: "samples", ...data });
        setMode("result");
      } else {
        const data = await api.executeCompilerCode({ code, language, stdin: "", timeout: 10 });
        setResult({ kind: "run", ...data });
        setMode("result");
      }
    } catch (err: any) {
      setError(err?.message || "Failed to run code");
      setMode("result");
    } finally {
      setRunning(false);
    }
  }, [code, language, samples]);

  const submitSolution = useCallback(async () => {
    setSubmitting(true);
    setError("");
    try {
      const data = await api.questions.submitCode(problemId, { code, language });
      setResult({ kind: "submit", ...data });
      setMode("result");
      if (data?.solved) onSolved?.(data);
    } catch (err: any) {
      setError(err?.message || "Failed to submit solution");
      setMode("result");
    } finally {
      setSubmitting(false);
    }
  }, [code, language, problemId, onSolved]);

  const verdict = summarizeVerdict(result);
  const completedCount = result?.results?.filter((r: any) => r.passed).length || 0;
  const totalCount = result?.results?.length || 0;

  return (
    <motion.section
      initial={reduced ? {} : { opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex h-full min-h-0 flex-col overflow-hidden rounded-3xl border border-brand-primary/10 bg-white shadow-soft-lg ${className}`}
    >
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-brand-primary/10 bg-gradient-to-r from-white to-brand-gold-pale px-4 py-3">
        <div className="min-w-0">
          <div className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.24em] text-brand-muted">
            <Terminal size={11} />
            Code
          </div>
          <div className={`mt-1 text-sm font-semibold ${verdict.tone}`}>{verdict.label}</div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="rounded-xl border border-brand-primary/15 bg-white px-3 py-2 text-xs text-text-primary outline-none"
          >
            {LANGUAGES.map((lang) => (
              <option key={lang.id} value={lang.id}>{lang.label}</option>
            ))}
          </select>
          <button
            onClick={runSamples}
            disabled={running}
            className="inline-flex items-center gap-1.5 rounded-xl bg-brand-secondary px-3 py-2 text-xs font-semibold text-text-primary transition-colors hover:bg-nature-moss disabled:opacity-50"
          >
            <Play size={12} />
            Run
          </button>
          <button
            onClick={submitSolution}
            disabled={submitting}
            className="inline-flex items-center gap-1.5 rounded-xl bg-brand-primary px-3 py-2 text-xs font-semibold text-text-primary transition-colors hover:opacity-90 disabled:opacity-50"
          >
            <Send size={12} />
            Submit
          </button>
          <button
            onClick={handleReset}
            className="inline-flex items-center gap-1.5 rounded-xl border border-brand-primary/15 bg-white px-3 py-2 text-xs font-semibold text-brand-muted transition-colors hover:text-text-primary"
          >
            <RotateCcw size={12} />
            Reset
          </button>
          <button
            onClick={handleCopy}
            className="inline-flex items-center gap-1.5 rounded-xl border border-brand-primary/15 bg-white px-3 py-2 text-xs font-semibold text-brand-muted transition-colors hover:text-text-primary"
          >
            <Copy size={12} />
            Copy
          </button>
        </div>
      </div>

      <div className="flex min-h-0 flex-1 flex-col">
        <div className="min-h-[320px] flex-1 border-b border-brand-primary/10">
          <Editor
            height="100%"
            language={language === "cpp" ? "cpp" : language === "typescript" ? "typescript" : language}
            theme="vs-light"
            value={code}
            onChange={(value) => setCode(value || "")}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineNumbers: "on",
              tabSize: 2,
              wordWrap: "on",
              automaticLayout: true,
              scrollBeyondLastLine: false,
              padding: { top: 14 },
              bracketPairColorization: { enabled: true },
            }}
          />
        </div>

        <div className="border-t border-brand-primary/10 bg-brand-bg px-4 py-3">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setMode("sample")}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition-colors ${mode === "sample" ? "bg-brand-primary text-text-primary" : "bg-white text-brand-muted"}`}
            >
              Samples
            </button>
            <button
              onClick={() => setMode("result")}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition-colors ${mode === "result" ? "bg-brand-primary text-text-primary" : "bg-white text-brand-muted"}`}
            >
              Result
            </button>
            <button
              onClick={() => setMode("submissions")}
              className={`rounded-full px-3 py-1.5 text-xs font-semibold transition-colors ${mode === "submissions" ? "bg-brand-primary text-text-primary" : "bg-white text-brand-muted"}`}
            >
              Submissions
            </button>
            <div className="ml-auto flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.22em] text-brand-muted">
              <Timer size={11} />
              LeetCode mode
            </div>
          </div>
        </div>

        <div className="min-h-0 flex-1 overflow-y-auto bg-white px-4 py-4">
          {mode === "sample" && (
            <div className="space-y-3">
              {samples.length > 0 ? samples.map((sample, index) => (
                <div key={sample.id} className="rounded-2xl border border-brand-primary/10 bg-brand-bg p-4">
                  <div className="mb-2 text-[10px] font-mono uppercase tracking-[0.24em] text-brand-muted">Example {index + 1}</div>
                  <div className="grid gap-3 md:grid-cols-2">
                    <div>
                      <div className="mb-1 text-xs font-semibold text-brand-muted">Input</div>
                      <pre className="whitespace-pre-wrap rounded-xl bg-white p-3 font-mono text-xs text-text-primary">{sample.input || "(empty)"}</pre>
                    </div>
                    <div>
                      <div className="mb-1 text-xs font-semibold text-brand-muted">Expected</div>
                      <pre className="whitespace-pre-wrap rounded-xl bg-white p-3 font-mono text-xs text-text-primary">{sample.expected || "(empty)"}</pre>
                    </div>
                  </div>
                </div>
              )) : (
                <div className="rounded-2xl border border-dashed border-brand-primary/20 bg-brand-bg p-5 text-sm text-brand-muted">
                  No visible samples. Use Submit to run hidden tests.
                </div>
              )}
            </div>
          )}

          {mode === "result" && (
            <div className="space-y-3">
              {running && (
                <div className="rounded-2xl border border-brand-primary/10 bg-brand-bg p-4 text-sm text-brand-muted">
                  Running...
                </div>
              )}
              {error && (
                <div className="rounded-2xl border border-brand-coral/20 bg-brand-coral-pale p-4 text-sm text-brand-coral">
                  {error}
                </div>
              )}
              {result && !error && (
                <div className="space-y-3">
                  <div className={`rounded-2xl border p-4 ${result.solved || result.all_passed ? "border-emerald-200 bg-emerald-50" : "border-brand-gold/20 bg-brand-gold-pale"}`}>
                    <div className={`text-sm font-semibold ${result.solved || result.all_passed ? "text-emerald-700" : "text-brand-coral"}`}>
                      {result.summary || verdict.detail}
                    </div>
                    <div className="mt-2 flex flex-wrap gap-3 text-xs text-brand-muted">
                      {typeof result.score === "number" && <span>Score: {result.score}%</span>}
                      {typeof result.xp_gained === "number" && <span>XP: +{result.xp_gained}</span>}
                      {typeof result.execution_time === "number" && <span>Time: {result.execution_time.toFixed(3)}s</span>}
                      {typeof result.memory_usage === "number" && <span>Memory: {formatMemory(result.memory_usage)}</span>}
                      {totalCount > 0 && <span>{completedCount}/{totalCount} passed</span>}
                    </div>
                  </div>

                  {result.results?.length > 0 && (
                    <div className="space-y-2">
                      {result.results.map((row: any, index: number) => (
                        <div key={index} className={`flex items-center gap-3 rounded-2xl border px-4 py-3 ${row.passed ? "border-emerald-200 bg-emerald-50" : "border-brand-coral/20 bg-brand-coral-pale"}`}>
                          {row.passed ? <CheckCircle2 size={16} className="text-emerald-600" /> : <XCircle size={16} className="text-brand-coral" />}
                          <div className="min-w-0 flex-1">
                            <div className="text-sm font-medium text-text-primary">Test {index + 1}</div>
                            {!row.passed && row.actual && <div className="mt-1 text-xs text-brand-muted">Actual: {row.actual}</div>}
                          </div>
                          {typeof row.execution_time === "number" && <div className="text-xs font-mono text-brand-muted">{row.execution_time.toFixed(3)}s</div>}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {mode === "submissions" && (
            <div className="rounded-2xl border border-dashed border-brand-primary/20 bg-brand-bg p-5 text-sm text-brand-muted">
              Submission history is shown in the full compiler and the backend record keeps the solved state.
            </div>
          )}
        </div>
      </div>
    </motion.section>
  );
}
