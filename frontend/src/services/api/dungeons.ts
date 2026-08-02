import { requestWithRetry } from "./request.ts";

export const dungeonsApi = {
  list() {
    return requestWithRetry("/api/v1/dungeons");
  },

  detail(dungeonId) {
    return requestWithRetry(`/api/v1/dungeons/${dungeonId}`);
  },

  start(dungeonId, stageIndex) {
    return requestWithRetry(`/api/v1/dungeons/${dungeonId}/start`, {
      method: "POST",
      body: JSON.stringify({ stage_index: stageIndex }),
    });
  },

  submit(dungeonId, stageIndex, payload) {
    return requestWithRetry(`/api/v1/dungeons/${dungeonId}/stage/${stageIndex}/submit`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  leaderboard(dungeonId, limit = 10) {
    return requestWithRetry(`/api/v1/dungeons/${dungeonId}/leaderboard?limit=${limit}`);
  },

  history() {
    return requestWithRetry("/api/v1/dungeons/history");
  },

  chests() {
    return requestWithRetry("/api/v1/dungeons/chests");
  },

  advance(dungeonId, stageIndex) {
    return requestWithRetry(`/api/v1/dungeons/${dungeonId}/advance`, {
      method: "POST",
      body: JSON.stringify({ stage_index: stageIndex }),
    });
  },
};
