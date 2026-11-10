import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { requestWithRetry, httpError } from "./request";

/**
 * Regression tests for the generic "Request failed" bug.
 *
 * The old code read `response.json()` and then used `body.detail` as the error
 * message. For anything that was not a FastAPI `{"detail": ...}` response —
 * the app's own `{success:false,error:{message}}` envelope, proxy 500s with an
 * empty/text body, HTML error pages, or a refused connection — the user saw
 * the literal string "Request failed". These tests pin the real message.
 */

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

describe("httpError", () => {
  it("reads the app middleware error envelope", async () => {
    const err = await httpError(
      jsonResponse(401, {
        success: false,
        error: {
          code: 401,
          message: "Invalid email or password",
          details: null,
          path: "/api/v1/auth/login",
          method: "POST",
          request_id: "abc",
        },
      })
    );
    expect(err.message).toBe("Invalid email or password");
    expect(err.status).toBe(401);
  });

  it("reads FastAPI's native detail string", async () => {
    const err = await httpError(jsonResponse(400, { detail: "Email already registered" }));
    expect(err.message).toBe("Email already registered");
    expect(err.status).toBe(400);
  });

  it("flattens FastAPI validation-error arrays", async () => {
    const err = await httpError(
      jsonResponse(422, {
        detail: [
          {
            loc: ["body", "email"],
            msg: "value is not a valid email address",
            type: "value_error",
          },
        ],
      })
    );
    expect(err.message).toBe("email: value is not a valid email address");
    expect(err.status).toBe(422);
  });

  it("explains an empty 500 instead of saying 'Request failed'", async () => {
    const err = await httpError(new Response("", { status: 500 }));
    expect(err.message).not.toBe("Request failed");
    expect(err.message).toContain("HTTP 500");
    expect(err.message).toContain("port 8000");
  });

  it("flags an HTML error page (request not routed to the API)", async () => {
    const err = await httpError(
      new Response("<!DOCTYPE html><html><body>Not found</body></html>", {
        status: 404,
        headers: { "Content-Type": "text/html" },
      })
    );
    expect(err.message).toMatch(/HTML page/);
    expect(err.status).toBe(404);
  });
});

describe("requestWithRetry error surfacing", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("surfaces the server message for a wrong password (login 401)", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        jsonResponse(401, {
          success: false,
          error: { code: 401, message: "Invalid email or password" },
        })
      )
    );

    await expect(
      requestWithRetry("/api/v1/auth/login", {
        method: "POST",
        body: "{}",
        skipAuthRefresh: true,
      })
    ).rejects.toThrow("Invalid email or password");

    vi.unstubAllGlobals();
  });

  it("reports an unreachable backend instead of the browser's 'Failed to fetch'", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new TypeError("Failed to fetch"))
    );

    const promise = requestWithRetry("/api/v1/auth/login", { method: "POST", body: "{}" });
    await expect(promise).rejects.toThrow(/Cannot reach the API server/);
    await expect(promise).rejects.toMatchObject({ status: 0 });

    vi.unstubAllGlobals();
  });
});
