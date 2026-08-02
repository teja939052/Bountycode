import { requestWithRetry as request } from "./request.ts";
export const aptitudeApi = {
  getCategories() {
    return request("/api/v1/aptitude/categories");
  },

  startTest(category, difficulty = "medium", questionCount = 20) {
    return request("/api/v1/aptitude/start", {
      method: "POST",
      body: JSON.stringify({ category, difficulty, question_count: questionCount }),
    });
  },

  submitAnswer(testId, questionIndex, answer) {
    return request("/api/v1/aptitude/answer", {
      method: "POST",
      body: JSON.stringify({ test_id: testId, question_index: questionIndex, answer }),
    });
  },

  completeTest(testId, timeTaken = 0) {
    return request(`/api/v1/aptitude/${testId}/complete?time_taken=${timeTaken}`, {
      method: "POST",
    });
  },

  getHistory() {
    return request("/api/v1/aptitude/history");
  },
};