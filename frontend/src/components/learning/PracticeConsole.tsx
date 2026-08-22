import { useEffect, useState, useCallback } from "react";
import Editor from "@monaco-editor/react";
import { Play, RotateCcw, Loader2, Terminal, ExternalLink, Code2 } from "lucide-react";
import api from "../../services/api";

const LANGS = [
  { id: "c", label: "C", monaco: "c" },
  { id: "cpp", label: "C++", monaco: "cpp" },
  { id: "java", label: "Java", monaco: "java" },
  { id: "python", label: "Python", monaco: "python" },
];

const DEFAULT_CODE = {
  c: `#include <stdio.h>\n\nint main() {\n    printf("Hello, world!\\n");\n    return 0;\n}`,
  cpp: `#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, world!" << endl;\n    return 0;\n}`,
  java: `public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, world!");\n    }\n}`,
  python: `print("Hello, world!")`,
};

function toLangId(raw) {
  const id = String(raw || "").toLowerCase();
  if (id === "cpp" || id === "c++") return "cpp";
  if (id === "java") return "java";
  if (id === "c") return "c";
  return "python";
}

type PracticeConsoleProps = {
  language?: string;
  initialCode?: string;
  height?: number;
  onResult?: (r: { stdout: string; stderr: string; success: boolean }) => void;
  title?: string;
  compact?: boolean;
  hideTitle?: boolean;
};

export default function PracticeConsole({
  language = "python",
  initialCode,
  height = 240,
  onResult,
  title = "Practice Console",
  compact = false,
  hideTitle = false,
}: PracticeConsoleProps) {
  const [lang, setLang] = useState(() => toLangId(language));
  const [code, setCode] = useState(initialCode ?? DEFAULT_CODE[toLangId(language)]);
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const nextLang = toLangId(language);
    setLang(nextLang);
    setCode(initialCode ?? DEFAULT_CODE[nextLang]);
    setOutput("");
    setError("");
  }, [language, initialCode]);

  const reset = () => {
    setCode(initialCode ?? DEFAULT_CODE[lang]);
    setOutput("");
    setError("");
  };

  const run = useCallback(async () => {
    setRunning(true);
    setOutput("");
    setError("");
    try {
      const result = await api.executeCompilerCode({ code, language: lang, stdin: "", timeout: 10 });
      if (result.success) {
        const out = result.stdout || "(no output)";
        setOutput(out);
        onResult?.({ stdout: out, stderr: result.stderr || "", success: true });
      } else {
        const msg = result.stderr || result.compile_error || result.error || "Execution failed";
        setError(msg);
        onResult?.({ stdout: "", stderr: msg, success: false });
      }
    } catch (err) {
      setError(err.message || "Failed to execute");
      onResult?.({ stdout: "", stderr: err.message, success: false });
    } finally {
      setRunning(false);
    }
  }, [code, lang, onResult]);

  return (
    <div className="overflow-hidden rounded-2xl border border-brand-primary/10 bg-surface-card/95 shadow-soft-lg">
      <div className="flex flex-col gap-3 border-b border-brand-primary/10 bg-white/70 px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
        <span className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.22em] text-brand-muted">
          <Code2 size={13} className="text-brand-secondary" />
          {hideTitle ? "Practice" : title}
        </span>
        <div className="flex flex-wrap items-center gap-2">
          <select
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            className="rounded-lg border border-brand-primary/15 bg-white px-3 py-1.5 text-xs text-text-primary focus:outline-none focus:border-brand-secondary/40"
          >
            {LANGS.map((l) => (
              <option key={l.id} value={l.id} className="bg-white">
                {l.label}
              </option>
            ))}
          </select>
          <button
            onClick={run}
            disabled={running}
            className="flex items-center gap-1.5 rounded-lg border border-brand-secondary/20 bg-brand-secondary/10 px-3 py-1.5 text-xs font-mono text-brand-secondary transition-all hover:bg-brand-secondary/15 disabled:opacity-50"
          >
            {running ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />}
            Run
          </button>
          <button
            onClick={reset}
            className="flex items-center gap-1.5 rounded-lg border border-brand-primary/10 bg-white px-2.5 py-1.5 text-xs font-mono text-brand-muted transition-all hover:text-text-primary"
          >
            <RotateCcw size={12} /> Reset
          </button>
          <a
            href="/playground"
            className="flex items-center gap-1 rounded-lg border border-brand-lavender/20 bg-brand-lavender-pale px-2.5 py-1.5 text-xs font-mono text-brand-lavender transition-all hover:bg-brand-lavender/20"
            title="Open the full digital playground"
          >
            <ExternalLink size={12} /> Playground
          </a>
        </div>
      </div>

      <div style={{ height }} className="border-b border-brand-primary/5">
        <Editor
          height="100%"
          language={lang === "cpp" ? "cpp" : lang === "java" ? "java" : lang === "c" ? "c" : "python"}
          theme="vs-dark"
          value={code}
          onChange={(val) => setCode(val || "")}
          options={{
            minimap: { enabled: false },
            fontSize: 13,
            tabSize: 2,
            lineNumbers: "on",
            wordWrap: "on",
            padding: { top: 8 },
            bracketPairColorization: { enabled: true },
            renderLineHighlight: "all",
            smoothScrolling: true,
            cursorBlinking: "smooth",
            cursorSmoothCaretAnimation: "on",
            scrollBeyondLastLine: false,
          }}
        />
      </div>

      {(output || error) && (
        <div>
          <div className="flex items-center gap-1.5 border-t border-brand-primary/5 bg-surface-base px-4 py-2 text-[10px] font-mono uppercase tracking-[0.22em] text-brand-muted">
            <Terminal size={11} /> Output
          </div>
          <pre className={`max-h-40 overflow-y-auto whitespace-pre-wrap bg-surface-base px-4 py-3 text-sm font-mono ${
            error ? "text-brand-coral" : "text-brand-secondary"
          }`}>
            {error || output}
          </pre>
        </div>
      )}
    </div>
  );
}
