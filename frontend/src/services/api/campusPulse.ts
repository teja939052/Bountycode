import { requestWithRetry } from "./request.ts";

const BASE = "/api/v1/pulse";

export const campusPulseApi = {
  activeBattles: () => requestWithRetry(`${BASE}/active-battles`),

  createBattle: (campus_a, campus_b, category) =>
    requestWithRetry(`${BASE}/create-battle`, {
      method: "POST",
      body: JSON.stringify({ campus_a, campus_b, category }),
    }),

  joinBattle: (battleId) =>
    requestWithRetry(`${BASE}/join-battle/${battleId}`, {
      method: "POST",
    }),

  submitAnswer: (battleId, answerData) =>
    requestWithRetry(`${BASE}/submit-answer/${battleId}`, {
      method: "POST",
      body: JSON.stringify(answerData),
    }),

  battleScores: (battleId) => requestWithRetry(`${BASE}/battle/${battleId}/scores`),

  campusRankings: (limit = 20) =>
    requestWithRetry(`${BASE}/campus-rankings?limit=${limit}`),

  dailyPulse: () =>
    requestWithRetry(`${BASE}/daily-pulse`, {
      method: "POST",
    }),
};