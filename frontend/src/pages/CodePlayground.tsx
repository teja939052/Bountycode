import { useState, useRef, useCallback, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Editor from "@monaco-editor/react";
import api from "../services/api";
import {
  Plus, Trash2, Play, RotateCcw, Save, Share2,
  FileCode, Folder, Terminal, RefreshCw, Download,
  Globe, Code2, X, Check, ExternalLink, Sparkles,
  Eye, Moon, Sun, Settings2, ChevronRight, ChevronDown,
  FileText, Image, FileJson, FileType,
} from "lucide-react";

const DEFAULT_PROJECT = {
  name: "my-project",
  files: [
    { id: "1", name: "index.html", language: "html", content: "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n  <title>My Project</title>\n  <link rel=\"stylesheet\" href=\"style.css\">\n</head>\n<body>\n  <h1>Hello, World! ✨</h1>\n  <p>Welcome to your Code Playground.</p>\n  <script src=\"script.js\"></script>\n</body>\n</html>" },
    { id: "2", name: "style.css", language: "css", content: "* { margin: 0; padding: 0; box-sizing: border-box; }\nbody {\n  font-family: system-ui, sans-serif;\n  background: linear-gradient(135deg, #0f0f1a, #1a1a2e);\n  color: #e2e8f0;\n  min-height: 100vh;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n}\nh1 {\n  font-size: 3rem;\n  background: linear-gradient(135deg, #6366f1, #a855f7);\n  -webkit-background-clip: text;\n  -webkit-text-fill-color: transparent;\n}" },
    { id: "3", name: "script.js", language: "javascript", content: "console.log('Hello from Code Playground! 🚀');\n\ndocument.querySelector('h1').addEventListener('click', () => {\n  alert('Welcome to the Playground!');\n});" },
  ],
};

const FILE_ICONS = {
  html: FileType, css: FileType, js: FileCode, javascript: FileCode,
  json: FileJson, py: FileCode, jsx: FileCode, tsx: FileCode,
};

const FILE_COLORS = {
  html: "text-orange-400", css: "text-blue-400", javascript: "text-yellow-400",
  js: "text-yellow-400", json: "text-green-400", py: "text-blue-300",
};

const THEMES = ["vs-dark", "vs-light", "hc-black"];

export default function CodePlayground() {
  const [project, setProject] = useState(DEFAULT_PROJECT);
  const [activeFileId, setActiveFileId] = useState(project.files[0].id);
  const [output, setOutput] = useState("");
  const [consoleOpen, setConsoleOpen] = useState(true);
  const [theme, setTheme] = useState("vs-dark");
  const [previewMode, setPreviewMode] = useState(false);
  const [showNewFile, setShowNewFile] = useState(false);
  const [newFileName, setNewFileName] = useState("");
  const [running, setRunning] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const iframeRef = useRef(null);

  const activeFile = project.files.find((f) => f.id === activeFileId);

  const updateFile = useCallback((fileId, content) => {
    setProject((prev) => ({
      ...prev,
      files: prev.files.map((f) => (f.id === fileId ? { ...f, content } : f)),
    }));
  }, []);

  const addFile = () => {
    if (!newFileName.trim()) return;
    const ext = newFileName.split(".").pop() || "txt";
    const langMap = { html: "html", css: "css", js: "javascript", jsx: "javascript", tsx: "typescript", json: "json", py: "python" };
    const newFile = {
      id: Date.now().toString(),
      name: newFileName.trim(),
      language: langMap[ext] || "plaintext",
      content: "",
    };
    setProject((prev) => ({ ...prev, files: [...prev.files, newFile] }));
    setActiveFileId(newFile.id);
    setNewFileName("");
    setShowNewFile(false);
  };

  const deleteFile = (fileId) => {
    if (project.files.length <= 1) return;
    setProject((prev) => ({
      ...prev,
      files: prev.files.filter((f) => f.id !== fileId),
    }));
    if (activeFileId === fileId) {
      setActiveFileId(project.files.find((f) => f.id !== fileId)?.id || project.files[0].id);
    }
  };

  const runProject = async () => {
    setRunning(true);
    setOutput("Running...\n");

    const htmlFile = project.files.find((f) => f.name.endsWith(".html"));
    if (htmlFile) {
      // Build inline HTML with CSS and JS
      let fullHtml = htmlFile.content;
      project.files.forEach((f) => {
        if (f.name.endsWith(".css")) {
          const styleTag = `<style>\n${f.content}\n</style>`;
          fullHtml = fullHtml.replace("</head>", `${styleTag}\n</head>`);
        }
        if (f.name.endsWith(".js")) {
          const scriptTag = `<script>\n${f.content}\n</script>`;
          fullHtml = fullHtml.replace("</body>", `${scriptTag}\n</body>`);
        }
      });
      if (iframeRef.current) {
        const blob = new Blob([fullHtml], { type: "text/html" });
        iframeRef.current.src = URL.createObjectURL(blob);
      }
      setOutput("✓ Live preview updated\n");
      setRunning(false);
      return;
    }

    // For non-HTML projects, use Piston API
    try {
      const result = await api.executeCompilerCode({
        code: activeFile?.content || "",
        language: activeFile?.language || "python",
        stdin: "",
        timeout: 10,
      });
      if (result.success) {
        setOutput(result.stdout || "✓ Executed successfully (no output)");
        if (result.stderr) setOutput((prev) => prev + "\n⚠ " + result.stderr);
      } else {
        setOutput("✗ Error: " + (result.error || result.stderr || "Execution failed"));
      }
    } catch (err) {
      setOutput("✗ Execution failed: " + (err.message || "Unknown error"));
    }
    setRunning(false);
  };

  const getLanguageForMonaco = (lang) => {
    const map = { html: "html", css: "css", javascript: "javascript", typescript: "typescript", json: "json", python: "python", plaintext: "plaintext" };
    return map[lang] || "plaintext";
  };

  return (
    <div className="h-screen bg-[#f8f5ef] text-text-primary flex flex-col overflow-hidden">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 bg-white border-border/95 border-b border-black/10 shrink-0 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-sm font-medium">
            <Code2 className="w-5 h-5 text-indigo-400" />
            <span className="text-text-primary">{project.name}</span>
          </div>
          <span className="text-[10px] text-brand-muted font-mono">{project.files.length} files</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPreviewMode(!previewMode)}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              previewMode ? "bg-indigo-600 text-text-primary" : "bg-surface-2 text-brand-secondary hover:text-text-primary"
            }`}
          >
            <Eye className="w-3.5 h-3.5" /> Preview
          </button>
          <button
            onClick={runProject}
            disabled={running}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-text-primary text-xs font-medium transition-all shadow-lg shadow-emerald-600/20"
          >
            {running ? <RefreshCw className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 fill-current" />}
            Run
          </button>
          <select
            value={theme}
            onChange={(e) => setTheme(e.target.value)}
            className="bg-white border border-black/10 rounded-lg px-2 py-1.5 text-xs text-text-primary"
          >
            {THEMES.map((t) => (
              <option key={t} value={t}>{t.replace("vs-", "").replace("hc", "high contrast")}</option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex-1 flex min-h-0">
        {/* Sidebar */}
        <div className={`${sidebarOpen ? "w-52" : "w-0"} bg-white border-border/85 border-r border-black/10 flex flex-col transition-all duration-200 shrink-0 overflow-hidden backdrop-blur-sm`}>
          <div className="flex items-center justify-between px-3 py-2 border-b border-black/10">
            <span className="text-[10px] font-semibold text-brand-muted uppercase tracking-wider">Files</span>
            <button
              onClick={() => setShowNewFile(true)}
              className="p-1 rounded hover:bg-surface-2 text-brand-secondary hover:text-text-primary transition-colors"
            >
              <Plus className="w-3.5 h-3.5" />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-1 space-y-0.5">
            {project.files.map((file) => {
              const ext = file.name.split(".").pop() || "";
              const IconComp = FILE_ICONS[ext] || FILE_ICONS[file.language] || FileCode;
              const color = FILE_COLORS[ext] || FILE_COLORS[file.language] || "text-slate-400";
              return (
                <div
                  key={file.id}
                  onClick={() => setActiveFileId(file.id)}
                  className={`group flex items-center gap-2 px-3 py-2 rounded-lg cursor-pointer text-xs transition-all ${
                    activeFileId === file.id
                      ? "bg-indigo-600/20 text-indigo-300 border border-indigo-500/30"
                      : "text-brand-secondary hover:bg-surface-2 hover:text-text-primary"
                  }`}
                >
                  <IconComp className={`w-3.5 h-3.5 ${color}`} />
                  <span className="flex-1 truncate">{file.name}</span>
                  <button
                    onClick={(e) => { e.stopPropagation(); deleteFile(file.id); }}
                    className="opacity-0 group-hover:opacity-100 p-0.5 rounded hover:bg-surface-2 text-brand-muted hover:text-red-400 transition-all"
                  >
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              );
            })}
          </div>
          {showNewFile && (
            <div className="p-2 border-t border-black/10">
              <input
                autoFocus
                value={newFileName}
                onChange={(e) => setNewFileName(e.target.value)}
                onKeyDown={(e) => { if (e.key === "Enter") addFile(); if (e.key === "Escape") setShowNewFile(false); }}
                placeholder="filename.html"
                className="w-full bg-white border border-black/10 rounded px-2 py-1.5 text-xs text-text-primary placeholder-brand-muted focus:outline-none focus:border-indigo-500/50"
              />
              <div className="flex items-center gap-1 mt-1.5">
                <button onClick={addFile} className="flex-1 py-1 bg-indigo-600 text-text-primary rounded text-[10px] font-medium">Add</button>
                <button onClick={() => setShowNewFile(false)} className="py-1 px-2 bg-surface-2 text-brand-secondary rounded text-[10px]">Cancel</button>
              </div>
            </div>
          )}
        </div>

        {/* Editor + Preview */}
        <div className="flex-1 flex min-h-0">
          <div className={`${previewMode ? "w-0" : "flex-1"} flex flex-col transition-all duration-200 overflow-hidden`}>
            <div className="flex-1 min-h-0">
              {activeFile && (
                <Editor
                  key={activeFile.id}
                  height="100%"
                  language={getLanguageForMonaco(activeFile.language)}
                  theme={theme}
                  value={activeFile.content}
                  onChange={(val) => updateFile(activeFile.id, val || "")}
                  options={{
                    fontSize: 13,
                    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
                    minimap: { enabled: false },
                    scrollBeyondLastLine: false,
                    lineNumbers: "on",
                    renderWhitespace: "selection",
                    tabSize: 2,
                    automaticLayout: true,
                    bracketPairColorization: { enabled: true },
                    padding: { top: 12 },
                  }}
                />
              )}
            </div>
          </div>

          {/* Preview panel */}
          <AnimatePresence>
            {previewMode && (
              <motion.div
                initial={{ width: 0, opacity: 0 }}
                animate={{ width: "50%", opacity: 1 }}
                exit={{ width: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="border-l border-black/10 flex flex-col bg-white"
              >
                <div className="flex items-center justify-between px-3 py-1.5 bg-surface-2 border-b border-black/10 shrink-0">
                  <span className="text-[10px] font-semibold text-brand-muted uppercase tracking-wider flex items-center gap-1.5">
                    <Globe className="w-3 h-3" /> Live Preview
                  </span>
                  <button onClick={() => setPreviewMode(false)} className="p-1 rounded hover:bg-surface-2 text-brand-muted transition-colors">
                    <X className="w-3 h-3" />
                  </button>
                </div>
                <div className="flex-1 min-h-0">
                  <iframe
                    ref={iframeRef}
                    className="w-full h-full border-0"
                    title="Preview"
                    sandbox="allow-scripts allow-same-origin"
                  />
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Console */}
      <div className={`${consoleOpen ? "h-36" : "h-8"} bg-white border-t border-black/10 shrink-0 transition-all duration-200 shadow-[0_-1px_0_rgba(0,0,0,0.04)]`}>
        <div
          onClick={() => setConsoleOpen(!consoleOpen)}
          className="flex items-center justify-between px-4 py-1.5 cursor-pointer hover:bg-surface-2"
        >
          <span className="text-[10px] font-semibold text-brand-muted uppercase tracking-wider flex items-center gap-1.5">
            <Terminal className="w-3 h-3" /> Console
          </span>
          <div className="flex items-center gap-2">
            <button onClick={(e) => { e.stopPropagation(); runProject(); }} className="text-[10px] text-brand-secondary hover:text-text-primary px-2 py-0.5 rounded bg-surface-2">
              Clear
            </button>
            {consoleOpen ? <ChevronDown className="w-3 h-3 text-brand-muted" /> : <ChevronRight className="w-3 h-3 text-brand-muted" />}
          </div>
        </div>
        {consoleOpen && (
          <div className="p-3 font-mono text-xs text-text-primary overflow-y-auto h-[calc(100%-28px)] whitespace-pre-wrap">
            {output || "Click Run to execute your code..."}
          </div>
        )}
      </div>
    </div>
  );
}
