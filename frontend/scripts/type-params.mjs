import { readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const API_DIR = join(process.cwd(), "src", "services", "api");
let changed = 0;

for (const f of readdirSync(API_DIR).sort()) {
  if (!f.endsWith(".ts")) continue;
  const src = readFileSync(join(API_DIR, f), "utf8");
  // only rewrite default params: `name = {}` preceded by `(` or `, `
  const out = src.replace(/([\(\s,])(\w+)\s*=\s*\{\}/g, "$1$2: Record<string, any> = {}");
  if (out !== src) {
    writeFileSync(join(API_DIR, f), out, "utf8");
    changed++;
    console.log(`typed defaults  ${f}`);
  }
}
console.log(`done: ${changed} files updated`);
