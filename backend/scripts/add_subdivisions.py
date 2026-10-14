"""Add subdivision field to company question banks.

Maps existing questions to company subdivisions (hiring tracks) so students
can practice by specific company band (e.g. TCS Ninja vs Digital vs Prime).
"""
from __future__ import annotations

import json
import os
import random

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DATA_DIR = os.path.join(_BACKEND_ROOT, "app", "data")

_SUBDIVISIONS = {
    "tcs_nqt": ["ninja", "digital", "prime"],
    "accenture": ["analyst", "senior_analyst"],
    "infosys": ["infytq", "specialist_program"],
    "wipro_nlth": ["wilp", "turbo"],
    "capgemini": ["engineer_trainee", "analyst"],
    "tcs_codevita": ["codevita", "digital"],
    "tech_mahindra": ["associate", "software_engineer"],
    "ltimindtree": ["associate", "system_engineer"],
    "hcl": ["associate", "software_engineer"],
    "cognizant_genc": ["genc", "genc_next"],
}

_FILES = {
    "tcs_nqt": "tcs_nqt_coding_verified.json",
    "accenture": "capgemini_accenture_verified.json",
    "infosys": "infosys_infytq_verified.json",
    "wipro_nlth": "wipro_nlth_verified.json",
    "capgemini": "capgemini_accenture_verified.json",
    "tcs_codevita": "tcs_codevita_verified.json",
    "tech_mahindra": "tech_mahindra_verified.json",
    "ltimindtree": "ltimindtree_verified.json",
    "hcl": "hcl_verified.json",
    "cognizant_genc": "cognizant_genc_verified.json",
}


def _assign_subdivision(company_key: str, q: dict) -> str:
    existing = q.get("subdivision") or q.get("hiring_track") or q.get("band")
    if existing:
        return existing
    subs = _SUBDIVISIONS.get(company_key, [])
    if subs:
        return random.choice(subs)
    return "general"


def main() -> None:
    for company_key, filename in _FILES.items():
        path = os.path.join(_DATA_DIR, filename)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated = False
        for q in data:
            if "subdivision" not in q:
                q["subdivision"] = _assign_subdivision(company_key, q)
                updated = True

        if updated:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[{company_key}] updated {filename}")
        else:
            print(f"[{company_key}] no changes in {filename}")


if __name__ == "__main__":
    main()
