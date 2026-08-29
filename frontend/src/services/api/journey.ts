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
  /** Record a completed learning activity and fan-out to mastery / SRS / XP. */
  recordActivity(payload: Record<string, unknown>) {
    return request("/api/v1/study/activity", {
      method: "POST",
      body: JSON.stringify(payload),
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
