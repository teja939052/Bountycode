import { requestWithRetry as request } from "./request.ts";

export const teamsApi = {
  getPresets() {
    return request("/api/v1/teams/presets");
  },

  create(data) {
    return request("/api/v1/teams/create", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getMyTeam() {
    return request("/api/v1/teams/my-team");
  },

  join(data) {
    return request("/api/v1/teams/join", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  leave() {
    return request("/api/v1/teams/leave", { method: "POST" });
  },

  getLeaderboard(limit = 20) {
    return request(`/api/v1/teams/leaderboard?limit=${limit}`);
  },

  getCollegeLeaderboard() {
    return request("/api/v1/teams/college-leaderboard");
  },

  contributeXP(data) {
    return request("/api/v1/teams/contribute-xp", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};