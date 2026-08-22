import { requestWithRetry as request } from "./request.ts";
export const behavioralApi = {
  getCategories() {
    return request("/api/v1/behavioral/categories");
  },

  getQuestion(questionId) {
    return request(`/api/v1/behavioral/question/${encodeURIComponent(questionId)}`);
  },

  getRandom(params = {}) {
    const qs = new URLSearchParams();
    if (params.category) qs.set("category", params.category);
    if (params.difficulty) qs.set("difficulty", params.difficulty);
    if (params.company) qs.set("company", params.company);
    return request(`/api/v1/behavioral/random?${qs.toString()}`);
  },

  getBySubCategory(subCategory) {
    return request(`/api/v1/behavioral/questions/sub-category/${encodeURIComponent(subCategory)}`);
  },

  submitAnswer(questionId, answer, timeTaken = 0) {
    return request("/api/v1/behavioral/answer", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, answer, time_taken: timeTaken }),
    });
  },

  getFeedback(questionId, answer) {
    return request("/api/v1/behavioral/feedback", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, answer }),
    });
  },

  getStats() {
    return request("/api/v1/behavioral/stats");
  },

  getHistory() {
    return request("/api/v1/behavioral/history");
  },
};