"""Content router: curated external resources with fallback. Metadata only."""
from datetime import datetime, timezone
from typing import Any, Dict, List

CURATED: Dict[str, List[Dict[str, Any]]] = {
    "percentages": [
        {"title": "IndiaBix Percentage", "url": "https://www.indiabix.com/aptitude/percentage/",
         "source": "indiabix", "stable": True},
    ],
}


def get_resources(pattern: str) -> List[Dict[str, Any]]:
    items = CURATED.get(pattern, [])
    out = []
    for r in items:
        out.append({
            "title": r["title"],
            "url": r["url"],
            "source": r["source"],
            "stable": r.get("stable", False),
            "accessed_at": datetime.now(timezone.utc).isoformat(),
            "fallback_search": "https://www.google.com/search?q=" + pattern + "+aptitude+practice",
        })
    return out


def record_external_completion(pattern: str, resource_url: str) -> Dict[str, Any]:
    return {
        "pattern": pattern,
        "resource_url": resource_url,
        "status": "opened",
        "verified": False,
        "requires_bountycode_check": True,
    }
