import re
import json
from typing import Dict, Any, List
from app.services.ai import chat_completion, parse_json


class ResumeEngine:
    """Strict, cost-optimized resume processing engine."""

    def __init__(self):
        # Regex patterns for ATS checks (zero-cost, algorithmic)
        self.ATS_PATTERNS = {
            "tables": re.compile(r'[\|\t]{2,}'),
            "columns": re.compile(r'\S{20,}\s{3,}\S{20,}'),
            "special_chars": re.compile(r'[\u25A0-\u25FF\u2B50\u2705\u2714\u2716\u26A0]'),
            "non_standard_fonts": re.compile(r'[\u2022\u2023\u25E6\u2043\u2219]'),
            "images": re.compile(r'\[image\]|\[photo\]|<img|!\[', re.IGNORECASE),
        }

        self.STANDARD_HEADERS = [
            "experience", "education", "skills", "summary", "objective",
            "projects", "certifications", "work history", "employment",
        ]

        self.WEAK_BULLET_PATTERNS = [
            re.compile(r'(?i)^responsible for\b'),
            re.compile(r'(?i)^helped with\b'),
            re.compile(r'(?i)^assisted in\b'),
            re.compile(r'(?i)^worked on\b'),
            re.compile(r'(?i)^participated in\b'),
            re.compile(r'(?i)^involved in\b'),
            re.compile(r'(?i)^was part of\b'),
        ]

        self.METRIC_PATTERNS = [
            re.compile(r'\d+%'),
            re.compile(r'\$\d+'),
            re.compile(r'\d+x\b'),
            re.compile(r'\d+ (percent|times|users|customers|team members)'),
            re.compile(r'reduced.*by \d+'),
            re.compile(r'increased.*by \d+'),
            re.compile(r'improved.*by \d+'),
            re.compile(r'saved.*\d+'),
        ]

    def verify_ats_formatting(self, plaintext_resume: str) -> Dict[str, Any]:
        """
        Zero-cost algorithmic ATS checker. No LLM calls.
        Returns flags for issues that will get resumes rejected by ATS.
        """
        flags = []
        score = 100

        # Check for graphical elements
        if self.ATS_PATTERNS["special_chars"].search(plaintext_resume):
            flags.append({
                "type": "SPECIAL_CHARS",
                "severity": "high",
                "msg": "Remove custom emojis/shapes. ATS reads them as gibberish.",
                "fix": "Replace with plain text equivalents"
            })
            score -= 15

        # Check for tables
        if self.ATS_PATTERNS["tables"].search(plaintext_resume):
            flags.append({
                "type": "TABLES",
                "severity": "high",
                "msg": "Tables detected. ATS cannot parse table structures.",
                "fix": "Convert to simple bullet lists"
            })
            score -= 20

        # Check for column layouts
        if self.ATS_PATTERNS["columns"].search(plaintext_resume):
            flags.append({
                "type": "MULTI_COLUMN",
                "severity": "high",
                "msg": "Multi-column layout detected. Causes parsing errors.",
                "fix": "Use single-column format"
            })
            score -= 15

        # Check for images
        if self.ATS_PATTERNS["images"].search(plaintext_resume):
            flags.append({
                "type": "IMAGES",
                "severity": "critical",
                "msg": "Images detected. ATS cannot read images.",
                "fix": "Remove all images and use text content"
            })
            score -= 25

        # Check for standard headers
        text_lower = plaintext_resume.lower()
        found_headers = [h for h in self.STANDARD_HEADERS if h in text_lower]
        if len(found_headers) < 3:
            flags.append({
                "type": "MISSING_HEADERS",
                "severity": "medium",
                "msg": f"Only {len(found_headers)} standard section headers found.",
                "fix": "Use: Experience, Education, Skills, Summary"
            })
            score -= 10

        # Check for contact info
        has_email = bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', plaintext_resume))
        has_phone = bool(re.search(r'[\d\-\(\)\s]{10,}', plaintext_resume))

        if not has_email:
            flags.append({
                "type": "NO_EMAIL",
                "severity": "high",
                "msg": "No email address found.",
                "fix": "Add professional email at top"
            })
            score -= 10

        if not has_phone:
            flags.append({
                "type": "NO_PHONE",
                "severity": "medium",
                "msg": "No phone number found.",
                "fix": "Add phone number"
            })
            score -= 5

        # Check for weak bullets
        lines = plaintext_resume.split('\n')
        weak_bullets = 0
        for line in lines:
            for pattern in self.WEAK_BULLET_PATTERNS:
                if pattern.match(line.strip()):
                    weak_bullets += 1
                    break

        if weak_bullets > 2:
            flags.append({
                "type": "WEAK_BULLETS",
                "severity": "medium",
                "msg": f"{weak_bullets} weak bullet points found (responsible for, helped with, etc.)",
                "fix": "Start with strong action verbs: Led, Built, Increased, Reduced"
            })
            score -= 10

        # Check for metrics
        metric_count = sum(1 for p in self.METRIC_PATTERNS if p.search(plaintext_resume))
        if metric_count < 2:
            flags.append({
                "type": "NO_METRICS",
                "severity": "medium",
                "msg": "Few quantified achievements found.",
                "fix": "Add numbers: percentages, dollar amounts, time saved"
            })
            score -= 10

        # Check word count
        word_count = len(plaintext_resume.split())
        if word_count < 200:
            flags.append({
                "type": "TOO_SHORT",
                "severity": "medium",
                "msg": f"Resume too short ({word_count} words).",
                "fix": "Aim for 400-600 words"
            })
            score -= 15
        elif word_count > 800:
            flags.append({
                "type": "TOO_LONG",
                "severity": "low",
                "msg": f"Resume too long ({word_count} words).",
                "fix": "Aim for 400-600 words"
            })
            score -= 5

        return {
            "passed": len(flags) == 0,
            "score": max(0, score),
            "flags": flags,
            "summary": f"{'Pass' if len(flags) == 0 else 'Fail'} - {len(flags)} issues found",
        }

    async def improve_bullet_strict(self, raw_bullet: str, context_industry: str = "tech") -> Dict[str, Any]:
        """
        Strict bullet improvement with metric enforcement.
        Uses X-Y-Z formula: Accomplished [X] as measured by [Y], by doing [Z].
        """
        system_prompt = (
            f"You are an elite technical recruiter specializing in {context_industry}. "
            "Transform weak bullets using the X-Y-Z formula: Accomplished [X] as measured by [Y], by doing [Z]. "
            "NEVER invent arbitrary currency numbers. If no metric is given, provide placeholder formats like '[X]%'. "
            "Return valid JSON matching the schema precisely."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Improve this bullet:\n\n{raw_bullet}"},
        ]

        response = await chat_completion(messages)
        result = parse_json(response)

        # Validate and clean the response
        return {
            "original": raw_bullet,
            "improved": result.get("improved", result.get("transformed_bullet", raw_bullet)),
            "action_verbs": result.get("action_verbs_used", result.get("action_verbs", [])),
            "metric_added": result.get("quantifiable_metric_added", result.get("metrics_added", [])),
            "ats_delta": result.get("estimated_ats_score_delta", result.get("ats_score_delta", 10)),
        }

    async def generate_missing_bullet(
        self,
        resume_text: str,
        job_description: str,
        missing_skill: str,
    ) -> Dict[str, Any]:
        """
        Generate a copy-pasteable bullet point that addresses a missing skill.
        This is the "Missing Bullet Generator" - the wallet puller.
        """
        system_prompt = (
            "You are an elite resume writer. Generate a single, powerful bullet point "
            "that addresses the missing skill/requirement. The bullet must:\n"
            "1. Be based on the candidate's existing experience (infer plausible context)\n"
            "2. Use the X-Y-Z formula: Accomplished [X] as measured by [Y], by doing [Z]\n"
            "3. Naturally incorporate the missing keyword\n"
            "4. Include a quantifiable metric (use [X]% placeholder if no real metric)\n"
            "5. Start with a strong action verb\n\n"
            "Return valid JSON with the bullet and explanation."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""RESUME:
{resume_text[:2000]}

JOB DESCRIPTION:
{job_description[:1000]}

MISSING SKILL TO ADDRESS: {missing_skill}

Generate a bullet point that bridges this gap."""},
        ]

        response = await chat_completion(messages)
        result = parse_json(response)

        return {
            "missing_skill": missing_skill,
            "generated_bullet": result.get("bullet", result.get("improved", "")),
            "explanation": result.get("explanation", "This bullet addresses the missing requirement"),
            "keywords_added": result.get("keywords_added", [missing_skill]),
        }

    async def tailor_resume_strict(
        self,
        resume_text: str,
        job_description: str,
        job_role: str = "",
    ) -> Dict[str, Any]:
        """
        Strict resume tailoring with keyword validation.
        Ensures no hallucinated keywords and validates against JD.
        """
        # Extract JD keywords algorithmically first
        jd_keywords = self._extract_keywords_algorithamic(job_description)
        resume_keywords = self._extract_keywords_algorithamic(resume_text)

        # Find gaps algorithmically
        missing_keywords = [kw for kw in jd_keywords if kw.lower() not in resume_text.lower()]

        system_prompt = (
            "You are an ATS optimization expert. Tailor the resume for the job description.\n\n"
            "RULES:\n"
            "1. ONLY use keywords that appear in the job description\n"
            "2. DO NOT invent or hallucinate experience\n"
            "3. Rephrase existing bullets to naturally include relevant keywords\n"
            "4. Maintain the original structure\n"
            "5. Provide specific, actionable changes\n\n"
            "Return valid JSON with the tailored resume and changes made."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"""ORIGINAL RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

TARGET ROLE: {job_role or 'not specified'}

TAILOR THIS RESUME. Focus on: {', '.join(missing_keywords[:10])}"""},
        ]

        response = await chat_completion(messages)
        result = parse_json(response)

        # Validate keywords used
        tailored_text = result.get("tailored_resume", result.get("optimized_resume", resume_text))
        keywords_used = [kw for kw in missing_keywords if kw.lower() in tailored_text.lower()]

        return {
            "tailored_resume": tailored_text,
            "keywords_added": keywords_used,
            "keywords_still_missing": [kw for kw in missing_keywords if kw not in keywords_used],
            "match_score": result.get("match_score", 70),
            "changes_made": result.get("changes_made", []),
        }

    def _extract_keywords_algorithamic(self, text: str) -> List[str]:
        """Extract keywords algorithmically (zero LLM cost)."""
        # Common tech keywords
        tech_keywords = [
            "python", "javascript", "java", "react", "node", "aws", "docker",
            "kubernetes", "sql", "mongodb", "redis", "git", "ci/cd", "agile",
            "scrum", "microservices", "rest", "graphql", "typescript", "go",
            "system design", "data structures", "algorithms", "machine learning",
        ]

        text_lower = text.lower()
        return [kw for kw in tech_keywords if kw in text_lower]
