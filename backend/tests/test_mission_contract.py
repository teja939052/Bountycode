"""Mission contract tests — structure, refs, tracks, and trust.

Proves: templates emit the canonical nine; exemplar missions validate
against the LIVE serving gate; service tracks resolve; generated
candidates are UNVERIFIED and never served; missions cannot reference
unservable content.
"""
import json
import os

from app.content import service_tracks
from app.content.curriculum.mission_templates import (
    aptitude, coding, company_quest, cs_core, reasoning, verbal,
)
from app.content.curriculum.missions import MISSIONS
from app.content.lesson_definitions import STEP_TYPES
from app.content.mission_definitions import (
    MissionDefinition, mission_index, validate_mission,
)
from app.services import question_store as qs


def test_templates_emit_canonical_nine():
    makers = [aptitude, reasoning, verbal, coding, cs_core, company_quest]
    for mod in makers:
        m = mod.template("x", "y")
        assert [s.stage for s in m.stages] == list(STEP_TYPES), mod.__name__
        assert any(s.stage == "mastery" and s.time_limit_seconds > 0
                   for s in m.stages), mod.__name__
        ix = {s.interaction for s in m.stages}
        ix |= {mm for s in m.stages for mm in s.moments}
        assert "change_one_thing" in ix, mod.__name__


def test_exemplar_missions_validate_live():
    assert len(MISSIONS) == 16, set(MISSIONS)
    for mid, m in MISSIONS.items():
        errors = validate_mission(m)
        assert errors == [], f"{mid}: {errors}"
        assert m.status == "unverified"  # structure is new: honest label
        assert m.provenance == "pattern-relevant"


def test_service_tracks_resolve():
    assert len(service_tracks.list_tracks()) == 6
    ids = service_tracks.track_mission_ids("tcs_nqt")
    assert "tcs_nqt.percentages_change" in ids
    assert "tcs_nqt.arrays_basics" in ids
    for mid in ids:
        assert mid in MISSIONS, f"track references unauthored mission {mid}"
    idx = mission_index(list(MISSIONS.values()))
    assert idx["tcs_nqt.percentages_change"]["frontend_slug"] == "percentages"
    assert idx["tcs_nqt.percentages_change"]["mentor_skill"] == "quant.percentages"


def test_mentor_skills_resolve_to_authored_speech():
    from app.services.mentor_service import resolve_captain_byte

    for skill in ("quant.percentages", "code.arrays"):
        out = resolve_captain_byte(canonical_skill=skill, moment="intro")
        assert out["block"], skill


def test_generated_candidates_unverified_and_unserved():
    path = os.path.join(os.path.dirname(__file__), "..", "app", "data",
                        "mission_candidates_percentages.json")
    with open(path, encoding="utf-8") as fh:
        items = json.load(fh)
    assert len(items) >= 10
    for it in items:
        assert it["trust_status"] == "unverified"
        assert it["companies"] == []
        assert "deterministic_generator" in it["provenance"]
        # Never served behind the gate:
        assert qs.find_one({"id": it["id"]}) is None


def test_mission_attaches_to_journey_action():
    from app.services.journey_engine import _mission_for_action

    a = _mission_for_action({"kind": "lesson", "skill_id": "quant.percentages"}, "tcs")
    assert a["mission_id"] == "tcs_nqt.percentages_change"
    assert a["track_id"] == "tcs_nqt"
    assert a["frontend_slug"] == "percentages"

    b = _mission_for_action({"kind": "lesson", "level": "arrays"}, "TCS")
    assert b["mission_id"] == "tcs_nqt.arrays_basics"

    # SRS reviews never carry missions; unknown companies match nothing.
    assert "mission_id" not in _mission_for_action({"kind": "srs"}, "tcs")
    assert "mission_id" not in _mission_for_action(
        {"kind": "lesson", "skill_id": "quant.percentages"}, "unknownco")


def test_mission_cannot_reference_unservable_content():
    m = MissionDefinition.model_validate({
        **MISSIONS["tcs_nqt.percentages_change"].model_dump(),
        "id": "test.bad_ref",
    })
    m.stages[2].bank_refs = ["gen_pct_0000"]  # unverified candidate
    errors = validate_mission(m)
    assert any("gen_pct_0000" in e and "not servable" in e for e in errors), errors
