"""Learning path service module.

Handles:
- Role-based learning path catalog
- Company-specific track catalog
- User enrollment and progress tracking
- Module unlocking and completion
- Diamonds rewards for path activities
- Recommendations based on user profile
"""
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any
from app.database import (
    users_collection,
    learning_progress_collection,
    user_learning_paths_collection,
    user_company_tracks_collection,
)
from app.services.gamification import record_practice
from app.data.learning_paths import ROLES, COMPANY_TRACKS
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Catalog helpers
# ---------------------------------------------------------------------------

def get_all_roles() -> List[Dict[str, Any]]:
    """Return all available role-based learning paths."""
    paths = []
    for key, role in ROLES.items():
        paths.append({
            "id": role["id"],
            "name": role["name"],
            "short_name": role["short_name"],
            "icon": role["icon"],
            "color": role["color"],
            "description": role["description"],
            "target_roles": role["target_roles"],
            "avg_package": role["avg_package"],
            "duration_weeks": role["duration_weeks"],
            "difficulty": role["difficulty"],
            "prerequisites": role["prerequisites"],
            "total_modules": len(role["modules"]),
            "total_xp": sum(m["xp_reward"] for m in role["modules"]) + role.get("final_project", {}).get("xp_reward", 0),
        })
    return paths


def get_role_path(role_id: str) -> Optional[Dict[str, Any]]:
    """Return a single role-based learning path."""
    return ROLES.get(role_id)


def get_all_company_tracks() -> List[Dict[str, Any]]:
    """Return all company-specific tracks."""
    tracks = []
    for key, track in COMPANY_TRACKS.items():
        total_modules = sum(len(s.get("modules", [])) for s in track.get("sections", []))
        total_xp = sum(
            m.get("diamonds", 0)
            for s in track.get("sections", [])
            for m in s.get("modules", [])
        )
        tracks.append({
            "id": track["id"],
            "company_id": track["company_id"],
            "name": track["name"],
            "full_name": track["full_name"],
            "icon": track["icon"],
            "color": track["color"],
            "role": track["role"],
            "package_range": track["package_range"],
            "duration_minutes": track["duration_minutes"],
            "difficulty": track["difficulty"],
            "description": track["description"],
            "total_sections": len(track.get("sections", [])),
            "total_modules": total_modules,
            "total_xp": total_xp,
        })
    return tracks


def get_company_track(track_id: str) -> Optional[Dict[str, Any]]:
    """Return a single company track."""
    return COMPANY_TRACKS.get(track_id)


# ---------------------------------------------------------------------------
# User progress helpers
# ---------------------------------------------------------------------------

async def _get_user_path_progress(user_id: str, path_id: str) -> Optional[Dict[str, Any]]:
    doc = await user_learning_paths_collection.find_one({"user_id": user_id, "path_id": path_id})
    return doc


async def _get_user_track_progress(user_id: str, track_id: str) -> Optional[Dict[str, Any]]:
    doc = await user_company_tracks_collection.find_one({"user_id": user_id, "track_id": track_id})
    return doc


def _serialize_progress(doc: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not doc:
        return {}
    result = dict(doc)
    if "_id" in result:
        result["_id"] = str(result["_id"])
    return result


# ---------------------------------------------------------------------------
# Enrollment
# ---------------------------------------------------------------------------

async def enroll_in_path(user_id: str, path_id: str) -> Dict[str, Any]:
    """Enroll user in a role-based learning path.

    Also sets the user's goal in the users collection so the Journey
    Engine and Study Engine can surface role-aligned activities.
    """
    role = ROLES.get(path_id)
    if not role:
        raise ValueError(f"Unknown role path: {path_id}")

    now = datetime.now(timezone.utc).isoformat()

    modules: Dict[str, Any] = {}
    for m in role["modules"]:
        modules[m["id"]] = {
            "module_id": m["id"],
            "completed": False,
            "completed_at": None,
            "xp_earned": 0,
            "score": None,
            "attempts": 0,
            "activities_completed": [],
        }

    doc = {
        "user_id": user_id,
        "path_id": path_id,
        "enrolled_at": now,
        "current_module_id": role["modules"][0]["id"] if role["modules"] else None,
        "modules": modules,
        "total_xp_earned": 0,
        "completed": False,
        "completed_at": None,
        "last_activity_at": now,
    }

    await user_learning_paths_collection.update_one(
        {"user_id": user_id, "path_id": path_id},
        {"$set": doc},
        upsert=True,
    )

    # ── Set user goal so Journey/Study engines pick it up ──
    try:
        await users_collection().update_one(
            {"user_id": user_id},
            {"$set": {
                "role_path": path_id,
                "target_role": role.get("short_name", path_id),
                "role_path_enrolled_at": now,
            }},
        )
    except Exception:
        pass

    try:
        await record_practice(user_id, "learning_path", 10, {"path_id": path_id, "action": "enroll"}, role=role.get("short_name", path_id))
    except Exception:
        pass

    return {"success": True, "path_id": path_id, "enrolled_at": now}


async def enroll_in_track(user_id: str, track_id: str, role: str = "sde") -> Dict[str, Any]:
    """Enroll user in a company-specific track.

    Also sets the user's company goal in the users collection so the Journey
    Engine and Study Engine can surface company-aligned activities.
    """
    track = COMPANY_TRACKS.get(track_id)
    if not track:
        raise ValueError(f"Unknown company track: {track_id}")

    now = datetime.now(timezone.utc).isoformat()

    sections: Dict[str, Any] = {}
    for section in track.get("sections", []):
        section_modules: Dict[str, Any] = {}
        for m in section.get("modules", []):
            section_modules[m["id"]] = {
                "module_id": m["id"],
                "completed": False,
                "completed_at": None,
                "xp_earned": 0,
                "score": None,
                "attempts": 0,
                "activities_completed": [],
            }
        sections[section["id"]] = {
            "section_id": section["id"],
            "title": section["title"],
            "completed": False,
            "modules": section_modules,
        }

    doc = {
        "user_id": user_id,
        "track_id": track_id,
        "enrolled_at": now,
        "current_section_id": track["sections"][0]["id"] if track.get("sections") else None,
        "sections": sections,
        "total_xp_earned": 0,
        "completed": False,
        "completed_at": None,
        "mock_score": None,
        "last_activity_at": now,
    }

    await user_company_tracks_collection.update_one(
        {"user_id": user_id, "track_id": track_id},
        {"$set": doc},
        upsert=True,
    )

    # ── Set user company goal so Journey/Study engines pick it up ──
    try:
        await users_collection().update_one(
            {"user_id": user_id},
            {"$set": {
                "company_track": track_id,
                "target_company": track.get("company_id", track_id),
                "company_track_enrolled_at": now,
            }},
        )
    except Exception:
        pass

    try:
        await record_practice(user_id, "company_track", 10, {"track_id": track_id, "action": "enroll"}, role=role or "sde")
    except Exception:
        pass

    return {"success": True, "track_id": track_id, "enrolled_at": now}


# ---------------------------------------------------------------------------
# Progress & completion
# ---------------------------------------------------------------------------

async def complete_path_module(
    user_id: str,
    path_id: str,
    module_id: str,
    score: Optional[float] = None,
) -> Dict[str, Any]:
    """Mark a role-based path module as completed and unlock next module."""
    role = ROLES.get(path_id)
    if not role:
        raise ValueError(f"Unknown role path: {path_id}")

    module_def = next((m for m in role["modules"] if m["id"] == module_id), None)
    if not module_def:
        raise ValueError(f"Unknown module: {module_id}")

    now = datetime.now(timezone.utc).isoformat()

    base_xp = module_def.get("xp_reward", 0)
    bonus_xp = 0
    if score is not None and score >= 80:
        bonus_xp = int(base_xp * 0.25)
    total_xp = base_xp + bonus_xp

    await user_learning_paths_collection.update_one(
        {"user_id": user_id, "path_id": path_id, f"modules.{module_id}": {"$exists": True}},
        {
            "$set": {
                f"modules.{module_id}.completed": True,
                f"modules.{module_id}.completed_at": now,
                f"modules.{module_id}.xp_earned": total_xp,
                f"modules.{module_id}.score": score,
                f"modules.{module_id}.attempts": {"$add": [f"modules.{module_id}.attempts", 1]},
                "last_activity_at": now,
            }
        },
    )

    await user_learning_paths_collection.update_one(
        {"user_id": user_id, "path_id": path_id},
        {
            "$inc": {"total_xp_earned": total_xp},
            "$set": {"last_activity_at": now},
        },
    )

    try:
        await record_practice(user_id, "learning_path", score or 50, {
            "path_id": path_id,
            "module_id": module_id,
            "action": "complete_module",
            "xp_earned": total_xp,
        }, role=role.get("short_name", path_id))
    except Exception:
        pass

    next_unlocks = module_def.get("unlocks", [])
    if next_unlocks:
        for next_id in next_unlocks:
            await user_learning_paths_collection.update_one(
                {"user_id": user_id, "path_id": path_id},
                {"$set": {f"modules.{next_id}.locked": False}},
            )

    all_completed_doc = await user_learning_paths_collection.find_one(
        {"user_id": user_id, "path_id": path_id},
        {"modules": 1}
    )
    all_completed = all(
        m.get("completed", False)
        for m in (all_completed_doc or {}).get("modules", {}).values()
    )

    if all_completed:
        await user_learning_paths_collection.update_one(
            {"user_id": user_id, "path_id": path_id},
            {"$set": {"completed": True, "completed_at": now}},
        )
        try:
            await record_practice(user_id, "learning_path", 100, {
                "path_id": path_id,
                "action": "complete_path",
                "xp_earned": role.get("final_project", {}).get("xp_reward", 200),
            }, role=role.get("short_name", path_id))
        except Exception:
            pass

    return {
        "success": True,
        "module_id": module_id,
        "xp_earned": total_xp,
        "base_xp": base_xp,
        "bonus_xp": bonus_xp,
        "next_unlocks": next_unlocks,
        "path_completed": all_completed,
    }


async def complete_track_module(
    user_id: str,
    track_id: str,
    module_id: str,
    score: Optional[float] = None,
    role: str = "sde",
) -> Dict[str, Any]:
    """Mark a company track module as completed."""
    track = COMPANY_TRACKS.get(track_id)
    if not track:
        raise ValueError(f"Unknown company track: {track_id}")

    module_def = None
    for section in track.get("sections", []):
        for m in section.get("modules", []):
            if m["id"] == module_id:
                module_def = m
                break
        if module_def:
            break

    if not module_def:
        raise ValueError(f"Unknown module: {module_id}")

    now = datetime.now(timezone.utc).isoformat()

    base_xp = module_def.get("diamonds", 0)
    bonus_xp = 0
    if score is not None and score >= 80:
        bonus_xp = int(base_xp * 0.25)
    total_xp = base_xp + bonus_xp

    await user_company_tracks_collection.update_one(
        {"user_id": user_id, "track_id": track_id},
        {
            "$set": {
                f"sections.$[].modules.{module_id}.completed": True,
                f"sections.$[].modules.{module_id}.completed_at": now,
                f"sections.$[].modules.{module_id}.xp_earned": total_xp,
                f"sections.$[].modules.{module_id}.score": score,
                "last_activity_at": now,
            }
        },
    )

    await user_company_tracks_collection.update_one(
        {"user_id": user_id, "track_id": track_id},
        {
            "$inc": {"total_xp_earned": total_xp},
            "$set": {"last_activity_at": now},
        },
    )

    try:
        await record_practice(user_id, "company_track", score or 50, {
            "track_id": track_id,
            "module_id": module_id,
            "action": "complete_module",
            "xp_earned": total_xp,
        }, role=role or "sde")
    except Exception:
        pass

    return {
        "success": True,
        "module_id": module_id,
        "xp_earned": total_xp,
        "base_xp": base_xp,
        "bonus_xp": bonus_xp,
    }


# ---------------------------------------------------------------------------
# User progress retrieval
# ---------------------------------------------------------------------------

async def get_user_path_progress(user_id: str, path_id: str) -> Dict[str, Any]:
    """Get user's progress in a role-based learning path."""
    doc = await user_learning_paths_collection.find_one({"user_id": user_id, "path_id": path_id})
    if not doc:
        return {"enrolled": False, "path_id": path_id}
    return _serialize_progress(doc)


async def get_user_track_progress(user_id: str, track_id: str) -> Dict[str, Any]:
    """Get user's progress in a company track."""
    doc = await user_company_tracks_collection.find_one({"user_id": user_id, "track_id": track_id})
    if not doc:
        return {"enrolled": False, "track_id": track_id}
    return _serialize_progress(doc)


async def get_all_user_paths(user_id: str) -> List[Dict[str, Any]]:
    """Get all learning paths with enrollment status and progress."""
    cursor = user_learning_paths_collection.find({"user_id": user_id})
    results = []
    async for doc in cursor:
        path_id = doc.get("path_id")
        role = ROLES.get(path_id)
        if not role:
            continue

        total_modules = len(role["modules"])
        completed_modules = sum(1 for m in doc.get("modules", {}).values() if m.get("completed"))

        results.append({
            "id": path_id,
            "name": role["name"],
            "short_name": role["short_name"],
            "icon": role["icon"],
            "color": role["color"],
            "description": role["description"],
            "enrolled": True,
            "progress_pct": round(completed_modules / total_modules * 100) if total_modules > 0 else 0,
            "completed": doc.get("completed", False),
            "current_module_id": doc.get("current_module_id"),
            "total_xp_earned": doc.get("total_xp_earned", 0),
            "completed_modules": completed_modules,
            "total_modules": total_modules,
        })
    return results


async def get_all_user_tracks(user_id: str) -> List[Dict[str, Any]]:
    """Get all company tracks with enrollment status and progress."""
    cursor = user_company_tracks_collection.find({"user_id": user_id})
    results = []
    async for doc in cursor:
        track_id = doc.get("track_id")
        track = COMPANY_TRACKS.get(track_id)
        if not track:
            continue

        total_modules = sum(len(s.get("modules", [])) for s in track.get("sections", []))
        completed_modules = sum(
            1
            for s in doc.get("sections", {}).values()
            for m in s.get("modules", {}).values()
            if m.get("completed")
        )

        results.append({
            "id": track_id,
            "company_id": track["company_id"],
            "name": track["name"],
            "full_name": track["full_name"],
            "icon": track["icon"],
            "color": track["color"],
            "role": track["role"],
            "package_range": track["package_range"],
            "enrolled": True,
            "progress_pct": round(completed_modules / total_modules * 100) if total_modules > 0 else 0,
            "completed": doc.get("completed", False),
            "current_section_id": doc.get("current_section_id"),
            "total_xp_earned": doc.get("total_xp_earned", 0),
            "completed_modules": completed_modules,
            "total_modules": total_modules,
        })
    return results


# ---------------------------------------------------------------------------
# User goal helpers
# ---------------------------------------------------------------------------

async def get_user_goal(user_id: str) -> Dict[str, Any]:
    """Read the user's role/company goal from the users collection.

    Returns a dict with:
      - role_path: the enrolled role path id (e.g. "sde")
      - company_track: the enrolled company track id (e.g. "tcs_nqt")
      - target_company: the resolved company name (e.g. "tcs")
      - target_role: the resolved role name (e.g. "SDE")
    """
    try:
        user_doc = await users_collection().find_one({"user_id": user_id}) or {}
    except Exception:
        return {}

    return {
        "role_path": user_doc.get("role_path", ""),
        "company_track": user_doc.get("company_track", ""),
        "target_company": user_doc.get("target_company", ""),
        "target_role": user_doc.get("target_role", "") or user_doc.get("role", ""),
    }


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

async def get_recommended_paths(user_id: str) -> List[Dict[str, Any]]:
    """Recommend learning paths based on user profile and activity."""
    user_doc = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user_doc:
        return get_all_roles()

    recommendations = []
    for role_id, role in ROLES.items():
        match_score = 50.0
        reasons = ["General placement preparation"]

        progress = await get_user_path_progress(user_id, role_id)
        if progress.get("enrolled"):
            match_score += 20
            reasons.append("Already enrolled")

        try:
            from app.services.skill_assessment import get_skill_graph
            skill_graph = await get_skill_graph(user_id)
            if skill_graph and skill_graph.get("skills"):
                relevant_skills = [s for s in skill_graph["skills"] if s.get("category") in role.get("skills", [])]
                if relevant_skills:
                    match_score += 15
                    reasons.append(f"Matched {len(relevant_skills)} existing skills")
        except Exception:
            pass

        recommendations.append({
            "path_id": role_id,
            "name": role["name"],
            "short_name": role["short_name"],
            "icon": role["icon"],
            "color": role["color"],
            "match_score": min(100, match_score),
            "reason": "; ".join(reasons),
            "based_on": ["user_profile", "skill_graph", "enrollment_history"],
        })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:3]
