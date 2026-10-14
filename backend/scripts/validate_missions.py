#!/usr/bin/env python3
"""CI gate: validate all backend MissionDefinition objects.

Exits 0 if every mission passes validate_mission().
Exits 1 and prints errors if any mission fails.
"""
from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.content.curriculum.missions import MISSIONS
from app.content.mission_definitions import validate_mission


def main() -> int:
    failed = []
    for mission_id, mission in MISSIONS.items():
        errors = validate_mission(mission)
        if errors:
            failed.append((mission_id, errors))

    if failed:
        print("FAIL: backend mission validation failed")
        for mission_id, errors in failed:
            print(f"  {mission_id}:")
            for error in errors:
                print(f"    - {error}")
        return 1

    print(f"OK: {len(MISSIONS)} backend missions validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
