import re
from typing import List, Dict, Tuple
from app.services.ai import chat_completion, parse_json


# Common weak bullet patterns
WEAK_PATTERNS = [
    r"responsible for",
    r"helped with",
    r"assisted in",
    r"worked on",
    r"participated in",
    r"involved in",
    r"contributed to",
    r"was part of",
]

# Strong action verbs by category
ACTION_VERBS = {
    "leadership": ["led", "managed", "directed", "oversaw", "spearheaded", "orchestrated", "guided", "mentored"],
    "achievement": ["achieved", "accomplished", "exceeded", "surpassed", "outperformed", "delivered", "secured"],
    "improvement": ["improved", "increased", "reduced", "optimized", "streamlined", "enhanced", "boosted", "accelerated"],
    "creation": ["created", "developed", "designed", "built", "launched", "implemented", "established", "founded"],
    "analysis": ["analyzed", "evaluated", "assessed", "investigated", "researched", "identified", "diagnosed"],
    "technical": ["automated", "integrated", "migrated", "deployed", "configured", "architected", "refactored"],
}


async def improve_bullet(bullet: str, job_role: str = "") -> Dict:
    """Improve a single bullet point with AI."""
    messages = [
        {
            "role": "system",
            "content": f"""You are an expert resume writer who transforms weak bullet points into powerful, ATS-friendly statements.

Current bullet: "{bullet}"

Transform this into a strong bullet point that:
1. Starts with a powerful action verb
2. Includes quantifiable metrics (numbers, percentages, dollar amounts)
3. Shows impact and results, not just responsibilities
4. Is specific and concrete
5. Is 1-2 lines max

Return ONLY valid JSON:
{{
    "original": "the original bullet",
    "improved": "the improved bullet point",
    "action_verb": "the action verb used",
    "metrics_added": ["metric 1", "metric 2"],
    "explanation": "why this is stronger",
    "ats_score_before": 40,
    "ats_score_after": 85
}}""",
        },
        {
            "role": "user",
            "content": f"Improve this bullet point for a {job_role or 'software engineer'} role:\n\n{bullet}",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)


async def improve_bullets(bullets: List[str], job_role: str = "") -> List[Dict]:
    """Improve multiple bullet points."""
    results = []
    for bullet in bullets:
        if bullet.strip():
            improved = await improve_bullet(bullet, job_role)
            results.append(improved)
    return results


def analyze_ats_formatting(resume_text: str) -> Dict:
    """Analyze resume for ATS formatting issues."""
    issues = []
    score = 100
    recommendations = []
    
    # Check for tables
    if "\t" in resume_text or "|" in resume_text:
        issues.append("Tables detected - ATS cannot parse tables properly")
        score -= 15
        recommendations.append("Convert tables to simple bullet lists")
    
    # Check for columns
    lines = resume_text.split("\n")
    for line in lines[:20]:
        if "  " in line and len(line) > 50:
            # Possible multi-column layout
            issues.append("Possible multi-column layout detected")
            score -= 10
            recommendations.append("Use single-column format for better ATS parsing")
            break
    
    # Check for images/graphics
    if any(marker in resume_text.lower() for marker in ["[image]", "[photo]", "icon", "logo"]):
        issues.append("Images/graphics detected - ATS cannot read images")
        score -= 20
        recommendations.append("Remove images and use text-based content")
    
    # Check for non-standard section headers
    standard_headers = ["experience", "education", "skills", "summary", "objective", "projects", "certifications"]
    found_headers = []
    for line in lines:
        line_lower = line.lower().strip()
        if any(h in line_lower for h in standard_headers):
            found_headers.append(line_lower)
    
    if len(found_headers) < 3:
        issues.append("Few standard section headers found")
        score -= 10
        recommendations.append("Use standard headers: Experience, Education, Skills, Summary")
    
    # Check for contact info
    has_email = bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', resume_text))
    has_phone = bool(re.search(r'[\d\-\(\)]{10,}', resume_text))
    
    if not has_email:
        issues.append("No email address found")
        score -= 10
        recommendations.append("Add a professional email address at the top")
    
    if not has_phone:
        issues.append("No phone number found")
        score -= 5
        recommendations.append("Add your phone number")
    
    # Check for special characters
    special_chars = len(re.findall(r'[^\w\s\-\.\,\@\#\$\%\^\&\*\(\)\+\=\/\>\<\:\;\!\?\[\]\{\}]', resume_text))
    if special_chars > 5:
        issues.append(f"Unusual characters detected ({special_chars})")
        score -= 5
        recommendations.append("Remove special characters that ATS may not recognize")
    
    # Check for date formats
    date_formats = re.findall(r'\b\d{4}\b', resume_text)
    if len(date_formats) < 2:
        issues.append("Few dates found - ATS looks for employment timeline")
        score -= 5
        recommendations.append("Add dates to your experience and education sections")
    
    # Check length
    word_count = len(resume_text.split())
    if word_count < 200:
        issues.append(f"Resume is too short ({word_count} words)")
        score -= 15
        recommendations.append("Aim for 400-600 words for a one-page resume")
    elif word_count > 800:
        issues.append(f"Resume is too long ({word_count} words)")
        score -= 10
        recommendations.append("Aim for 400-600 words - be concise")
    
    # Check for bullet points
    bullet_count = resume_text.count("•") + resume_text.count("- ") + resume_text.count("▸")
    if bullet_count < 5:
        issues.append(f"Few bullet points ({bullet_count})")
        score -= 10
        recommendations.append("Use bullet points for readability - aim for 5-8 per section")
    
    return {
        "score": max(0, score),
        "issues": issues,
        "recommendations": recommendations,
        "checks_passed": {
            "email": has_email,
            "phone": has_phone,
            "standard_headers": len(found_headers) >= 3,
            "bullet_points": bullet_count >= 5,
            "appropriate_length": 200 <= word_count <= 800,
            "no_tables": "\t" not in resume_text and "|" not in resume_text,
            "no_images": not any(m in resume_text.lower() for m in ["[image]", "[photo]"]),
        },
        "word_count": word_count,
        "bullet_count": bullet_count,
    }


async def generate_tailored_resume(
    resume_text: str,
    job_description: str,
    job_role: str = "",
) -> Dict:
    """Generate a tailored version of resume for a specific job."""
    messages = [
        {
            "role": "system",
            "content": f"""You are an expert resume writer who tailors resumes for specific job descriptions.

Given the original resume and job description:
1. Identify the top 10 keywords from the job description
2. Rephrase bullet points to include relevant keywords naturally
3. Highlight matching skills and experience
4. Remove irrelevant information
5. Maintain the original structure but optimize content

Return ONLY valid JSON:
{{
    "tailored_resume": "The complete tailored resume text",
    "keywords_added": ["keyword 1", "keyword 2"],
    "keywords_matched": ["keyword 3", "keyword 4"],
    "changes_made": ["change 1", "change 2"],
    "match_score": 75,
    "missing_keywords": ["keyword 5"],
    "recommendations": ["rec 1", "rec 2"]
}}""",
        },
        {
            "role": "user",
            "content": f"""ORIGINAL RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Tailor this resume for the {job_role or 'target role'} position.""",
        },
    ]
    
    response = await chat_completion(messages)
    return parse_json(response)
