"""Batch execution verification for reviewed legacy coding questions.

Runs isolated execution per testcase (subprocess, timeout) and reports:
- signature ↔ inputs alignment
- computed expected vs stored expected
- hidden/visible distinctness
- aggregate PASS/FAIL per question

Usage:
  python scripts/verify_batch.py --limit 50 --offset 0
Writes: app/data/verify_batch_report.json
"""
import json, os, re, ast, subprocess, sys, tempfile, argparse
from collections import Counter

BANK = r"D:\Project-Fremen\backend\app\data\legacy_enriched_coding.json"
OUT = r"D:\Project-Fremen\backend\app\data\verify_batch_report.json"

def extract_fn(code):
    m = re.search(r"^\s*def\s+(\w+)\s*\(([^)]*)\)", code, re.M)
    if not m: return "", []
    name = m.group(1)
    params = [p.strip().split("=")[0].split(":")[0].strip() for p in m.group(2).split(",") if p.strip()]
    return name, [p for p in params if p not in ("self","cls")]

def try_exec(code, fn, params, inp_val, timeout=3):
    # inp_val is already parsed python object from enriched file
    # Need to decide args: if inp_val is dict -> kwargs, elif len(params)==1 -> (inp_val,), else try tuple unpack
    if not fn: return None, "no_fn"
    try:
        if isinstance(inp_val, dict):
            args = ()
            kwargs = inp_val
            call = f"{fn}(**_kwargs)"
        elif len(params) == 1:
            args = (inp_val,)
            kwargs = {}
            call = f"{fn}(*_args)"
        elif isinstance(inp_val, (list, tuple)) and len(inp_val) == len(params):
            args = tuple(inp_val)
            kwargs = {}
            call = f"{fn}(*_args)"
        else:
            return None, "param_mismatch"
    except Exception as e:
        return None, f"arg_build:{e}"

    runner = f"""{code}
import json as _j
try:
    _res = {call}
    try: print(_j.dumps(_res, default=str))
    except: print(repr(_res))
except Exception as _e:
    print("ERR:"+_e.__class__.__name__+":"+str(_e)[:300])
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tf:
        tf.write(f"_args = {repr(args)}\n_kwargs = {repr(kwargs)}\n")
        tf.write(runner)
        path = tf.name
    try:
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=timeout)
        out = (proc.stdout or "").strip()
        if out.startswith("ERR:"): return None, out[:400]
        if proc.returncode != 0: return None, (proc.stderr or out)[:400]
        if not out: return None, "no_output"
        try: return json.loads(out), None
        except: return out, None
    except subprocess.TimeoutExpired:
        return None, "timeout"
    finally:
        try: os.unlink(path)
        except: pass

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--offset", type=int, default=0)
    args = ap.parse_args()

    data = json.load(open(BANK, encoding="utf-8"))
    reviewed = [q for q in data if q.get("trust_status") == "reviewed"]
    batch = reviewed[args.offset: args.offset + args.limit]
    print(f"Verifying batch offset={args.offset} limit={args.limit} (reviewed pool {len(reviewed)})")

    results = []
    counts = Counter()
    for q in batch:
        qid = q["id"]
        code = q["solution"]["code"]
        fn, params = extract_fn(code)
        tcs = (q.get("testcases") or []) + (q.get("hidden_testcases") or [])
        # checks
        checks = {}
        checks["has_fn"] = bool(fn)
        checks["has_tcs"] = len(tcs) > 0
        checks["question_len"] = len(q.get("question",""))
        checks["fn_params"] = params
        # hidden/visible distinctness
        vis = q.get("testcases") or []
        hid = q.get("hidden_testcases") or []
        checks["visible"] = len(vis)
        checks["hidden"] = len(hid)
        checks["hidden_distinct"] = len(hid)==0 or any(h != v for h in hid for v in vis)

        per_tc = []
        all_pass = True
        fail_reason = None
        for tc in tcs:
            inp = tc["input"]
            exp = tc["expected"]
            computed, err = try_exec(code, fn, params, inp)
            if err:
                # param_mismatch is expected for multi-arg with single literal — not a code failure
                if err == "param_mismatch":
                    per_tc.append({"input": inp, "expected": exp, "computed": None, "error": err, "skipped": True})
                    continue
                per_tc.append({"input": inp, "expected": exp, "computed": None, "error": err})
                all_pass = False
                fail_reason = err
                break
            # normalize compare via json repr
            try:
                exp_norm = json.dumps(exp, sort_keys=True, default=str)
                comp_norm = json.dumps(computed, sort_keys=True, default=str)
            except:
                exp_norm = repr(exp); comp_norm = repr(computed)
            match = exp_norm == comp_norm
            per_tc.append({"input": inp, "expected": exp, "computed": computed, "match": match})
            if not match:
                all_pass = False
                fail_reason = f"mismatch expected {exp_norm[:80]} vs computed {comp_norm[:80]}"
                break

        # Only mark PASS if every non-skipped tc matched and at least one tc executed
        executed = [t for t in per_tc if not t.get("skipped")]
        if not executed:
            verdict = "SKIP"
            counts["SKIP"] += 1
        elif all_pass:
            verdict = "PASS"
            counts["PASS"] += 1
        else:
            verdict = "FAIL"
            counts["FAIL"] += 1

        results.append({
            "id": qid,
            "title": q["title"][:80],
            "topic": q.get("topic"),
            "difficulty": q.get("difficulty"),
            "function": fn,
            "params": params,
            "verdict": verdict,
            "fail_reason": fail_reason,
            "checks": checks,
            "testcases": per_tc[:4],  # cap for report size
        })
        print(f"  {qid[:8]} {verdict:5s} fn={fn} params={params} vis={len(vis)} hid={len(hid)} {fail_reason or ''}")

    print(f"\nBatch verdict: {dict(counts)}")
    report = {
        "offset": args.offset,
        "limit": args.limit,
        "reviewed_pool": len(reviewed),
        "counts": dict(counts),
        "results": results,
        "note": "PASS = all executed tcs matched stored expected. FAIL = mismatch or exec error. SKIP = param_mismatch/no executable tc (needs authoring). PASS does NOT auto-promote to verified — still requires signature↔prompt and constraint validation."
    }
    json.dump(report, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
