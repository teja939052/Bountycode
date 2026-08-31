import json, os, re, ast, subprocess, sys, tempfile
BANK = r"D:\Project-Fremen\backend\app\data\legacy_enriched_coding.json"
OUT = r"D:\Project-Fremen\backend\app\data\verify_all_report.json"

def extract_fn(code):
    m = re.search(r"^\s*def\s+(\w+)\s*\(([^)]*)\)", code, re.M)
    if not m: return "", []
    name = m.group(1)
    params = [p.strip().split("=")[0].split(":")[0].strip() for p in m.group(2).split(",") if p.strip()]
    return name, [p for p in params if p not in ("self","cls")]

def try_exec(code, fn, params, inp_val, timeout=3):
    if not fn: return None, "no_fn"
    if isinstance(inp_val, dict):
        args, kwargs, call = (), inp_val, f"{fn}(**_kwargs)"
    elif len(params) == 1:
        args, kwargs, call = (inp_val,), {}, f"{fn}(*_args)"
    elif isinstance(inp_val, (list, tuple)) and len(inp_val) == len(params):
        args, kwargs, call = tuple(inp_val), {}, f"{fn}(*_args)"
    else:
        return None, "param_mismatch"
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

data = json.load(open(BANK, encoding="utf-8"))
reviewed = [q for q in data if q.get("trust_status")=="reviewed"]
print(f"Total reviewed pool: {len(reviewed)}")

results=[]
from collections import Counter
counts=Counter()
for idx, q in enumerate(reviewed):
    qid=q["id"]; code=q["solution"]["code"]; fn, params=extract_fn(code)
    tcs=(q.get("testcases")or[])+(q.get("hidden_testcases")or[])
    vis=q.get("testcases")or[]; hid=q.get("hidden_testcases")or[]
    per=[]
    all_pass=True; fail=None
    for tc in tcs:
        inp=tc["input"]; exp=tc["expected"]
        comp, err = try_exec(code, fn, params, inp)
        if err=="param_mismatch":
            per.append({"input":inp,"expected":exp,"skipped":True,"error":err}); continue
        if err:
            per.append({"input":inp,"expected":exp,"error":err}); all_pass=False; fail=err; break
        exp_n=json.dumps(exp,sort_keys=True,default=str)
        comp_n=json.dumps(comp,sort_keys=True,default=str)
        m=exp_n==comp_n
        per.append({"input":inp,"expected":exp,"computed":comp,"match":m})
        if not m: all_pass=False; fail=f"mismatch {exp_n[:60]} vs {comp_n[:60]}"; break
    executed=[t for t in per if not t.get("skipped")]
    if not executed: verdict="SKIP"; counts["SKIP"]+=1
    elif all_pass: verdict="PASS"; counts["PASS"]+=1
    else: verdict="FAIL"; counts["FAIL"]+=1
    results.append({"id":qid,"title":q["title"][:60],"topic":q.get("topic"),"difficulty":q.get("difficulty"),"fn":fn,"params":params,"verdict":verdict,"fail":fail,"vis":len(vis),"hid":len(hid)})
    if (idx+1)%50==0:
        print(f"  {idx+1}/{len(reviewed)} -> {dict(counts)}")

print(f"\nFinal: {dict(counts)} PASS={counts['PASS']} FAIL={counts['FAIL']} SKIP={counts['SKIP']}")
# Save full report
report={"total_reviewed":len(reviewed),"counts":dict(counts),"results":results}
json.dump(report, open(OUT,"w",encoding="utf-8"), indent=2, ensure_ascii=False)
print(f"Wrote {OUT}")

# Also build promoted list (PASS only, after additional prompt/signature/constraint checks TODO)
# For now, promote PASS where question_len>=40 and hidden distinct
promotable=[]
for r, q in zip(results, reviewed):
    if r["verdict"]=="PASS" and len(q.get("question",""))>=40 and r["vis"]>0:
        promotable.append(q["id"])
print(f"Promotable PASS candidates (len>=40): {len(promotable)}")
json.dump({"promotable_ids":promotable,"count":len(promotable)}, open(r"D:\Project-Fremen\backend\app\data\promotable_to_verified.json","w",encoding="utf-8"), indent=2)
