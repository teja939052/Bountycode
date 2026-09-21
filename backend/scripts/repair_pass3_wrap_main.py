"""Third-pass repair: wrap main() functions to accept test inputs.

For coding questions where the only callable function is main() with no args,
wrap the code so main() can accept the test input as an argument.
"""
from __future__ import annotations

import ast
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LOGGER = logging.getLogger("repair_pass3")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

DATA_DIR = Path(__file__).resolve().parents[1] / "app" / "data"


def wrap_main_to_accept_input(src: str) -> str:
    """Wrap main() to accept a stdin string as first argument and capture output."""
    try:
        tree = ast.parse(src)
    except Exception:
        return src

    has_main = False
    main_args = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "main":
            has_main = True
            main_args = len(node.args.args)
            break

    if not has_main or main_args > 0:
        return src

    # Wrap: add a wrapper that calls main with stdin content and captures output
    wrapper = """
import sys
from io import StringIO
import ast

def _pp_main(*args, **kwargs):
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    if args:
        input_data = str(args[0])
    elif kwargs:
        parts = []
        for k, v in kwargs.items():
            parts.append(f"{k} = {repr(v)}")
        input_data = "\\n".join(parts)
    else:
        input_data = ""
    sys.stdin = StringIO(input_data)
    sys.stdout = StringIO()
    try:
        main()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

"""
    return wrapper + src


def main() -> None:
    path = DATA_DIR / "questions_bank.json"
    LOGGER.info("Loading %s", path)
    data = json.loads(path.read_text(encoding="utf-8"))

    wrapped = 0
    for q in data:
        if str(q.get("type", "")).lower() != "coding":
            continue
        sol = q.get("solution") or {}
        if not isinstance(sol, dict):
            continue
        code = str(sol.get("code") or "")
        if not code:
            continue

        new_code = wrap_main_to_accept_input(code)
        if new_code != code:
            sol["code"] = new_code
            wrapped += 1

    LOGGER.info("Wrapped %d main() functions", wrapped)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Saved to %s", path)


if __name__ == "__main__":
    main()
