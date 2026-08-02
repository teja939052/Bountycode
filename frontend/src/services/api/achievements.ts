import { requestWithRetry as request } from "./request.ts";

export const achievementsApi = {
  getChains() {
    return request("/api/v1/achievements/chains");
  },

  getStats() {
    return request("/api/v1/achievements/stats");
  },

  updateProgress(data) {
    return request("/api/v1/achievements/progress", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};