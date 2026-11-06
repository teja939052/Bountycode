import { useState, useCallback, useRef } from "react";

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

const BROWSER_LANGUAGES = new Set(["python", "javascript"]);

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

const MAX_BROWSER_CODE_CHARS = 20_000;

function runJavaScriptInWorker(code: string, timeoutMs: number): Promise<BrowserRunResult> {
  if (typeof Worker === "undefined" || typeof window === "undefined") {
    return Promise.resolve({
      success: false,
      stdout: "",
      stderr: "This browser does not support the isolated code runner.",
      exit_code: 1,
      source: "browser",
    });
  }
  if (code.length > MAX_BROWSER_CODE_CHARS) {
    return Promise.resolve({
      success: false,
      stdout: "",
      stderr: "This exercise is too large to run in the browser.",
      exit_code: 1,
      source: "browser",
    });
  }

  // Worker code has no DOM, cookies or localStorage. Network-facing APIs are
  // disabled for this educational runner; server submissions remain separate.
  const workerSource = [
    "const send = self.postMessage.bind(self);",
    "const lines = [];",
    "const stringify = (value) => {",
    "  if (typeof value === 'string') return value;",
    "  try { const json = JSON.stringify(value); return json === undefined ? String(value) : json; }",
    "  catch (_) { return String(value); }",
    "};",
    "const write = (...args) => {",
    "  const current = lines.join('\\n').length;",
    "  const remaining = 20000 - current;",
    "  if (remaining > 0) lines.push(args.map(stringify).join(' ').slice(0, remaining));",
    "};",
    "const safeConsole = { log: write, info: write, warn: write, error: write, debug: write, clear: () => { lines.length = 0; } };",
    "for (const key of ['fetch','XMLHttpRequest','WebSocket','EventSource','BroadcastChannel','SharedWorker','Worker','importScripts','MessageChannel']) {",
    "  try { Object.defineProperty(self, key, { value: undefined, writable: false, configurable: false }); } catch (_) {}",
    "}",
    "try { Object.defineProperty(self, 'console', { value: safeConsole, writable: false, configurable: false }); } catch (_) { self.console = safeConsole; }",
    "self.onmessage = async ({ data }) => {",
    "  try {",
    "    const AsyncFunction = Object.getPrototypeOf(async function () {}).constructor;",
    "    const run = new AsyncFunction('console', data.code);",
    "    const returned = await run(safeConsole);",
    "    if (returned !== undefined) write(returned);",
    "    send({ type: 'result', success: true, stdout: lines.join('\\n').slice(0, 20000), stderr: '' });",
    "  } catch (error) {",
    "    send({ type: 'result', success: false, stdout: lines.join('\\n').slice(0, 20000), stderr: String(error && error.message || error).slice(0, 5000) });",
    "  }",
    "};",
  ].join("\n");

  let worker: Worker;
  let objectUrl = "";
  try {
    objectUrl = URL.createObjectURL(new Blob([workerSource], { type: "text/javascript" }));
    worker = new Worker(objectUrl, { name: "bountycode-learning-runner" });
  } catch (error: any) {
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    return Promise.resolve({
      success: false,
      stdout: "",
      stderr: error?.message || "Could not start the browser runner.",
      exit_code: 1,
      source: "browser",
    });
  }

  return new Promise((resolve) => {
    let settled = false;
    const startedAt = performance.now();
    const finish = (result: Omit<BrowserRunResult, "source">) => {
      if (settled) return;
      settled = true;
      window.clearTimeout(timer);
      worker.terminate();
      URL.revokeObjectURL(objectUrl);
      resolve({
        ...result,
        execution_time: Number(((performance.now() - startedAt) / 1000).toFixed(3)),
        memory_usage: 0,
        source: "browser",
      });
    };
    const timer = window.setTimeout(() => {
      finish({
        success: false,
        stdout: "",
        stderr: "Execution timed out. Check for an infinite loop and try again.",
        exit_code: -1,
      });
    }, Math.max(250, Math.min(timeoutMs, 5000)));

    worker.onmessage = (event: MessageEvent) => {
      const message = event.data || {};
      finish({
        success: Boolean(message.success),
        stdout: String(message.stdout || ""),
        stderr: String(message.stderr || ""),
        exit_code: message.success ? 0 : 1,
      });
    };
    worker.onerror = (event) => {
      finish({
        success: false,
        stdout: "",
        stderr: event.message || "The browser runner stopped unexpectedly.",
        exit_code: 1,
      });
    };
    worker.postMessage({ code });
  });
}

export function isBrowserNativeLanguage(language: string): boolean {
  return BROWSER_LANGUAGES.has(language.toLowerCase());
}

export function useBrowserRuntime() {
  const [pyodideReady, setPyodideReady] = useState(false);
  const [pyodideError, setPyodideError] = useState<string | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  // Pyodide is loaded only after a learner chooses to run Python. Opening
  // a JavaScript or reading lesson should not download the Python runtime.

  const executePython = useCallback(
    async (code: string, stdin = "", timeoutMs = 5000): Promise<BrowserRunResult> => {
      if (abortRef.current) abortRef.current.abort();
      const controller = new AbortController();
      abortRef.current = controller;

      const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

      try {
        const pyodide = await getPyodide();
        setPyodideReady(true);
        setPyodideError(null);

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
        setPyodideReady(false);
        setPyodideError(message);
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
      return runJavaScriptInWorker(code, timeoutMs);
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
