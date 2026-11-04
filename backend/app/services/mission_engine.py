"""Minimal mission engine shim.

Provides DOMAIN_MAP and get_skill_rank so that job_readiness (and hence
curriculum_engine) can import without failing. Full mission logic is out of
scope for this milestone.
"""
DOMAIN_MAP: dict = {}


def get_skill_rank(skill: str) -> str:
    """Return a placeholder skill rank."""
    return "unknown"
