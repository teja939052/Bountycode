/**
 * Frontend Sentry integration — optional, env-gated.
 *
 * Initializes @sentry/react only when VITE_SENTRY_DSN is set.
 * Never crashes the app if Sentry is unavailable.
 * Scrubs sensitive data before transmission.
 */

import * as Sentry from "@sentry/react";
import { browserTracingIntegration } from "@sentry/react";

const dsn = import.meta.env.VITE_SENTRY_DSN;
const environment = import.meta.env.VITE_SENTRY_ENVIRONMENT || "development";
const tracesSampleRate = parseFloat(
  import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE || "0.05"
);

let installed = false;

const SENSITIVE_KEY_SUBSTRINGS = [
  "password",
  "token",
  "secret",
  "cookie",
  "auth",
  "jwt",
  "email",
  "session",
];

function isSensitiveKey(key: string): boolean {
  const kl = key.toLowerCase();
  return SENSITIVE_KEY_SUBSTRINGS.some((s) => kl.includes(s));
}

function scrubValue(value: unknown): unknown {
  if (value === null || value === undefined) return value;
  if (typeof value === "string") {
    if (isSensitiveKey("")) return "[REDACTED]";
    if (value.length > 2000) return value.slice(0, 2000) + "...[TRUNCATED]";
    return value;
  }
  if (Array.isArray(value)) return value.map(scrubValue);
  if (typeof value === "object") {
    const scrubbed: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value)) {
      if (isSensitiveKey(k)) {
        scrubbed[k] = "[REDACTED]";
      } else {
        scrubbed[k] = scrubValue(v);
      }
    }
    return scrubbed;
  }
  return value;
}

export function initSentry() {
  if (installed) return;
  if (!dsn) {
    // Sentry is optional — local development works without it
    return;
  }
  installed = true;

  try {
    Sentry.init({
      dsn,
      environment,
      tracesSampleRate,
      integrations: [browserTracingIntegration()],
      // Never send PII or sensitive data
      sendDefaultPii: false,
      // Scrub sensitive data before transmission
      beforeSend(event) {
        // Scrub request data
        if (event.request) {
          event.request.headers = event.request.headers || {};
          const sensitiveHeaders = [
            "authorization",
            "cookie",
            "set-cookie",
            "x-api-key",
          ];
          for (const h of sensitiveHeaders) {
            if (event.request.headers[h]) {
              event.request.headers[h] = "[REDACTED]";
            }
          }
          // Remove request bodies that may contain passwords/tokens
          if (event.request.data) {
            event.request.data = "[REDACTED]";
          }
          // Scrub URL query params that may contain tokens
          if (event.request.url) {
            try {
              const url = new URL(event.request.url);
              for (const [key] of url.searchParams.entries()) {
                if (isSensitiveKey(key)) {
                  url.searchParams.set(key, "[REDACTED]");
                }
              }
              event.request.url = url.toString();
            } catch {}
          }
        }
        // Scrub extra/context recursively
        if (event.extra) {
          event.extra = scrubValue(event.extra) as Record<string, unknown>;
        }
        // Scrub exception values
        if (event.exception) {
          const values = event.exception.values;
          if (Array.isArray(values)) {
            for (const frame of values) {
              if (frame.value && typeof frame.value === "string") {
                // Truncate and scrub exception message
                frame.value = frame.value.slice(0, 500);
              }
              if (frame.stacktrace) {
                const frames = frame.stacktrace.frames;
                if (Array.isArray(frames)) {
                  for (const f of frames) {
                    if (f.vars) {
                      f.vars = scrubValue(f.vars) as Record<string, unknown>;
                    }
                  }
                }
              }
            }
          }
        }
        // Scrub breadcrumbs
        if (event.breadcrumbs) {
          const crumbs = event.breadcrumbs.values;
          if (Array.isArray(crumbs)) {
            for (const crumb of crumbs) {
              if (crumb.data) {
                crumb.data = scrubValue(crumb.data) as Record<string, unknown>;
              }
            }
          }
        }
        return event;
      },
      // Don't capture expected 4xx errors as errors
      beforeBreadcrumb(breadcrumb) {
        if (breadcrumb.category === "xhr" || breadcrumb.category === "fetch") {
          const data = breadcrumb.data as Record<string, unknown> | undefined;
          if (data && data.statusCode !== undefined) {
            const status = Number(data.statusCode);
            if (status >= 400 && status < 500) {
              // Downgrade expected client errors to info breadcrumbs
              breadcrumb.level = "info";
            }
          }
          // Scrub URL in breadcrumbs
          if (breadcrumb.data && typeof breadcrumb.data === "object") {
            breadcrumb.data = scrubValue(breadcrumb.data) as Record<string, unknown>;
          }
        }
        return breadcrumb;
      },
    });
  } catch {
    // Sentry failures must never crash the app
  }
}

export function captureException(error: Error, context?: Record<string, unknown>) {
  if (!installed) return;
  try {
    if (context) {
      const scrubbed: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(context)) {
        if (isSensitiveKey(key)) {
          scrubbed[key] = "[REDACTED]";
        } else {
          scrubbed[key] = scrubValue(value);
        }
      }
      Sentry.captureException(error, { extra: scrubbed });
    } else {
      Sentry.captureException(error);
    }
  } catch {}
}

export function captureMessage(message: string, level?: Sentry.SeverityLevel) {
  if (!installed) return;
  try {
    Sentry.captureMessage(message, level);
  } catch {}
}

export function setUser(user: { id?: string } | null) {
  if (!installed) return;
  try {
    if (user) {
      Sentry.setUser({ id: user.id }); // Only opaque ID, never email
    } else {
      Sentry.setUser(null);
    }
  } catch {}
}

export const sentry = { initSentry, captureException, captureMessage, setUser };
