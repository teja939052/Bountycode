#!/usr/bin/env node
/**
 * Migrates a directory's `.js` files to `.ts` (or `.jsx` to `.tsx` when the
 * dir contains JSX) and rewrites every import specifier across src/ + scripts/
 * that pointed at the renamed files.
 *
 * Usage: node scripts/migrate-to-ts.mjs <dir>
 */
import { readdirSync, readFileSync, renameSync, writeFileSync, statSync } from "node:fs";
import { join, resolve, dirname, extname } from "node:path";

const dirArg = process.argv[2];
if (!dirArg) {
  console.error("usage: node scripts/migrate-to-ts.mjs <dir>");
  process.exit(1);
}
const DIR = resolve(process.cwd(), dirArg);
const ROOT = resolve(process.cwd());
const SRC = join(ROOT, "src");

const renamed = new Map(); // old file path -> new file path

function walk(dir) {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(join(dir, e.name)) : [join(dir, e.name)]
  );
}

function hasJsx(files) {
  return files.some((f) => f.endsWith(".jsx"));
}

// 1. rename files
const allFiles = walk(DIR);
const isJsxDir = hasJsx(allFiles);
for (const f of allFiles) {
  if (isJsxDir && f.endsWith(".jsx")) {
    const ts = f.slice(0, -4) + ".tsx";
    renameSync(f, ts);
    renamed.set(f, ts);
    console.log(`renamed  ${f.replace(ROOT, ".")}  ->  ${ts.replace(ROOT, ".")}`);
  } else if (!isJsxDir && f.endsWith(".js")) {
    const ts = f.slice(0, -3) + ".ts";
    renameSync(f, ts);
    renamed.set(f, ts);
    console.log(`renamed  ${f.replace(ROOT, ".")}  ->  ${ts.replace(ROOT, ".")}`);
  }
}

if (renamed.size === 0) {
  console.log("nothing to rename");
  process.exit(0);
}

// 2. rewrite specifiers in every src/script file
let changed = 0;
for (const file of walk(SRC).concat(walk(join(ROOT, "scripts")))) {
  if (!/\.(js|jsx|ts|tsx|mjs)$/.test(file)) continue;
  const src = readFileSync(file, "utf8");
  const out = src.replace(/from\s+(['"])([^'"]+)\1/g, (whole, q, spec) => {
    if (!spec.endsWith(".js") && !spec.endsWith(".jsx")) return whole;
    // resolve the specifier against the importing file's dir
    let abs;
    if (spec.startsWith("./") || spec.startsWith("../")) {
      abs = resolve(dirname(file), spec);
    } else if (spec.startsWith("/")) {
      abs = join(ROOT, spec);
    } else {
      return whole;
    }
    if (renamed.has(abs)) {
      changed++;
      const newExt = abs.endsWith(".jsx") ? ".tsx" : ".ts";
      return `from ${q}${spec.slice(0, spec.lastIndexOf("."))}${newExt}${q}`;
    }
    return whole;
  });
  if (out !== src) writeFileSync(file, out, "utf8");
}

console.log(`rewrote ${changed} import specifier(s)`);
console.log("done");
