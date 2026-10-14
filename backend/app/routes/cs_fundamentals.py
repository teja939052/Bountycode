from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any

from app.middleware.auth import get_current_user
from app.data.cs_fundamentals_theory import get_cs_domains, get_cs_topics, get_cs_theory, get_cs_by_domain

router = APIRouter(prefix="/api/v1/cs-fundamentals", tags=["cs-fundamentals"])


@router.get("/theory")
async def list_theory(user=Depends(get_current_user)):
    domains = get_cs_domains()
    topics = get_cs_topics()
    by_domain: Dict[str, List[Dict[str, str]]] = {}
    for topic in topics:
        by_domain.setdefault(topic["domain"], []).append(topic)
    return {
        "domains": domains,
        "topics": topics,
        "by_domain": by_domain,
        "total": len(topics),
    }


@router.get("/theory/{topic_id}")
async def get_theory(topic_id: str, user=Depends(get_current_user)):
    topic = get_cs_theory(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Theory topic not found.")
    return topic


@router.get("/domain/{domain}")
async def get_domain_theory(domain: str, user=Depends(get_current_user)):
    topics = get_cs_by_domain(domain)
    if not topics:
        raise HTTPException(status_code=404, detail="Domain not found.")
    return {
        "domain": domain,
        "topics": topics,
        "total": len(topics),
    }
