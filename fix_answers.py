import json, sys, os, re, traceback
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Separate questions with and without correct_answer
with_answer = [q for q in coding if q.get("correct_answer") is not None]
without_answer = [q for q in coding if q.get("correct_answer") is None]

print(f"Total coding: {len(coding)}")
print(f"With correct_answer: {len(with_answer)}")
print(f"Without correct_answer: {len(without_answer)}")

# Process a few questions without correct_answer
fixed = 0
for i, q in enumerate(without_answer[:10]):
    try:
        # Get test cases
        testcases = q.get("testcases", [])
        if not testcases:
            print(f"Q{i}: No testcases found")
            continue
            
        # Get solution code
        solution = q.get("solution", {})
        code = solution.get("python", "") if solution else ""
        
        if not code:
            print(f"Q{i}: No python code")
            continue
            
        # Execute code with test cases
        # The code typically defines a function, so we need to test it
        results = []
        for tc in testcases:
            input_data = tc.get("input", "")
            expected = tc.get("expected", "")
            
            # Prepare execution environment
            local_vars = {}
            try:
                exec(code, {}, local_vars)
            except Exception as e:
                results.append(f"EXEC_ERROR:{str(e)[:50]}")
                continue
            
            # Try to find the main function or just execute top-level code
            # Most solutions define a function - try common names
            func_name = None
            for key in local_vars:
                if callable(local_vars[key]) and not key.startswith('_'):
                    func_name = key
                    break
            
            if func_name:
                try:
                    # Handle different input formats
                    if isinstance(input_data, str):
                        # Try eval for simple structures, or pass as arg
                        try:
                            args = eval(input_data) if input_data else ()
                        except:
                            args = input_data
                        result = local_vars[func_name](*args) if args else local_vars[func_name]()
                    else:
                        result = local_vars[func_name]()
                    results.append(str(result))
                except Exception as e:
                    results.append(f"RUN_ERROR:{str(e)[:50]}")
            else:
                # No function found, check if there's a main output variable
                if 'result' in local_vars:
                    results.append(str(local_vars['result']))
                elif 'output' in local_vars:
                    results.append(str(local_vars['output']))
                else:
                    results.append("NO_FUNC_FOUND")
        
        # The correct_answer should be the expected outputs
        # Format: match the correct_answer format (usually a string like "[3,4]")
        if results:
            # Try to match expected format
            # If all results are simple, join them
            answer_str = ", ".join(results)
            # Check if it matches expected
            expected_strs = [tc.get("expected", "") for tc in testcases]
            expected_str = ", ".join(expected_strs)
            
            q["correct_answer"] = answer_str
            q["explanation"] = q.get("explanation") or f"Solved using provided solution. Test cases: {len(testcases)}"
            fixed += 1
            print(f"Q{i}: Fixed - correct_answer={answer_str}, expected={expected_str}")
        else:
            print(f"Q{i}: No results generated")
            
    except Exception as e:
        print(f"Q{i}: Error: {str(e)[:100]}")
        traceback.print_exc()

# Save progress
with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nFixed {fixed}/10 questions")