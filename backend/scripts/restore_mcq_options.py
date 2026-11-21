"""Build the small verified-MCQ option overlay without rewriting questions_bank.json."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "app" / "data"
BANK = DATA / "questions_bank.json"
SOURCE = DATA / "verified_placement_questions.json"
OUTPUT = DATA / "verified_mcq_option_overrides.json"
PLACEHOLDER = re.compile(r"Option [A-D0-9]+", re.IGNORECASE)
MCQ_TYPES = {"aptitude", "logical", "verbal"}

def _rows(data):
    if isinstance(data, dict):
        for key in ("questions", "items"):
            if key in data:
                return data[key]
    return data

def _placeholder(options):
    values = list(options.values()) if isinstance(options, dict) else list(options or [])
    return bool(values) and any(PLACEHOLDER.fullmatch(str(v).strip()) for v in values)

def _resolve_index(source):
    options = [str(value).strip() for value in (source.get("options") or [])]
    if len(options) < 4 or len(set(options)) != len(options):
        return None
    answer = str(source.get("correct_answer") or "").strip()
    exact = [i for i, option in enumerate(options) if option == answer]
    if len(exact) == 1:
        return exact[0]
    index = source.get("correct_index")
    if isinstance(index, int) and 0 <= index < len(options) and answer:
        if answer.startswith(options[index]) or options[index].startswith(answer):
            return index
    return None

def build_overlay():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    source = _rows(json.loads(SOURCE.read_text(encoding="utf-8")))
    source_by_id = {str(item["id"]): item for item in source if isinstance(item, dict) and item.get("id")}
    items, demote_ids = [], []
    for question in bank:
        if question.get("type") not in MCQ_TYPES or not _placeholder(question.get("options")):
            continue
        original_id = str(question.get("id"))
        reference = source_by_id.get(original_id)
        if not reference:
            if question.get("trust_status") in ("verified", "reviewed"):
                demote_ids.append(original_id)
            continue
        index = _resolve_index(reference)
        if index is None:
            if question.get("trust_status") in ("verified", "reviewed"):
                demote_ids.append(original_id)
            continue
        options = [str(value).strip() for value in reference["options"]]
        item = {"id": original_id, "type": question["type"], "options": options,
                "correct_index": index, "correct_answer": options[index]}
        for field in ("explanation", "reasoning_steps", "shortcut", "common_trap", "hints"):
            if reference.get(field):
                item[field] = reference[field]
        items.append(item)
    return {"version": 1, "source_bank": SOURCE.name,
            "note": "Source-backed verified MCQ repairs; no trust status is promoted.",
            "items": items, "demote_ids": sorted(set(demote_ids))}

if __name__ == "__main__":
    result = build_overlay()
    print(f"overrides={len(result['items'])} demote_ids={len(result['demote_ids'])}")
    if "--dry-run" not in __import__("sys").argv:
        OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
