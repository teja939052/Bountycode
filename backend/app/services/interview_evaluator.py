"""Structured AI interview evaluation service.

Wraps interview answer evaluation in explicit Pydantic schemas so that
technical accuracy, behavioral STAR structure, and communication metrics
are always returned in a deterministic shape.

Rubric definitions are versioned JSON to support auditability.
Every criterion score is grounded in a quoted transcript segment (quote-or-zero).

KNOWN ISSUE: Some LLM backends emit inline thinking/reasoning tokens instead
of producing final JSON. When this happens, JSON extraction fails. The current
behavior is to raise an explicit error rather than silently returning zero
scores. Do NOT ship this feature to students until a reliable model or
structured-output backend is configured.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.services.ai_core import chat_completion, parse_json


RUBRIC_VERSIONS: Dict[str, Dict[str, Any]] = {
    "behavioral": {
        "version": "1.0",
        "criteria": [
            {"id": "situation_present", "label": "Situation", "min": 0, "max": 1, "requires_quote": True},
            {"id": "task_clarity", "label": "Task", "min": 0, "max": 2, "requires_quote": True},
            {"id": "action_specificity", "label": "Action", "min": 0, "max": 3, "requires_quote": True},
            {"id": "result_quantified", "label": "Result", "min": 0, "max": 2, "requires_quote": True},
        ],
        "max_total": 8,
    },
    "hr": {
        "version": "1.0",
        "criteria": [
            {"id": "tone_professional", "label": "Professional Tone", "min": 0, "max": 2, "requires_quote": True},
            {"id": "clarity_structure", "label": "Clarity & Structure", "min": 0, "max": 2, "requires_quote": True},
            {"id": "no_red_flags", "label": "No Red Flags", "min": 0, "max": 2, "requires_quote": True},
            {"id": "alignment", "label": "Role Alignment", "min": 0, "max": 2, "requires_quote": True},
        ],
        "max_total": 8,
    },
    "technical": {
        "version": "1.0",
        "criteria": [
            {"id": "correctness", "label": "Correctness", "min": 0, "max": 3, "requires_quote": True},
            {"id": "depth", "label": "Depth", "min": 0, "max": 2, "requires_quote": True},
            {"id": "tradeoffs", "label": "Trade-offs", "min": 0, "max": 2, "requires_quote": True},
            {"id": "communication", "label": "Communication", "min": 0, "max": 2, "requires_quote": True},
            {"id": "complexity", "label": "Complexity Awareness", "min": 0, "max": 1, "requires_quote": True},
        ],
        "max_total": 10,
    },
    "system_design": {
        "version": "1.0",
        "criteria": [
            {"id": "requirements", "label": "Requirements Gathering", "min": 0, "max": 2, "requires_quote": True},
            {"id": "scalability", "label": "Scalability", "min": 0, "max": 2, "requires_quote": True},
            {"id": "tradeoffs", "label": "Trade-offs", "min": 0, "max": 2, "requires_quote": True},
            {"id": "components", "label": "Component Design", "min": 0, "max": 2, "requires_quote": True},
            {"id": "bottlenecks", "label": "Bottleneck Identification", "min": 0, "max": 2, "requires_quote": True},
        ],
        "max_total": 10,
    },
    "gd": {
        "version": "1.0",
        "criteria": [
            {"id": "opened_with_position", "label": "Opened With Position", "min": 0, "max": 1, "requires_quote": True},
            {"id": "built_on_others", "label": "Built on Others' Points", "min": 0, "max": 2, "requires_quote": True},
            {"id": "avoided_pitfall", "label": "Avoided Common Pitfall", "min": 0, "max": 2, "requires_quote": True},
            {"id": "time_management", "label": "Time Management", "min": 0, "max": 2, "requires_quote": True},
        ],
        "max_total": 7,
    },
}


class CriterionScore(BaseModel):
    id: str
    label: str
    score: int = Field(ge=0)
    max: int
    quote: str = Field(default="", description="Exact transcript segment supporting this score. Empty => score must be 0.")
    quote_verified: bool = Field(default=False, description="True when quote is a verbatim transcript substring (code-checked, not model-claimed).")


class EvaluationRubric(BaseModel):
    mode: str = "technical"
    rubric_version: str = "1.0"
    criteria: List[CriterionScore] = Field(default_factory=list)
    overall_score: int = Field(ge=0)
    filler_words: List[str] = Field(default_factory=list)
    critique: str = Field(default="")
    remediation: str = Field(default="")


class InterviewEvaluator:
    @staticmethod
    async def evaluate_response(
        question_text: str,
        expected_points: List[str],
        student_transcript: str,
        company_target: str,
        interview_mode: str = "technical",
    ) -> Dict[str, Any]:
        mode_key = (interview_mode or "technical").lower().strip()
        rubric_def = RUBRIC_VERSIONS.get(mode_key, RUBRIC_VERSIONS["technical"])
        criteria_defs = rubric_def["criteria"]
        max_total = rubric_def["max_total"]
        rubric_version = rubric_def["version"]

        criteria_prompt = "\n".join(
            f"- {c['id']} ({c['label']}): score {c['min']}-{c['max']}. "
            f"{'QUOTE REQUIRED: include the exact transcript sentence that justifies this score. If no quote possible, score MUST be 0.' if c.get('requires_quote') else ''}"
            for c in criteria_defs
        )

        system_instruction = f"""
You are an evaluation engine. Output ONLY JSON. No thinking, no reasoning, no explanation.

Evaluate the interview transcript against these criteria. For EACH criterion:
1. Assign a score within the specified range.
2. Quote the EXACT transcript sentence.
3. If no quote possible, score MUST be 0.

Criteria:
{criteria_prompt}

Output ONLY this JSON:
{{
  "criteria": [{{"id": "criterion_id", "score": 0, "quote": "exact text"}}],
  "filler_words": [],
  "critique": "text",
  "remediation": "text"
}}

RULES:
- No quote => score MUST be 0
- Quotes must be verbatim from the transcript
- Be strict, not generous
- Do NOT include any text before or after the JSON
- Do NOT explain your reasoning
- Do NOT use markdown code fences
"""

        prompt = f"""
Question: "{question_text}"
Transcript: "{student_transcript}"
"""

        try:
            raw = await chat_completion(
                [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.1,
                max_tokens=4000,
            )
            
            # Aggressive JSON extraction: find last complete JSON object
            raw_stripped = raw
            for prefix in [
                "Here's a thinking process",
                "Here is a thinking process",
                "Thinking process:",
                "Thought process:",
                "Let me think through this:",
                "Let's think step by step:",
                "Step-by-step reasoning:",
                "Reasoning:",
            ]:
                idx = raw_stripped.find(prefix)
                if idx != -1:
                    raw_stripped = raw_stripped[idx + len(prefix):]
                    break
            
            # Find the last JSON object in the response
            json_matches = list(re.finditer(r'\{[\s\S]*\}', raw_stripped))
            parsed = {}
            for match in reversed(json_matches):
                try:
                    candidate = parse_json(match.group())
                    if isinstance(candidate, dict) and "criteria" in candidate:
                        parsed = candidate
                        break
                except Exception:
                    continue
            
            if not parsed:
                # No valid JSON found - this is a system error, not a zero score
                raise ValueError("No valid JSON found in model output")
            
            raw_criteria = parsed.get("criteria", [])
            criteria_by_id = {c["id"]: c for c in criteria_defs}
            scored_criteria: List[CriterionScore] = []
            total = 0

            # Structural quote-or-zero: a quote counts only when it is a
            # verbatim (whitespace-normalized, case-insensitive) substring
            # of the transcript. Prompt instructions ask the model for this,
            # but the guarantee is enforced here in code, so a hallucinated
            # quote can never carry a nonzero score.
            def _norm(s: str) -> str:
                return re.sub(r"\s+", " ", str(s or "")).strip().lower()

            transcript_norm = _norm(student_transcript)
            for cdef in criteria_defs:
                cid = cdef["id"]
                raw_match = next((c for c in raw_criteria if c.get("id") == cid), {})
                score = int(raw_match.get("score", 0))
                quote = str(raw_match.get("quote", "")).strip()
                quote_verified = bool(quote) and _norm(quote) in transcript_norm
                if cdef.get("requires_quote") and not quote_verified:
                    score = 0
                    quote = ""
                score = max(cdef["min"], min(cdef["max"], score))
                total += score
                scored_criteria.append(CriterionScore(
                    id=cid,
                    label=cdef["label"],
                    score=score,
                    max=cdef["max"],
                    quote=quote,
                    quote_verified=quote_verified,
                ))

            overall = min(max_total, max(0, total))
            rubric = EvaluationRubric(
                mode=mode_key,
                rubric_version=rubric_version,
                criteria=scored_criteria,
                overall_score=overall,
                filler_words=parsed.get("filler_words", []),
                critique=str(parsed.get("critique", "")),
                remediation=str(parsed.get("remediation", "")),
            )
            return rubric.model_dump()
        except Exception as e:
            # Return explicit error state instead of zero scores
            return {
                "error": True,
                "error_type": "evaluation_failed",
                "error_message": str(e),
                "mode": mode_key,
                "rubric_version": rubric_version,
                "criteria": [
                    CriterionScore(id=c["id"], label=c["label"], score=0, max=c["max"], quote="")
                    for c in criteria_defs
                ],
                "overall_score": 0,
                "filler_words": [],
                "critique": "Evaluation failed. Please retry.",
                "remediation": "Retry the assessment.",
            }
