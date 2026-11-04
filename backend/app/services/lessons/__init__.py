"""Lesson catalog loader — aggregates all track modules into _LESSONS dict."""
from typing import Dict

from .python import PYTHON_LESSONS
from .java import JAVA_LESSONS
from .cpp import CPP_LESSONS
from .dsa import DSA_LESSONS
from .aptitude import APTITUDE_LESSONS
from .logical import LOGICAL_LESSONS
from .verbal import VERBAL_LESSONS
from .dbms import DBMS_LESSONS
from .os import OS_LESSONS
from .networks import NETWORKS_LESSONS
from .oop import OOP_LESSONS
from .company_prep import COMPANY_PREP_LESSONS

_LESSONS: Dict[str, dict] = {}

for _lessons in (
    PYTHON_LESSONS,
    JAVA_LESSONS,
    CPP_LESSONS,
    DSA_LESSONS,
    APTITUDE_LESSONS,
    LOGICAL_LESSONS,
    VERBAL_LESSONS,
    DBMS_LESSONS,
    OS_LESSONS,
    NETWORKS_LESSONS,
    OOP_LESSONS,
    COMPANY_PREP_LESSONS,
):
    for _l in _lessons:
        _LESSONS[_l["id"]] = _l

__all__ = ["_LESSONS", "PYTHON_LESSONS", "JAVA_LESSONS", "CPP_LESSONS",
           "DSA_LESSONS", "APTITUDE_LESSONS", "LOGICAL_LESSONS",
           "VERBAL_LESSONS", "DBMS_LESSONS", "OS_LESSONS",
           "NETWORKS_LESSONS", "OOP_LESSONS", "COMPANY_PREP_LESSONS"]
