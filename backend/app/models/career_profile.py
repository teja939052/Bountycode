from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ContactInfo(BaseModel):
    email: str = ""
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    website: str = ""


class EducationEntry(BaseModel):
    school: str = ""
    degree: str = ""
    field: str = ""
    start_year: str = ""
    end_year: str = ""
    gpa: str = ""
    highlights: List[str] = []


class ExperienceEntry(BaseModel):
    title: str = ""
    company: str = ""
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    current: bool = False
    bullets: List[str] = []


class ProjectEntry(BaseModel):
    name: str = ""
    description: str = ""
    tech_stack: List[str] = []
    link: str = ""
    highlights: List[str] = []


class CertificationEntry(BaseModel):
    name: str = ""
    issuer: str = ""
    date: str = ""
    expiry: str = ""
    credential_id: str = ""


class CareerProfile(BaseModel):
    id: Optional[str] = None
    user_id: str
    full_name: str = ""
    contact: ContactInfo = Field(default_factory=ContactInfo)
    summary: str = ""
    skills: List[str] = []
    experience: List[ExperienceEntry] = []
    education: List[EducationEntry] = []
    projects: List[ProjectEntry] = []
    certifications: List[CertificationEntry] = []
    custom_sections: Dict[str, Any] = {}
    source: str = "manual"  # manual | resume_upload | github | linkedin
    resume_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    contact: Optional[ContactInfo] = None
    summary: Optional[str] = None
    skills: Optional[List[str]] = None
    experience: Optional[List[ExperienceEntry]] = None
    education: Optional[List[EducationEntry]] = None
    projects: Optional[List[ProjectEntry]] = None
    certifications: Optional[List[CertificationEntry]] = None
    custom_sections: Optional[Dict[str, Any]] = None


class ProfileFromResumeRequest(BaseModel):
    resume_text: str
    resume_id: Optional[str] = None
