"""Authored missions (trust-marked, UNVERIFIED until reviewed).

Every mission validates against the live serving gate before it ships.
See docs/MISSION_CONTRACT.md.
"""
from __future__ import annotations

from typing import Dict

from app.content.mission_definitions import MissionDefinition

from app.content.curriculum.missions.tcs_nqt_percentages_change import (
    MISSION as PERCENTAGES,
)
from app.content.curriculum.missions.tcs_nqt_ratio_proportion import (
    MISSION as RATIO,
)
from app.content.curriculum.missions.tcs_nqt_averages import (
    MISSION as AVERAGES,
)
from app.content.curriculum.missions.tcs_nqt_profit_loss import (
    MISSION as PROFIT,
)
from app.content.curriculum.missions.tcs_nqt_time_work import (
    MISSION as TIMEWORK,
)
from app.content.curriculum.missions.tcs_nqt_blood_relations import (
    MISSION as BLOOD,
)
from app.content.curriculum.missions.tcs_nqt_directions import (
    MISSION as DIRECTIONS,
)
from app.content.curriculum.missions.tcs_nqt_coding_decoding import (
    MISSION as CODINGDEC,
)
from app.content.curriculum.missions.tcs_nqt_number_series import (
    MISSION as SERIES,
)
from app.content.curriculum.missions.tcs_nqt_sentence_correction import (
    MISSION as GRAMMAR,
)
from app.content.curriculum.missions.tcs_nqt_reading_comprehension import (
    MISSION as READING,
)
from app.content.curriculum.missions.tcs_nqt_variables_basics import (
    MISSION as VARIABLES,
)
from app.content.curriculum.missions.tcs_nqt_conditions import (
    MISSION as CONDITIONS,
)
from app.content.curriculum.missions.tcs_nqt_loops_basics import (
    MISSION as LOOPS,
)
from app.content.curriculum.missions.tcs_nqt_strings_basics import (
    MISSION as STRINGS,
)
from app.content.curriculum.missions.tcs_nqt_arrays_basics import (
    MISSION as ARRAYS,
)

MISSIONS: Dict[str, MissionDefinition] = {
    PERCENTAGES.id: PERCENTAGES,
    RATIO.id: RATIO,
    AVERAGES.id: AVERAGES,
    PROFIT.id: PROFIT,
    TIMEWORK.id: TIMEWORK,
    BLOOD.id: BLOOD,
    DIRECTIONS.id: DIRECTIONS,
    CODINGDEC.id: CODINGDEC,
    SERIES.id: SERIES,
    GRAMMAR.id: GRAMMAR,
    READING.id: READING,
    VARIABLES.id: VARIABLES,
    CONDITIONS.id: CONDITIONS,
    LOOPS.id: LOOPS,
    STRINGS.id: STRINGS,
    ARRAYS.id: ARRAYS,
}
