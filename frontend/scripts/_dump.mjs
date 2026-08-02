import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
const d = join(process.cwd(), "src", "services", "api");
const skip = (s, i) => {
  const q = s[i]; i++;
  while (i < s.length) {
    if (s[i] === "\\") { i += 2; continue; }
    if (s[i] === q) return i + 1;
    if (q === "`" && s[i] === "$" && s[i + 1] === "{") { let dep = 0; i++; do { if (s[i] === "{") dep++; else if (s[i] === "}") dep--; i++; } while (dep > 0 && i < s.length); continue; }
    i++;
  }
  return i;
};
const slice = (src, b) => {
  let dep = 0, i = b;
  while (i < src.length) {
    const c = src[i];
    if (c === '"' || c === "'" || c === "`") { i = skip(src, i); continue; }
    if (c === "{") dep++; else if (c === "}") { dep--; if (dep === 0) return src.slice(b + 1, i); }
    i++;
  }
  return src.slice(b + 1);
};
const stop = new Set(["method", "body", "if", "requestWithRetry", "credentials", "async", "function"]);
for (const f of readdirSync(d)) {
  if (!f.endsWith(".js") || f === "index.js" || f === "flat.js") continue;
  const src = readFileSync(join(d, f), "utf8");
  for (const m of src.matchAll(/export const (\w+Api)\s*=\s*\{/g)) {
    const obj = slice(src, m.index + m[0].length - 1);
    const keys = [...obj.matchAll(/^\s*(\w+)\s*[:\(]/gm)].map((k) => k[1]).filter((k) => !stop.has(k));
    if (keys.length) console.log(m[1] + ": " + keys.join(", "));
  }
}
