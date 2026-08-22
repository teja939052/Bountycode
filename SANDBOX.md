# Sandboxing OpenCode

> **TL;DR**: OpenCode is an agent with full user permissions. Before running it on any
> untrusted repo (or any repo that might `git push` / exfiltrate secrets), wrap it in a
> sandbox. This doc is the canonical "how we run OpenCode securely" guide for this
> machine so the setup is reproducible.

## Threat model (why this matters here)

OpenCode inherits the **full permissions of the user that launches it**. In this repo
that means it could read/write:

- `.env`, `.env.local`, any `*.pem`, `~/.ssh/id_*`, CI tokens, DB passwords embedded in
  scripts, etc.

The in-app permission prompts are a **UX feature, not a security boundary**. Treat them
as convenience warnings, not isolation.

## Recommended, self-hosted solutions (ranked)

### 1. opencode-sandbox  (default choice — purpose-built, simplest)

A lightweight Docker image with git / python / node pre-installed, running as a
**non-root user**. Supports AMD64 + ARM64 (Apple Silicon).

**Setup:**
`bash <(curl -fsSL https://raw.githubusercontent.com/sri-paex/opencode-sandbox/main/install.sh)`

This registers an `oh` command. Then in **any** project:

```bash
cd ~/my-untrusted-repo
oh            # launches OpenCode inside the sandbox container
```

The container mounts the project at `/workspace` (read-write) but **does not** mount:

- `$HOME/.ssh`
- `$HOME/.gitconfig` (uses a sandbox-local one)
- the host `$HOME` at all (only the project dir)

**Allow-list mounts (what IS exposed):**
```
/workspace   <- the project you cd'd into
/opt/opencode-config  <- read-only shared config (optional)
```

### 2. Microsandbox  (highest isolation — microVMs, sub-100ms boot)

For code-execution flows or untrusted agent code, run inside a **micro-VM** with
hardware-level isolation and ~100ms cold start. OCI-compatible so you can use standard
images.

Install: `curl -fsSL https://microsandbox.dev/install.sh | bash`

Then from `backend/app/services/`:
```bash
msb run -- python -c "exec(open('code_executor.py').read())"
```

### 3. AI Sandbox Wrapper  (multi-tool, batteries-included)

Wraps OpenCode **and** other agents (amp, droid...). Protects SSH keys + API tokens,
supports per-project DB isolation. Install via `npx @sandbox-ai/setup` then
`sandbox opencode` from inside a project.

## This host (Windows, no Docker)

If Docker isn't available on the host, fall back to the local wrapper script
`./sandbox-opencode.bat`, which:

1. **Unsets** every known secret-bearing env var (`GITHUB_TOKEN`, `GIT_AUTHOR_*`,
   `AWS_*`, `DATABASE_URL`, `OPENROUTER_API_KEY`, etc.).
2. **Runs OpenCode in the repo root only** (no parent-dir escalation).
3. **Disables network egress** by prefixing `opencode --no-network` where supported.

```bat
@echo off
REM ./sandbox-opencode.bat  — minimal local sandbox for Windows hosts w/o Docker
setlocal
for %%V in (GITHUB_TOKEN GIT_AUTHOR_NAME GIT_AUTHOR_EMAIL AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY OPENROUTER_API_KEY DATABASE_URL) do set "%%V="
opencode --no-network
endlocal
```

## Backend code-execution fallback (already wired)

The compiler engine (`backend/app/services/code_executor.py`) has a **multi-hop
fallback chain** when the public Piston API is rate-limited or unreachable:

```
Piston API  →  Wandbox  →  Glot.io  →  local sandbox (self-hosted, zero egress)
```

- **Wandbox + Glot.io** (`backend/app/services/remote_fallbacks.py`): free anonymous
  JSON APIs, tried in parallel after Piston. Gate with `USE_REMOTE_FALLBACKS=true`.
  Best-effort providers with per-IP rate limits — treated as a UX fallback, not a
  security boundary. Optional free Glot.io token via `GLOT_API_TOKEN`.
  Per-run cap `REMOTE_FALLBACK_TIMEOUT` (default 8s, clamped 1–15s).
- **Local sandbox** (`backend/app/services/local_sandbox.py`, `execute_local`):
  self-hosted fallback that needs no external API. Set `USE_LOCAL_SANDBOX=true`.

### Local sandbox details

- Languages: **Python** (full) and **JavaScript** (needs a healthy `node` on the host).
- Isolation (no Docker needed):
  - Hard timeout via subprocess `kill` (`SANDBOX_TIMEOUT`, default 5s).
  - Restricted builtins — `open`, `exec`, `eval`, `__import__` blocked by default.
  - **Safe-module allowlist** for `import`: `sys`, `math`, `collections`, `itertools`,
    `functools`, `re`, `json`, `bisect`, `heapq`, `random`, `string`, `statistics`,
    `typing`, `dataclasses`, `copy`, `decimal`, `fractions`, `queue`, `array`,
    `struct`, `calendar`, `datetime`, `time`, `operator`, `pprint`.
  - Blocks `os`, `socket`, `subprocess`, `requests`, `urllib`, etc.
  - POSIX-only `RLIMIT_CPU`/`RLIMIT_AS` resource limits (skipped on Windows).
- Verified: output capture, `input()`, stdin, timeout kills infinite loops,
  blocked-import rejection, and `execute_against_test_cases` all work end-to-end.
  Remote providers verified live (Wandbox + Glot return `source: wandbox` /
  `source: glot_io`) with a broken Piston URL forcing the fallback path.

> Note: these are **UX-level fallbacks**, not a hard security boundary. For multi-tenant
> or adversarial workloads, keep a true container sandbox (self-hosted Piston, Judge0,
> or Microsandbox) behind it.

## Quick checklist before every untrusted session

- [ ] Are there secret files? `ls .env* *.pem` — if yes, run via `opencode-sandbox`.
- [ ] Is Docker present? `docker run --rm hello-world` → if yes, use `oh`.
- [ ] Otherwise use `./sandbox-opencode.bat`.
- [ ] After the session, `git status --porcelain` and revert anything unexpected.

## Related reading

- OpenCode docs: https://opencode.ai (permission system is UX-only, not security).
- Dany Fortin decomposition / Piston-API rate-limit observations tracked in `FUTURE.md`.
