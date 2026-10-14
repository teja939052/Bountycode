"""Service-based company tracks — the mission journey per company.

Overlays already exist in company_overlays.py (funnels, weights, filters);
COMPANY_JOURNEYS covers tcs/amazon/meta/google only. This module adds the
service-based mission tracks the placement funnel actually needs, reusing
those models — no new system, just the missing journey data.

Each track stage lists mission_ids (authored missions, validated by
mission_definitions.validate_mission) AND a bank_filter fallback so the
journey engine serves verified bank questions directly until every mission
is authored. Stages without authored missions are honest about it: the
filter is the path, not a placeholder mission.

Provenance: pattern weights come from the company overlay; any sentence of
the form "asked at X" requires bank refs with verified provenance +
companies tags, else the mission is labeled pattern-relevant.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TrackStage(BaseModel):
    order: int
    title: str
    description: str = ""
    mission_ids: List[str] = Field(default_factory=list)
    bank_filter: Dict[str, Any] = Field(default_factory=dict)
    passing_score: float = 70.0


class ServiceTrack(BaseModel):
    track_id: str  # e.g. "tcs_nqt"
    company_overlay_id: str  # e.g. "tcs"
    role_id: str = "sde"
    display_name: str = ""
    weeks: int = 10
    stages: List[TrackStage] = Field(default_factory=list)


def _aptitude_filter(company: str) -> Dict[str, Any]:
    return {"type": ["aptitude", "logical", "verbal"], "companies": [company]}


def _coding_filter(company: str) -> Dict[str, Any]:
    return {"type": ["coding"], "difficulty": ["easy", "medium"], "companies": [company]}


SERVICE_TRACKS: Dict[str, ServiceTrack] = {}


def _track(track_id: str, company: str, display: str, stages: List[TrackStage],
           weeks: int = 10) -> ServiceTrack:
    t = ServiceTrack(track_id=track_id, company_overlay_id=company,
                     display_name=display, weeks=weeks, stages=stages)
    SERVICE_TRACKS[track_id] = t
    return t


_track("tcs_nqt", "tcs", "TCS NQT", [
    TrackStage(order=1, title="Diagnostic",
               description="Baseline per topic; assigns starting levels.",
               bank_filter=_aptitude_filter("tcs"), passing_score=0),
    TrackStage(order=2, title="Aptitude Gauntlet",
               description="Quant, reasoning, verbal under time.",
               mission_ids=["tcs_nqt.percentages_change", "tcs_nqt.ratio_proportion",
                            "tcs_nqt.averages", "tcs_nqt.profit_loss",
                            "tcs_nqt.time_work", "tcs_nqt.blood_relations",
                            "tcs_nqt.directions", "tcs_nqt.coding_decoding",
                            "tcs_nqt.number_series", "tcs_nqt.sentence_correction",
                            "tcs_nqt.reading_comprehension"],
               bank_filter=_aptitude_filter("tcs")),
    TrackStage(order=3, title="Coding Foundations",
               description="Output prediction, pseudo-code, easy programs.",
               mission_ids=["tcs_nqt.variables_basics", "tcs_nqt.conditions",
                            "tcs_nqt.loops_basics", "tcs_nqt.strings_basics",
                            "tcs_nqt.arrays_basics"],
               bank_filter=_coding_filter("tcs")),
    TrackStage(order=4, title="CS Core Flash",
               description="OOPs, DBMS/SQL, OS/CN interview answers.",
               bank_filter={"type": ["coding"], "topic": ["oops", "dbms", "sql"],
                            "companies": ["tcs"]}),
    TrackStage(order=5, title="NQT Mock",
               description="Full-length simulation on the NQT pattern.",
               bank_filter={"companies": ["tcs"]}, passing_score=70),
])

_track("infosys_sp", "infosys", "Infosys SP", [
    TrackStage(order=1, title="Diagnostic", description="Baseline per topic.",
               bank_filter=_aptitude_filter("infosys"), passing_score=0),
    TrackStage(order=2, title="Aptitude + Reasoning",
               description="Quant with a reasoning emphasis; pseudo-code next.",
               bank_filter=_aptitude_filter("infosys")),
    TrackStage(order=3, title="Pseudo-code + Coding",
               description="Output prediction first, then easy programs.",
               bank_filter=_coding_filter("infosys")),
    TrackStage(order=4, title="Technical Interview",
               description="OOPs, DBMS, project explanation.",
               bank_filter={"companies": ["infosys"]}),
    TrackStage(order=5, title="InfyTQ Mock",
               description="Full-length simulation on the InfyTQ pattern.",
               bank_filter={"companies": ["infosys"]}, passing_score=70),
])

_track("wipro_nlth", "wipro", "Wipro NLTH", [
    TrackStage(order=1, title="Diagnostic", description="Baseline per topic.",
               bank_filter=_aptitude_filter("wipro"), passing_score=0),
    TrackStage(order=2, title="Aptitude Sprint",
               description="Speed-first quant and logic.",
               bank_filter=_aptitude_filter("wipro")),
    TrackStage(order=3, title="Coding + Essay",
               description="Easy programs plus written communication.",
               bank_filter=_coding_filter("wipro")),
    TrackStage(order=4, title="Business Interview",
               description="Communication-led technical + HR.",
               bank_filter={"companies": ["wipro"]}),
    TrackStage(order=5, title="NLTH Mock",
               description="Full-length simulation on the NLTH pattern.",
               bank_filter={"companies": ["wipro"]}, passing_score=70),
])

_track("cognizant_genc", "cognizant", "Cognizant GenC", [
    TrackStage(order=1, title="Diagnostic", description="Baseline per topic.",
               bank_filter=_aptitude_filter("cognizant"), passing_score=0),
    TrackStage(order=2, title="Aptitude + Reasoning",
               description="Quant, logic, verbal with GenC weightage.",
               bank_filter=_aptitude_filter("cognizant")),
    TrackStage(order=3, title="Coding + SQL",
               description="Easy programs, SQL queries, cloud basics.",
               bank_filter=_coding_filter("cognizant")),
    TrackStage(order=4, title="Technical + HR",
               description="CS core plus communication.",
               bank_filter={"companies": ["cognizant"]}),
    TrackStage(order=5, title="GenC Mock",
               description="Full-length simulation on the GenC pattern.",
               bank_filter={"companies": ["cognizant"]}, passing_score=70),
])

_track("accenture", "accenture", "Accenture", [
    TrackStage(order=1, title="Diagnostic", description="Baseline per topic.",
               bank_filter=_aptitude_filter("accenture"), passing_score=0),
    TrackStage(order=2, title="Cognitive + Technical",
               description="Abstract reasoning plus pseudo-code.",
               bank_filter=_aptitude_filter("accenture")),
    TrackStage(order=3, title="Coding",
               description="Easy-medium programs.",
               bank_filter=_coding_filter("accenture")),
    TrackStage(order=4, title="Communication + Interview",
               description="Versant-style communication plus technical HR.",
               bank_filter={"companies": ["accenture"]}),
    TrackStage(order=5, title="Accenture Mock",
               description="Full-length simulation on the Accenture pattern.",
               bank_filter={"companies": ["accenture"]}, passing_score=70),
])

_track("capgemini", "capgemini", "Capgemini", [
    TrackStage(order=1, title="Diagnostic", description="Baseline per topic.",
               bank_filter=_aptitude_filter("capgemini"), passing_score=0),
    TrackStage(order=2, title="Aptitude + Reasoning",
               description="Quant, logic puzzles, verbal.",
               bank_filter=_aptitude_filter("capgemini")),
    TrackStage(order=3, title="Pseudo-code + Coding",
               description="Data-structure tracing plus easy programs.",
               bank_filter=_coding_filter("capgemini")),
    TrackStage(order=4, title="Technical + HR",
               description="CS core plus behavioral.",
               bank_filter={"companies": ["capgemini"]}),
    TrackStage(order=5, title="Capgemini Mock",
               description="Full-length simulation on the Capgemini pattern.",
               bank_filter={"companies": ["capgemini"]}, passing_score=70),
])


def get_track(track_id: str) -> Optional[ServiceTrack]:
    return SERVICE_TRACKS.get(track_id)


def list_tracks() -> List[str]:
    return sorted(SERVICE_TRACKS)


def track_mission_ids(track_id: str) -> List[str]:
    t = SERVICE_TRACKS.get(track_id)
    if not t:
        return []
    return [m for s in t.stages for m in s.mission_ids]
