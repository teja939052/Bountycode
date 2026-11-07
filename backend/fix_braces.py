with open('app/content/world2_problem_solver.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the problematic line
idx = content.find('"Prove It: Maximum Depth"')
if idx >= 0:
    # Find test_cases after this
    tc_idx = content.find('test_cases=[', idx)
    if tc_idx >= 0:
        snippet = content[tc_idx:tc_idx+400]
        print("test_cases snippet:")
        print(snippet)
        
        # Count braces
        opens = snippet.count('{')
        closes = snippet.count('}')
        print(f"\nOpening braces: {opens}")
        print(f"Closing braces: {closes}")
        print(f"Difference: {opens - closes}")
else:
    print("Not found")
