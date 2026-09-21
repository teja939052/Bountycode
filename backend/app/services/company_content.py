"""Company content sync — ensures blueprints have sufficient verified content.

Maps company_blueprints.json sections to the question bank and reports coverage
gaps. This is a READ-ONLY diagnostic service: it does not modify content.
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_BACKEND_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
_BLUEPRINT_PATH = os.path.join(_BACKEND_ROOT, "app", "data", "company_blueprints.json")

# Minimum verified questions per section before we flag a gap
_MIN_SECTION_COVERAGE = 5


class CompanyContentAnalyzer:
    """Analyze coverage of company blueprints against the question bank."""

    def __init__(self, question_bank: List[Dict[str, Any]]):
        self._bank = question_bank
        self._blueprints = self._load_blueprints()

    # ── Public API ─────────────────────────────────────────────────────

    def coverage_report(self, company: Optional[str] = None) -> Dict[str, Any]:
        """Generate a coverage report for one company or all companies."""
        if company:
            bp = self._find_blueprint(company)
            if not bp:
                return {"error": f"No blueprint for company: {company}"}
            return {
                "company": company,
                "blueprint": bp.get("name", company),
                "sections": self._analyze_sections(bp),
            }

        # All companies
        reports = []
        for key, bp in self._blueprints.items():
            reports.append({
                "company": key,
                "name": bp.get("name", key),
                "sections": self._analyze_sections(bp),
            })
        return {"companies": reports}

    def gaps(self, company: Optional[str] = None) -> List[Dict[str, Any]]:
        """Return a flat list of coverage gaps (sections needing more content)."""
        report = self.coverage_report(company)
        gaps: List[Dict[str, Any]] = []

        if "companies" in report:
            for comp in report["companies"]:
                for sec in comp.get("sections", []):
                    if sec.get("status") == "gap":
                        gaps.append({
                            "company": comp["company"],
                            "section": sec["name"],
                            "current": sec["verified_count"],
                            "needed": _MIN_SECTION_COVERAGE,
                        })
        elif "sections" in report:
            for sec in report.get("sections", []):
                if sec.get("status") == "gap":
                    gaps.append({
                        "company": report.get("company", "unknown"),
                        "section": sec["name"],
                        "current": sec["verified_count"],
                        "needed": _MIN_SECTION_COVERAGE,
                    })
        return gaps

    def section_questions(
        self, company: str, section: str, difficulty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Return verified questions matching a company + section."""
        matches: List[Dict[str, Any]] = []
        for q in self._bank:
            companies = q.get("companies", [])
            if isinstance(companies, str):
                companies = [companies]
            if company.lower() not in [c.lower() for c in companies]:
                continue
            q_topic = (q.get("topic") or "").lower()
            q_sub = (q.get("sub_topic") or "").lower()
            if section.lower() not in (q_topic + " " + q_sub):
                continue
            if difficulty and q.get("difficulty") != difficulty:
                continue
            matches.append(q)
        return matches

    # ── Internals ──────────────────────────────────────────────────────

    def _load_blueprints(self) -> Dict[str, Any]:
        try:
            with open(_BLUEPRINT_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("company_blueprints", {})
        except Exception as exc:
            logger.warning("Failed to load blueprints: %s", exc)
            return {}

    def _find_blueprint(self, company: str) -> Optional[Dict[str, Any]]:
        key = company.lower()
        # Direct match
        if key in self._blueprints:
            return self._blueprints[key]
        # Alias match (e.g. "tcs" -> "tcs_nqt")
        for bp in self._blueprints.values():
            aliases = [a.lower() for a in bp.get("companies", [])]
            if key in aliases:
                return bp
        return None

    def _analyze_sections(self, bp: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze each section in a blueprint for coverage."""
        structure = bp.get("structure", {})
        sections: List[Dict[str, Any]] = []

        for stage_key in ("foundation", "advanced"):
            stage = structure.get(stage_key, {})
            topics = stage.get("topics", {})
            for section_key, info in topics.items():
                # Count questions matching this section
                count = self._count_for_section(bp, section_key)
                target = info.get("questions", info.get("problems", 0))
                sections.append({
                    "name": section_key,
                    "stage": stage_key,
                    "verified_count": count,
                    "target": target,
                    "status": "ok" if count >= _MIN_SECTION_COVERAGE else "gap",
                })
        return sections

    def _count_for_section(
        self, bp: Dict[str, Any], section_key: str
    ) -> int:
        """Count verified questions for a blueprint section."""
        companies = [bp.get("name", "").lower()] + [
            c.lower() for c in bp.get("companies", [])
        ]
        count = 0
        for q in self._bank:
            q_companies = q.get("companies", [])
            if isinstance(q_companies, str):
                q_companies = [q_companies]
            if not any(c.lower() in [qc.lower() for qc in q_companies] for c in companies):
                continue
            q_topic = (q.get("topic") or "").lower()
            q_sub = (q.get("sub_topic") or "").lower()
            if section_key.lower() in (q_topic + " " + q_sub):
                count += 1
        return count
