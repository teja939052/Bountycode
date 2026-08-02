import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const API_DIR = join(process.cwd(), "src", "services", "api");

const LOCAL_FILES = [
  "achievements.ts", "auth.ts", "chat.ts", "economy.ts", "guilds.ts",
  "referrals.ts", "seasons.ts", "skillTrees.ts", "teams.ts", "tournaments.ts",
];

const CANONICAL = readFileSync(join(API_DIR, "request.ts"), "utf8");
// canonical function + preamble (from `const API_BASE` through the closing of request function)
const fnStart = CANONICAL.indexOf("export async function requestWithRetry");
const canonicalFn = CANONICAL.slice(0, fnStart) + CANONICAL.slice(fnStart).replace("export async function requestWithRetry", "async function request");

for (const f of LOCAL_FILES) {
  const src = readFileSync(join(API_DIR, f), "utf8");
  const reqIdx = src.indexOf("async function request");
  const body = src.slice(0, reqIdx + src.slice(reqIdx).indexOf("\n}") + 2);
  const matches = body.trim() === canonicalFn.trim();
  const hasOtherCodeAfter = src.slice(body.length).trim().length > 0;
  console.log(`${f.padEnd(28)} preambleMatchesCanonical=${matches}  hasExportsAfter=${hasOtherCodeAfter}  localFnEnd=${body.split("\n").length} lines`);
}
