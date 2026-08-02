import { requestWithRetry } from "./request.ts";

const BASE = "/api/v1/share";

export const shareableAchievementsApi = {
  generate: (achievement_type, score_data) =>
    requestWithRetry(`${BASE}/generate`, {
      method: "POST",
      body: JSON.stringify({ achievement_type, score_data }),
    }),

  getCard: (token) => requestWithRetry(`${BASE}/card/${token}`),

  share: (token) =>
    requestWithRetry(`${BASE}/${token}/share`, {
      method: "POST",
    }),

  myCards: () => requestWithRetry(`${BASE}/my-cards`),

  leaderboard: (limit = 10) =>
    requestWithRetry(`${BASE}/leaderboard?limit=${limit}`),
};