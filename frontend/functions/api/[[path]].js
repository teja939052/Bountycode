/* Cloudflare Pages Function: same-origin /api/* proxy → Render backend.
 *
 * Why: the SPA calls same-origin `/api/...` (see services/api/request.ts
 * with empty VITE_API_URL). This proxy forwards those calls to the real
 * API, so (1) no CORS / preview-domain allowlisting, (2) auth cookies stay
 * first-party, (3) the backend URL is a runtime Pages secret (API_URL),
 * never baked into the JS bundle. Direct cross-origin mode (VITE_API_URL
 * set) keeps working unchanged.
 */
export async function onRequest({ request, env }) {
  const apiBase = (env.API_URL || "").replace(/\/+$/, "");
  if (!apiBase) {
    return new Response("API_URL not configured", { status: 503 });
  }
  const url = new URL(request.url);
  const target = apiBase + url.pathname + url.search;

  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("content-length");

  const init = {
    method: request.method,
    headers,
    redirect: "manual",
  };
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = request.body;
    init.duplex = "half";
  }
  const upstream = await fetch(target, init);

  const out = new Headers(upstream.headers);
  return new Response(upstream.body, { status: upstream.status, headers: out });
}
