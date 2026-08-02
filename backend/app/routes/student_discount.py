from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.middleware.auth import get_current_user
from app.services.student_discount import verify_student_discount, get_student_discount_status

router = APIRouter(prefix="/api/v1/discount", tags=["discount"])


class VerifyDiscountRequest(BaseModel):
    email: str


@router.post("/student/verify")
async def verify_student(req: VerifyDiscountRequest, user=Depends(get_current_user)):
    if not req.email or "@" not in req.email:
        raise HTTPException(status_code=400, detail="Valid email is required")
    return await verify_student_discount(user["id"], req.email)


@router.get("/student/status")
async def student_status(user=Depends(get_current_user)):
    return await get_student_discount_status(user["id"])
