#!/usr/bin/env node
/**
 * Dumps which namespace(s) define each "missing" flat api.<name> method.
 * Usage: node scripts/map-flat-api.mjs
 */
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const ROOT = process.cwd();
const API_DIR = join(ROOT, "src", "services", "api");

const nsMethods = {};
for (const f of readdirSync(API_DIR)) {
  if (!f.endsWith(".js") || f === "index.js") continue;
  const src = readFileSync(join(API_DIR, f), "utf8");
  const re = /export const (\w+Api)\s*=\s*\{([\s\S]*?)\n\};/g;
  let m;
  while ((m = re.exec(src)) !== null) {
    const name = m[1];
    const body = m[2];
    const keyRe = /^\s*(\w+)\s*:/gm;
    let k;
    while ((k = keyRe.exec(body)) !== null) {
      (nsMethods[k[1]] = nsMethods[k[1]] || new Set()).add(name);
    }
  }
}

const flatNames = new Set();
const re = /\bapi\.([A-Za-z_$][\w$]*)/g;
function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(join(dir, e.name)) : [join(dir, e.name)]
  );
}
const srcDir = join(ROOT, "src");
for (const file of walk(srcDir)) {
  if (!/\.(js|jsx)$/.test(file)) continue;
  const src = readFileSync(file, "utf8");
  let match;
  while ((match = re.exec(src)) !== null) {
    flatNames.add(match[1]);
  }
}

const TOP_LEVEL = new Set([
  "getMe", "register", "login", "logout", "updateProfile", "changePassword",
  "forgotPassword", "resetPassword", "onboardingStatus", "onboardingComplete",
  "cloudinaryImage", "cloudinaryVideo", "optimizeImage",
]);

for (const name of flatNames) {
  if (TOP_LEVEL.has(name)) continue;
  const owners = [...(nsMethods[name] || [])];
  console.log(`${name}  =>  ${owners.length ? owners.join(", ") : "** NO OWNER **"}`);
}
