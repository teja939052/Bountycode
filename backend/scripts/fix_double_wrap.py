"""Fix double-wrapped main() functions in questions_bank.json."""
from __future__ import annotations

import ast
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

LOGGER = logging.getLogger("fix_double_wrap")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

DATA_DIR = Path(__file__).resolve().parents[1] / "app" / "data"


def fix_wrapped_code(src: str) -> str:
    """Remove duplicate wrappers and keep only one clean wrapper."""
    # Check if already wrapped
    has_pp_main = "_pp_main" in src
    has_main = "def main():" in src
    
    if not has_pp_main or not has_main:
        return src
    
    # Split by the _pp_main definition
    parts = src.split("def _pp_main")
    if len(parts) < 2:
        return src
    
    # Find the last occurrence of the wrapper start
    # We want to keep only one wrapper before main()
    # Strategy: find the first _pp_main and remove everything before main()
    # that's not part of the wrapper
    
    # Simpler: just replace the whole thing with a single clean wrapper
    wrapper = """import sys
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
    
    # Extract just the main() function and everything after it
    main_idx = src.rfind("def main(")
    if main_idx == -1:
        main_idx = src.rfind("def main():")
    if main_idx == -1:
        return src
    
    main_and_after = src[main_idx:]
    return wrapper + main_and_after


def main() -> None:
    path = DATA_DIR / "questions_bank.json"
    LOGGER.info("Loading %s", path)
    data = json.loads(path.read_text(encoding="utf-8"))

    fixed = 0
    for q in data:
        if str(q.get("type", "")).lower() != "coding":
            continue
        sol = q.get("solution") or {}
        if not isinstance(sol, dict):
            continue
        code = str(sol.get("code") or "")
        if not code or "_pp_main" not in code:
            continue

        new_code = fix_wrapped_code(code)
        if new_code != code:
            sol["code"] = new_code
            fixed += 1

    LOGGER.info("Fixed %d double-wrapped functions", fixed)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    LOGGER.info("Saved to %s", path)


if __name__ == "__main__":
    main()
