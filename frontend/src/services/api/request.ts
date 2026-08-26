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
const MAX_CACHE_SIZE = 200;
const memoryCache = new Map<string, { data: unknown; timestamp: number }>();
const inFlight = new Map<string, Promise<unknown>>();

export function clearApiCache() {
  memoryCache.clear();
}

function pruneCache() {
  if (memoryCache.size <= MAX_CACHE_SIZE) return;
  const now = Date.now();
  for (const [key, entry] of memoryCache.entries()) {
    if (now - entry.timestamp > MEMORY_CACHE_TTL) {
      memoryCache.delete(key);
    }
  }
  if (memoryCache.size > MAX_CACHE_SIZE) {
    const entries = Array.from(memoryCache.entries());
    entries.sort((a, b) => a[1].timestamp - b[1].timestamp);
    const toRemove = entries.slice(0, memoryCache.size - MAX_CACHE_SIZE);
    for (const [key] of toRemove) {
      memoryCache.delete(key);
    }
  }
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
  if (status !== undefined && (status >= 500 || status === 408)) return true;
  if (error && (error as Error).name === "TypeError") return true;
  if (error && (error as Error).name === "AbortError") return true;
  return false;
}

function isIdempotent(method?: string) {
  return (
    !method ||
    method === "GET" ||
    method === "HEAD" ||
    method === "OPTIONS" ||
    method === "PUT" ||
    method === "DELETE"
  );
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

  // Single-flight: if the same idempotent request is already in flight,
  // share the promise instead of firing a duplicate network call. This
  // stops N components from each hammering the same GET on page load.
  if (options.method !== "POST" && inFlight.has(key)) {
    return inFlight.get(key) as Promise<T>;
  }

  pruneCache();

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };

  const run = (async () => {
    let lastError: unknown;
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
          ...options,
          headers,
          credentials: "include",
        });

        if (response.status === 401 && attempt === 0) {
          try {
            await fetch(`${API_BASE}/api/v1/auth/refresh`, {
              method: "POST",
              credentials: "include",
            });
            continue;
          } catch {
            throw new Error("Session expired");
          }
        }

        if (!response.ok) {
          const error: ApiErrorBody = await response.json().catch(() => ({ detail: "Request failed" }));
          const err = new Error(error.detail || "Request failed") as Error & {
            error_explanation?: string | null;
            status?: number;
          };
          err.error_explanation = error.error_explanation || null;
          err.status = response.status;

          if (attempt < maxRetries && isIdempotent(options.method) && isRetryable(response.status, err)) {
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
        if (attempt < maxRetries && isIdempotent(options.method) && isRetryable(undefined, err)) {
          const delay = Math.min(500 * Math.pow(2, attempt), 3000);
          await sleep(delay);
          continue;
        }
        throw err;
      }
    }

    throw lastError || new Error("Request failed after retries");
  })();

  if (options.method !== "POST") {
    inFlight.set(key, run);
    run
      .then(() => inFlight.delete(key))
      .catch(() => inFlight.delete(key));
  }

  return run as Promise<T>;
}
