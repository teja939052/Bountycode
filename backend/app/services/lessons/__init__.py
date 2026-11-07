"""Lesson catalog loader — aggregates all track modules into one dict.

Rules enforced here (see docs/learning/BOUNTYCODE_LESSON_AUDIT.md):
- Never silently overwrite: a duplicate lesson id logs an error and is dropped;
  the first module in import order wins deterministically.
- Every dropped id is recorded in ``_DROPPED_DUPLICATES`` so tests can assert
  the catalog is clean (empty) rather than papering over data bugs.
"""
from typing import Dict, List, Tuple

from .python import PYTHON_LESSONS
from .python_content import PYTHON_CONTENT_LESSONS
from .java import JAVA_LESSONS
from .cpp import CPP_LESSONS
from .c import C_LESSONS
from .dsa import DSA_LESSONS
from .aptitude import APTITUDE_LESSONS
from .logical import LOGICAL_LESSONS
from .verbal import VERBAL_LESSONS
from .dbms import DBMS_LESSONS
from .os import OS_LESSONS
from .networks import NETWORKS_LESSONS
from .oop import OOP_LESSONS
from .company_prep import COMPANY_PREP_LESSONS
from .debugging import DEBUGGING_LESSONS
from .system_design import SYSTEM_DESIGN_LESSONS
from .behavioral import BEHAVIORAL_LESSONS
from .architecture import ARCHITECTURE_LESSONS

import logging

logger = logging.getLogger(__name__)

_LESSONS: Dict[str, dict] = {}

# (lesson_id, winner_module, loser_module) for every dropped duplicate
_DROPPED_DUPLICATES: List[Tuple[str, str, str]] = []
_SEEN_MODULE: Dict[str, str] = {}

_TRACK_MODULES: List[Tuple[str, List[dict]]] = [
    ("python", PYTHON_LESSONS),
    ("python_content", PYTHON_CONTENT_LESSONS),
    ("java", JAVA_LESSONS),
    ("cpp", CPP_LESSONS),
    ("c", C_LESSONS),
    ("dsa", DSA_LESSONS),
    ("aptitude", APTITUDE_LESSONS),
    ("logical", LOGICAL_LESSONS),
    ("verbal", VERBAL_LESSONS),
    ("dbms", DBMS_LESSONS),
    ("os", OS_LESSONS),
    ("networks", NETWORKS_LESSONS),
    ("oop", OOP_LESSONS),
    ("company_prep", COMPANY_PREP_LESSONS),
    ("debugging", DEBUGGING_LESSONS),
    ("system_design", SYSTEM_DESIGN_LESSONS),
    ("behavioral", BEHAVIORAL_LESSONS),
    ("architecture", ARCHITECTURE_LESSONS),
]

for _module_name, _lessons in _TRACK_MODULES:
    for _l in _lessons:
        if _l["id"] in _LESSONS:
            logger.error(
                "Duplicate lesson id %r (kept first occurrence from %r, dropped from %r)",
                _l["id"],
                _SEEN_MODULE[_l["id"]],
                _module_name,
            )
            _DROPPED_DUPLICATES.append((_l["id"], _SEEN_MODULE[_l["id"]], _module_name))
            continue
        _LESSONS[_l["id"]] = _l
        _SEEN_MODULE[_l["id"]] = _module_name

__all__ = [
    "_LESSONS",
    "_DROPPED_DUPLICATES",
    "PYTHON_LESSONS",
    "PYTHON_CONTENT_LESSONS",
    "JAVA_LESSONS",
    "CPP_LESSONS",
    "C_LESSONS",
    "DSA_LESSONS",
    "APTITUDE_LESSONS",
    "LOGICAL_LESSONS",
    "VERBAL_LESSONS",
    "DBMS_LESSONS",
    "OS_LESSONS",
    "NETWORKS_LESSONS",
    "OOP_LESSONS",
    "COMPANY_PREP_LESSONS",
    "DEBUGGING_LESSONS",
    "SYSTEM_DESIGN_LESSONS",
    "BEHAVIORAL_LESSONS",
    "ARCHITECTURE_LESSONS",
]
