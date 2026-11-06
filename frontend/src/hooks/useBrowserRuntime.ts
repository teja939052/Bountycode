import { useState, useCallback } from "react";

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
const MAX_BROWSER_CODE_CHARS = 20_000;
const MAX_OUTPUT_CHARS = 20_000;
const PYODIDE_VERSION = "0.23.4";
const PYODIDE_BASE_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

function failure(stderr: string, exitCode = 1): BrowserRunResult {
  return { success: false, stdout: "", stderr, exit_code: exitCode, source: "browser" };
}

/**
 * Python runs in a disposable Worker, not the application's window. This
 * removes direct access to the DOM, localStorage and page authentication state.
 * Network/worker APIs are disabled after Pyodide initializes. This is a
 * formative low-cost runner only; server-side grading remains authoritative.
 */
function runPythonInWorker(
  code: string,
  stdin: string,
  timeoutMs: number,
  onReady: () => void,
): Promise<BrowserRunResult> {
  if (typeof Worker === "undefined" || typeof window === "undefined") {
    return Promise.resolve(failure("This browser does not support the isolated Python runner."));
  }
  if (code.length > MAX_BROWSER_CODE_CHARS) {
    return Promise.resolve(failure("This exercise is too large to run in the browser."));
  }

  const workerSource = `
    const send = self.postMessage.bind(self);
    const baseUrl = ${JSON.stringify(PYODIDE_BASE_URL)};
    const maxOutput = ${MAX_OUTPUT_CHARS};
    let pyodide;
    const append = (current, value) => (current + String(value)).slice(0, maxOutput);

    async function initialize() {
      importScripts(baseUrl + "pyodide.js");
      pyodide = await self.loadPyodide({ indexURL: baseUrl });

      // Learner code executes only after the runtime has loaded and the
      // network/worker APIs have been removed from its Worker global.
      for (const key of [
        "fetch", "XMLHttpRequest", "WebSocket", "EventSource",
        "BroadcastChannel", "SharedWorker", "Worker", "importScripts",
        "MessageChannel", "WebTransport", "caches", "indexedDB"
      ]) {
        try {
          Object.defineProperty(self, key, {
            value: undefined, writable: false, configurable: false
          });
        } catch (_) {}
      }
      try {
        Object.defineProperty(self, "postMessage", {
          value: undefined, writable: false, configurable: false
        });
      } catch (_) {}

      self.addEventListener("message", async ({ data }) => {
        let stdout = "";
        let stderr = "";
        pyodide.setStdout({ batched: (value) => { stdout = append(stdout, value + "\\n"); } });
        pyodide.setStderr({ batched: (value) => { stderr = append(stderr, value + "\\n"); } });
        try {
          pyodide.globals.set("__bountycode_stdin", String(data.stdin || ""));
          pyodide.runPython(
            "import sys\\nfrom io import StringIO\\nsys.stdin = StringIO(__bountycode_stdin)"
          );
          pyodide.globals.delete("__bountycode_stdin");
          await pyodide.runPythonAsync(String(data.code || ""));
          send({ type: "result", success: true, stdout: stdout.trimEnd(), stderr: "" });
        } catch (error) {
          send({
            type: "result",
            success: false,
            stdout: stdout.trimEnd(),
            stderr: append(stderr, String(error && error.message || error)).slice(0, 5000)
          });
        }
      });
      send({ type: "ready" });
    }

    initialize().catch((error) => {
      send({ type: "load_error", error: String(error && error.message || error).slice(0, 5000) });
    });
  `;

  let worker: Worker;
  let objectUrl = "";
  try {
    objectUrl = URL.createObjectURL(new Blob([workerSource], { type: "text/javascript" }));
    worker = new Worker(objectUrl, { name: "bountycode-python-runner" });
  } catch (error: any) {
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    return Promise.resolve(failure(error?.message || "Could not start the Python runner."));
  }

  return new Promise((resolve) => {
    let settled = false;
    let executionTimer: number | undefined;
    const startedAt = performance.now();
    const loadTimer = window.setTimeout(() => {
      finish(failure("Python runtime initialization timed out. Check your connection and retry.", -1));
    }, 20_000);

    const finish = (result: BrowserRunResult) => {
      if (settled) return;
      settled = true;
      window.clearTimeout(loadTimer);
      if (executionTimer !== undefined) window.clearTimeout(executionTimer);
      worker.terminate();
      URL.revokeObjectURL(objectUrl);
      resolve({
        ...result,
        execution_time: Number(((performance.now() - startedAt) / 1000).toFixed(3)),
        memory_usage: 0,
        source: "browser",
      });
    };

    worker.onmessage = (event: MessageEvent) => {
      const message = event.data || {};
      if (message.type === "ready") {
        onReady();
        executionTimer = window.setTimeout(() => {
          finish(failure("Execution timed out. Check for an infinite loop and try again.", -1));
        }, Math.max(250, Math.min(timeoutMs, 10_000)));
        worker.postMessage({ code, stdin });
      } else if (message.type === "load_error") {
        finish(failure(message.error || "Failed to load the Python runtime."));
      } else if (message.type === "result") {
        finish({
          success: Boolean(message.success),
          stdout: String(message.stdout || "").slice(0, MAX_OUTPUT_CHARS),
          stderr: String(message.stderr || "").slice(0, 5_000),
          exit_code: message.success ? 0 : 1,
          source: "browser",
        });
      }
    };
    worker.onerror = (event) => {
      finish(failure(event.message || "The Python runner stopped unexpectedly."));
    };
  });
}

function runJavaScriptInWorker(code: string, timeoutMs: number): Promise<BrowserRunResult> {
  if (typeof Worker === "undefined" || typeof window === "undefined") {
    return Promise.resolve(failure("This browser does not support the isolated code runner."));
  }
  if (code.length > MAX_BROWSER_CODE_CHARS) {
    return Promise.resolve(failure("This exercise is too large to run in the browser."));
  }

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
    return Promise.resolve(failure(error?.message || "Could not start the browser runner."));
  }

  return new Promise((resolve) => {
    let settled = false;
    const startedAt = performance.now();
    const timer = window.setTimeout(() => {
      finish(failure("Execution timed out. Check for an infinite loop and try again.", -1));
    }, Math.max(250, Math.min(timeoutMs, 5_000)));

    const finish = (result: BrowserRunResult) => {
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

    worker.onmessage = (event: MessageEvent) => {
      const message = event.data || {};
      finish({
        success: Boolean(message.success),
        stdout: String(message.stdout || ""),
        stderr: String(message.stderr || ""),
        exit_code: message.success ? 0 : 1,
        source: "browser",
      });
    };
    worker.onerror = (event) => {
      finish(failure(event.message || "The browser runner stopped unexpectedly."));
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

  const executePython = useCallback(
    async (code: string, stdin = "", timeoutMs = 5_000): Promise<BrowserRunResult> => {
      const result = await runPythonInWorker(code, stdin, timeoutMs, () => {
        setPyodideReady(true);
        setPyodideError(null);
      });
      if (!result.success) setPyodideError(result.stderr);
      return result;
    },
    [],
  );

  const executeJavaScript = useCallback(
    async (code: string, _stdin = "", timeoutMs = 5_000): Promise<BrowserRunResult> => {
      return runJavaScriptInWorker(code, timeoutMs);
    },
    [],
  );

  const execute = useCallback(
    async (language: string, code: string, stdin = "", timeoutMs = 5_000): Promise<BrowserRunResult> => {
      const normalized = language.toLowerCase();
      if (normalized === "python") return executePython(code, stdin, timeoutMs);
      if (normalized === "javascript" || normalized === "js") {
        return executeJavaScript(code, stdin, timeoutMs);
      }
      return failure(`Browser execution is not supported for ${language}. Use the backend executor.`);
    },
    [executePython, executeJavaScript],
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
