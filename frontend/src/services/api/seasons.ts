import { requestWithRetry as request } from "./request.ts";

export const seasonsApi = {
  getCurrent() {
    return request("/api/v1/seasons/current");
  },

  getAll() {
    return request("/api/v1/seasons/all");
  },

  updateProgress(data) {
    return request("/api/v1/seasons/progress", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getLeaderboard(seasonKey) {
    return request(`/api/v1/seasons/leaderboard/${seasonKey}`);
  },
};