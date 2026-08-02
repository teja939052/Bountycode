import { requestWithRetry as request } from "./request.ts";

export const tournamentsApi = {
  getPresets() {
    return request("/api/v1/tournaments/presets");
  },

  create(data) {
    return request("/api/v1/tournaments/create", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getActive() {
    return request("/api/v1/tournaments/active");
  },

  join(data) {
    return request(`/api/v1/tournaments/join/${data.tournament_id}`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  submit(data) {
    return request(`/api/v1/tournaments/submit/${data.tournament_id}`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getLeaderboard(tournamentId) {
    return request(`/api/v1/tournaments/leaderboard/${tournamentId}`);
  },

  getHistory() {
    return request("/api/v1/tournaments/history");
  },
};