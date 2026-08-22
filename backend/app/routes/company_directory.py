"""
Company Directory + Placement/Internship Calendar (2026-2027).

Serves the curated dataset of 140+ companies with, for each:
  * what they ask, * how the interview goes (process), * what to focus on,
  * and how to prepare using PlacementPro (our features).
Plus a month-by-month 2026-2027 calendar of drives, internship windows,
exams and hackathons.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from bson import ObjectId
from app.middleware.auth import get_current_user
from app.database import users_collection
from app.data.companies_2026_2027 import (
    get_companies,
    get_company,
    search_companies,
    get_calendar,
)

router = APIRouter(prefix="/api/v1/company-directory", tags=["Company Directory"])


@router.get("/companies")
async def list_companies(
    user=Depends(get_current_user),
    q: str = Query(None, description="Free-text search across name/tags/focus"),
    type: str = Query(None, description="Filter by company type"),
    tier: str = Query(None, description="Filter by tier"),
    month: str = Query(None, description="Filter by calendar month, e.g. 'Sep 2026'"),
    limit: int = Query(200, ge=1, le=500),
):
    if q:
        results = search_companies(q)
    else:
        results = get_companies()

    if type:
        results = [c for c in results if c.get("type") == type]
    if tier:
        results = [c for c in results if c.get("tier") == tier]
    if month:
        results = [c for c in results if month in c.get("calendar_months", [])]

    return {
        "count": len(results[:limit]),
        "total": len(results),
        "companies": results[:limit],
    }


@router.get("/companies/{company_id}")
async def get_company_detail(company_id: str, user=Depends(get_current_user)):
    company = get_company(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("/search")
async def search(user=Depends(get_current_user), q: str = Query("", min_length=1)):
    return {"count": len(search_companies(q)), "companies": search_companies(q)}


@router.get("/calendar")
async def calendar(user=Depends(get_current_user)):
    return {"calendar": get_calendar()}


@router.get("/filters")
async def filters(user=Depends(get_current_user)):
    companies = get_companies()
    types = sorted({c["type"] for c in companies})
    tiers = sorted({c["tier"] for c in companies})
    months = sorted({m for c in companies for m in c.get("calendar_months", [])})
    return {"types": types, "tiers": tiers, "months": months}


@router.get("/companies/{company_id}/progress")
async def get_progress(company_id: str, user=Depends(get_current_user)):
    doc = await users_collection.find_one(
        {"_id": ObjectId(user["id"])}, {"company_prep": 1}
    )
    completed = (doc or {}).get("company_prep", {}).get(company_id, [])
    return {"company_id": company_id, "completed": completed}


@router.post("/companies/{company_id}/progress")
async def save_progress(company_id: str, request: Request, user=Depends(get_current_user)):
    try:
        body = await request.json()
    except Exception:
        body = {}
    completed = [str(x) for x in (body.get("completed") or [])]
    await users_collection.update_one(
        {"_id": ObjectId(user["id"])},
        {"$set": {f"company_prep.{company_id}": completed}},
        upsert=True,
    )
    return {"ok": True, "company_id": company_id, "completed": completed}
