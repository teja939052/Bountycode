import { requestWithRetry } from "./request.ts";

const BASE = "/api/v1/trending";

export const trendingChallengesApi = {
  feed: (limit = 10) => requestWithRetry(`${BASE}/feed?limit=${limit}`),

  engage: (questionId) =>
    requestWithRetry(`${BASE}/engage/${questionId}`, {
      method: "POST",
    }),

  stats: () => requestWithRetry(`${BASE}/stats`),
};