export const API_BASE = import.meta.env.VITE_API_URL || "";

let authToken: string | null = null;

export function setAuthToken(token: string | null) {
  authToken = token;
}

export function getAuthToken(): string | null {
  return authToken;
}

export interface ApiErrorBody {
  detail?: string;
  error_explanation?: string | null;
  [key: string]: unknown;
}

export interface ApiRequestOptions extends RequestInit {
  headers?: Record<string, string>;
  skipAuthRefresh?: boolean;
}

const MEMORY_CACHE_TTL = 60000;
const MAX_CACHE_SIZE = 200;
const memoryCache = new Map<string, { data: unknown; timestamp: number }>();
const inFlight = new Map<string, Promise<unknown>>();
let refreshPromise: Promise<void> | null = null;

async function ensureAuth() {
  if (refreshPromise) return refreshPromise;
  refreshPromise = fetch(`${API_BASE}/api/v1/auth/refresh`, {
    method: "POST",
    credentials: "include",
  })
    .then(async (res) => {
      if (!res.ok) throw new Error("Session expired");
      const data = await res.json().catch(() => ({}));
      if ((data as { token?: string }).token) {
        setAuthToken((data as { token: string }).token);
      }
    })
    .catch((err) => {
      refreshPromise = null;
      throw err;
    });
  return refreshPromise;
}

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

export type ApiError = Error & {
  error_explanation?: string | null;
  status?: number;
  body?: string;
};

/** Flatten a FastAPI `detail` value (string, validation-error array, object) into one line. */
function normalizeDetail(detail: unknown): string | null {
  if (typeof detail === "string" && detail.trim()) return detail.trim();
  if (Array.isArray(detail)) {
    const parts = detail
      .map((item) => {
        if (typeof item === "string") return item;
        if (item && typeof item === "object") {
          const rec = item as { msg?: unknown; message?: unknown; loc?: unknown };
          const msg = typeof rec.msg === "string" ? rec.msg : typeof rec.message === "string" ? rec.message : "";
          const loc = Array.isArray(rec.loc) ? rec.loc.filter((p) => p !== "body").join(".") : "";
          if (msg) return loc ? `${loc}: ${msg}` : msg;
        }
        return "";
      })
      .filter(Boolean);
    if (parts.length) return parts.join("; ");
  }
  if (detail && typeof detail === "object") {
    try {
      return JSON.stringify(detail);
    } catch {
      return null;
    }
  }
  return null;
}

function unreachableMessage(): string {
  return API_BASE
    ? `Cannot reach the API at ${API_BASE}. Check your connection and that the server is running.`
    : "Cannot reach the API server. In local dev, make sure the backend is running on port 8000.";
}

/**
 * Turn a failed HTTP response into an ApiError with a message that actually
 * describes the failure.
 *
 * Why: the previous code fell back to the literal string "Request failed"
 * whenever the body was not JSON (proxy errors, HTML error pages, empty 500s),
 * which hid the real cause. Keep `status` on the error so callers can branch.
 */
export async function httpError(response: Response): Promise<ApiError> {
  const raw = await response.text().catch(() => "");
  let body: ApiErrorBody = {};
  if (raw) {
    try {
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed === "object") body = parsed as ApiErrorBody;
    } catch {
      // Not JSON: proxy/HTML/plain-text error page, handled below.
    }
  }

  const withMessage = body as { message?: unknown; error?: unknown };
  const envelope = withMessage.error;
  const envelopeObj =
    envelope && typeof envelope === "object" ? (envelope as { message?: unknown; details?: unknown }) : null;

  // Three error shapes exist in this API:
  //   1. FastAPI native:        { "detail": "Invalid email or password" }
  //   2. App middleware:        { "success": false, "error": { "code": 401, "message": "..." } }
  //   3. Validation:            { "detail": [{ "loc": [...], "msg": "..." }] }
  const serverMessage =
    normalizeDetail(body.detail) ||
    normalizeDetail(withMessage.message) ||
    normalizeDetail(envelopeObj?.message) ||
    (typeof envelope === "string" ? normalizeDetail(envelope) : null);

  const isHtml = /^\s*<(!doctype|html|head|body)/i.test(raw);
  const snippet = raw.trim().slice(0, 160);

  let message = serverMessage;
  if (!message) {
    if (isHtml) {
      message = `The server returned an HTML page instead of API data (HTTP ${response.status}). The /api request was not routed to the backend.`;
    } else if (response.status >= 500) {
      message =
        response.status === 502 || response.status === 504
          ? `The API proxy could not reach the backend (HTTP ${response.status}).`
          : `The API failed to handle the request (HTTP ${response.status}).`;
      if (!API_BASE) message += " Check that the backend is running on port 8000.";
    } else if (snippet) {
      message = snippet;
    } else {
      message = `Request failed (HTTP ${response.status}).`;
    }
  }

  const err = new Error(message) as ApiError;
  err.error_explanation = body.error_explanation || normalizeDetail(envelopeObj?.details) || null;
  err.status = response.status;
  err.body = raw.slice(0, 2000);
  return err;
}

export async function requestBlob(endpoint: string, options: ApiRequestOptions = {}) {
  const headers: Record<string, string> = {
    ...(options.headers || {}),
  };

  let response: Response;
  try {
    response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
      credentials: "include",
    });
  } catch {
    const err = new Error(unreachableMessage()) as ApiError;
    err.status = 0;
    throw err;
  }

  if (response.status === 401) {
    throw new Error("Session expired");
  }

  if (!response.ok) {
    throw await httpError(response);
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

  if (getAuthToken()) {
    headers.Authorization = `Bearer ${getAuthToken()}`;
  }

  const run = (async () => {
    let lastError: unknown;
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
          ...options,
          headers,
          credentials: "include",
        });

        if (response.status === 401 && attempt === 0 && !options.skipAuthRefresh) {
          try {
            await ensureAuth();
            continue;
          } catch {
            throw new Error("Session expired");
          }
        }

        if (!response.ok) {
          const err = await httpError(response);

          if (attempt < maxRetries && isIdempotent(options.method) && isRetryable(response.status, err)) {
            const delay = Math.min(1000 * Math.pow(2, attempt), 5000);
            await sleep(delay);
            continue;
          }
          throw err;
        }

        const raw: T = await response.json();
        const data =
          raw &&
          typeof raw === "object" &&
          "success" in raw &&
          "data" in raw
            ? (raw as { success: boolean; data: T }).data
            : raw;
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
        // A TypeError/AbortError here means fetch never got a response at all
        // (DNS failure, refused connection, proxy down, offline). Surface that
        // instead of the browser's bare "Failed to fetch".
        const name = (err as Error)?.name;
        if (name === "TypeError" || name === "AbortError") {
          const wrapped = new Error(
            typeof navigator !== "undefined" && navigator.onLine === false
              ? "You appear to be offline. Reconnect and try again."
              : unreachableMessage()
          ) as ApiError;
          wrapped.status = 0;
          wrapped.error_explanation = null;
          throw wrapped;
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
