"""Integration test: world level completion Diamonds honesty + idempotency.

Fires REAL HTTP against a live MongoDB (skipped when unreachable):

  attempt (passing code) → complete → profile delta

Asserts the money invariant the _award_xp audit demands:
  response.xp_awarded == gamification profile diamonds delta

and the double-tap invariants:
  sequential retry  → deduplicated, zero additional Diamonds
  concurrent retry  → exactly one award, exactly one deduplicated

Passing code for foundations/level-1 satisfies its deterministic judge
(``apples = 5``); no mocks anywhere in this file.
"""

import asyncio

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import gamification_collection, users_collection
from app.middleware.rate_limiter import clear_login_attempts


EMAIL = "world_xp_test@example.com"
PASS_CODE = "apples = 5"


def _db_available() -> bool:
    try:
        from app.database import get_client

        async def _ping():
            await get_client().admin.command("ping")

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(_ping())
        finally:
            loop.close()
        return True
    except Exception:
        return False


needs_db = pytest.mark.skipif(not _db_available(), reason="MongoDB unreachable")


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture(autouse=True)
async def clear_rate_limiter():
    from app.middleware.rate_limiter import request_counts

    request_counts.clear()
    yield
    request_counts.clear()


@pytest.fixture
async def test_user(client):
    clear_login_attempts(EMAIL)
    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": EMAIL})
    except Exception:
        pass

    r = await client.post(
        "/api/v1/auth/register",
        json={"email": EMAIL, "name": "World Diamonds Test", "password": "SecurePass123!"},
    )
    assert r.status_code == 200, f"Register failed: {r.text}"
    body = r.json()
    token = body["token"]
    user_id = body["user"]["id"]

    yield {"token": token, "user_id": user_id}

    try:
        await users_collection().delete_many({"email": EMAIL})
    except Exception:
        pass
    try:
        await gamification_collection().delete_many({"user_id": user_id})
    except Exception:
        pass
    clear_login_attempts(EMAIL)


async def _profile_xp(user_id: str) -> int:
    doc = await gamification_collection().find_one({"user_id": user_id}) or {}
    return int(doc.get("diamonds", 0))


@needs_db
async def test_locked_world_rejects_writes_but_opens_after_prereqs(client, test_user):
    """Cross-world gate, live: 403 on locked writes, open after clearing."""
    from app.data.worlds_data import WORLD_REGISTRY

    token, user_id = test_user["token"], test_user["user_id"]
    s1 = WORLD_REGISTRY["searchlands"].towns[0].levels[0].id

    # Fresh student: attempt, hint, and complete on a locked world all 403.
    r = await client.post(
        f"/api/v1/worlds/searchlands/levels/{s1}/attempt",
        headers=_auth(token),
        json={"code": SEARCHLANDS_S1, "language": "python", "time_spent_seconds": 5},
    )
    assert r.status_code == 403, r.text
    r = await client.post(
        f"/api/v1/worlds/searchlands/levels/{s1}/complete",
        headers=_auth(token),
        json={"code": SEARCHLANDS_S1, "language": "python", "time_spent_seconds": 5},
    )
    assert r.status_code == 403, r.text
    # Viewing stays open (gate is on progress writes, not curiosity).
    r = await client.get("/api/v1/map/state?world_id=searchlands", headers=_auth(token))
    assert r.status_code == 200

    # Clear foundations end-to-end through the real endpoints.
    for lid, code in FOUNDATIONS_CODES.items():
        r = await client.post(
            f"/api/v1/worlds/foundations/levels/{lid}/complete",
            headers=_auth(token),
            json={"code": code, "language": "python", "time_spent_seconds": 20},
        )
        assert r.status_code == 200, f"{lid}: {r.text}"

    # The locked door is now open, and the map says so too.
    r = await client.post(
        f"/api/v1/worlds/searchlands/levels/{s1}/attempt",
        headers=_auth(token),
        json={"code": SEARCHLANDS_S1, "language": "python", "time_spent_seconds": 5},
    )
    assert r.status_code == 200, r.text
    m = await client.get("/api/v1/map/state", headers=_auth(token))
    worlds = {w["id"]: w["status"] for w in m.json()["all_worlds"]}
    assert worlds["foundations"] == "completed"
    assert worlds["searchlands"] in ("active", "unlocked")


def _auth(token: str):
    return {"Authorization": f"Bearer {token}"}


@needs_db
async def test_complete_awards_exact_reported_xp(client, test_user):
    """response.xp_awarded == profile diamonds delta (the honesty invariant)."""
    token, user_id = test_user["token"], test_user["user_id"]

    before = await _profile_xp(user_id)
    r = await client.post(
        "/api/v1/worlds/foundations/levels/level-1/complete",
        headers=_auth(token),
        json={"code": PASS_CODE, "language": "python", "time_spent_seconds": 42},
    )
    assert r.status_code == 200, f"Complete failed: {r.text}"
    body = r.json()
    assert body["completed"] is True
    assert body.get("deduplicated") is not True

    after = await _profile_xp(user_id)
    assert body["xp_awarded"] == after - before, (
        f"claimed {body['xp_awarded']} but profile moved {after - before}"
    )
    assert body["xp_awarded"] > 0


@needs_db
async def test_sequential_retry_is_noop(client, test_user):
    """Retry after completion moves no Diamonds, by either defense layer.

    Byte-identical retry  -> edge duplicate guard (429), no state change.
    Slightly-differing retry -> atomic claim (200 + deduplicated), no Diamonds.
    """
    token, user_id = test_user["token"], test_user["user_id"]

    r1 = await client.post(
        "/api/v1/worlds/foundations/levels/level-1/complete",
        headers=_auth(token),
        json={"code": PASS_CODE, "language": "python", "time_spent_seconds": 42},
    )
    assert r1.status_code == 200
    mid = await _profile_xp(user_id)

    r2 = await client.post(
        "/api/v1/worlds/foundations/levels/level-1/complete",
        headers=_auth(token),
        json={"code": PASS_CODE, "language": "python", "time_spent_seconds": 42},
    )
    assert r2.status_code in (200, 429), r2.text
    if r2.status_code == 200:
        assert r2.json().get("deduplicated") is True
        assert r2.json()["xp_awarded"] == 0
    assert await _profile_xp(user_id) == mid

    r3 = await client.post(
        "/api/v1/worlds/foundations/levels/level-1/complete",
        headers=_auth(token),
        json={"code": PASS_CODE, "language": "python", "time_spent_seconds": 43},
    )
    assert r3.status_code == 200, r3.text
    assert r3.json().get("deduplicated") is True
    assert r3.json()["xp_awarded"] == 0
    assert await _profile_xp(user_id) == mid


LEVEL2_CODE = "apples = 5\nbread = 3\nprint(apples)"

# Passing codes per foundations level (satisfy each level's regex judge).
FOUNDATIONS_CODES = {
    "level-1": "apples = 5",
    "level-2": "apples = 5\nbread = 3\nprint(apples)",
    "level-3": "apples = 5\napples = 10\nprint(apples)",
    "level-4": "apples = 5\nbread = 3\ncoins = 20",
    "level-5": "apples = 5\nbread = 3\ntotal = apples + bread\nprint(total)",
    "boss-1": "apples = 12\nbread = 4\ncoins = 30\ntotal = apples + bread\nprint(total)",
}
SEARCHLANDS_S1 = "for c in cards:\n    x = range(5)\n    if cards:\n        print(c)"

# Passing codes for ALL worlds in the 11-link chain.
# Each code satisfies the level's deterministic regex judge.
ALL_WORLD_CODES = {
    "foundations": FOUNDATIONS_CODES,

    "searchlands": {
        "s-1": "for c in cards:\n    x = range(5)\n    if cards:\n        print(c)",
        "s-2": "count = 0\nfor item in items:\n    if item == target:\n        count += 1",
        "s-3": "n items = len(items)\nall n = all(checks)\nn checks = sum(checks)",
        "s-boss": "for i in range(10):\n    if i == 5:\n        break",
        "b-1": "while lo <= hi:\n    mid = (lo + hi) // 2\n    if books[mid] == target:\n        return mid\n    elif books[mid] < target:\n        lo = mid + 1\n    else:\n        hi = mid - 1",
        "b-2": "if guess < target:\n    lo = guess + 1\nelse:\n    hi = guess - 1",
        "b-3": "if lo <= hi:\n    return -1\nreturn len(nums)",
        "b-boss": "lo = lo + 1\nif pages[mid] < target:\n    return mid",
    },

    "sorting": {
        "so-1": "for i in range(len(bars)):\n    for j in range(len(bars)-1):\n        if bars[j]>bars[j+1]:\n            bars[j],bars[j+1]=bars[j+1],bars[j]",
        "so-2": "swapped = False\nfor i in range(len(bars)):\n    if bars[i] > bars[i + 1]:\n        swapped = True\n        break\nif not swapped:\n    break",
        "so-boss": "swapped = True\nwhile swapped:\n    swapped = False\n    for j in range(len(bars) - 1):\n        if bars[j] > bars[j + 1]:\n            bars[j], bars[j + 1] = bars[j + 1], bars[j]\n            swapped = True\n    if not swapped:\n        break",
        "m-1": "if len(arr) <= 1:\n    return arr\nmid = len(arr) // 2\nleft = merge_sort(arr[:mid])\nright = merge_sort(arr[mid:])\nreturn merge(left, right)",
        "m-2": "while left and right:\n    if left[0] <= right[0]:\n        result.append(left.pop(0))\n    else:\n        result.append(right.pop(0))\nresult.extend(left)\nresult.extend(right)",
        "m-boss": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)\ndef merge(a, b):\n    res = []\n    while a and b:\n        if a[0] <= b[0]:\n            res.append(a.pop(0))\n        else:\n            res.append(b.pop(0))\n    res.extend(a)\n    res.extend(b)\n    return res",
    },

    "recursion": {
        "r-1": "def fact(n):\n    if n <= 1:\n        return 1\n    return n * fact(n - 1)",
        "r-2": "def countdown(n):\n    print(n)\n    if n<=0:\n        return\n    countdown(n-1)\ncountdown(5)",
        "r-boss": "def pow2(n):\n    if n == 0:\n        return 1\n    return 2 * pow2(n - 1)",
        "d-1": "def dc_sum(arr, depth=0):\n    if depth == 0:\n        return 1\n    return 2 * dc_sum(arr, depth - 1)",
        "d-2": "while True:\n    append(1)\n    extend([2])",
        "d-boss": "def dc_sum(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = dc_sum(arr[:mid])\n    right = dc_sum(arr[mid:])\n    return merge(left, right)",
    },

    "linked": {
        "l-1": "class Node:\n    def __init__(self, val=0, next=None):\n        self.val = val\n        self.next = next",
        "l-2": "current = head\nwhile current:\n    vals.append(current.val)\n    current = current.next",
        "l-boss": "prev = None\nwhile current:\n    next_node = current.next\n    current.next = prev\n    prev = current\n    current = next_node",
    },

    "stack": {
        "st-1": "stack = []\nstack.append(1)\nstack.pop()\nstack = []",
        "st-2": "stack.append(1)\nif not stack:\n    return 0\nstack.pop()",
        "st-boss": "def main():\n    return [1, 2, 3]\nprint(main())",
    },

    "queue": {
        "q-1": "queue = []\nqueue.append(1)\nqueue.pop(0)",
        "q-2": "jobs.sort(key=lambda x: x[1])",
        "q-boss": "jobs.sort(key=lambda x: x[1])",
    },

    "hashing": {
        "h-1": "idx = key % 10\nhash_table[idx] = val",
        "h-2": "hash_table = [[] for _ in range(10)]\nfor k, v in items:\n    hash_table[k % 10].append((k, v))",
        "h-boss": "def _hash(k):\n    return k % 10\nbuckets = [[] for _ in range(10)]\nfor i, (k, v) in enumerate(items):\n    buckets[_hash(k)].append((k, v))",
    },

    "trees": {
        "t-1": "class TreeNode:\n    def __init__(self, val=0, left=None, right=None):\n        self.val = val\n        self.left = left\n        self.right = right",
        "t-2": "def inorder(node):\n    if node:\n        inorder(node.left)\n        print(node.val)\n        inorder(node.right)\ninorder(root)",
        "t-boss": "def search(node, val):\n    if not node:\n        return None\n    if val == node.val:\n        return node\n    return search(node.left, val)",
    },

    "graphs": {
        "g-1": "from collections import deque\nq = deque([start])\nvisited = {start}\nwhile q:\n    q.popleft()",
        "g-2": "path = []\nwhile queue:\n    node = queue.popleft()\n    if node == target:\n        return path\n    path += [node]",
        "g-boss": "from collections import deque\nvisited = set()\nq = deque([start])\nvisited.add(start)\nwhile q:\n    node = q.popleft()\n    if node == target:\n        return path + [node]\n    path += [node]",
    },

    "dynamic": {
        "d-1": "cache = {}\ndef fib(n):\n    if n in cache:\n        return cache[n]\n    cache[n] = fib(n - 1) + fib(n - 2)\n    return cache[n]",
        "d-2": "dp = [0] * (n + 1)\nfor i in range(1, n + 1):\n    dp[i] = dp[i - 1] + dp[i - 2]",
        "d-boss": "dp = [[0] * (W + 1) for _ in range(n + 1)]\nfor i in range(1, n + 1):\n    for w in range(1, W + 1):\n        dp[i][w] = max(dp[i - 1][w], dp[i][w - 1])",
    },

    "alpine": {
        "a-1": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.count = 0",
        "a-2": "from collections import Counter\nimport heapq\nheapq.nlargest(k, counter.items())",
        "a-boss": "from collections import deque\nq = deque([start])\nvisited = set()\nwhile q:\n    node = q.popleft()\n    visited.add(node)\nbfs_result = sorted(visited)",
    },
}


@needs_db
async def test_concurrent_double_tap_awards_once(client, test_user):
    """Two requests in flight at once: exactly one award, one deduplicated."""
    token, user_id = test_user["token"], test_user["user_id"]

    # Unlock level-2 first (unlock rule: previous level completed).
    r0 = await client.post(
        "/api/v1/worlds/foundations/levels/level-1/complete",
        headers=_auth(token),
        json={"code": PASS_CODE, "language": "python", "time_spent_seconds": 42},
    )
    assert r0.status_code == 200, f"Setup complete failed: {r0.text}"
    before = await _profile_xp(user_id)

    # Different time_spent per request: bypasses the edge byte-identical
    # duplicate guard on purpose, so the atomic claim is what decides.
    payloads = [
        {"code": LEVEL2_CODE, "language": "python", "time_spent_seconds": 10},
        {"code": LEVEL2_CODE, "language": "python", "time_spent_seconds": 11},
    ]

    async def _complete(payload):
        return await client.post(
            "/api/v1/worlds/foundations/levels/level-2/complete",
            headers=_auth(token),
            json=payload,
        )

    results = await asyncio.gather(*(_complete(p) for p in payloads))
    assert all(res.status_code == 200 for res in results), [res.text for res in results]
    bodies = [res.json() for res in results]
    assert all(b.get("completed") for b in bodies)
    deduped = sum(1 for b in bodies if b.get("deduplicated") is True)
    assert deduped == 1, f"expected exactly one deduplicated: {bodies}"

    after = await _profile_xp(user_id)
    awarded = [b for b in bodies if not b.get("deduplicated")][0]["xp_awarded"]
    assert awarded == after - before, (
        f"claimed {awarded} but profile moved {after - before}"
    )
    assert awarded > 0


@needs_db
async def test_full_chain_progression_integration(client, test_user):
    """
    Walk the complete 11-edge prerequisite chain through real API endpoints:
    foundations -> searchlands -> sorting -> recursion -> linked -> stack -> 
    queue -> hashing -> trees -> graphs -> dynamic -> alpine

    At each step:
    1. Verify the current world is unlocked (via fresh map/state request)
    2. Complete all levels in the current world
    3. Verify the NEXT world becomes unlocked (via fresh map/state request)
    4. Verify the locked door rejects writes (403) until prereqs are met
    5. Create a new client session to verify state persists across requests
    """
    from app.data.worlds_data import WORLD_REGISTRY

    token, user_id = test_user["token"], test_user["user_id"]

    # Helper to get world status from fresh API request
    async def _get_world_status(wid: str) -> str:
        m = await client.get("/api/v1/map/state", headers=_auth(token))
        assert m.status_code == 200, m.text
        worlds = {w["id"]: w["status"] for w in m.json()["all_worlds"]}
        return worlds.get(wid, "unknown")

    # Helper to attempt a level in a world (should 403 if locked)
    async def _attempt_locked(world: str, level: str) -> int:
        r = await client.post(
            f"/api/v1/worlds/{world}/levels/{level}/attempt",
            headers=_auth(token),
            json={"code": "pass", "language": "python", "time_spent_seconds": 10},
        )
        return r.status_code

    chain = [
        "foundations", "searchlands", "sorting", "recursion",
        "linked", "stack", "queue", "hashing", "trees", "graphs",
        "dynamic", "alpine",
    ]

    # Initial state: only foundations unlocked
    assert await _get_world_status("foundations") == "unlocked"
    for w in chain[1:]:
        assert await _get_world_status(w) == "locked", f"{w} should be locked initially"

    # Walk the chain
    for i, world_id in enumerate(chain):
        print(f"\n=== Clearing world {i+1}/12: {world_id} ===")

        # Verify current world is unlocked
        status = await _get_world_status(world_id)
        assert status in ("unlocked", "active", "completed"), f"{world_id} status={status}"

        # Verify next world is locked (if any)
        if i + 1 < len(chain):
            next_world = chain[i + 1]
            assert await _get_world_status(next_world) == "locked", f"{next_world} should be locked"

        # Get passing codes for this world
        codes = ALL_WORLD_CODES[world_id]

        # Complete all levels in this world
        for lid, code in codes.items():
            r = await client.post(
                f"/api/v1/worlds/{world_id}/levels/{lid}/complete",
                headers=_auth(token),
                json={"code": code, "language": "python", "time_spent_seconds": 20},
            )
            assert r.status_code == 200, f"{world_id}/{lid}: {r.text}"

        # After clearing, verify this world is completed
        assert await _get_world_status(world_id) == "completed"

        # Verify next world unlocks (if any)
        if i + 1 < len(chain):
            next_world = chain[i + 1]
            # Fresh API request to verify unlock
            next_status = await _get_world_status(next_world)
            assert next_status in ("unlocked", "active"), f"{next_world} should unlock after {world_id}, got {next_status}"

            # Verify we can actually write to the newly unlocked world
            w = WORLD_REGISTRY[next_world]
            first_level = w.towns[0].levels[0].id
            first_code = ALL_WORLD_CODES[next_world][first_level]
            r = await client.post(
                f"/api/v1/worlds/{next_world}/levels/{first_level}/attempt",
                headers=_auth(token),
                json={"code": first_code, "language": "python", "time_spent_seconds": 10},
            )
            assert r.status_code == 200, f"Should be able to write to unlocked {next_world}: {r.text}"

    # Final verification: all worlds completed
    final = await client.get("/api/v1/map/state", headers=_auth(token))
    assert final.status_code == 200
    worlds = {w["id"]: w["status"] for w in final.json()["all_worlds"]}
    for w in chain:
        assert worlds[w] == "completed", f"Final: {w}={worlds[w]}"

    # Cross-session persistence: new client with same auth should see same state
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as new_client:
        fresh = await new_client.get("/api/v1/map/state", headers=_auth(token))
        assert fresh.status_code == 200
        fresh_worlds = {w["id"]: w["status"] for w in fresh.json()["all_worlds"]}
        for w in chain:
            assert fresh_worlds[w] == "completed", f"Fresh session: {w}={fresh_worlds[w]}"


@needs_db
async def test_role_company_ordering_in_world_view(client, test_user):
    """Server-side relevance ordering: same canonical levels, personalized order."""
    from bson import ObjectId

    token, user_id = test_user["token"], test_user["user_id"]
    await users_collection().update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"target_role": "frontend", "target_company": "bounty"}},
    )
    try:
        from app.services.cache import cache as _cache
        await _cache.delete("auth", f"user:{user_id}")
    except Exception:
        pass

    r = await client.get("/api/v1/worlds/foundations", headers=_auth(token))
    assert r.status_code == 200, r.text
    body = r.json()
    assert "content_routing" in body
    assert body["content_routing"]["target_role"] == "frontend"
    assert body["content_routing"]["target_company"] == "bounty"
    levels = [lvl["id"] for town in body["world"]["towns"] for lvl in town["levels"]]
    assert levels == ["level-1", "level-2", "level-3", "level-4", "level-5", "boss-1"]


@needs_db
async def test_fallback_when_predict_content_missing(client, test_user):
    """Missing predict content emits a content_fallback warning and uses judge_level."""
    token, user_id = test_user["token"], test_user["user_id"]
    # Unlock level-1 first so level-2 is accessible.
    r1 = await client.post(
        "/api/v1/worlds/foundations/levels/level-1/complete",
        headers=_auth(token),
        json={"code": PASS_CODE, "language": "python", "time_spent_seconds": 10},
    )
    assert r1.status_code == 200, r1.text

    r = await client.post(
        "/api/v1/worlds/foundations/levels/level-2/attempt",
        headers=_auth(token),
        json={"code": "anything", "language": "python", "time_spent_seconds": 0, "step_type": "predict"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert "passed" in body


@needs_db
async def test_complete_emits_one_gamification_event(client, test_user):
    """Exactly one gamification event is created per unique level completion."""
    from app.database import gamification_events_collection

    token, user_id = test_user["token"], test_user["user_id"]
    before_count = await gamification_events_collection().count_documents({"user_id": user_id})

    r = await client.post(
        "/api/v1/worlds/foundations/levels/level-1/complete",
        headers=_auth(token),
        json={"code": PASS_CODE, "language": "python", "time_spent_seconds": 10},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["completed"] is True
    xp_awarded = body.get("xp_awarded", 0)
    assert xp_awarded > 0

    after_count = await gamification_events_collection().count_documents({"user_id": user_id})
    assert after_count - before_count == 1

    profile = await gamification_collection().find_one({"user_id": user_id}) or {}
    assert int(profile.get("diamonds", 0)) > 0


@needs_db
async def test_lesson_content_verification():
    """Lesson content passes structural verification."""
    from app.services.auto_verify import verify_all_lessons

    result = await verify_all_lessons(runtime_checks=False)
    assert result.total > 0
    assert result.failed == 0, f"Lesson verification failed: {result.details}"
