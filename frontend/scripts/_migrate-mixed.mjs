import { readdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { join, resolve, dirname } from "node:path";

const ROOT = resolve(process.cwd());
const SRC = join(ROOT, "src");
const targetDir = process.argv[2];
const DIR = resolve(process.cwd(), targetDir);

const renamed = new Map();
for (const f of readdirSync(DIR)) {
  if (!f.endsWith(".js") && !f.endsWith(".jsx")) continue;
  const abs = join(DIR, f);
  const newName = f.endsWith(".jsx") ? f.slice(0, -4) + ".tsx" : f.slice(0, -3) + ".ts";
  renameSync(abs, join(DIR, newName));
  renamed.set(abs, join(DIR, newName));
  console.log(`renamed ${f} -> ${newName}`);
}

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(join(dir, e.name)) : [join(dir, e.name)]
  );
}

let changed = 0;
for (const file of walk(SRC)) {
  if (!/\.(js|jsx|ts|tsx)$/.test(file)) continue;
  const src = readFileSync(file, "utf8");
  const out = src.replace(/from\s+(['"])([^'"]+)\1/g, (whole, q, spec) => {
    if (!/\.(js|jsx)$/.test(spec)) return whole;
    let abs;
    if (spec.startsWith("./") || spec.startsWith("../")) abs = resolve(dirname(file), spec);
    else if (spec.startsWith("/")) abs = join(ROOT, spec);
    else return whole;
    if (renamed.has(abs)) {
      changed++;
      const newExt = spec.endsWith(".jsx") ? ".tsx" : ".ts";
      return `from ${q}${spec.slice(0, spec.lastIndexOf("."))}${newExt}${q}`;
    }
    return whole;
  });
  if (out !== src) writeFileSync(file, out, "utf8");
}
console.log(`rewrote ${changed} import specifier(s)`);
