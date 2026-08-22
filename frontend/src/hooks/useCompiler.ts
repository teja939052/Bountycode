import { useState, useEffect, useRef, useCallback } from "react";

export interface CompilerResult {
  success: boolean;
  stdout?: string;
  stderr?: string;
  compile_error?: string;
  exit_code?: number;
  execution_time?: number;
  memory_usage?: number;
  summary?: string;
  all_passed?: boolean;
  passed_count?: number;
  total_count?: number;
  results?: Array<{
    passed: boolean;
    input?: string;
    expected?: string;
    actual?: string;
    error?: string;
    execution_time?: number;
    is_hidden?: boolean;
  }>;
  [key: string]: unknown;
}

export interface CompilerError {
  message: string;
  type: "compile" | "runtime" | "tle" | "mle" | "network" | "validation";
  isCompileError?: boolean;
  isRuntimeError?: boolean;
  isTimeout?: boolean;
  stderr?: string;
  hint?: string;
  line?: number | null;
  explanation?: string | null;
}

export interface SubmissionResult {
  solved: boolean;
  summary: string;
  score: number;
  xp_gained: number;
  results?: Array<{
    passed: boolean;
    execution_time?: number;
  }>;
  [key: string]: unknown;
}

export interface TraceData {
  success: boolean;
  source?: string;
  trace?: any[];
  [key: string]: unknown;
}

export interface EditorSettings {
  fontSize: number;
  theme: string;
  tabSize: number;
}

const LANGUAGES = [
  { id: "python", name: "Python", version: "3.10.0", icon: "🐍" },
  { id: "javascript", name: "JavaScript", version: "18.15.0", icon: "🟨" },
  { id: "typescript", name: "TypeScript", version: "5.0.3", icon: "🔷" },
  { id: "java", name: "Java", version: "15.0.2", icon: "☕" },
  { id: "cpp", name: "C++", version: "10.2.0", icon: "⚡" },
  { id: "c", name: "C", version: "10.2.0", icon: "🔧" },
  { id: "go", name: "Go", version: "1.16.2", icon: "🐹" },
  { id: "rust", name: "Rust", version: "1.68.2", icon: "🦀" },
];

const DEFAULT_CODE: Record<string, string> = {
  python: `def solution():\n    # Your code here\n    pass\n\nif __name__ == "__main__":\n    print(solution())`,
  javascript: `function solution() {\n    // Your code here\n}\n\nconsole.log(solution());`,
  java: `public class Main {\n    public static void main(String[] args) {\n        // Your code here\n    }\n}`,
  cpp: `#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}`,
  c: `#include <stdio.h>\n\nint main() {\n    // Your code here\n    return 0;\n}`,
  go: `package main\n\nimport "fmt"\n\nfunc main() {\n    // Your code here\n}`,
  rust: `fn main() {\n    // Your code here\n}`,
  typescript: `function solution(): any {\n    // Your code here\n}\n\nconsole.log(solution());`,
};

const DEFAULT_CODE_PROBLEM: Record<string, string> = {
  python: `import sys\n\n# Read all input from stdin\ndata = sys.stdin.read().strip().splitlines()\n# TODO: parse the input and print the answer\nprint("")`,
};

const CodeCache = {
  getKey: (problemId: string | undefined, language: string) =>
    `pp_code_${problemId || "default"}_${language}`,
  save: (problemId: string | undefined, language: string, code: string) => {
    try {
      localStorage.setItem(
        CodeCache.getKey(problemId, language),
        JSON.stringify({ code, ts: Date.now() })
      );
    } catch {}
  },
  load: (problemId: string | undefined, language: string): string | null => {
    try {
      const d = JSON.parse(
        localStorage.getItem(CodeCache.getKey(problemId, language)) || "null"
      );
      if (d && Date.now() - d.ts < 7 * 86400000) return d.code;
    } catch {}
    return null;
  },
  remove: (problemId: string | undefined, language: string) => {
    try {
      localStorage.removeItem(CodeCache.getKey(problemId, language));
    } catch {}
  },
};

function getDefaultCode(language: string, isProblemMode: boolean): string {
  if (isProblemMode && DEFAULT_CODE_PROBLEM[language]) return DEFAULT_CODE_PROBLEM[language];
  return DEFAULT_CODE[language] || "";
}

function formatTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return `${h}h ${m}m ${s}s`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

function formatMemory(bytes: number | null): string {
  if (!bytes) return "N/A";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function parseErrorLine(message: string): number | null {
  if (!message) return null;
  const patterns = [
    /line (\d+)/i,
    /Line (\d+)/,
    /at line (\d+)/i,
    /:(\d+):\d+/,
    /\((\d+),\d+\)/,
  ];
  for (const p of patterns) {
    const m = message.match(p);
    if (m) return parseInt(m[1]);
  }
  return null;
}

function detectErrorType(
  stderr: string | undefined,
  compileError: string | undefined,
  exitCode: number | undefined
): CompilerError["type"] {
  if (compileError) return "compile";
  if (stderr?.includes("Time Limit") || stderr?.includes("timeout")) return "tle";
  if (stderr?.includes("Memory Limit") || stderr?.includes("memory")) return "mle";
  if (exitCode !== 0 && !stderr) return "runtime";
  return "runtime";
}

function normalizeTopics(problem: any): string[] {
  if (!problem) return [];
  const topics = Array.isArray(problem.topics) ? problem.topics : [];
  const fallback = problem.topic ? [problem.topic] : [];
  return [...topics, ...fallback]
    .map((topic: any) => String(topic).trim())
    .filter(Boolean);
}

function getStarterProblemType(topics: string[]): string {
  const topicSet = new Set(topics.map((t) => t.toLowerCase()));
  if ([...topicSet].some((t) => t.includes("linked list") || t.includes("linked_list")))
    return "linked_list";
  if ([...topicSet].some((t) => t.includes("tree") || t.includes("bst"))) return "binary_tree";
  if ([...topicSet].some((t) => t.includes("graph") || t === "bfs" || t === "dfs")) return "graph";
  if ([...topicSet].some((t) => t.includes("dynamic programming") || t === "dp")) return "dp";
  return "class";
}

export function useCompiler(problemId?: string, problem?: any) {
  const isProblemMode = Boolean(problemId);

  const [language, setLanguage] = useState(LANGUAGES[0].id);
  const [code, setCode] = useState(() => {
    const cached = CodeCache.load(problemId, LANGUAGES[0].id);
    if (cached) return cached;
    return getDefaultCode(LANGUAGES[0].id, isProblemMode);
  });
  const [stdin, setStdin] = useState("");
  const [testCases, setTestCases] = useState<Array<{ id: number; input: string; expected: string; isHidden: boolean }>>([
    { id: 1, input: "", expected: "", isHidden: false },
  ]);
  const [results, setResults] = useState<CompilerResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<CompilerError | null>(null);
  const [executionTime, setExecutionTime] = useState<number | null>(null);
  const [memoryUsage, setMemoryUsage] = useState<number | null>(null);
  const [submissionResult, setSubmissionResult] = useState<SubmissionResult | null>(null);
  const [savedIndicator, setSavedIndicator] = useState(false);
  const [boilerplateLoading, setBoilerplateLoading] = useState(false);
  const [statusNote, setStatusNote] = useState("");
  const [creativeLoading, setCreativeLoading] = useState(false);
  const [creativeMode, setCreativeMode] = useState("mentor");
  const [creativeResult, setCreativeResult] = useState<any>(null);
  const [creativeError, setCreativeError] = useState("");
  const [activeTestCase, setActiveTestCase] = useState(0);
  const [showExpected, setShowExpected] = useState(true);
  const [viewMode, setViewMode] = useState<"editor" | "visualizer">("editor");
  const [traceData, setTraceData] = useState<TraceData | null>(null);
  const [traceLoading, setTraceLoading] = useState(false);
  const [fontSize, setFontSize] = useState(14);
  const [editorTheme, setEditorTheme] = useState("vs");
  const [tabSize, setTabSize] = useState(2);
  const [showSettings, setShowSettings] = useState(false);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [activeTab, setActiveTab] = useState<"testcases" | "console" | "creative" | "submissions">("testcases");
  const [splitRatio, setSplitRatio] = useState(50);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showLeftPanel, setShowLeftPanel] = useState(true);
  const [timerRunning, setTimerRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const [submissions, setSubmissions] = useState<any[]>([]);
  const [runHistory, setRunHistory] = useState<any[]>([]);
  const editorRef = useRef<any>(null);
  const splitRef = useRef<HTMLDivElement>(null);
  const isDragging = useRef(false);

  const problemTopics = normalizeTopics(problem);
  const starterProblemType = getStarterProblemType(problemTopics);

  useEffect(() => {
    if (timerRunning) {
      timerRef.current = setInterval(() => setElapsed((e) => e + 1), 1000);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [timerRunning]);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const handleCodeChange = useCallback(
    (value: string | undefined) => {
      setCode(value || "");
      if (!timerRunning && isProblemMode) setTimerRunning(true);
    },
    [timerRunning, isProblemMode]
  );

  const autoSaveCode = useCallback(() => {
    if (code && code !== DEFAULT_CODE[language]) {
      CodeCache.save(problemId, language, code);
      setSavedIndicator(true);
      setTimeout(() => setSavedIndicator(false), 2000);
    }
  }, [code, language, problemId]);

  useEffect(() => {
    const t = setTimeout(autoSaveCode, 3000);
    return () => clearTimeout(t);
  }, [code, autoSaveCode]);

  useEffect(() => {
    if (!LANGUAGES.find((l) => l.id === language)) setLanguage(LANGUAGES[0].id);
    const cached = CodeCache.load(problemId, language);
    setCode(cached || getDefaultCode(language, isProblemMode) || getDefaultCode(LANGUAGES[0].id, isProblemMode));
    setResults(null);
    setError(null);
    setSubmissionResult(null);
    setTraceData(null);
    setViewMode("editor");
    setStatusNote("");
  }, [language]);

  useEffect(() => {
    if (problemId && problem) {
      const visible = problem.visible_test_cases || [];
      setTestCases(
        visible.length > 0
          ? visible.map((tc: any, i: number) => ({
              id: i + 1,
              input: tc.input || tc.stdin || "",
              expected: tc.expected || tc.expected_output || "",
              isHidden: false,
            }))
          : [{ id: 1, input: "", expected: "", isHidden: false }]
      );
      setResults(null);
      setSubmissionResult(null);
      if (problemTopics.length > 0) {
        setStatusNote(`Starter focus: ${problemTopics.slice(0, 3).join(", ")}`);
      }
      setCreativeResult(null);
      setCreativeError("");
    }
  }, [problemId, problem]);

  useEffect(() => {
    if (problemId) {
      import("../services/api").then(({ default: api }) => {
        api.submissions
          .getProblemSubmissions(problemId, 10)
          .then(setSubmissions)
          .catch(() => {});
      });
    }
  }, [problemId]);

  const handleSplitDrag = useCallback(
    (e: MouseEvent) => {
      if (!splitRef.current || !isDragging.current) return;
      const rect = splitRef.current.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const pct = Math.min(75, Math.max(25, (x / rect.width) * 100));
      setSplitRatio(pct);
    },
    []
  );

  useEffect(() => {
    const up = () => {
      isDragging.current = false;
    };
    window.addEventListener("mousemove", handleSplitDrag);
    window.addEventListener("mouseup", up);
    return () => {
      window.removeEventListener("mousemove", handleSplitDrag);
      window.removeEventListener("mouseup", up);
    };
  }, [handleSplitDrag]);

  const addTestCase = () =>
    setTestCases([...testCases, { id: Date.now(), input: "", expected: "", isHidden: false }]);

  const removeTestCase = (id: number) => {
    if (testCases.length <= 1) return;
    setTestCases(testCases.filter((tc) => tc.id !== id));
    if (activeTestCase >= testCases.length - 1)
      setActiveTestCase(Math.max(0, testCases.length - 2));
  };

  const updateTestCase = (id: number, field: string, value: string) =>
    setTestCases(testCases.map((tc) => (tc.id === id ? { ...tc, [field]: value } : tc)));

  const copyCode = () => {
    navigator.clipboard?.writeText(code);
    setSavedIndicator(true);
    setTimeout(() => setSavedIndicator(false), 1500);
  };

  const downloadCode = () => {
    const ext =
      language === "cpp" ? "cpp" : language === "javascript" ? "js" : language === "typescript" ? "ts" : language;
    const blob = new Blob([code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `solution.${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const resetCode = () => {
    CodeCache.remove(problemId, language);
    setCode(getDefaultCode(language, isProblemMode));
    setStatusNote("Reset to template");
  };

  const currentLang = LANGUAGES.find((l) => l.id === language) || LANGUAGES[0];

  return {
    language,
    setLanguage,
    code,
    setCode: handleCodeChange,
    setCodeDirect: setCode,
    stdin,
    setStdin,
    testCases,
    setTestCases,
    results,
    setResults,
    loading,
    setLoading,
    error,
    setError,
    executionTime,
    setExecutionTime,
    memoryUsage,
    setMemoryUsage,
    submissionResult,
    setSubmissionResult,
    savedIndicator,
    boilerplateLoading,
    setBoilerplateLoading,
    statusNote,
    setStatusNote,
    creativeLoading,
    setCreativeLoading,
    creativeMode,
    setCreativeMode,
    creativeResult,
    setCreativeResult,
    creativeError,
    setCreativeError,
    activeTestCase,
    setActiveTestCase,
    showExpected,
    setShowExpected,
    viewMode,
    setViewMode,
    traceData,
    setTraceData,
    traceLoading,
    setTraceLoading,
    fontSize,
    setFontSize,
    editorTheme,
    setEditorTheme,
    tabSize,
    setTabSize,
    showSettings,
    setShowSettings,
    showShortcuts,
    setShowShortcuts,
    activeTab,
    setActiveTab,
    splitRatio,
    setSplitRatio,
    isFullscreen,
    setIsFullscreen,
    showLeftPanel,
    setShowLeftPanel,
    timerRunning,
    setTimerRunning,
    elapsed,
    submissions,
    setSubmissions,
    runHistory,
    setRunHistory,
    editorRef,
    splitRef,
    isDragging,
    isProblemMode,
    problemTopics,
    starterProblemType,
    currentLang,
    langs: LANGUAGES,
    addTestCase,
    removeTestCase,
    updateTestCase,
    copyCode,
    downloadCode,
    resetCode,
    autoSaveCode,
    handleCodeChange,
    handleSplitDrag,
    formatTime,
    formatMemory,
    parseErrorLine,
    detectErrorType,
    getDefaultCode,
    CodeCache,
    passedCount: results?.results?.filter((r) => r.passed).length || 0,
    totalCount: results?.results?.length || 0,
  };
}
