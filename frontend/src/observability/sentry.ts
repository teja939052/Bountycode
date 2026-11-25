"""Frontend Sentry integration — optional, env-gated.

Initializes @sentry/react only when VITE_SENTRY_DSN is set.
Never crashes the app if Sentry is unavailable.
Scrubs sensitive data before transmission.
"""

import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/react";

const dsn = import.meta.env.VITE_SENTRY_DSN;
const environment = import.meta.env.VITE_SENTRY_ENVIRONMENT || "development";
const tracesSampleRate = parseFloat(
  import.meta.env.VITE_SENTRY_TRACES_SAMPLE_RATE || "0.1"
);

let installed = false;

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
      integrations: [new BrowserTracing()],
      // Never send PII or sensitive data
      sendDefaultPii: false,
      // Scrub sensitive data before transmission
      beforeSend(event) {
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
        }
        // Remove request bodies that may contain passwords/tokens
        if (event.request && event.request.data) {
          event.request.data = "[REDACTED]";
        }
        // Scrub extra/context
        if (event.extra) {
          for (const key of Object.keys(event.extra)) {
            const kl = key.toLowerCase();
            if (
              kl.includes("password") ||
              kl.includes("token") ||
              kl.includes("secret") ||
              kl.includes("cookie") ||
              kl.includes("auth") ||
              kl.includes("email")
            ) {
              event.extra[key] = "[REDACTED]";
            }
          }
        }
        return event;
      },
      // Don't capture expected 4xx errors as errors
      beforeBreadcrumb(breadcrumb) {
        if (breadcrumb.category === "xhr" || breadcrumb.category === "fetch") {
          const data = breadcrumb.data as any;
          if (data && data.statusCode >= 400 && data.statusCode < 500) {
            // Downgrade expected client errors to info breadcrumbs
            breadcrumb.level = "info";
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
      // Scrub context before sending
      const scrubbed: Record<string, unknown> = {};
      for (const [key, value] of Object.entries(context)) {
        const kl = key.toLowerCase();
        if (
          kl.includes("password") ||
          kl.includes("token") ||
          kl.includes("secret") ||
          kl.includes("cookie") ||
          kl.includes("auth") ||
          kl.includes("email")
        ) {
          scrubbed[key] = "[REDACTED]";
        } else {
          scrubbed[key] = value;
        }
      }
      Sentry.captureException(error, { extra: scrubbed });
    } else {
      Sentry.captureException(error);
    }
  } catch {}
}

export function captureMessage(message: string, level?: Sentry.Severity) {
  if (!installed) return;
  try {
    Sentry.captureMessage(message, level);
  } catch {}
}

export function setUser(user: { id?: string; email?: string } | null) {
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
