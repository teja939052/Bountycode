"""Read-only structural validation for the v2 placement-prep intake candidates."""
import json
from collections import Counter
from pathlib import Path
BACKEND_ROOT = Path(__file__).resolve().parents[1]
INTAKE = BACKEND_ROOT / "app" / "data" / "intake"

def load(name):
    return json.loads((INTAKE / name).read_text(encoding="utf-8"))

def validate_mcqs(name, count, types, topics):
    items = load(name)
    if not isinstance(items, list) or len(items) != count:
        raise ValueError(f"{name}: expected {count} records")
    ids, questions = set(), set()
    for i, item in enumerate(items):
        label = f"{name}[{i}]"
        qid = str(item.get("id") or "").strip()
        question = str(item.get("question") or "").strip()
        if not qid or qid in ids or not question or question in questions:
            raise ValueError(f"{label}: missing or duplicate id/question")
        ids.add(qid); questions.add(question)
        if item.get("type") not in types or item.get("trust_status") != "unverified":
            raise ValueError(f"{label}: wrong type or trust state")
        options = item.get("options")
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(f"{label}: exactly four options required")
        opts = [str(v).strip() for v in options]
        if any(not v for v in opts) or len(set(opts)) != 4:
            raise ValueError(f"{label}: options must be unique and non-empty")
        idx = item.get("correct_index")
        if type(idx) is not int or not 0 <= idx < 4 or opts[idx] != str(item.get("correct_answer") or "").strip():
            raise ValueError(f"{label}: answer index/text mismatch")
        if not str(item.get("explanation") or "").strip() or item.get("topic") not in topics:
            raise ValueError(f"{label}: explanation or topic missing/invalid")
    if Counter(x.get("topic") for x in items) != Counter(topics):
        raise ValueError(f"{name}: topic distribution mismatch")
    return items

def validate_all():
    aptitude_topics = {"percentages":25,"profit_loss":25,"discount":25,"ratio":25,"time_work":25,"average_speed":25,"trains":25,"averages":25,"interest":25,"series":25}
    aptitude = validate_mcqs("aptitude_generated_v2.json",250,{"aptitude","logical"},aptitude_topics)
    if Counter(x["type"] for x in aptitude) != Counter({"aptitude":225,"logical":25}):
        raise ValueError("Unexpected aptitude/logical candidate split")
    pseudo = validate_mcqs("pseudocode_generated_v2.json",60,{"cs_fundamentals"},{"pseudocode":60})
    if any("what is the output" not in x["question"].lower() for x in pseudo):
        raise ValueError("Pseudocode prompts must ask for the displayed code output")
    verbal_topics = {"synonyms":20,"antonyms":20,"sentence_correction":20,"fill_in_the_blank":20,"one_word_substitution":20,"idioms":20}
    verbal = validate_mcqs("verbal_generated_v2.json",120,{"verbal"},verbal_topics)
    essay_data = load("essay_prompts_v2.json")
    essays = essay_data.get("prompts",[])
    if len(essays)!=28 or len(essay_data.get("rubric",{}).get("criteria",[]))!=4:
        raise ValueError("Expected 28 essays and a four-criterion rubric")
    if any(x.get("trust_status")!="unverified" for x in essays):
        raise ValueError("Essay prompts must remain unverified")
    spoken = load("spoken_english_tasks_v2.json")
    if len(spoken)!=30 or any(x.get("trust_status")!="unverified" for x in spoken):
        raise ValueError("Expected 30 unverified spoken-English tasks")
    blueprints = load("company_blueprints_additions.json")
    drafts = blueprints.get("company_blueprints_additions",{})
    if len(drafts)!=4 or "DRAFT" not in str(blueprints.get("_readme","")).upper():
        raise ValueError("Expected four draft company blueprints")
    if any(not v.get("conflict") or not v.get("source",{}).get("url") for v in drafts.values()):
        raise ValueError("Every company blueprint draft must preserve a source and conflict note")
    return {"mcq_candidates":len(aptitude)+len(pseudo)+len(verbal),"essay_prompts":len(essays),"spoken_tasks":len(spoken),"company_blueprint_drafts":len(drafts)}

if __name__ == "__main__":
    print(json.dumps(validate_all(),indent=2))
