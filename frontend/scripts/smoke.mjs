#!/usr/bin/env node
/**
 * PlacementPro smoke test.
 *
 * Verifies the app boots, key pages render without crashing, and the core
 * backend flows (auth + telemetry) work. Run with:  npm run smoke
 *
 * - Auto-starts the Vite dev server if it isn't already running (kills it on exit).
 * - Requires the backend on :8000 (start it first via backend\start_backend.ps1).
 * - Uses headless Edge/Chrome to detect runtime JS crashes (Invalid hook call,
 *   React error boundaries, blank pages).
 */
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { setTimeout as sleep } from "node:timers/promises";

const FRONTEND = process.env.VITE_URL || "http://localhost:5173";
const API = process.env.API_URL || "http://localhost:8000";
const TEST_EMAIL = "smoke.test@ppro.app";
const TEST_PASSWORD = "Smoke@1234";

const results = [];
let startedVite = null;

function record(name, pass, detail = "") {
  results.push({ name, pass, detail });
  console.log(`${pass ? "PASS" : "FAIL"}  ${name}${detail ? `  — ${detail}` : ""}`);
}

async function waitFor(url, timeoutMs = 60000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const res = await fetch(url);
      if (res.status < 500) return true;
    } catch {}
    await sleep(1000);
  }
  return false;
}

function findBrowser() {
  const candidates = [
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  ];
  return candidates.find((p) => existsSync(p));
}

async function dumpDom(url) {
  const browser = findBrowser();
  if (!browser) throw new Error("No Edge/Chrome found for headless DOM check");
  const profile = mkdtempSync(join(tmpdir(), "pp-smoke-"));
  const outFile = join(profile, "dom.html");
  try {
    const dom = await new Promise((resolve, reject) => {
      const child = spawn(
        browser,
        [
          "--headless=new",
          "--disable-gpu",
          "--no-sandbox",
          `--user-data-dir=${profile}`,
          "--virtual-time-budget=15000",
          "--dump-dom",
          url,
        ],
        { stdio: ["ignore", "pipe", "pipe"], windowsHide: true }
      );
      let stdout = "";
      let stderr = "";
      child.stdout.on("data", (d) => (stdout += d));
      child.stderr.on("data", (d) => (stderr += d));
      child.on("close", (code) => {
        if (stdout.trim().startsWith("<!DOCTYPE") || stdout.length > 1000) {
          resolve(stdout);
        } else {
          reject(new Error(`headless browser exited ${code}: ${stderr.slice(0, 300)}`));
        }
      });
      child.on("error", reject);
    });
    return dom;
  } finally {
    rmSync(profile, { recursive: true, force: true });
  }
}

async function checkPage(path, { expect, forbid }) {
  const name = `page ${path} renders`;
  try {
    const dom = await dumpDom(`${FRONTEND}${path}`);
    const missing = expect.filter((s) => !dom.includes(s));
    const bad = forbid.filter((s) => dom.includes(s));
    if (missing.length === 0 && bad.length === 0) {
      record(name, true, `found ${expect.length} expected marker(s)`);
    } else {
      record(name, false, `missing=${missing.join(",")} bad=${bad.join(",")}`);
    }
  } catch (err) {
    record(name, false, err.message);
  }
}

async function apiCheck() {
  // unauthenticated /me should 401 (proves auth middleware runs, not blocked)
  try {
    const me = await fetch(`${API}/api/v1/auth/me`);
    record("GET /api/v1/auth/me unauth -> 401", me.status === 401, `got ${me.status}`);
  } catch (err) {
    record("GET /api/v1/auth/me unauth -> 401", false, err.message);
  }

  // telemetry must not be rate-limited or dedup-blocked
  let blocked = 0;
  for (let i = 0; i < 20; i++) {
    try {
      const r = await fetch(`${API}/api/v1/analytics/track`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ event: "page_view", path: `/smoke-${i}` }),
      });
      if (r.status === 429) blocked++;
    } catch {
      blocked++;
    }
  }
  record("telemetry burst (20x) no 429", blocked === 0, blocked ? `${blocked} blocked` : "all passed");

  // full auth flow (reuses fixed account: 200 on first run, 400 "already registered" after)
  try {
    const reg = await fetch(`${API}/api/v1/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: TEST_EMAIL, password: TEST_PASSWORD, name: "Smoke" }),
    });
    const regBody = await reg.json();
    const regErr = regBody?.error?.message || regBody?.detail || "";
    const regOk = reg.status === 200 || (reg.status === 400 && /already registered/i.test(regErr));
    record("register -> 200 (or already registered)", regOk, `got ${reg.status}`);

    const login = await fetch(`${API}/api/v1/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email: TEST_EMAIL, password: TEST_PASSWORD }),
    });
    const setCookie = login.headers.get("set-cookie") || "";
    const token = (setCookie.split(";")[0] || "").split("=")[1];
    record("login -> 200 + cookie", login.status === 200 && Boolean(token), `got ${login.status}, cookie=${Boolean(token)}`);

    if (token) {
      const me = await fetch(`${API}/api/v1/auth/me`, { headers: { Cookie: `pp_token=${token}` } });
      record("GET /me with cookie -> 200", me.status === 200, `got ${me.status}`);
    }
  } catch (err) {
    record("auth flow", false, err.message);
  }

  // debug log endpoint
  try {
    const r = await fetch(`${API}/api/v1/debug/log`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: "smoke test log", level: "info", url: FRONTEND }),
    });
    record("POST /api/v1/debug/log -> 200", r.status === 200, `got ${r.status}`);
  } catch (err) {
    record("POST /api/v1/debug/log -> 200", false, err.message);
  }
}

async function main() {
  console.log("PlacementPro smoke test");
  console.log(`  frontend: ${FRONTEND}`);
  console.log(`  backend:  ${API}`);
  console.log("");

  const backendUp = await waitFor(`${API}/api/v1/debug/logs`, 5000);
  if (!backendUp) {
    record("backend reachable", false, "start backend first: backend\\start_backend.ps1");
    return finish();
  }
  record("backend reachable", true);

  let viteUp = await waitFor(FRONTEND, 5000);
  if (!viteUp) {
    console.log("  -> starting vite dev server...");
    startedVite = spawn("node", ["node_modules/vite/bin/vite.js"], {
      cwd: process.cwd(),
      stdio: "ignore",
      windowsHide: true,
      detached: true,
    });
    viteUp = await waitFor(FRONTEND, 60000);
  }
  if (!viteUp) {
    record("frontend reachable", false, "could not start or reach vite dev server");
    return finish();
  }
  record("frontend reachable", true);

  await checkPage("/", { expect: ["anime-style progression"], forbid: ["Something went wrong", "Invalid hook"] });
  await checkPage("/register", { expect: ["Initialize Cadet Profile"], forbid: ["Something went wrong", "Invalid hook"] });
  await checkPage("/login", { expect: ["Access Command Deck"], forbid: ["Something went wrong", "Invalid hook"] });

  await apiCheck();
  return finish();
}

function finish() {
  const failures = results.filter((r) => !r.pass);
  console.log("");
  console.log(`${results.length - failures.length}/${results.length} checks passed`);
  if (startedVite) {
    try {
      process.kill(-startedVite.pid);
    } catch {}
  }
  process.exit(failures.length > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
