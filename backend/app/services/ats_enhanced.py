import re
from collections import Counter
from typing import List, Dict, Tuple


# Common ATS keywords by industry
TECH_KEYWORDS = {
    "programming": ["python", "javascript", "java", "c++", "typescript", "go", "rust", "ruby", "php", "swift"],
    "frameworks": ["react", "angular", "vue", "node.js", "django", "flask", "fastapi", "spring", "rails", "next.js"],
    "databases": ["sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "dynamodb", "cassandra"],
    "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "jenkins", "github actions"],
    "skills": ["agile", "scrum", "git", "rest api", "graphql", "microservices", "testing", "debugging"],
    "soft_skills": ["leadership", "communication", "teamwork", "problem-solving", "analytical", "creative"],
}

INDUSTRY_KEYWORDS = {
    "finance": ["quantitative", "financial modeling", "risk management", "compliance", "audit", "sox"],
    "marketing": ["seo", "sem", "content marketing", "social media", "analytics", "campaign", "brand"],
    "healthcare": ["hipaa", "clinical", "patient", "medical", "healthcare", "compliance"],
}


def extract_keywords(text: str) -> Dict[str, List[str]]:
    """Extract keywords from text by category."""
    text_lower = text.lower()
    found = {}
    
    for category, keywords in {**TECH_KEYWORDS, **INDUSTRY_KEYWORDS}.items():
        found[category] = [kw for kw in keywords if kw in text_lower]
    
    return found


def calculate_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """Calculate semantic similarity between resume and job description."""
    resume_words = set(resume_text.lower().split())
    jd_words = set(jd_text.lower().split())
    
    if not jd_words:
        return 0
    
    intersection = resume_words & jd_words
    union = resume_words | jd_words
    
    # Jaccard similarity
    jaccard = len(intersection) / len(union) if union else 0
    
    # Keyword overlap with weighting
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    
    keyword_matches = 0
    total_jd_keywords = 0
    
    for category in jd_keywords:
        total_jd_keywords += len(jd_keywords[category])
        for kw in jd_keywords[category]:
            if kw in str(resume_keywords).lower():
                keyword_matches += 1
    
    keyword_score = keyword_matches / total_jd_keywords if total_jd_keywords > 0 else 0
    
    # Combined score
    return round((jaccard * 0.4 + keyword_score * 0.6) * 100, 1)


def analyze_sections(resume_text: str) -> Dict[str, Dict]:
    """Analyze resume sections and score each."""
    sections = {
        "summary": {"score": 0, "feedback": "", "present": False},
        "experience": {"score": 0, "feedback": "", "present": False},
        "skills": {"score": 0, "feedback": "", "present": False},
        "education": {"score": 0, "feedback": "", "present": False},
    }
    
    text_lower = resume_text.lower()
    
    # Check for summary/objective
    if any(kw in text_lower for kw in ["summary", "objective", "profile", "about"]):
        sections["summary"]["present"] = True
        sections["summary"]["score"] = 70
        sections["summary"]["feedback"] = "Summary section found"
    
    # Check for experience
    if any(kw in text_lower for kw in ["experience", "employment", "work history", "position"]):
        sections["experience"]["present"] = True
        sections["experience"]["score"] = 75
        sections["experience"]["feedback"] = "Experience section found"
    
    # Check for skills
    if any(kw in text_lower for kw in ["skills", "technologies", "competencies", "proficiencies"]):
        sections["skills"]["present"] = True
        sections["skills"]["score"] = 80
        sections["skills"]["feedback"] = "Skills section found"
    
    # Check for education
    if any(kw in text_lower for kw in ["education", "degree", "university", "college", "bachelor", "master"]):
        sections["education"]["present"] = True
        sections["education"]["score"] = 75
        sections["education"]["feedback"] = "Education section found"
    
    return sections


def analyze_impact_statements(resume_text: str) -> Dict:
    """Analyze if resume uses impact statements with metrics."""
    lines = resume_text.split("\n")
    impact_lines = 0
    total_lines = 0
    metrics_found = []
    
    metric_patterns = [
        r'\d+%',  # Percentages
        r'\$\d+',  # Dollar amounts
        r'\d+x',  # Multipliers
        r'\d+ \w+ users',  # User counts
        r'reduced.*by \d+',  # Reduction metrics
        r'increased.*by \d+',  # Increase metrics
        r'improved.*by \d+',  # Improvement metrics
    ]
    
    for line in lines:
        line = line.strip()
        if len(line) > 10:  # Skip short lines
            total_lines += 1
            for pattern in metric_patterns:
                if re.search(pattern, line.lower()):
                    impact_lines += 1
                    metrics_found.append(line[:50])
                    break
    
    impact_ratio = impact_lines / total_lines if total_lines > 0 else 0
    score = min(100, int(impact_ratio * 200))  # Scale to 0-100
    
    return {
        "score": score,
        "impact_ratio": round(impact_ratio * 100, 1),
        "impact_lines": impact_lines,
        "total_lines": total_lines,
        "sample_metrics": metrics_found[:3],
        "feedback": f"{impact_ratio*100:.0f}% of lines contain impact metrics" if impact_ratio > 0 else "No impact metrics found - add numbers, percentages, and results",
    }


def analyze_formatting(resume_text: str) -> Dict:
    """Analyze resume formatting quality."""
    issues = []
    score = 100
    
    # Check for common formatting issues
    if len(resume_text) > 5000:
        issues.append("Resume may be too long (over 5000 characters)")
        score -= 10
    
    if resume_text.count("\n\n\n") > 0:
        issues.append("Excessive blank lines detected")
        score -= 5
    
    # Check for bullet points
    bullet_count = resume_text.count("•") + resume_text.count("-") + resume_text.count("▸")
    if bullet_count < 5:
        issues.append("Few bullet points - use bullets for readability")
        score -= 10
    
    # Check for action verbs
    action_verbs = ["led", "managed", "developed", "implemented", "created", "improved", "increased", "reduced", "achieved", "delivered"]
    verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
    if verb_count < 3:
        issues.append("Few action verbs - start bullets with strong verbs")
        score -= 15
    
    return {
        "score": max(0, score),
        "issues": issues,
        "bullet_count": bullet_count,
        "action_verb_count": verb_count,
    }


def generate_keyword_gaps(resume_text: str, jd_text: str) -> Dict:
    """Generate detailed keyword gap analysis."""
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(jd_text)
    
    present = []
    missing = []
    suggestions = []
    
    for category, keywords in jd_keywords.items():
        for kw in keywords:
            if kw in str(resume_keywords).lower():
                present.append({"keyword": kw, "category": category})
            else:
                missing.append({"keyword": kw, "category": category})
                suggestions.append(f"Add '{kw}' to your skills section")
    
    return {
        "present": present,
        "missing": missing,
        "suggestions": suggestions[:10],  # Top 10 suggestions
        "match_rate": round(len(present) / (len(present) + len(missing)) * 100, 1) if (present or missing) else 0,
    }


def calculate_ats_score(resume_text: str, jd_text: str = None) -> Dict:
    """Calculate comprehensive ATS score with detailed breakdown."""
    # Section analysis
    sections = analyze_sections(resume_text)
    section_scores = [s["score"] for s in sections.values() if s["present"]]
    section_avg = sum(section_scores) / len(section_scores) if section_scores else 0
    
    # Impact analysis
    impact = analyze_impact_statements(resume_text)
    
    # Formatting analysis
    formatting = analyze_formatting(resume_text)
    
    # Keyword analysis (if JD provided)
    keyword_analysis = None
    keyword_score = 60  # Default if no JD
    if jd_text:
        keyword_analysis = generate_keyword_gaps(resume_text, jd_text)
        keyword_score = keyword_analysis["match_rate"]
    
    # Weighted final score
    weights = {
        "section_completeness": 0.25,
        "impact_statements": 0.25,
        "formatting": 0.20,
        "keywords": 0.30,
    }
    
    final_score = int(
        section_avg * weights["section_completeness"] +
        impact["score"] * weights["impact_statements"] +
        formatting["score"] * weights["formatting"] +
        keyword_score * weights["keywords"]
    )
    
    # Generate recommendations
    recommendations = []
    if not sections["summary"]["present"]:
        recommendations.append("Add a professional summary at the top")
    if impact["score"] < 50:
        recommendations.append("Add more metrics and quantified achievements")
    if formatting["score"] < 70:
        recommendations.extend(formatting["issues"])
    if keyword_analysis and keyword_analysis["missing"]:
        recommendations.append(f"Add missing keywords: {', '.join([k['keyword'] for k in keyword_analysis['missing'][:3]])}")
    
    return {
        "overall_score": min(100, final_score),
        "breakdown": {
            "section_completeness": {"score": round(section_avg, 1), "weight": "25%"},
            "impact_statements": {"score": impact["score"], "weight": "25%"},
            "formatting": {"score": formatting["score"], "weight": "20%"},
            "keywords": {"score": round(keyword_score, 1), "weight": "30%"},
        },
        "sections": sections,
        "impact_analysis": impact,
        "formatting_analysis": formatting,
        "keyword_analysis": keyword_analysis,
        "recommendations": recommendations[:5],
    }
