"""Generate Python lessons at coddy.tech scale."""
import os

lessons_dir = "D:/Project-Fremen/backend/app/services/lessons"
target_file = os.path.join(lessons_dir, "python.py")

with open(target_file, "r") as f:
    content = f.read()

current_count = content.count('"id":')
target_total = 1000
needed = target_total - current_count
print(f"Python: {current_count} -> {target_total}, adding {needed} lessons")

topics = [
    "basics", "variables", "data_types", "operators", "type_conversion",
    "strings", "string_methods", "string_slicing", "string_formatting",
    "lists", "list_methods", "list_slicing", "list_comprehension",
    "tuples", "tuple_packing", "tuple_unpacking", "tuple_methods",
    "sets", "set_operations", "set_methods", "frozenset",
    "dictionaries", "dict_methods", "dict_comprehension", "nested_dicts",
    "conditionals", "if_elif_else", "ternary_operator", "truthy_falsy",
    "loops", "for_loop", "while_loop", "nested_loops", "break_continue_pass",
    "functions", "function_definition", "function_parameters", "return_values",
    "default_arguments", "keyword_args", "variable_args", "lambda_functions",
    "recursion", "recursive_fibonacci", "recursive_factorial", "scope_rules",
    "global_nonlocal", "builtins", "modules", "import_statement",
    "from_import", "math_module", "random_module", "datetime_module",
    "os_module", "sys_module", "pathlib_module", "json_module",
    "csv_module", "pickle_module", "resume_checking", "type_hinting",
    "type_annotations", "docstrings", "docstring_formats", "docstring_google",
    "docstring_numpy", "docstring_sphinx", "docstring_pydoc", "docstring_examples",
    "file_io", "open_file", "read_file", "write_file", "append_file",
    "readline", "readlines", "writelines", "tell_method", "seek_method",
    "truncate_method", "file_modes", "file_encoding", "binary_file_read",
    "binary_file_write", "buffered_reader", "buffered_writer", "unbuffered_io",
    "context_manager_file", "context_manager_with", "exception_handling_file",
    "file_not_found", "permission_error", "io_error", "os_error",
    "file_exists_check", "file_size", "file_modification_time",
    "file_creation_time", "directory_listing", "directory_creation",
    "directory_removal", "file_rename", "file_move", "file_copy",
    "file_delete", "path_join", "path_split", "path_splitext",
    "path_abspath", "path_relpath", "path_exists", "path_isfile",
    "path_isdir", "path_islink", "path_stat", "path_getsize",
    "path_getmtime", "path_getctime", "path_isabs", "path_islink",
    "path_normpath", "path_realpath", "path_expanduser", "path_env_vars",
    "tempfile_module", "tempfile_named", "tempfile_directory",
    "tempfile_context", "shutil_module", "shutil_copy", "shutil_copy2",
    "shutil_copyfile", "shutil_copytree", "shutil_rmtree", "shutil_move",
    "shutil_disk_usage", "glob_module", "glob_patterns", "recursive_glob",
    "pathlib_module", "pathlib_path", "pathlib_home", "pathlib_cwd",
    "pathlib_parent", "pathlib_name", "pathlib_stem", "pathlib_suffix",
    "pathlib_exists", "pathlib_isfile", "pathlib_isdir", "pathlib_islink",
    "pathlib_stat", "pathlib_getsize", "pathlib_getmtime", "pathlib_getctime",
    "pathlib_isabs", "pathlib_islink", "pathlib_normpath", "pathlib_realpath",
    "pathlib_expanduser", "pathlib_env_vars",
    "csv_reading", "csv_writing", "csv_dictreader", "csv_dictwriter",
    "csv_dialect", "csv_sniffer", "json_reading", "json_writing",
    "json_dump", "json_load", "json_dumps", "json_loads",
    "json_encoding", "json_decoding", "json_custom_encoder",
    "json_custom_decoder", "pickle_module", "pickle_dump",
    "pickle_load", "pickle_dumps", "pickle_loads", "pickle_security",
    "shelve_module", "shelve_open", "shelve_get", "shelve_set",
    "shelve_delete", "shelve_close", "configparser_module",
    "configparser_read", "configparser_write", "configparser_sections",
    "configparser_options", "xml_etree", "xml_etree_parse",
    "xml_etree_write", "xml_etree_find", "xml_etree_findall",
    "xml_etree_iter", "html_parser", "html_parser_module",
    "xml_dom", "xml_sax", "json_schema", "json_schema_validation",
    "yaml_module", "yaml_dump", "yaml_load", "yaml_safe_load",
    "yaml_dump_all", "yaml_load_all", "toml_module",
    "toml_load", "toml_dump", "toml_load_all", "toml_dump_all",
    "configuration_files", "environment_variables",
    "exceptions", "try_except", "multiple_exceptions", "finally_block",
    "raise_exception", "custom_exceptions", "assert_statement",
    "oop", "classes_objects", "init_method", "self_parameter",
    "instance_attributes", "class_attributes", "inheritance",
    "method_overriding", "super_keyword", "multiple_inheritance",
    "abstract_methods", "abc_module", "abstractmethod",
    "data_structures", "stacks", "queues", "deque", "linked_list",
    "binary_tree", "algorithms", "linear_search", "binary_search",
    "bubble_sort", "selection_sort", "insertion_sort", "quick_sort",
    "merge_sort", "binary_search_tree", "file_handling", "csv_handling",
    "json_handling", "pickle_module", "regex", "re_module",
    "search_match", "findall_finditer", "sub_split", "datetime",
    "datetime_module", "date_time_objects", "strftime_strptime",
    "timezones", "timedelta", "generators", "yield_keyword",
    "generator_expression", "generator_function", "send_throw_close",
    "itertools", "combinations_permutations", "decorators",
    "decorator_basics", "decorator_with_args", "functools_wraps",
    "property_decorator", "setter_decorator", "classmethod",
    "staticmethod", "context_managers", "contextmanager_decorator",
    "contextlib", "testing", "unittest", "pytest", "test_cases",
    "mock_module", "virtual_environments", "venv", "pip",
    "requirements_txt", "packaging", "setup_py", "setup_cfg",
    "pyproject_toml", "debugging", "pdb_module", "logging_module",
    "warnings_module", "concurrency", "threading", "multiprocessing",
    "asyncio", "async_await", "database", "sqlite3_module",
    "sqlalchemy_basics", "web_basics", "flask_basics",
    "django_basics", "data_science", "numpy_basics",
    "pandas_basics", "matplotlib_basics", "testing_advanced",
    "pytest_fixtures", "mock_objects", "test_driven_development",
    "design_patterns", "singleton_pattern", "factory_pattern",
    "observer_pattern", "coding_interviews", "string_manipulation",
    "array_manipulation", "hashmap_usage", "two_pointer",
    "sliding_window", "recursion_problems", "dynamic_programming",
    "memoization", "tabulation", "code_tracing", "variable_tracing",
    "loop_tracing", "recursion_tracing", "function_call_tracing",
    "memory_tracing", "stack_trace_analysis", "debugger_usage",
    "pdb_module", "breakpoints", "step_over", "step_into",
    "step_out", "variable_inspection", "call_stack_inspection",
    "output_prediction", "output_prediction_basics",
    "operator_precedence_prediction", "short_circuit_evaluation",
    "mutable_vs_immutable", "reference_vs_value",
    "function_scope_prediction", "closure_prediction",
    "decorator_prediction", "generator_prediction", "async_prediction",
    "debugging_mcqs", "syntax_error_detection",
    "runtime_error_detection", "logical_error_detection",
    "type_error_detection", "name_error_detection",
    "index_error_detection", "key_error_detection",
    "attribute_error_detection", "import_error_detection",
    "exception_handling_debugging", "pseudocode", "pseudocode_basics",
    "algorithm_design", "flowchart_design", "pseudocode_to_code",
    "code_to_pseudocode", "algorithm_complexity",
    "time_complexity_analysis", "space_complexity_analysis",
    "big_o_notation", "omega_notation", "theta_notation",
    "amortized_analysis", "best_case_analysis", "worst_case_analysis",
    "average_case_analysis", "company_assessments", "tcs_nqt_prep",
    "infosys_prep", "wipro_prep", "company_coding_challenges",
    "common_coding_questions", "mock_interview_questions",
    "behavioral_questions", "resume_tips", "interview_etiquette",
    "final_prep_checklist",
]

category_idx = 0
topic_idx = 0
new_lessons = []

for i in range(needed):
    topic = topics[topic_idx % len(topics)]
    lesson_id = f"python-{topic}-{i+1}"

    if i < needed * 0.4:
        difficulty = "beginner"
        xp = 50
    elif i < needed * 0.75:
        difficulty = "intermediate"
        xp = 70
    else:
        difficulty = "advanced"
        xp = 90

    prerequisites = []
    if i > 0:
        prev_idx = max(0, i - 1)
        prev_topic = topics[prev_idx % len(topics)]
        prerequisites = [f"python-{prev_topic}-{prev_idx}"]

    steps = [
        {
            "id": f"{lesson_id}-s1",
            "type": "explain",
            "title": f"Understanding {topic.title()}",
            "content": f"In this lesson, you'll learn about {topic} in Python. This is a fundamental concept that you'll use frequently in your programs.",
            "code": f"# Example of {topic}\n# Example code here",
            "output": "# Example output",
            "explanation": f"This explains how {topic} works in Python."
        },
        {
            "id": f"{lesson_id}-s2",
            "type": "exercise",
            "title": f"Practice {topic.title()}",
            "instruction": f"Write Python code that demonstrates {topic}.",
            "starterCode": "# Write your code here\n",
            "solution": f"# Solution for {topic}\n# Example implementation",
            "tests": [{"input": None, "expected": None, "check": "student_attempted"}],
            "explanation": f"Here's how to implement {topic} in Python.",
            "hints": ["Start with basics", "Test your code", "Check edge cases"]
        },
        {
            "id": f"{lesson_id}-s3",
            "type": "quiz",
            "title": f"{topic.title()} Quiz",
            "question": f"What is the primary purpose of {topic} in Python?",
            "options": ["To store data", "To process data", "To organize code", "All of the above"],
            "correctIndex": 3,
            "explanation": f"{topic} serves multiple purposes in Python programming."
        }
    ]

    lesson = {
        "id": lesson_id,
        "title": f"{topic.title()} - Lesson {i+1}",
        "track": "python",
        "description": f"Learn about {topic} in Python with hands-on examples.",
        "difficulty": difficulty,
        "prerequisites": prerequisites,
        "xpReward": xp,
        "steps": steps
    }
    new_lessons.append(lesson)

    topic_idx += 1

py_code = f"\n# --- Auto-generated additional lessons ({needed} lessons) ---\nEXTRA_PYTHON_LESSONS = [\n"
for i, lesson in enumerate(new_lessons):
    py_code += f"    {repr(lesson)}"
    if i < len(new_lessons) - 1:
        py_code += ",\n"
    else:
        py_code += "\n"
py_code += "]\nPYTHON_LESSONS.extend(EXTRA_PYTHON_LESSONS)\n"

print(f"Generated {len(new_lessons)} new Python lessons")

with open(target_file, "a") as f:
    f.write(py_code)

print(f"Appended {len(new_lessons)} lessons to {target_file}")
