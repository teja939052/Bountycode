# Service-company preparation: source-backed blueprint map

**Checked:** 10 November 2026  
**Scope:** Indian graduate / early-career recruitment preparation. This is a preparation map, not a claim to possess any employer's private test bank.

## Evidence levels used by Bountycode

- **Official-current:** The employer currently publishes the named section or stage on an official careers/recruitment page.
- **Official-role-dependent:** The employer confirms assessments, but says the content or process varies by role or drive.
- **Pattern-relevant:** A learning skill is a reasonable preparation target for a published broad category. It is not a claim that the employer asks this exact item.
- **Unverified:** We have not found a sufficiently current primary source. Keep the area as general preparation; do not publish exact timings, counts or weights.

## Employer map

| Employer / programme | What current public evidence supports | What Bountycode should provide | What we must not claim |
|---|---|---|---|
| **TCS All India NQT (2026 batch)** | Official TCS page describes a 190-minute integrated test: Foundation 75 minutes (Numerical, Verbal, Reasoning; 25 minutes each) and Advanced 115 minutes (Advanced Quantitative & Reasoning 25 minutes, Advanced Coding 90 minutes). Advanced is mandatory for Digital/Prime consideration. | Foundation numerical, verbal and reasoning; advanced quantitative reasoning; timed coding; then role/skill-aware technical interview preparation. Maintain a dated 2026 blueprint version. | Do not call the full pattern universal to every TCS drive, BPS role or year. Do not invent a separate pseudocode section in this published NQT blueprint. |
| **Accenture India** | Official recruitment guidance says technical assessments are role/experience aligned and may evaluate problem solving, logical reasoning, applied technical knowledge and coding in an engineering environment. Most assessments take about 30–90 minutes; the candidate's invitation is definitive. | Logical/problem-solving drills, applied technical scenarios, role-specific coding, debugging and communication. Allow blueprint variants by role. | Do not publish fixed counts, section order or a universal Accenture paper. |
| **Cognizant GenC** | Official GenC page says assessments vary by role and may cover communication, aptitude and/or technical skills. | Communication, aptitude and technical foundations as configurable components; role-specific interview and project explanation. | Do not imply every GenC candidate receives every section or a fixed number of questions. |
| **HCLTech AMP / Ascend** | Official campus-hiring page describes cognitive testing (Numerical, Verbal, Reasoning; approximately 90 minutes), Coding/Technical (60–90 minutes) and Versant English speaking/listening. | Cognitive drills, practical coding/technical basics, spoken English practice and interview readiness. | Do not treat approximate stage durations as a contract for every hiring event or AMP tier. |
| **Wipro Elite** | Official Early Careers page confirms Elite as a technical graduate hiring programme, but the source reviewed does not establish a universal current section count or test duration. | General quantitative, reasoning, verbal, programming logic, coding and technical fundamentals; enable drive-specific overrides when a current invite or official notice is available. | Do not publish precise timing, question counts or a fixed section sequence without a dated primary source. |
| **Infosys** | Official HackWithInfy 2026 material describes a distinct coding competition with a three-hour Round 1, a three-hour Round 2 and a grand finale. This is not the same as every Infosys fresher hiring route. | Build coding depth and problem solving. Keep a separate HackWithInfy competition blueprint, clearly named and versioned, rather than using it as a proxy for all graduate hiring. | Do not label HackWithInfy rounds as the universal Infosys campus OA. |
| **Capgemini India** | Official recruitment process says proctored technical and language assessments may apply, followed by role-dependent technical interviews; one or two technical interviews may be conducted depending on the position. | Technical fundamentals, language/communication practice, coding and interview preparation with configurable stages. | Do not claim exact section counts or a single universal fresher assessment. |
| **Tech Mahindra** | The current primary-source search in this audit did not establish an authoritative, current universal campus-test pattern. Older candidate manuals/reports are dated and should be treated as anecdotal. | General cognitive, coding and technical preparation; add a dated drive-specific overlay only when a current official notice is collected. | Do not publish old timing/count information as a current guarantee. |
| **LTIMindtree** | No sufficiently specific current primary-source campus blueprint was verified in this audit. | Shared service-company core: aptitude, reasoning, verbal, coding and CS fundamentals. | Do not invent an LTIMindtree-only paper or section weights. |

## Shared curriculum for service-company readiness

The following is Bountycode's **cross-company preparation curriculum**, not a claim that every employer assesses all of it in one test.

1. **Quantitative aptitude:** percentages, successive change, ratio/proportion, averages, profit/loss, time & work, speed/distance, mixtures, interest, probability, permutations/combinations and data interpretation.
2. **Logical reasoning:** series, syllogisms, coding-decoding, directions, blood relations, arrangements, statement/conclusion, data sufficiency and constraint reasoning.
3. **Verbal and communication:** grammar, sentence correction, reading comprehension, inference, para-jumbles, vocabulary-in-context, concise email writing, spoken clarity and professional updates.
4. **Programming logic / pseudocode:** variable-state tables, operators, conditions, loops, nested loops, arrays/strings, functions, parameter passing, recursion basics and debugging. This is a Bountycode learning differentiator, but should only be placed in a company blueprint when a source supports that section.
5. **Coding / service-level DSA:** arrays, strings, hashing, sorting/searching, two pointers, sliding window, stacks/queues, linked lists, trees basics, complexity and implementation/testing discipline.
6. **CS / engineering foundations:** OOP, DBMS, SQL, operating systems, computer networks, HTTP/API basics, Git, SDLC, testing, debugging, security basics and practical cloud/DevOps vocabulary appropriate to the role.
7. **Interview readiness:** project walkthrough, problem-solving explanation, technical fundamentals, behavioral examples and role-specific communication. Rubric-based answers must be evaluated against observable criteria rather than generated confidence scores.

## Storage and interoperability direction

Bountycode already has a canonical Learning Object model in backend/app/content/learning_object.py and versioned file-based content. Reuse it. Do not create a third playable registry or move question text, answers or test cases into MongoDB.

Keep these layers distinct:
- **Content artifact:** immutable item/lesson ID, version, skill/pattern, learning objective, question/task, answer/rubric, worked explanation, hints, misconception targets and transfer task.
- **Assessment composition:** versioned company/programme blueprint, section, item IDs, timing, selection rules, scoring policy and publication date.
- **Provenance/trust:** exact source URL and checked date for employer claims; synthetic/canonical/candidate-reported label for items; separate automated-validation evidence and human reviewer evidence.
- **Learner evidence:** attempts, responses, result, timing, hints, rubric breakdown, event context and content version. Store this as learner state/telemetry, not as question content.

1EdTech QTI provides an established interchange model for assessment items, tests/sections and results between item banks, authoring tools, delivery systems and scoring systems. ADL xAPI provides a well-known event model for describing learning experiences with actor, verb, object, result and context. Bountycode should remain on its existing internal schema for now and consider QTI/xAPI adapters only when interoperability is required.

## Versioning rules

- Blueprint ID is stable; each blueprint revision increments version.
- Record effective_from, last_verified_at, source_urls, scope and confidence.
- A source update creates a new blueprint version; it does not silently rewrite historical attempts.
- Each attempt stores the blueprint version and content item versions used.
- Exact company-question provenance is not inherited from a topic tag.
- When the public source only establishes broad skills, use pattern_relevant and explain the basis.
- When evidence is absent, use unverified and do not infer a company-specific format.

## Source register

1. TCS — [All India NQT Hiring, 2026 batch](https://www.tcs.com/careers/india/tcs-all-india-nqt-hiring) — official section names and timing.
2. Accenture — [Recruitment process and technical assessments](https://www.accenture.com/in-en/careers/explore-careers/area-of-interest/journey-to-accenture) — role/experience-dependent assessment scope and typical duration.
3. Cognizant — [GenC programme](https://careers.cognizant.com/india-en/pathways-to-cognizant/genc-program) — assessment scope may include communication, aptitude and/or technical skills depending on role.
4. HCLTech — [Campus Hiring / AMP](https://www.hcltech.com/careers/campus-hiring) — Ascend test stages and approximate durations.
5. Wipro — [Early Careers](https://careers.wipro.com/content/Early-Careers/) — confirmation of Elite as a technical graduate hiring programme.
6. Infosys — [HackWithInfy](https://www.infosys.com/careers/hackwithinfy.html) and [2026 terms](https://www.infosys.com/careers/hackwithinfy/2026/hwi-terms-conditions.pdf) — a separately scoped coding competition.
7. Capgemini — [India recruitment process](https://www.capgemini.com/in-en/careers/join-capgemini/recruitment-process/) — assessments and interviews vary by position.
8. 1EdTech — [QTI specification](https://www.1edtech.org/standards/qti/index) — assessment item/test/result interoperability.
9. ADL — [xAPI statement data model](https://github.com/adlnet/xAPI-Spec/blob/master/xAPI-Data.md) — learning experience event representation.

**Audit boundary:** Sources checked 10 November 2026. This is a snapshot, not a perpetual guarantee. Re-check before publishing a future drive blueprint.
