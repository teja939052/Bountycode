# BountyCode — Agent Standing Orders

## Source of Truth (binding)

Read `docs/BOUNTYCODE_VISION_LOCK.md` and `docs/PRD_SERVICE_BASED_V1.md` before making product or architecture decisions.

Do not contradict them silently.
Do not create alternative launch dates, product names, positioning, or competing strategic priorities.

If implementation reality conflicts with these documents:
1. report the conflict,
2. show the evidence,
3. stop before making a strategic change.

## Standing Orders (apply to every task, override all other instructions)

1. **Verify before changing.** Never trust docs, comments, or audit claims — read the call sites.
2. **No destructive rewrites.** Before any migration or deletion: produce a written architecture proposal + migration map + test plan.
3. **Single source of truth, everywhere.** Backend: `record_practice` is the only XP writer. Frontend: `useGamificationState` is the only XP/level/streak reader.
4. **UI never computes reward math.** Every reward display renders exactly what the server returns.
5. **Ground truth by execution.** Any "correct answer" in interactive content must be computed by running code, then human-confirmed.
6. **Integrity labels.** "TCS-pattern practice" unless the question is documented as asked at TCS. Readiness below evidence threshold shows "Not enough evidence yet," never a number.
7. **No ✅-style claims.** "Feature exists" is not "feature works." Anything reported done includes how it was verified.
8. **Content is founder-authored.** The agent builds tooling and renderers. It does not author launch content, does not mass-generate questions, and does not "fill gaps" with AI content.

## Forbidden Scope (building any of these = task failure)

- ❌ New gamification mechanics (guilds, seasons, cards, new worlds, pet systems, avatars)
- ❌ Mobile app, video content of any kind
- ❌ FAANG/product-company content, tracks, or positioning
- ❌ New registries, new orchestration layers, backend rewrites
- ❌ Bulk question generation; touching the 6,216 unverified bank items except to keep them quarantined
- ❌ Interest graphs, recommendation engines, social features, forums
- ❌ Deleting routes/pages without the route-parity test protecting the invariant
- ❌ Any work not mapped to a Phase 1 workstream in the PRD

## Verification Standard

Do not consider compile/build success sufficient.

Every critical loop requires runtime evidence:
student action → database state → returned API state → UI result → next state.

All destructive changes require an audit before execution.
