import { requestWithRetry as request } from "./request.ts";
export const questionsApi = {
  browse(params: Record<string, any> = {}) {
    const qs = new URLSearchParams();
    if (params.company) qs.set("company", params.company);
    if (params.role) qs.set("role", params.role);
    if (params.topic) qs.set("topic", params.topic);
    if (params.sub_topic) qs.set("sub_topic", params.sub_topic);
    if (params.difficulty) qs.set("difficulty", params.difficulty);
    if (params.type) qs.set("type", params.type);
    if (params.search) qs.set("search", params.search);
    if (params.page) qs.set("page", params.page);
    if (params.limit) qs.set("limit", params.limit);
    return request(`/api/v1/questions/browse?${qs.toString()}`);
  },

  getFilters() {
    return request("/api/v1/questions/filters");
  },

  getFull(questionId) {
    return request(`/api/v1/questions/${encodeURIComponent(questionId)}`);
  },

  isSolved(questionId) {
    return request(`/api/v1/questions/${encodeURIComponent(questionId)}/solved`);
  },

  submitAnswer(questionId, answer, timeTaken = null) {
    return request("/api/v1/questions/answer", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, answer, time_taken: timeTaken }),
    });
  },

  submitCode(questionId, payload) {
    return request(`/api/v1/questions/${encodeURIComponent(questionId)}/submit`, payload);
  },

  getSolution(questionId, hintLevel = 1) {
    return request(`/api/v1/questions/${encodeURIComponent(questionId)}/solution`, {
      method: "POST",
      body: JSON.stringify({ hint_level: hintLevel }),
    });
  },

  upvote(questionId, vote = 1) {
    return request("/api/v1/questions/upvote", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, vote }),
    });
  },

  getStats() {
    return request("/api/v1/questions/stats");
  },

  getRecent(limit = 20) {
    return request(`/api/v1/questions/recent?limit=${limit}`);
  },

  getRandom(params: Record<string, any> = {}) {
    const qs = new URLSearchParams();
    if (params.type) qs.set("type", params.type);
    if (params.difficulty) qs.set("difficulty", params.difficulty);
    if (params.topic) qs.set("topic", params.topic);
    if (params.company) qs.set("company", params.company);
    qs.set("exclude_solved", "true");
    return request(`/api/v1/questions/random?${qs.toString()}`);
  },

  getCompanyQuestions(company, page = 1, limit = 20) {
    return request(`/api/v1/questions/company/${encodeURIComponent(company)}?page=${page}&limit=${limit}`);
  },

  getTopics() {
    return request("/api/v1/questions/topics");
  },

  submitQuestion(payload) {
    return request("/api/v1/questions/submit", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  getCompanyMocks() {
    return request("/api/v1/placement/mocks/companies");
  },

  startMockTest(company) {
    return request("/api/v1/placement/mocks/start", {
      method: "POST",
      body: JSON.stringify({ company }),
    });
  },

  submitMockAnswer(testId, questionIndex, answer) {
    return request("/api/v1/placement/mocks/answer", {
      method: "POST",
      body: JSON.stringify({ test_id: testId, question_index: questionIndex, answer }),
    });
  },

  completeMockTest(testId, answers = null) {
    return request("/api/v1/placement/mocks/complete", {
      method: "POST",
      body: JSON.stringify({ test_id: testId, answers }),
    });
  },

  getMockHistory() {
    return request("/api/v1/placement/mocks/history");
  },
};