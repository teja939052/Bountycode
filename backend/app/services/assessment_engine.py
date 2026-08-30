import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.services.real_ats import RealATSScanner

logger = logging.getLogger(__name__)


class AssessmentDefinition:
    """Represents a structured assessment with stages, competencies, and rubrics."""

    def __init__(self, definition_data: dict):
        self.id = definition_data.get("id")
        self.role = definition_data.get("role")
        self.level = definition_data.get("level")
        self.duration_minutes = definition_data.get("duration_minutes", 60)
        self.competencies = definition_data.get("competencies", [])
        self.stages = definition_data.get("stages", [])
        self.rubric = definition_data.get("rubric", {})

    def validate_stage(self, stage_name: str, answer: dict) -> Optional[dict]:
        """Validate a stage answer and return scoring."""
        for stage in self.stages:
            if stage.get("stage") == stage_name:
                return self._score_stage(stage, answer)
        return None

    def _score_stage(self, stage: dict, answer: dict) -> dict:
        """Score a single stage answer based on rubric."""
        stage_type = stage.get("type", "rubric")
        points = stage.get("points", 0)

        if stage_type == "rubric":
            rubric = self.rubric.get(stage.get("competency", ""), {})
            categories = rubric.get("excellent", {})
            answer_text = answer.get("answer", "") or ""
            score = 0
            if answer_text:
                for key in categories:
                    if key.lower() in answer_text.lower():
                        score += 1
            return {
                "stage": stage.get("stage"),
                "points_earned": min(points, score * (points // max(1, len(categories)))),
                "points_possible": points,
                "feedback": f"Stage {stage.get('stage')}: partial rubric evaluation",
            }

        elif stage_type == "code_execution":
            code = answer.get("code", "")
            if code:
                scanner = RealATSScanner()
                scan = scanner.full_scan(code)
                return {
                    "stage": stage.get("stage"),
                    "points_earned": scan.get("ats_score", 0),
                    "points_possible": points,
                    "feedback": f"Code analysis: score {scan.get('ats_score', 0)}/100, grade {scan.get('grade', 'F')}",
                    "ats_simulation": {
                        "parsing_score": scan.get("parsing_score", 0),
                        "detected_sections": scan.get("detected_sections", {}),
                        "missing_sections": [s for s in scan.get("missing_sections", [])],
                        "landmines_found": [
                            {"type": lm["type"], "message": lm["message"]}
                            for lm in scan.get("landmines_found", [])
                        ],
                    },
                }
            return {
                "stage": stage.get("stage"),
                "points_earned": 0,
                "points_possible": points,
                "feedback": "No code provided for execution",
            }

        elif stage_type == "mcq":
            correct = answer.get("correct", False)
            selected = answer.get("selected", False)
            return {
                "stage": stage.get("stage"),
                "points_earned": points if correct == selected else 0,
                "points_possible": points,
                "feedback": "Correct!" if correct == selected else "Incorrect.",
            }

        elif stage_type == "system_design":
            response = answer.get("response", "")
            points_earned = 0
            if response:
                keywords = ["scaling", "caching", "database", "api", "load balancer", "tradeoffs"]
                found = sum(1 for kw in keywords if kw.lower() in response.lower())
                points_earned = min(points, found * (points // max(1, len(keywords))))
            return {
                "stage": stage.get("stage"),
                "points_earned": points_earned,
                "points_possible": points,
                "feedback": f"System design evaluation: {found}/{len(keywords)} key components identified",
            }

        else:
            return {
                "stage": stage.get("stage"),
                "points_earned": 0,
                "points_possible": points,
                "feedback": "Stage evaluation not yet implemented for this type.",
            }

    def generate_evidence_report(self, stage_results: list) -> dict:
        """Aggregate stage results into a competency evidence report."""
        competency_scores: Dict[str, dict] = {
            c: {"score": 0, "total": 0, "evidence": []} for c in self.competencies
        }

        for result in stage_results:
            stage_name = result.get("stage", "")
            score_data = result.get("points_earned", 0)
            points_possible = result.get("points_possible", 1)

            for comp in self.competencies:
                if any(kw in stage_name.lower() for kw in comp.lower().split()):
                    competency_scores[comp]["score"] += score_data
                    competency_scores[comp]["total"] += points_possible
                    feedback = result.get("feedback", "")
                    if feedback and len(competency_scores[comp]["evidence"]) < 3:
                        competency_scores[comp]["evidence"].append(
                            {
                                "stage": stage_name,
                                "score_contribution": score_data,
                                "total_possible": points_possible,
                                "feedback": feedback,
                            }
                        )

        report: dict = {
            "assessment_id": self.id,
            "role": self.role,
            "level": self.level,
            "generated_at": datetime.now().isoformat(),
            "competency_breakdown": {},
            "overall_readiness": 0,
        }

        for comp, data in competency_scores.items():
            pct = (data["score"] / data["total"] * 100) if data["total"] > 0 else 0
            report["competency_breakdown"][comp] = {
                "score": data["score"],
                "total": data["total"],
                "percentage": round(pct, 1),
                "evidence": data["evidence"],
            }
            report["overall_readiness"] += pct

        if self.competencies:
            report["overall_readiness"] = round(
                report["overall_readiness"] / len(self.competencies), 1
            )

        return report


class AssessmentSession:
    """Manages a single assessment session state."""

    def __init__(self, definition: AssessmentDefinition):
        self.definition = definition
        self.stage_index = 0
        self.stage_answers: list = []
        self.start_time: Optional[Any] = None
        self.end_time: Optional[Any] = None
        self.ai_mode: Optional[str] = None

    def start(self, ai_mode: str = "prohibited") -> dict:
        """Start a new assessment session."""
        self.ai_mode = ai_mode
        self.stage_index = 0
        self.stage_answers = []
        self.start_time = datetime.now()
        self.end_time = None
        return {
            "assessment_id": self.definition.id,
            "ai_mode": self.ai_mode,
            "stages_total": len(self.definition.stages)
            if self.definition.stages
            else 0,
            "message": "Assessment session started.",
        }

    def submit_stage(self, stage_name: str, answer: dict) -> dict:
        """Submit an answer for a stage and advance to next stage."""
        score_result = self.definition.validate_stage(stage_name, answer)
        self.stage_answers.append(
            {
                "stage": stage_name,
                "answer": answer,
                "score": score_result,
                "submitted_at": datetime.now().isoformat(),
            }
        )
        self.stage_index += 1
        self.end_time = datetime.now()
        next_stage = (
            self.definition.stages[self.stage_index]["stage"]
            if self.stage_index < len(self.definition.stages)
            else None
        )
        return {
            "stage_completed": stage_name,
            "score": score_result,
            "next_stage": next_stage,
            "stages_remaining": len(self.definition.stages) - self.stage_index,
            "message": f"Stage '{stage_name}' submitted.",
        }

    def get_report(self) -> dict:
        """Generate final evidence report for the completed assessment."""
        if self.end_time is None:
            return {"status": "assessment not completed"}
        return self.definition.generate_evidence_report(self.stage_answers)


class AssessmentEngine:
    """High-level engine for creating and managing assessments."""

    def __init__(self):
        self.definitions: Dict[str, AssessmentDefinition] = {}
        self.sessions: Dict[str, AssessmentSession] = {}
        self._load_definitions()

    def _load_definitions(self) -> None:
        """Load assessment definitions from JSON file."""
        try:
            # Resolve path relative to this module file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            definitions_path = os.path.join(base_dir, "..", "data", "assessment_definitions.json")
            with open(definitions_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for name, def_data in data.get("assessment_definitions", {}).items():
                self.definitions[name] = AssessmentDefinition(def_data)
            logger.info(f"Loaded {len(self.definitions)} assessment definitions")
        except Exception as e:
            logger.warning(f"Could not load assessment definitions: {e}")

    def get_definition(self, definition_id: str) -> Optional[AssessmentDefinition]:
        """Get an assessment definition by ID."""
        return self.definitions.get(definition_id)

    def create_session(self, definition_id: str, ai_mode: str = "prohibited") -> Optional[dict]:
        """Create a new assessment session."""
        definition = self.get_definition(definition_id)
        if not definition:
            return None
        session = AssessmentSession(definition)
        # Store session
        session_id = f"session_{definition_id}_{id(session)}"
        self.sessions[session_id] = session
        result = session.start(ai_mode=ai_mode)
        result["session_id"] = session_id
        return result

    def submit_answer(self, session_id: str, stage_name: str, answer: dict) -> dict:
        """Submit an answer for a stage in a session."""
        # Look up session by ID
        session = self.sessions.get(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}
        return session.submit_stage(stage_name, answer)

    def end_session(self, session_id: str) -> Optional[dict]:
        """End a session and get report."""
        session = self.sessions.get(session_id)
        if not session:
            return None
        return session.get_report()


# Global engine instance
engine = AssessmentEngine()

# For FastAPI dependency injection
get_assessment_engine = lambda: engine