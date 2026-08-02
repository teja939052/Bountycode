from datetime import datetime, timezone, timedelta
from app.database import users_collection
from bson import ObjectId

MAX_ENERGY = 10
RECHARGE_HOURS = 4
ENERGY_PER_DAY = 6


async def get_energy(user: dict) -> dict:
    """Get current energy for user. Auto-recharges based on time elapsed."""
    now = datetime.now(timezone.utc)
    last_energy_time = user.get("last_energy_time", user.get("created_at", now))

    if user.get("plan") in ("pro", "lifetime"):
        return {"energy": MAX_ENERGY, "max": MAX_ENERGY, "next_recharge": None, "is_unlimited": True}

    if last_energy_time is None:
        last_energy_time = now

    last_energy_utc = last_energy_time.replace(tzinfo=timezone.utc) if last_energy_time.tzinfo is None else last_energy_time

    current_energy = user.get("energy", ENERGY_PER_DAY)
    hours_since = (now - last_energy_utc).total_seconds() / 3600
    recharge_amount = int(hours_since / RECHARGE_HOURS)

    if recharge_amount > 0:
        current_energy = min(MAX_ENERGY, current_energy + recharge_amount)
        new_last_time = last_energy_utc + timedelta(hours=recharge_amount * RECHARGE_HOURS)
        await users_collection.update_one(
            {"_id": ObjectId(user["id"])},
            {"$set": {"energy": current_energy, "last_energy_time": new_last_time}},
        )

    next_recharge = None
    if current_energy < MAX_ENERGY:
        next_recharge_hours = RECHARGE_HOURS - (hours_since % RECHARGE_HOURS)
        next_recharge = now + timedelta(hours=next_recharge_hours)

    return {
        "energy": current_energy,
        "max": MAX_ENERGY,
        "next_recharge": next_recharge.isoformat() if next_recharge else None,
        "is_unlimited": False,
    }


async def consume_energy(user: dict, amount: int = 1) -> bool:
    """Consume energy. Returns True if successful."""
    if user.get("plan") in ("pro", "lifetime"):
        return True

    current_energy = user.get("energy", ENERGY_PER_DAY)
    if current_energy < amount:
        return False

    new_energy = current_energy - amount
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"energy": new_energy}},
    )
    return True


async def add_daily_energy(user: dict) -> dict:
    """Add daily bonus energy (called on login)."""
    now = datetime.now(timezone.utc)
    today = now.date()
    last_daily = user.get("last_daily_energy_date")

    if last_daily:
        last_daily_date = last_daily.date() if isinstance(last_daily, datetime) else last_daily
        if last_daily_date == today:
            return {"added": False}

    current_energy = user.get("energy", ENERGY_PER_DAY)
    new_energy = min(MAX_ENERGY, current_energy + ENERGY_PER_DAY)

    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {"energy": new_energy, "last_daily_energy_date": now}},
    )

    return {"added": True, "energy": new_energy}
