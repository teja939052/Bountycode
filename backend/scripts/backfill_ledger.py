"""Backfill pre-ledger Diamonds as legacy_migration events.

Run from backend/:
  python scripts/backfill_ledger.py

For each user with Diamonds > 0 but no gamification_events, creates a single
legacy_migration event capturing their current state as the baseline.

This ensures every user with Diamonds has at least one ledger row, making
profile.diamonds == sum(gamification_events.xp_awarded) reconcile.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from datetime import datetime, timezone
import uuid
from app.database import gamification_collection, gamification_events_collection


async def backfill():
    """Find users with Diamonds but no events, and create legacy_migration events."""
    # Find all gamification profiles with diamonds > 0
    cursor = gamification_collection.find({"diamonds": {"$gt": 0}})
    profiles = await cursor.to_list(length=10000)
    
    backfilled = 0
    skipped = 0
    already_has_events = 0
    
    for profile in profiles:
        user_id = profile.get("user_id")
        if not user_id:
            continue
        
        diamonds = profile.get("diamonds", 0)
        if diamonds <= 0:
            skipped += 1
            continue
        
        # Check if user already has any gamification_events
        existing_count = await gamification_events_collection.count_documents(
            {"user_id": user_id}
        )
        if existing_count > 0:
            already_has_events += 1
            continue
        
        # Create legacy_migration event
        event = {
            "event_id": uuid.uuid4().hex,
            "user_id": user_id,
            "activity_id": f"legacy_{user_id}",
            "activity_type": "legacy_migration",
            "score": 0,
            "score_raw": 0,
            "base_xp": diamonds,
            "multipliers": {
                "streak": 1.0,
                "combo": 1.0,
                "first_of_day": False,
                "critical": 1.0,
                "double_xp": False,
            },
            "xp_awarded": diamonds,
            "coins_awarded": profile.get("coins", 0),
            "stars_awarded": profile.get("stars_total", 0),
            "new_badges": profile.get("badges", []),
            "level_after": profile.get("level", 1),
            "reward_policy_version": "legacy",
            "metadata": {
                "reason": "backfill_pre_ledger",
                "source": "backfill_ledger.py",
                "original_xp": diamonds,
                "original_coins": profile.get("coins", 0),
                "original_stars": profile.get("stars_total", 0),
                "original_streak": profile.get("streak", 0),
                "original_level": profile.get("level", 1),
                "backfilled_at": datetime.now(timezone.utc).isoformat(),
            },
            "created_at": datetime.now(timezone.utc),
        }
        
        await gamification_events_collection.insert_one(event)
        backfilled += 1
    
    print(f"Backfill complete:")
    print(f"  Profiles with Diamonds > 0: {len(profiles)}")
    print(f"  Already have events: {already_has_events}")
    print(f"  Backfilled (legacy_migration): {backfilled}")
    print(f"  Skipped (Diamonds=0): {skipped}")
    
    # Verify reconciliation
    total_profiles = await gamification_collection.count_documents({})
    profiles_with_xp = await gamification_collection.count_documents({"diamonds": {"$gt": 0}})
    profiles_with_events = 0
    mismatched = 0
    
    cursor2 = gamification_collection.find({"diamonds": {"$gt": 0}})
    all_profiles = await cursor2.to_list(length=10000)
    
    for p in all_profiles:
        uid = p.get("user_id")
        if not uid:
            continue
        ev_count = await gamification_events_collection.count_documents({"user_id": uid})
        if ev_count > 0:
            profiles_with_events += 1
            # Sum Diamonds from events
            pipeline = [
                {"$match": {"user_id": uid}},
                {"$group": {"_id": None, "total_xp": {"$sum": "$xp_awarded"}}}
            ]
            result = await gamification_events_collection.aggregate(pipeline).to_list(1)
            event_xp = result[0]["total_xp"] if result else 0
            profile_xp = p.get("diamonds", 0)
            if abs(event_xp - profile_xp) > 1:
                mismatched += 1
    
    print(f"\nReconciliation check:")
    print(f"  Total profiles: {total_profiles}")
    print(f"  Profiles with Diamonds > 0: {profiles_with_xp}")
    print(f"  Profiles with events: {profiles_with_events}")
    print(f"  Diamonds mismatches (|event_sum - profile_xp| > 1): {mismatched}")


if __name__ == "__main__":
    asyncio.run(backfill())
