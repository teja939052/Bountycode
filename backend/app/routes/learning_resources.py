"""Read-only catalogue of curated external learning resources.

Resources are links to their publishers. This route never mirrors third-party
files and never records resource opens as mastery evidence.
"""
import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/v1/learning-resources", tags=["learning-resources"])
_CATALOG_PATH = Path(__file__).resolve().parents[2] / "data" / "content" / "resource_catalog.json"


@lru_cache(maxsize=1)
def _catalog() -> Dict[str, Any]:
    with _CATALOG_PATH.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("resources"), list):
        raise RuntimeError("Learning resource catalogue has an invalid structure")
    return data


def _tokens(value: str) -> set[str]:
    return {part for part in re.split(r"[^a-z0-9]+", value.lower()) if len(part) > 2}


def _score(resource: Dict[str, Any], domain: str, topic: str) -> int:
    score = 0
    wanted_domain = domain.strip().lower().replace("-", "_")
    domains = {str(item).lower().replace("-", "_") for item in resource.get("domains", [])}
    aliases = {
        "os": {"operating_systems"},
        "operating_systems": {"os"},
        "networks": {"computer_networks"},
        "computer_networks": {"networks"},
        "aptitude": {"quantitative_aptitude", "mathematics"},
        "quantitative": {"quantitative_aptitude", "mathematics"},
        "verbal": {"verbal_ability", "communication"},
        "dsa": {"algorithms"},
        "algorithms": {"dsa"},
        "cs": {"computer_science", "computer_science_fundamentals"},
    }
    if wanted_domain and (wanted_domain in domains or domains.intersection(aliases.get(wanted_domain, set()))):
        score += 10
    elif wanted_domain and not domains.intersection(aliases.get(wanted_domain, set())):
        score -= 2

    topic_tokens = _tokens(topic)
    if topic_tokens:
        resource_topics = _tokens(" ".join(resource.get("topics", [])))
        title_tokens = _tokens(resource.get("title", ""))
        score += 4 * len(topic_tokens.intersection(resource_topics))
        score += 2 * len(topic_tokens.intersection(title_tokens))
    return score


@router.get("")
async def list_learning_resources(
    domain: str = Query(default="", max_length=80),
    topic: str = Query(default="", max_length=160),
    limit: int = Query(default=12, ge=1, le=40),
):
    """Return relevant source links; no student progress or mastery is changed."""
    resources = _catalog()["resources"]
    ranked = []
    for resource in resources:
        score = _score(resource, domain, topic)
        if score > 0 or (not domain.strip() and not topic.strip()):
            ranked.append((score, resource))
    ranked.sort(key=lambda item: (-item[0], item[1].get("title", "")))
    return {
        "resources": [resource for _, resource in ranked[:limit]],
        "count": min(len(ranked), limit),
        "total_matches": len(ranked),
        "filters": {"domain": domain, "topic": topic},
        "catalog_version": _catalog().get("schema_version", "unknown"),
        "notice": "Resources open at their original publishers. Free access does not automatically grant republication rights.",
    }
