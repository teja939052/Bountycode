import re

filepath = 'D:/Project-Fremen/backend/app/routes/questions.py'
with open(filepath, 'r') as f:
    content = f.read()

old_error_block = """    if not execution_result.get("success", False):
        raise HTTPException(
            status_code=400,
            detail=execution_result.get("error", "Failed to execute test cases"),
        )"""

new_error_block = """    if not execution_result.get("success", False):
        raw_error = execution_result.get("error", "Failed to execute test cases")
        error_explanation = _explain_compiler_error(raw_error, source_code, language)
        raise HTTPException(
            status_code=400,
            detail=raw_error,
            error_explanation=error_explanation,
        )"""

if old_error_block in content:
    content = content.replace(old_error_block, new_error_block)
    print("Replaced error handling block")
else:
    print("ERROR: Could not find error handling block")

# Add the _explain_compiler_error function after the serializer function
serializer_fn = """def serialize_question(q):
    q["id"] = str(q.pop("_id"))
    if not q.get("companies"):
        company = q.get("company")
        if isinstance(company, list):
            q["companies"] = company
        elif isinstance(company, str) and company:
            q["companies"] = [company]
        else:
            q["companies"] = assign_companies()
    return q


def _question_title(q: dict) -> str:
    return q.get("question") or q.get("question_title", "")"""

explanation_function = """def serialize_question(q):
    q["id"] = str(q.pop("_id"))
    if not q.get("companies"):
        company = q.get("company")
        if isinstance(company, list):
            q["companies"] = company
        elif isinstance(company, str) and company:
            q["companies"] = [company]
        else:
            q["companies"] = assign_companies()
    return q


def _question_title(q: dict) -> str:
    return q.get("question") or q.get("question_title", "")


def _explain_compiler_error(error_message: str, source_code: str, language: str) -> str:
    \"\"\"Provide a user-friendly explanation for code execution errors.\"\"\"
    error_lower = error_message.lower()

    if "compile" in error_lower or "syntax" in error_lower:
        return (
            "Your code has a syntax error that stopped compilation before it could run. "
            "This means the code has invalid grammar for the chosen language. "
            "Common causes:\\n"
            "- Missing colons at the end of if/for/while statements (Python)\\n"
            "- Missing semicolons or braces (C/Java/JavaScript)\\n"
            "- Misspelled keywords or variable names\\n"
            "- Missing closing parentheses, brackets, or braces\\n"
            "Please review the error message above and check your syntax carefully."
        )
    elif "timeout" in error_lower or "timelimit" in error_lower or "time limit" in error_lower:
        return (
            "Your code exceeded the time limit for execution. "
            "This usually means your solution has an inefficient algorithm with too high time complexity. "
            "Consider:\\n"
            "- Using a more efficient algorithm (e.g., binary search instead of linear scan)\\n"
            "- Avoiding nested loops where possible\\n"
            "- Using appropriate data structures (hash maps, sets, heaps)"
        )
    elif "memory" in error_lower or "mle" in error_lower or "out of memory" in error_lower:
        return (
            "Your code exceeded the memory limit. "
            "This usually means your solution is using too much memory. "
            "Consider:\\n"
            "- Using more memory-efficient data structures\\n"
            "- Avoiding storing unnecessary data\\n"
            "- Processing data in a streaming fashion instead of loading everything at once"
        )
    elif "runtime" in error_lower or "exception" in error_lower or "error" in error_lower:
        return (
            "Your code crashed during execution. "
            "This is typically caused by:\\n"
            "- Division by zero\\n"
            "- Accessing an array index out of bounds\\n"
            "- Using a null/None value where an object is expected\\n"
            "- Infinite loops that eventually exhaust resources\\n"
            "Check your edge cases and make sure all variables are properly initialized."
        )
    else:
        return (
            "Your code failed to produce the expected output. "
            "This could be due to:\\n"
            "- A logic error in your algorithm\\n"
            "- Not handling all edge cases (empty input, single element, etc.)\\n"
            "- Integer overflow in languages like C++ or Java\\n"
            "Review the algorithm logic and test with different inputs to find the bug."
        )


def _question_title(q: dict) -> str:
    return q.get("question") or q.get("question_title", "")"""

content = content.replace(serializer_fn, explanation_function)
print("Added explanation function")

with open(filepath, 'w') as f:
    f.write(content)
print(f"Updated {filepath}")
print(f"New size: {len(content)} chars")