export const API_BASE = import.meta.env.VITE_API_URL || "";

export interface ApiErrorBody {
  detail?: string;
  error_explanation?: string | null;
  [key: string]: unknown;
}

export interface ApiRequestOptions extends RequestInit {
  headers?: Record<string, string>;
}

const MEMORY_CACHE_TTL = 60000;
const memoryCache = new Map<string, { data: unknown; timestamp: number }>();

export function clearApiCache() {
  memoryCache.clear();
}

export async function requestBlob(endpoint: string, options: ApiRequestOptions = {}) {
  const headers: Record<string, string> = {
    ...(options.headers || {}),
  };

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (response.status === 401) {
    throw new Error("Session expired");
  }

  if (!response.ok) {
    const error: ApiErrorBody = await response.json().catch(() => ({ detail: "Request failed" }));
    const err = new Error(error.detail || "Request failed") as Error & {
      error_explanation?: string | null;
      status?: number;
    };
    err.error_explanation = error.error_explanation || null;
    err.status = response.status;
    throw err;
  }

  return response.blob();
}

function cacheKey(endpoint: string, options: ApiRequestOptions) {
  return `${options.method || "GET"}:${endpoint}:${JSON.stringify(options.body || "")}`;
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isRetryable(status: number | undefined, error: unknown) {
  if (status !== undefined && (status >= 500 || status === 408 || status === 429)) return true;
  if (error && (error as Error).name === "TypeError") return true;
  if (error && (error as Error).name === "AbortError") return true;
  return false;
}

export async function requestWithRetry<T = any>(
  endpoint: string,
  options: ApiRequestOptions = {},
  maxRetries = 3
): Promise<T> {
  const key = cacheKey(endpoint, options);
  const now = Date.now();

  if (options.method !== "POST" && memoryCache.has(key)) {
    const cached = memoryCache.get(key)!;
    if (now - cached.timestamp < MEMORY_CACHE_TTL) {
      return cached.data as T;
    }
    memoryCache.delete(key);
  }

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  let lastError: unknown;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
        credentials: "include",
      });

      if (response.status === 401) {
        throw new Error("Session expired");
      }

      if (!response.ok) {
        const error: ApiErrorBody = await response.json().catch(() => ({ detail: "Request failed" }));
        const err = new Error(error.detail || "Request failed") as Error & {
          error_explanation?: string | null;
          status?: number;
        };
        err.error_explanation = error.error_explanation || null;
        err.status = response.status;

        if (attempt < maxRetries && isRetryable(response.status, err)) {
          const delay = Math.min(1000 * Math.pow(2, attempt), 5000);
          await sleep(delay);
          continue;
        }
        throw err;
      }

      const data: T = await response.json();
      if (options.method !== "POST") {
        memoryCache.set(key, { data, timestamp: now });
      }
      return data;
    } catch (err) {
      lastError = err;
      if (attempt < maxRetries && isRetryable(undefined, err)) {
        const delay = Math.min(500 * Math.pow(2, attempt), 3000);
        await sleep(delay);
        continue;
      }
    }
  }

  throw lastError || new Error("Request failed after retries");
}
