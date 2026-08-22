"""Resume AI functions: analysis, ATS optimization, content generation."""

import logging
from typing import Dict, Any, List
from app.services.ai_core import chat_completion, parse_json

logger = logging.getLogger(__name__)


async def analyze_resume(resume_text: str) -> Dict[str, Any]:
    system_prompt = """You are an expert resume reviewer and ATS (Applicant Tracking System) specialist.
Analyze the provided resume text thoroughly across 4 dimensions.

SCORING DIMENSIONS (each 1-10):
1. CONTENT: Relevance of experience, achievements quantified, skills listed, education details
2. FORMATTING: Structure, readability, consistent formatting, appropriate length (1-2 pages)
3. KEYWORDS: Industry-relevant keywords, technical terms, action verbs present
4. IMPACT: Strong action verbs, quantified achievements, clear value proposition

The output MUST be valid JSON with this exact structure:
{
    "score": 7,
    "overall_score": 7,
    "sections": {
        "content": {"score": 7, "feedback": "Detailed feedback on content"},
        "formatting": {"score": 6, "feedback": "Detailed feedback on formatting"},
        "keywords": {"score": 8, "feedback": "Detailed feedback on keywords"},
        "impact": {"score": 5, "feedback": "Detailed feedback on impact"}
    },
    "feedback": "Overall assessment paragraph",
    "suggestions": [
        "Specific actionable suggestion 1",
        "Specific actionable suggestion 2",
        "Specific actionable suggestion 3"
    ]
}

Be specific and actionable in your suggestions. Reference actual parts of the resume.

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze this resume:\n\n{resume_text[:4000]}"},
    ]

    result = await chat_completion(messages)
    parsed = parse_json(result)

    parsed.setdefault("score", 5)
    parsed.setdefault("overall_score", parsed["score"])
    parsed.setdefault("sections", {
        "content": {"score": 5, "feedback": ""},
        "formatting": {"score": 5, "feedback": ""},
        "keywords": {"score": 5, "feedback": ""},
        "impact": {"score": 5, "feedback": ""},
    })
    parsed.setdefault("feedback", "Resume needs improvement.")
    parsed.setdefault("suggestions", ["Add more quantified achievements", "Include more industry keywords"])

    return parsed


async def optimize_ats(resume_text: str, job_description: str) -> Dict[str, Any]:
    system_prompt = """You are an ATS (Applicant Tracking System) optimization expert.
Compare the resume against the job description and optimize it.

STEPS:
1. Extract all important keywords from the job description
2. Check which keywords are present/missing in the resume
3. Rewrite the resume to naturally incorporate missing keywords
4. Keep the original meaning while improving ATS compatibility
5. List all changes made

The output MUST be valid JSON with this exact structure:
{
    "ats_score": 65,
    "missing_keywords": ["keyword1", "keyword2", "keyword3"],
    "present_keywords": ["keyword4", "keyword5"],
    "optimized_resume": "The fully optimized resume text...",
    "changes_made": [
        "Added 'machine learning' to skills section",
        "Rewrote project description to include 'REST API'",
        "Updated job title to match ATS expectations"
    ]
}

Rules:
- ats_score is 0-100 (percentage of keyword match)
- missing_keywords: important terms from JD not in resume (max 15)
- present_keywords: important terms already in resume (max 15)
- optimized_resume: complete rewritten resume incorporating missing keywords naturally
- changes_made: list every modification made

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"RESUME:\n{resume_text[:3000]}\n\nJOB DESCRIPTION:\n{job_description[:2000]}\n\nOptimize this resume for the job description."},
    ]

    result = await chat_completion(messages, max_tokens=4000)
    parsed = parse_json(result)

    parsed.setdefault("ats_score", 50)
    parsed.setdefault("missing_keywords", [])
    parsed.setdefault("present_keywords", [])
    parsed.setdefault("optimized_resume", resume_text)
    parsed.setdefault("changes_made", ["General formatting improvements"])

    return parsed


async def generate_resume_content(
    name: str,
    email: str,
    target_role: str,
    experience: List[Dict[str, str]],
    education: List[Dict[str, str]],
    skills: List[str],
) -> Dict[str, Any]:
    exp_text = ""
    for exp in experience:
        exp_text += f"- {exp.get('role', 'Role')} at {exp.get('company', 'Company')} ({exp.get('duration', 'Duration')})\n  {exp.get('description', '')}\n"

    edu_text = ""
    for edu in education:
        edu_text += f"- {edu.get('degree', 'Degree')} from {edu.get('school', 'School')} ({edu.get('year', 'Year')}) GPA: {edu.get('gpa', 'N/A')}\n"

    system_prompt = f"""You are an expert resume writer. Generate professional resume content.
Target role: {target_role}
Name: {name}
Email: {email}

The content should:
- Use strong action verbs (Led, Developed, Implemented, Optimized, Architected)
- Quantify achievements where possible
- Be ATS-friendly with relevant keywords
- Be concise and impactful
- Follow a clean, professional format

The output MUST be valid JSON with this exact structure:
{{
    "content": "Full resume text with sections clearly separated",
    "sections": {{
        "summary": "Professional summary paragraph",
        "experience": [
            {{
                "company": "Company Name",
                "role": "Job Title",
                "duration": "Jan 2022 - Present",
                "bullets": ["Achievement 1 with metrics", "Achievement 2"]
            }}
        ],
        "education": [
            {{
                "school": "University Name",
                "degree": "Degree",
                "year": "2020",
                "gpa": "3.8"
            }}
        ],
        "skills": ["Skill 1", "Skill 2"]
    }}
}}

Return ONLY the JSON object. No markdown, no explanation."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Generate resume for {name} targeting {target_role}.\n\nExperience:\n{exp_text}\n\nEducation:\n{edu_text}\n\nSkills: {', '.join(skills)}"},
    ]

    result = await chat_completion(messages, max_tokens=3000)
    parsed = parse_json(result)

    parsed.setdefault("content", f"{name}\n{email}\n\n{target_role}")
    parsed.setdefault("sections", {
        "summary": "",
        "experience": experience,
        "education": education,
        "skills": skills,
    })

    return parsed