import { useState, useEffect, useCallback, useRef } from "react";

export interface BrowserRunResult {
  success: boolean;
  stdout: string;
  stderr: string;
  compile_error?: string;
  exit_code?: number;
  execution_time?: number;
  memory_usage?: number;
  source: "browser";
}

const BROWSER_LANGUAGES = new Set(["python", "javascript", "typescript"]);

let pyodideInstance: any = null;
let pyodideLoading: Promise<any> | null = null;

async function getPyodide() {
  if (pyodideInstance) return pyodideInstance;
  if (pyodideLoading) return pyodideLoading;

  // Pyodide loads from CDN at runtime (no npm dependency on purpose: the
  // package is ~10MB and the hook already pins a CDN indexURL). A bare
  // "pyodide" specifier breaks the production bundle (nothing to resolve),
  // so import the full CDN URL, which bundlers leave alone. Callers already
  // handle load failure via pyodideReady/pyodideError and fall back to
  // server execution.
  // @ts-ignore - pyodide CDN module is not in node_modules
  pyodideLoading = import("https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js")
    .then(async (mod: unknown) => {
      const loadPyodide =
        (mod as { loadPyodide?: unknown }).loadPyodide ??
        (window as unknown as { loadPyodide?: unknown }).loadPyodide;
      if (typeof loadPyodide !== "function") throw new Error("pyodide loader unavailable");
      const pyodide = await (loadPyodide as (opts?: { indexURL?: string }) => Promise<unknown>)({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.23.4/full/",
      });
      pyodideInstance = pyodide;
      return pyodide;
    })
    .catch((err) => {
      pyodideLoading = null;
      throw err;
    });

  return pyodideLoading;
}

export function isBrowserNativeLanguage(language: string): boolean {
  return BROWSER_LANGUAGES.has(language.toLowerCase());
}

export function useBrowserRuntime() {
  const [pyodideReady, setPyodideReady] = useState(false);
  const [pyodideError, setPyodideError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => {
    let cancelled = false;
    getPyodide()
      .then(() => {
        if (!cancelled) {
          setPyodideReady(true);
          setPyodideError(null);
        }
      })
      .catch((err) => {
        if (!cancelled) {
          setPyodideReady(false);
          setPyodideError(err?.message || "Failed to load browser runtime");
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const executePython = useCallback(
    async (code: string, stdin = "", timeoutMs = 5000): Promise<BrowserRunResult> => {
      if (abortRef.current) abortRef.current.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

      try {
        const pyodide = await getPyodide();

        if (stdin.trim()) {
          pyodide.runPython(`
import sys
from io import StringIO
sys.stdin = StringIO("${stdin.replace(/"/g, '\\"').replace(/\n/g, "\\n")}")
          `);
        }

        let stdoutText = "";
        pyodide.setStdout({
          batched: (msg: string) => {
            stdoutText += msg + "\n";
          },
        });

        pyodide.setStderr({
          batched: (msg: string) => {
            if (!stdoutText.includes(msg)) stdoutText += msg + "\n";
          },
        });

        await pyodide.runPythonAsync(code, { signal: controller.signal });
        clearTimeout(timeoutId);

        return {
          success: true,
          stdout: stdoutText.trim(),
          stderr: "",
          exit_code: 0,
          execution_time: 0,
          memory_usage: 0,
          source: "browser",
        };
      } catch (err: any) {
        clearTimeout(timeoutId);
        const message = err?.message || String(err);
        const isAbort = err?.name === "AbortError";

        return {
          success: false,
          stdout: "",
          stderr: isAbort ? "Execution timed out" : message,
          compile_error: "",
          exit_code: isAbort ? -1 : 1,
          execution_time: timeoutMs / 1000,
          memory_usage: 0,
          source: "browser",
        };
      } finally {
        if (abortRef.current === controller) abortRef.current = null;
      }
    },
    []
  );

  const executeJavaScript = useCallback(
    async (code: string, _stdin = "", timeoutMs = 5000): Promise<BrowserRunResult> => {
      if (abortRef.current) abortRef.current.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      const timeoutPromise = new Promise<never>((_, reject) => {
        const id = setTimeout(() => {
          controller.abort();
          reject(new Error("Execution timed out"));
        }, timeoutMs);
        controller.signal.addEventListener("abort", () => clearTimeout(id), { once: true });
      });

      try {
        const result = await Promise.race([
          new Promise<BrowserRunResult>((resolve) => {
            const originalLog = console.log;
            const originalError = console.error;
            const originalWarn = console.warn;
            const logs: string[] = [];
            console.log = (...args: any[]) => {
              logs.push(args.map(String).join(" "));
            };
            console.error = (...args: any[]) => {
              logs.push(args.map(String).join(" "));
            };
            console.warn = (...args: any[]) => {
              logs.push(args.map(String).join(" "));
            };

            try {
              const fn = new Function(code);
              fn();
              resolve({
                success: true,
                stdout: logs.join("\n").trim(),
                stderr: "",
                exit_code: 0,
                execution_time: 0,
                memory_usage: 0,
                source: "browser",
              });
            } catch (err: any) {
              resolve({
                success: false,
                stdout: logs.join("\n").trim(),
                stderr: err?.message || String(err),
                compile_error: "",
                exit_code: 1,
                execution_time: 0,
                memory_usage: 0,
                source: "browser",
              });
            } finally {
              console.log = originalLog;
              console.error = originalError;
              console.warn = originalWarn;
            }
          }),
          timeoutPromise,
        ]);

        return result as BrowserRunResult;
      } catch (err: any) {
        return {
          success: false,
          stdout: "",
          stderr: err?.message || "Execution failed",
          compile_error: "",
          exit_code: -1,
          execution_time: timeoutMs / 1000,
          memory_usage: 0,
          source: "browser",
        };
      } finally {
        if (abortRef.current === controller) abortRef.current = null;
      }
    },
    []
  );

  const execute = useCallback(
    async (
      language: string,
      code: string,
      stdin = "",
      timeoutMs = 5000
    ): Promise<BrowserRunResult> => {
      const normalized = language.toLowerCase();

      if (normalized === "python") {
        return executePython(code, stdin, timeoutMs);
      }

      if (normalized === "javascript" || normalized === "js") {
        return executeJavaScript(code, stdin, timeoutMs);
      }

      return {
        success: false,
        stdout: "",
        stderr: `Browser execution is not supported for ${language}. Use the backend executor.`,
        compile_error: "",
        exit_code: 1,
        source: "browser",
      };
    },
    [executePython, executeJavaScript]
  );

  return {
    pyodideReady,
    pyodideError,
    isBrowserNative: (language: string) => isBrowserNativeLanguage(language),
    execute,
    executePython,
    executeJavaScript,
  };
}
