import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Analyze code patterns
code_lengths = []
has_loops = []
has_recursion = []
uses_input = []
uses_print = []

for q in coding[:100]:  # Sample first 100
    solution = q.get("solution", {})
    code = solution.get("code", "") or solution.get("python", "")
    if code:
        code_lengths.append(len(code))
        has_loops.append("for" in code or "while" in code)
        has_recursion.append("def " in code and code.count("def ") > 1)
        uses_input.append("input(" in code)
        uses_print.append("print(" in code)

print(f"Sample of 100 coding questions:")
print(f"  Questions with code: {len([q for q in coding[:100] if q.get('solution', {}).get('code') or q.get('solution', {}).get('python')])}/100")
print(f"  Average code length: {sum(code_lengths)/len(code_lengths) if code_lengths else 0:.0f}")
print(f"  Has loops: {sum(has_loops)}/{len(has_loops)}")
print(f"  Has recursion: {sum(has_recursion)}/{len(has_recursion)}")
print(f"  Uses input(): {sum(uses_input)}/{len(uses_input)}")
print(f"  Uses print(): {sum(uses_print)}/{len(uses_print)}")

# Check all 6279
total_with_code = 0
total_loops = 0
total_recursion = 0
total_input = 0
total_print = 0

for q in coding:
    solution = q.get("solution", {})
    code = solution.get("code", "") or solution.get("python", "")
    if code:
        total_with_code += 1
        total_loops += 1 if ("for" in code or "while" in code) else 0
        total_recursion += 1 if ("def " in code and code.count("def ") > 1) else 0
        total_input += 1 if "input(" in code else 0
        total_print += 1 if "print(" in code else 0

print(f"\nAll {len(coding)} coding questions:")
print(f"  Questions with code: {total_with_code}")
print(f"  Has loops: {total_loops}/{total_with_code} ({total_loops/total_with_code*100 if total_with_code else 0:.1f}%)")
print(f"  Has recursion: {total_recursion}/{total_with_code} ({total_recursion/total_with_code*100 if total_with_code else 0:.1f}%)")
print(f"  Uses input(): {total_input}/{total_with_code} ({total_input/total_with_code*100 if total_with_code else 0:.1f}%)")
print(f"  Uses print(): {total_print}/{total_with_code} ({total_print/total_with_code*100 if total_with_code else 0:.1f}%)")