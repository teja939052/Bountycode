#!/usr/bin/env node
/**
 * Static check: finds `api.<name>(...)` calls in the frontend that do not exist
 * on the aggregated `api` object from src/services/api/index.js.
 *
 * Usage: node scripts/check-api.mjs   (or npm run check:api)
 */
import { readdirSync, readFileSync } from "node:fs";
import { join, sep } from "node:path";

const ROOT = process.cwd();
const API_DIR = join(ROOT, "src", "services", "api");
const SRC_DIR = join(ROOT, "src");

const TOP_LEVEL_DELEGATES = new Set([
  "getMe", "register", "login", "logout", "updateProfile", "changePassword",
  "forgotPassword", "resetPassword", "onboardingStatus", "onboardingComplete",
  "cloudinaryImage", "cloudinaryVideo", "optimizeImage",
]);

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(join(dir, e.name)) : [join(dir, e.name)]
  );
}

function readMethods(file) {
  const src = readFileSync(file, "utf8");
  const methods = new Set();
  // object literal keys inside exported const *Api = { ... }
  const re = /export const (\w+Api)(?::\s*[^{]+)?\s*=\s*\{([\s\S]*?)\n\};/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const body = m[2];
    const keyRe = /^\s*(\w+)\s*:/gm;
    let k;
    while ((k = keyRe.exec(body)) !== null) methods.add(k[1]);
  }
  return methods;
}

const allMethods = new Set();
for (const f of walk(API_DIR)) {
  if (/\.(js|ts)$/.test(f)) {
    for (const m of readMethods(f)) allMethods.add(m);
  }
}

const nsRe = /^\s*(\w+):\s*(\w+Api),?\s*$/gm;
const apiIdx = readFileSync(join(API_DIR, "index.ts"), "utf8");
const namespaces = new Set();
let m;
while ((m = nsRe.exec(apiIdx)) !== null) namespaces.add(m[1]);

// flat layers add more known methods (auto-generated + hand-mapped overrides)
for (const extra of ["flat.ts", "flatOverrides.ts"]) {
  const src = readFileSync(join(API_DIR, extra), "utf8");
  for (const k of src.matchAll(/^\s{2}(\w+)\s*:/gm)) allMethods.add(k[1]);
}

const problems = [];
const count = new Map();

for (const file of walk(SRC_DIR)) {
  if (!/\.(js|jsx|ts|tsx)$/.test(file)) continue;
  if (file.includes(`${API_DIR}${sep}`) || file === join(API_DIR, "index.ts")) continue;
  const src = readFileSync(file, "utf8");
  // match `api.<name>` (dot-bounded so namespaces aren't mistaken as calls)
  const re = /\bapi\.([A-Za-z_$][\w$]*)/g;
  let match;
  while ((match = re.exec(src)) !== null) {
    const name = match[1];
    // skip object key shorthand / property read: only flag call-ish usage
    const after = src.slice(match.index + match[0].length);
    const isCallish = /^\s*\(/.test(after) || /^\s*\./.test(after) || /^\s*[=,)\]]/.test(after);
    if (!isCallish) continue;
    if (namespaces.has(name) || TOP_LEVEL_DELEGATES.has(name) || allMethods.has(name)) {
      continue;
    }
    count.set(name, (count.get(name) || 0) + 1);
    if (count.get(name) <= 5) {
      const rel = file.replace(/\\/g, "/").replace(ROOT.replace(/\\/g, "/") + "/", "");
      problems.push(`  ${name}  (${rel})`);
    }
  }
}

if (count.size === 0) {
  console.log("OK: no missing api.* methods found");
} else {
  console.log(`MISSING api.* methods (${count.size}):`);
  for (const [name, n] of count) {
    console.log(`  api.${name}  — used ${n} time(s)`);
  }
  console.log("");
  console.log("First occurrences:");
  for (const p of problems.slice(0, 30)) console.log(p);
  process.exitCode = 1;
}
