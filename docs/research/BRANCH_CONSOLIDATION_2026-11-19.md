# Bountycode Branch Consolidation — 19 November 2026

## Consolidated working branch

- Working branch: integration/bountycode-consolidation-2026-11-18
- Baseline before this report commit: be2e9e7b2ab201456405096605836a6fc2ef9c06
- Default branch: main
- Mainline reconciliation PR: #17, merged into integration
- PR #17 merge commit: 15e7de88ce7dc7d2f8819a30401ceda425fdd6bd
- Primary release PR: #15, integration → main, remains open
- Source branches: preserved; none deleted

The integration branch is now 319 commits ahead of main and 0 commits behind main. It is the consolidated engineering workspace. This does not mean the code is production-accepted: see the CI section below.

## Pull-request disposition

| PR | Subject | Disposition |
|---|---|---|
| #1 | Service-company placement learning loop | Previously merged into main |
| #2 | Lesson timing / learning interaction | Previously merged into its service-company branch |
| #3 | Academy unification and resume | Previously merged into main; later branch-only assets recovered below |
| #4 | Diagnostic evidence integrity | Closed unmerged; changed lesson and diagnostic files are represented in integration. The integration study route is a superset containing prerequisite endpoints. |
| #5 | Verified MCQ repair and intake v2 | Closed unmerged; intake files/scripts/tests are represented. Integration question_store has additional later logic; integration verbal candidates contain later uniqueness corrections. |
| #6 | Trusted adaptive assessment and authored curriculum | Previously merged into integration |
| #7 | Account menu cleanup | Closed unmerged; desktop menu is superseded by the current UserMenu component. The mobile account disclosure is present in integration. |
| #8 | Pricing page | Previously merged into integration; Pricing.tsx matches the source branch |
| #9 | Curriculum expansion | Previously merged into main; its branch has no unique changes relative to integration |
| #10 | Mock OA student flow | Previously merged into integration |
| #11 | Service-company content quality | Previously merged into integration |
| #12 | Open learning resource library | Previously merged into integration |
| #13 | Grounded content gap audit | Previously merged into integration; its three changed files match integration |
| #14 | Grouped navigation menu | Previously merged into main; branch has no unique changes relative to integration |
| #15 | Consolidated integration | Remains open against main; not merged because full CI is not green |
| #16 | Effective-date update | Previously merged into main and included by PR #17 |
| #17 | Reconcile mainline into integration | Reopened and merged during this consolidation |
| #18 | Mock OA branch review | Closed duplicate of #10; source files are represented in integration |
| #19 | Resource library branch review | Closed duplicate of #12; all seven changed files match integration |
| #20 | Service-company quality branch review | Closed duplicate of #11; source content is represented; integration keeps a later corrected lesson-cleanup test |

## Branch-by-branch disposition

### Already represented or with no unique work

The following branches are behind integration or their relevant source files are already present:

- bountycode/learning-platform-completion
- curriculum/fill-core-learning-gaps
- feat/coding-aptitude-learning-engine
- feat/navbar-grouped-more-menu
- feature/placement-core-learning-integrity-v1
- fix/adaptive-quiz-skill-graph-snapshot-20261107
- fix/onboarding-and-navbar
- ui/pricing-page-refresh
- audit/grounded-content-gap-targets-2026-11-17
- feat/open-learning-resource-library
- feat/mock-oa-student-flow
- feat/service-company-content-quality-mainline
- feat/content-quality-intake-v2-20261107
- fix/diagnostic-evidence-integrity
- ui/account-menu-cleanup (superseded by UserMenu)
- fix/service-company-learning-loop (one merge-only commit; no file changes)
- backup/integration-before-reconciliation-2026-11-19 (retained as backup)

Tree-level checks were used rather than commit-count comparisons alone because several pull requests were squash-merged or manually reconciled.

### Candidate-only recovery

The branch bountycode/academy-unification-and-resume contains potentially useful additional lessons and question material, but also alternate question governance, skill graph, SRS, study, company-mock and frontend route implementations. The content is retained without restoring competing runtime systems.

Copied into backend/app/data/candidates/academy_unification_2026_11_19:

- 20 additional lesson JSON drafts
- 5 question-bank snapshots (original coding bank, service-OA index, and parts 1–3)
- Company exam ontology, skill-graph proposal, scrim catalog, service-company sprint config and content-quality policy
- 4 historical engineering reports archived under docs/research/archive/academy_unification_2026_11_19

Five earlier legacy lesson candidates remain under backend/app/data/candidates/legacy_lessons.

The branch audit/fixes-2026-10-13 contains a legacy pattern/theory system and a pre-cut world registry. 40 source assets were preserved under backend/app/data/candidates/audit_fixes_2026_10_13. The historical active worlds_data.py was not restored; its backup snapshot is retained only as a candidate.

All candidate directories are deliberately non-serving. They are not added to explicit question-bank lists, the live lesson directory, or the active content root. They require content validation, canonical skill mapping, deduplication, provenance review and trust lifecycle transitions before any promotion.

### Kept separate because of architectural conflict or age

- architecture-cleanup: 23 branch-only commits, 300 changed paths in the comparison result, and 689 commits behind main. Its AGENTS.md retires the current Vision Lock/PRD and conflicts with the active product authority; it also carries alternate world/curriculum registries and CI/config changes. Not merged wholesale.
- feature/self-hosted-judge0 and infra/judge0-self-host: identical to each other, but represent a deeply diverged infrastructure snapshot. Kept separate as a future execution-provider experiment; not mixed into the current hosted-compiler launch path.
- bountycode/academy-unification-and-resume: alternative service-OA routes, skill graph, SRS/study services, question governance/store changes, and orphaned frontend route system were not restored as active implementations. Only candidate content and historical docs were preserved.
- audit/fixes-2026-10-13: old runtime world registry and superseded Vision/PRD snapshots were not restored.

No source branch was deleted.

## Safety verification for candidate isolation

The current runtime paths inspected are explicit:

- question_store loads named bank files from backend/app/data; it does not recursively scan candidates/.
- company_lessons reads the direct live lessons directory, not candidates/.
- content_loader walks backend/app/content, not backend/app/data/candidates/.

Therefore, the recovered JSON and Python candidate assets are not automatically student-served or imported by these loaders.

## Current validation status

PR #15 is the consolidated release candidate. On the last inspected run before candidate-archive commits, CI reported 36 failed, 932 passed and 11 collection errors; the Learning Experience workflow passed. Failures included world-count/spec conflicts, mastery evidence expectations, lesson content contracts, compiler-service behavior, deterministic timestamp comparisons, and legacy usage-test collection errors.

Later commits have triggered fresh CI runs. Their final results must be checked before merging PR #15 into main. Do not treat candidate-archive commits or branch reconciliation as proof that the product is production-ready.

## Next action

Continue all development on integration/bountycode-consolidation-2026-11-18. Fix the current failing test categories against the authoritative Vision Lock and actual runtime contracts, rerun the entire suite, verify frontend build/type-check, and only then merge PR #15 into main.

