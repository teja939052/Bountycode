"""Gamification Law enforcement tests.

Law (AGENTS.md): the only writer of diamonds/streak/level/badges (and the
league counters) is record_practice() plus spend_xp() for debits, and every
mutation appends one immutable gamification_events row.
"""
import ast
import re
from pathlib import Path

import pytest

APP_ROOT = Path(__file__).resolve().parents[1] / "app"

# Functions inside services/gamification.py that are allowed to mutate
# economy fields. Everything else in the codebase must not.
ALLOWED_WRITERS = {
    "record_practice",
    "spend_xp",
    "claim_daily_login",
    "award_bonus_xp",
    "initialize_gamification",
    "_append_ledger_event",
}

ECONOMY_FIELD = re.compile(r"""["'](diamonds|streak|longest_streak|level|badges|coins|combo|league)["']""")
UPDATE_OP = re.compile(r'"\$(inc|set|addToSet|push|unset)"')


def _iter_economy_writes():
    """Yield (file, func, lineno, line) for every $inc/$set touching economy fields."""
    for path in list((APP_ROOT / "services").glob("*.py")) + list((APP_ROOT / "routes").glob("*.py")):
        src = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            seg = ast.get_source_segment(src, node) or ""
            for i, line in enumerate(seg.splitlines(), start=node.lineno):
                if UPDATE_OP.search(line) and ECONOMY_FIELD.search(line):
                    yield path.name, node.name, i, line.strip()


class TestGamificationLawStatic:
    def test_no_rogue_economy_writers(self):
        violations = [
            f"{f}:{func}:{ln}: {line}"
            for f, func, ln, line in _iter_economy_writes()
            if not (f == "gamification.py" and func in ALLOWED_WRITERS)
        ]
        assert not violations, "Rogue economy writers found:\n" + "\n".join(violations)

    def test_spend_xp_exists_as_debit_path(self):
        src = (APP_ROOT / "services" / "gamification.py").read_text(encoding="utf-8-sig")
        assert "async def spend_xp(" in src
        assert '"$gte"' in src  # atomic balance guard


class _FakeResult:
    def __init__(self, modified_count):
        self.modified_count = modified_count


class TestSpendXp:
    @pytest.mark.asyncio
    async def test_spend_success_decrements_and_ledgers(self, mocker):
        from app.services import gamification as g

        mock_coll = mocker.AsyncMock()
        mock_coll.update_one.return_value = _FakeResult(1)
        mock_coll.find_one.return_value = {"user_id": "u1", "diamonds": 70}
        mocker.patch.object(g, "gamification_collection", mock_coll)

        events = []
        mocker.patch.object(
            g, "_append_ledger_event",
            mocker.AsyncMock(side_effect=lambda *a, **k: events.append((a, k))),
        )

        result = await g.spend_xp("u1", 30, "streak_repair")
        assert result["success"] is True
        assert result["balance"] == 70

        # atomic guard: only decrements when balance covers it
        args, _ = mock_coll.update_one.call_args
        assert args[0] == {"user_id": "u1", "diamonds": {"$gte": 30}}
        assert args[1]["$inc"] == {"diamonds": -30}

        # immutable ledger row with negative award
        assert len(events) == 1
        (uid, activity, awarded), _ = events[0][0][:3], events[0]
        assert uid == "u1" and activity == "spend" and awarded == -30

    @pytest.mark.asyncio
    async def test_spend_insufficient_balance_declines(self, mocker):
        from app.services import gamification as g

        mock_coll = mocker.AsyncMock()
        mock_coll.update_one.return_value = _FakeResult(0)
        mock_coll.find_one.return_value = {"user_id": "u1", "diamonds": 5}
        mocker.patch.object(g, "gamification_collection", mock_coll)
        ledger = mocker.AsyncMock()
        mocker.patch.object(g, "_append_ledger_event", ledger)

        result = await g.spend_xp("u1", 30, "streak_repair")
        assert result["success"] is False
        assert result["balance"] == 5
        ledger.assert_not_called()

    @pytest.mark.asyncio
    async def test_spend_rejects_non_positive(self, mocker):
        from app.services import gamification as g

        with pytest.raises(ValueError):
            await g.spend_xp("u1", 0, "x")
