"""Company OA Simulator — flagship Placement Simulation Engine component.

Implements the blueprint described in the A-grade BountyCode plan:

    MOCK OA  ──▶  SCORE ENGINE  ──▶  SKILL DIAGNOSTICS  ──▶  READINESS  ──▶  NEXT MISSIONS

Key design principles (from the research doc):
- Blueprint Engine: company/role/exam-style drives question-type distribution.
- Deterministic: question selection, scoring, time analysis, readiness all run WITHOUT AI.
- AI is OPTIONAL: only used for deeper coding explanation / nuanced feedback if available.
- Hidden test-case coding grading reuses the existing CodeExecutionEngine.
- Integrity Mode: opt-in browser signals recorded and surfaced (not "cheat detection").
- Time Intelligence: per-question timing produces actionable test-taking strategy advice.
"""
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from dataclasses import asdict
from bson import ObjectId
import logging

from app.middleware.auth import get_current_user
from app.database import oa_sessions_collection, integrity_events_collection, coding_challenges_collection, usage_collection, skill_graph_collection
from app.data.aptitude_question_bank import (
    get_questions_by_category,
    get_random_questions,
)
from app.data.behavioral_question_bank import get_random_question, get_questions_by_category
from app.config import get_settings

try:
    from app.data.company_blueprints import company_blueprints as _BLUEPRINT_DATA
except Exception:
    _BLUEPRINT_DATA = {"company_blueprints": {}}

from app.services.readiness_report import generate_readiness_pdf
from app.services.readiness_engine import compute_readiness

router = APIRouter(prefix="/api/v1/oa", tags=["oa"])
settings = get_settings()

# ---------------------------------------------------------------------------
# Blueprint Engine — company/role/exam-style → question-type distribution
# Each value is the weight (percentage) of questions of that type in the OA.
# ---------------------------------------------------------------------------
OA_BLUEPRINTS: Dict[str, Dict[str, float]] = {
    # Generic software engineer fresher OA
    "swe": {
        "coding": 0.25,
        "dsa": 0.15,
        "cs_fundamentals": 0.20,
        "aptitude": 0.25,
        "behavioral": 0.10,
        "situational": 0.05,
    },
    "amazon": {
        "coding": 0.40,
        "dsa": 0.30,
        "behavioral": 0.20,
        "aptitude": 0.10,
    },
    "google": {
        "coding": 0.30,
        "dsa": 0.45,
        "cs_fundamentals": 0.15,
        "behavioral": 0.10,
    },
    "microsoft": {
        "coding": 0.35,
        "dsa": 0.30,
        "cs_fundamentals": 0.20,
        "behavioral": 0.15,
    },
    "meta": {
        "coding": 0.35,
        "dsa": 0.35,
        "behavioral": 0.15,
        "cs_fundamentals": 0.15,
    },
    "tcs": {
        "aptitude": 0.40,
        "coding": 0.25,
        "cs_fundamentals": 0.20,
        "behavioral": 0.15,
    },
    # TCS NQT (National Qualifier Test) two-stage structure (Foundation + Advanced).
    # Weights mirror the real paper's section emphasis; the live per-question counts
    # vary by year, so this is labelled "pattern-relevant" (see TCS_NQT_STRUCTURE),
    # NOT a claim of exact verified counts.
    "tcs_nqt": {
        # Foundation
        "aptitude": 0.20,
        "logical": 0.20,
        "verbal": 0.20,
        # Advanced
        "cs_fundamentals": 0.15,
        "coding": 0.25,
    },
    "infosys": {
        "aptitude": 0.45,
        "coding": 0.25,
        "cs_fundamentals": 0.20,
        "behavioral": 0.10,
    },
    "wipro": {
        "aptitude": 0.40,
        "coding": 0.30,
        "cs_fundamentals": 0.20,
        "behavioral": 0.10,
    },
    # Infosys InfyTQ (3-hr online test). SOURCE: indian_companies.py
    # infosys.infytq_pattern (Aptitude&Logic 30q/30m, Programming MCQ 20q/20m,
    # Coding 3q/90m, SQL 5q/20m). SQL is OMITTED: the engine has no SQL judge,
    # so the blueprint distributes over servable sections only. Pattern-relevant.
    "infytq": {
        "aptitude": 0.30,
        "logical": 0.15,
        "cs_fundamentals": 0.25,
        "coding": 0.30,
    },
    # Wipro NLTH (96 min). SOURCE: indian_companies.py wipro.nlth_pattern
    # (Aptitude 20q/20m incl. quant+logical, Coding 2q/60m, English 20q/16m).
    # Pattern-relevant.
    "wipro_nlth": {
        "aptitude": 0.25,
        "logical": 0.15,
        "verbal": 0.30,
        "coding": 0.30,
    },
    # Accenture AMCAT-style assessment (90 min). SOURCE: indian_companies.py
    # accenture.amcat_pattern (Numerical 25q/20m, Logical 25q/25m, Verbal 25q/20m,
    # Coding 2q/25m). Pattern-relevant.
    "accenture": {
        "aptitude": 0.25,
        "logical": 0.25,
        "verbal": 0.25,
        "coding": 0.25,
    },
    # Cognizant GenC assessment (90 min). SOURCE: indian_companies.py
    # cognizant.genc_pattern (Aptitude 25q/25m mixed num/logical/verbal,
    # Programming 2q/45m, Essay 1q/20m). Essay writing is OMITTED: it cannot be
    # auto-graded to placement standard. Pattern-relevant.
    "cognizant": {
        "aptitude": 0.35,
        "logical": 0.15,
        "verbal": 0.15,
        "coding": 0.35,
    },
    # Capgemini online assessment (90 min). SOURCE: company_blueprints.json
    # capgemini structure (Aptitude quant+logical ~25q/25m, Verbal ~25q/25m,
    # Coding 2 problems/30m). Pattern-relevant.
    "capgemini": {
        "aptitude": 0.25,
        "logical": 0.15,
        "verbal": 0.25,
        "coding": 0.35,
    },
    # IBM entry-level Cognitive Ability + coding (75 min). SOURCE:
    # company_blueprints.json ibm structure (~50q/30m cognitive, 2 problems/45m).
    # Pattern-relevant.
    "ibm": {
        "aptitude": 0.20,
        "logical": 0.20,
        "verbal": 0.10,
        "coding": 0.50,
    },
    "general": {
        "coding": 0.25,
        "dsa": 0.15,
        "cs_fundamentals": 0.20,
        "aptitude": 0.25,
        "behavioral": 0.10,
        "situational": 0.05,
    },
}

# Section metadata: human labels + default time budget (minutes) per question.
# `stage` groups sections into exam stages (e.g. TCS NQT Foundation / Advanced)
# so the client can render two-stage structure without a separate engine.
SECTION_META = {
    "coding": {"label": "Coding", "minutes": 25, "kind": "code", "stage": "advanced"},
    "dsa": {"label": "DSA", "minutes": 12, "kind": "mcq", "stage": "advanced"},
    "cs_fundamentals": {"label": "Programming Logic", "minutes": 8, "kind": "mcq", "stage": "advanced"},
    "aptitude": {"label": "Numerical Ability", "minutes": 5, "kind": "mcq", "stage": "foundation"},
    "logical": {"label": "Reasoning Ability", "minutes": 5, "kind": "mcq", "stage": "foundation"},
    "verbal": {"label": "Verbal Ability", "minutes": 5, "kind": "mcq", "stage": "foundation"},
    "behavioral": {"label": "Behavioral", "minutes": 10, "kind": "text", "stage": "foundation"},
    "situational": {"label": "Situational", "minutes": 6, "kind": "mcq", "stage": "foundation"},
}

# Aptitude bank sub-categories used to fill non-verified sections.
# logical/verbal use the dedicated verified bank and are intentionally omitted
# here (they are never backfilled from legacy content).
APT_BANK_MAP = {
    "dsa": "technical",
    "cs_fundamentals": "technical",
    "aptitude": "quantitative",
    "situational": "logical",
}

BEHAVIORAL_CATS = ["leadership", "teamwork", "growth", "conflict", "situational", "problem_solving", "amazon_leadership"]

# TCS NQT — 190-minute Foundation + Advanced exam structure.
# SOURCE: publicly reported TCS NQT format (application/assessment guidance). The
# precise per-section question counts change between hiring cycles, so we expose
# the structure as "pattern-relevant" rather than claiming exact verified counts.
# `minutes` reflect the real aggregate pacing across the two stages (Foundation
# aptitude/reasoning/verbal + Advanced programming-logic & 2 coding problems).
TCS_NQT_STRUCTURE = {
    "title": "TCS NQT — Foundation + Advanced",
    "duration_minutes": 190,
    "stages": [
        {
            "id": "foundation",
            "title": "Foundation",
            "sections": ["aptitude", "logical", "verbal"],
            "note": "Numerical Ability, Reasoning Ability, Verbal Ability",
        },
        {
            "id": "advanced",
            "title": "Advanced",
            "sections": ["cs_fundamentals", "coding"],
            "note": "Programming Logic (MCQ) + 2 coding problems",
        },
    ],
    "provenance": "pattern-relevant",  # adapted from public TCS NQT format, not exact verifiable counts
}

# Infosys InfyTQ — 180-minute online test structure.
# SOURCE: indian_companies.py infosys.infytq_pattern. SQL section omitted
# (no SQL judge in the engine); weights cover servable sections only.
INFYTQ_STRUCTURE = {
    "title": "Infosys InfyTQ — Online Test",
    "duration_minutes": 180,
    "stages": [
        {
            "id": "aptitude_logic",
            "title": "Aptitude & Logic",
            "sections": ["aptitude", "logical"],
            "note": "Quantitative, Logical, Data Interpretation (~30 questions, 30 min)",
        },
        {
            "id": "programming",
            "title": "Programming MCQ + Coding",
            "sections": ["cs_fundamentals", "coding"],
            "note": "Programming concepts MCQ (~20) + 3 coding problems (~110 min)",
        },
    ],
    "provenance": "pattern-relevant",  # from in-repo InfyTQ pattern, not exact verifiable counts
}

# Wipro NLTH — 96-minute online test structure.
# SOURCE: indian_companies.py wipro.nlth_pattern.
WIPRO_NLTH_STRUCTURE = {
    "title": "Wipro NLTH — Online Test",
    "duration_minutes": 96,
    "stages": [
        {
            "id": "aptitude",
            "title": "Aptitude",
            "sections": ["aptitude", "logical"],
            "note": "Quantitative + Logical (~20 questions, 20 min)",
        },
        {
            "id": "english",
            "title": "English",
            "sections": ["verbal"],
            "note": "Grammar, Vocabulary, Sentence Completion (~20 questions, 16 min)",
        },
        {
            "id": "coding",
            "title": "Coding",
            "sections": ["coding"],
            "note": "2 coding problems (60 min)",
        },
    ],
    "provenance": "pattern-relevant",  # from in-repo NLTH pattern, not exact verifiable counts
}

# Accenture AMCAT-style assessment — 90-minute structure.
# SOURCE: indian_companies.py accenture.amcat_pattern.
ACCENTURE_STRUCTURE = {
    "title": "Accenture — Online Assessment",
    "duration_minutes": 90,
    "stages": [
        {
            "id": "cognitive",
            "title": "Cognitive",
            "sections": ["aptitude", "logical", "verbal"],
            "note": "Numerical 25q/20m + Logical 25q/25m + Verbal 25q/20m",
        },
        {
            "id": "coding",
            "title": "Coding",
            "sections": ["coding"],
            "note": "2 coding problems (25 min)",
        },
    ],
    "provenance": "pattern-relevant",  # from in-repo AMCAT pattern, not exact verifiable counts
}

# Cognizant GenC assessment — 90-minute structure.
# SOURCE: indian_companies.py cognizant.genc_pattern. Essay writing omitted
# (not auto-gradable to placement standard).
COGNIZANT_STRUCTURE = {
    "title": "Cognizant GenC — Online Assessment",
    "duration_minutes": 90,
    "stages": [
        {
            "id": "aptitude",
            "title": "Aptitude",
            "sections": ["aptitude", "logical", "verbal"],
            "note": "Numerical + Logical + Verbal (~25 questions, 25 min)",
        },
        {
            "id": "programming",
            "title": "Programming",
            "sections": ["coding"],
            "note": "2 coding problems (45 min)",
        },
    ],
    "provenance": "pattern-relevant",  # from in-repo GenC pattern, not exact verifiable counts
}

# Map blueprint section names to OA engine section names.
_SECTION_NAME_MAP = {
    "quantitative_aptitude": "aptitude",
    "verbal_ability": "verbal",
    "reasoning_ability": "logical",
    "advanced_aptitude": "aptitude",
    "advanced_coding": "coding",
    "numerical_ability": "aptitude",
    "logical_reasoning": "logical",
    "coding": "coding",
    "aptitude_logic": "aptitude",
    "programming_mcq": "cs_fundamentals",
    "computer_basics": "cs_fundamentals",
    "technical": "cs_fundamentals",
    "problem_solving": "aptitude",
    "communication": "behavioral",
    "english": "verbal",
}


def _load_blueprint_structures() -> dict:
    """Load exam structures from company_blueprints.json and convert to the
    _EXAM_STRUCTURE_FOR format. Falls back to hardcoded structures on error."""
    loaded = {}
    try:
        for key, bp in _BLUEPRINT_DATA.get("company_blueprints", {}).items():
            structure = bp.get("structure", {})
            stages = []
            for stage_key, stage_label in [("foundation", "Foundation"), ("advanced", "Advanced")]:
                stage = structure.get(stage_key)
                if not stage:
                    continue
                raw_sections = stage.get("sections", [])
                mapped = [_SECTION_NAME_MAP.get(s, s) for s in raw_sections]
                total_q = stage.get("questions", 0)
                topics = stage.get("topics", {})
                counts = []
                for s in mapped:
                    topic_key = next((k for k, v in topics.items() if _SECTION_NAME_MAP.get(k, k) == s), None)
                    if topic_key:
                        info = topics[topic_key]
                        n = info.get("questions", info.get("problems", 0))
                    else:
                        n = 0
                    counts.append(f"{s}: {n}q")
                note = f"{stage_label} — {total_q} questions. " + ", ".join(counts)
                stages.append({
                    "id": stage_key,
                    "title": stage_label,
                    "sections": mapped,
                    "note": note,
                })
            if stages:
                loaded[key] = {
                    "title": bp.get("name", key),
                    "duration_minutes": bp.get("duration_minutes", 90),
                    "stages": stages,
                    "provenance": bp.get("provenance_status", "pattern-relevant"),
                }
                # Also register aliases
                for alias in bp.get("companies", []):
                    loaded[alias] = loaded[key]
    except Exception:
        pass
    return loaded


# Extend hardcoded structures with blueprint-loaded ones (blueprints win on conflict).
_EXAM_STRUCTURE_FOR = {
    "tcs": TCS_NQT_STRUCTURE,
    "tcs_nqt": TCS_NQT_STRUCTURE,
    "infosys": INFYTQ_STRUCTURE,
    "infytq": INFYTQ_STRUCTURE,
    "wipro": WIPRO_NLTH_STRUCTURE,
    "wipro_nlth": WIPRO_NLTH_STRUCTURE,
    "nlth": WIPRO_NLTH_STRUCTURE,
    "accenture": ACCENTURE_STRUCTURE,
    "amcat": ACCENTURE_STRUCTURE,
    "cognizant": COGNIZANT_STRUCTURE,
    "genc": COGNIZANT_STRUCTURE,
}
_EXAM_STRUCTURE_FOR.update(_load_blueprint_structures())


def _blueprint_section_durations(company: str, role: str) -> Dict[str, int]:
    """Return per-section total time budgets (seconds) from company_blueprints.json.
    Empty dict if no blueprint or no duration data."""
    try:
        bp = _BLUEPRINT_DATA.get("company_blueprints", {}).get(company.lower())
        if not bp:
            # Try aliases (e.g. "tcs" -> "tcs_nqt")
            for key, candidate in _BLUEPRINT_DATA.get("company_blueprints", {}).items():
                if company.lower() in [c.lower() for c in candidate.get("companies", [])]:
                    bp = candidate
                    break
        if not bp:
            return {}
        structure = bp.get("structure", {})
        durations = {}
        for stage_key in ("foundation", "advanced"):
            stage = structure.get(stage_key, {})
            topics = stage.get("topics", {})
            for section_key, info in topics.items():
                oa_section = _SECTION_NAME_MAP.get(section_key, section_key)
                if "duration_minutes" in info:
                    durations[oa_section] = info["duration_minutes"] * 60
        return durations
    except Exception:
        return {}


def _blueprint_exact_distribution(company: str, role: str) -> Optional[Dict[str, int]]:
    """Return exact section question counts from company_blueprints.json when available.
    Returns None if the blueprint has no exact counts."""
    try:
        bp = _BLUEPRINT_DATA.get("company_blueprints", {}).get(company.lower())
        if not bp:
            # Try aliases (e.g. "tcs" -> "tcs_nqt")
            for key, candidate in _BLUEPRINT_DATA.get("company_blueprints", {}).items():
                if company.lower() in [c.lower() for c in candidate.get("companies", [])]:
                    bp = candidate
                    break
        if not bp:
            return None
        structure = bp.get("structure", {})
        dist = {}
        for stage_key in ("foundation", "advanced"):
            stage = structure.get(stage_key, {})
            topics = stage.get("topics", {})
            for section_key, info in topics.items():
                oa_section = _SECTION_NAME_MAP.get(section_key, section_key)
                if oa_section in dist:
                    continue
                if "questions" in info:
                    dist[oa_section] = info["questions"]
                elif "problems" in info:
                    dist[oa_section] = info["problems"]
        return dist if dist else None
    except Exception:
        return None

# Marking schemes per company exam (raw-mark units). Every scheme carries
# mandatory provenance. Unknown/not-stated => "none": penalties are NEVER
# invented. Under "none", scoring is bit-identical to the legacy 100/0 mean.
MARKING_SCHEMES = {
    "tcs_nqt": {"correct": 1, "wrong": 0, "skip": 0,
                "provenance": "pattern-relevant: NQT publicly reports no negative marking in most cycles"},
    "infytq": {"correct": 1, "wrong": 0, "skip": 0,
               "provenance": "pattern-relevant: no verified penalty schedule published"},
    "wipro_nlth": {"correct": 1, "wrong": 0, "skip": 0,
                   "provenance": "pattern-relevant: no verified penalty schedule published"},
    "accenture": {"correct": 1, "wrong": 0, "skip": 0,
                  "provenance": "pattern-relevant: no verified penalty schedule published"},
    "cognizant": {"correct": 1, "wrong": 0, "skip": 0,
                  "provenance": "pattern-relevant: no verified penalty schedule published"},
    "capgemini": {"correct": 1, "wrong": 0, "skip": 0,
                  "provenance": "pattern-relevant: no verified penalty schedule published"},
    "ibm": {"correct": 1, "wrong": 0, "skip": 0,
            "provenance": "pattern-relevant: no verified penalty schedule published"},
    "default": {"correct": 1, "wrong": 0, "skip": 0,
                "provenance": "default: no penalty assumed"},
}


def _marking_for(company: str) -> dict:
    """Resolve the marking scheme for a company exam key (canonical aliases
    included). Always returns a scheme; never invents penalties."""
    key = (company or "").lower().strip()
    from app.services.question_store import canonical_company_key
    canon = canonical_company_key(key)
    exam_key = {
        "tcs": "tcs_nqt", "tcs_nqt": "tcs_nqt",
        "infosys": "infytq", "infytq": "infytq",
        "wipro": "wipro_nlth", "wipro_nlth": "wipro_nlth", "nlth": "wipro_nlth",
        "accenture": "accenture", "amcat": "accenture",
        "cognizant": "cognizant", "genc": "cognizant",
        "capgemini": "capgemini", "capgemini_amcat": "capgemini",
        "ibm": "ibm", "ibm_kv": "ibm", "ibm_cv": "ibm",
    }.get(canon, canon)
    scheme = dict(MARKING_SCHEMES.get(exam_key, MARKING_SCHEMES["default"]))
    scheme["exam_key"] = exam_key
    return scheme

OA_FREE_LIMIT = 1  # mirrors FREE_TIER_COMPANY_MOCK_LIMIT


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------
class StartOARequest(BaseModel):
    company: str = Field("general", description="Company blueprint key (amazon/google/tcs/...)")
    role: str = Field("swe", description="Target role key (swe/...); currently drives blueprint selection")
    total_questions: int = Field(20, ge=5, le=40, description="Total number of questions")
    duration_minutes: int = Field(90, ge=10, le=200, description="Total OA duration in minutes (e.g. 190 for TCS NQT Foundation+Advanced)")
    mode: str = Field("calm", description="calm | pressure | boss")
    integrity: bool = Field(False, description="Enable opt-in integrity signal tracking")
    verified_only: bool = Field(True, description="Serve ONLY independently verified content (trusted packs). Default True (A2 trust gate 2026-09-10): sections lacking enough verified questions are skipped, and an OA with no servable sections returns 422 instead of legacy content. Set False ONLY to explicitly opt into the legacy/unverified mix.")


class SubmitOAItem(BaseModel):
    question_uid: str = Field(..., description="Unique question id within the session")
    answer: Any = Field(..., description="MCQ option index/string, code string, or text response")
    language: Optional[str] = Field(None, description="Language for coding answers")
    time_taken: int = Field(0, ge=0, description="Seconds spent on this question")
    test_cases: Optional[List[dict]] = Field(None, description="Client-run test case results for coding (optional)")


class SubmitOABatch(BaseModel):
    session_id: str
    items: List[SubmitOAItem] = Field(default_factory=list)


class IntegritySignal(BaseModel):
    session_id: str
    event: str = Field(..., description="tab_hidden|fullscreen_exit|copy_paste|blur|focus")
    at: float = Field(..., description="Client timestamp (epoch seconds)")
    detail: Optional[str] = ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _resolve_blueprint(company: str, role: str) -> Dict[str, float]:
    key = (company or "general").lower().strip()
    # Canonical company OAs use the real exam structures (pattern-relevant).
    # Legacy generic keys ("tcs", "infosys", "wipro") resolve to the same.
    _CANONICAL_ALIAS = {
        "tcs": "tcs_nqt",
        "infosys": "infytq",
        "wipro": "wipro_nlth",
        "nlth": "wipro_nlth",
        "amcat": "accenture",
        "genc": "cognizant",
    }
    if key in _CANONICAL_ALIAS:
        key = _CANONICAL_ALIAS[key]
    if key in OA_BLUEPRINTS:
        return OA_BLUEPRINTS[key]
    if role and role.lower() in OA_BLUEPRINTS:
        return OA_BLUEPRINTS[role.lower()]
    return OA_BLUEPRINTS["general"]


def _distribute(total: int, blueprint: Dict[str, float]) -> Dict[str, int]:
    """Distribute total questions across sections by blueprint weight (largest remainder)."""
    raw = {sec: blueprint[sec] * total for sec in blueprint}
    floor = {sec: int(v) for sec, v in raw.items()}
    assigned = sum(floor.values())
    remainder = sorted(blueprint.keys(), key=lambda s: raw[s] - floor[s], reverse=True)
    i = 0
    while assigned < total:
        floor[remainder[i % len(remainder)]] += 1
        assigned += 1
        i += 1
    # drop zero-count sections
    return {sec: n for sec, n in floor.items() if n > 0}


# Map OA sections to verified question-store types (Content Trust).
# Behavioral/situational are intentionally ABSENT: no independently verified
# content exists for them, so they are never served as "trusted".
_VERIFIED_TYPE_FOR_SECTION = {
    "aptitude": "aptitude",
    "cs_fundamentals": "cs_fundamentals",
    "logical": "logical",
    "verbal": "verbal",
    "coding": "coding",
    "dsa": "coding",
}


def _verified_questions_for(section: str, count: int, company: str = None) -> list:
    """Pull `count` exclusively verified questions for a section from the
    canonical verified bank. Returns [] if none/none enough. Never returns
    legacy content. When `company` is given, company-tagged verified items
    come first, backfilled with general verified stock to reach `count`
    (every item served is still TRUSTED and carries its own provenance)."""
    qtype = _VERIFIED_TYPE_FOR_SECTION.get(section)
    if not qtype:
        return []
    try:
        from app.services import question_store as qs
    except Exception:
        return []
    try:
        picked: list = []
        seen = set()
        if company:
            bank = qs.company_verified_bank(company)
            for q in bank["items"]:
                if q.get("type") == qtype and q.get("id") not in seen:
                    picked.append(dict(q))
                    seen.add(q.get("id"))
                if len(picked) >= count:
                    break
        if len(picked) < count:
            rows = qs.find({"type": qtype}).only_verified().to_list(count * 2)
            for q in rows:
                if q.get("id") not in seen:
                    picked.append(dict(q))
                    seen.add(q.get("id"))
                if len(picked) >= count:
                    break
        return picked[:count]
    except Exception:
        return []


def _to_oa_mcq(q: dict, section: str, meta: dict, idx: int) -> dict:
    """Convert a verified MCQ (aptitude/logical/verbal/cs_fundamentals) into
    an OA question dict. Keeps the independent reasoning trail on the server
    copy for the scorecard, strips answer keys from the client payload below."""
    options = q.get("options") or q.get("multiple_choice_options") or []
    correct = q.get("correct_index")
    if correct is None:
        correct = q.get("correct_answer")
    return {
        "question_uid": f"{section}-{idx}",
        "section": section,
        "section_label": meta["label"],
        "kind": "mcq",
        "question": q.get("question", ""),
        "options": options,
        "time_limit": meta["minutes"] * 60,
        "difficulty": q.get("difficulty", "medium"),
        "topic": q.get("topic", ""),
        "sub_topic": q.get("sub_topic", ""),
        "_correct_index": correct,
        "_explanation": q.get("reasoning_steps") or q.get("explanation", ""),
        "_shortcut": q.get("shortcut", ""),
        "_common_trap": q.get("common_trap", ""),
        "trust_status": q.get("trust_status", "unverified"),
        "source_bank": q.get("source_bank", ""),
        "verification_version": q.get("verification_version"),
        "question_id": q.get("id", ""),
        "stage": meta.get("stage", ""),
        "verified_by_takers": q.get("verified_by_takers"),
    }


def _to_oa_code(q: dict, section: str, meta: dict, idx: int) -> dict:
    """Convert a verified coding question into an OA code question. Uses the
    verified testcases + hidden testcases and exposes starter code built from
    the verified signature."""
    tc = q.get("testcases") or []
    hidden = q.get("hidden_testcases") or []
    code = (q.get("solution") or {}).get("code") or ""
    def _ser(t):
        """Serialize {'input': [...], 'expected': ...} for the execution engine."""
        inp = t.get("input", [])
        if isinstance(inp, (list, tuple)) and len(inp) == 1 and isinstance(inp[0], (list, dict)):
            inp = inp[0]
        return {"input": inp, "expected": t.get("expected")}
    starter_py = _starter_from(code)
    return {
        "question_uid": f"{section}-{idx}",
        "section": section,
        "section_label": meta["label"],
        "kind": "code",
        "question": q.get("question") or q.get("title", ""),
        "description": q.get("question", ""),
        "starter_code": {"python": starter_py},
        "language": "python",
        "test_cases": [_ser(t) for t in (tc + hidden)],
        "time_limit": meta["minutes"] * 60,
        "difficulty": q.get("difficulty", "medium"),
        "topic": q.get("topic", "arrays"),
        "function_name": _fn_name_from_code(starter_py),
        "trust_status": q.get("trust_status", "unverified"),
        "source_bank": q.get("source_bank", ""),
        "verification_version": q.get("verification_version"),
        "question_id": q.get("id", ""),
        "stage": meta.get("stage", ""),
        "verified_by_takers": q.get("verified_by_takers"),
    }


def _starter_from(code: str) -> str:
    """Strip the candidate solution body into a 'pass' skeleton for the
    student, so we never leak the answer in the starter code."""
    if not code:
        return "def solve():\n    pass"
    lines = [l for l in code.splitlines() if l.strip()]
    if not lines:
        return "def solve():\n    pass"
    header = lines[0].rstrip(":")
    return header + ":\n    # your implementation here\n    pass"


def _fn_name_from_code(code: str) -> str:
    """First top-level `def` name in a code string (the gradeable entry
    point). Empty when none — caller keeps legacy stdin-mode behavior."""
    import re as _re
    if not code:
        return ""
    m = _re.search(r"^\s*def\s+([A-Za-z_]\w*)\s*\(", code, _re.MULTILINE)
    return m.group(1) if m else ""


async def _build_questions(dist: Dict[str, int], verified_only: bool = True, company: str = None, section_durations: Dict[str, int] = None) -> List[dict]:
    section_durations = section_durations or {}
    out: List[dict] = []
    for sec, count in dist.items():
        meta = SECTION_META.get(sec, {"label": sec, "minutes": 8, "kind": "mcq"})
        total_section_seconds = section_durations.get(sec)
        if total_section_seconds is not None:
            per_q = max(30, int(total_section_seconds / max(count, 1)))
        else:
            per_q = meta["minutes"] * 60
        if meta["kind"] == "mcq":
            if verified_only:
                v = _verified_questions_for(sec, count, company=company)
                if len(v) < count:
                    continue
                for idx, q in enumerate(v[:count]):
                    out.append(_to_oa_mcq(q, sec, meta, idx))
                continue
            cat = APT_BANK_MAP.get(sec, "quantitative")
            qs = get_random_questions(cat, count)
            if not qs:
                qs = get_questions_by_category(cat)[:count]
            for idx, q in enumerate(qs[:count]):
                out.append({
                    "question_uid": f"{sec}-{idx}",
                    "section": sec,
                    "section_label": meta["label"],
                    "kind": "mcq",
                    "question": q.get("question", ""),
                    "options": q.get("options", []),
                    "time_limit": per_q,
                    "difficulty": q.get("difficulty", "medium"),
                    "topic": q.get("topic", ""),
                    "_correct_index": q.get("correct_index", q.get("correct_answer", 0)),
                    "_explanation": q.get("explanation", ""),
                    "stage": meta.get("stage", ""),
                })
        elif meta["kind"] == "code":
            if verified_only:
                v = _verified_questions_for(sec, count, company=company)
                if len(v) < count:
                    continue
                for idx, q in enumerate(v[:count]):
                    out.append(_to_oa_code(q, sec, meta, idx))
                continue
            items = []
            try:
                cursor = coding_challenges_collection.find({}).limit(count)
                async for d in cursor:
                    items.append(d)
            except Exception:
                items = []
            for idx in range(count):
                if idx < len(items):
                     c = items[idx]
                     out.append({
                         "question_uid": f"{sec}-{idx}",
                         "section": sec,
                         "section_label": meta["label"],
                         "kind": "code",
                         "question": c.get("title", c.get("question", "Solve the coding problem")),
                         "description": c.get("description", c.get("prompt", "")),
                         "starter_code": c.get("starter_code", {}),
                         "language": c.get("language", "python"),
                         "test_cases": c.get("test_cases", []),
                         "time_limit": per_q,
                         "difficulty": c.get("difficulty", "medium"),
                         "topic": c.get("topic", "arrays"),
                         "stage": meta.get("stage", ""),
                     })
                else:
                    out.append({
                        "question_uid": f"{sec}-{idx}",
                        "section": sec,
                        "section_label": meta["label"],
                        "kind": "code",
                        "question": "Two Sum: return indices of two numbers that add up to target.",
                        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                        "starter_code": {"python": "def two_sum(nums, target):\n    # your code here\n    pass"},
                        "language": "python",
                        "test_cases": [
                            {"input": "[2,7,11,15] 9", "expected": "[0,1]"},
                            {"input": "[3,2,4] 6", "expected": "[1,2]", "is_hidden": True},
                        ],
                        "time_limit": per_q,
                        "difficulty": "easy",
                        "topic": "arrays",
                        "stage": meta.get("stage", ""),
                    })
        else:
            if verified_only:
                continue
            for idx in range(count):
                q = get_random_question(BEHAVIORAL_CATS[idx % len(BEHAVIORAL_CATS)])
                if not q:
                    q = {}
                star = q.get("star_framework", {})
                if hasattr(star, "__dataclass_fields__"):
                    star = asdict(star)
                out.append({
                    "question_uid": f"{sec}-{idx}",
                    "section": sec,
                    "section_label": meta["label"],
                    "kind": "text",
                    "question": q.get("title", q.get("question", "Describe a challenge you overcame.")),
                    "star_framework": star,
                    "tips": q.get("tips", []),
                    "time_limit": per_q,
                    "difficulty": q.get("difficulty", "medium"),
                    "topic": q.get("category", sec),
                })
    return out


def _correct_position(qdef: dict) -> int:
    """Resolve a verified MCQ's answer key to a stable option index.

    The verified bank uses dict-style options ("A"/"B"/"C"/"D") with
    ``correct_index='A'`` for aptitude/logical/verbal and list-style options
    (cs_fundamentals) with an integer ``correct_index``. This maps both to the
    position a student must pick — clients submit the option index, so this
    must match or every letter-answered question misgrades.
    """
    options = qdef.get("options") or qdef.get("multiple_choice_options") or []
    correct = qdef.get("_correct_index", qdef.get("correct_index", 0))
    if isinstance(correct, int):
        return correct
    if isinstance(correct, str):
        if correct.strip().isdigit():
            return int(correct)
        keys = list(options.keys()) if isinstance(options, dict) else []
        if correct in keys:
            return keys.index(correct)
    ca = qdef.get("correct_answer")
    if ca is not None:
        if isinstance(options, dict):
            match = next(
                (k for k, v in options.items()
                 if str(v).strip().lower() == str(ca).strip().lower()),
                None,
            )
            if match is None:
                match = ca if ca in options else None
            if match is not None:
                return list(options.keys()).index(match)
        if isinstance(options, list):
            tokens = [str(o).strip().lower() for o in options]
            if str(ca).strip().lower() in tokens:
                return tokens.index(str(ca).strip().lower())
    return 0


def _user_position(raw, qdef: dict) -> int:
    """Resolve a student's MCQ answer to an option index (accepts index or letter)."""
    if isinstance(raw, int) and not isinstance(raw, bool):
        return raw
    options = qdef.get("options") or qdef.get("multiple_choice_options") or []
    text = str(raw).strip().lower()
    if isinstance(options, dict):
        keys = list(options.keys())
        if text in {str(k).strip().lower() for k in keys}:
            return keys.index(next(k for k in keys if str(k).strip().lower() == text))
        vals = [str(v).strip().lower() for v in options.values()]
        if text in vals:
            return vals.index(text)
    elif isinstance(options, list):
        vals = [str(o).strip().lower() for o in options]
        if text in vals:
            return vals.index(text)
    try:
        return int(text)
    except (ValueError, TypeError):
        return -2


def _score_mcq(item: SubmitOAItem, qdef: dict, scheme: dict = None) -> float:
    """Grade one MCQ in raw marks under the exam's marking scheme.
    Unanswered (None/""/-1 sentinel) earns `skip` marks — an unanswered
    question is not a wrong answer. Under the default scheme this is
    bit-identical to the legacy 100/0 scoring after normalization."""
    scheme = scheme or MARKING_SCHEMES["default"]
    correct = _correct_position(qdef)
    raw = item.answer
    if raw is None or raw == "" or raw == -1:
        return float(scheme["skip"])
    return float(scheme["correct"]) if _user_position(raw, qdef) == correct else float(scheme["wrong"])


async def _run_diagnosis_and_repair(user_id: str, sess: dict, section_avg: dict, scorecard: list) -> dict:
    """Feed the verified OA scorecard into the EXISTING diagnosis + repair
    loop (study_engine.diagnose_mock_oa + repair_service.create_repair_mission).
    Hardened to produce skill-level evidence (topic/sub_topic), time-tier,
    and concrete retest via verified questions. Best-effort."""
    try:
        from app.services.study_engine import diagnose_mock_oa
        from app.services.repair_service import create_repair_mission
    except Exception:
        return {}

    sections: Dict[str, dict] = {}
    skill_stats: Dict[str, dict] = {}
    for pq in scorecard:
        sec = pq.get("section", "other")
        correct = 1 if pq.get("score", 0) >= 100 else 0
        s = sections.setdefault(sec, {"correct": 0, "total": 0})
        s["correct"] += correct
        s["total"] += 1
        # skill key = topic or topic/sub_topic
        skill = pq.get("topic") or sec
        sub = pq.get("sub_topic") or ""
        key = f"{skill}/{sub}" if sub else skill
        ss = skill_stats.setdefault(key, {"correct": 0, "total": 0, "times": [], "slow": 0})
        ss["correct"] += correct
        ss["total"] += 1
        ss["times"].append(int(pq.get("time_taken", 0)))

    responses = {
        "score": sum(pq.get("score", 0) >= 100 for pq in scorecard),
        "total_questions": len(scorecard),
        "sections": sections,
        "time_per_question": [int(pq.get("time_taken", 0)) for pq in scorecard],
    }
    try:
        diagnosis = await diagnose_mock_oa(user_id, responses)
    except Exception:
        diagnosis = {}

    # Skill-level weaknesses: <70% and at least 2 questions or single hard fail
    avg_time = sum(int(pq.get("time_taken", 0)) for pq in scorecard) / max(len(scorecard), 1)
    skill_weaknesses = []
    for skill, st in skill_stats.items():
        pct = (st["correct"] / st["total"] * 100) if st["total"] else 0
        slow = sum(1 for t in st["times"] if t > avg_time * 1.5) if avg_time else 0
        if pct < 70:
            skill_weaknesses.append({
                "skill": skill,
                "correct": st["correct"],
                "total": st["total"],
                "pct": round(pct, 1),
                "avg_time_s": round(sum(st["times"])/len(st["times"]), 1) if st["times"] else 0,
                "slow_count": slow,
            })
    skill_weaknesses.sort(key=lambda x: x["pct"])
    # enrich diagnosis with skill evidence
    if skill_weaknesses:
        diagnosis["skill_weaknesses"] = skill_weaknesses
        diagnosis["primary_weakness"] = skill_weaknesses[0]["skill"]
        # concrete repair chain
        primary = skill_weaknesses[0]
        diagnosis["repair_chain"] = [
            f"Concept lesson: {primary['skill']}",
            f"Guided problem: {primary['skill']}",
            f"3 verified practice: {primary['skill']}",
            "SRS review",
        ]
        diagnosis["retest_condition"] = ">=80% across 3 verified questions on primary weakness"

    missions = []
    # Prefer skill weaknesses over section weaknesses for repair
    weakness_keys = [w["skill"] for w in skill_weaknesses[:2]] if skill_weaknesses else diagnosis.get("weaknesses", [])[:3]
    for weakness in weakness_keys[:3]:
        try:
            mission = await create_repair_mission(user_id, [weakness], source="mock_oa")
            # Attach verified retest question ids for this skill
            retest_ids = []
            try:
                from app.services import question_store as qs
                # best-effort: pull 3 verified for this skill topic
                topic = weakness.split("/")[0]
                rows = qs.find({"topic": topic}).only_verified().to_list(3)
                retest_ids = [r.get("id") for r in rows]
            except Exception:
                pass
            missions.append({
                "skill": weakness,
                "mission_title": mission.title,
                "recommended_lessons": mission.recommended_lessons,
                "recommended_exercises": mission.recommended_exercises,
                "recommended_quizzes": mission.recommended_quizzes,
                "retest_verified_ids": retest_ids,
            })
        except Exception:
            continue

    return {
        "diagnosis": diagnosis,
        "repair_missions": missions,
    }



def _score_text(item: SubmitOAItem, qdef: dict) -> float:
    """Deterministic STAR rubric (no AI): presence of Situation/Task/Action/Result markers."""
    text = (item.answer or "").strip()
    if not text:
        return 0.0
    low = text.lower()
    markers = ["situation", "task", "action", "result", "impact", "outcome", "learned", "team", "i "]
    hits = sum(1 for m in markers if m in low)
    length_score = min(1.0, len(text) / 400.0)
    return round(min(100.0, (hits / len(markers)) * 70 + length_score * 30), 1)


async def _score_code(item: SubmitOAItem, qdef: dict, function_name: str = ""):
    """Grade coding via existing CodeExecutionEngine (hidden test cases) when available."""
    from app.services.code_executor import CodeExecutionEngine
    engine = CodeExecutionEngine()
    tcs = item.test_cases or qdef.get("test_cases", [])
    if not tcs:
        return 0.0, {"note": "no test cases"}
    try:
        result = await engine.execute_against_test_cases(
            source_code=item.answer,
            language=item.language or qdef.get("language", "python"),
            test_cases=tcs,
            function_name=function_name or qdef.get("function_name", "") or "",
        )
    except Exception as e:
        return 0.0, {"error": str(e)}
    if not result.get("success"):
        return 0.0, result
    cases = result.get("results", [])
    if not cases:
        passed = result.get("passed", 0)
        total = result.get("total", len(tcs))
        return round(100.0 * passed / max(total, 1), 1), result
    passed = sum(1 for c in cases if c.get("passed"))
    return round(100.0 * passed / max(len(cases), 1), 1), result


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@router.get("/blueprints")
async def list_blueprints():
    """Return available company/role OA blueprints."""
    return {
        "blueprints": {
            k: {"distribution": v, "sections": list(v.keys())}
            for k, v in OA_BLUEPRINTS.items()
        }
    }


@router.get("/templates")
async def list_oa_templates():
    """Return company OA templates with last_verified_at freshness dates."""
    try:
        import json, os
        path = os.path.join(os.path.dirname(__file__), "..", "data", "company_blueprints.json")
        with open(path, "r", encoding="utf-8") as f:
            doc = json.load(f)
        templates = []
        for key, bp in doc.get("company_blueprints", {}).items():
            templates.append({
                "id": key,
                "name": bp.get("name", key),
                "full_name": bp.get("full_name", key),
                "duration_minutes": bp.get("duration_minutes", 90),
                "role": bp.get("role", "SDE"),
                "hiring_tracks": bp.get("hiring_tracks", []),
                "ctc_range": bp.get("ctc_range", {}),
                "structure": bp.get("structure", {}),
                "exam_rules": bp.get("exam_rules", {}),
                "provenance_status": bp.get("provenance_status", "pattern-relevant"),
                "last_verified_at": bp.get("last_verified_at"),
            })
        return {"templates": templates}
    except Exception:
        return {"templates": []}


def _load_trusted_packs() -> list:
    """Load the 10 trusted pack definitions (data artifact, not an engine)."""
    import json, os
    path = os.path.join(os.path.dirname(__file__), "..", "data", "trusted_packs.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            doc = json.load(f)
        return doc.get("packs", [])
    except Exception:
        return []


def _verified_stock() -> dict:
    """Return count of verified questions per type, from the canonical store."""
    stock = {}
    try:
        from app.services import question_store as qs
        if not qs._questions:
            qs.load_all()
        for q in qs._questions:
            if q.get("trust_status") == "verified":
                t = q.get("type", "other")
                stock[t] = stock.get(t, 0) + 1
    except Exception:
        pass
    return stock


@router.get("/trusted-packs")
async def list_trusted_packs():
    """Read-only list of the 10 trusted placement packs. Each pack runs on the
    shared independently-verified pool (verified_only=true). Section demand is
    validated against live verified stock: sections with insufficient verified
    questions are reported so clients can warn rather than silently backfill
    with unverified legacy content."""
    packs = _load_trusted_packs()
    stock = _verified_stock()
    mapped = {"aptitude": "aptitude", "logical": "logical", "verbal": "verbal",
              "cs_fundamentals": "cs_fundamentals", "coding": "coding", "dsa": "coding"}
    result = []
    for p in packs:
        availability = {}
        all_met = True
        unmet = []
        for sec, need in p.get("sections", {}).items():
            have = stock.get(mapped.get(sec, sec), 0)
            ok = have >= need
            availability[sec] = {"needed": need, "verified_available": have, "satisfied": ok}
            if not ok:
                all_met = False
                unmet.append(sec)
        result.append({
            "id": p.get("id"),
            "company": p.get("company"),
            "stage": p.get("stage"),
            "role": p.get("role"),
            "difficulty": p.get("difficulty"),
            "duration_minutes": p.get("duration_minutes"),
            "total_questions": p.get("total_questions"),
            "provenance": p.get("provenance"),
            "sections": p.get("sections"),
            "availability": availability,
            "fully_verified": all_met,
            "unmet_sections": unmet,
        })
    total_verified = sum(stock.values())
    return {"trusted_packs": result, "verified_total": total_verified, "verified_universe": stock}


@router.post("/{company}/start")
async def start_oa(company: str, req: StartOARequest, user=Depends(get_current_user)):
    """Start a company OA simulation. Returns the full question set + timer config."""
    if user.get("plan") == "free":
        # count this month's OA attempts
        start_month = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        used = await oa_sessions_collection.count_documents({
            "user_id": user["id"], "created_at": {"$gte": start_month}
        })
        if used >= OA_FREE_LIMIT:
            raise HTTPException(
                status_code=403,
                detail=f"Free tier OA limit reached ({OA_FREE_LIMIT}). Upgrade to Pro for unlimited company OAs.",
            )

    blueprint = _resolve_blueprint(company, req.role)
    exact_dist = _blueprint_exact_distribution(company, req.role)
    section_durations = _blueprint_section_durations(company, req.role)
    if exact_dist:
        exact_total = sum(exact_dist.values())
        if exact_total > 0 and req.total_questions < exact_total:
            scale = req.total_questions / exact_total
            scaled = {}
            remainder = []
            for sec, count in exact_dist.items():
                scaled[sec] = max(1, int(count * scale)) if count > 0 else 0
                remainder.append((count * scale - scaled[sec], sec))
            remainder.sort(reverse=True)
            i = 0
            while sum(scaled.values()) < req.total_questions:
                _, sec = remainder[i % len(remainder)]
                scaled[sec] += 1
                i += 1
            dist = {sec: n for sec, n in scaled.items() if n > 0}
        else:
            dist = exact_dist
    else:
        dist = _distribute(req.total_questions, blueprint)
    questions = await _build_questions(dist, verified_only=req.verified_only, company=company, section_durations=section_durations)

    if req.verified_only and not questions:
        raise HTTPException(
            status_code=422,
            detail=(
                "No independently verified questions available for this blueprint's "
                "sections. Verified-only assessments require sufficient verified "
                "stock in every demanded section."
            ),
        )

    # Per-question timing budget + pressure-mode penalties. Answer keys
    # (`_correct_index`, `_explanation`) must REMAIN on the stored session doc
    # because _score_mcq reads `_correct_index` at completion; the client-safe
    # payload below strips every `_`-prefixed key.
    pressure = req.mode == "pressure"
    for q in questions:
        if pressure:
            q["time_limit"] = int(q["time_limit"] * 0.7)

    now = datetime.now(timezone.utc)
    # Build section-level structure from question list
    section_groups: Dict[str, List[dict]] = {}
    for q in questions:
        sec = q.get("section", "other")
        section_groups.setdefault(sec, []).append(q)
    sections = []
    for sec, qs in section_groups.items():
        meta = SECTION_META.get(sec, {"label": sec, "minutes": 8})
        section_time_limit = sum(int(q.get("time_limit", meta["minutes"] * 60)) for q in qs)
        sections.append({
            "id": sec,
            "title": meta.get("label", sec),
            "type": sec,
            "question_ids": [q["question_uid"] for q in qs],
            "time_limit_s": section_time_limit,
            "started_at": now.isoformat() if sec == list(section_groups.keys())[0] else None,
            "submitted_at": None,
            "answers": [],
        })
    session_doc = {
        "user_id": user["id"],
        "company": company.lower(),
        "role": req.role,
        "blueprint": blueprint,
        "mode": req.mode,
        "integrity_enabled": req.integrity,
        "verified_only": req.verified_only,
        "questions": questions,
        "sections": sections,
        "status": "in_progress",
        "answers": {},
        "integrity_signals": [],
        "tab_switch_count": 0,
        "fullscreen_exits": 0,
        "started_at": now,
        "duration_minutes": req.duration_minutes,
        "ends_at": now + timedelta(minutes=req.duration_minutes),
        "created_at": now,
        "score_breakdown": {},
    }
    res = await oa_sessions_collection.insert_one(session_doc)
    session_id = str(res.inserted_id)
    # Mirror the public session_id onto the document so lookups by
    # session_id (rather than Mongo _id) work consistently.
    await oa_sessions_collection.update_one(
        {"_id": res.inserted_id},
        {"$set": {"session_id": session_id}},
    )

    # Build client-safe payload (no answer keys exposed)
    safe_questions = []
    for q in questions:
        safe = {k: v for k, v in q.items() if not k.startswith("_")}
        safe_questions.append(safe)

    scheme = _marking_for(company)
    struct = _EXAM_STRUCTURE_FOR.get(company.lower())
    stage_budgets = None
    if struct:
        per_stage = {}
        for q in questions:
            per_stage[q.get("stage", "")] = per_stage.get(q.get("stage", ""), 0) + int(q.get("time_limit", 0) or 0)
        stage_budgets = [
            {"id": s["id"], "title": s["title"],
             "budget_minutes": round(per_stage.get(s["id"], 0) / 60.0, 1)}
            for s in struct.get("stages", [])
        ]

    # Lookup blueprint for exam rules (with alias fallback)
    _bp = None
    for _key, _candidate in _BLUEPRINT_DATA.get("company_blueprints", {}).items():
        if company.lower() == _key.lower() or company.lower() in [c.lower() for c in _candidate.get("companies", [])]:
            _bp = _candidate
            break
    _exam_rules = _bp.get("exam_rules", {}) if _bp else {}

    return {
        "session_id": session_id,
        "company": company.lower(),
        "mode": req.mode,
        "blueprint": blueprint,
        "marking_scheme": scheme,
        "stage_budgets": stage_budgets,
        "exam_structure": (
            _EXAM_STRUCTURE_FOR.get(company.lower())
            or _EXAM_STRUCTURE_FOR.get(req.role.lower())
        ),
        "duration_minutes": req.duration_minutes,
        "ends_at": session_doc["ends_at"].isoformat(),
        "integrity_enabled": req.integrity,
        "total_questions": len(safe_questions),
        "questions": safe_questions,
        "negative_marking": _exam_rules.get("negative_marking"),
        "back_navigation": _exam_rules.get("back_navigation"),
        "section_switching": _exam_rules.get("section_switching"),
    }

    # Beta funnel: track first OA start
    try:
        from app.services.analytics_service import track_event
        asyncio.create_task(track_event(
            event="beta_oa_start",
            path=f"/api/v1/oa/{company}/start",
            user_id=user["id"],
            meta={"company": company, "role": req.role, "total_questions": len(safe_questions)},
        ))
    except Exception:
        pass


@router.post("/answer")
async def submit_oa_answer(req: SubmitOABatch, user=Depends(get_current_user)):
    """Submit one or more OA answers. Records answers + timing for scoring at completion."""
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(req.session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess:
        raise HTTPException(status_code=404, detail="OA session not found")
    if sess["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if sess.get("status") == "completed":
        raise HTTPException(status_code=400, detail="OA already completed")

    # Late-submit guard: past ends_at the window is closed. Mark expired and
    # refuse (410); the client should call complete to score answered items.
    ends_at = sess.get("ends_at")
    if ends_at:
        try:
            end = ends_at if isinstance(ends_at, datetime) else datetime.fromisoformat(str(ends_at))
            if end.tzinfo is None:
                end = end.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > end:
                await oa_sessions_collection.update_one(
                    {"_id": ObjectId(req.session_id)},
                    {"$set": {"status": "expired"}},
                )
                raise HTTPException(
                    status_code=410,
                    detail="Time window expired. Complete the assessment to score answered questions.",
                )
        except HTTPException:
            raise
        except Exception:
            pass

    # Index question defs by uid
    qdefs = {q["question_uid"]: q for q in sess["questions"]}
    stored = dict(sess.get("answers", {}))
    for item in req.items:
        qdef = qdefs.get(item.question_uid)
        if not qdef:
            continue
        stored[item.question_uid] = {
            "answer": item.answer,
            "language": item.language,
            "time_taken": item.time_taken,
            "test_cases": item.test_cases,
            "section": qdef["section"],
            "kind": qdef["kind"],
            "difficulty": qdef.get("difficulty", "medium"),
            "topic": qdef.get("topic", ""),
        }
    await oa_sessions_collection.update_one(
        {"_id": ObjectId(req.session_id)},
        {"$set": {"answers": stored, "updated_at": datetime.now(timezone.utc)}},
    )
    return {"received": len(req.items), "session_id": req.session_id}


@router.post("/integrity")
async def record_integrity_signal(req: IntegritySignal, user=Depends(get_current_user)):
    """Opt-in integrity signal recording (tab visibility, fullscreen, copy/paste, blur)."""
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(req.session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess or sess["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="Session not found")
    if not sess.get("integrity_enabled"):
        return {"recorded": False, "note": "integrity mode not enabled for this session"}
    signal = {
        "event": req.event,
        "at": req.at,
        "detail": req.detail,
        "user_id": user["id"],
        "session_id": req.session_id,
        "created_at": datetime.now(timezone.utc),
    }
    await integrity_events_collection.insert_one(signal)
    await oa_sessions_collection.update_one(
        {"_id": ObjectId(req.session_id)},
        {"$push": {"integrity_signals": signal}},
    )
    # Increment counters for tab switches and fullscreen exits
    if req.event in ("tab_hidden", "blur"):
        await oa_sessions_collection.update_one(
            {"_id": ObjectId(req.session_id)},
            {"$inc": {"tab_switch_count": 1}},
        )
    elif req.event in ("fullscreen_exit",):
        await oa_sessions_collection.update_one(
            {"_id": ObjectId(req.session_id)},
            {"$inc": {"fullscreen_exits": 1}},
        )
    return {"recorded": True}


@router.post("/{session_id}/complete")
async def complete_oa(session_id: str, user=Depends(get_current_user)):
    """Grade the OA, produce the scorecard, update readiness, and surface next missions."""
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess:
        raise HTTPException(status_code=404, detail="OA session not found")
    if sess["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    qdefs = {q["question_uid"]: q for q in sess["questions"]}
    answers = sess.get("answers", {})
    marking = _marking_for(sess.get("company", ""))

    section_scores: Dict[str, List[float]] = {}
    section_times: Dict[str, List[int]] = {}
    topic_times: Dict[str, List[int]] = {}
    per_question = []
    raw_marks = 0.0
    max_marks = 0.0

    for uid, ans in answers.items():
        qdef = qdefs.get(uid, {})
        kind = ans.get("kind", "mcq")
        if kind == "mcq":
            marks = _score_mcq(
                SubmitOAItem(question_uid=uid, answer=ans.get("answer", -1)), qdef,
                marking,
            )
            max_m = float(marking["correct"])
            score = marks / max_m * 100.0 if max_m else 0.0
        elif kind == "text":
            score = _score_text(
                SubmitOAItem(question_uid=uid, answer=ans.get("answer", "")), qdef
            )
            marks, max_m = score, 100.0
        else:  # code
            fname = qdef.get("function_name", "") or ""
            if not fname:
                # Sessions built before function_name was populated: infer
                # from the starter signature when the submission defines it.
                import re as _re2
                starter = (qdef.get("starter_code") or {}).get("python", "")
                cand = _fn_name_from_code(starter)
                if cand and _re2.search(
                        rf"^\s*def\s+{cand}\s*\(", ans.get("answer") or "", _re2.MULTILINE):
                    fname = cand
            score, _ = await _score_code(
                SubmitOAItem(
                    question_uid=uid,
                    answer=ans.get("answer", ""),
                    language=ans.get("language"),
                    test_cases=ans.get("test_cases"),
                ),
                qdef,
                function_name=fname,
            )
            marks, max_m = score, 100.0
        sec = ans.get("section", "other")
        section_scores.setdefault(sec, []).append(score)
        raw_marks += marks
        max_marks += max_m
        t = int(ans.get("time_taken", 0))
        section_times.setdefault(sec, []).append(t)
        topic_times.setdefault(ans.get("topic", "misc"), []).append(t)
        per_question.append({
            "question_uid": uid,
            "section": sec,
            "section_label": qdef.get("section_label", sec),
            "score": score,
            "marks_awarded": marks,
            "max_marks": max_m,
            "time_taken": t,
            "difficulty": ans.get("difficulty", "medium"),
            "topic": ans.get("topic", ""),
        })

    # Section averages (clamped to [0, 100] so penalizing schemes can't poison
    # downstream readiness/diagnosis; raw marks stay truthful on the scorecard)
    section_avg = {}
    for sec, scores in section_scores.items():
        section_avg[sec] = round(max(0.0, min(100.0, sum(scores) / len(scores))) if scores else 0.0, 1)

    # Overall = blueprint-weighted average
    blueprint = sess.get("blueprint", {})
    if blueprint:
        overall = sum(section_avg.get(s, 0) * w for s, w in blueprint.items())
    else:
        overall = round(sum(section_avg.values()) / max(len(section_avg), 1), 1)
    overall = round(min(100.0, max(0.0, overall)), 1)

    # Time Intelligence
    time_intel = _build_time_intelligence(section_times, topic_times, sess.get("duration_minutes", 90))

    # Strong / weak areas
    strong = sorted(section_avg.items(), key=lambda x: x[1], reverse=True)[:2]
    weak = sorted(section_avg.items(), key=lambda x: x[1])[:3]

    # Verdict
    if overall >= 75:
        verdict = "INTERVIEW READY"
    elif overall >= 55:
        verdict = "NEEDS PREPARATION"
    else:
        verdict = "NOT READY"

    # Integrity summary
    signals = sess.get("integrity_signals", [])
    integrity_summary = {}
    for s in signals:
        integrity_summary[s.get("event", "unknown")] = integrity_summary.get(s.get("event", "unknown"), 0) + 1

    result = {
        "session_id": session_id,
        "company": sess.get("company"),
        "mode": sess.get("mode"),
        "overall_readiness": overall,
        "verdict": verdict,
        "readiness_message": (
            f"You are {overall}% ready for "
            f"{(_EXAM_STRUCTURE_FOR.get((sess.get('company') or '').lower(), {}).get('title') or (sess.get('company') or '').title())}"
        ),
        "marking_scheme": marking,
        "raw_marks": round(raw_marks, 2),
        "max_marks": round(max_marks, 2),
        "section_scores": {SECTION_META.get(s, {}).get("label", s): v for s, v in section_avg.items()},
        "section_scores_raw": section_avg,
        "score_breakdown": {
            s: {
                "avg": round(v, 1),
                "correct": sum(1 for pq in per_question if pq.get("section") == s and pq.get("score", 0) >= 100),
                "total": sum(1 for pq in per_question if pq.get("section") == s),
            }
            for s, v in section_avg.items()
        },
        "strong_areas": [SECTION_META.get(s, {}).get("label", s) for s, _ in strong],
        "weak_areas": [SECTION_META.get(s, {}).get("label", s) for s, _ in weak],
        "time_intelligence": time_intel,
        "questions_answered": len(per_question),
        "total_questions": len(sess["questions"]),
        "integrity_signals": integrity_summary,
        "tab_switch_count": sess.get("tab_switch_count", 0),
        "fullscreen_exits": sess.get("fullscreen_exits", 0),
        "scorecard": per_question,
        "next_missions": _next_missions(weak, topic_times),
    }

    await oa_sessions_collection.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"status": "completed", "result": result, "completed_at": datetime.now(timezone.utc)}},
    )

    # Feed readiness (best-effort, non-blocking)
    try:
        section_trust = _section_trust_ratios(sess.get("questions") or [])
        await _update_readiness(user["id"], sess.get("company"), overall, section_avg, section_trust=section_trust)
    except Exception:
        pass

    # Diagnosis -> persisted repair missions (existing loop, best-effort)
    try:
        diagnosis = await _run_diagnosis_and_repair(user["id"], sess, section_avg, per_question)
        if diagnosis:
            result["diagnosis"] = diagnosis.get("diagnosis", {})
            result["repair_missions"] = diagnosis.get("repair_missions", [])
            await oa_sessions_collection.update_one(
                {"_id": ObjectId(session_id)},
                {"$set": {"result": result, "diagnosis": result.get("diagnosis"), "repair_missions": result.get("repair_missions") or []}},
            )
    except Exception:
        pass

    # â”€â”€ Emit canonical LearningEvents for every section + the overall OA â”€â”€
    # Each section produces one event with diagnosis codes derived from
    # accuracy + time performance.  This feeds the unified outcome report.
    try:
        from app.services.study_engine import emit_learning_event
        from app.services.diagnosis import diagnose_oa_section_failure
        from app.services.skill_taxonomy import canonical_skill_id, parse_oa_section

        assessment_id = str(session_id)
        for sec, avg_score in section_avg.items():
            skill = parse_oa_section(sec)
            sec_scores = section_scores.get(sec, [])
            total = len(sec_scores)
            correct = sum(1 for s in sec_scores if s >= 100)
            sec_times = section_times.get(sec, [])
            codes = diagnose_oa_section_failure(
                sec, avg_score, total, correct,
                time_per_question=sec_times,
                question_stats=[
                    {
                        "correct": pq.get("score", 0) >= 100,
                        "difficulty": pq.get("difficulty", "medium"),
                    }
                    for pq in per_question if pq.get("section") == sec
                ],
            )
            await emit_learning_event(user["id"], {
                "activity_type": "oa_complete",
                "source": "oa",
                "skill_id": skill,
                "assessment_id": assessment_id,
                "company": sess.get("company"),
                "role": sess.get("role"),
                "passed": avg_score >= 70,
                "score": avg_score,
                "time_spent_seconds": int(sum(sec_times)),
                "mastery_before": None,
                "mastery_after": avg_score,
                "diagnosis_codes": codes,
                "metadata": {
                    "section": sec,
                    "section_label": SECTION_META.get(sec, {}).get("label", sec),
                    "overall_readiness": overall,
                },
            })

        # Overall OA completion event
        await emit_learning_event(user["id"], {
            "activity_type": "mock_oa",
            "source": "oa",
            "skill_id": canonical_skill_id(sess.get("mode")) or "oa.overall",
            "assessment_id": assessment_id,
            "company": sess.get("company"),
            "role": sess.get("role"),
            "passed": overall >= 70,
            "score": overall,
            "time_spent_seconds": int(sess.get("duration_minutes", 90) * 60),
            "mastery_before": None,
            "mastery_after": overall,
            "diagnosis_codes": [],
            "metadata": {
                "mode": sess.get("mode"),
                "blueprint_company": sess.get("company"),
                "section_count": len(section_avg),
                "weak_sections": [s for s, v in section_avg.items() if v < 70],
            },
        })
    except Exception as exc:
        logger.warning("OA LearningEvent emission failed: %s", exc)

    # Beta funnel: track OA completion
    try:
        from app.services.analytics_service import track_event
        asyncio.create_task(track_event(
            event="beta_oa_complete",
            path=f"/api/v1/oa/{sess.get('company')}/complete",
            user_id=user["id"],
            meta={
                "company": sess.get("company"),
                "overall": overall,
                "verdict": verdict,
                "questions_answered": len(per_question),
                "total_questions": len(sess["questions"]),
            },
        ))
    except Exception:
        pass

    return result


@router.get("/{session_id}/result")
async def get_oa_result(session_id: str, user=Depends(get_current_user)):
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess:
        raise HTTPException(status_code=404, detail="OA session not found")
    if sess["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if sess.get("status") != "completed":
        raise HTTPException(status_code=400, detail="OA not completed yet")
    return sess.get("result", {})


@router.get("/{session_id}/readiness-report")
async def download_readiness_report(session_id: str, user=Depends(get_current_user)):
    try:
        sess = await oa_sessions_collection.find_one({"_id": ObjectId(session_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid session ID")
    if not sess:
        raise HTTPException(status_code=404, detail="OA session not found")
    if sess["user_id"] != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    if sess.get("status") != "completed":
        raise HTTPException(status_code=400, detail="OA not completed yet")

    company = sess.get("company")
    try:
        readiness = await compute_readiness(user["id"], company=company)
    except Exception:
        readiness = sess.get("result") or {}

    user_name = user.get("name") or user.get("email") or "Candidate"
    user_email = user.get("email") or ""
    try:
        pdf_bytes = await generate_readiness_pdf(user_name, user_email, readiness, company=company)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {exc}")

    filename = f"readiness-report-{company or 'general'}-{session_id}.pdf"
    return StreamingResponse(
        iter([pdf_bytes]),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/history")
async def get_oa_history(user=Depends(get_current_user)):
    cursor = oa_sessions_collection.find(
        {"user_id": user["id"]},
        {"questions": 0, "answers": 0, "integrity_signals": 0},
    ).sort("created_at", -1).limit(20)
    out = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        out.append(doc)
    return {"sessions": out}


# ---------------------------------------------------------------------------
# Time Intelligence + Next Missions
# ---------------------------------------------------------------------------
def _build_time_intelligence(section_times: Dict[str, List[int]], topic_times: Dict[str, List[int]], total_min: int):
    intel = {"by_section": {}, "advice": []}
    for sec, times in section_times.items():
        avg = round(sum(times) / max(len(times), 1) / 60.0, 1)
        intel["by_section"][SECTION_META.get(sec, {}).get("label", sec)] = {
            "avg_minutes": avg,
            "total_minutes": round(sum(times) / 60.0, 1),
            "questions": len(times),
        }
    # Topic-level slow spots
    topic_avgs = {t: sum(v) / max(len(v), 1) for t, v in topic_times.items()}
    if topic_avgs:
        fast = min(topic_avgs, key=lambda k: topic_avgs[k])
        slow = max(topic_avgs, key=lambda k: topic_avgs[k])
        if topic_avgs[slow] > 0 and topic_avgs[slow] >= 1.8 * max(topic_avgs[fast], 1):
            intel["advice"].append(
                f"You spend {round(topic_avgs[slow] / max(topic_avgs[fast], 1), 1)}x longer "
                f"on {slow} problems. Consider abandoning after ~12 min if stuck."
            )
    intel["advice"].append(
        "Allocate time by section weight; autosave is on — don't re-edit submitted answers."
    )
    return intel


def _section_to_route(section: str, topic: str = "") -> str:
    section_routes = {
        "aptitude": "/aptitude",
        "logical": "/question-bank",
        "verbal": "/question-bank",
        "coding": "/coding",
        "cs_fundamentals": "/question-bank",
        "dsa": "/question-bank",
        "behavioral": "/question-bank",
        "situational": "/question-bank",
    }
    base = section_routes.get(section, "/question-bank")
    if base == "/question-bank" and topic:
        return f"/question-bank?topic={topic}"
    return base


def _trusted_count(topic: str = "", qtype: str = "") -> int:
    try:
        from app.services import question_store
        query: Dict[str, Any] = {}
        if topic:
            query["topic"] = topic
        if qtype:
            query["type"] = qtype
        return len(question_store.find(query).only_verified().limit(50).to_list())
    except Exception:
        return 0


def _next_missions(weak: List[tuple], topic_times: Dict[str, List[int]]):
    missions = []
    for sec, _ in weak:
        label = SECTION_META.get(sec, {}).get("label", sec)
        route = _section_to_route(sec, sec)
        if _trusted_count(qtype=sec) >= 10:
            missions.append({
                "title": f"Practice {label} (target 75%+)",
                "to": route,
                "action": "practice",
            })
    if topic_times:
        slow = max(topic_times, key=lambda k: sum(topic_times[k]) / max(len(topic_times[k]), 1))
        if _trusted_count(topic=slow) >= 10:
            missions.append({
                "title": f"Drill {slow} timed sets — you lose the most time here",
                "to": f"/question-bank?topic={slow}",
                "action": "drill",
            })
    if not missions:
        missions.append({
            "title": "Take another OA to validate consistency",
            "to": "/mock-oa",
            "action": "retest",
        })
    return missions[:4]


def _section_trust_ratios(questions: List[dict]) -> Dict[str, float]:
    ratios: Dict[str, float] = {}
    groups: Dict[str, list] = {}
    for q in questions:
        sec = str(q.get("section", "other"))
        groups.setdefault(sec, []).append(q)
    for sec, qs in groups.items():
        if not qs:
            continue
        trusted = 0
        for q in qs:
            status = str(q.get("trust_status", "")).lower()
            if status in ("verified", "reviewed", "automated_checked"):
                trusted += 1
        ratios[sec] = trusted / len(qs)
    return ratios


async def _update_readiness(user_id: str, company: str, overall: float, section_avg: Dict[str, float], section_trust: Optional[Dict[str, float]] = None):
    """Best-effort: store OA outcomes as a readiness signal for the existing readiness engine."""
    col = skill_graph_collection()
    doc = await col.find_one({"user_id": user_id})
    if not doc:
        doc = {"user_id": user_id, "categories": {}, "oa_outcomes": []}
    outcomes = doc.get("oa_outcomes", [])
    outcomes.append({
        "company": company,
        "overall": overall,
        "sections": section_avg,
        "section_trust": section_trust or {},
        "at": datetime.now(timezone.utc).isoformat(),
    })
    # Keep last 20
    outcomes = outcomes[-20:]
    cats = doc.get("categories", {})
    for sec, score in section_avg.items():
        key = sec
        prev = cats.get(key, {})
        prev_score = prev.get("score", 0)
        trust = (section_trust or {}).get(sec, 1.0)
        weighted = score * trust
        new_score = round(prev_score * 0.6 + weighted * 0.4, 1)
        cats[key] = {"score": new_score, "source": "oa", "trust": trust}
    await col.update_one(
        {"user_id": user_id},
        {"$set": {"categories": cats, "oa_outcomes": outcomes}},
        upsert=True,
    )
