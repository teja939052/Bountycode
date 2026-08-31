import json, sys, os, tempfile
sys.path.insert(0, r"D:\Project-Fremen\backend")
bank = json.load(open("app/data/questions_bank.json", encoding="utf-8"))
coding = [q for q in bank if q.get("type") == "coding"]
# Test first 5 coding questions by executing solution code
results = []
for idx, q in enumerate(coding[:5]):
    code = (q.get("solution") or {}).get("code", "")
    language = (q.get("solution") or {}).get("language", "python")
    # build exec namespace
    ns = {}
    try:
        exec(compile(code, "<string>", "exec"), ns, ns)
        fn_name = [k for k in ns if not k.startswith("__")][0]
        fn = ns[fn_name]
        # derive simple test input from problem statement or correct_answer
        ca = q.get("correct_answer")
        # try running fn with no args or minimal; capture any output
        try:
            # if function takes 2 args (like searchRange), use simple inputs
            if fn_name == "searchRange":
                result = fn([3, 4, 5, 6], 4)
            elif fn_name == "containsDuplicate":
                result = fn([1, 2, 3, 1])
            elif fn_name == "groupAnagrams":
                result = fn(["eat", "tea", "tan", "ate", "nat", "bat"])
            elif fn_name == "productExceptSelf":
                result = fn([1, 2, 3, 4])
            elif fn_name == "lengthOfLIS":
                result = fn([10, 9, 2, 5, 3, 7, 101, 18])
            elif fn_name == "dailyTemperatures":
                result = fn([73, 74, 75, 71, 69, 72, 76, 73])
            elif fn_name == "topKFrequent":
                result = fn([1, 1, 1, 2, 2, 3], 2)
            elif fn_name == "groupAnagrams" and "group" in fn_name.lower():
                result = fn(["eat", "tea", "tan", "ate", "nat", "bat"])
            else:
                # try calling fn with no args
                result = fn()
            results.append({
                "id": q["id"],
                "exec_ok": True,
                "result": result,
                "correct_answer": str(ca) if ca else None
            })
        except Exception as e2:
            results.append({
                "id": q["id"],
                "exec_ok": False,
                "error": str(e2)[:80],
                "correct_answer": str(ca) if ca else None
            })
    except Exception as e1:
        results.append({
            "id": q["id"],
            "exec_ok": False,
            "error": str(e1)[:80],
            "correct_answer": str(q.get("correct_answer")) if q.get("correct_answer") else None
        })
for r in results:
    print(r["id"], r["exec_ok"], "result=", r.get("result"), "ca=", r.get("correct_answer"))