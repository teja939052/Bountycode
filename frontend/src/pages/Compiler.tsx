import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import api from "../services/api";
import Editor from "@monaco-editor/react";
import CelebrationOverlay from "../components/CelebrationOverlay";
import AlgorithmVisualizer from "../components/AlgorithmVisualizer";
import { playSound } from "../utils/soundEffects";
import {
  Play, RotateCcw, Plus, Trash2, CheckCircle, XCircle,
  AlertTriangle, Clock, Terminal, Settings2, Send, ChevronDown,
  ChevronUp, Save, Cloud, History, X, Fullscreen, Minimize2,
  Code2, Zap, Timer, Eye, EyeOff, Copy, Download, Upload,
  Cpu, HardDrive, ChevronLeft, ChevronRight, FileCode, RefreshCw,
  Loader, Sparkles, Bookmark, Share2, Flag, MessageSquare, BookOpen,
  WandSparkles, Keyboard
} from "lucide-react";

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

const PROBLEM_LANGUAGES = [
  { id: "python", name: "Python", version: "3.10.0", icon: "🐍" },
  { id: "java", name: "Java", version: "15.0.2", icon: "☕" },
  { id: "cpp", name: "C++", version: "10.2.0", icon: "⚡" },
  { id: "javascript", name: "JavaScript", version: "18.15.0", icon: "🟨" },
  { id: "c", name: "C", version: "10.2.0", icon: "🔧" },
  { id: "go", name: "Go", version: "1.16.2", icon: "🐹" },
  { id: "rust", name: "Rust", version: "1.68.2", icon: "🦀" },
  { id: "typescript", name: "TypeScript", version: "5.0.3", icon: "🔷" },
];

const DEFAULT_CODE = {
  python: `def solution():\n    # Your code here\n    pass\n\nif __name__ == "__main__":\n    print(solution())`,
  javascript: `function solution() {\n    // Your code here\n}\n\nconsole.log(solution());`,
  java: `public class Main {\n    public static void main(String[] args) {\n        // Your code here\n    }\n}`,
  cpp: `#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}`,
  c: `#include <stdio.h>\n\nint main() {\n    // Your code here\n    return 0;\n}`,
  go: `package main\n\nimport "fmt"\n\nfunc main() {\n    // Your code here\n}`,
  rust: `fn main() {\n    // Your code here\n}`,
  typescript: `function solution(): any {\n    // Your code here\n}\n\nconsole.log(solution());`,
};

const THEMES = [
  { id: "vs-dark", name: "Dark" },
  { id: "vs", name: "Light" },
  { id: "hc-black", name: "High Contrast" },
  { id: "hc-blue", name: "High Contrast Blue" },
];

const FONT_SIZES = [12, 13, 14, 15, 16, 18, 20, 22];

const IDE_SHORTCUTS = [
  ["Ctrl + Enter", "Run code"],
  ["Ctrl + Shift + Enter", "Submit solution"],
  ["Ctrl + Alt + V", "Open visualizer"],
  ["Ctrl + Alt + T", "Jump to test cases"],
  ["Ctrl + Alt + C", "Jump to console"],
  ["Ctrl + S", "Save code"],
  ["Ctrl + L", "Reset to template"],
];

const CodeCache = {
  getKey: (problemId, language) => `pp_code_${problemId || "default"}_${language}`,
  save: (problemId, language, code) => {
    try {
      localStorage.setItem(CodeCache.getKey(problemId, language), JSON.stringify({ code, ts: Date.now() }));
    } catch {}
  },
  load: (problemId, language) => {
    try {
      const d = JSON.parse(localStorage.getItem(CodeCache.getKey(problemId, language)));
      if (d && Date.now() - d.ts < 7 * 86400000) return d.code;
    } catch {}
    return null;
  },
  remove: (problemId, language) => {
    try { localStorage.removeItem(CodeCache.getKey(problemId, language)); } catch {}
  },
};

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return `${h}h ${m}m ${s}s`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}

function formatMemory(bytes) {
  if (!bytes) return "N/A";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function parseErrorLine(message) {
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

function detectErrorType(stderr, compileError, exitCode) {
  if (compileError) return "compile";
  if (stderr?.includes("Time Limit") || stderr?.includes("timeout")) return "tle";
  if (stderr?.includes("Memory Limit") || stderr?.includes("memory")) return "mle";
  if (exitCode !== 0 && !stderr) return "runtime";
  return "runtime";
}

function normalizeTopics(problem) {
  if (!problem) return [];
  const topics = Array.isArray(problem.topics) ? problem.topics : [];
  const fallback = problem.topic ? [problem.topic] : [];
  return [...topics, ...fallback].map((topic) => String(topic).trim()).filter(Boolean);
}

function getStarterProblemType(topics: string[]) {
  const topicSet = new Set(topics.map((topic: string) => topic.toLowerCase()));
  if ([...topicSet].some((topic: string) => topic.includes("linked list") || topic.includes("linked_list"))) return "linked_list";
  if ([...topicSet].some((topic: string) => topic.includes("tree") || topic.includes("bst"))) return "binary_tree";
  if ([...topicSet].some((topic: string) => topic.includes("graph") || topic === "bfs" || topic === "dfs")) return "graph";
  if ([...topicSet].some((topic: string) => topic.includes("dynamic programming") || topic === "dp")) return "dp";
  return "class";
}

export default function Compiler({ problemId, problem }: { problemId?: string; problem?: any } = {}) {
  const isProblemMode = Boolean(problemId);
  const langs = isProblemMode ? PROBLEM_LANGUAGES : LANGUAGES;

  const [language, setLanguage] = useState(langs[0].id);
  const [code, setCode] = useState(() => CodeCache.load(problemId, langs[0].id) || DEFAULT_CODE[langs[0].id] || "");
  const [stdin, setStdin] = useState("");
  const [testCases, setTestCases] = useState([{ id: 1, input: "", expected: "", isHidden: false }]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [executionTime, setExecutionTime] = useState(null);
  const [memoryUsage, setMemoryUsage] = useState(null);
  const [submissionResult, setSubmissionResult] = useState(null);
  const [showCelebration, setShowCelebration] = useState(false);
  const [savedIndicator, setSavedIndicator] = useState(false);
  const [boilerplateLoading, setBoilerplateLoading] = useState(false);
  const [statusNote, setStatusNote] = useState("");
  const [creativeLoading, setCreativeLoading] = useState(false);
  const [creativeMode, setCreativeMode] = useState("mentor");
  const [creativeResult, setCreativeResult] = useState(null);
  const [creativeError, setCreativeError] = useState("");
  const [activeTestCase, setActiveTestCase] = useState(0);
  const [showExpected, setShowExpected] = useState(true);

  // Trace & Visualizer State
  const [viewMode, setViewMode] = useState("editor"); // "editor" | "visualizer"
  const [traceData, setTraceData] = useState(null);
  const [traceLoading, setTraceLoading] = useState(false);

  // Editor settings
  const [fontSize, setFontSize] = useState(14);
  const [editorTheme, setEditorTheme] = useState("vs");
  const [tabSize, setTabSize] = useState(2);
  const [showSettings, setShowSettings] = useState(false);
  const [showShortcuts, setShowShortcuts] = useState(false);

  // Panel management
  const [activeTab, setActiveTab] = useState("testcases");
  const [splitRatio, setSplitRatio] = useState(50);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [showLeftPanel, setShowLeftPanel] = useState(true);

  // Timer
  const [timerRunning, setTimerRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const timerRef = useRef(null);

  // Submission history
  const [submissions, setSubmissions] = useState([]);

  // Run history (for this session)
  const [runHistory, setRunHistory] = useState([]);

  const editorRef = useRef(null);
  const splitRef = useRef(null);
  const isDragging = useRef(false);
  const problemTopics = normalizeTopics(problem);
  const starterProblemType = getStarterProblemType(problemTopics);

  // Timer
  useEffect(() => {
    if (timerRunning) {
      timerRef.current = setInterval(() => setElapsed((e) => e + 1), 1000);
    }
    return () => clearInterval(timerRef.current);
  }, [timerRunning]);

  // Start timer on first keystroke
  const handleCodeChange = useCallback((value) => {
    setCode(value || "");
    if (!timerRunning && isProblemMode) setTimerRunning(true);
  }, [timerRunning, isProblemMode]);

  // Auto-save
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

  // Load cached code on language change
  useEffect(() => {
    if (!langs.find((l) => l.id === language)) setLanguage(langs[0].id);
    const cached = CodeCache.load(problemId, language);
    setCode(cached || DEFAULT_CODE[language] || DEFAULT_CODE[langs[0].id] || "");
    setResults(null);
    setError(null);
    setSubmissionResult(null);
    setTraceData(null);
    setViewMode("editor");
    setStatusNote("");
  }, [language]);

  // Load test cases from problem
  useEffect(() => {
    if (problemId && problem) {
      const visible = problem.visible_test_cases || [];
      setTestCases(
        visible.length > 0
          ? visible.map((tc, i) => ({ id: i + 1, input: tc.input || tc.stdin || "", expected: tc.expected || tc.expected_output || "", isHidden: false }))
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

  // Load submission history
  useEffect(() => {
    if (problemId) {
      api.getProblemSubmissions(problemId, 10).then(setSubmissions).catch(() => {});
    }
  }, [problemId]);

  // Resizable split handler
  const handleSplitDrag = useCallback((e) => {
    if (!splitRef.current || !isDragging.current) return;
    const rect = splitRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const pct = Math.min(75, Math.max(25, (x / rect.width) * 100));
    setSplitRatio(pct);
  }, []);

  useEffect(() => {
    const up = () => { isDragging.current = false; };
    window.addEventListener("mousemove", handleSplitDrag);
    window.addEventListener("mouseup", up);
    return () => {
      window.removeEventListener("mousemove", handleSplitDrag);
      window.removeEventListener("mouseup", up);
    };
  }, [handleSplitDrag]);

  const handleRun = async () => {
    setLoading(true);
    setError(null);
    setResults(null);
    setExecutionTime(null);
    setMemoryUsage(null);
    try {
      const data = await api.executeCompilerCode({ code, language, stdin, timeout: 10 });
      if (data.success) {
        setResults(data);
        setExecutionTime(data.execution_time);
        setMemoryUsage(data.memory_usage);
        setRunHistory(prev => [{ ...data, timestamp: Date.now() }, ...prev].slice(0, 20));
        playSound.success();
      } else {
        playSound.error();
        const errType = detectErrorType(data.stderr, data.compile_error, data.exit_code);
        setError({
          message: data.compile_error || data.stderr || data.error || "Execution failed",
          type: errType,
          isCompileError: errType === "compile",
          isRuntimeError: errType === "runtime",
          isTimeout: errType === "tle" || errType === "mle",
          stderr: data.stderr,
          hint: data.hint,
          line: parseErrorLine(data.compile_error || data.stderr),
        });
      }
    } catch (err) {
      playSound.error();
      setError({
        message: err.message,
        type: "network",
        explanation: err.error_explanation || null,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleRunTestCases = async () => {
    const valid = testCases.filter((tc) => tc.input || tc.expected);
    if (!valid.length) { setError({ message: "Add at least one test case with input or expected output", type: "validation" }); return; }
    setLoading(true);
    setError(null);
    setResults(null);
    setExecutionTime(null);
    setMemoryUsage(null);
    try {
      const data = await api.executeCompilerTestCases({ code, language, test_cases: valid, timeout: 10 });
      setResults(data);
      const totalTime = data.results?.reduce((a, r) => a + (r.execution_time || 0), 0) || 0;
      setExecutionTime(totalTime);
      if (data.all_passed) playSound.success();
      else playSound.error();
    } catch (err) {
      playSound.error();
      setError({
        message: err.message,
        type: "network",
        explanation: err.error_explanation || null,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleTraceCode = async () => {
    setTraceLoading(true);
    setError(null);
    try {
      const data = await api.traceCompilerCode({ code, language, stdin });
      if (data.success) {
        setTraceData(data);
        setViewMode("visualizer");
        setStatusNote(
          data.source === "ast_trace"
            ? "Live Python trace generated from AST instrumentation"
            : data.source === "ai_trace"
              ? "AI-generated execution trace ready"
              : "Fallback execution trace ready"
        );
        playSound.badge();
      } else {
        playSound.error();
        setError({ message: data.error || "Trace generation failed", type: "runtime" });
      }
    } catch (err) {
      playSound.error();
      setError({
        message: err.message,
        type: "network",
        explanation: err.error_explanation || null,
      });
    } finally {
      setTraceLoading(false);
    }
  };

  const handleLoadBoilerplate = async () => {
    if (!problemTopics.length) {
      setCode(DEFAULT_CODE[language] || "");
      setStatusNote("Inserted default starter template");
      return;
    }

    setBoilerplateLoading(true);
    try {
      const payload = await api.getCompilerBoilerplate(language, problemTopics);
      const boilerplate = payload?.boilerplate || DEFAULT_CODE[language] || "";
      setCode(boilerplate);
      CodeCache.save(problemId, language, boilerplate);
      setSavedIndicator(true);
      setTimeout(() => setSavedIndicator(false), 1500);
      setStatusNote(`Loaded ${starterProblemType.replace("_", " ")} starter for ${problemTopics.slice(0, 3).join(", ")}`);
      playSound.success();
    } catch (err) {
      setError({
        message: err.message || "Failed to load starter code",
        type: "network",
      });
    } finally {
      setBoilerplateLoading(false);
    }
  };

  const getProblemDescription = () => {
    return problem?.statement
      || problem?.description
      || problem?.question
      || problem?.question_title
      || problemTopics.join(", ")
      || "Coding challenge";
  };

  const handleCreativeMind = async () => {
    setCreativeLoading(true);
    setCreativeError("");
    try {
      const data = await api.creativeMind({
        problemDescription: getProblemDescription(),
        code,
        language,
        topic: problemTopics.slice(0, 3).join(", "),
        mode: creativeMode,
      });
      setCreativeResult(data);
      setActiveTab("creative");
      setStatusNote(`Creative coach ready in ${creativeMode} mode`);
      playSound.success();
    } catch (err) {
      playSound.error();
      setCreativeError(err.message || "Creative coach failed to load");
    } finally {
      setCreativeLoading(false);
    }
  };

  const handleSubmit = async () => {
    if (!problemId) { setError({ message: "No problem selected. Open a problem to submit.", type: "validation" }); return; }
    setLoading(true);
    setError(null);
    setSubmissionResult(null);
    try {
      const data = await api.submitQuestionCode(problemId, { code, language });
      setSubmissionResult(data);
      if (data.solved) {
        setShowCelebration(true);
        playSound.levelUp();
      } else {
        playSound.error();
      }
      if (problemId) {
        api.getProblemSubmissions(problemId, 10).then(setSubmissions).catch(() => {});
      }
    } catch (err) {
      playSound.error();
      setError({
        message: err.message,
        type: "network",
        explanation: err.error_explanation || null,
      });
    } finally {
      setLoading(false);
    }
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handler = (e) => {
      const key = e.key.toLowerCase();
      if ((e.ctrlKey || e.metaKey) && key === "enter") {
        e.preventDefault();
        if (e.shiftKey) handleSubmit();
        else handleRun();
      }
      if ((e.ctrlKey || e.metaKey) && e.altKey && key === "v") {
        e.preventDefault();
        setViewMode("visualizer");
        if (!traceData) handleTraceCode();
      }
      if ((e.ctrlKey || e.metaKey) && e.altKey && key === "t") {
        e.preventDefault();
        setActiveTab("testcases");
      }
      if ((e.ctrlKey || e.metaKey) && e.altKey && key === "c") {
        e.preventDefault();
        setActiveTab("console");
      }
      if ((e.ctrlKey || e.metaKey) && key === "s") {
        e.preventDefault();
        autoSaveCode();
      }
      if ((e.ctrlKey || e.metaKey) && key === "l") {
        e.preventDefault();
        setCode(DEFAULT_CODE[language] || "");
        setStatusNote("Reset to template");
      }
    };

    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [autoSaveCode, handleRun, handleSubmit, handleTraceCode, language, traceData]);

  const addTestCase = () => setTestCases([...testCases, { id: Date.now(), input: "", expected: "", isHidden: false }]);
  const removeTestCase = (id) => {
    if (testCases.length <= 1) return;
    setTestCases(testCases.filter((tc) => tc.id !== id));
    if (activeTestCase >= testCases.length - 1) setActiveTestCase(Math.max(0, testCases.length - 2));
  };
  const updateTestCase = (id, field, value) => setTestCases(testCases.map((tc) => (tc.id === id ? { ...tc, [field]: value } : tc)));

  const copyCode = () => {
    navigator.clipboard?.writeText(code);
    setSavedIndicator(true);
    setTimeout(() => setSavedIndicator(false), 1500);
  };

  const downloadCode = () => {
    const ext = LANGUAGES.find(l => l.id === language)?.icon ? `.${language === "cpp" ? "cpp" : language === "javascript" ? "js" : language === "typescript" ? "ts" : language}` : ".txt";
    const blob = new Blob([code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `solution${ext}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleEditorMount = (editor) => {
    editorRef.current = editor;
    editor.focus();
  };

  const currentLang = LANGUAGES.find((l) => l.id === language) || langs[0];

  const passedCount = results?.results?.filter(r => r.passed).length || 0;
  const totalCount = results?.results?.length || 0;

  return (
    <div className={`h-full flex flex-col ${isFullscreen ? "fixed inset-0 z-50 bg-gray-50" : ""}`}>
      {/* Celebration */}
      <CelebrationOverlay show={showCelebration} type="perfect" message="Problem Solved!" onClose={() => setShowCelebration(false)} />

      {/* Top Bar */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-gray-200 bg-space-panel/80">
        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-gray-400">main.{currentLang?.id === "cpp" ? "cpp" : currentLang?.id || "txt"}</span>
          {problemId && <span className="text-[10px] text-gray-500">#{problemId.slice(-6)}</span>}
          <AnimatePresence>
            {savedIndicator && (
              <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex items-center gap-1 text-[10px] text-green-400">
                <Cloud size={10} /> Saved
              </motion.span>
            )}
          </AnimatePresence>
          {statusNote && (
            <span className="hidden md:inline-flex items-center gap-1 text-[10px] px-2 py-1 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20">
              <Sparkles size={10} />
              {statusNote}
            </span>
          )}
          {isProblemMode && (
            <div className="flex items-center gap-1.5 px-2 py-1 rounded-md bg-gray-800/50 text-xs font-mono">
              <Timer size={12} className={timerRunning ? "text-green-400" : "text-gray-500"} />
              <span className={timerRunning ? "text-green-400" : "text-gray-500"}>{formatTime(elapsed)}</span>
              {timerRunning && (
                <button onClick={() => setTimerRunning(false)} className="text-gray-500 hover:text-red-400">
                  <X size={10} />
                </button>
              )}
            </div>
          )}
          {executionTime !== null && (
            <div className="flex items-center gap-1.5 text-[10px] text-gray-500">
              <Cpu size={10} />
              <span>{executionTime.toFixed(3)}s</span>
              {memoryUsage > 0 && (
                <>
                  <HardDrive size={10} className="ml-1" />
                  <span>{formatMemory(memoryUsage)}</span>
                </>
              )}
            </div>
          )}
        </div>
        <div className="flex items-center gap-1.5">
          {/* Mode Switcher */}
          <div className="bg-slate-900 border border-slate-700 p-0.5 rounded-lg flex items-center mr-1">
            <button
              onClick={() => setViewMode("editor")}
              className={`px-2 py-0.5 text-xs font-medium rounded-md transition-colors ${
                viewMode === "editor" ? "bg-indigo-600 text-white font-bold" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Code Editor
            </button>
            <button
              onClick={() => {
                if (!traceData) handleTraceCode();
                else setViewMode("visualizer");
              }}
              className={`px-2 py-0.5 text-xs font-medium rounded-md transition-colors flex items-center gap-1 ${
                viewMode === "visualizer" ? "bg-indigo-600 text-white font-bold" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Sparkles size={11} className="text-purple-300 animate-pulse" />
              Visualizer
            </button>
          </div>

          <select value={language} onChange={(e) => setLanguage(e.target.value)} className="px-2 py-1 bg-space-panel border border-gray-200 rounded text-xs text-gray-200 focus:outline-none max-w-[100px] sm:max-w-none">
            {langs.map((l) => <option key={l.id} value={l.id}>{l.icon} {l.name}</option>)}
          </select>
          <button onClick={handleRun} disabled={loading} className="flex items-center gap-1 px-2 sm:px-2.5 py-1 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white text-xs font-medium rounded transition-colors">
            {loading ? <Loader size={11} className="animate-spin" /> : <><Play size={11} /> <span className="hidden sm:inline">Run</span></>}
          </button>
          <button onClick={handleTraceCode} disabled={traceLoading} className="flex items-center gap-1 px-2 sm:px-2.5 py-1 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white text-xs font-medium rounded transition-colors shadow-purple-600/30">
            {traceLoading ? <Loader size={11} className="animate-spin" /> : <><Sparkles size={11} /> <span className="hidden sm:inline">Visualize</span></>}
          </button>
          <button onClick={handleCreativeMind} disabled={creativeLoading} className="flex items-center gap-1 px-2 sm:px-2.5 py-1 bg-fuchsia-600 hover:bg-fuchsia-700 disabled:opacity-50 text-white text-xs font-medium rounded transition-colors shadow-fuchsia-600/30">
            {creativeLoading ? <Loader size={11} className="animate-spin" /> : <><WandSparkles size={11} /> <span className="hidden sm:inline">Creative</span></>}
          </button>
          <button
            onClick={handleLoadBoilerplate}
            disabled={boilerplateLoading}
            className="flex items-center gap-1 px-2 sm:px-2.5 py-1 bg-amber-500 hover:bg-amber-600 disabled:opacity-50 text-white text-xs font-medium rounded transition-colors"
            title={problemTopics.length > 0 ? `Load starter for ${starterProblemType}` : "Load default starter code"}
          >
            {boilerplateLoading ? <Loader size={11} className="animate-spin" /> : <><BookOpen size={11} /> <span className="hidden sm:inline">Starter</span></>}
          </button>
          {problemId && (
            <button onClick={handleSubmit} disabled={loading} className="flex items-center gap-1 px-2 sm:px-2.5 py-1 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white text-xs font-medium rounded transition-colors">
              {loading ? <Loader size={11} className="animate-spin" /> : <><Send size={11} /> <span className="hidden sm:inline">Submit</span></>}
            </button>
          )}
          <button onClick={copyCode} className="hidden sm:block p-1.5 text-gray-400 hover:text-text-primary" title="Copy code (Ctrl+L to reset)"><Copy size={13} /></button>
          <button onClick={downloadCode} className="hidden sm:block p-1.5 text-gray-400 hover:text-text-primary" title="Download"><Download size={13} /></button>
          <button onClick={() => { CodeCache.remove(problemId, language); setCode(DEFAULT_CODE[language] || ""); }} className="hidden sm:block p-1.5 text-gray-400 hover:text-text-primary" title="Reset to template"><RotateCcw size={13} /></button>
          <button onClick={() => setShowSettings(!showSettings)} className="p-1.5 text-gray-400 hover:text-text-primary" title="Settings"><Settings2 size={13} /></button>
          {isProblemMode && (
            <button onClick={() => { setActiveTab("submissions"); }} className="hidden sm:block p-1.5 text-gray-400 hover:text-text-primary" title="Submissions"><History size={13} /></button>
          )}
          <button
            onClick={() => setShowLeftPanel((prev) => !prev)}
            className="hidden md:block p-1.5 text-gray-400 hover:text-text-primary"
            title={showLeftPanel ? "Hide editor panel" : "Show editor panel"}
          >
            {showLeftPanel ? <ChevronLeft size={13} /> : <ChevronRight size={13} />}
          </button>
          <button onClick={() => setIsFullscreen(!isFullscreen)} className="p-1.5 text-gray-400 hover:text-text-primary" title="Fullscreen">
            {isFullscreen ? <Minimize2 size={13} /> : <Fullscreen size={13} />}
          </button>
        </div>
      </div>

      {/* Settings Dropdown */}
      <AnimatePresence>
        {showSettings && (
          <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }} exit={{ height: 0, opacity: 0 }} className="border-b border-gray-200 bg-space-panel/50 overflow-hidden">
            <div className="px-4 py-3 flex flex-wrap gap-6">
              <div>
                <label className="block text-[10px] text-gray-500 mb-1">Font Size</label>
                <select value={fontSize} onChange={(e) => setFontSize(Number(e.target.value))} className="px-2 py-1 bg-gray-50 border border-gray-200 rounded text-xs text-gray-200">
                  {FONT_SIZES.map((s) => <option key={s} value={s}>{s}px</option>)}
                </select>
              </div>
              <div>
                <label className="block text-[10px] text-gray-500 mb-1">Editor Theme</label>
                <select value={editorTheme} onChange={(e) => setEditorTheme(e.target.value)} className="px-2 py-1 bg-gray-50 border border-gray-200 rounded text-xs text-gray-200">
                  {THEMES.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-[10px] text-gray-500 mb-1">Tab Size</label>
                <select value={tabSize} onChange={(e) => setTabSize(Number(e.target.value))} className="px-2 py-1 bg-gray-50 border border-gray-200 rounded text-xs text-gray-200">
                  <option value={2}>2 spaces</option>
                  <option value={4}>4 spaces</option>
                </select>
              </div>
              <div className="flex items-end">
                <button onClick={() => setShowShortcuts(true)} className="text-xs text-cyber-blue hover:underline">Keyboard Shortcuts</button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Main Content: Resizable split or Visualizer */}
      {viewMode === "visualizer" ? (
        <div className="flex-1 overflow-y-auto p-4 bg-slate-950">
          <AlgorithmVisualizer traceData={traceData} code={code} language={language} />
        </div>
      ) : (
        <div ref={splitRef} className="flex-1 flex flex-col md:flex-row overflow-hidden relative">
        {/* Left: Editor */}
        {showLeftPanel && (
          <div className="flex flex-col h-1/2 md:h-full" style={{ width: typeof window !== 'undefined' && window.innerWidth < 768 ? '100%' : `${splitRatio}%` }}>
            <Editor
              height="100%"
              language={language === "cpp" ? "cpp" : language === "c" ? "c" : language}
              theme={editorTheme}
              value={code}
              onChange={handleCodeChange}
              onMount={handleEditorMount}
              options={{
                minimap: { enabled: false },
                fontSize,
                tabSize,
                lineNumbers: "on",
                roundedSelection: false,
                scrollBeyondLastLine: false,
                automaticLayout: true,
                wordWrap: "on",
                padding: { top: 12 },
                bracketPairColorization: { enabled: true },
                suggest: { showWords: false },
                quickSuggestions: false,
                renderLineHighlight: "all",
                smoothScrolling: true,
                cursorBlinking: "smooth",
                cursorSmoothCaretAnimation: "on",
                formatOnPaste: true,
                formatOnType: true,
              }}
            />
          </div>
        )}

        {/* Drag handle */}
        {showLeftPanel && (
          <div
            className="hidden md:block w-1 bg-space-border hover:bg-cyber-blue cursor-col-resize transition-colors z-10"
            onMouseDown={() => { isDragging.current = true; }}
          />
        )}

        {/* Right: Tabs + Console */}
        <div className="flex flex-col overflow-hidden h-1/2 md:h-full" style={{ width: typeof window !== 'undefined' && window.innerWidth < 768 ? '100%' : showLeftPanel ? `${100 - splitRatio}%` : "100%" }}>
          {/* Tabs */}
          <div className="flex items-center gap-0 border-b border-gray-200 bg-space-panel/30">
            <button
              onClick={() => setActiveTab("testcases")}
              className={`px-3 py-2 text-xs font-medium border-b-2 transition-colors ${activeTab === "testcases" ? "border-cyber-blue text-cyber-blue" : "border-transparent text-gray-500 hover:text-gray-300"}`}
            >
              <span className="flex items-center gap-1"><Terminal size={12} /> Test Cases</span>
            </button>
            <button
              onClick={() => setActiveTab("console")}
              className={`px-3 py-2 text-xs font-medium border-b-2 transition-colors ${activeTab === "console" ? "border-cyber-green text-cyber-green" : "border-transparent text-gray-500 hover:text-gray-300"}`}
            >
              <span className="flex items-center gap-1"><Code2 size={12} /> Console</span>
              {results && (
                <span className={`ml-1 text-[10px] px-1.5 rounded-full font-medium ${
                  results.all_passed ? "bg-green-800 text-green-300" : results.passed_count > 0 ? "bg-yellow-800 text-yellow-300" : "bg-red-800 text-red-300"
                }`}>{results.passed_count}/{results.total_count}</span>
              )}
            </button>
            <button
              onClick={() => { setActiveTab("creative"); if (!creativeResult && !creativeLoading) handleCreativeMind(); }}
              className={`px-3 py-2 text-xs font-medium border-b-2 transition-colors ${activeTab === "creative" ? "border-fuchsia-400 text-fuchsia-300" : "border-transparent text-gray-500 hover:text-gray-300"}`}
            >
              <span className="flex items-center gap-1"><WandSparkles size={12} /> Creative Mind</span>
            </button>
            {problemId && (
              <button
                onClick={() => { setActiveTab("submissions"); }}
                className={`px-3 py-2 text-xs font-medium border-b-2 transition-colors ${activeTab === "submissions" ? "border-yellow-400 text-yellow-400" : "border-transparent text-gray-500 hover:text-gray-300"}`}
              >
                <span className="flex items-center gap-1"><History size={12} /> Submissions</span>
                {submissions.length > 0 && <span className="ml-1 text-[10px] text-gray-500">({submissions.length})</span>}
              </button>
            )}
            <div className="flex-1" />
            {activeTab === "testcases" && (
              <button onClick={handleRunTestCases} disabled={loading} className="mr-2 px-2.5 py-1 bg-green-600 hover:bg-green-700 disabled:opacity-50 text-white text-[11px] font-medium rounded transition-colors flex items-center gap-1">
                {loading ? <Loader size={10} className="animate-spin" /> : <Play size={10} />} Run All
              </button>
            )}
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-y-auto">
            {activeTab === "creative" && (
              <div className="p-4 space-y-4">
                <div className="flex items-center justify-between gap-3 flex-wrap">
                  <div>
                    <div className="text-[10px] font-mono uppercase tracking-[0.3em] text-fuchsia-400/70">Creative Mind</div>
                    <h3 className="text-lg font-semibold text-white mt-1">Turn this problem into a story you can remember</h3>
                    <p className="text-xs text-gray-400 mt-1">Pick a coaching style and let the IDE reframe the challenge for you.</p>
                  </div>
                  <button
                    onClick={handleCreativeMind}
                    disabled={creativeLoading}
                    className="px-3 py-1.5 rounded-lg bg-fuchsia-600 hover:bg-fuchsia-700 disabled:opacity-50 text-white text-xs font-medium flex items-center gap-2"
                  >
                    {creativeLoading ? <Loader size={11} className="animate-spin" /> : <WandSparkles size={11} />}
                    Refresh coach
                  </button>
                </div>

                <div className="flex flex-wrap gap-2">
                  {[
                    { id: "mentor", label: "Mentor" },
                    { id: "story", label: "Story Mode" },
                    { id: "boss", label: "Boss Fight" },
                  ].map((mode) => (
                    <button
                      key={mode.id}
                      onClick={() => setCreativeMode(mode.id)}
                      className={`px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                        creativeMode === mode.id
                          ? "bg-fuchsia-600 text-white"
                          : "bg-white/5 text-gray-400 hover:text-white border border-white/10"
                      }`}
                    >
                      {mode.label}
                    </button>
                  ))}
                </div>

                {creativeError && (
                  <div className="rounded-xl border border-red-500/30 bg-red-950/20 p-3 text-sm text-red-300">
                    {creativeError}
                  </div>
                )}

                {!creativeResult && !creativeLoading && (
                  <div className="rounded-2xl border border-dashed border-fuchsia-500/30 bg-fuchsia-500/5 p-5 text-sm text-gray-300">
                    Press <span className="text-fuchsia-300 font-semibold">Refresh coach</span> to generate a creative breakdown for this problem.
                  </div>
                )}

                {creativeLoading && (
                  <div className="rounded-2xl border border-white/10 bg-white/5 p-5 flex items-center gap-3 text-sm text-gray-300">
                    <Loader size={14} className="animate-spin text-fuchsia-400" />
                    Building your creative coach...
                  </div>
                )}

                {creativeResult && (
                  <div className="grid gap-4">
                    <div className="rounded-2xl bg-gradient-to-br from-fuchsia-600/20 via-slate-900 to-indigo-950 border border-fuchsia-500/20 p-5">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <div className="text-[10px] uppercase tracking-[0.35em] text-fuchsia-300/80 font-mono">{creativeResult.title || "Creative Mind"}</div>
                          <p className="text-white text-lg font-semibold mt-2">{creativeResult.mission}</p>
                        </div>
                        <div className="px-2 py-1 rounded-full bg-white/10 text-[10px] font-mono text-gray-300 uppercase">
                          {creativeMode}
                        </div>
                      </div>
                      <div className="mt-4 space-y-3 text-sm text-gray-200">
                        <div>
                          <span className="text-fuchsia-300 font-semibold">Analogy: </span>
                          <span>{creativeResult.analogy}</span>
                        </div>
                        <div>
                          <span className="text-cyan-300 font-semibold">First move: </span>
                          <span>{creativeResult.first_move}</span>
                        </div>
                        <div>
                          <span className="text-amber-300 font-semibold">Mini challenge: </span>
                          <span>{creativeResult.micro_challenge}</span>
                        </div>
                        <div>
                          <span className="text-rose-300 font-semibold">Edge case watch: </span>
                          <span>{creativeResult.edge_case_watch}</span>
                        </div>
                      </div>
                    </div>
                    <div className="rounded-2xl border border-white/10 bg-white/5 p-4 text-sm text-gray-200">
                      <div className="text-[10px] uppercase tracking-[0.3em] text-gray-500 font-mono mb-2">Coach note</div>
                      <p className="leading-relaxed">{creativeResult.pep_talk}</p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === "testcases" && (
              <div className="p-3 space-y-3">
                {/* Custom stdin input */}
                {!isProblemMode && (
                  <div>
                    <label className="block text-[10px] text-gray-500 mb-1">Standard Input (stdin)</label>
                    <textarea
                      value={stdin}
                      onChange={(e) => setStdin(e.target.value)}
                      placeholder="Enter input here..."
                      className="w-full px-2 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs text-gray-200 focus:border-cyber-blue focus:outline-none resize-none font-mono"
                      rows={3}
                    />
                  </div>
                )}

                {/* Test case tabs */}
                <div className="flex items-center gap-1 overflow-x-auto">
                  {testCases.map((tc, idx) => {
                    const tcResult = results?.results?.[idx];
                    return (
                      <button
                        key={tc.id}
                        onClick={() => setActiveTestCase(idx)}
                        className={`flex items-center gap-1.5 px-2.5 py-1 text-[10px] rounded-lg transition-all shrink-0 ${
                          activeTestCase === idx
                            ? "bg-gray-700 text-white border border-gray-500"
                            : "bg-gray-800/50 text-gray-400 hover:bg-gray-800"
                        }`}
                      >
                        {tcResult && (
                          tcResult.passed
                            ? <CheckCircle size={10} className="text-green-400" />
                            : <XCircle size={10} className="text-red-400" />
                        )}
                        Case {idx + 1}
                      </button>
                    );
                  })}
                  <button onClick={addTestCase} className="p-1.5 text-cyber-blue hover:text-cyber-blue/80" title="Add test case"><Plus size={14} /></button>
                </div>

                {/* Active test case input */}
                {testCases[activeTestCase] && (
                  <motion.div key={testCases[activeTestCase].id} initial={{ opacity: 0, y: 5 }} animate={{ opacity: 1, y: 0 }} className="bg-gray-50/50 rounded-lg p-3 border border-gray-200 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-mono text-gray-500">Case {activeTestCase + 1} of {testCases.length}</span>
                      <div className="flex items-center gap-2">
                        {testCases.length > 1 && (
                          <button onClick={() => removeTestCase(testCases[activeTestCase].id)} className="text-gray-600 hover:text-red-400 flex items-center gap-1 text-[10px]">
                            <Trash2 size={11} /> Remove
                          </button>
                        )}
                      </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      <div>
                        <label className="block text-[10px] text-gray-500 mb-1">Input</label>
                        <textarea value={testCases[activeTestCase].input} onChange={(e) => updateTestCase(testCases[activeTestCase].id, "input", e.target.value)} placeholder="stdin..." className="w-full px-2 py-1.5 bg-space-panel border border-gray-200 rounded text-xs text-gray-200 focus:border-cyber-blue focus:outline-none resize-none font-mono" rows={4} />
                      </div>
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <label className="text-[10px] text-gray-500">Expected Output</label>
                          <button onClick={() => setShowExpected(!showExpected)} className="text-gray-600 hover:text-gray-400">
                            {showExpected ? <EyeOff size={10} /> : <Eye size={10} />}
                          </button>
                        </div>
                        {showExpected ? (
                          <textarea value={testCases[activeTestCase].expected} onChange={(e) => updateTestCase(testCases[activeTestCase].id, "expected", e.target.value)} placeholder="Expected..." className="w-full px-2 py-1.5 bg-space-panel border border-gray-200 rounded text-xs text-gray-200 focus:border-cyber-blue focus:outline-none resize-none font-mono" rows={4} />
                        ) : (
                          <div className="w-full px-2 py-1.5 bg-space-panel border border-gray-200 rounded text-xs text-gray-500 italic font-mono" style={{ height: "94px" }}>Hidden</div>
                        )}
                      </div>
                    </div>

                    {/* Result for this test case */}
                    {results?.results?.[activeTestCase] && (
                      <div className={`p-2 rounded text-[11px] ${results.results[activeTestCase].passed ? "bg-green-900/20 text-green-400" : "bg-red-900/20 text-red-400"}`}>
                        <div className="flex items-center gap-2">
                          {results.results[activeTestCase].passed ? <CheckCircle size={12} /> : <XCircle size={12} />}
                          <span>{results.results[activeTestCase].passed ? "Passed" : "Failed"}</span>
                          {results.results[activeTestCase].execution_time > 0 && (
                            <span className="text-gray-500 ml-auto">{results.results[activeTestCase].execution_time.toFixed(3)}s</span>
                          )}
                        </div>
                        {!results.results[activeTestCase].passed && results.results[activeTestCase].actual && !results.results[activeTestCase].is_hidden && (
                          <div className="mt-1 space-y-0.5">
                            <div><span className="text-gray-500">Actual: </span><span className="text-red-300">{results.results[activeTestCase].actual}</span></div>
                            {results.results[activeTestCase].error && <div><span className="text-gray-500">Error: </span><span className="text-red-300">{results.results[activeTestCase].error}</span></div>}
                          </div>
                        )}
                      </div>
                    )}
                  </motion.div>
                )}
              </div>
            )}

            {activeTab === "console" && (
              <div className="p-3">
                <div className="bg-gray-50 rounded-lg p-3 font-mono text-xs min-h-[200px] max-h-[400px] overflow-y-auto">
                  {/* Loading */}
                  {loading && (
                    <div className="flex items-center gap-2 text-gray-400">
                      <Loader size={14} className="animate-spin text-cyber-blue" />
                      <span>Executing...</span>
                    </div>
                  )}

                  {/* Error */}
                  {!loading && error && (
                    <div className="space-y-2">
                      <div className={`flex items-start gap-2 p-3 rounded-lg ${
                        error.type === "compile" ? "bg-red-900/30 text-red-400" :
                        error.type === "tle" || error.type === "mle" ? "bg-orange-900/30 text-orange-400" :
                        error.type === "network" ? "bg-purple-900/30 text-purple-400" :
                        "bg-red-900/30 text-red-400"
                      }`}>
                        <AlertTriangle size={14} className="mt-0.5 shrink-0" />
                        <div className="flex-1">
                          <div className="font-medium flex items-center gap-2">
                            {error.type === "compile" && <span className="text-[10px] px-1.5 py-0.5 bg-red-800/50 rounded font-medium">Compilation Error</span>}
                            {error.type === "runtime" && <span className="text-[10px] px-1.5 py-0.5 bg-orange-800/50 rounded font-medium">Runtime Error</span>}
                            {error.type === "tle" && <span className="text-[10px] px-1.5 py-0.5 bg-orange-800/50 rounded font-medium">Time Limit Exceeded</span>}
                            {error.type === "mle" && <span className="text-[10px] px-1.5 py-0.5 bg-orange-800/50 rounded font-medium">Memory Limit Exceeded</span>}
                            {error.type === "network" && <span className="text-[10px] px-1.5 py-0.5 bg-purple-800/50 rounded font-medium">Network Error</span>}
                            {error.type === "validation" && <span className="text-[10px] px-1.5 py-0.5 bg-yellow-800/50 rounded font-medium">Input Error</span>}
                          </div>
                          <pre className="mt-2 whitespace-pre-wrap break-words text-[11px] leading-relaxed">{error.message}</pre>
                          {error.stderr && error.stderr !== error.message && (
                            <pre className="mt-1 text-[10px] text-gray-500 whitespace-pre-wrap break-words">{error.stderr}</pre>
                          )}
                          {error.line && (
                            <button onClick={() => editorRef.current?.setPosition({ lineNumber: error.line, column: 1 })} className="mt-2 text-cyber-blue hover:underline text-[11px]">
                              Jump to line {error.line}
                            </button>
                          )}
                          {error.explanation && (
                            <div className="mt-2 p-2 bg-blue-900/20 rounded border border-blue-800/30">
                              <p className="text-[10px] font-semibold text-blue-400 mb-1">Why your code failed:</p>
                              <p className="text-[10px] text-gray-300 whitespace-pre-wrap">{error.explanation}</p>
                            </div>
                          )}
                          {error.hint && (
                            <p className="mt-2 text-[10px] text-gray-400 italic">{error.hint}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Submission result */}
                  {!loading && submissionResult && (
                    <div className="space-y-3">
                      <div className={`flex items-center gap-2 ${submissionResult.solved ? "text-green-400" : "text-yellow-400"}`}>
                        {submissionResult.solved ? <CheckCircle size={16} /> : <XCircle size={16} />}
                        <span className="font-medium">{submissionResult.summary}</span>
                      </div>
                      <div className="text-xs text-gray-400 flex gap-4">
                        <span>Score: {submissionResult.score}%</span>
                        <span>XP: +{submissionResult.xp_gained}</span>
                        <span>Time: {formatTime(elapsed)}</span>
                      </div>
                      {/* Test case results */}
                      <div className="grid grid-cols-1 gap-1.5 mt-2">
                        {submissionResult.results?.map((r, i) => (
                          <div key={i} className={`flex items-center gap-2 px-2.5 py-1.5 rounded text-xs ${r.passed ? "bg-green-900/20 text-green-400" : "bg-red-900/20 text-red-400"}`}>
                            {r.passed ? <CheckCircle size={12} /> : <XCircle size={12} />}
                            <span>Test {i + 1}</span>
                            {r.execution_time && <span className="text-gray-500 ml-auto">{r.execution_time.toFixed(3)}s</span>}
                          </div>
                        ))}
                      </div>
                      {submissionResult.solved && (
                        <div className="flex items-center gap-2 p-3 bg-green-900/20 rounded-lg text-green-400 text-sm">
                          <Sparkles size={16} />
                          <span className="font-medium">Congratulations! You solved this problem!</span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Test case results */}
                  {!loading && results && results.all_passed !== undefined && (
                    <div className="space-y-2">
                      <div className={`flex items-center gap-2 ${results.all_passed ? "text-green-400" : "text-yellow-400"}`}>
                        {results.all_passed ? <CheckCircle size={16} /> : <XCircle size={16} />}
                        <span className="font-medium">{results.summary}</span>
                      </div>
                      <div className="flex items-center gap-4 text-[10px] text-gray-500">
                        <span>{passedCount}/{totalCount} passed</span>
                        {executionTime > 0 && <span>Total: {executionTime.toFixed(3)}s</span>}
                      </div>
                      {results.results?.map((r, i) => (
                        <div key={i} className={`p-2.5 rounded-lg ${r.passed ? "bg-green-900/20" : "bg-red-900/20"}`}>
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-gray-400 text-[11px]">Test {i + 1} {r.is_hidden ? "(hidden)" : ""}</span>
                            <div className="flex items-center gap-2">
                              {r.execution_time && <span className="text-[10px] text-gray-500">{r.execution_time.toFixed(3)}s</span>}
                              {r.passed ? <CheckCircle size={12} className="text-green-400" /> : <XCircle size={12} className="text-red-400" />}
                            </div>
                          </div>
                          {!r.is_hidden && !r.passed && (
                            <div className="space-y-1 text-[11px] mt-1">
                              <div><span className="text-gray-500">Input: </span><span className="text-gray-300">{r.input}</span></div>
                              <div><span className="text-gray-500">Expected: </span><span className="text-green-400">{r.expected}</span></div>
                              <div><span className="text-gray-500">Actual: </span><span className="text-red-400">{r.actual}</span></div>
                            </div>
                          )}
                          {r.error && <div className="text-red-400 text-[11px] mt-1">{r.error}</div>}
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Stdout */}
                  {!loading && results && results.success && results.stdout && !results.summary && (
                    <pre className="text-green-700 whitespace-pre-wrap">{results.stdout}</pre>
                  )}

                  {/* Empty state */}
                  {!loading && !results && !error && !submissionResult && (
                    <div className="text-gray-600 text-center py-8">
                      <Terminal size={24} className="mx-auto mb-2 opacity-50" />
                      <p className="text-xs">Run your code to see output</p>
                      <p className="text-[10px] text-gray-700 mt-1">Ctrl+Enter to run · Ctrl+Shift+Enter to submit</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === "submissions" && (
              <div className="p-3">
                {submissions.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <History size={24} className="mx-auto mb-2 opacity-50" />
                    <p className="text-xs">No submissions yet</p>
                  </div>
                ) : (
                  <div className="space-y-2">
                    <div className="text-[10px] text-gray-500 mb-2">Recent Submissions</div>
                    {submissions.map((sub, i) => (
                      <div key={sub.id || i} className={`flex items-center gap-3 p-2.5 rounded-lg border ${sub.passed || sub.all_passed ? "bg-green-900/10 border-green-800/30" : "bg-red-900/10 border-red-800/30"}`}>
                        {sub.passed || sub.all_passed ? <CheckCircle size={14} className="text-green-400 shrink-0" /> : <XCircle size={14} className="text-red-400 shrink-0" />}
                        <div className="flex-1 min-w-0">
                          <div className="text-xs text-gray-300 truncate">{sub.language} — {sub.passed_count || 0}/{sub.total_count || "?"} passed</div>
                          <div className="text-[10px] text-gray-500">{sub.created_at ? new Date(sub.created_at).toLocaleString() : ""}</div>
                        </div>
                        {sub.execution_time && <span className="text-[10px] text-gray-500 shrink-0">{sub.execution_time?.toFixed(2)}s</span>}
                        {sub.score !== undefined && <span className="text-[10px] text-gray-400 shrink-0">{sub.score}%</span>}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
      )} 

      <div className="flex items-center justify-between gap-3 px-3 py-2 border-t border-gray-200 bg-space-panel/70 text-[10px] text-gray-500 font-mono">
        <div className="flex items-center gap-3 overflow-x-auto">
          <span className="flex items-center gap-1"><Keyboard size={10} /> Shortcuts ready</span>
          <span>{currentLang?.name || language}</span>
          <span>{editorTheme}</span>
          <span>{showLeftPanel ? "split view" : "focus mode"}</span>
        </div>
        <div className="flex items-center gap-2">
          {traceData?.source && <span>trace: {traceData.source}</span>}
          {problemTopics.length > 0 && <span>topics: {problemTopics.slice(0, 2).join(", ")}</span>}
        </div>
      </div>

      {/* Keyboard shortcuts modal */}
      <AnimatePresence>
        {showShortcuts && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-50 flex items-center justify-center bg-black/60" onClick={() => setShowShortcuts(false)}>
            <motion.div initial={{ scale: 0.95 }} animate={{ scale: 1 }} exit={{ scale: 0.95 }} className="bg-space-panel border border-gray-200 rounded-xl p-6 max-w-md w-full mx-4 shadow-xl" onClick={(e) => e.stopPropagation()}>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-text-primary">Keyboard Shortcuts</h3>
                <button onClick={() => setShowShortcuts(false)} className="text-gray-400 hover:text-text-primary"><X size={16} /></button>
              </div>
              <div className="space-y-2">
                {IDE_SHORTCUTS.map(([key, desc]) => (
                  <div key={key} className="flex items-center justify-between py-1.5">
                    <span className="text-xs text-gray-300">{desc}</span>
                    <kbd className="px-2 py-0.5 bg-gray-800 border border-gray-700 rounded text-[11px] text-gray-400 font-mono">{key}</kbd>
                  </div>
                ))}
                <div className="pt-2 border-t border-gray-700/60 text-[11px] text-gray-500">
                  Tip: use Starter to pull problem-aware boilerplate before you code.
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
