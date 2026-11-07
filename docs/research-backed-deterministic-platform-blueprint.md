# Bountycode research-backed deterministic platform blueprint

## Product decision

Bountycode should prepare learners for service-company hiring without pretending that one permanent exam pattern exists. Official employer pages show that TCS, Infosys, Wipro, Accenture, Cognizant and Capgemini vary by hiring cycle, role, cohort, campus route and invitation. Therefore every company pathway must be a versioned assessment profile with a source URL, effective date, confidence level and last-verified timestamp.

The stable product is not a leaked-paper simulator. It is a deterministic competency system that teaches observable skills, schedules retrieval, serves equivalent assessment forms, scores with auditable rules and explains the evidence behind every readiness recommendation.

## The canonical learning loop

```text
profile and target pathway
  -> baseline diagnostic
  -> canonical competency graph
  -> prerequisite lesson
  -> guided example
  -> independent practice
  -> spaced retrieval
  -> timed company-form assessment
  -> server scoring and evidence snapshot
  -> misconception diagnosis
  -> repair mission
  -> delayed equivalent retest
  -> mastery and readiness update
```

The curriculum graph must distinguish formative practice from summative assessment. XP, streaks and badges can motivate practice, but they must not raise a mastery claim. Mastery requires independent performance, time evidence, transfer to an unseen item and successful delayed retrieval.

## Deterministic assessment rules

Each question must carry a canonical skill ID, observable subskill, difficulty, task type, prerequisites, explanation, hint ladder, misconception tags, provenance and trust status. Each assessment must carry a purpose, blueprint version, skill weights, time limit, form seed, scoring rules and interpretation. The same evidence snapshot plus the same seed must produce the same form; a different seed may produce an equivalent form from the same approved pool.

The first implementation tranche adds an evidence-first quiz composer. It prioritizes weak skills, due reviews, target skills and target-company matches, balances unseen exposure and prevents one skill from consuming the entire form. The selection evidence is stored with the quiz session so the learner and the system can explain why each question appeared.

## Employer pattern policy

TCS All India NQT 2026 publishes a 75-minute Foundation section and a 115-minute Advanced section, but TCS iON publishes other NQT variants with different durations and counts. Store these as separate profiles.

Infosys HackWithInfy 2026 officially describes two individual three-hour coding assessments and a team-based finale, while current public InfyTQ counts are not stable enough to become a universal default.

Wipro's employer-hosted WILP and National Talent Hunt pages show different eligibility and assessment routes. Accenture's official material describes role- and campaign-dependent online assessments, usually completed in one sitting. Cognizant GenC and Capgemini official pages also describe conditional, role- or drive-dependent stages rather than one universal paper.

The platform must show "official current", "official historical", "secondary reported" or "unknown" beside employer metadata. Unknown question counts and cutoffs remain unknown. A practice score never becomes an offer probability.

## Learning science and quality gates

The platform should use spaced retrieval, interleaving, actionable feedback, worked examples, self-explanation and delayed retesting. Feedback must identify the failing concept or test, give a minimal repair, and require the learner to act on it. Content release should block malformed debugging/API/SQL scenarios, missing answer keys, duplicate items and untraceable sources.

## Priority roadmap

1. Canonicalize every lesson, quiz item, diagnostic question, OA section and repair mission into one competency namespace.
2. Make quiz composition evidence-driven and reproducible.
3. Add concept-level misconception tags and repair/retest policies.
4. Keep company profiles versioned and provenance-aware.
5. Add hidden-test coding, SQL execution, debugging, communication and STAR rubrics as independent assessment types.
6. Validate content quality and lesson-link integrity in CI.
7. Measure outcomes: first-attempt accuracy, delayed retention, transfer, weakness recovery, independent mastery and company-form readiness.

## References

[1]: https://www.tcs.com/careers/india/tcs-all-india-nqt-hiring "TCS All India NQT hiring page"
[2]: https://www.tcsion.com/hub/national-qualifier-test/it-career-readiness-pack/ "TCS iON IT career readiness pack"
[3]: https://www.infosys.com/careers/hackwithinfy.html "Infosys HackWithInfy"
[4]: https://www.infosys.com/careers/hackwithinfy/2026/hwi-terms-conditions.pdf "HackWithInfy 2026 terms"
[5]: https://app.joinsuperset.com/company/wipro/wilp.html "Wipro WILP employer-hosted process"
[6]: https://app.joinsuperset.com/company/wipro/nth.html "Wipro National Talent Hunt employer-hosted process"
[7]: https://www.accenture.com/in-en/careers/explore-careers/area-of-interest/journey-to-accenture "Accenture assessment FAQ"
[8]: https://careers.cognizant.com/india-en/pathways-to-cognizant/genc-program/ "Cognizant GenC program"
[9]: https://app.joinsuperset.com/company/cognizant/GenC-2026-OnCampus.html "Cognizant GenC 2026 campus listing"
[10]: https://www.capgemini.com/in-en/careers/join-capgemini/recruitment-process/ "Capgemini India recruitment process"
[11]: https://ies.ed.gov/ncee/wwc/practiceguide/1 "IES practice guide on organizing instruction and study"
[12]: https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/feedback "EEF feedback evidence"
[13]: https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/metacognition-and-self-regulation "EEF metacognition and self-regulation evidence"
[14]: https://www.aera.net/About-AERA/AERA-Rules-Policies/Association-Policies/Position-Statement-on-High-Stakes-Testing/mid/16176/dnnprintmode/true?SkinSrc=%5BG%5DSkins%2F_default%2FNo%20Skin%26ContainerSrc=%5BG%5DContainers%2F_default%2FNo%20Skin "AERA high-stakes testing validity statement"
