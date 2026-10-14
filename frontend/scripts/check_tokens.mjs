#!/usr/bin/env node
// Fails when a class used in src/ does not exist in the generated Tailwind CSS.
//
// Why this exists: 15 `nature-*` tokens were used across 7 files with no
// definition in tailwind.config.js or index.css. `npm run typecheck`, the unit
// tests, and `npm run build` all passed green while those pages rendered
// completely unstyled. Nothing in the toolchain notices a class that resolves
// to nothing. This does.
//
// Method: ask Tailwind to actually compile the project, then check each
// candidate class against the emitted CSS. Ground truth, not a reimplementation
// of Tailwind's resolution rules.
//
// Usage: node scripts/check_tokens.mjs [--verbose]

import { execFileSync } from "node:child_process";
import { readdirSync, readFileSync, statSync, mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, extname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const SRC = join(ROOT, "src");
const VERBOSE = process.argv.includes("--verbose");

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (entry === "node_modules" || entry === "archive") continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) walk(full, out);
    else if ([".tsx", ".ts", ".jsx", ".js"].includes(extname(entry))) out.push(full);
  }
  return out;
}

const files = walk(SRC);
if (VERBOSE) console.log(`scanning ${files.length} files under src/`);

// ── 1. Compile the real stylesheet ──────────────────────────────────────
const tmp = mkdtempSync(join(tmpdir(), "tw-"));
const entry = join(tmp, "in.css");
const outFile = join(tmp, "out.css");

// A tiny entry that mirrors index.css's Tailwind directives. index.css itself
// imports fonts/keyframes we do not need for class resolution.
writeFileSync(
  entry,
  `@tailwind base;\n@tailwind components;\n@tailwind utilities;\n`
);

let css;
try {
  // Invoke the JS entrypoint directly. The .cmd shim fails with EINVAL under
  // spawnSync on Windows.
  const cli = join(ROOT, "node_modules", "tailwindcss", "lib", "cli.js");
  execFileSync(process.execPath, [cli, "-c", join(ROOT, "tailwind.config.js"), "-i", entry, "-o", outFile], {
    cwd: ROOT,
    stdio: ["ignore", "ignore", "pipe"],
  });
  css = readFileSync(outFile, "utf8");
} catch (err) {
  console.error("FAIL: could not compile Tailwind CSS.");
  console.error(String(err.stderr || err.message).slice(0, 2000));
  rmSync(tmp, { recursive: true, force: true });
  process.exit(2);
}
rmSync(tmp, { recursive: true, force: true });

if (VERBOSE) console.log(`compiled stylesheet: ${css.length} bytes`);

// ── 2. Index the emitted class names ───────────────────────────────────
// Tailwind emits `.foo\/10`, `.md\:foo`, `@media` nested rules, etc.
const present = new Set();
for (const m of css.matchAll(/\.((?:[a-zA-Z0-9_-]|\\.)+)/g)) {
  present.add(m[1].replace(/\\(.)/g, "$1"));
}

// Hand-written classes in index.css (theme switcher, animations, component
// layers) are legitimate too. index.css is not in the compile above, so index
// its selectors separately rather than reporting false positives.
try {
  const cssFiles = readdirSync(SRC)
    .filter((f) => extname(f) === ".css")
    .map((f) => join(SRC, f));
  for (const f of cssFiles) {
    const raw = readFileSync(f, "utf8");
    for (const m of raw.matchAll(/\.((?:[a-zA-Z0-9_-]|\\.)+)/g)) {
      present.add(m[1].replace(/\\(.)/g, "$1"));
    }
    if (VERBOSE) console.log(`indexed ${f.replace(ROOT, "")}`);
  }
} catch {
  // no css files to index
}

// ── 3. Collect candidate classes from source ───────────────────────────
// Only classes that look like they encode a color/shape token, so we do not
// drown in prose words. Dynamic template interpolations are skipped.
const candidates = new Map(); // cls -> [{file, line}]

const CLASS_ATTR = /(?:class(?:Name)?\s*=\s*(?:"([^"]*)"|\{`([^`]*)`\}))/g;

for (const file of files) {
  const src = readFileSync(file, "utf8");
  let m;
  while ((m = CLASS_ATTR.exec(src)) !== null) {
    const raw = m[1] ?? m[2] ?? "";
    const line = src.slice(0, m.index).split("\n").length;
    for (const token of raw.split(/[\s\n]+/)) {
      // Template literals and JSX string concatenation leave stray quotes and
      // commas on tokens (`text-amber-200"`, `to-",`). Strip them.
      const cls = token.replace(/["'`,]/g, "").replace(/[{}()]/g, "").trim();
      if (!cls) continue;
      // Skip interpolations: dynamic by design.
      if (cls.includes("${") || cls.includes("$") || cls.includes("`")) continue;
      // Skip fragments produced by splitting on JS operators (.replace(/, +/).
      if (cls.includes(".replace") || /^[a-z-]+-[a-z]*\.[a-z(]/.test(cls)) continue;
      // Skip arbitrary values (bg-[...], text-[...]). Tailwind's JIT emits them
      // with escaped punctuation (`,` -> \2c ) that cannot be matched against
      // the raw source string. They are not part of the theme contract.
      if (cls.includes("[")) continue;
      // Skip bare fragment words left by template-literal splitting
      // (`from-`, `to-`, `via-` are prefixes awaiting a dynamic value).
      if (/^(?:from|via|to|bg|text|border|ring|fill|stroke|divide|accent|outline|decoration|caret|shadow)?-$/.test(cls)) continue;
      // A candidate must start with a known Tailwind utility prefix.
      if (!/^(?:[a-z-]+:)*(?:bg|text|border|from|via|to|ring|fill|stroke|accent|divide|outline|decoration|caret|shadow|font|grid|flex|rounded|container)-/.test(cls)) {
        continue;
      }
      if (!candidates.has(cls)) candidates.set(cls, []);
      const loc = { file: file.replace(ROOT, ""), line };
      const list = candidates.get(cls);
      if (!list.some((l) => l.file === loc.file && l.line === loc.line)) list.push(loc);
    }
  }
}

if (VERBOSE) console.log(`${candidates.size} candidate classes`);

// ── 4. Report ───────────────────────────────────────────────────────────
const missing = [];
for (const [cls, locs] of candidates) {
  // A class may be emitted with its variants stripped (hover:foo -> .foo:hover
  // is actually .hover\:foo, but `foo` is also emitted on its own if used bare).
  // Normalise away leading variants and check the tail segment too.
  const candidatesNorm = new Set([cls]);
  const stripped = cls.replace(/^(?:[a-z]+:)+/, "");
  candidatesNorm.add(stripped);
  const noOpacity = stripped.replace(/\/(?:DEFAULT|\d+|auto|none|full)$/, "");
  candidatesNorm.add(noOpacity);

  // A variant must resolve as itself. Falling back to the variant-stripped
  // name would hide a broken `dark:`/`hover:` layer behind a bare class that
  // happens to exist, which is exactly the failure this check exists to catch.
  const hasVariants = /^[a-z]+:/.test(cls);
  const cands = hasVariants
    ? new Set([cls, cls.replace(/\/(?:DEFAULT|\d+|auto|none|full)$/, "")])
    : candidatesNorm;

  let found = false;
  for (const c of cands) {
    if (present.has(c)) { found = true; break; }
  }
  if (!found) missing.push({ cls, locs });
}

if (VERBOSE) {
  const sample = [...present].slice(0, 15);
  console.log(`emitted classes indexed: ${present.size}, e.g. ${sample.join(", ")}`);
}

if (missing.length) {
  const byFile = new Map();
  for (const { cls, locs } of missing) {
    for (const l of locs) {
      const arr = byFile.get(l.file) || [];
      arr.push({ cls, line: l.line });
      byFile.set(l.file, arr);
    }
  }
  const total = missing.reduce((n, m) => n + m.locs.length, 0);
  console.error(
    `\nFAIL: ${missing.length} class(es) not emitted by Tailwind, across ${byFile.size} file(s) (${total} usages)\n`
  );
  for (const [file, list] of [...byFile].sort()) {
    console.error(`  ${file}`);
    const shown = list.slice(0, 12);
    for (const i of shown) console.error(`    line ${i.line}: ${i.cls}`);
    if (list.length > shown.length) console.error(`    ... and ${list.length - shown.length} more`);
  }
  console.error(
    "\nA class that resolves to nothing is invisible to typecheck and build." +
      "\nDefine it in tailwind.config.js / index.css, or remove the usage.\n"
  );
  process.exit(1);
}

console.log(`OK: all ${candidates.size} candidate classes are emitted by Tailwind (${files.length} files).`);
