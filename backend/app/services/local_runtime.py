"""
Local Runtime — Pyodide (Python) + Web Worker (JavaScript)
Runs in the BROWSER, not on the server. Server only provides the worker code.
"""

# ──────────────────────────────────────────────────────────────────
# Backend provides worker initialization code
# ──────────────────────────────────────────────────────────────────

PYODIDE_WORKER_JS = r"""
// Pyodide Worker for Python Execution
// This runs in a dedicated Web Worker

let pyodide = null;
let pyodideReady = false;
const pendingRequests = new Map();

self.onmessage = async function(e) {
    const { type, id, payload } = e.data;

    if (type === 'init') {
        await initPyodide(payload.pyodideUrl, payload.packages);
        self.postMessage({ type: 'ready', id });
        return;
    }

    if (!pyodideReady) {
        pendingRequests.set(id, { resolve: null, reject: null });
        // Wait for init
        await new Promise((resolve, reject) => {
            pendingRequests.set(id, { resolve, reject });
        });
    }

    if (type === 'execute') {
        try {
            const result = await executePython(payload.code, payload.stdin, payload.timeout);
            self.postMessage({ type: 'result', id, success: true, result });
        } catch (err) {
            self.postMessage({ type: 'result', id, success: false, error: err.message });
        }
    }
};

async function initPyodide(pyodideUrl, packages) {
    try {
        // Load Pyodide
        importScripts(pyodideUrl);
        pyodide = await loadPyodide({
            indexURL: pyodideUrl.replace('pyodide.js', ''),
        });

        // Load requested packages
        if (packages && packages.length > 0) {
            await pyodide.loadPackage(packages);
        }

        // Pre-load common modules
        await pyodide.loadPackage(['micropip']);
        
        pyodideReady = true;

        // Resolve pending requests
        for (const [id, { resolve }] of pendingRequests) {
            resolve();
        }
        pendingRequests.clear();

    } catch (err) {
        console.error('Pyodide init failed:', err);
        for (const [id, { reject }] of pendingRequests) {
            reject(err);
        }
        pendingRequests.clear();
        throw err;
    }
}

async function executePython(code, stdin, timeout) {
    if (!pyodide) throw new Error('Pyodide not initialized');

    // Set up stdin capture
    const stdinData = stdin || '';
    let inputIndex = 0;

    pyodide.stdin = () => {
        if (inputIndex >= stdinData.length) return null;
        const char = stdinData[inputIndex++];
        return char.charCodeAt(0);
    };

    // Capture stdout/stderr
    let stdout = '';
    let stderr = '';

    const originalStdout = pyodide.stdout;
    const originalStderr = pyodide.stderr;

    pyodide.stdout = (text) => { stdout += text; };
    pyodide.stderr = (text) => { stderr += text; };

    try {
        // Execute with timeout
        const executePromise = pyodide.runPythonAsync(code);
        
        const timeoutPromise = new Promise((_, reject) => {
            setTimeout(() => reject(new Error('Execution timed out')), timeout || 5000);
        });

        await Promise.race([executePromise, timeoutPromise]);

        return {
            stdout: stdout,
            stderr: stderr,
            success: true,
        };

    } catch (err) {
        return {
            stdout: stdout,
            stderr: stderr + '\n' + err.message,
            success: false,
            error: err.message,
        };

    } finally {
        pyodide.stdout = originalStdout;
        pyodide.stderr = originalStderr;
    }
}
"""

JAVASCRIPT_WORKER_JS = r"""
// JavaScript Worker for JS Execution
// Runs student JS in isolated Worker context

const MAX_EXECUTION_TIME = 5000; // 5 seconds
const MAX_OUTPUT_LENGTH = 10000;

self.onmessage = function(e) {
    const { type, id, payload } = e.data;

    if (type === 'execute') {
        executeJS(payload.code, payload.stdin, payload.timeout)
            .then(result => {
                self.postMessage({ type: 'result', id, success: true, result });
            })
            .catch(err => {
                self.postMessage({ type: 'result', id, success: false, error: err.message });
            });
    }
};

async function executeJS(code, stdin, timeout) {
    // Strict mode
    const strictCode = '"use strict";\n' + code;
    
    // Wrap in async function for timeout
    const wrappedCode = `
        (async () => {
            const input = ${JSON.stringify(stdin || '')};
            let inputIndex = 0;
            
            // Mock console
            const logs = [];
            const errors = [];
            const originalLog = console.log;
            const originalError = console.error;
            console.log = (...args) => logs.push(args.map(String).join(' '));
            console.error = (...args) => errors.push(args.map(String).join(' '));
            
            // Mock prompt/alert
            window.prompt = () => input;
            window.alert = (msg) => logs.push('alert: ' + msg);
            
            try {
                ${strictCode}
            } catch (err) {
                errors.push(err.message);
            } finally {
                console.log = originalLog;
                console.error = originalError;
                return { logs, errors };
            }
        })()
    `;

    // Execute with timeout
    const startTime = Date.now();
    
    try {
        // Use Function constructor for sandboxed execution
        const fn = new Function(wrappedCode);
        const result = await Promise.race([
            fn(),
            new Promise((_, reject) => 
                setTimeout(() => reject(new Error('Execution timed out')), timeout || MAX_EXECUTION_TIME)
            )
        ]);

        const executionTime = Date.now() - startTime;
        
        // Truncate output
        const stdout = (result.logs || []).join('\n').slice(0, MAX_OUTPUT_LENGTH);
        const stderr = (result.errors || []).join('\n').slice(0, MAX_OUTPUT_LENGTH);

        return {
            stdout,
            stderr,
            executionTime,
            success: stderr === '',
        };

    } catch (err) {
        return {
            stdout: '',
            stderr: err.message,
            executionTime: Date.now() - startTime,
            success: false,
            error: err.message,
        };
    }
}
"""

# ──────────────────────────────────────────────────────────────────
# Frontend Runtime Service (TypeScript)
# ──────────────────────────────────────────────────────────────────

RUNTIME_SERVICE_TS = r"""
// frontend/src/services/localRuntime.ts

type ExecutionResult = {
  success: boolean;
  stdout: string;
  stderr: string;
  executionTime?: number;
  error?: string;
};

type WorkerMessage = 
  | { type: 'init'; id: string; payload: { pyodideUrl: string; packages: string[] } }
  | { type: 'execute'; id: string; payload: { code: string; stdin: string; timeout: number } }
  | { type: 'result'; id: string; success: boolean; result?: ExecutionResult; error?: string };

class LocalRuntime {
  private pythonWorker: Worker | null = null;
  private jsWorker: Worker | null = null;
  private pendingPython = new Map<string, (result: ExecutionResult) => void>();
  private pendingJS = new Map<string, (result: ExecutionResult) => void>();
  private pythonReady = false;
  private jsReady = false;

  constructor() {
    if (typeof window !== 'undefined') {
      this.initWorkers();
    }
  }

  private initWorkers() {
    // Python Worker (Pyodide)
    this.pythonWorker = new Worker(new URL('./workers/python.worker.ts', import.meta.url), { type: 'module' });
    this.pythonWorker.onmessage = (e: MessageEvent<WorkerMessage>) => this.handlePythonMessage(e.data);

    // JavaScript Worker
    this.jsWorker = new Worker(new URL('./workers/js.worker.ts', import.meta.url), { type: 'module' });
    this.jsWorker.onmessage = (e: MessageEvent<WorkerMessage>) => this.handleJSMessage(e.data);
  }

  private handlePythonMessage(msg: WorkerMessage) {
    if (msg.type === 'ready') {
      this.pythonReady = true;
      // Resolve any pending init
    } else if (msg.type === 'result') {
      const resolver = this.pendingPython.get(msg.id);
      if (resolver) {
        this.pendingPython.delete(msg.id);
        resolver(msg.result || { success: false, stdout: '', stderr: msg.error || 'Unknown error' });
      }
    }
  }

  private handleJSMessage(msg: WorkerMessage) {
    if (msg.type === 'result') {
      const resolver = this.pendingJS.get(msg.id);
      if (resolver) {
        this.pendingJS.delete(msg.id);
        resolver(msg.result || { success: false, stdout: '', stderr: msg.error || 'Unknown error' });
      }
    }
  }

  async initPython(packages: string[] = []) {
    if (!this.pythonWorker || this.pythonReady) return;
    
    const pyodideUrl = '/pyodide/pyodide.js'; // Served from public folder
    
    return new Promise<void>((resolve, reject) => {
      const id = crypto.randomUUID();
      this.pendingPython.set(id, (result) => {
        if (result.success) {
          this.pythonReady = true;
          resolve();
        } else {
          reject(new Error(result.stderr || 'Pyodide init failed'));
        }
      });
      
      this.pythonWorker!.postMessage({
        type: 'init',
        id,
        payload: { pyodideUrl, packages }
      });
    });
  }

  async executePython(code: string, stdin: string = '', timeout: number = 5000): Promise<ExecutionResult> {
    if (!this.pythonWorker) throw new Error('Python worker not initialized');
    if (!this.pythonReady) await this.initPython();

    return new Promise((resolve) => {
      const id = crypto.randomUUID();
      this.pendingPython.set(id, resolve);
      this.pythonWorker!.postMessage({
        type: 'execute',
        id,
        payload: { code, stdin, timeout }
      });
    });
  }

  async executeJavaScript(code: string, stdin: string = '', timeout: number = 5000): Promise<ExecutionResult> {
    if (!this.jsWorker) throw new Error('JS worker not initialized');

    return new Promise((resolve) => {
      const id = crypto.randomUUID();
      this.pendingJS.set(id, resolve);
      this.jsWorker!.postMessage({
        type: 'execute',
        id,
        payload: { code, stdin, timeout }
      });
    });
  }

  isPythonReady() { return this.pythonReady; }
  isJSReady() { return this.jsReady; }
}

export const localRuntime = new LocalRuntime();
"""

# ──────────────────────────────────────────────────────────────────
# Backend Route for Runtime Worker Files
# ──────────────────────────────────────────────────────────────────

RUNTIME_ROUTE_PY = r'''
from fastapi import APIRouter, Response
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/api/v1/runtime", tags=["local-runtime"])

@router.get("/workers/python.worker.js")
async def get_python_worker():
    """Serve Pyodide worker JavaScript."""
    from app.services.local_runtime import PYODIDE_WORKER_JS
    return PlainTextResponse(PYODIDE_WORKER_JS, media_type="application/javascript")

@router.get("/workers/js.worker.js")
async def get_js_worker():
    """Serve JavaScript worker."""
    from app.services.local_runtime import JAVASCRIPT_WORKER_JS
    return PlainTextResponse(JAVASCRIPT_WORKER_JS, media_type="application/javascript")

@router.get("/pyodide/{path:path}")
async def get_pyodide_file(path: str):
    """Proxy Pyodide files from CDN or local static."""
    # In production, serve from local static or CDN
    # For now, redirect to CDN
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"https://cdn.jsdelivr.net/pyodide/v0.25.1/full/{path}")
'''

print("Local Runtime service created.")
print("Files needed:")
print("  - backend/app/services/local_runtime.py (this file)")
print("  - backend/app/routes/runtime.py (serves worker files)")
print("  - frontend/src/services/localRuntime.ts (TypeScript client)")
print("  - frontend/public/pyodide/ (Pyodide files for offline)")