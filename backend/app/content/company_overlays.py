"""Company overlays — versioned company profiles for the placement platform.

This module is the SINGLE source of truth for company-specific preparation data.
It supersedes:
- readiness_engine.COMPANY_PROFILES (partial data)
- company_blueprints.json (exam structure only)

No second company registry is created. All existing systems should migrate to
read from this module.

Design constraints:
- No claim of "most asked" unless independently verified evidence exists.
  Use calibrated pattern relevance levels instead.
- Versioned profiles with effective_from / effective_to.
- Provenance and confidence are explicit fields.
- Content trust: this module defines configuration only; no question content lives here.
"""

from __future__ import annotations

import copy
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class CompanyOverlay:
    """Versioned company profile for preparation guidance."""
    company_id: str
    display_name: str
    role: str  # e.g. "sde", "qa_test_engineer", "data_analyst"
    assessment_stages: List[Dict[str, Any]] = field(default_factory=list)
    skill_weights: Dict[str, float] = field(default_factory=dict)
    pattern_relevance: Dict[str, float] = field(default_factory=dict)
    question_filters: Dict[str, Any] = field(default_factory=dict)
    mock_blueprint: Dict[str, Any] = field(default_factory=dict)
    interview_focus: List[str] = field(default_factory=list)
    effective_from: str = ""
    effective_to: str = ""
    version: str = "1.0"
    source: str = "platform_config"
    provenance: str = "manually_curated"
    confidence: float = 0.8
    min_solved: int = 0
    min_medium: int = 0
    min_hard: int = 0
    min_skills: Dict[str, float] = field(default_factory=dict)
    focus_topics: List[str] = field(default_factory=list)
    interview_rounds: List[str] = field(default_factory=list)
    typical_timeline_weeks: int = 4
    match_weights: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "company_id": self.company_id,
            "display_name": self.display_name,
            "role": self.role,
            "assessment_stages": self.assessment_stages,
            "skill_weights": self.skill_weights,
            "pattern_relevance": self.pattern_relevance,
            "question_filters": self.question_filters,
            "mock_blueprint": self.mock_blueprint,
            "interview_focus": self.interview_focus,
            "effective_from": self.effective_from,
            "effective_to": self.effective_to,
            "version": self.version,
            "source": self.source,
            "provenance": self.provenance,
            "confidence": self.confidence,
            "min_solved": self.min_solved,
            "min_medium": self.min_medium,
            "min_hard": self.min_hard,
            "min_skills": self.min_skills,
            "focus_topics": self.focus_topics,
            "interview_rounds": self.interview_rounds,
            "typical_timeline_weeks": self.typical_timeline_weeks,
            "match_weights": self.match_weights,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _overlay(
    company_id: str,
    display_name: str,
    role: str = "sde",
    *,
    assessment_stages: Optional[List[Dict[str, Any]]] = None,
    skill_weights: Optional[Dict[str, float]] = None,
    pattern_relevance: Optional[Dict[str, float]] = None,
    question_filters: Optional[Dict[str, Any]] = None,
    mock_blueprint: Optional[Dict[str, Any]] = None,
    interview_focus: Optional[List[str]] = None,
    effective_from: str = "2025-01-01",
    effective_to: str = "",
    version: str = "2025-01",
    source: str = "platform_config",
    provenance: str = "manually_curated",
    confidence: float = 0.8,
    min_solved: int = 0,
    min_medium: int = 0,
    min_hard: int = 0,
    min_skills: Optional[Dict[str, float]] = None,
    focus_topics: Optional[List[str]] = None,
    interview_rounds: Optional[List[str]] = None,
    typical_timeline_weeks: int = 4,
    match_weights: Optional[Dict[str, float]] = None,
) -> CompanyOverlay:
    return CompanyOverlay(
        company_id=company_id,
        display_name=display_name,
        role=role,
        assessment_stages=assessment_stages or [],
        skill_weights=skill_weights or {},
        pattern_relevance=pattern_relevance or {},
        question_filters=question_filters or {},
        mock_blueprint=mock_blueprint or {},
        interview_focus=interview_focus or [],
        effective_from=effective_from,
        effective_to=effective_to,
        version=version,
        source=source,
        provenance=provenance,
        confidence=confidence,
        min_solved=min_solved,
        min_medium=min_medium,
        min_hard=min_hard,
        min_skills=min_skills or {},
        focus_topics=focus_topics or [],
        interview_rounds=interview_rounds or [],
        typical_timeline_weeks=typical_timeline_weeks,
        match_weights=match_weights or {},
    )


# ---------------------------------------------------------------------------
# Canonical company overlay definitions
# ---------------------------------------------------------------------------
# Pattern relevance is a 0.0–1.0 calibration, NOT a claim of "most asked".
# 0.8–1.0 = heavily emphasized in preparation materials
# 0.5–0.7 = regularly appears
# 0.2–0.4 = occasionally appears
# 0.0–0.1 = rare

_COMPANY_OVERLAYS: Dict[str, CompanyOverlay] = {}

def _build_overlays() -> Dict[str, CompanyOverlay]:
    o: Dict[str, CompanyOverlay] = {}

    # ── TCS (Tata Consultancy Services) ──────────────────────────────────
    o["tcs"] = _overlay(
        "tcs", "TCS", role="sde",
        min_solved=50, min_medium=20, min_hard=5,
        min_skills={"dsa": 50, "aptitude": 60, "verbal": 50, "coding": 50},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Verbal"],
        interview_rounds=["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.10, "resume": 0.03, "projects": 0.02},
        pattern_relevance={
            "aptitude.quantitative": 0.9,
            "aptitude.verbal": 0.8,
            "aptitude.logical": 0.8,
            "dsa.arrays_hashing": 0.7,
            "dsa.strings": 0.6,
            "dsa.binary_search": 0.5,
            "foundation.control_flow": 0.6,
            "cs_fundamentals.oops": 0.5,
            "cs_fundamentals.sql": 0.4,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding"],
            "difficulty": ["easy", "medium"],
            "companies": ["tcs"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "advanced_aptitude", "advanced_coding"],
            "total_questions": 82,
            "duration_minutes": 190,
            "negative_marking": False,
        },
        interview_focus=["communication", "aptitude_application", "basic_coding"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="tcsonly_released_structure",
        confidence=0.85,
    )

    # ── Infosys ──────────────────────────────────────────────────────────
    o["infosys"] = _overlay(
        "infosys", "Infosys", role="sde",
        min_solved=60, min_medium=25, min_hard=5,
        min_skills={"dsa": 45, "aptitude": 55, "verbal": 45, "coding": 45},
        focus_topics=["Arrays", "Strings", "Basic Data Structures", "Aptitude", "Pseudo-code"],
        interview_rounds=["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.32, "dsa": 0.23, "cs_fundamentals": 0.13, "coding": 0.15, "interview": 0.12, "resume": 0.03, "projects": 0.02},
        pattern_relevance={
            "aptitude.quantitative": 0.9,
            "aptitude.verbal": 0.75,
            "aptitude.logical": 0.75,
            "dsa.arrays_hashing": 0.65,
            "dsa.strings": 0.6,
            "foundation.control_flow": 0.6,
            "foundation.programming_basics": 0.6,
            "cs_fundamentals.oops": 0.5,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding"],
            "difficulty": ["easy", "medium"],
            "companies": ["infosys"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "pseudo_code", "coding"],
            "total_questions": 70,
            "duration_minutes": 100,
            "negative_marking": False,
        },
        interview_focus=["logical_reasoning", "communication", "basic_dsa"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="infytq_released_structure",
        confidence=0.85,
    )

    # ── Wipro ────────────────────────────────────────────────────────────
    o["wipro"] = _overlay(
        "wipro", "Wipro", role="sde",
        min_solved=40, min_medium=15, min_hard=3,
        min_skills={"dsa": 40, "aptitude": 50, "verbal": 40, "coding": 40},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Verbal"],
        interview_rounds=["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=3,
        match_weights={"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.10, "resume": 0.03, "projects": 0.02},
        pattern_relevance={
            "aptitude.quantitative": 0.85,
            "aptitude.verbal": 0.7,
            "aptitude.logical": 0.7,
            "dsa.arrays_hashing": 0.6,
            "dsa.strings": 0.55,
            "foundation.control_flow": 0.55,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding"],
            "difficulty": ["easy", "medium"],
            "companies": ["wipro"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding"],
            "total_questions": 60,
            "duration_minutes": 90,
            "negative_marking": False,
        },
        interview_focus=["communication", "aptitude_application", "basic_coding"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="wipro_nlth_released_structure",
        confidence=0.8,
    )

    # ── Accenture ────────────────────────────────────────────────────────
    o["accenture"] = _overlay(
        "accenture", "Accenture", role="sde",
        min_solved=80, min_medium=30, min_hard=8,
        min_skills={"dsa": 55, "aptitude": 55, "verbal": 60, "coding": 55},
        focus_topics=["Arrays", "Strings", "Pseudo-code Tracing", "Aptitude", "Communication", "Critical Thinking"],
        interview_rounds=["Cognitive Assessment", "Technical Assessment", "Coding Test", "Interview"],
        typical_timeline_weeks=5,
        match_weights={"aptitude": 0.25, "dsa": 0.20, "cs_fundamentals": 0.10, "coding": 0.15, "interview": 0.20, "resume": 0.05, "projects": 0.05},
        pattern_relevance={
            "aptitude.quantitative": 0.85,
            "aptitude.verbal": 0.8,
            "aptitude.logical": 0.75,
            "dsa.arrays_hashing": 0.65,
            "dsa.strings": 0.6,
            "foundation.control_flow": 0.6,
            "foundation.programming_basics": 0.55,
            "behavioral.communication": 0.7,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding", "cs_fundamentals"],
            "difficulty": ["easy", "medium"],
            "companies": ["accenture"],
        },
        mock_blueprint={
            "sections": ["cognitive_assessment", "technical_assessment", "coding_test", "communication_assessment"],
            "total_questions": 90,
            "duration_minutes": 150,
            "negative_marking": False,
        },
        interview_focus=["communication", "cognitive_skills", "pseudo_code_tracing", "team_collaboration"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="accenture_careers_released_structure",
        confidence=0.8,
    )

    # ── Cognizant ────────────────────────────────────────────────────────
    o["cognizant"] = _overlay(
        "cognizant", "Cognizant", role="sde",
        min_solved=60, min_medium=25, min_hard=5,
        min_skills={"dsa": 50, "aptitude": 60, "verbal": 55, "coding": 50},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Verbal", "Communication"],
        interview_rounds=["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.30, "dsa": 0.25, "cs_fundamentals": 0.10, "coding": 0.15, "interview": 0.15, "resume": 0.03, "projects": 0.02},
        pattern_relevance={
            "aptitude.quantitative": 0.85,
            "aptitude.verbal": 0.75,
            "aptitude.logical": 0.7,
            "dsa.arrays_hashing": 0.65,
            "dsa.strings": 0.55,
            "foundation.control_flow": 0.55,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding"],
            "difficulty": ["easy", "medium"],
            "companies": ["cognizant"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding"],
            "total_questions": 70,
            "duration_minutes": 100,
            "negative_marking": False,
        },
        interview_focus=["communication", "aptitude_application", "basic_coding"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="cognizant_genc_released_structure",
        confidence=0.8,
    )

    # ── Capgemini ────────────────────────────────────────────────────────
    o["capgemini"] = _overlay(
        "capgemini", "Capgemini", role="sde",
        min_solved=60, min_medium=25, min_hard=6,
        min_skills={"dsa": 50, "aptitude": 55, "verbal": 50, "coding": 55},
        focus_topics=["Arrays", "Pseudo-code Tracing", "Basic Algorithms", "Aptitude", "Communication"],
        interview_rounds=["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.25, "dsa": 0.20, "cs_fundamentals": 0.15, "coding": 0.20, "interview": 0.12, "resume": 0.03, "projects": 0.05},
        pattern_relevance={
            "aptitude.quantitative": 0.8,
            "aptitude.verbal": 0.7,
            "aptitude.logical": 0.65,
            "dsa.arrays_hashing": 0.6,
            "foundation.control_flow": 0.6,
            "foundation.programming_basics": 0.55,
            "behavioral.communication": 0.6,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding", "cs_fundamentals"],
            "difficulty": ["easy", "medium"],
            "companies": ["capgemini"],
        },
        mock_blueprint={
            "sections": ["pseudo_code", "quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding"],
            "total_questions": 75,
            "duration_minutes": 120,
            "negative_marking": False,
        },
        interview_focus=["pseudo_code_tracing", "communication", "coding_fundamentals"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="capgemini_released_structure",
        confidence=0.8,
    )

    # ── HCLTech ──────────────────────────────────────────────────────────
    o["hcltech"] = _overlay(
        "hcltech", "HCLTech", role="sde",
        min_solved=50, min_medium=20, min_hard=5,
        min_skills={"dsa": 45, "aptitude": 55, "verbal": 50, "coding": 45},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Verbal"],
        interview_rounds=["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "resume": 0.03, "projects": 0.05},
        pattern_relevance={
            "aptitude.quantitative": 0.85,
            "aptitude.verbal": 0.7,
            "aptitude.logical": 0.7,
            "dsa.arrays_hashing": 0.6,
            "dsa.strings": 0.55,
            "foundation.control_flow": 0.5,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding"],
            "difficulty": ["easy", "medium"],
            "companies": ["hcltech"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding"],
            "total_questions": 65,
            "duration_minutes": 100,
            "negative_marking": False,
        },
        interview_focus=["communication", "aptitude_application", "basic_coding"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="hcltech_released_structure",
        confidence=0.8,
    )

    # ── Tech Mahindra ────────────────────────────────────────────────────
    o["tech_mahindra"] = _overlay(
        "tech_mahindra", "Tech Mahindra", role="sde",
        min_solved=50, min_medium=20, min_hard=4,
        min_skills={"dsa": 45, "aptitude": 55, "verbal": 50, "coding": 45},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Networking Basics"],
        interview_rounds=["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "resume": 0.03, "projects": 0.05},
        pattern_relevance={
            "aptitude.quantitative": 0.85,
            "aptitude.verbal": 0.7,
            "aptitude.logical": 0.7,
            "dsa.arrays_hashing": 0.6,
            "dsa.strings": 0.55,
            "cs_fundamentals.networks": 0.5,
            "foundation.control_flow": 0.5,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding", "cs_fundamentals"],
            "difficulty": ["easy", "medium"],
            "companies": ["tech_mahindra"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding", "networking_basics"],
            "total_questions": 70,
            "duration_minutes": 110,
            "negative_marking": False,
        },
        interview_focus=["communication", "networking_basics", "aptitude_application"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="tech_mahindra_released_structure",
        confidence=0.75,
    )

    # ── LTIMindtree ──────────────────────────────────────────────────────
    o["ltimindtree"] = _overlay(
        "ltimindtree", "LTIMindtree", role="sde",
        min_solved=50, min_medium=20, min_hard=4,
        min_skills={"dsa": 45, "aptitude": 55, "verbal": 50, "coding": 45},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Verbal"],
        interview_rounds=["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.28, "dsa": 0.22, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.15, "resume": 0.03, "projects": 0.05},
        pattern_relevance={
            "aptitude.quantitative": 0.85,
            "aptitude.verbal": 0.7,
            "aptitude.logical": 0.7,
            "dsa.arrays_hashing": 0.6,
            "dsa.strings": 0.55,
            "foundation.control_flow": 0.5,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding"],
            "difficulty": ["easy", "medium"],
            "companies": ["ltimindtree"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding"],
            "total_questions": 65,
            "duration_minutes": 100,
            "negative_marking": False,
        },
        interview_focus=["communication", "aptitude_application", "basic_coding"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="ltimindtree_released_structure",
        confidence=0.75,
    )

    # ── Mphasis ──────────────────────────────────────────────────────────
    o["mphasis"] = _overlay(
        "mphasis", "Mphasis", role="sde",
        min_solved=40, min_medium=15, min_hard=3,
        min_skills={"dsa": 40, "aptitude": 50, "verbal": 45, "coding": 40},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Verbal"],
        interview_rounds=["Online Aptitude", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=3,
        match_weights={"aptitude": 0.28, "dsa": 0.20, "cs_fundamentals": 0.12, "coding": 0.15, "interview": 0.17, "resume": 0.03, "projects": 0.05},
        pattern_relevance={
            "aptitude.quantitative": 0.8,
            "aptitude.verbal": 0.65,
            "aptitude.logical": 0.65,
            "dsa.arrays_hashing": 0.55,
            "dsa.strings": 0.5,
            "foundation.control_flow": 0.45,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding"],
            "difficulty": ["easy", "medium"],
            "companies": ["mphasis"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding"],
            "total_questions": 55,
            "duration_minutes": 90,
            "negative_marking": False,
        },
        interview_focus=["communication", "aptitude_application", "basic_coding"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="mphasis_released_structure",
        confidence=0.7,
    )

    # ── Coforge ──────────────────────────────────────────────────────────
    o["coforge"] = _overlay(
        "coforge", "Coforge", role="sde",
        min_solved=50, min_medium=20, min_hard=4,
        min_skills={"dsa": 45, "aptitude": 55, "verbal": 50, "coding": 45},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Verbal", "SQL"],
        interview_rounds=["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.25, "dsa": 0.20, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.15, "resume": 0.05, "projects": 0.05},
        pattern_relevance={
            "aptitude.quantitative": 0.8,
            "aptitude.verbal": 0.7,
            "aptitude.logical": 0.65,
            "dsa.arrays_hashing": 0.6,
            "dsa.strings": 0.55,
            "cs_fundamentals.sql": 0.6,
            "foundation.control_flow": 0.5,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding", "cs_fundamentals"],
            "difficulty": ["easy", "medium"],
            "companies": ["coforge"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding", "sql_basics"],
            "total_questions": 65,
            "duration_minutes": 100,
            "negative_marking": False,
        },
        interview_focus=["sql_fundamentals", "communication", "aptitude_application"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="coforge_released_structure",
        confidence=0.75,
    )

    # ── Persistent ───────────────────────────────────────────────────────
    o["persistent"] = _overlay(
        "persistent", "Persistent", role="sde",
        min_solved=50, min_medium=20, min_hard=4,
        min_skills={"dsa": 45, "aptitude": 55, "verbal": 50, "coding": 45},
        focus_topics=["Arrays", "Strings", "Basic Algorithms", "Aptitude", "Verbal", "SQL"],
        interview_rounds=["Online Assessment", "Coding Test", "Technical Interview", "HR Round"],
        typical_timeline_weeks=4,
        match_weights={"aptitude": 0.25, "dsa": 0.20, "cs_fundamentals": 0.15, "coding": 0.15, "interview": 0.15, "resume": 0.05, "projects": 0.05},
        pattern_relevance={
            "aptitude.quantitative": 0.8,
            "aptitude.verbal": 0.7,
            "aptitude.logical": 0.65,
            "dsa.arrays_hashing": 0.6,
            "dsa.strings": 0.55,
            "cs_fundamentals.sql": 0.55,
            "foundation.control_flow": 0.5,
        },
        question_filters={
            "type": ["aptitude", "logical", "verbal", "coding", "cs_fundamentals"],
            "difficulty": ["easy", "medium"],
            "companies": ["persistent"],
        },
        mock_blueprint={
            "sections": ["quantitative_aptitude", "verbal_ability", "reasoning_ability", "coding", "sql_basics"],
            "total_questions": 65,
            "duration_minutes": 100,
            "negative_marking": False,
        },
        interview_focus=["sql_fundamentals", "communication", "aptitude_application"],
        version="2025-01",
        effective_from="2025-01-15",
        provenance="persistent_released_structure",
        confidence=0.75,
    )

    return o


def _ensure_overlays() -> Dict[str, CompanyOverlay]:
    global _COMPANY_OVERLAYS
    if not _COMPANY_OVERLAYS:
        _COMPANY_OVERLAYS = _build_overlays()
    return _COMPANY_OVERLAYS


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_company(company_id: str) -> Optional[CompanyOverlay]:
    """Return a company overlay by canonical company_id, or None."""
    return _ensure_overlays().get(company_id.lower().strip())


def get_all_companies() -> Dict[str, CompanyOverlay]:
    """Return all company overlays (read-only copy)."""
    return dict(_ensure_overlays())


def get_company_ids() -> List[str]:
    """Return all canonical company IDs."""
    return list(_ensure_overlays().keys())


def get_active_companies() -> Dict[str, CompanyOverlay]:
    """Return companies whose effective_from <= today and (effective_to is empty or >= today)."""
    from datetime import datetime
    now = datetime.now().date().isoformat()
    return {
        cid: co for cid, co in _ensure_overlays().items()
        if co.effective_from <= now and (not co.effective_to or co.effective_to >= now)
    }


def get_question_filters(company_id: str) -> Dict[str, Any]:
    """Return the question_filters dict for a company, or {}."""
    co = get_company(company_id)
    if not co:
        return {}
    return dict(co.question_filters)


def get_pattern_relevance(company_id: str) -> Dict[str, float]:
    """Return pattern relevance scores for a company, or {}."""
    co = get_company(company_id)
    if not co:
        return {}
    return dict(co.pattern_relevance)


def get_match_weights(company_id: str) -> Dict[str, float]:
    """Return readiness match weights for a company, falling back to generic weights."""
    co = get_company(company_id)
    if not co:
        return {}
    return dict(co.match_weights)


def get_mock_blueprint(company_id: str) -> Dict[str, Any]:
    """Return the mock OA blueprint for a company, or {}."""
    co = get_company(company_id)
    if not co:
        return {}
    return dict(co.mock_blueprint)


def get_interview_focus(company_id: str) -> List[str]:
    """Return interview focus areas for a company, or []."""
    co = get_company(company_id)
    if not co:
        return []
    return list(co.interview_focus)


def get_min_skills(company_id: str) -> Dict[str, float]:
    """Return minimum skill thresholds for a company, or {}."""
    co = get_company(company_id)
    if not co:
        return {}
    return dict(co.min_skills)


def to_readiness_profile(company_id: str) -> Optional[Dict[str, Any]]:
    """Convert a company overlay to the shape expected by readiness_engine (backward compat).

    Returns None if the company is not found.
    """
    co = get_company(company_id)
    if not co:
        return None
    return {
        "company": co.company_id,
        "assessment_variant": co.role,
        "version": co.version,
        "effective_date": co.effective_from,
        "min_solved": co.min_solved,
        "min_medium": co.min_medium,
        "min_hard": co.min_hard,
        "min_skills": co.min_skills,
        "focus_topics": co.focus_topics,
        "interview_rounds": co.interview_rounds,
        "typical_timeline_weeks": co.typical_timeline_weeks,
        "match_weights": co.match_weights,
    }


# ---------------------------------------------------------------------------
# Migration helpers
# ---------------------------------------------------------------------------

def migrate_readiness_company_profiles() -> Dict[str, Dict[str, Any]]:
    """Return a dict shaped like readiness_engine.COMPANY_PROFILES, built from overlays.

    This allows readiness_engine to read from company_overlays without breaking
    its existing interface. When all callers migrate to company_overlays directly,
    this helper can be removed.
    """
    result = {}
    for cid, co in _ensure_overlays().items():
        result[cid] = to_readiness_profile(cid) or {}
    return result
