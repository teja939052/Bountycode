import { requestWithRetry as request } from "./request.ts";

async function fetchTodayPlan() {
  // Prefer the service-company sprint engine (ordered curriculum + weak skills).
  try {
    const sprint = await request<{ success?: boolean; data?: any }>("/api/v1/sprint/today");
    const data = (sprint as any)?.data ?? sprint;
    if (data && (Array.isArray(data.tasks) || data.next)) {
      return sprint;
    }
  } catch {
    // Fall through to legacy Study Engine.
  }
  return request("/api/v1/study/today");
}

export const journeyApi = {
  /** Canonical journey state — character position + world map + today's activity. */
  getState() {
    return request("/api/v1/journey/state");
  },
  /** Today's plan: service-company sprint first, then Study Engine. */
  getToday() {
    return fetchTodayPlan();
  },
  /** Record a completed learning activity and fan-out to mastery / SRS / Diamonds. */
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
