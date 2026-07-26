import re
from typing import Dict, Any, List, Tuple
from collections import Counter


class RealATSScanner:
    """
    Production ATS scanner that simulates enterprise parsing behavior.
    Mimics Workday, Taleo, Greenhouse, Lever, iCIMS parsing logic.
    """

    def __init__(self):
        # Standard section headers that enterprise ATS parsers recognize
        self.standard_headers = {
            "experience": [
                "work experience", "professional experience", "employment history",
                "experience", "career history", "work history", "positions held",
            ],
            "education": [
                "education", "academic profile", "qualifications", "academic background",
                "degree", "university", "education background",
            ],
            "skills": [
                "skills", "technical skills", "core competencies", "technologies",
                "proficiencies", "skill set", "technical proficiencies",
            ],
            "summary": [
                "summary", "objective", "profile", "about me", "career objective",
                "professional summary", "career summary",
            ],
            "projects": [
                "projects", "key projects", "notable projects", "project experience",
            ],
            "certifications": [
                "certifications", "certificates", "licenses", "credentials",
            ],
        }

        # Contact information patterns
        self.contact_patterns = {
            "email": r'[\w.-]+@[\w.-]+\.\w{2,}',
            "phone": r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}',
            "linkedin": r'linkedin\.com/in/[\w-]+',
            "github": r'github\.com/[\w-]+',
        }

        # ATS parsing landmines
        self.landmines = {
            "tables": {
                "pattern": r'(?:\|.*\|.*\||\t.*\t.*\t)',
                "severity": "CRITICAL",
                "message": "Table structure detected - ATS will scramble content horizontally",
                "fix": "Convert tables to single-column bullet lists",
            },
            "columns": {
                "pattern": r'(?:\S{15,}\s{4,}\S{15,})',
                "severity": "CRITICAL",
                "message": "Multi-column layout detected - content will be read out of order",
                "fix": "Use single-column linear layout",
            },
            "images": {
                "pattern": r'(?:\[image\]|\[photo\]|<img|<svg|!\[)',
                "severity": "CRITICAL",
                "message": "Images/graphics detected - invisible to ATS",
                "fix": "Remove all images, use text content only",
            },
            "special_chars": {
                "pattern": r'[\u25A0-\u25FF\u2B50\u2705\u2714\u2716\u2605\u2022\u25CF\u25CB\u2713\u2717]',
                "severity": "HIGH",
                "message": "Unicode symbols may not render in ATS",
                "fix": "Replace with plain text (use - or * for bullets)",
            },
            "headers_footers": {
                "pattern": r'(?:^---+$|^\*\*\*+$|^===+$)',
                "severity": "MEDIUM",
                "message": "Horizontal rules detected - may be parsed as section breaks",
                "fix": "Remove decorative lines, use spacing instead",
            },
            "text_boxes": {
                "pattern": r'(?:┌.*┐|├.*┤|└.*┘|╔.*╗)',
                "severity": "CRITICAL",
                "message": "Text box/frame detected - content will be ignored",
                "fix": "Remove box frames, use plain text layout",
            },
        }

        # Weak bullet patterns (ATS and recruiter turn-offs)
        self.weak_bullets = [
            r'(?i)^\s*(?:responsible for|duties include|tasked with)\b',
            r'(?i)^\s*(?:helped|assisted|supported|participated)\b',
            r'(?i)^\s*(?:worked on|involved in|familiar with)\b',
            r'(?i)^\s*(?:was part of|contributed to)\b',
        ]

        # Strong action verbs
        self.strong_verbs = [
            "led", "managed", "built", "created", "implemented", "designed",
            "increased", "reduced", "improved", "optimized", "automated",
            "delivered", "launched", "established", "spearheaded", "orchestrated",
            "developed", "engineered", "architected", "deployed", "refactored",
            "streamlined", "accelerated", "transformed", "revolutionized",
        ]

        # Metric patterns
        self.metric_patterns = [
            r'\d+%',                          # Percentages
            r'\$\d+(?:,\d{3})*(?:\.\d{2})?',  # Dollar amounts
            r'\d+x\b',                        # Multipliers
            r'\d+\s*(?:users|customers|clients|team members|engineers|developers)',
            r'(?:reduced|increased|improved|saved|generated|achieved|delivered)\s+(?:by\s+)?\d+',
            r'\d+\s*(?:hours|days|weeks|months|years)',
            r'\d+\s*(?:K|M|B)\b',             # Thousands/Millions/Billions
        ]

    def full_scan(self, resume_text: str, job_description: str = None) -> Dict[str, Any]:
        """
        Complete ATS scan with structural parsing simulation.
        Returns detailed analysis of what would happen when ATS processes this resume.
        """
        # Phase 1: Structural parsing simulation
        parsing_result = self.simulate_ats_parsing(resume_text)

        # Phase 2: Section detection
        section_result = self.detect_sections(resume_text)

        # Phase 3: Contact information
        contact_result = self.detect_contact_info(resume_text)

        # Phase 4: Content quality
        content_result = self.analyze_content(resume_text)

        # Phase 5: Keyword matching (if JD provided)
        keyword_result = None
        if job_description:
            keyword_result = self.match_keywords(resume_text, job_description)

        # Calculate overall score
        overall_score = self.calculate_score(
            parsing_result, section_result, contact_result, content_result, keyword_result
        )

        # Generate line-by-line fixes
        line_fixes = self.generate_line_fixes(resume_text, parsing_result, section_result)

        return {
            "ats_score": overall_score["score"],
            "grade": overall_score["grade"],
            "would_pass_ats": overall_score["score"] >= 70,
            "parsing_simulation": parsing_result,
            "section_detection": section_result,
            "contact_detection": contact_result,
            "content_analysis": content_result,
            "keyword_analysis": keyword_result,
            "line_fixes": line_fixes,
            "critical_issues": self.get_critical_issues(parsing_result, section_result, contact_result),
            "recommendations": self.generate_recommendations(
                parsing_result, section_result, content_result, keyword_result
            ),
        }

    def simulate_ats_parsing(self, raw_text: str) -> Dict[str, Any]:
        """
        Simulate the mechanical and structural parsing pass of a modern ATS.
        This is the core engine that detects parsing failures.
        """
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

        # Track detected sections
        detected_sections = {k: False for k in self.standard_headers.keys()}
        section_line_map = {k: None for k in self.standard_headers.keys()}

        # 1. Section Header Detection
        current_section = None
        for i, line in enumerate(lines):
            lower_line = line.lower().strip(":- ")
            for section, variations in self.standard_headers.items():
                if lower_line in variations or any(v in lower_line for v in variations):
                    detected_sections[section] = True
                    section_line_map[section] = i + 1
                    current_section = section
                    break

        # 2. Landmine Detection
        landmines_found = []
        for landmine_name, landmine_config in self.landmines.items():
            if re.search(landmine_config["pattern"], raw_text, re.MULTILINE):
                landmines_found.append({
                    "type": landmine_name,
                    "severity": landmine_config["severity"],
                    "message": landmine_config["message"],
                    "fix": landmine_config["fix"],
                })

        # 3. Missing Section Detection
        missing_sections = []
        for section, found in detected_sections.items():
            if not found:
                missing_sections.append({
                    "section": section,
                    "severity": "CRITICAL",
                    "message": f"Missing '{section.upper()}' header - ATS cannot categorize this content",
                    "fix": f"Add a clear section header titled '{section.capitalize()}' on its own line",
                })

        # 4. Calculate parsing success score
        critical_count = sum(1 for l in landmines_found if l["severity"] == "CRITICAL")
        high_count = sum(1 for l in landmines_found if l["severity"] == "HIGH")
        missing_count = len(missing_sections)

        parsing_score = 100
        parsing_score -= critical_count * 20
        parsing_score -= high_count * 10
        parsing_score -= missing_count * 8
        parsing_score = max(0, parsing_score)

        return {
            "parsing_score": parsing_score,
            "parsed_successfully": critical_count == 0 and missing_count == 0,
            "detected_sections": detected_sections,
            "section_line_map": section_line_map,
            "missing_sections": missing_sections,
            "landmines_found": landmines_found,
            "total_lines": len(lines),
            "critical_count": critical_count,
            "high_count": high_count,
        }

    def detect_sections(self, text: str) -> Dict[str, Any]:
        """Detect and score resume sections."""
        lines = text.split('\n')
        found_sections = []
        missing_sections = []

        for section, variations in self.standard_headers.items():
            found = False
            line_number = None
            for i, line in enumerate(lines):
                if any(v in line.lower().strip(":- ") for v in variations):
                    found = True
                    line_number = i + 1
                    break

            if found:
                found_sections.append({"section": section, "line": line_number})
            else:
                missing_sections.append(section)

        # Section completeness score
        completeness = len(found_sections) / len(self.standard_headers) * 100

        return {
            "score": completeness,
            "found_sections": found_sections,
            "missing_sections": missing_sections,
            "completeness": f"{completeness:.0f}%",
            "passed": len(missing_sections) == 0,
        }

    def detect_contact_info(self, text: str) -> Dict[str, Any]:
        """Detect contact information."""
        found_contact = {}
        missing_contact = []

        for contact_type, pattern in self.contact_patterns.items():
            match = re.search(pattern, text)
            if match:
                found_contact[contact_type] = match.group()
            else:
                missing_contact.append(contact_type)

        # Contact completeness
        completeness = len(found_contact) / len(self.contact_patterns) * 100

        return {
            "score": completeness,
            "found": found_contact,
            "missing": missing_contact,
            "has_email": "email" in found_contact,
            "has_phone": "phone" in found_contact,
            "has_linkedin": "linkedin" in found_contact,
            "has_github": "github" in found_contact,
        }

    def analyze_content(self, text: str) -> Dict[str, Any]:
        """Analyze resume content quality."""
        lines = text.split('\n')
        word_count = len(text.split())

        # Count action verbs
        verb_count = 0
        for line in lines:
            if any(verb in line.lower() for verb in self.strong_verbs):
                verb_count += 1

        # Count metrics
        metric_count = 0
        for pattern in self.metric_patterns:
            metric_count += len(re.findall(pattern, text, re.IGNORECASE))

        # Count weak bullets
        weak_count = 0
        for line in lines:
            for weak_pattern in self.weak_bullets:
                if re.search(weak_pattern, line.strip()):
                    weak_count += 1
                    break

        # Calculate content score
        content_score = 100
        if verb_count < 8:
            content_score -= 15
        if metric_count < 3:
            content_score -= 15
        if weak_count > 2:
            content_score -= 10
        if word_count < 300:
            content_score -= 15
        elif word_count > 700:
            content_score -= 10

        return {
            "score": max(0, content_score),
            "word_count": word_count,
            "action_verb_count": verb_count,
            "metric_count": metric_count,
            "weak_bullet_count": weak_count,
            "has_enough_content": 300 <= word_count <= 700,
            "density": round(metric_count / max(1, word_count) * 100, 2),
        }

    def match_keywords(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        """Match resume keywords against job description."""
        # Extract important keywords from JD
        jd_keywords = self._extract_keywords(job_description)
        resume_lower = resume_text.lower()

        matched = []
        missing = []

        for keyword, importance in jd_keywords.items():
            if keyword.lower() in resume_lower:
                matched.append({"keyword": keyword, "importance": importance})
            else:
                missing.append({"keyword": keyword, "importance": importance})

        # Sort by importance
        matched.sort(key=lambda x: x["importance"], reverse=True)
        missing.sort(key=lambda x: x["importance"], reverse=True)

        total = len(jd_keywords)
        match_rate = len(matched) / total * 100 if total > 0 else 0

        return {
            "score": match_rate,
            "matched_keywords": matched,
            "missing_keywords": missing,
            "match_rate": f"{match_rate:.1f}%",
            "total_keywords": total,
            "matched_count": len(matched),
            "missing_count": len(missing),
        }

    def _extract_keywords(self, text: str) -> Dict[str, int]:
        """Extract important keywords with importance scores."""
        important_keywords = {
            "python": 3, "javascript": 3, "java": 3, "react": 3, "node": 2,
            "aws": 3, "docker": 2, "kubernetes": 2, "sql": 3, "mongodb": 2,
            "git": 2, "agile": 2, "scrum": 2, "ci/cd": 2, "rest": 2,
            "microservices": 2, "system design": 3, "algorithms": 3,
            "data structures": 3, "machine learning": 2, "api": 2,
            "typescript": 2, "golang": 2, "rust": 2, "redis": 2,
            "postgresql": 2, "mysql": 2, "graphql": 2, "terraform": 2,
        }

        text_lower = text.lower()
        found = {}

        for keyword, importance in important_keywords.items():
            if keyword in text_lower:
                found[keyword] = importance

        return found

    def calculate_score(
        self,
        parsing: Dict,
        sections: Dict,
        contact: Dict,
        content: Dict,
        keywords: Dict = None,
    ) -> Dict[str, Any]:
        """Calculate overall ATS score with weighted components."""
        weights = {
            "parsing": 0.30,   # Most critical - if ATS can't parse, nothing matters
            "sections": 0.25,  # ATS needs sections to categorize
            "contact": 0.10,   # Basic requirement
            "content": 0.20,   # Content quality
            "keywords": 0.15,  # JD matching
        }

        scores = {
            "parsing": parsing["parsing_score"],
            "sections": sections["score"],
            "contact": contact["score"],
            "content": content["score"],
            "keywords": keywords["score"] if keywords else 70,
        }

        weighted_score = sum(scores[k] * weights[k] for k in weights)

        # Determine grade
        if weighted_score >= 90:
            grade = "A"
        elif weighted_score >= 80:
            grade = "B"
        elif weighted_score >= 70:
            grade = "C"
        elif weighted_score >= 60:
            grade = "D"
        else:
            grade = "F"

        return {
            "score": round(weighted_score, 1),
            "grade": grade,
            "breakdown": scores,
            "weights": weights,
        }

    def get_critical_issues(
        self,
        parsing: Dict,
        sections: Dict,
        contact: Dict,
    ) -> List[Dict[str, str]]:
        """Get list of critical issues that will cause ATS rejection."""
        critical = []

        # Parsing issues
        for landmine in parsing.get("landmines_found", []):
            if landmine["severity"] == "CRITICAL":
                critical.append({
                    "issue": landmine["message"],
                    "fix": landmine["fix"],
                    "impact": "High - ATS will reject or misparse your resume",
                })

        # Missing sections
        for section in sections.get("missing_sections", []):
            critical.append({
                "issue": f"Missing {section} section",
                "fix": f"Add a '{section.capitalize()}' section header",
                "impact": "High - ATS cannot categorize your experience",
            })

        # Missing contact
        if not contact.get("has_email"):
            critical.append({
                "issue": "No email address found",
                "fix": "Add professional email at top of resume",
                "impact": "Critical - Cannot contact you for interview",
            })

        return critical

    def generate_recommendations(
        self,
        parsing: Dict,
        sections: Dict,
        content: Dict,
        keywords: Dict = None,
    ) -> List[Dict[str, str]]:
        """Generate specific, actionable recommendations."""
        recommendations = []

        # Format recommendations
        if not parsing["parsed_successfully"]:
            recommendations.append({
                "priority": "critical",
                "category": "format",
                "action": "Fix formatting issues that prevent ATS from reading your resume",
                "impact": "High - ATS will reject your resume without reading content",
            })

        # Section recommendations
        for section in sections.get("missing_sections", []):
            recommendations.append({
                "priority": "high",
                "category": "sections",
                "action": f"Add a {section.title()} section to your resume",
                "impact": "High - ATS uses sections to categorize your experience",
            })

        # Content recommendations
        if content["action_verb_count"] < 8:
            recommendations.append({
                "priority": "medium",
                "category": "content",
                "action": "Start bullet points with strong action verbs (Led, Built, Increased, Reduced)",
                "impact": "Medium - Action verbs show initiative and impact",
            })

        if content["metric_count"] < 3:
            recommendations.append({
                "priority": "medium",
                "category": "content",
                "action": "Add quantified achievements (%, $, numbers) to at least 3 bullet points",
                "impact": "Medium - Metrics demonstrate real impact",
            })

        # Keyword recommendations
        if keywords and keywords["missing_count"] > 0:
            top_missing = keywords["missing_keywords"][:5]
            recommendations.append({
                "priority": "high",
                "category": "keywords",
                "action": f"Add missing keywords: {', '.join([k['keyword'] for k in top_missing])}",
                "impact": "High - ATS filters resumes by keyword matching",
            })

        return recommendations

    def generate_line_fixes(
        self,
        text: str,
        parsing: Dict,
        sections: Dict,
    ) -> List[Dict[str, Any]]:
        """Generate line-by-line fix suggestions."""
        fixes = []
        lines = text.split('\n')

        # Check each line for issues
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            if not line_stripped:
                continue

            # Check for weak bullets
            for weak_pattern in self.weak_bullets:
                if re.search(weak_pattern, line_stripped):
                    fixes.append({
                        "line": i + 1,
                        "original": line_stripped,
                        "issue": "Weak bullet - starts with passive verb",
                        "suggestion": self._suggest_bullet_rewrite(line_stripped),
                        "reason": "ATS and recruiters prefer active voice with action verbs",
                    })
                    break

        # Add section-specific fixes
        for section in parsing.get("missing_sections", []):
            fixes.append({
                "line": None,
                "original": None,
                "issue": f"Missing {section} section",
                "suggestion": f"Add '{section.capitalize()}' as a section header on its own line",
                "reason": "ATS uses section headers to categorize your experience",
            })

        return fixes[:20]  # Limit to 20 fixes

    def _suggest_bullet_rewrite(self, bullet: str) -> str:
        """Suggest a rewrite for a weak bullet."""
        # Simple rewrite suggestions
        replacements = {
            "responsible for": "Managed",
            "helped with": "Contributed to",
            "assisted in": "Supported",
            "worked on": "Developed",
            "participated in": "Collaborated in",
            "involved in": "Contributed to",
        }

        rewritten = bullet
        for weak, strong in replacements.items():
            if weak.lower() in rewritten.lower():
                rewritten = re.sub(re.escape(weak), strong, rewritten, flags=re.IGNORECASE)
                break

        return rewritten
