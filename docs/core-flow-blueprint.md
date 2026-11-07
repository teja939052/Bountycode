# Bountycode core placement-preparation flow

This blueprint translates current employer information and learning evidence into a deterministic, low-cost product direction for Indian service-company placement preparation.

## Product rules

Bountycode should separate verified employer or drive facts from product recommendations. Every volatile assessment pattern needs an employer, edition/cohort, effective date, source URL, and confidence label. TCS, Infosys, Wipro, Accenture, and Cognizant all vary by drive, role, cohort, or invitation; the platform must not present one universal syllabus, cutoff, duration, or job guarantee.

The core learner model should be explainable. Track per-competency accuracy, response time, difficulty, recency, confidence, hint use, misconception tags, practical-task performance, and employer-format exposure. Select the next activity using weakest actionable skills, due spaced review, and periodic mixed transfer assessments. Mastery should require repeated success across variants plus delayed recheck. XP, streaks, and levels are engagement signals, not competence evidence.

The core path must work without generative AI or an expensive hosted compiler. Use human-authored items, fixed answer keys, rule-based feedback, output tracing, pseudocode, debugging, SQL validation, test-case design, and optional local or lightweight execution.

## Core flow

1. Onboarding captures target employer(s), target role, assessment track, assessment date, available time, days per week, language, device, accessibility needs, runtime availability, learning preference, and consent.
2. A 10–15 minute diagnostic samples aptitude, verbal, reasoning, programming, SQL, and core CS with easy, medium, and edge-case items. Store correctness, timing, hints, confidence, and error tags.
3. The plan produces a level path: Orientation, Foundations, Core Skills, Applied Readiness, Timed Performance, and Interview Ready.
4. Daily learning combines foundational repair, concept lesson, guided and independent practice, spaced review, and employer-format assessment when readiness is sufficient.
5. After each attempt, show competency evidence and explain the next action. Retake diagnostics and transfer assessments update the plan.
6. Employer mocks are configurable and dated. TCS Foundation and Advanced, Infosys InfyTQ and HackWithInfy, Wipro WILP/NTH, Accenture campus, and Cognizant GenC must be separate tracks with variability warnings.
7. Application and operational checklists track official-channel verification, eligibility, documents, assessment invitation, interview, offer/LOI, pre-skilling, and joining status separately.

## Research-backed assessment direction

The cited TCS All India NQT drive describes a 75-minute Foundation section and a 115-minute Advanced section, with Advanced coding for Digital/Prime aspiration in that drive. HackWithInfy 2026 describes three-hour individual coding rounds. Wipro WILP describes an 80-minute assessment followed by a 20-minute voice assessment. Accenture and Cognizant explicitly emphasize role- or invitation-dependent variation, so their detailed configurations must remain editable and invitation-driven.

Retrieval practice, actionable feedback, formative assessment, and aligned outcomes support the diagnostic → practice → feedback → delayed review loop. A 2026 gamification study found that points and progress bars increased reported motivation but did not improve delayed recall, so gamification should support the evidence loop rather than replace it.

## Sources

- [1]: https://www.tcsion.com/hub/national-qualifier-test/ "TCS iON National Qualifier Test"
- [2]: https://www.tcs.com/careers/india/tcs-all-india-nqt-hiring "TCS All India NQT Hiring"
- [3]: https://www.infosys.com/careers/hackwithinfy.html "Infosys HackWithInfy"
- [4]: https://www.infosys.com/careers/hackwithinfy/2026/hwi-terms-conditions.pdf "HackWithInfy 2026 Terms"
- [5]: https://app.joinsuperset.com/company/wipro/wilp.html "Wipro WILP cohort assessment"
- [6]: https://app.joinsuperset.com/company/wipro/nth.html "Wipro NTH cohort assessment"
- [7]: https://www.accenture.com/in-en/careers/explore-careers/area-of-interest/journey-to-accenture "Accenture assessment guidance"
- [8]: https://careers.cognizant.com/india-en/pathways-to-cognizant/genc-program/ "Cognizant GenC program"
- [9]: https://ctl.wustl.edu/resources/using-retrieval-practice-to-increase-student-learning/ "Washington University retrieval practice"
- [10]: https://educationendowmentfoundation.org.uk/education-evidence/teaching-learning-toolkit/feedback "Education Endowment Foundation feedback evidence"
- [11]: https://teaching.cornell.edu/teaching-resources/assessment-evaluation/measuring-student-learning "Cornell formative assessment guidance"
- [12]: https://research-portal.uu.nl/ws/portalfiles/portal/277804433/1-s2.0-S0747563225003097-main.pdf "2026 adaptive retrieval and gamification study"

## Assessment runtime implemented in the next tranche

The OA runtime now versions every attempt with an engine and blueprint version, keeps server-side answer persistence, and returns section-level deterministic evidence. The browser additionally stores an active attempt envelope and per-session state so a reload can restore questions, section position, answers, timing state, and review flags when storage is available. Learners can flag questions for review, see an autosave indicator, and send review/resume metadata with completion. The server stores this metadata with the result and continues to emit section and overall learning events for readiness and repair missions.
