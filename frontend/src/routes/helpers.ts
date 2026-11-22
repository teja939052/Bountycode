/**
 * Typed URL construction helpers for BountyCode frontend.
 *
 * Never manually concatenate dynamic paths. Always use these helpers to build
 * URLs from the route catalog. This guarantees:
 *
 *   • Single source of truth for route paths
 *   • Type-safe parameter substitution
 *   • Automatic 404 detection for unknown routes
 *   • Easy refactoring when paths change
 */
import {
  getRouteByPath,
  RouteDefinition,
  ROUTE_CATALOG,
} from "./catalog";

type RouteParams = Record<string, string | number | boolean>;

/**
 * Build a URL for a route by ID, substituting any :params.
 *
 * @example
 *   routeUrl("lesson-player", { lessonId: "python-hello" })
 *   // → "/lessons/python-hello"
 *
 * @example
 *   routeUrl("question-bank-detail", { questionId: "q-123" })
 *   // → "/question-bank/q-123"
 */
export function routeUrl(routeId: string, params?: RouteParams): string {
  const route = ROUTE_CATALOG.find((r) => r.id === routeId);
  if (!route) {
    console.error(`[routeUrl] Unknown route ID: ${routeId}`);
    return "/";
  }
  let url = route.path;
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      url = url.replace(new RegExp(`:${key}`, "g"), String(value));
    }
  }
  // Catch any remaining unsubstituted params
  const remaining = url.match(/:\w+/);
  if (remaining) {
    console.error(
      `[routeUrl] Unsubstituted params in route "${routeId}": ${remaining.join(
        ", "
      )}`
    );
  }
  return url;
}

/**
 * Build a URL from a raw path string, substituting :params.
 * Use this only when you don't have a stable route ID.
 *
 * @example
 *   pathUrl("/lessons/:lessonId", { lessonId: "python-hello" })
 *   // → "/lessons/python-hello"
 */
export function pathUrl(path: string, params?: RouteParams): string {
  let url = path;
  if (params) {
    for (const [key, value] of Object.entries(params)) {
      url = url.replace(new RegExp(`:${key}`, "g"), String(value));
    }
  }
  return url;
}

/**
 * Resolve a route definition by path (supports parametric matching).
 * Returns undefined if no route matches.
 */
export function resolveRoute(path: string): RouteDefinition | undefined {
  return getRouteByPath(path);
}

/**
 * All route IDs available in the catalog.
 */
export const ROUTE_IDS: string[] = ROUTE_CATALOG.map((r) => r.id);

/**
 * All hub names available in the catalog.
 */
export const HUB_NAMES: string[] = [
  ...new Set(ROUTE_CATALOG.map((r) => r.hub)),
];

/**
 * Check whether a path requires authentication.
 */
export function requiresAuth(path: string): boolean {
  const route = getRouteByPath(path);
  return route ? route.auth !== "public" : true;
}

/**
 * Check whether a path requires admin authorization.
 */
export function requiresAdmin(path: string): boolean {
  const route = getRouteByPath(path);
  return route ? route.auth === "admin" : false;
}

/**
 * Get the error boundary type for a path, if any.
 */
export function getErrorBoundaryType(
  path: string
): string | undefined {
  const route = getRouteByPath(path);
  return route?.errorBoundary;
}

// Re-export the catalog for direct access when needed
export { ROUTE_CATALOG };
