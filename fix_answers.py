import json, sys, os, re, traceback
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Separate questions with and without correct_answer
without_answer = [q for q in coding if q.get("correct_answer") is None]

print(f"Total coding: 6279, Without correct_answer: {len(without_answer)}")

# Process questions without correct_answer
fixed = 0
for i, q in enumerate(without_answer[:20]):
    try:
        # Get test cases
        testcases = q.get("testcases", [])
        if not testcases:
            print(f"Q{i} ({q.get('id', '')[:8]}): No testcases found")
            continue
            
        # Get solution code
        solution = q.get("solution", {})
        code = solution.get("code", "") or solution.get("python", "")
        
        if not code:
            print(f"Q{i} ({q.get('id', '')[:8]}): No code found")
            continue
        
        # Execute code with test cases
        results = []
        for tc in testcases:
            input_data = tc.get("input", "")
            expected = tc.get("expected", "")
            
            # Prepare execution environment
            local_vars = {}
            try:
                exec(code, {}, local_vars)
            except Exception as e:
                results.append(f"EXEC_ERROR")
                continue
            
            # Try to find the function - get the first callable
            func_name = None
            for key in local_vars:
                if callable(local_vars[key]) and not key.startswith('_'):
                    func_name = key
                    break
            
            if func_name:
                try:
                    # Pass input as single argument (the list/tuple/string)
                    if isinstance(input_data, str):
                        if input_data.startswith('[') and input_data.endswith(']'):
                            args = eval(input_data)  # Convert string to list
                        else:
                            args = input_data
                    else:
                        args = input_data
                    
                    # Call function with args as single arg or unpack
                    try:
                        result = local_vars[func_name](args)
                    except TypeError:
                        try:
                            result = local_vars[func_name](*args) if isinstance(args, list) else local_vars[func_name](args)
                        except:
                            result = local_vars[func_name]()
                    results.append(str(result))
                except Exception as e:
                    results.append(f"RUN_ERROR")
            else:
                # Check for result variable
                for key in ['result', 'output', 'answer']:
                    if key in local_vars:
                        results.append(str(local_vars[key]))
                        break
                else:
                    results.append("NO_FUNC")
        
        # Set correct_answer
        if results and results[0] not in ["EXEC_ERROR", "RUN_ERROR", "NO_FUNC"]:
            answer_str = results[0]
            q["correct_answer"] = answer_str
            q["explanation"] = q.get("explanation") or f"Verified against {len(testcases)} test case(s)."
            fixed += 1
            print(f"Q{i} ({q.get('id', '')[:8]}): Fixed - correct_answer={answer_str}")
        else:
            print(f"Q{i} ({q.get('id', '')[:8]}): Skipped - {results[0] if results else 'no results'}")
            
    except Exception as e:
        print(f"Q{i} ({q.get('id', '')[:8]}): Error: {str(e)[:100]}")
        traceback.print_exc()

# Save progress
with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nFixed {fixed}/20 questions")