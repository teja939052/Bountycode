import { requestWithRetry as request } from "./request.ts";
export const learningModulesApi = {
  list(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    if (params.difficulty) query.append("difficulty", params.difficulty);
    if (params.topic) query.append("topic", params.topic);
    if (params.company) query.append("company", params.company);
    if (params.page) query.append("page", params.page);
    if (params.limit) query.append("limit", params.limit);
    const qs = query.toString();
    return request(`/api/v1/learning-modules${qs ? `?${qs}` : ""}`);
  },

  get(moduleId) {
    return request(`/api/v1/learning-modules/${moduleId}`);
  },

  start(moduleId) {
    return request(`/api/v1/learning-modules/${moduleId}/start`, {
      method: "POST",
    });
  },

  completeStep(moduleId, stepNumber) {
    return request(
      `/api/v1/learning-modules/${moduleId}/steps/${stepNumber}/complete`,
      { method: "POST" }
    );
  },

  getProgress() {
    return request("/api/v1/learning-modules/user/progress");
  },

  getRecommendations(company = null) {
    const qs = company ? `?company=${encodeURIComponent(company)}` : "";
    return request(`/api/v1/learning-modules/recommendations${qs}`);
  },
};