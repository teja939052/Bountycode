import { requestWithRetry as request } from "./request.ts";
export const systemDesignApi = {
  start(difficulty = "medium", topic = "") {
    return request("/api/v1/system-design/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic }),
    });
  },

  submitAnswer(sessionId, question, answer, diagramDescription = "") {
    return request("/api/v1/system-design/answer", {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId, question, answer, diagram_description: diagramDescription }),
    });
  },

  getResult(sessionId) {
    return request(`/api/v1/system-design/${sessionId}/result`);
  },

  getHistory() {
    return request("/api/v1/system-design/history");
  },
};

export const systemDesignTestsApi = {
  getCategories() {
    return request("/api/v1/system-design-tests/categories");
  },

  listProblems(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, v);
    });
    return request(`/api/v1/system-design-tests/problems?${query.toString()}`);
  },

  getProblem(problemId) {
    return request(`/api/v1/system-design-tests/problem/${problemId}`);
  },

  evaluate(problemId, answer) {
    return request(`/api/v1/system-design-tests/evaluate/${problemId}`, {
      method: "POST",
      body: JSON.stringify({ answer }),
    });
  },

  getModelAnswer(problemId) {
    return request(`/api/v1/system-design-tests/model-answer/${problemId}`);
  },

  getRubric() {
    return request("/api/v1/system-design-tests/rubric");
  },

  getHistory(limit = 20) {
    return request(`/api/v1/system-design-tests/history?limit=${limit}`);
  },

  getStats() {
    return request("/api/v1/system-design-tests/stats");
  },

  getLeaderboard() {
    return request("/api/v1/system-design-tests/leaderboard");
  },
};