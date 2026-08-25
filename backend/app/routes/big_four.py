"""Big 4 Consul's Trade Route - Deloitte/PwC/EY/KPMG style prep.

Three cargo holds:
1. Firm intelligence (static profiles).
2. Case-study practice with AI evaluation on the consulting
   framework: Identify -> Assess -> Prioritize -> Mitigate -> Monitor.
3. SQL screening drill (static hand-verified MCQ bank).
"""

from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.middleware.auth import get_current_user
from app.services.gamification import record_practice

router = APIRouter(prefix="/api/v1/big-four", tags=["big-four"])

FIRMS = [
    {
        "firm_id": "deloitte",
        "name": "Deloitte",
        "tagline": "Audit, tax, consulting and risk advisory at global scale.",
        "values": [
            "Lead the way",
            "Serve with integrity",
            "Take care of each other",
            "Foster inclusion",
            "Collaborate for measurable impact",
        ],
        "rounds": [
            "Online assessment (quant + logical + verbal)",
            "Versant English / communication test",
            "Technical interview (project deep-dive)",
            "Partner round (behavioral + culture fit)",
        ],
        "prep_tips": [
            "Know your resume projects cold - partner rounds dig into ownership.",
            "Practice structured speaking; Versant penalizes hesitation.",
            "Have one integrity story ready - it is a stated core value.",
        ],
    },
    {
        "firm_id": "pwc",
        "name": "PwC",
        "tagline": "Trust-led professional services; big on purpose.",
        "values": [
            "Act with integrity",
            "Make a difference",
            "Care",
            "Work together",
            "Reimagine the possible",
        ],
        "rounds": [
            "Online assessment (numerical + reasoning + game-based)",
            "Technical / HR combined screen",
            "Case discussion or business scenario",
            "Partner interview (values-driven behavioral)",
        ],
        "prep_tips": [
            "Weave 'reimagine the possible' into a project story.",
            "Game-based assessments reward steady, consistent play - do not rush.",
            "Prepare a 'make a difference' example from college or work.",
        ],
    },
    {
        "firm_id": "ey",
        "name": "EY (Ernst & Young)",
        "tagline": "Building a better working world; strong tech-risk practice.",
        "values": [
            "Integrity",
            "Respect",
            "Teamwork",
            "Enthusiasm with energy",
            "Relationships built on doing the right thing",
        ],
        "rounds": [
            "Online assessment (aptitude + coding basics)",
            "Group discussion / case study",
            "Technical interview (SQL, data, domain)",
            "HR + partner round",
        ],
        "prep_tips": [
            "GD rounds reward structure over volume - speak second, summarize.",
            "Brush up Excel + SQL; tech-risk roles test both.",
            "'Building a better working world' - align project impact to it.",
        ],
    },
    {
        "firm_id": "kpmg",
        "name": "KPMG",
        "tagline": "Cutting through complexity; audit and advisory depth.",
        "values": [
            "Integrity - we do what is right",
            "Excellence - we never stop learning",
            "Courage - we think and act boldly",
            "Together - we go further",
            "For better - we act with purpose",
        ],
        "rounds": [
            "Online assessment (quant + verbal + logical)",
            "Technical interview (analytics/finance fundamentals)",
            "Managerial round (scenario handling)",
            "HR round",
        ],
        "prep_tips": [
            "'Cutting through complexity' - frame answers as simplify-and-solve.",
            "Scenario rounds test client-handling judgment; use STAR format.",
            "Know basic IFRS/audit vocabulary if applying to assurance.",
        ],
    },
]

CASE_STUDIES = [
    {
        "case_id": "deloitte-data-breach",
        "firm_id": "deloitte",
        "title": "Client X Data Breach Response",
        "context": (
            "Your client, a mid-size fintech, discovered that a third-party "
            "vendor had unauthorized access to customer PII for roughly three "
            "weeks before detection. Regulators require notification within 72 "
            "hours of confirmed breach scope. The board is asking whether to "
            "pause an ongoing product launch."
        ),
        "task": (
            "Structure a consulting response: how would you identify the full "
            "impact, assess severity, prioritize actions, mitigate damage, and "
            "set up monitoring so this does not repeat?"
        ),
        "framework": ["Identify", "Assess", "Prioritize", "Mitigate", "Monitor"],
    },
    {
        "case_id": "pwc-market-entry",
        "firm_id": "pwc",
        "title": "Retail Chain Digital Expansion",
        "context": (
            "A 400-store retail chain wants to launch quick-commerce delivery "
            "in six metro cities within nine months. Competitors already have "
            "10-minute delivery. The CFO fears margin dilution; the CEO wants "
            "market share."
        ),
        "task": (
            "Identify the key risks and value drivers, assess which cities and "
            "segments to start with, prioritize investments, propose mitigation "
            "for the margin concern, and define metrics to monitor the pilot."
        ),
        "framework": ["Identify", "Assess", "Prioritize", "Mitigate", "Monitor"],
    },
    {
        "case_id": "ey-erp-migration",
        "firm_id": "ey",
        "title": "ERP Migration Gone Over Budget",
        "context": (
            "A manufacturing client is 14 months into an ERP migration that is "
            "8 months late and 40% over budget. The vendor blames scope creep; "
            "the client's internal team blames poor data quality. Go-live is "
            "scheduled during peak season."
        ),
        "task": (
            "Identify root causes, assess options (delay vs phased go-live vs "
            "descoping), prioritize a recovery plan, mitigate peak-season risk, "
            "and set up governance monitoring."
        ),
        "framework": ["Identify", "Assess", "Prioritize", "Mitigate", "Monitor"],
    },
    {
        "case_id": "kpmg-tax-compliance",
        "firm_id": "kpmg",
        "title": "Multi-State Tax Compliance Mess",
        "context": (
            "An e-commerce client expanded into 11 states in 18 months without "
            "a unified tax engine. Notices have started arriving from two "
            "states. Finance runs reconciliation in spreadsheets."
        ),
        "task": (
            "Identify exposure across states, assess penalty and interest "
            "liability, prioritize remediation order, mitigate regulator "
            "escalation risk, and propose a monitoring cadence plus tooling."
        ),
        "framework": ["Identify", "Assess", "Prioritize", "Mitigate", "Monitor"],
    },
]

SQL_QUESTIONS: List[Dict] = [
    {
        "id": "sql-01",
        "topic": "Basics",
        "question": "Which clause filters rows BEFORE grouping?",
        "options": ["HAVING", "WHERE", "GROUP BY", "ORDER BY"],
        "correct_answer": "WHERE",
        "explanation": "WHERE filters individual rows first; HAVING filters aggregated groups afterwards.",
    },
    {
        "id": "sql-02",
        "topic": "Joins",
        "question": "INNER JOIN between employees and departments returns:",
        "options": [
            "All employees even without a department",
            "Only rows with matches in BOTH tables",
            "All departments even without employees",
            "Cartesian product of both tables",
        ],
        "correct_answer": "Only rows with matches in BOTH tables",
        "explanation": "INNER JOIN keeps only matched pairs; unmatched rows are dropped from both sides.",
    },
    {
        "id": "sql-03",
        "topic": "Aggregates",
        "question": "SELECT COUNT(col) ignores:",
        "options": ["Zero values", "NULL values", "Duplicates", "Empty strings"],
        "correct_answer": "NULL values",
        "explanation": "COUNT(col) counts non-NULL values only; COUNT(*) counts every row.",
    },
    {
        "id": "sql-04",
        "topic": "Subqueries",
        "question": "A correlated subquery executes:",
        "options": [
            "Once for the whole query",
            "Once per row of the outer query",
            "Only if indexes exist",
            "Never - it is invalid syntax",
        ],
        "correct_answer": "Once per row of the outer query",
        "explanation": "Correlated subqueries reference outer columns, so they re-run per candidate row.",
    },
    {
        "id": "sql-05",
        "topic": "Indexes",
        "question": "Which column benefits MOST from a B-tree index?",
        "options": [
            "Gender with 2 distinct values",
            "Boolean flag column",
            "employee_id with unique values",
            "Column used only in SELECT list",
        ],
        "correct_answer": "employee_id with unique values",
        "explanation": "High-cardinality columns give indexes selectivity; low-cardinality flags rarely help.",
    },
    {
        "id": "sql-06",
        "topic": "Normalization",
        "question": "Second normal form removes:",
        "options": [
            "Transitive dependencies",
            "Partial dependencies on composite keys",
            "Repeating groups",
            "Multivalued dependencies",
        ],
        "correct_answer": "Partial dependencies on composite keys",
        "explanation": "1NF removes repeating groups, 2NF removes partial dependency on part of a composite key, 3NF removes transitive dependencies.",
    },
    {
        "id": "sql-07",
        "topic": "Aggregates",
        "question": "To filter groups by aggregate value you use:",
        "options": ["WHERE sum(x) > 100", "HAVING SUM(x) > 100", "FILTER x > 100", "GROUP WHERE x > 100"],
        "correct_answer": "HAVING SUM(x) > 100",
        "explanation": "Aggregates cannot appear in WHERE; HAVING applies after GROUP BY aggregation.",
    },
    {
        "id": "sql-08",
        "topic": "Joins",
        "question": "LEFT JOIN keeps unmatched rows from:",
        "options": [
            "The right table only",
            "Neither table",
            "The left table (NULLs filled on the right)",
            "Both tables",
        ],
        "correct_answer": "The left table (NULLs filled on the right)",
        "explanation": "LEFT JOIN preserves every left-table row, padding missing right-side columns with NULLs.",
    },
    {
        "id": "sql-09",
        "topic": "Set Ops",
        "question": "UNION differs from UNION ALL because UNION:",
        "options": [
            "Is faster",
            "Keeps duplicates",
            "Removes duplicate rows",
            "Works on different column counts",
        ],
        "correct_answer": "Removes duplicate rows",
        "explanation": "UNION deduplicates via an implicit sort/hash; UNION ALL skips that and is faster.",
    },
    {
        "id": "sql-10",
        "topic": "Transactions",
        "question": "ROLLBACK after an UPDATE without COMMIT:",
        "options": [
            "Is illegal",
            "Undoes the update",
            "Commits partially",
            "Only undoes deletes",
        ],
        "correct_answer": "Undoes the update",
        "explanation": "Uncommitted changes live in the transaction; ROLLBACK discards them entirely.",
    },
    {
        "id": "sql-11",
        "topic": "DDL vs DML",
        "question": "Which statement is DDL rather than DML?",
        "options": ["UPDATE", "INSERT", "ALTER TABLE", "DELETE"],
        "correct_answer": "ALTER TABLE",
        "explanation": "ALTER changes schema (DDL); UPDATE/INSERT/DELETE change data (DML).",
    },
    {
        "id": "sql-12",
        "topic": "Keys",
        "question": "A foreign key may reference:",
        "options": [
            "Any column",
            "A unique or primary key column",
            "Only numeric columns",
            "Only indexed text columns",
        ],
        "correct_answer": "A unique or primary key column",
        "explanation": "FKs must point at a key guaranteed unique - PRIMARY KEY or UNIQUE constraint.",
    },
    {
        "id": "sql-13",
        "topic": "Window Functions",
        "question": "ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) gives:",
        "options": [
            "Global rank ignoring department",
            "Dense rank within department",
            "Per-department sequence ordered by salary descending",
            "Total count per department",
        ],
        "correct_answer": "Per-department sequence ordered by salary descending",
        "explanation": "PARTITION BY restarts numbering per department; ORDER BY sets sequence direction.",
    },
    {
        "id": "sql-14",
        "topic": "Nulls",
        "question": "WHERE col = NULL returns:",
        "options": [
            "Rows where col is NULL",
            "All rows",
            "No rows - use IS NULL instead",
            "Syntax error",
        ],
        "correct_answer": "No rows - use IS NULL instead",
        "explanation": "= NULL evaluates to UNKNOWN for every row; NULL checks require IS NULL / IS NOT NULL.",
    },
    {
        "id": "sql-15",
        "topic": "Performance",
        "question": "Leading wildcard LIKE '%term' typically:",
        "options": [
            "Uses indexes fine",
            "Prevents index usage causing scans",
            "Is faster than exact match",
            "Errors in standard SQL",
        ],
        "correct_answer": "Prevents index usage causing scans",
        "explanation": "B-tree indexes order by prefix; a leading % makes the tree unusable, forcing a scan.",
    },
]


class SubmitAnswer(BaseModel):
    answer: str


class CheckSql(BaseModel):
    question_id: str
    answer: str


class SubmitCase(BaseModel):
    response: str


@router.get("/firms")
async def get_firms():
    """Static Big 4 intelligence cards."""
    return {"firms": FIRMS}


@router.get("/cases")
async def list_cases():
    return {
        "cases": [
            {k: c[k] for k in ("case_id", "firm_id", "title")}
            for c in CASE_STUDIES
        ]
    }


@router.get("/cases/{case_id}")
async def get_case(case_id: str):
    case = next((c for c in CASE_STUDIES if c["case_id"] == case_id), None)
    if not case:
        raise HTTPException(status_code=404, detail="Unknown case")
    return {"case": {k: v for k, v in case.items() if k != "model_answer"}}


async def _grade_case(case: Dict, response: str) -> Dict:
    """AI-grade a case response against the five-step framework."""
    empty = not response.strip()
    if empty:
        return {"overall": 0, "dimensions": [], "feedback": "No response submitted."}

    try:
        from app.services.ai import chat_completion, parse_json

        dims = ", ".join(case["framework"])
        instruction = f"""You are a Big 4 consulting senior manager grading a junior's case response.

CASE TITLE: {case['title']}
CONTEXT: {case['context'][:900]}
TASK: {case['task'][:500]}

Grade the CANDIDATE RESPONSE on these dimensions (0-20 each): {dims}

CANDIDATE RESPONSE:
{response[:3500]}

Return STRICT JSON only:
{{"dimensions": [{{"name": "<dimension>", "score": <0-20>, "note": "<one short line>"}}], "feedback": "<two sentences max>"}}"""

        raw = await chat_completion(
            [{"role": "user", "content": instruction}],
            use_cache=False,
            temperature=0.2,
            max_tokens=450,
        )
        data = parse_json(raw)
        dims_out = []
        for d in data.get("dimensions", [])[:5]:
            dims_out.append({
                "name": str(d.get("name", ""))[:40],
                "score": max(0, min(20, int(d.get("score") or 0))),
                "note": str(d.get("note", ""))[:160],
            })
        if not dims_out:
            raise ValueError("no dimensions parsed")
        overall = sum(d["score"] for d in dims_out)
        return {
            "overall": overall,
            "max_overall": len(dims_out) * 20,
            "dimensions": dims_out,
            "feedback": str(data.get("feedback", ""))[:400],
        }
    except Exception:
        # Deterministic fallback: credit structure keywords per framework step.
        words = response.lower()
        hints = {
            "Identify": ["identify", "root cause", "impact", "scope", "stakeholder"],
            "Assess": ["assess", "severity", "risk", "quantify", "measure", "estimate"],
            "Prioritize": ["priorit", "critical path", "first", "urgent", "rank"],
            "Mitigate": ["mitigat", "control", "prevent", "reduce", "remediat"],
            "Monitor": ["monitor", "kpi", "metric", "review", "dashboard", "cadence"],
        }
        dims_out = []
        for name in case["framework"]:
            hit = any(k in words for k in hints.get(name, []))
            dims_out.append({
                "name": name,
                "score": 12 if hit else 5,
                "note": "step addressed" if hit else "not clearly addressed",
            })
        return {
            "overall": sum(d["score"] for d in dims_out),
            "max_overall": len(dims_out) * 20,
            "dimensions": dims_out,
            "feedback": "Offline structural estimate - connect each step explicitly for full credit.",
        }


@router.post("/cases/{case_id}/submit")
async def submit_case(
    case_id: str, req: SubmitCase, user=Depends(get_current_user)
):
    """Submit a case response; graded against the consulting framework."""
    case = next((c for c in CASE_STUDIES if c["case_id"] == case_id), None)
    if not case:
        raise HTTPException(status_code=404, detail="Unknown case")

    grade = await _grade_case(case, req.response)
    pct = grade["overall"] * 100 // max(grade.get("max_overall", 100), 1)

    try:
        await record_practice(user["id"], "case_study", pct, metadata={
            "source": "big_four",
            "case_id": case_id,
        })
    except Exception:
        pass

    return {"case_id": case_id, "title": case["title"], **grade}


@router.get("/sql/meta")
async def sql_meta():
    topics = sorted({q["topic"] for q in SQL_QUESTIONS})
    return {"total": len(SQL_QUESTIONS), "topics": topics}


@router.get("/sql/questions")
async def sql_questions(count: int = 8, topic: str = ""):
    pool = [q for q in SQL_QUESTIONS if not topic or q["topic"] == topic]
    import random

    n = min(max(count, 1), len(pool))
    picked = random.sample(pool, n)
    return {
        "questions": [
            {k: q[k] for k in ("id", "topic", "question", "options")} for q in picked
        ]
    }


@router.post("/sql/check")
async def sql_check(req: CheckSql, user=Depends(get_current_user)):
    q = next((q for q in SQL_QUESTIONS if q["id"] == req.question_id), None)
    if not q:
        raise HTTPException(status_code=404, detail="Unknown question")
    correct = req.answer.strip().lower() == q["correct_answer"].strip().lower()
    return {
        "correct": correct,
        "correct_answer": q["correct_answer"],
        "explanation": q["explanation"],
    }


class SqlComplete(BaseModel):
    correct: int
    total: int


@router.post("/sql/complete")
async def sql_complete(req: SqlComplete, user=Depends(get_current_user)):
    if req.total <= 0:
        raise HTTPException(status_code=400, detail="Invalid totals")
    pct = int(req.correct * 100 / req.total)
    try:
        await record_practice(user["id"], "aptitude", pct, metadata={
            "source": "big_four_sql",
            "drill": "consul_sql_screening",
        })
    except Exception:
        pass
    return {"recorded": True, "accuracy_pct": pct}
