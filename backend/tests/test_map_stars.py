"""Adventure-map star + layout invariants.

Pure-function tests (no DB): they pin the 1-3 star thresholds, the
serpentine bounds, and the anti hint-laundering property so the next
refactor cannot silently change what students see on the map.

Evidence model (see routes/worlds.py attempt/hint/complete + services/lesson.py):
hints_used and attempts accumulate on ONE entry per node. Retries append;
nothing resets them. Stars therefore cannot be laundered by retrying.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.data.worlds_data import WORLD_REGISTRY
from app.routes.map import (
    HORIZON_VISIBLE_AHEAD,
    WORLD_ADVENTURE_NAMES,
    _campfire_node,
    _inject_campfire,
    _repair_node,
    _serpentine_xy,
    _should_offer_repair,
    _stars_for_entry,
    _world_summary,
)
from app.routes.worlds import is_world_unlocked, world_progress


def _entry(best=0, hints=0, completed=True, attempts=1, failed=0):
    return {
        "completed": completed,
        "best_score": best,
        "score": best,
        "hints_used": [f"h{i}" for i in range(hints)],
        "attempts": attempts,
        "failed_attempts": failed,
    }


# ─── Star thresholds ───

def test_three_stars_needs_high_best_and_minimal_hints():
    assert _stars_for_entry(_entry(best=100, hints=0)) == 3
    assert _stars_for_entry(_entry(best=85, hints=1)) == 3


def test_hint_spam_caps_at_two_stars():
    # best is perfect but 2+ hints were used -> independence not shown
    assert _stars_for_entry(_entry(best=100, hints=2)) == 2
    assert _stars_for_entry(_entry(best=95, hints=5)) == 2


def test_mid_best_is_two_stars():
    assert _stars_for_entry(_entry(best=84, hints=0)) == 2
    assert _stars_for_entry(_entry(best=60, hints=0)) == 2


def test_low_best_is_one_star():
    assert _stars_for_entry(_entry(best=59, hints=0)) == 1
    assert _stars_for_entry(_entry(best=0, hints=0)) == 1


def test_incomplete_is_zero_stars():
    assert _stars_for_entry(_entry(best=0, completed=False)) == 0
    assert _stars_for_entry(_entry(best=100, completed=False)) == 0


def test_recovery_can_reach_three_stars_on_a_clean_pass():
    # Struggled (failed attempts) then passed clean: same bar as first-try.
    assert _stars_for_entry(_entry(best=95, hints=1, attempts=4, failed=3)) == 3


def test_recovery_with_hint_spam_stays_at_two():
    # The anti-laundering pin: failed attempts + hint spam cannot reach 3.
    assert _stars_for_entry(_entry(best=100, hints=3, attempts=6, failed=5)) == 2


# ─── Layout bounds (ship + badges stay inside the stage) ───

def test_serpentine_stays_inside_stage():
    for total in (1, 2, 6, 8, 25, 80):
        for i in range(total):
            p = _serpentine_xy(i, total)
            assert 48.0 <= p["x"] <= 292.0, (total, i, p)
            assert 60.0 <= p["y"] <= 560.0, (total, i, p)


def test_serpentine_walks_bottom_to_top():
    first = _serpentine_xy(0, 6)
    last = _serpentine_xy(5, 6)
    assert first["y"] > last["y"]


def test_horizon_is_eight():
    assert HORIZON_VISIBLE_AHEAD == 8


# ─── Campfire injection (transient, pre-boss, never a gate) ───

def _level_nodes(n_levels=5, with_boss=True):
    nodes = []
    for i in range(n_levels):
        is_boss = with_boss and i == n_levels - 1
        nodes.append({
            "node_id": f"foundations:level-{i}",
            "is_boss": is_boss,
            "kind": "world_boss" if is_boss else "battle",
            "status": "completed" if i < 2 else "unlocked",
        })
    return nodes


def test_no_campfire_when_nothing_due():
    nodes = _level_nodes()
    assert _inject_campfire(nodes, 0) == -1
    assert len(nodes) == 5


def test_no_campfire_when_no_boss_to_protect():
    nodes = _level_nodes(with_boss=False)
    assert _inject_campfire(nodes, 3) == -1
    assert len(nodes) == 5


def test_campfire_lands_immediately_before_boss():
    nodes = _level_nodes()
    at = _inject_campfire(nodes, 3)
    assert at == 4
    assert len(nodes) == 6
    camp = nodes[4]
    assert camp["kind"] == "srs_campfire"
    assert camp["node_id"] == "foundations:campfire_rest"
    assert camp["due_count"] == 3
    assert camp["status"] == "unlocked"
    assert nodes[5]["is_boss"] is True
    # Path chain passes through the campfire, unlock order untouched.
    assert nodes[3]["node_id"] != camp["node_id"]


def test_campfire_node_is_transient_shape():
    camp = _campfire_node("foundations", 2)
    assert camp["stars"] == 0
    assert camp["is_boss"] is False
    assert camp["diamonds"] == 0


# ─── Repair trigger + branch shape ───

def test_repair_trigger_needs_real_struggle():
    assert _should_offer_repair({"completed": False, "failed_attempts": 1, "hints_used": []}) is True
    assert _should_offer_repair({"completed": False, "failed_attempts": 0, "hints_used": ["h0", "h1"]}) is True
    assert _should_offer_repair({"completed": False, "failed_attempts": 0, "hints_used": ["h0"]}) is False
    assert _should_offer_repair({"completed": False, "failed_attempts": 0, "hints_used": []}) is False
    # A cleared node never sprouts a branch, however bloody its history.
    assert _should_offer_repair({"completed": True, "failed_attempts": 5, "hints_used": ["h0", "h1", "h2"]}) is False


def test_repair_node_merges_back_and_stays_on_stage():
    node = _repair_node("foundations", "level-2", "things", "Level 2", "loops", {"x": 280.0, "y": 400.0})
    assert node["kind"] == "repair"
    assert node["node_id"] == "foundations:level-2_repair"
    assert node["is_branch"] is True
    assert node["branch_from"] == "foundations:level-2"
    assert node["path_next"] == ["foundations:level-2"]
    assert node["title"] == "Repair: loops"
    assert node["status"] == "unlocked"
    assert 48.0 <= node["position"]["x"] <= 292.0
    assert node["position"]["y"] >= 60.0


def test_repair_node_generic_label_without_weak_skill():
    node = _repair_node("foundations", "level-2", "things", "Level 2", None, {"x": 100.0, "y": 300.0})
    assert node["title"] == "Repair: steady the basics"
    assert node["position"]["x"] == 172.0


# ─── All-worlds identity + gating ───

def test_every_world_has_an_adventure_name():
    missing = [wid for wid in WORLD_REGISTRY if wid not in WORLD_ADVENTURE_NAMES]
    assert missing == [], f"worlds without adventure identity: {missing}"


def _complete_all(world_id):
    w = WORLD_REGISTRY[world_id]
    return {f"{world_id}:{l.id}": {"completed": True} for t in w.towns for l in t.levels}


def test_every_prereq_id_resolves():
    """A mistyped prereq must fail here, not in front of a student."""
    for wid, w in WORLD_REGISTRY.items():
        for pid in list(getattr(w, "prerequisites", []) or []):
            assert pid in WORLD_REGISTRY, f"{wid} prereq {pid!r} does not exist"


def test_full_chain_unlocks_link_by_link():
    """Walk the entire 11-edge chain: each cleared world opens the next."""
    ordered = sorted(WORLD_REGISTRY.values(), key=lambda w: w.order)
    assert len(ordered) == 12
    completed: dict = {}
    for i, world in enumerate(ordered):
        by_id = {w.id: _world_summary(w, completed) for w in ordered}
        # Worlds behind us are completed; the frontier is open; everything
        # ahead is locked. Each cleared world opens exactly the next link.
        for j, w in enumerate(ordered):
            if j < i:
                assert by_id[w.id]["status"] == "completed", w.id
            elif j == i:
                assert by_id[w.id]["status"] in ("unlocked", "active"), w.id
                assert is_world_unlocked(w.id, completed) is True
            else:
                assert by_id[w.id]["status"] == "locked", f"{w.id} open too early"
                assert is_world_unlocked(w.id, completed) is False
        # Earned progress is never locked out, even mid-chain.
        assert world_progress(world.id, completed)["total"] > 0
        completed.update(_complete_all(world.id))
        assert _world_summary(world, completed)["status"] == "completed"
    # After the summit: everything completed.
    by_id = {w.id: _world_summary(w, completed) for w in ordered}
    assert all(s["status"] == "completed" for s in by_id.values())


def test_fresh_student_sees_foundations_open_rest_locked():
    by_id = {w.id: _world_summary(w, {}) for w in WORLD_REGISTRY.values()}
    assert by_id["foundations"]["status"] == "unlocked"
    assert by_id["searchlands"]["status"] == "locked"
    assert by_id["alpine"]["status"] == "locked"
    assert by_id["foundations"]["done"] == 0
    assert by_id["foundations"]["total"] == 6


def test_clearing_foundations_unlocks_searchlands():
    completed = _complete_all("foundations")
    by_id = {w.id: _world_summary(w, completed) for w in WORLD_REGISTRY.values()}
    assert by_id["foundations"]["status"] == "completed"
    assert by_id["searchlands"]["status"] == "unlocked"
    assert by_id["sorting"]["status"] == "locked"


def test_progress_marks_world_active_and_keeps_it_open():
    completed = {"foundations:level-1": {"completed": True}}
    assert _world_summary(WORLD_REGISTRY["foundations"], completed)["status"] == "active"
    assert is_world_unlocked("searchlands", completed) is False
    # Partial progress inside a later world never gets locked out.
    first_search = WORLD_REGISTRY["searchlands"].towns[0].levels[0].id
    partial = {f"searchlands:{first_search}": {"completed": True}}
    assert is_world_unlocked("searchlands", partial) is True
