// @ts-nocheck
import { useEffect, useState, useCallback } from "react";
import Editor from "@monaco-editor/react";
import { Play, RotateCcw, Loader2, Terminal, ExternalLink, Code2, Copy, Check } from "lucide-react";
import api from "../../services/api";
import { useBrowserRuntime } from "../../hooks/useBrowserRuntime";

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

function toLangId(raw: string | number | undefined) {
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
  hideTitle?: boolean;
};

export default function PracticeConsole({
  language = "python",
  initialCode,
  height = 240,
  onResult,
  title = "Practice Console",
  hideTitle = false,
}: PracticeConsoleProps) {
  const [lang, setLang] = useState(() => toLangId(language));
  const [code, setCode] = useState(initialCode ?? DEFAULT_CODE[toLangId(language)]);
  const [output, setOutput] = useState("");
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);
  const { isBrowserNative, execute: browserExecute } = useBrowserRuntime();


  useEffect(() => {
    const nextLang = toLangId(language);
    setLang(nextLang);
    setCode(initialCode ?? DEFAULT_CODE[nextLang]);
    setOutput("");
    setError("");
  }, [language, initialCode]);

  const reset = () => {
    const nextLang = toLangId(lang);
    setLang(nextLang);
    setCode(initialCode ?? DEFAULT_CODE[nextLang]);
    setOutput("");
    setError("");
    setCopied(false);
  };

  const copyCode = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // clipboard unavailable
    }
  };

  const run = useCallback(async () => {
    setRunning(true);
    setOutput("");
    setError("");
    try {
      if (isBrowserNative(lang)) {
        const result = await browserExecute(lang, code, "", 10000);
        if (result.success) {
          const out = result.stdout || "(no output)";
          setOutput(out);
          onResult?.({ stdout: out, stderr: result.stderr || "", success: true });
        } else {
          const msg = result.stderr || result.compile_error || "Execution failed";
          setError(msg);
          onResult?.({ stdout: "", stderr: msg, success: false });
        }
        return;
      }
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
      const message = err instanceof Error ? err.message : String(err);
      setError(message || "Failed to execute");
      onResult?.({ stdout: "", stderr: message || "Failed to execute", success: false });
    } finally {
      setRunning(false);
    }
  }, [code, lang, onResult, isBrowserNative, browserExecute]);

  return (
    <div className="overflow-hidden rounded-2xl border border-border bg-surface shadow-soft-lg">
      <div className="flex flex-col gap-3 border-b border-border bg-surface-2 px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
        <span className="flex items-center gap-2 text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted">
          <Code2 size={13} className="text-primary" />
          {hideTitle ? "Practice" : title}
        </span>
        <div className="flex flex-wrap items-center gap-2">
          <select
            value={lang}
            onChange={(e) => setLang(e.target.value)}
            className="rounded-lg border border-border bg-surface px-3 py-1.5 text-xs text-text-primary outline-none focus:border-primary/40"
          >
            {LANGS.map((l) => (
              <option key={l.id} value={l.id} className="bg-surface">
                {l.label}
              </option>
            ))}
          </select>
          <button
            onClick={run}
            disabled={running}
            className="flex items-center gap-1.5 rounded-lg border border-primary/20 bg-primary/10 px-3 py-1.5 text-xs font-medium text-primary-dark transition-all hover:bg-primary/15 disabled:opacity-50"
          >
            {running ? <Loader2 size={12} className="animate-spin" /> : <Play size={12} />}
            Run
          </button>
           <button
             onClick={reset}
             className="flex items-center gap-1.5 rounded-lg border border-border bg-surface px-2.5 py-1.5 text-xs font-medium text-text-muted transition-all hover:text-text-primary"
           >
             <RotateCcw size={12} /> Reset
           </button>
           <button
             onClick={copyCode}
             className="flex items-center gap-1 rounded-lg border border-border bg-surface px-2.5 py-1.5 text-xs font-medium text-text-muted transition-all hover:text-text-primary"
             title="Copy code"
           >
             {copied ? <Check size={12} /> : <Copy size={12} />}
           </button>
           <a
             href="/playground"
             className="flex items-center gap-1 rounded-lg border border-ocean/20 bg-ocean-soft px-2.5 py-1.5 text-xs font-medium text-ocean transition-all hover:bg-ocean/10"
             title="Open the full digital playground"
           >
             <ExternalLink size={12} /> Playground
           </a>

        </div>
      </div>

      <div style={{ height }} className="border-b border-border">
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
          <div className="flex items-center gap-1.5 border-t border-border bg-surface-2 px-4 py-2 text-[10px] font-mono uppercase tracking-[0.22em] text-text-muted">
            <Terminal size={11} /> Output
          </div>
          <pre className={`max-h-40 overflow-y-auto whitespace-pre-wrap bg-surface px-4 py-3 text-sm font-mono ${
            error ? "text-coral" : "text-primary"
          }`}>
            {error || output}
          </pre>
        </div>
      )}
    </div>
  );
}
