import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const API_DIR = join(process.cwd(), "src", "services", "api");

for (const f of readdirSync(API_DIR).sort()) {
  if (!f.endsWith(".ts") || ["index.ts", "flat.ts", "flatOverrides.ts"].includes(f)) continue;
  const src = readFileSync(join(API_DIR, f), "utf8");
  const usesRequest = /\brequest\s*\(/.test(src);
  const importsRWR = /requestWithRetry/.test(src);
  const definesLocal = /(?:async\s+)?function request\s*\(|const request\s*=/.test(src);
  const importAlias = src.match(/import\s*\{[^}]*requestWithRetry[^}]*\}\s*from[^;]+/) || [];
  if (!usesRequest) continue;
  const status = definesLocal ? "LOCAL-DEF" : importsRWR ? "IMPORTS-RWR" : "BARE (BUG)";
  const note = importsRWR && !definesLocal ? "uses requestWithRetry?" : "";
  console.log(`${status.padEnd(14)} ${f.padEnd(28)} ${note}`);
}
