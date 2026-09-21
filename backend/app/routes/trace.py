"""Route for algorithm trace generation — provides step-by-step visual data
for the AlgorithmTracer frontend component.

Student-facing: POST /api/v1/trace/generate
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any

router = APIRouter(prefix="/api/v1/trace", tags=["trace"])


class TraceRequest(BaseModel):
    algorithm: str
    input_data: dict[str, Any] = {}


@router.post("/generate")
async def generate_trace_endpoint(req: TraceRequest):
    """Generate step-by-step algorithm trace for visualization.

    Returns the full visual_trace document (kind, algorithm, version, initial, steps, questions).
    The frontend AlgorithmTracer reads .steps from this response.
    """
    from app.services.algorithm_tracer import generate_trace

    trace = generate_trace(req.algorithm, req.input_data)
    if not trace or trace.get("error"):
        raise HTTPException(
            status_code=400,
            detail=trace.get("error", f"Unknown algorithm '{req.algorithm}' or invalid input. "
            f"Supported: sliding_window_max, two_sum, binary_search, bubble_sort"),
        )
    return trace
