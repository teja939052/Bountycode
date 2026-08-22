const API_BASE = import.meta.env.VITE_API_URL || "";
const MAX_KEEP = 50;
const STORAGE_KEY = "pp_debug_errors";
const IS_BROWSER = typeof window !== "undefined" && typeof document !== "undefined";

let installed = false;
let errors = [];

function persist() {
  if (!IS_BROWSER) return;
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify(errors.slice(0, 20).map((e) => ({ message: e.message, component: e.component, url: e.url, at: e.at })))
    );
  } catch {}
}

function addError(entry) {
  errors.unshift(entry);
  if (errors.length > MAX_KEEP) errors.length = MAX_KEEP;
  persist();
  reportToBackend(entry);
  setTimeout(() => {
    window.dispatchEvent(new CustomEvent("pp-error-tracked", { detail: entry }));
  }, 0);
}

function truncate(str, max) {
  if (!str) return str;
  return str.length > max ? str.slice(0, max) : str;
}

async function reportToBackend(entry) {
  if (!IS_BROWSER) return;
  try {
    await fetch(`${API_BASE}/api/v1/debug/log`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: truncate(entry.message, 2000),
        stack: truncate(entry.stack, 8000),
        url: truncate(entry.url || window.location.href, 500),
        component: truncate(entry.component, 200),
        level: entry.level || "error",
        user_agent: truncate(navigator.userAgent, 500),
      }),
      keepalive: true,
    }).catch(() => {});
  } catch {}
}

function cleanStack(stack) {
  if (!stack) return stack;
  return stack.split("\n").slice(0, 12).join("\n");
}

function getErrorLevel(err) {
  if (err && (err.message || "").match(/timeout|abort|network|failed to fetch|session expired/i)) {
    return "warn";
  }
  return "error";
}

export function trackError(error, component) {
  if (!IS_BROWSER) return;
  const message = (error && error.message) || String(error || "Unknown error");
  addError({
    message,
    stack: cleanStack((error && error.stack) || ""),
    component: component || "global",
    url: window.location.href,
    at: new Date().toISOString(),
    level: getErrorLevel(error),
  });
}

export function getTrackedErrors() {
  return errors;
}

export function clearTrackedErrors() {
  errors = [];
  if (!IS_BROWSER) return;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {}
}

export function installGlobalErrorTracker() {
  if (!IS_BROWSER) return;
  if (installed) return;
  installed = true;

  try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    if (Array.isArray(stored)) errors = stored.map((e) => ({ ...e, level: "stored" }));
  } catch {}

  window.addEventListener(
    "error",
    (event) => {
      trackError(event.error || new Error(event.message || "window error"), "window");
    },
    true
  );

  window.addEventListener(
    "unhandledrejection",
    (event) => {
      const reason = event.reason;
      let message;
      let stack;
      if (reason instanceof Error) {
        message = reason.message;
        stack = reason.stack;
      } else if (typeof reason === "string") {
        message = reason;
      } else {
        try {
          message = JSON.stringify(reason);
        } catch {
          message = String(reason);
        }
      }
      addError({
        message: message || "Unhandled promise rejection",
        stack: cleanStack(stack),
        component: "unhandledrejection",
        url: window.location.href,
        at: new Date().toISOString(),
        level: getErrorLevel(reason),
      });
    }
  );

  const originalError = console.error;
  console.error = (...args) => {
    originalError.apply(console, args);
    try {
      const joined = args.map((a) => (a instanceof Error ? a.message + "\n" + (a.stack || "") : typeof a === "string" ? a : JSON.stringify(a))).join(" | ");
      if (joined && joined.length < 3000) {
        addError({
          message: truncate(joined, 2000),
          stack: "",
          component: "console.error",
          url: window.location.href,
          at: new Date().toISOString(),
          level: "error",
        });
      }
    } catch {}
  };
}

export const errorTracker = { trackError, getTrackedErrors, clearTrackedErrors, installGlobalErrorTracker };
export default errorTracker;
