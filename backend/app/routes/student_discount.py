"""Student discount verification (academic email check)."""
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr
from app.middleware.auth import get_current_user
from app.services.student_discount import verify_student_discount, get_student_discount_status

router = APIRouter(prefix="/api/v1/discount", tags=["discount"])


class VerifyStudentRequest(BaseModel):
    email: EmailStr


@router.post("/verify-student")
async def verify_student(req: VerifyStudentRequest, user=Depends(get_current_user)):
    return await verify_student_discount(user["id"], req.email)


@router.get("/student-status")
async def student_status(user=Depends(get_current_user)):
    return await get_student_discount_status(user["id"])
