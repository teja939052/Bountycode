import json, sys
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Analyze code patterns - first 100
sample = coding[:100]

code_lengths = []
has_loops = []
has_recursion = []
uses_input = []
uses_print = []

for q in sample:
    solution = q.get("solution", {})
    code = ""
    if isinstance(solution, dict):
        code = solution.get("code", "") or solution.get("python", "")
    elif isinstance(solution, str):
        code = solution
    
    if code:
        code_lengths.append(len(code))
        has_loops.append("for" in code or "while" in code)
        # Check for recursion - function calling itself
        recursion = False
        if "def " in code:
            # Simple check for self-referential function
            func_names = [line.split("def ")[1].split("(")[0].strip() for line in code.split("\n") if line.startswith("def ")]
            for name in func_names:
                if name in code:
                    recursion = True
        has_recursion.append(recursion)
        uses_input.append("input(" in code)
        uses_print.append("print(" in code)

print(f"Sample of 100 coding questions:")
print(f"  Questions with code: {len(code_lengths)}/{len(sample)}")
print(f"  Average code length: {sum(code_lengths)/len(code_lengths):.0f}")
print(f"  Has loops: {sum(has_loops)}/{len(has_loops)} ({sum(has_loops)/len(has_loops)*100:.1f}%)")
print(f"  Has recursion: {sum(has_recursion)}/{len(has_recursion)} ({sum(has_recursion)/len(has_recursion)*100:.1f}%)")
print(f"  Uses input(): {sum(uses_input)}/{len(uses_input)}")
print(f"  Uses print(): {sum(uses_print)}/{len(uses_print)}")

# Now check all 6279
total_with_code = 0
total_loops = 0
total_recursion = 0
total_input = 0
total_print = 0

for q in coding:
    solution = q.get("solution", {})
    code = ""
    if isinstance(solution, dict):
        code = solution.get("code", "") or solution.get("python", "")
    elif isinstance(solution, str):
        code = solution
    
    if code:
        total_with_code += 1
        total_loops += 1 if ("for" in code or "while" in code) else 0
        # Check for recursion
        recursion = False
        if "def " in code:
            func_names = [line.split("def ")[1].split("(")[0].strip() for line in code.split("\n") if line.startswith("def ")]
            for name in func_names:
                if name in code:
                    recursion = True
        total_recursion += 1 if recursion else 0
        total_input += 1 if "input(" in code else 0
        total_print += 1 if "print(" in code else 0

print(f"\nAll {len(coding)} coding questions:")
print(f"  Questions with code: {total_with_code}")
print(f"  Has loops: {total_loops}/{total_with_code} ({total_loops/total_with_code*100 if total_with_code else 0:.1f}%)")
print(f"  Has recursion: {total_recursion}/{total_with_code} ({total_recursion/total_with_code*100 if total_with_code else 0:.1f}%)")
print(f"  Uses input(): {total_input}/{total_with_code} ({total_input/total_with_code*100 if total_with_code else 0:.1f}%)")
print(f"  Uses print(): {total_print}/{total_with_code} ({total_print/total_with_code*100 if total_with_code else 0:.1f}%)")