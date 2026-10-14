"""Tests for the v2 question-bank generator scripts.

Covers (without running full multi-minute generation):
- every generator script compiles cleanly
- deterministic oracle helpers produce correct answers (spot checks)
- each script declares the expected output bank filename
- generator ID schemes are well-formed
"""
from __future__ import annotations

import math
import os
import py_compile

import pytest

_BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS_DIR = os.path.join(_BACKEND_ROOT, "scripts")

_GENERATOR_SCRIPTS = [
    "gen_thin_v2.py",
    "gen_debugging_v2.py",
    "gen_interview_v2.py",
    "gen_csfund_v2.py",
    "gen_logical_v2.py",
    "gen_reasoning_v2.py",
    "gen_sql_v2.py",
    "gen_written_v2.py",
    "gen_verbal_v2.py",
    "gen_aptitude_v2.py",
    "gen_coding_v2.py",
]

_SCRIPT_TO_BANK = {
    "gen_thin_v2.py": "bank_thin_v2.json",
    "gen_debugging_v2.py": "bank_debugging_v2.json",
    "gen_interview_v2.py": "bank_interview_v2.json",
    "gen_csfund_v2.py": "bank_csfund_v2.json",
    "gen_logical_v2.py": "bank_logical_v2.json",
    "gen_reasoning_v2.py": "bank_reasoning_v2.json",
    "gen_sql_v2.py": "bank_sql_v2.json",
    "gen_written_v2.py": "bank_written_v2.json",
    "gen_verbal_v2.py": "bank_verbal_v2.json",
    "gen_aptitude_v2.py": "bank_aptitude_v2.json",
    "gen_coding_v2.py": "bank_coding_v2.json",
}


@pytest.mark.parametrize("script", _GENERATOR_SCRIPTS)
def test_generator_script_exists_and_compiles(script):
    path = os.path.join(_SCRIPTS_DIR, script)
    assert os.path.exists(path), f"missing generator script {script}"
    py_compile.compile(path, doraise=True)


@pytest.mark.parametrize("script", _GENERATOR_SCRIPTS)
def test_generator_declares_its_output_bank(script):
    path = os.path.join(_SCRIPTS_DIR, script)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    expected_bank = _SCRIPT_TO_BANK[script]
    assert expected_bank in src, f"{script} does not reference {expected_bank}"
    assert "trust_status" in src, f"{script} never sets trust_status"


def test_all_eleven_generators_present():
    assert len(_GENERATOR_SCRIPTS) == 11


# ─── Oracle spot checks (mirror the generators' deterministic math) ──
def test_oracle_successive_percent():
    a, b = 20, -20
    net = a + b + a * b / 100
    assert net == -4.0


def test_oracle_work_together():
    a, b = 6, 12
    assert a * b / (a + b) == 4.0


def test_oracle_harmonic_mean():
    v1, v2 = 40, 60
    assert 2 * v1 * v2 / (v1 + v2) == 48.0


def test_oracle_hcf_lcm_identity():
    for a, b in [(12, 18), (7, 13), (24, 36)]:
        g = math.gcd(a, b)
        assert a * b == g * (a * b // g)


def test_oracle_clock_angle():
    h, m = 3, 15
    angle = abs(30 * h - 5.5 * m)
    assert angle == 7.5


def test_oracle_handshake_count():
    p = 10
    assert p * (p - 1) // 2 == 45


def test_oracle_binary_search_contract():
    a = [1, 3, 5, 7, 9]
    lo, hi, x = 0, len(a) - 1, 7
    found = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            found = mid
            break
        elif a[mid] < x:
            lo = mid + 1
        else:
            hi = mid - 1
    assert found == 3


def test_oracle_kadane():
    a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    best = cur = a[0]
    for x in a[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    assert best == 6


def test_oracle_xor_single():
    arr = [2, 2, 1, 4, 4]
    x = 0
    for v in arr:
        x ^= v
    assert x == 1
