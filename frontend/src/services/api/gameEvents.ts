import { requestWithRetry } from "./request.ts";

export const gameEventsApi = {
  boss() {
    return requestWithRetry("/api/v1/game/boss");
  },

  attackBoss(id, damage) {
    return requestWithRetry(`/api/v1/game/boss/${id}/damage`, {
      method: "POST",
      body: JSON.stringify({ damage }),
    });
  },

  claimBoss(id) {
    return requestWithRetry(`/api/v1/game/boss/${id}/claim`, {
      method: "POST",
    });
  },

  seasons() {
    return requestWithRetry("/api/v1/game/seasons");
  },

  seasonLeaderboard(id) {
    return requestWithRetry(`/api/v1/game/seasons/${id}/leaderboard`);
  },

  addSeasonXp(id, amount) {
    return requestWithRetry(`/api/v1/game/seasons/${id}/xp`, {
      method: "POST",
      body: JSON.stringify({ amount }),
    });
  },

  combo() {
    return requestWithRetry("/api/v1/game/combo");
  },

  recordCombo(success) {
    return requestWithRetry("/api/v1/game/combo/record", {
      method: "POST",
      body: JSON.stringify({ success }),
    });
  },
};
