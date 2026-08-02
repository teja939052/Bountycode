#!/usr/bin/env node
/**
 * Consolidates every api module onto the canonical request helper
 * (src/services/api/request.ts -> requestWithRetry) imported as `request`.
 *
 *  - BARE files (call `request(...)` with no definition) get the import prepended
 *    (fixes a latent runtime ReferenceError).
 *  - LOCAL-DEF files (duplicate their own preamble + request function) get the
 *    duplicated block stripped and replaced with the import.
 */
import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const API_DIR = join(process.cwd(), "src", "services", "api");
const IMPORT = `import { requestWithRetry as request } from "./request.ts";\n`;

function isBare(src) {
  return /\brequest\s*\(/.test(src) && !/function request\s*\(/.test(src) && !/requestWithRetry/.test(src);
}

function hasLocalDef(src) {
  return /function request\s*\(/.test(src);
}

let bare = 0, localDef = 0;
for (const f of readdirSync(API_DIR).sort()) {
  if (!f.endsWith(".ts") || ["index.ts", "flat.ts", "flatOverrides.ts", "request.ts"].includes(f)) continue;
  const src = readFileSync(join(API_DIR, f), "utf8");

  if (isBare(src)) {
    writeFileSync(join(API_DIR, f), IMPORT + src, "utf8");
    console.log(`BARE      ${f}  -> import added`);
    bare++;
    continue;
  }

  if (hasLocalDef(src)) {
    // strip preamble + local request fn: from file start through the line
    // right after the function's closing brace (blank line follows)
    const lines = src.split("\n");
    const reqIdx = lines.findIndex((l) => l.includes("function request("));
    // walk to the closing brace of the function
    let depth = 0, end = reqIdx;
    for (let i = reqIdx; i < lines.length; i++) {
      const line = lines[i];
      depth += (line.match(/\{/g) || []).length;
      depth -= (line.match(/\}/g) || []).length;
      if (depth <= 0) { end = i; break; }
    }
    const rest = lines.slice(end + 1).join("\n").replace(/^\n+/, "");
    writeFileSync(join(API_DIR, f), IMPORT + "\n" + rest, "utf8");
    console.log(`LOCAL-DEF ${f}  -> preamble stripped, import added`);
    localDef++;
  }
}
console.log(`done: ${bare} bare, ${localDef} local-def`);
