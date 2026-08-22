import { useCallback, useEffect, useRef } from "react";
import useWebSocket from "./useWebSocket";
import api from "../services/api";

/**
 * Async execution enabled when:
 *  1. Explicitly opted in via env flag, OR
 *  2. Backend advertises DOCKER_SANDBOX_ENABLED / queue availability.
 */
export const ASYNC_COMPILER_ENABLED =
  import.meta.env.VITE_ASYNC_COMPILER === "true" || import.meta.env.VITE_ASYNC_COMPILER === "1";

/**
 * useCompilerQueue — submit compiler jobs through the async job queue and
 * resolve when the backend pushes `job_completed` / `job_failed` over the
 * WebSocket. Falls back to the sync path when async is disabled or the WS
 * closes before the job finishes.
 */
export function useCompilerQueue() {
  const pendingRef = useRef<Map<string, { resolve: (v: unknown) => void; reject: (e: Error) => void }>>(new Map());
  const statusRef = useRef<"idle" | "connecting" | "open" | "closed">("idle");

  const { status, send } = useWebSocket({
    enabled: ASYNC_COMPILER_ENABLED,
    pingIntervalMs: 30_000,
    onMessage: (msg) => {
      const { type, payload } = msg as { type?: string; payload?: { job_id?: string; result?: unknown; error?: string } };
      if (!payload?.job_id) return;
      const pending = pendingRef.current.get(payload.job_id);
      if (!pending) return;

      if (type === "job_completed") {
        pendingRef.current.delete(payload.job_id);
        pending.resolve(payload.result);
      } else if (type === "job_failed") {
        pendingRef.current.delete(payload.job_id);
        pending.reject(new Error(payload.error || "Job failed"));
      }
    },
    onOpen: () => {
      statusRef.current = "open";
    },
    onClose: () => {
      statusRef.current = "closed";
      // Fail anything still waiting so callers fall back to sync
      for (const [jobId, p] of pendingRef.current) {
        p.reject(new Error(`WS closed before job ${jobId} completed`));
      }
      pendingRef.current.clear();
    },
  });

  useEffect(() => {
    statusRef.current = status;
  }, [status]);

  const waitForJob = useCallback((jobId: string, timeoutMs = 60_000): Promise<unknown> => {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        pendingRef.current.delete(jobId);
        reject(new Error(`Job ${jobId} timed out`));
      }, timeoutMs);
      const wrapped = {
        resolve: (v: unknown) => {
          clearTimeout(timer);
          resolve(v);
        },
        reject: (e: Error) => {
          clearTimeout(timer);
          reject(e);
        },
      };
      pendingRef.current.set(jobId, wrapped);
    });
  }, []);

  /**
   * Run a compiler op. `run` is the sync API call (returns the result);
   * `submitAsync` posts the payload with async_mode and returns `{job_id}`.
   * Returns the result object regardless of path.
   */
  const execute = useCallback(
    async ({
      run,
      submitAsync,
      timeoutMs = 60_000,
    }: {
      run: () => Promise<unknown>;
      submitAsync: () => Promise<{ job_id?: string }>;
      timeoutMs?: number;
    }): Promise<unknown> => {
      if (!ASYNC_COMPILER_ENABLED) {
        return run();
      }
      try {
        const { job_id } = await submitAsync();
        if (!job_id) return run();
        if (statusRef.current !== "open") {
          // WS not connected — don't wait indefinitely; poll-free fallback
          return run();
        }
        return await waitForJob(job_id, timeoutMs);
      } catch (err) {
        // Queue path failed (no broker, auth, etc.) — fall back to sync
        return run();
      }
    },
    [waitForJob]
  );

  return { execute, asyncEnabled: ASYNC_COMPILER_ENABLED, wsStatus: status, send };
}

export default useCompilerQueue;
