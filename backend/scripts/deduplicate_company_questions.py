"""Deduplicate company question files by normalized question text.

Removes duplicate questions across all sections and companies, keeping the first occurrence.
"""
from __future__ import annotations

import json
import os
import re
from collections import Counter

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BACKEND_ROOT, "app", "data")

_FILES = {
    "cognizant": "cognizant_genc_verified.json",
    "wipro": "wipro_nlth_verified.json",
    "capgemini": "capgemini_accenture_verified.json",
    "infosys": "infosys_infytq_verified.json",
    "tcs": "tcs_nqt_coding_verified.json",
}


def _normalize(q: dict) -> str:
    title = str(q.get("question") or q.get("question_title") or q.get("title") or "")
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()[:80]


def main() -> None:
    total_removed = 0
    for company, filename in _FILES.items():
        path = os.path.join(_DATA_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        seen = set()
        deduped = []
        removed = 0
        for q in data:
            key = _normalize(q)
            if key in seen:
                removed += 1
                continue
            seen.add(key)
            deduped.append(q)

        if removed:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(deduped, f, indent=2, ensure_ascii=False)
            print(f"[{company}] removed {removed} duplicates from {filename} ({len(deduped)} remaining)")
        else:
            print(f"[{company}] no duplicates in {filename} ({len(data)} remaining)")

        total_removed += removed

    print(f"\nTotal duplicates removed: {total_removed}")


if __name__ == "__main__":
    main()
