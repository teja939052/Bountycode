# Service Company Coverage Matrix

**Commit:** 6703c4e004377f3a7bf51058e7e9732475a52da4
**Date:** 2026-11-18

## Company Blueprints (6 companies)

| Company | Blueprint ID | Pathways | Assessment Stages |
|---------|-------------|----------|-------------------|
| TCS | tcs_nqt | Ninja, Digital, Prime | Foundation, Advanced Aptitude, Advanced Coding |
| Infosys | infosys | Systems Engineer, Specialist Programmer | Aptitude, Coding, Behavioral |
| Wipro | wipro_nlth | ELITE, Turbo | Aptitude, Coding, Written Communication |
| Accenture | accenture | Associate, Application Developer | Cognitive, Coding, Communication |
| Capgemini | capgemini | Associate, Analyst | Aptitude, Pseudocode, Behavioral |
| IBM | ibm | Associate System Engineer, Application Developer | Cognitive, Coding, Technical |

## Company Role Packages (6 packages)

| Package ID | Name | Worlds | Emphasis | Hours |
|------------|------|--------|----------|-------|
| tcs | TCS NQT Preparation | foundations, aptitude_quant, aptitude_reasoning, aptitude_verbal, problem_solver, under_pressure, hiring_arena | Aptitude, reasoning, verbal, coding | 100 |
| infosys | Infosys Preparation | foundations, aptitude_quant, aptitude_reasoning, aptitude_verbal, problem_solver, communication, hiring_arena | Aptitude, coding, behavioral | 90 |
| wipro | Wipro NLTH Preparation | foundations, aptitude_quant, aptitude_reasoning, aptitude_verbal, problem_solver, communication, hiring_arena | Aptitude, coding, written comm | 80 |
| accenture | Accenture Preparation | foundations, aptitude_quant, aptitude_reasoning, aptitude_verbal, problem_solver, communication, cs_fundamentals, hiring_arena | Cognitive, coding, CS fundamentals | 100 |
| capgemini | Capgemini Preparation | foundations, aptitude_quant, aptitude_reasoning, aptitude_verbal, problem_solver, communication, hiring_arena | Pseudocode, behavioral | 80 |
| ibm | IBM Preparation | foundations, aptitude_quant, aptitude_reasoning, aptitude_verbal, problem_solver, cs_fundamentals, sql_dbms, hiring_arena | CS fundamentals, SQL | 90 |

## Shared Foundation (One Engine, Company Overlays)

All company packages reuse the same canonical worlds:
- **Foundations** — programming basics (all companies)
- **Aptitude worlds** — quant, reasoning, verbal (all service companies)
- **Problem solver** — DSA coding (all companies)
- **Communication** — spoken English, email, group discussion, behavioral (Infosys, Wipro, Accenture, Capgemini)
- **CS Fundamentals** — OS, networks, OOP, complexity (Accenture, IBM)
- **SQL/DBMS** — querying and design (IBM)

## Coverage Targets (Not Yet Implemented)

| Company | Status | Notes |
|---------|--------|-------|
| Cognizant (GenC) | Not implemented | Can use same pattern as existing packages |
| HCLTech | Not implemented | Can use same pattern |
| Tech Mahindra | Not implemented | Can use same pattern |
| Mphasis | Not implemented | Can use same pattern |
| Hexaware | Not implemented | Can use same pattern |
| Persistent Systems | Not implemented | Can use same pattern |

**Design principle:** One canonical skill taxonomy across all companies. A skill (e.g., `dsa.arrays`) is not duplicated per employer. Company-specific overlays only change emphasis, weighting, and assessment structure — never the underlying curriculum.
