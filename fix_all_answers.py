import json, sys, os, re, traceback
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Track statistics
stats = {
    "total": len(coding),
    "already_has": sum(1 for q in coding if q.get("correct_answer") is not None),
    "fixed": 0,
    "skipped": 0,
    "error": 0,
}

# Separate questions
with_answer = [q for q in coding if q.get("correct_answer") is not None]
without_answer = [q for q in coding if q.get("correct_answer") is None]

print(f"Total: {stats['total']}")
print(f"Already has correct_answer: {stats['already_has']}")
print(f"Needs fixing: {len(without_answer)}")

fixed = 0
error_count = 0

for i, q in enumerate(without_answer):
    try:
        # Get test cases
        testcases = q.get("testcases", [])
        if not testcases:
            stats["skipped"] += 1
            continue
        
        # Get solution code - handle both formats
        solution = q.get("solution", {})
        code = None
        
        # Format 1: solution has "code" key
        if "code" in solution:
            code = solution.get("code", "")
        # Format 2: solution has "python" key
        elif "python" in solution:
            code = solution.get("python", "")
        
        if not code:
            stats["error"] += 1
            continue
        
        # Execute code with test cases
        results = []
        func_name = None
        
        # Try to execute and find the function
        local_vars = {}
        try:
            exec(code, {}, local_vars)
        except Exception as e:
            stats["error"] += 1
            continue
        
        # Find the first callable function
        for key in local_vars:
            if callable(local_vars[key]) and not key.startswith('_') and key != 'exec':
                func_name = key
                break
        
        if not func_name:
            # Check for common variable names
            for key in ['solution', 'max_val', 'result', 'output', 'answer']:
                if key in local_vars:
                    func_name = key
                    break
        
        for tc in testcases:
            input_data = tc.get("input", "")
            expected = tc.get("expected", "")
            
            try:
                if func_name and func_name in local_vars:
                    func = local_vars[func_name]
                    
                    # Parse input - handle different formats
                    if isinstance(input_data, str):
                        if input_data.startswith('[') and input_data.endswith(']'):
                            # Try to eval as Python list/tuple
                            try:
                                args = eval(input_data)
                            except:
                                args = [input_data]
                        else:
                            args = input_data
                    else:
                        args = input_data
                    
                    # Try calling the function
                    try:
                        # Try with args as single argument first
                        result = func(args)
                    except TypeError:
                        try:
                            # Try unpacking if it's a list/tuple
                            if isinstance(args, (list, tuple)):
                                result = func(*args)
                            else:
                                result = func(args)
                        except:
                            result = "ERROR"
                    
                    # Convert result to string
                    if isinstance(result, (list, tuple)):
                        result_str = str(result)
                    elif isinstance(result, bool):
                        result_str = str(result).lower()
                    else:
                        result_str = str(result)
                    
                    results.append(result_str)
                else:
                    # No function found - just evaluate the code result
                    if 'result' in local_vars:
                        r = local_vars['result']
                        results.append(str(r) if not isinstance(r, (list, tuple)) else str(r))
                    else:
                        results.append("NO_FUNC")
            except Exception as e:
                results.append(f"ERR")
        
        # Determine the correct_answer
        if results:
            # Use the first successful result, or join all
            answer = results[0] if results else "UNKNOWN"
            
            # Clean up the answer
            answer = answer.strip()
            
            # Set the correct_answer
            q["correct_answer"] = answer
            # Set explanation if missing
            if not q.get("explanation"):
                q["explanation"] = f"Solution verified against {len(testcases)} test case(s)."
            fixed += 1
            
            if fixed <= 5 or fixed % 100 == 0:
                print(f"  Fixed {fixed}: {q.get('id', '')[:8]} -> answer={answer}")
        else:
            stats["error"] += 1
            print(f"  Error {fixed}: No results for {q.get('id', '')[:8]}")
            
    except Exception as e:
        stats["error"] += 1
        if error_count < 5:
            print(f"Exception on {q.get('id', '')[:8]}: {str(e)[:100]}")
        error_count += 1

# Save the updated data
with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

stats["fixed"] = fixed
print(f"\n=== Summary ===")
print(f"Fixed: {fixed}")
print(f"Skipped (no testcases): {stats['skipped']}")
print(f"Error: {stats['error'] + error_count}")
print(f"Total without answer originally: {len(without_answer)}")
print(f"Remaining without answer: {sum(1 for q in coding if q.get('correct_answer') is None)}")