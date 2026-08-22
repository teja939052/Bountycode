import { useState, useEffect, useCallback } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
import Spinner from "../components/ui/Spinner";
import {
  Wand2,
  FileCode,
  CheckCircle2,
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  Sparkles,
  Code2,
  Shield,
  Zap,
  Eye,
  Download,
  Share2,
  Clock,
  ChevronRight,
  SplitSquareVertical,
} from "lucide-react";

const LANGUAGES = [
  { value: "python", label: "Python" },
  { value: "javascript", label: "JavaScript" },
  { value: "typescript", label: "TypeScript" },
  { value: "java", label: "Java" },
  { value: "cpp", label: "C++" },
  { value: "go", label: "Go" },
  { value: "rust", label: "Rust" },
  { value: "csharp", label: "C#" },
  { value: "ruby", label: "Ruby" },
  { value: "swift", label: "Swift" },
];

const ASPECTS = [
  { value: "performance", label: "Performance", icon: Zap, color: "text-emerald-500" },
  { value: "security", label: "Security", icon: Shield, color: "text-red-500" },
  { value: "readability", label: "Readability", icon: Eye, color: "text-blue-500" },
  { value: "architecture", label: "Architecture", icon: Code2, color: "text-purple-500" },
];

const EXAMPLES = [
  "Build a REST API for a todo app with FastAPI",
  "Create a weather CLI app that fetches data from OpenWeatherMap",
  "Make a Tic-Tac-Toe game with Python and Pygame",
  "Build a URL shortener web app with Flask and SQLite",
  "Create a Markdown to HTML converter in Node.js",
  "Build a terminal-based text editor in Go",
  "Write a web scraper for job listings in Python",
];

export default function ProjectGenerator() {
  const [activeTab, setActiveTab] = useState("generate");
  const [description, setDescription] = useState("");
  const [language, setLanguage] = useState("python");
  const [framework, setFramework] = useState("");
  const [loading, setLoading] = useState(false);
  const [project, setProject] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContents, setFileContents] = useState({});
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [reviewResult, setReviewResult] = useState(null);
  const [reviewLoading, setReviewLoading] = useState(false);
  const [reviewCode, setReviewCode] = useState("");
  const [improveResult, setImproveResult] = useState(null);
  const [improveLoading, setImproveLoading] = useState(false);
  const [improveAspect, setImproveAspect] = useState("readability");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const loadHistory = useCallback(async () => {
    setHistoryLoading(true);
    try {
      const data = await api.getProjectHistory();
      setHistory(data.projects || []);
    } catch {
      // silent
    } finally {
      setHistoryLoading(false);
    }
  }, []);

  useEffect(() => {
    if (activeTab === "generate") loadHistory();
  }, [activeTab, loadHistory]);

  const handleGenerate = async () => {
    if (!description.trim()) return;
    setLoading(true);
    setError("");
    setProject(null);
    setSelectedFile(null);
    setFileContents({});
    try {
      const data = await api.generateProject(description, language, framework);
      setProject(data);
      const contents = {};
      (data.files || []).forEach((f) => {
        contents[f.path] = f.content;
      });
      setFileContents(contents);
      if (data.files?.length) setSelectedFile(data.files[0].path);
      loadHistory();
    } catch (err) {
      setError(err.message || "Generation failed");
    } finally {
      setLoading(false);
    }
  };

  const handleFileEdit = (path, newContent) => {
    setFileContents((prev) => ({ ...prev, [path]: newContent }));
    setProject((prev) => ({
      ...prev,
      files: (prev?.files || []).map((f) =>
        f.path === path ? { ...f, content: newContent } : f
      ),
    }));
  };

  const handleRunReview = async () => {
    const filesToReview = project?.files || [];
    if (!filesToReview.length && !reviewCode.trim()) return;

    let files = filesToReview.length
      ? filesToReview
      : [{ path: "code.txt", content: reviewCode, language: "text" }];

    setReviewLoading(true);
    setReviewResult(null);
    try {
      const data = await api.reviewProject(files);
      setReviewResult(data);
    } catch (err) {
      setError(err.message || "Review failed");
    } finally {
      setReviewLoading(false);
    }
  };

  const handleImprove = async () => {
    const target = project?.files?.find((f) => f.path === selectedFile);
      const code = target?.content || "";
    if (!code.trim()) return;

    setImproveLoading(true);
    setImproveResult(null);
    try {
      const data = await api.improveCode({
        file_path: selectedFile || "code.txt",
        content: code,
        language: target?.language || language,
        aspect: improveAspect,
      });
      setImproveResult(data);
    } catch (err) {
      setError(err.message || "Improvement failed");
    } finally {
      setImproveLoading(false);
    }
  };

  const handleSave = async () => {
    if (!project) return;
    try {
      await api.saveProject({
        files: project.files,
        description: project.description,
        tech_stack: project.tech_stack,
        setup_instructions: project.setup_instructions,
      });
      loadHistory();
    } catch (err) {
      setError(err.message || "Save failed");
    }
  };

  const handleLoadProject = async (pid) => {
    try {
      const data = await api.getProject(pid);
      setProject(data);
      const contents = {};
      (data.files || []).forEach((f) => {
        contents[f.path] = f.content;
      });
      setFileContents(contents);
      if (data.files?.length) setSelectedFile(data.files[0].path);
      setActiveTab("generate");
    } catch {
      // silent
    }
  };

  const handleExport = () => {
    if (!project) return;
    const allContent = project.files
      .map((f) => `// ${f.path}\n\n${f.content}\n`)
      .join("\n\n");
    const blob = new Blob([allContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "project.zip.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  const currentFile = project?.files?.find((f) => f.path === selectedFile);

  const scoreColor = (s) => (s >= 80 ? "text-green-500" : s >= 50 ? "text-yellow-500" : "text-red-500");
  const scoreBg = (s) =>
    s >= 80 ? "bg-green-100 border-green-300" : s >= 50 ? "bg-yellow-100 border-yellow-300" : "bg-red-100 border-red-300";

  const tabs = [
    { key: "generate", label: "Generate", icon: Wand2 },
    { key: "review", label: "Review", icon: CheckCircle2 },
    { key: "improve", label: "Improve", icon: Sparkles },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
      <div className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Wand2 className="text-brand-sky" size={32} />
            AI Project Generator
          </h1>
          <p className="mt-2 text-brand-muted">
            Describe any project idea in natural language &mdash; AI generates complete code, reviews it, and suggests improvements.
          </p>
        </div>

        {error && (
          <div className="mb-6 flex items-center gap-3 rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
            <AlertTriangle size={18} />
            {error}
            <button onClick={() => setError("")} className="ml-auto font-medium hover:underline">Dismiss</button>
          </div>
        )}

        {/* Tabs */}
        <div className="mb-6 flex gap-2 border-b border-brand-primary/10 pb-1">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-2 px-5 py-3 text-sm font-medium rounded-t-xl transition-all ${
                activeTab === tab.key
                  ? "bg-surface-card border border-brand-primary/10 text-brand-sky shadow-sm"
                  : "text-gray-400 hover:text-brand-secondary"
              }`}
            >
              <tab.icon size={16} />
              {tab.label}
            </button>
          ))}
        </div>

        {/* ============ GENERATE TAB ============ */}
        {activeTab === "generate" && (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <div className="rounded-2xl border border-brand-primary/10 bg-surface-card p-6 shadow-sm">
                <label className="block text-sm font-semibold text-brand-primary mb-2">Describe your project</label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="e.g., Build a REST API for a blog with FastAPI and SQLite..."
                  rows={5}
                  className="w-full rounded-xl border border-brand-primary/20 px-4 py-3 text-sm focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20 outline-none resize-none"
                />
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {EXAMPLES.slice(0, 4).map((ex) => (
                    <button
                      key={ex}
                      onClick={() => setDescription(ex)}
                      className="rounded-full border border-brand-primary/10 bg-surface-base px-3 py-1 text-xs text-brand-muted hover:border-brand-sky/30 hover:text-brand-sky transition-colors"
                    >
                      {ex.length > 40 ? ex.slice(0, 40) + "..." : ex}
                    </button>
                  ))}
                </div>

                <div className="mt-5 grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-brand-primary mb-1.5">Language</label>
                    <select
                      value={language}
                      onChange={(e) => setLanguage(e.target.value)}
                      className="w-full rounded-xl border border-brand-primary/20 px-3 py-2.5 text-sm focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20 outline-none"
                    >
                      {LANGUAGES.map((l) => (
                        <option key={l.value} value={l.value}>{l.label}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-brand-primary mb-1.5">Framework (optional)</label>
                    <input
                      value={framework}
                      onChange={(e) => setFramework(e.target.value)}
                      placeholder="e.g., FastAPI, React, Flask"
                      className="w-full rounded-xl border border-brand-primary/20 px-3 py-2.5 text-sm focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20 outline-none"
                    />
                  </div>
                </div>

                <button
                  onClick={handleGenerate}
                  disabled={!description.trim() || loading}
                  className="mt-5 w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-brand-sky to-blue-600 px-6 py-3 text-sm font-semibold text-white shadow-lg transition-all hover:from-blue-600 hover:to-brand-sky disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? <Spinner /> : <Wand2 size={18} />}
                  {loading ? "Generating..." : "Generate Project"}
                </button>
              </div>

              {/* History */}
              <div className="rounded-2xl border border-brand-primary/10 bg-surface-card p-6 shadow-sm">
                <h3 className="text-sm font-semibold text-brand-primary mb-3 flex items-center gap-2">
                  <Clock size={16} /> Past Projects
                </h3>
                {historyLoading ? (
                  <div className="flex justify-center py-4"><Spinner /></div>
                ) : history.length === 0 ? (
                  <p className="text-xs text-gray-400">No projects yet. Generate your first one!</p>
                ) : (
                  <div className="space-y-2 max-h-64 overflow-y-auto">
                    {history.map((p) => (
                      <button
                        key={p.project_id}
                        onClick={() => handleLoadProject(p.project_id)}
                        className="w-full text-left rounded-xl border border-brand-primary/5 bg-surface-base px-4 py-3 text-xs hover:border-brand-sky/30 hover:bg-brand-sky/5 transition-all"
                      >
                        <div className="font-medium text-brand-primary truncate">{p.description}</div>
                        <div className="mt-1 flex items-center gap-2">
                          <span className="rounded bg-blue-100 px-2 py-0.5 text-[10px] font-mono text-blue-700">{p.language}</span>
                          {(p.tech_stack || []).slice(0, 3).map((t) => (
                            <span key={t} className="rounded bg-surface-card/50 px-2 py-0.5 text-[10px] text-brand-muted">{t}</span>
                          ))}
                          <span className="ml-auto text-[10px] text-gray-400">
                            {new Date(p.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Generated Project */}
            <div className="lg:col-span-3">
              {!project ? (
                <div className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-brand-primary/10 bg-surface-card p-12 text-center">
                  <Wand2 size={48} className="text-gray-300 mb-4" />
                  <h3 className="text-lg font-semibold text-gray-400">Your generated project will appear here</h3>
                  <p className="mt-1 text-sm text-gray-400">Describe a project idea and click Generate</p>
                </div>
              ) : (
                <div className="rounded-2xl border border-brand-primary/10 bg-surface-card shadow-sm overflow-hidden">
                  <div className="flex items-center justify-between border-b border-brand-primary/5 px-5 py-3">
                    <div className="flex items-center gap-3">
                      <FileCode size={18} className="text-brand-sky" />
                      <span className="text-sm font-semibold text-brand-primary truncate max-w-[300px]">
                        {project.description}
                      </span>
                    </div>
                    <div className="flex items-center gap-2">
                      <button onClick={handleSave} className="rounded-lg border border-brand-primary/10 px-3 py-1.5 text-xs font-medium text-brand-secondary hover:bg-surface-card">
                        Save
                      </button>
                      <button onClick={handleExport} className="rounded-lg border border-brand-primary/10 px-3 py-1.5 text-xs font-medium text-brand-secondary hover:bg-surface-card flex items-center gap-1">
                        <Download size={12} /> Export
                      </button>
                    </div>
                  </div>

                  {/* Tech stack badges */}
                  <div className="flex flex-wrap gap-1.5 px-5 py-2 border-b border-gray-50 bg-surface-base/50">
                    {(project.tech_stack || []).map((t) => (
                      <span key={t} className="rounded-full bg-gradient-to-r from-brand-sky/10 to-blue-100 px-3 py-0.5 text-xs font-medium text-blue-700">
                        {t}
                      </span>
                    ))}
                    <span className="text-xs text-gray-400 ml-auto">{project.files?.length || 0} files</span>
                  </div>

                  {/* File tree + code viewer */}
                  <div className="flex h-[500px]">
                    <div className="w-56 shrink-0 border-r border-brand-primary/5 bg-surface-base/50 overflow-y-auto p-2">
                      <div className="text-[10px] font-semibold uppercase tracking-wider text-gray-400 px-2 mb-2">Files</div>
                      {(project.files || []).map((f) => (
                        <button
                          key={f.path}
                          onClick={() => setSelectedFile(f.path)}
                          className={`w-full text-left rounded-lg px-3 py-2 text-xs font-mono transition-colors ${
                            selectedFile === f.path
                              ? "bg-brand-sky/10 text-brand-sky font-medium"
                              : "text-brand-secondary hover:bg-surface-card/50"
                          }`}
                        >
                          {f.path}
                        </button>
                      ))}
                    </div>
                    <div className="flex-1 flex flex-col">
                      {currentFile ? (
                        <>
                          <div className="flex items-center justify-between border-b border-brand-primary/5 px-4 py-2 bg-surface-base/30">
                            <span className="text-xs font-mono text-brand-muted">{currentFile.path}</span>
                            <span className="rounded bg-surface-card/50 px-2 py-0.5 text-[10px] text-brand-muted">{currentFile.language}</span>
                          </div>
                          <textarea
                            value={fileContents[currentFile.path] || ""}
                            onChange={(e) => handleFileEdit(currentFile.path, e.target.value)}
                            className="flex-1 w-full p-4 text-sm font-mono leading-relaxed outline-none resize-none bg-surface-card"
                            spellCheck={false}
                          />
                        </>
                      ) : (
                        <div className="flex items-center justify-center flex-1 text-gray-400 text-sm">
                          Select a file to view
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Setup instructions */}
                  {project.setup_instructions && (
                    <div className="border-t border-brand-primary/5 bg-surface-base/70 px-5 py-4">
                      <h4 className="text-xs font-semibold text-brand-secondary mb-2">Setup Instructions</h4>
                      <pre className="text-xs text-brand-muted whitespace-pre-wrap font-sans">{project.setup_instructions}</pre>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ============ REVIEW TAB ============ */}
        {activeTab === "review" && (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <div className="rounded-2xl border border-brand-primary/10 bg-surface-card p-6 shadow-sm">
                <h3 className="text-sm font-semibold text-brand-primary mb-2">Code to Review</h3>
                {project && project.files?.length ? (
                  <div className="space-y-2 mb-4">
                    <p className="text-xs text-brand-muted">Using files from current project ({project.files.length} files)</p>
                    <div className="flex flex-wrap gap-1.5">
                      {project.files.map((f) => (
                        <span key={f.path} className="rounded-full bg-blue-50 px-3 py-1 text-xs font-mono text-blue-600">
                          {f.path}
                        </span>
                      ))}
                    </div>
                  </div>
                ) : (
                  <textarea
                    value={reviewCode}
                    onChange={(e) => setReviewCode(e.target.value)}
                    placeholder="Paste code to review..."
                    rows={10}
                    className="w-full rounded-xl border border-brand-primary/20 px-4 py-3 text-sm font-mono focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20 outline-none resize-none"
                  />
                )}
                <button
                  onClick={handleRunReview}
                  disabled={reviewLoading}
                  className="mt-4 w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 px-6 py-3 text-sm font-semibold text-white shadow-lg transition-all hover:from-green-600 hover:to-emerald-500 disabled:opacity-50"
                >
                  {reviewLoading ? <Spinner /> : <CheckCircle2 size={18} />}
                  {reviewLoading ? "Reviewing..." : "Run Review"}
                </button>
              </div>
            </div>

            <div className="lg:col-span-3">
              {!reviewResult ? (
                <div className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-brand-primary/10 bg-surface-card p-12 text-center">
                  <CheckCircle2 size={48} className="text-gray-300 mb-4" />
                  <h3 className="text-lg font-semibold text-gray-400">AI Code Review</h3>
                  <p className="mt-1 text-sm text-gray-400">Generate a project first, or paste code to review</p>
                </div>
              ) : (
                <div className="rounded-2xl border border-brand-primary/10 bg-surface-card shadow-sm overflow-hidden">
                  <div className="flex items-center gap-6 p-6 border-b border-brand-primary/5">
                    <div className={`flex items-center justify-center w-24 h-24 rounded-full border-4 ${scoreBg(reviewResult.score)}`}>
                      <span className={`text-3xl font-bold ${scoreColor(reviewResult.score)}`}>{reviewResult.score}</span>
                    </div>
                    <div>
                      <h3 className="text-lg font-bold text-white">Code Quality Score</h3>
                      <p className="text-sm text-brand-muted">
                        {reviewResult.score >= 80 ? "Great shape! Minor improvements." :
                         reviewResult.score >= 50 ? "Decent — some areas need work." :
                         "Needs significant improvement."}
                      </p>
                    </div>
                  </div>

                  <div className="p-6 space-y-6">
                    {reviewResult.strengths?.length > 0 && (
                      <div>
                        <h4 className="text-sm font-semibold text-green-700 mb-2 flex items-center gap-1.5">
                          <CheckCircle2 size={15} /> Strengths
                        </h4>
                        <ul className="space-y-1">
                          {reviewResult.strengths.map((s, i) => (
                            <li key={i} className="flex items-start gap-2 text-sm text-brand-secondary">
                              <span className="mt-0.5 w-1.5 h-1.5 rounded-full bg-green-400 shrink-0" />
                              {s}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {reviewResult.improvements?.length > 0 && (
                      <div>
                        <h4 className="text-sm font-semibold text-amber-700 mb-2 flex items-center gap-1.5">
                          <AlertTriangle size={15} /> Improvements
                        </h4>
                        <ul className="space-y-1">
                          {reviewResult.improvements.map((s, i) => (
                            <li key={i} className="flex items-start gap-2 text-sm text-brand-secondary">
                              <span className="mt-0.5 w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0" />
                              {s}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {reviewResult.suggested_fixes?.length > 0 && (
                      <div>
                        <h4 className="text-sm font-semibold text-blue-700 mb-2 flex items-center gap-1.5">
                          <FileCode size={15} /> Suggested Fixes
                        </h4>
                        <div className="space-y-2">
                          {reviewResult.suggested_fixes.map((fix, i) => (
                            <div key={i} className="rounded-xl border border-blue-100 bg-blue-50/50 px-4 py-3">
                              <div className="flex items-center gap-2 text-xs font-mono text-blue-600 mb-1">
                                {fix.file}{fix.line != null ? `:${fix.line}` : ""}
                              </div>
                              <div className="text-sm font-medium text-brand-primary">{fix.issue}</div>
                              <div className="text-xs text-brand-muted mt-0.5">{fix.suggestion}</div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {reviewResult.security_concerns?.length > 0 && (
                      <div>
                        <h4 className="text-sm font-semibold text-red-700 mb-2 flex items-center gap-1.5">
                          <Shield size={15} /> Security Concerns
                        </h4>
                        <ul className="space-y-1">
                          {reviewResult.security_concerns.map((s, i) => (
                            <li key={i} className="flex items-start gap-2 text-sm text-red-600">
                              <AlertTriangle size={14} className="mt-0.5 shrink-0" />
                              {s}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {reviewResult.best_practices?.length > 0 && (
                      <div>
                        <h4 className="text-sm font-semibold text-purple-700 mb-2 flex items-center gap-1.5">
                          <Sparkles size={15} /> Best Practices
                        </h4>
                        <ul className="space-y-1">
                          {reviewResult.best_practices.map((s, i) => (
                            <li key={i} className="flex items-start gap-2 text-sm text-brand-secondary">
                              <span className="mt-0.5 w-1.5 h-1.5 rounded-full bg-purple-400 shrink-0" />
                              {s}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* ============ IMPROVE TAB ============ */}
        {activeTab === "improve" && (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <div className="rounded-2xl border border-brand-primary/10 bg-surface-card p-6 shadow-sm">
                <h3 className="text-sm font-semibold text-brand-primary mb-3">Improve Code</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-medium text-brand-muted mb-1">File</label>
                    {project?.files?.length ? (
                      <select
                        value={selectedFile || ""}
                        onChange={(e) => setSelectedFile(e.target.value)}
                        className="w-full rounded-xl border border-brand-primary/20 px-3 py-2.5 text-sm focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20 outline-none"
                      >
                        {project.files.map((f) => (
                          <option key={f.path} value={f.path}>{f.path}</option>
                        ))}
                      </select>
                    ) : (
                      <input
                        value={selectedFile || "code.txt"}
                        onChange={(e) => setSelectedFile(e.target.value)}
                        className="w-full rounded-xl border border-brand-primary/20 px-3 py-2.5 text-sm focus:border-brand-sky focus:ring-2 focus:ring-brand-sky/20 outline-none"
                      />
                    )}
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-brand-muted mb-2">Focus Area</label>
                    <div className="grid grid-cols-2 gap-2">
                      {ASPECTS.map((a) => (
                        <button
                          key={a.value}
                          onClick={() => setImproveAspect(a.value)}
                          className={`flex items-center gap-2 rounded-xl border px-4 py-3 text-sm transition-all ${
                            improveAspect === a.value
                              ? "border-brand-sky bg-brand-sky/5 text-brand-sky font-medium"
                              : "border-brand-primary/10 text-brand-muted hover:border-brand-primary/20"
                          }`}
                        >
                          <a.icon size={16} className={a.color} />
                          {a.label}
                        </button>
                      ))}
                    </div>
                  </div>

                  <button
                    onClick={handleImprove}
                    disabled={improveLoading}
                    className="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-lg transition-all hover:from-indigo-600 hover:to-purple-500 disabled:opacity-50"
                  >
                    {improveLoading ? <Spinner /> : <Sparkles size={18} />}
                    {improveLoading ? "Improving..." : "Improve Code"}
                  </button>
                </div>
              </div>
            </div>

            <div className="lg:col-span-3">
              {!improveResult ? (
                <div className="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-brand-primary/10 bg-surface-card p-12 text-center">
                  <Sparkles size={48} className="text-gray-300 mb-4" />
                  <h3 className="text-lg font-semibold text-gray-400">AI Code Improvement</h3>
                  <p className="mt-1 text-sm text-gray-400">Select a file and focus area, then click Improve</p>
                </div>
              ) : (
                <div className="rounded-2xl border border-brand-primary/10 bg-surface-card shadow-sm overflow-hidden">
                  <div className="border-b border-brand-primary/5 px-5 py-3">
                    <h3 className="text-sm font-semibold text-brand-primary flex items-center gap-2">
                      <SplitSquareVertical size={16} className="text-purple-500" />
                      Original vs Improved ({improveAspect})
                    </h3>
                  </div>

                  <div className="grid grid-cols-2 divide-x divide-gray-200 min-h-[400px]">
                    <div className="p-4">
                      <div className="text-[10px] font-semibold uppercase tracking-wider text-gray-400 mb-2">Original</div>
                      <pre className="text-xs font-mono leading-relaxed text-brand-secondary whitespace-pre-wrap h-[360px] overflow-y-auto">
                        {currentFile?.content || "No code"}
                      </pre>
                    </div>
                    <div className="p-4">
                      <div className="text-[10px] font-semibold uppercase tracking-wider text-emerald-500 mb-2">Improved</div>
                      <pre className="text-xs font-mono leading-relaxed text-white whitespace-pre-wrap h-[360px] overflow-y-auto">
                        {improveResult.improved_code || "No improvements generated"}
                      </pre>
                    </div>
                  </div>

                  {improveResult.changes?.length > 0 && (
                    <div className="border-t border-brand-primary/5 bg-surface-base/70 px-5 py-4">
                      <h4 className="text-xs font-semibold text-brand-secondary mb-2">Changes Made</h4>
                      <div className="space-y-2">
                        {improveResult.changes.map((c, i) => (
                          <div key={i} className="rounded-lg border border-brand-primary/10 bg-surface-card px-4 py-2.5">
                            <div className="flex items-start gap-2">
                              <ChevronRight size={14} className="mt-0.5 text-purple-500 shrink-0" />
                              <div>
                                <div className="text-sm font-medium text-brand-primary">{c.description}</div>
                                <div className="text-xs text-gray-400 mt-0.5">{c.reason}</div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="border-t border-brand-primary/5 px-5 py-3 flex justify-end">
                    <button
                      onClick={() => {
                        if (currentFile && improveResult?.improved_code) {
                          handleFileEdit(currentFile.path, improveResult.improved_code);
                          setImproveResult(null);
                        }
                      }}
                      className="flex items-center gap-1.5 rounded-lg bg-brand-sky px-4 py-2 text-xs font-semibold text-white hover:bg-blue-600 transition-colors"
                    >
                      <CheckCircle2 size={14} />
                      Apply Changes
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
