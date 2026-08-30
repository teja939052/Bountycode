import json, sys, os, re, traceback
sys.path.insert(0, r"D:\Project-Fremen\backend")

with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

coding = [q for q in data if q.get("type") == "coding"]

# Find the 3,400 questions with test_cases (underscore format) and no correct_answer
format3 = [q for q in coding if q.get("test_cases") and q.get("correct_answer") is None]
format3_with_answer = [q for q in coding if q.get("test_cases") and q.get("correct_answer") is not None]

print(f"Total coding: {len(coding)}")
print(f"With test_cases format: {len(format3) + len(format3_with_answer)}")
print(f"Without answer (need fixing): {len(format3)}")
print(f"With answer already: {len(format3_with_answer)}")

# Fix the format3 questions
fixed = 0
review = 0

for i, q in enumerate(format3):
    try:
        test_cases = q.get("test_cases", [])
        if not test_cases:
            review += 1
            continue
        
        solution = q.get("solution", "")
        if not solution:
            review += 1
            continue
        
        # The solution is often a method like "def maxSubArray(self, nums):"
        # We need to execute it with the test case inputs
        
        # Prepare execution environment
        local_vars = {}
        try:
            # Execute the method definition
            exec(solution, {"__builtins__": {}}, local_vars)
        except Exception as e:
            review += 1
            continue
        
        # Find the main method/function
        method_name = None
        # Try common method names
        for key in local_vars:
            if callable(local_vars[key]) and not key.startswith('_'):
                method_name = key
                break
        
        if not method_name:
            # Try to find from the solution code
            m = re.search(r'def\s+(\w+)\s*\(', solution)
            if m:
                method_name = m.group(1)
        
        if not method_name:
            review += 1
            continue
        
        method = local_vars.get(method_name)
        if not method:
            review += 1
            continue
        
        # Execute with each test case and collect results
        results = []
        for tc in test_cases:
            input_data = tc.get("input", {})
            expected = tc.get("output", "")
            
            try:
                # The method typically takes specific arguments
                # Common patterns: method(nums), self.nums, etc.
                # Try passing the main data structure
                
                if isinstance(input_data, dict):
                    # Extract the main array/target from the dict
                    nums = input_data.get("nums", [])
                    target = input_data.get("target", None)
                    
                    # Call the method
                    if target is not None:
                        result = method(nums, target)
                    else:
                        result = method(nums)
                    
                    # Format result
                    if isinstance(result, (list, tuple)):
                        result_str = str(result)
                    elif isinstance(result, bool):
                        result_str = str(result).lower()
                    else:
                        result_str = str(result)
                    
                    results.append(result_str)
                else:
                    results.append("UNKNOWN_FORMAT")
            except Exception as e:
                results.append(f"ERROR:{str(e)[:30]}")
        
        # Determine correct_answer
        if results:
            # Use the first non-error result, or join results
            answer = results[0] if results else "UNKNOWN"
            # Clean up
            answer = answer.strip()
            
            # Only set if it looks like a valid answer (not "computed" or "ERROR")
            if answer and answer.lower() not in ['computed', 'error', 'unknown', 'none']:
                q["correct_answer"] = answer
                q["explanation"] = q.get("explanation") or f"Executed solution against {len(test_cases)} test case(s)."
                fixed += 1
            else:
                review += 1
                q["correct_answer"] = "REVIEW_NEEDED"
                q["explanation"] = q.get("explanation") or "Answer requires manual review - execution produced placeholder output"
        else:
            review += 1
            q["correct_answer"] = "REVIEW_NEEDED"
            q["explanation"] = q.get("explanation") or "Answer requires manual review"
    
    except Exception as e:
        review += 1
        if review <= 5:
            print(f"Exception on {q.get('id', '')[:8]}: {str(e)[:100]}")
        q["correct_answer"] = "REVIEW_NEEDED"
        q["explanation"] = q.get("explanation") or "Answer requires manual review - error"

# Save
with open(r"D:\Project-Fremen\backend\app\data\questions_bank_curated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\n=== Format 3 Fix Summary ===")
print(f"Fixed: {fixed}")
print(f"Review needed: {review}")
print(f"Remaining without answer: {sum(1 for q in coding if q.get('correct_answer') is None)}")
print(f"Total with answer: {sum(1 for q in coding if q.get('correct_answer') is not None)}")