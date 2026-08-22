import { requestWithRetry as request } from "./request.ts";
export const hrApi = {
  getCategories() {
    return request("/api/v1/hr/categories");
  },

  getQuestion(questionId) {
    return request(`/api/v1/hr/question/${encodeURIComponent(questionId)}`);
  },

  getRandom(params = {}) {
    const qs = new URLSearchParams();
    if (params.category) qs.set("category", params.category);
    if (params.difficulty) qs.set("difficulty", params.difficulty);
    if (params.company) qs.set("company", params.company);
    return request(`/api/v1/hr/random?${qs.toString()}`);
  },

  submitAnswer(questionId, answer, timeTaken = 0) {
    return request("/api/v1/hr/answer", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, answer, time_taken: timeTaken }),
    });
  },

  getFeedback(questionId, answer) {
    return request("/api/v1/hr/feedback", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, answer }),
    });
  },

  getStats() {
    return request("/api/v1/hr/stats");
  },

  getHistory() {
    return request("/api/v1/hr/history");
  },
};