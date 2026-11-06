# Bountycode Learning Experience Standard

**Status:** Product and content standard  
**Audience:** Product, curriculum authors, frontend, backend and QA  
**Primary learner:** A beginner preparing for service-company and entry-level software roles

## 1. Product promise

Bountycode should take a learner from their current knowledge to demonstrable placement readiness through one coherent learning system.

The Academy is the learner's source of truth for:
- what to learn next;
- why it is next;
- what evidence proves a skill;
- what needs revision;
- how a target company's assessment maps to the underlying skills.

Journey and game systems motivate progress. They must not create a competing curriculum or a second definition of mastery.

## 2. Curriculum architecture

Use two connected layers rather than duplicating lessons for each employer.

### Universal skill curriculum
Canonical concepts and lessons for:
- programming fundamentals and code reading;
- C, C++, Java and Python fundamentals;
- data structures, algorithms and complexity;
- quantitative aptitude;
- logical and analytical reasoning;
- verbal ability and workplace communication;
- SQL, DBMS, operating systems and computer networks;
- debugging, Git, command line and practical software habits.

### Employer assessment overlays
A target such as TCS NQT, Infosys, Wipro or Accenture maps its assessment modules onto canonical skills. Each employer overlay should store:
- employer and assessment-track identifier;
- assessment section and topic;
- canonical skill/concept IDs;
- format and duration, when verified;
- source URL, verification date and version;
- whether the mapping is confirmed, inferred or awaiting review.

Do not fork a separate copy of a lesson for every company. A learner should master a concept once, then practise the employer-specific format.

Company patterns change. Do not present an old pattern, duration or eligibility rule as universal. Mark the source and last verification date.

## 3. Required lesson anatomy

A beginner-facing lesson should normally follow this sequence:

1. **Outcome:** State what the learner will be able to do.
2. **Prerequisite check:** Confirm the few concepts needed to understand this lesson.
3. **Explain:** Teach one small idea in plain language, with a mental model or analogy.
4. **Worked example:** Demonstrate the solution step by step and narrate the decisions.
5. **Guided retrieval:** Ask the learner to predict, recall or choose before revealing feedback.
6. **Deliberate practice:** Ask the learner to apply the idea, not merely recognize a definition.
7. **Transfer:** Change the numbers, context, input or constraint so the learner must use the concept again.
8. **Mastery check:** Use a fresh assessment that is not a copy of the worked example.
9. **Next action:** Explain whether to progress, practise a prerequisite or schedule revision.

Not every lesson needs every interaction type. The sequence should fit the learning objective and avoid unnecessary interaction for its own sake.

## 4. Supported interactive exercise patterns

Use a varied exercise mix:

- multiple choice for quick concept checks;
- typed answers for numeric, textual or SQL outputs;
- predict-the-output code tracing;
- fill-in-the-blank code completion;
- debugging and error identification;
- step ordering and algorithm sequencing;
- variable tables and dry-run traces;
- runnable code with hidden test cases;
- short projects that combine several skills;
- timed company-format quizzes and mocks.

A lesson with code should progress from reading code, to tracing it, to completing it, to writing and testing code independently. Code-tracing exercises are not a substitute for a real compiler-backed coding task.

## 5. Feedback rules

Feedback should help the learner repair their mental model.

- Tell the learner whether the response is correct.
- Explain the exact reasoning, not only the answer.
- For common mistakes, identify the likely misconception.
- Use progressive hints: point to the concept, narrow the location, then give a stronger clue.
- Do not reveal final assessment answer keys before submission.
- Allow a learner to revisit an explanation and retry after remediation.
- Distinguish a first-attempt result from eventual mastery after practice.

A wrong answer is useful evidence, not a reason to punish the learner or hide the next step.

## 6. Personalization and adaptive progression

Recommendations should use evidence, not arbitrary randomness.

Capture, where available:
- concept and prerequisite IDs;
- correctness and assessment score;
- question difficulty and format;
- attempts and recency;
- time taken;
- hints used;
- whether performance transfers to a new question;
- spaced-review success or lapse;
- the learner's target employer, role and expected assessment date;
- the learner's daily time budget and accessibility preferences.

The adaptive engine should:
1. preserve prerequisite order;
2. surface overdue reviews at an appropriate point;
3. identify the highest-impact unfinished skill for the selected target;
4. adapt difficulty within a learner's productive challenge range;
5. provide extra worked examples or smaller steps after repeated errors;
6. interleave related skills after foundational understanding;
7. schedule revision based on recall performance;
8. explain why a task was recommended.

Do not label a concept mastered from a single lucky multiple-choice response. Require repeated and varied evidence, and retain confidence/attempt counts alongside a mastery estimate.

## 7. A useful daily learning session

A default 30-minute session can be:
- 5 minutes: due retrieval and spaced review;
- 10 minutes: new teaching and a worked example;
- 10 minutes: deliberate practice and a code/aptitude challenge;
- 5 minutes: a mixed recall check and reflection.

The daily plan should scale to shorter and longer time budgets. Do not let streak mechanics make the learner complete low-value tasks just to preserve a streak.

## 8. Service-company preparation

Company preparation should connect skills to assessment behaviour.

For example, TCS's published NQT pattern for the cited hiring cycle separated Foundation (Numerical, Verbal and Reasoning) and Advanced (Advanced Quantitative/Reasoning and Coding) sections. Keep the track versioned and re-check the official hiring page before publishing any new cycle details.

Accenture describes technical assessments as evaluating applied problem-solving, logical reasoning, technical knowledge and coding in job-relevant scenarios. Company mocks should test application, not memorization of leaked or purportedly exact questions.

Build readiness from:
- topic mastery;
- first-attempt and final mastery results;
- timed section accuracy;
- coding tests passed;
- explanation quality and communication performance;
- consistency on unseen mixed questions.

Never imply a readiness percentage guarantees selection.

## 9. Accessibility and learner control

Every learning flow should support:
- keyboard-only navigation and visible focus;
- semantic headings, labels and feedback announcements;
- readable contrast, zoom and responsive layouts;
- reduced-motion preferences;
- clear code font and copyable code;
- useful loading, retry and offline states;
- progress recovery after accidental navigation or connection loss;
- no forced countdown for ordinary learning;
- optional language support without changing the meaning of technical terms.

Keep lesson checkpoints lightweight. A temporary save failure should not block a learner from continuing.

## 10. Content quality gate

Before publishing a lesson, verify:
- the learning outcome is observable;
- prerequisites are satisfied;
- examples are correct and independently checked;
- answer keys are valid and kept server-side;
- every interactive item has a useful explanation;
- typed answers define normalization and accepted alternatives when needed;
- code samples have deterministic expected outputs;
- assessments test transfer and do not simply repeat the lesson;
- the company-topic mapping actually matches the taught skill;
- the lesson is accessible and readable on mobile;
- a human reviewer has checked factual and editorial quality.

Structural tests are necessary but are not a substitute for subject-matter review.

## 11. What to measure

Prioritize learning outcomes over vanity metrics.

- time to first successful independent solve;
- first-attempt accuracy and eventual mastery;
- delayed recall after 7 and 30 days;
- performance on unseen transfer questions;
- coding submissions passing hidden tests;
- repeated misconception rate;
- lesson-step drop-off and resume success;
- time spent per mastered concept;
- mock section score and calibration against later performance.

Treat lesson completion, XP and streaks as engagement measures, not proof of learning.

## 12. References used for the design

- Coddy: https://coddy.tech/ — roadmaps, small interactive lessons, browser practice and progressive support.
- DataCamp interactive learning: https://www.datacamp.com/interactive-learning — short hands-on exercises and immediate feedback.
- Teaching the science of learning (2018): https://pmc.ncbi.nlm.nih.gov/articles/PMC5780548/ — spaced practice, interleaving, retrieval, elaboration, concrete examples and dual coding.
- 2026 meta-analysis of retrieval, distributed and interleaved practice: https://link.springer.com/article/10.1007/s10648-026-10225-5
- TCS NQT official hiring page: https://www.tcs.com/careers/india/tcs-all-india-nqt-hiring
- Accenture careers assessment guidance: https://www.accenture.com/in-en/careers/explore-careers/area-of-interest/journey-to-accenture
