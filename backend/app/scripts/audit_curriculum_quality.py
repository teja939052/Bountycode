"""Print a JSON quality audit of the programming curriculum.

Run from backend/: python -m app.scripts.audit_curriculum_quality
Optional language filters: --languages python,java
"""
import argparse
import json

from app.services.curriculum_quality import audit_curriculum


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--languages", default="", help="Comma-separated language IDs")
    args = parser.parse_args()
    languages = [item.strip() for item in args.languages.split(",") if item.strip()]
    print(json.dumps(audit_curriculum(languages or None), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
