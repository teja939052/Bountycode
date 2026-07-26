from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class GenerateResume(BaseModel):
    name: str
    email: str = ""
    phone: str = ""
    target_role: str = ""
    experience: List[Dict[str, str]] = []
    education: List[Dict[str, str]] = []
    skills: List[str] = []


class OptimizeRequest(BaseModel):
    resume_id: str
    job_description: str


class ResumeAnalysis(BaseModel):
    overall_score: int = 0
    sections: Dict[str, Any] = {}
    strengths: List[str] = []
    improvements: List[str] = []


class ATSOptimization(BaseModel):
    ats_score: int = 0
    missing_keywords: List[str] = []
    present_keywords: List[str] = []
    optimized_resume: str = ""
    changes_made: List[str] = []
