import { requestWithRetry } from "./request.ts";
import { journeyApi } from "./journey.ts";

/**
 * Mission adapter (V4 internal wiring).
 *
 * NOTE: there is no `/api/v1/missions/*` backend — the previous functions in
 * this module called dead endpoints. This adapter rewires the Mission Shell to
 * the canonical systems instead of inventing parallel ones:
 *
 * - identity/next action → GET /api/v1/journey/state (journey_engine)
 * - daily plan           → GET /api/v1/study/today     (study_engine)
 * - completion/evidence  → POST /api/v1/study/activity (record_activity →
 *                           mastery + SRS + record_practice + LearningEvent)
 * - repair/retest        → /api/v1/repair/*            (repair_service,
 *                           verified-only via question_store)
 */
export const missionApi = {
  /** Backend-decided journey state (single next action, character, map). */
  getJourneyState() {
    return journeyApi.getState();
  },
  /** Study Engine daily plan (next / reviews / practice / challenge). */
  getToday() {
    return journeyApi.getToday();
  },
  /**
   * Canonical completion sink. Payload keys (study_engine.record_activity):
   * type, skill_id, passed, score, attempts, time_spent, hints_used,
   * diagnosis_codes, question_id/trust_status (Content Trust instrumentation).
   * Returns authoritative server numbers (score, diamonds, mastery_before/after).
   */
  recordActivity(payload: Record<string, unknown>) {
    return journeyApi.recordActivity(payload);
  },
  /** Active repair missions + next-best recommendation. */
  listRepairMissions() {
    return requestWithRetry("/api/v1/repair/missions");
  },
  completeRepairMission(missionId: string) {
    return requestWithRetry("/api/v1/repair/missions/complete", {
      method: "POST",
      body: JSON.stringify({ mission_id: missionId }),
    });
  },
  /** Verified-only retest for a weakness skill (never backfilled). */
  getRetest(skill: string, count = 3) {
    return requestWithRetry(
      `/api/v1/repair/retest?skill=${encodeURIComponent(skill)}&count=${count}`,
    );
  },
  submitRetest(body: Record<string, unknown>) {
    return requestWithRetry("/api/v1/repair/retest/submit", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },
};

export default missionApi;
