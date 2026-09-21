import { requestWithRetry as request } from "./api/request.ts";
import type { AuthUser } from "./api/types.ts";

export interface LockDefinition {
  id: string;
  type:
    | "multiple_choice"
    | "code_expression"
    | "concept_check"
    | "runtime"
    | "prediction"
    | "arrange"
    | "fill_the_lock"
    | "fix_the_bug";
  label: string;
  description: string;
  accepted?: string[];
  rejected?: string[];
  hint_text: string;
  misconception?: string;
}

export interface HintLevel {
  id: number;
  text: string;
  reveals?: string;
  is_final: boolean;
}

export interface ProblemData {
  id: string;
  title: string;
  description: string;
  mode:
    | "predict"
    | "arrange"
    | "fill_the_lock"
    | "fix_the_bug"
    | "full_coding"
    | "oa";
  difficulty: "easy" | "medium" | "hard";
  learning_goal: string;
  time_complexity: string;
  space_complexity: string;
  estimated_xp: number;
  locks: LockDefinition[];
  hint_graph: HintLevel[];
  misconceptions: string[];
}

export interface SubmissionResult {
  success: boolean;
  mode: string;
  message: string;
  passed_tests?: number;
  total_tests?: number;
  score?: number;
  xp_awarded?: number;
  mastery_gain?: number;
  lock_unlocked?: string;
  hint_index?: number;
  hint_text?: string;
  misconception?: string;
}

export interface SRSDueEntry {
  problem_id: string;
  due_date: string;
  times_shown: number;
  times_correct: number;
  mastery: number;
}

export interface StaticAnalysisResult {
  language: string;
  ast_valid: boolean;
  patterns: Record<string, boolean>;
  variables: string[];
  functions: string[];
  loops: Array<{ type: string; lineno: number }>;
  conditionals: Array<{ lineno: number }>;
  complexity_hint?: string;
  errors: string[];
}

export interface LockState {
  problem_id: string;
  unlocked_locks: string[];
  current_lock: LockDefinition | null;
  progress: string;
  attempts: number;
  hint_index: number;
  misconceptions_hit: string[];
}

const BASE = "/api/v1/problems";

// ────────────────────────────────────────────────────────────────
// Problem API
// ────────────────────────────────────────────────────────────────
export async function fetchProblems(
  opts: { difficulty?: string; mode?: string; limit?: number } = {},
): Promise<ProblemData[]> {
  const params = new URLSearchParams();
  if (opts.difficulty) params.append("difficulty", opts.difficulty);
  if (opts.mode) params.append("mode", opts.mode);
  params.append("limit", String(opts.limit ?? 50));
  const qs = params.toString();
  return request<ProblemData[]>(`${BASE}?${qs}`);
}

export async function fetchProblem(problemId: string): Promise<ProblemData> {
  return request<ProblemData>(`${BASE}/${problemId}`);
}

export async function fetchProblemVisible(
  problemId: string,
): Promise<ProblemData> {
  return request<ProblemData>(`${BASE}/${problemId}/visible`);
}

// ────────────────────────────────────────────────────────────────
// Lock Engine API
// ────────────────────────────────────────────────────────────────
export async function fetchLockState(problemId: string): Promise<LockState> {
  return request<LockState>(`${BASE}/${problemId}/lock-state`);
}

export async function resetLocks(
  problemId: string,
): Promise<{ message: string; problem_id: string }> {
  return request(`${BASE}/${problemId}/reset-locks`, { method: "POST" });
}

// ────────────────────────────────────────────────────────────────
// Judge API
// ────────────────────────────────────────────────────────────────
export interface CodeSubmission {
  problem_id: string;
  language: string;
  code: string;
  stdin?: string;
  attempt_number?: number;
}

export async function checkLock(
  problemId: string,
  submission: Omit<CodeSubmission, "problem_id">,
): Promise<SubmissionResult> {
  return request<SubmissionResult>(`${BASE}/${problemId}/check-lock`, {
    method: "POST",
    body: JSON.stringify({ ...submission, problem_id: problemId }),
  });
}

export async function runFullProblem(
  problemId: string,
  submission: Omit<CodeSubmission, "problem_id">,
): Promise<SubmissionResult> {
  return request<SubmissionResult>(`${BASE}/${problemId}/run`, {
    method: "POST",
    body: JSON.stringify({ ...submission, problem_id: problemId }),
  });
}

export async function staticAnalysis(
  problemId: string,
  submission: { code: string; language: string },
): Promise<{ problem_id: string; analysis: StaticAnalysisResult }> {
  return request(`${BASE}/${problemId}/static-analysis`, {
    method: "POST",
    body: JSON.stringify({ ...submission, problem_id: problemId }),
  });
}

// ────────────────────────────────────────────────────────────────
// SRS API
// ────────────────────────────────────────────────────────────────
export async function fetchDueProblems(
  limit = 20,
): Promise<{ due_problems: SRSDueEntry[] }> {
  return request(`${BASE}/srs/due?limit=${limit}`);
}

export async function fetchMastery(
  problemId: string,
): Promise<{ problem_id: string; mastery: number }> {
  return request(`${BASE}/srs/mastery/${problemId}`);
}

// ────────────────────────────────────────────────────────────────
// Deterministic Hint Generator (no AI)
// ────────────────────────────────────────────────────────────────
export function generateHint(
  lock: LockDefinition,
  studentCode: string,
): { hintText: string } {
  const code = studentCode.toLowerCase();

  if (lock.type === "code_expression" || lock.type === "fill_the_lock") {
    if (lock.id === "choose-mid" && code.includes("(low + high) / 2")) {
      return { hintText: "Use integer division // to avoid float indices." };
    }
    if (lock.id === "choose-mid" && code.includes("arr[0]")) {
      return { hintText: "The midpoint is an index, not a value." };
    }
  }

  if (lock.type === "fix_the_bug") {
    if (code.includes("high = mid - 1") && code.includes("target")) {
      return {
        hintText: "Captain Byte: You found the target but walked toward the wrong half.",
      };
    }
  }

  return { hintText: lock.hint_text || "Think it through step by step." };
}

// ────────────────────────────────────────────────────────────────
// Local Runtime — browser Workers (Pyodide Python + JS)
// ────────────────────────────────────────────────────────────────
export interface ExecutionResult {
  success: boolean;
  stdout: string;
  stderr: string;
  executionTime?: number;
  error?: string;
}

type WorkerMessage =
  | {
      type: "init";
      id: string;
      payload: { pyodideUrl: string; packages: string[] };
    }
  | {
      type: "execute";
      id: string;
      payload: { code: string; stdin: string; timeout: number };
    }
  | {
      type: "result";
      id: string;
      success: boolean;
      result?: ExecutionResult;
      error?: string;
    };

class LocalRuntime {
  private pythonWorker: Worker | null = null;
  private jsWorker: Worker | null = null;
  private pendingPython = new Map<string, (r: ExecutionResult) => void>();
  private pendingJS = new Map<string, (r: ExecutionResult) => void>();
  private pythonReady = false;

  private pythonWorkerUrl = "/api/v1/runtime/workers/python.worker.js";
  private jsWorkerUrl = "/api/v1/runtime/workers/js.worker.js";
  private pyodideUrl = "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js";
  private defaultPackages = ["micropip", "numpy"];

  ensurePythonWorker(): void {
    if (this.pythonWorker || typeof window === "undefined") return;
    this.pythonWorker = new Worker(this.pythonWorkerUrl);
    this.pythonWorker.onmessage = (e: MessageEvent<WorkerMessage>) => {
      const msg = e.data;
      if (msg.type === "result") {
        const resolve = this.pendingPython.get(msg.id);
        if (resolve) {
          this.pendingPython.delete(msg.id);
          resolve(
            msg.result || {
              success: false,
              stdout: "",
              stderr: msg.error || "Unknown error",
            },
          );
        }
      }
    };
  }

  ensureJSWorker(): void {
    if (this.jsWorker || typeof window === "undefined") return;
    this.jsWorker = new Worker(this.jsWorkerUrl);
    this.jsWorker.onmessage = (e: MessageEvent<WorkerMessage>) => {
      const msg = e.data;
      if (msg.type === "result") {
        const resolve = this.pendingJS.get(msg.id);
        if (resolve) {
          this.pendingJS.delete(msg.id);
          resolve(
            msg.result || {
              success: false,
              stdout: "",
              stderr: msg.error || "Unknown error",
            },
          );
        }
      }
    };
  }

  private initPython(): Promise<void> {
    this.ensurePythonWorker();
    return new Promise((resolve, reject) => {
      const worker = this.pythonWorker!;
      const id = crypto.randomUUID();
      this.pendingPython.set(id, () => {
        this.pythonReady = true;
        resolve();
      });
      worker.onerror = () => reject(new Error("Python worker failed"));
      worker.postMessage({
        type: "init",
        id,
        payload: { pyodideUrl: this.pyodideUrl, packages: this.defaultPackages },
      });
      // Safety timeout in case the worker never acks.
      setTimeout(() => {
        if (this.pendingPython.has(id)) {
          this.pendingPython.delete(id);
          reject(new Error("Pyodide load timed out"));
        }
      }, 30000);
    });
  }

  async executePython(
    code: string,
    stdin = "",
    timeout = 10000,
  ): Promise<ExecutionResult> {
    this.ensurePythonWorker();
    if (typeof window === "undefined") {
      return { success: false, stdout: "", stderr: "Not in a browser" };
    }
    if (!this.pythonReady) {
      try {
        await this.initPython();
      } catch (err) {
        return { success: false, stdout: "", stderr: String(err) };
      }
    }
    return new Promise((resolve) => {
      const id = crypto.randomUUID();
      this.pendingPython.set(id, resolve);
      this.pythonWorker!.postMessage({
        type: "execute",
        id,
        payload: { code, stdin, timeout },
      });
    });
  }

  async executeJavaScript(
    code: string,
    stdin = "",
    timeout = 5000,
  ): Promise<ExecutionResult> {
    this.ensureJSWorker();
    if (typeof window === "undefined") {
      return { success: false, stdout: "", stderr: "Not in a browser" };
    }
    return new Promise((resolve) => {
      const id = crypto.randomUUID();
      this.pendingJS.set(id, resolve);
      this.jsWorker!.postMessage({
        type: "execute",
        id,
        payload: { code, stdin, timeout },
      });
    });
  }
}

export const localRuntime = new LocalRuntime();

// ────────────────────────────────────────────────────────────────
// Mastery
// ────────────────────────────────────────────────────────────────
export function calculateMastery(timesCorrect: number, timesShown: number): number {
  if (timesShown <= 0) return 0;
  return Math.round((timesCorrect / timesShown) * 100);
}

export type { AuthUser };
