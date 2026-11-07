"""CI test: verify no file outside gamification.py modifies protected gamification fields.

Run from backend/:
  python scripts/test_gamification_violations.py

Checks for direct $inc/$set on gamification_collection with protected fields:
  diamonds, coins, stars_total, streak, weekly_league_xp, monthly_league_xp

Exit code 0 = pass, 1 = violation found.
"""
import sys
import os
import re

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")

# Protected fields that ONLY gamification.py may write via $inc/$set
PROTECTED = {"diamonds", "coins", "stars_total", "streak", "weekly_league_xp", "monthly_league_xp"}

# Files that ARE allowed to write these fields
ALLOWED = {"gamification.py", "gamification_core.py"}


def check_file(filepath: str, rel_path: str) -> list:
    """Check if file does $inc/$set on protected fields on gamification_collection."""
    if os.path.basename(filepath) in ALLOWED:
        return []

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    violations = []

    # Find all gamification_collection.update_one/update_many calls
    # and check if they contain $inc/$set with protected fields
    for match in re.finditer(
        r'gamification_collection\s*\.\s*update_(?:one|many)\s*\(',
        content,
    ):
        # Find the matching closing paren (simple brace counting)
        start = match.start()
        depth = 0
        in_string = False
        string_char = None
        end = start

        for i in range(start, min(start + 2000, len(content))):
            c = content[i]
            if in_string:
                if c == string_char and content[i - 1] != "\\":
                    in_string = False
            else:
                if c in ('"', "'"):
                    in_string = True
                    string_char = c
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        end = i
                        break

        block = content[start:end + 1]

        # Check for $inc or $set with protected fields
        for op_match in re.finditer(r'["\']?\$(?:inc|set)["\']?\s*:\s*\{', block):
            # Extract the dict content
            op_start = op_match.end()
            op_depth = 1
            op_end = op_start
            for j in range(op_start, len(block)):
                if block[j] == "{":
                    op_depth += 1
                elif block[j] == "}":
                    op_depth -= 1
                    if op_depth == 0:
                        op_end = j
                        break
            dict_content = block[op_start:op_end]

            for field in PROTECTED:
                if re.search(rf'["\']?{re.escape(field)}["\']?\s*:', dict_content):
                    line_num = content[:start].count("\n") + 1
                    violations.append((rel_path, line_num, field, dict_content.strip()[:100]))

    return violations


def main():
    all_violations = []
    for root, _, files in os.walk(APP_DIR):
        for fname in sorted(files):
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, os.path.dirname(APP_DIR))
            all_violations.extend(check_file(fpath, rel))

    if all_violations:
        print(f"VIOLATIONS: {len(all_violations)}")
        for path, ln, fld, txt in all_violations:
            print(f"  {path}:{ln} [{fld}]")
            print(f"    {txt}")
        sys.exit(1)
    else:
        print("PASS: No gamification law violations")
        sys.exit(0)


if __name__ == "__main__":
    main()
