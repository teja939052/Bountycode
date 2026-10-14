"""Mission grammar gate.

One standard, enforced. Run before any mission content is published:

    python validate.py            # all mission content
    python validate.py --strict   # fail (exit 1) on any non-conforming mission

THE STANDARD (ADR: BOUNTYCODE_CURRICULUM_STRUCTURE)

A mission teaches through ONE grammar. Not a card, not a quiz, not an article.

  Canonical teaching stages — backend STEP_TYPES, every one is required:
      intro (chrome) then
      discover | manipulate | predict | build | break | debug
      | retrieve | transfer | mastery

  Composition chrome (framing, not teaching):  intro | practice | recognize
  prove == mastery,  recognize == predict — aliases, not new stages.

  Interaction subtypes (stage.interaction.kind, never a top-level stage)
  required evidence for this gate:
      change_one_thing   student must reuse the idea with one value changed
      timed_prove        assessment under placement conditions

  Captain Byte: every mission carries authored mentor moments. Generic
  motivational copy is a bug, never a fallback.

Formats in the tree today:

  patterns.ts          CANONICAL   `kind: "<stage>"` markers, machine-checkable
  *.tsx (21 files)     JSX components exported as FlagshipMissionProps
  world1.ts            legacy MissionStep `type:` engine grammar

Mass production must target the canonical form only; the other two are
reported so drift is visible instead of silent.
"""
from __future__ import annotations

import os
import re
import sys
from typing import Dict, List, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))

CANONICAL: List[str] = [
    "discover", "manipulate", "predict", "build",
    "break", "debug", "retrieve", "transfer", "mastery",
]

# Chrome frames a mission but does not teach by itself.
CHROME: List[str] = ["intro", "practice", "recognize"]

# Evidence the lesson loop actually ran, not just named.
REQUIRED_INTERACTIONS: List[str] = ["change_one_thing", "timed_prove"]

#: Legacy engine grammar (engine/missionTypes.ts) — drifted from ADR.
LEGACY_TYPES: List[str] = [
    "story", "discover", "predict", "build",
    "break", "debug", "prove", "reward",
]

#: Converged engine vocabulary. missionTypes.ts mirrors backend STEP_TYPES;
#: chrome frames but does not teach. Anything outside this set is a violation.
CONVERGED_VOCAB: List[str] = CANONICAL + ["intro", "practice", "recognize", "reward"]

KIND_RE = re.compile(r'kind:\s*"([a-z_]+)"')
LEGACY_RE = re.compile(r'type:\s*"(story|discover|predict|build|break|debug|prove|reward)"')
STEP_TYPE_RE = re.compile(r'type:\s*"([a-z_]+)"')
BLOCK_RE = re.compile(r"\b([A-Z][A-Za-z]+Block)\b\s*\(")
PHASE_RE = re.compile(
    r"(Visual|Manipulate|Predict|Build|Break|Fix|Recall|Transfer|Prove|Reward|Brief|Intro)[A-Za-z]*Block"
)


def _read(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def classify(text: str) -> str:
    if KIND_RE.search(text):
        return "canonical"
    if BLOCK_RE.search(text):
        return "jsx"
    if LEGACY_RE.search(text):
        return "legacy"
    return "unknown"


def canonical_report(name: str, text: str) -> Tuple[bool, str, Dict]:
    kinds = KIND_RE.findall(text)
    found = set(kinds)
    missing_stage = [s for s in CANONICAL if s not in found]
    missing_chrome = [s for s in CHROME if s not in found]
    missing_ix = [s for s in REQUIRED_INTERACTIONS if s not in found]
    ok = not missing_stage and not missing_ix and not missing_chrome
    detail = (
        "stages %d/%d  chrome %d/%d  evidence %s"
        % (
            len(CANONICAL) - len(missing_stage), len(CANONICAL),
            len(CHROME) - len(missing_chrome), len(CHROME),
            "ok" if not missing_ix else "missing " + ",".join(missing_ix),
        )
    )
    if missing_stage:
        detail += "  missing " + ",".join(missing_stage)
    return ok, detail, {"stages": missing_stage, "chrome": missing_chrome, "ix": missing_ix}


def jsx_report(name: str, text: str) -> Tuple[bool, str, Dict]:
    """JSX missions: detect the teaching blocks actually rendered."""
    blocks = set(PHASE_RE.findall(text))
    mapped = {
        "Visual": "discover", "Manipulate": "manipulate", "Predict": "predict",
        "Build": "build", "Break": "break", "Fix": "debug", "Recall": "retrieve",
        "Transfer": "transfer", "Prove": "mastery", "Reward": "mastery",
        "Brief": "intro", "Intro": "intro",
    }
    present = {mapped[b] for b in blocks if b in mapped}
    missing = [s for s in CANONICAL if s not in present]

    # Evidence, by structure not by keyword: these missions name their blocks.
    has_ix = (
        "change_one_thing" in text
        or "ChangeOneThing" in text
        or re.search(r"\bfunction\s+Change[A-Za-z]*Block\b", text) is not None
    )
    # A placement block only counts as timed proof if it actually constrains time.
    placement = re.search(r"\bfunction\s+Placement[A-Za-z]*Block\b", text) is not None
    has_timed = (
        placement
        and re.search(r"\b(timed|timeLimit|countdown|secondsRemaining|PlacementTimer)\b", text) is not None
    )

    # THE LAW (strict): retrieve must exist as a Recall stage, and the timed
    # proof must be real — a shared PlacementTimer wired to lock the answer.
    law_missing = []
    if "retrieve" in missing:
        law_missing.append("retrieve/RecallBlock")
    if not has_ix:
        law_missing.append("change_one_thing")
    if not has_timed:
        law_missing.append("timed_prove(PlacementTimer)")
    if not re.search(r"PlacementTimer\s+seconds=\{\d+\}", text):
        law_missing.append("PlacementTimer")
    if "disabled={locked}" not in text:
        law_missing.append("expiry lock (disabled={locked})")
    if not re.search(r'id:\s*"recall"', text):
        law_missing.append('recall step entry (id: "recall")')

    ok = not missing and not law_missing
    detail = "jsx stages %d/%d  change_one_thing=%s timed_prove=%s" % (
        len(CANONICAL) - len(missing), len(CANONICAL), has_ix, has_timed,
    )
    if missing:
        detail += "  missing " + ",".join(missing)
    if law_missing:
        detail += "  LAW " + ",".join(law_missing)
    return ok, detail, {"stages": missing, "law": law_missing}


def legacy_report(name: str, text: str) -> Tuple[bool, str, Dict]:
    """engine/missionTypes content: every step type must be converged
    vocabulary, and all nine canonical stages must be present. The legacy
    names (story/prove-as-stage) are violations, not aliases."""
    types = set(STEP_TYPE_RE.findall(text))
    noncanonical = sorted(t for t in types if t not in CONVERGED_VOCAB)
    missing = [s for s in CANONICAL if s not in types]
    legacy = sorted(t for t in types if t in ("story", "prove"))
    ok = not noncanonical and not missing and not legacy
    detail = "engine types %d  canonical %d/9" % (
        len(types), len(CANONICAL) - len(missing),
    )
    if legacy:
        detail += "  LEGACY " + ",".join(legacy)
    if noncanonical:
        detail += "  NON-CANONICAL " + ",".join(noncanonical)
    if missing:
        detail += "  missing " + ",".join(missing)
    return ok, detail, {"types": sorted(types), "missing": missing, "legacy": legacy}


def main(argv: List[str]) -> int:
    strict = "--strict" in argv
    files = sorted(
        f for f in os.listdir(HERE)
        if f.endswith((".ts", ".tsx")) and f not in ("__all.ts",)
    )

    counts = {"canonical": 0, "jsx": 0, "legacy": 0, "unknown": 0}
    failures: List[str] = []

    print("Mission grammar gate — ADR: BOUNTYCODE_CURRICULUM_STRUCTURE")
    print("canonical: " + " | ".join(CANONICAL))
    print("evidence : " + " | ".join(REQUIRED_INTERACTIONS))
    print("-" * 78)

    for name in files:
        if name in ("validate.py",):
            continue
        text = _read(os.path.join(HERE, name))
        fmt = classify(text)
        counts[fmt] += 1
        if fmt == "canonical":
            ok, detail, _ = canonical_report(name, text)
        elif fmt == "jsx":
            ok, detail, _ = jsx_report(name, text)
        elif fmt == "legacy":
            ok, detail, _ = legacy_report(name, text)
        else:
            ok, detail = False, "no recognizable mission structure"
        status = "PASS" if ok else "FAIL"
        if not ok:
            failures.append(name)
        print("  %-4s %-26s %-9s %s" % (status, name, fmt, detail))

    print("-" * 78)
    print(
        "format spread: canonical=%d jsx=%d legacy=%d unknown=%d   "
        "conforming=%d  failing=%d"
        % (
            counts["canonical"], counts["jsx"], counts["legacy"],
            counts["unknown"], len(files) - len(failures), len(failures),
        )
    )

    if counts["unknown"]:
        print(
            "UNKNOWN FORMAT: %d file(s) carry no recognizable mission structure. "
            "Author in canonical `patterns.ts` form or the JSX FlagshipMission form."
            % counts["unknown"]
        )

    print(
        "MISSION CONTRACT: canonical stages + change_one_thing + timed_prove. "
        "A simpler format is not faster — the validator says no."
    )

    if strict and failures:
        print("STRICT: failing missions -> " + ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
