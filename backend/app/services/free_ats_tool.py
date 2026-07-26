import re
from typing import Dict, Any


class FreeATSTool:
    """
    Zero-cost, algorithmic ATS checker for marketing.
    This is the "Free Tool Trap" - gives value, drives signups.
    No LLM calls = zero operational cost.
    """

    def __init__(self):
        self.ISSUE_PATTERNS = {
            "tables": {
                "pattern": re.compile(r'[\|\t]{2,}'),
                "severity": "critical",
                "message": "Tables detected - ATS cannot parse table structures",
                "fix": "Convert tables to simple bullet lists",
                "impact": "High - ATS may skip entire sections",
            },
            "columns": {
                "pattern": re.compile(r'\S{20,}\s{4,}\S{20,}'),
                "severity": "critical",
                "message": "Multi-column layout detected",
                "fix": "Use single-column format for ATS compatibility",
                "impact": "High - Content may be read out of order",
            },
            "images": {
                "pattern": re.compile(r'\[image\]|\[photo\]|<img|!\[', re.IGNORECASE),
                "severity": "critical",
                "message": "Images/graphics detected",
                "fix": "Remove images - ATS cannot read them",
                "impact": "Critical - Information in images is invisible",
            },
            "special_chars": {
                "pattern": re.compile(r'[\u25A0-\u25FF\u2B50\u2705\u2714\u2716\u26A0\u2605\u2606]'),
                "severity": "high",
                "message": "Special characters/emojis detected",
                "fix": "Replace with plain text",
                "impact": "Medium - May cause parsing errors",
            },
            "headers": {
                "pattern": re.compile(r'(?i)(experience|education|skills|summary|objective|projects|certifications)', re.IGNORECASE),
                "severity": "medium",
                "message": "Standard section headers check",
                "fix": "Use standard headers: Experience, Education, Skills",
                "impact": "Medium - ATS looks for these to categorize content",
                "check": "contains",  # Special check - need at least 3
            },
            "email": {
                "pattern": re.compile(r'[\w.-]+@[\w.-]+\.\w+'),
                "severity": "high",
                "message": "Email address check",
                "fix": "Add professional email at top",
                "impact": "High - Contact info is essential",
                "check": "must_contain",
            },
            "phone": {
                "pattern": re.compile(r'[\d\-\(\)\s]{10,}'),
                "severity": "medium",
                "message": "Phone number check",
                "fix": "Add phone number",
                "impact": "Medium - Contact info completeness",
                "check": "must_contain",
            },
        }

        self.WEAK_BULLETS = [
            re.compile(r'(?i)^responsible for\b'),
            re.compile(r'(?i)^helped with\b'),
            re.compile(r'(?i)^assisted in\b'),
            re.compile(r'(?i)^worked on\b'),
            re.compile(r'(?i)^participated in\b'),
            re.compile(r'(?i)^involved in\b'),
            re.compile(r'(?i)^was part of\b'),
            re.compile(r'(?i)^familiar with\b'),
        ]

        self.STRONG_VERBS = [
            "led", "managed", "built", "created", "implemented", "designed",
            "increased", "reduced", "improved", "optimized", "automated",
            "delivered", "launched", "established", "spearheaded", "orchestrated",
        ]

    def analyze(self, resume_text: str) -> Dict[str, Any]:
        """
        Full ATS analysis - zero LLM cost.
        Returns detailed report suitable for Reddit/Discord responses.
        """
        issues = []
        score = 100

        # Run all pattern checks
        for check_name, check_info in self.ISSUE_PATTERNS.items():
            if check_info.get("check") == "contains":
                # Special check - count matches
                matches = check_info["pattern"].findall(resume_text)
                if check_name == "headers" and len(matches) < 3:
                    issues.append({
                        "type": "MISSING_HEADERS",
                        "severity": "medium",
                        "message": f"Only {len(matches)} standard section headers found",
                        "fix": "Use: Experience, Education, Skills, Summary",
                        "impact": "ATS uses headers to categorize content",
                    })
                    score -= 15
            elif check_info.get("check") == "must_contain":
                if not check_info["pattern"].search(resume_text):
                    issues.append({
                        "type": check_name.upper(),
                        "severity": check_info["severity"],
                        "message": check_info["message"],
                        "fix": check_info["fix"],
                        "impact": check_info["impact"],
                    })
                    score -= 10 if check_info["severity"] == "high" else 5
            else:
                if check_info["pattern"].search(resume_text):
                    issues.append({
                        "type": check_name.upper(),
                        "severity": check_info["severity"],
                        "message": check_info["message"],
                        "fix": check_info["fix"],
                        "impact": check_info["impact"],
                    })
                    # Deduct based on severity
                    if check_info["severity"] == "critical":
                        score -= 20
                    elif check_info["severity"] == "high":
                        score -= 15
                    else:
                        score -= 10

        # Check for weak bullets
        weak_count = sum(1 for p in self.WEAK_BULLETS if p.search(resume_text))
        if weak_count > 2:
            issues.append({
                "type": "WEAK_BULLETS",
                "severity": "medium",
                "message": f"{weak_count} weak bullet points found",
                "fix": "Start with strong action verbs (Led, Built, Increased)",
                "impact": "Reduces impact and ATS scoring",
            })
            score -= 10

        # Check for metrics
        metric_patterns = [r'\d+%', r'\$\d+', r'\d+x\b']
        metric_count = sum(1 for p in metric_patterns if re.search(p, resume_text))
        if metric_count < 2:
            issues.append({
                "type": "NO_METRICS",
                "severity": "medium",
                "message": "Few quantified achievements found",
                "fix": "Add numbers: percentages, dollar amounts, time saved",
                "impact": "ATS and recruiters look for measurable impact",
            })
            score -= 10

        # Word count check
        word_count = len(resume_text.split())
        if word_count < 200:
            issues.append({
                "type": "TOO_SHORT",
                "severity": "medium",
                "message": f"Resume too short ({word_count} words)",
                "fix": "Aim for 400-600 words",
                "impact": "May appear lacking in experience",
            })
            score -= 15
        elif word_count > 800:
            issues.append({
                "type": "TOO_LONG",
                "severity": "low",
                "message": f"Resume too long ({word_count} words)",
                "fix": "Aim for 400-600 words",
                "impact": "Recruiters spend 6 seconds scanning",
            })
            score -= 5

        return {
            "score": max(0, score),
            "passed": len([i for i in issues if i["severity"] in ["critical", "high"]]) == 0,
            "issues": issues,
            "summary": self._generate_summary(score, issues, word_count),
            "reddit_format": self._format_for_reddit(score, issues, word_count),
        }

    def _generate_summary(self, score: int, issues: list, word_count: int) -> str:
        """Generate a human-readable summary."""
        critical = len([i for i in issues if i["severity"] == "critical"])
        high = len([i for i in issues if i["severity"] == "high"])
        medium = len([i for i in issues if i["severity"] == "medium"])

        if score >= 80:
            return f"Your resume looks good! Score: {score}/100. {len(issues)} minor issues to fix."
        elif score >= 60:
            return f"Your resume needs some work. Score: {score}/100. {critical + high} critical issues found."
        else:
            return f"Your resume has significant ATS issues. Score: {score}/100. Fix the {critical + high} critical issues first."

    def _format_for_reddit(self, score: int, issues: list, word_count: int) -> str:
        """Format analysis for Reddit/Discord responses."""
        lines = [
            f"**ATS Score: {score}/100**",
            f"Word count: {word_count}",
            "",
        ]

        if issues:
            lines.append("**Issues found:**")
            for issue in issues[:5]:  # Top 5 issues
                emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(issue["severity"], "⚪")
                lines.append(f"- {emoji} {issue['message']}")
                lines.append(f"  Fix: {issue['fix']}")
            lines.append("")
        else:
            lines.append("No major issues found! Your resume should pass most ATS systems.")
            lines.append("")

        lines.append("*Powered by PlacementPro - Free ATS Checker*")

        return "\n".join(lines)
