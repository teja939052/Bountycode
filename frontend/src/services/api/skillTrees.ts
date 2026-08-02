import { requestWithRetry as request } from "./request.ts";

export const skillTreesApi = {
  getAll() {
    return request("/api/v1/skill-trees/all");
  },

  getProgress() {
    return request("/api/v1/skill-trees/progress");
  },

  updateProgress(data) {
    return request("/api/v1/skill-trees/progress", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};