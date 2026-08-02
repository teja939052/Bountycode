from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app.database import users_collection, offers_collection
from app.middleware.auth import get_current_user
from app.services.ai import generate_salary_benchmark, generate_offer_comparison
from app.config import get_settings
from bson import ObjectId

router = APIRouter(prefix="/api/v1/salary", tags=["salary"])
settings = get_settings()


class SalaryBenchmarkRequest(BaseModel):
    job_title: str
    location: str
    company: str = ""
    years_experience: int = 0
    level: str = ""


class OfferComparisonRequest(BaseModel):
    offers: List[dict]


class SaveOfferRequest(BaseModel):
    company: str = ""
    title: str = ""
    offered_salary: float = 0
    total_compensation: float = 0
    location: str = ""
    years_experience: int = 0
    level: str = ""
    benefits: str = ""
    notes: str = ""


@router.post("/benchmark")
async def get_salary_benchmark(req: SalaryBenchmarkRequest, user=Depends(get_current_user)):
    benchmark = await generate_salary_benchmark(
        req.job_title, req.location, req.company, req.years_experience, req.level
    )
    return benchmark


@router.post("/compare")
async def compare_offers(req: OfferComparisonRequest, user=Depends(get_current_user)):
    if len(req.offers) < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 offers to compare")

    comparison = await generate_offer_comparison(req.offers)
    return comparison


@router.post("/save")
async def save_offer(req: SaveOfferRequest, user=Depends(get_current_user)):
    offer = req.model_dump()
    offer["user_id"] = user["id"]
    offer["created_at"] = datetime.now(timezone.utc)

    result = await offers_collection.insert_one(offer)

    return {"offer_id": str(result.inserted_id)}


@router.get("/history")
async def get_offer_history(user=Depends(get_current_user)):
    cursor = offers_collection.find(
        {"user_id": user["id"]}
    ).sort("created_at", -1).limit(20)

    offers = []
    async for doc in cursor:
        offers.append({
            "id": str(doc["_id"]),
            "company": doc.get("company", ""),
            "title": doc.get("title", ""),
            "total_compensation": doc.get("total_compensation", 0),
            "created_at": doc.get("created_at"),
        })

    return {"offers": offers}
