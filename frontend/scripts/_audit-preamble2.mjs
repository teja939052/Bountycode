import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const API_DIR = join(process.cwd(), "src", "services", "api");
const canon = readFileSync(join(API_DIR, "request.ts"), "utf8").split("\n");
const canonPreamble = canon.slice(0, 20).join("\n"); // lines 1-20 (incl `export async function requestWithRetry(...) {`)
const canonBody = canon.slice(21, 79).join("\n").trim(); // inner body

for (const f of readdirSync(API_DIR).sort()) {
  if (!f.endsWith(".ts") || ["index.ts", "flat.ts", "flatOverrides.ts", "request.ts"].includes(f)) continue;
  const lines = readFileSync(join(API_DIR, f), "utf8").split("\n");
  const reqLine = lines.findIndex((l) => l.includes("function request("));
  if (reqLine === -1) continue;
  // preamble check: lines 1..reqLine should equal canon preamble (modulo signature)
  const localPre = lines.slice(0, reqLine).join("\n");
  const canonPre = canon.slice(0, reqLine).join("\n");
  const localBody = lines.slice(reqLine + 1, reqLine + 60).join("\n").trim();
  const sigOk = lines[reqLine].trim().startsWith("async function request(endpoint");
  const preOk = localPre === canonPre;
  const bodyOk = localBody.startsWith(canonBody);
  console.log(`${f.padEnd(28)} reqAt=${reqLine} sig=${sigOk} pre=${preOk} body=${bodyOk}`);
}
