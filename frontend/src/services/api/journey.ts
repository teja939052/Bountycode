// @ts-nocheck
import { requestWithRetry as request } from "./request.ts";

export const journeyApi = {
  /** Canonical journey state — character position + world map + today's activity. */
  getState() {
    return request("/api/v1/journey/state");
  },
  /** Study Engine's today payload (next / reviews / practice / challenge). */
  getToday() {
    return request("/api/v1/study/today");
  },
  /** Record a completed learning activity and fan-out to mastery / SRS / Diamonds. */
  recordActivity(payload: Record<string, unknown>) {
    const unifiedPayload = {
      lesson_id: (payload.question_id as string) || (payload.skill_id as string) || "unknown",
      activity_type: (payload.type as string) || "learn",
      score: typeof payload.score === "number" ? payload.score : 0,
      passed: typeof payload.passed === "boolean" ? payload.passed : false,
      time_spent_seconds: typeof payload.time_spent === "number" ? payload.time_spent : 0,
      diagnosis_codes: (payload.diagnosis_codes as string[]) || [],
      metadata: (payload.metadata as Record<string, any>) || {},
    };
    return request("/api/v1/unified/activity", {
      method: "POST",
      body: JSON.stringify(unifiedPayload),
    });
  },
  /** World level detail (for the level-player overlay). */
  getWorldView(worldId: string) {
    return request(`/api/v1/worlds/${worldId}`);
  },
  attemptLevel(worldId: string, levelId: string, payload: Record<string, unknown>) {
    return request(`/api/v1/worlds/${worldId}/levels/${levelId}/attempt`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
  completeLevel(worldId: string, levelId: string, payload: Record<string, unknown>) {
    return request(`/api/v1/worlds/${worldId}/levels/${levelId}/complete`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};

export default journeyApi;
