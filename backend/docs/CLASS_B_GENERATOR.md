# Class B Aptitude/Reasoning/Verbal Question Generator

## Pipeline Overview

```
Request (category, count, difficulty)
        ↓
1. Generate batch with worked_solution + trick + trap
        ↓
2. For each question:
   a. Independent re-solve × 2 (no proposed answer in context)
   b. Agreement gate: all re-solves must agree on A/B/C/D
   c. Re-solve answer must match proposed correct_answer
   d. Numeric check if answer is numeric
   e. Quality score ≥ 60
        ↓
3. Spot-check 10% of batch (structural check)
        ↓
4. Quality report: promoted/rejected/reasons
        ↓
5. Admin review → promote to verified pool
```

## Acceptance Criteria

| Gate | Requirement |
|------|-------------|
| Agreement | 2/2 independent re-solves agree on same option |
| Answer match | Re-solve answer == proposed correct_answer |
| Numeric | If numeric, re-computed value matches within tolerance |
| Quality score | ≥ 60/100 |
| Structural | No missing fields, 4 options, valid correct_answer |
| Spot-check | 10% sample passes structural check |
| Pass rate | ≥ 70% of batch promoted |

## Generation Prompt (Few-Shot)

```
You are an elite aptitude test question writer for Indian campus placement preparation.

Output exactly 5 questions in this JSON format:

[
  {
    "question_id": "generated:quant:easy:0",
    "question_type": "aptitude",
    "category": "quant",
    "difficulty": 2,
    "topic": "percentages",
    "subtopic": "percentage-change",
    "question": "If a number is increased by 20% and then decreased by 20%, what is the net change?",
    "options": {
      "A": "0%",
      "B": "4% decrease",
      "C": "4% increase",
      "D": "20% decrease"
    },
    "correct_answer": "B",
    "worked_solution": "Start with 100. +20% → 120. -20% of 120 = 24. Final = 120-24 = 96. Net change = 96-100 = -4, so 4% decrease.",
    "trick": "Same percent up then down is NOT zero — use multiplying factors: 1.2 × 0.8 = 0.96",
    "trap": "Students think +20% then -20% cancels out. It doesn't because the base changes.",
    "explanation": "Successive percentage changes multiply: (1+p/100)(1-p/100) = 1 - (p/100)², so there is always a net decrease.",
    "time_benchmark_s": 30,
    "company_tags": ["TCS", "Infosys", "Wipro"]
  }
]

Rules:
- Worked solution must show every step with numbers
- Trick must be a named technique students can practice
- Trap must explain the most common wrong path
- Options A-D must be plausible
- Return ONLY the JSON array
```

## Re-Solve Verifier Prompt

```
You are an independent verifier. Solve this question yourself.

Question: {question}
Options:
A: {opt_a}
B: {opt_b}
C: {opt_c}
D: {opt_d}

Proposed answer: {proposed}

Work through it step by step. State your final answer as exactly one of: A, B, C, or D.

Return JSON:
{"answer": "<A|B|C|D>", "confidence": <0-100>, "steps": "<brief>"}
```

## Numeric Verification

```
Question: {question}
Expected answer: {expected}
Proposed numeric answer: {proposed}

Re-compute the answer from scratch. Return JSON:
{"correct": true/false, "expected": <number>, "proposed": <number>}
```

## Sympy Check Harness (for numeric questions)

```python
import re
import sympy

def sympy_check(question_text: str, expected: float, proposed: float) -> bool:
    """Use sympy to verify numeric answers where possible."""
    # Extract numbers and expressions from question
    # Try to parse as sympy expression
    # Evaluate and compare with tolerance
    try:
        # Example: "What is 15% of 200?"
        # Extract "15% of 200" → 0.15 * 200
        expr = re.sub(r'(\d+)%', r'(\1/100)', question_text)
        # This is a simplified example; real implementation would be more robust
        result = sympy.sympify(expr)
        return abs(float(result) - expected) < 1e-6
    except Exception:
        return abs(expected - proposed) < 1e-6
```

## Batch Execution

```python
from app.services.class_b_generator import generate_batch, verify_batch

# 1. Generate
questions = await generate_batch(
    category="quant",
    question_type="aptitude",
    count=20,
    difficulty=3,
)

# 2. Verify
report = await verify_batch(questions)

# 3. Review report
print(f"Pass rate: {report['pass_rate']:.0%}")
print(f"Passed: {report['passed']}/{report['total']}")
print(f"Rejection reasons: {report['rejection_reasons']}")

# 4. Promote if pass rate ≥ 70%
if report["pass_rate"] >= 0.70:
    from app.services.content_promotion import promote_questions
    promotion = promote_questions([q for q in questions if q.trust_status == "reviewed"])
    print(f"Promoted: {promotion['promoted']}")
```

## Admin Endpoints

```
POST /api/v1/admin/questions/generate
  body: { category, question_type, count, difficulty }
  returns: { generated, questions }

POST /api/v1/admin/questions/verify
  body: { questions, spot_check_fraction }
  returns: quality report

POST /api/v1/admin/questions/promote
  body: { questions, reviewer_id }
  returns: promotion report

GET /api/v1/admin/questions/pipeline
  returns: { agreement_required, pass_threshold, spot_check_fraction }
```

## Failure Mode Recovery

If pass rate < 70%:
1. Inspect `rejection_reasons` in report
2. Common issues:
   - Re-solve disagreement → question ambiguous or multiple valid answers
   - Answer mismatch → proposed answer is wrong, regenerate
   - Numeric check fail → arithmetic error in worked solution
   - Low quality score → missing trick/trap/solution
3. Fix prompt or regenerate with stricter constraints
4. Re-run verification

## Target Topics (Week 1)

Priority order for Time & Work batch:
1. Basic time-work (A alone, B alone, together)
2. Pipes and cisterns
3. Work and wages
4. Alternating work
5. Group work efficiency
6. Efficiency ratios
7. Work with removal/leakage
8. Mixed work problems
9. Time-work-distance coupling
10. Comparative work rates

Each topic: 6 questions (4 easy, 2 medium) = 60 total.
