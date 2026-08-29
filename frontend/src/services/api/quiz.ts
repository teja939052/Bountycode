import { requestWithRetry as request } from "./request.ts";

export const quizApi = {
  // Build a quiz session
  buildQuiz(options = {}) {
    return request("/api/v1/quiz/build", {
      method: "POST",
      body: JSON.stringify(options),
    });
  },

  // Submit an answer
  submitAnswer(submission) {
    return request("/api/v1/quiz/answer", {
      method: "POST",
      body: JSON.stringify(submission),
    });
  },

  // Get a hint
  getHint(questionId, hintLevel = 1, hintsAlreadyUsed = 0) {
    return request("/api/v1/quiz/hint", {
      method: "POST",
      body: JSON.stringify({
        question_id: questionId,
        hint_level: hintLevel,
        hints_already_used: hintsAlreadyUsed,
      }),
    });
  },

  // Calculate quiz results
  calculateResults(payload) {
    return request("/api/v1/quiz/results", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  // Get learning path
  getLearningPath(options = {}) {
    return request("/api/v1/quiz/learning-path", {
      method: "POST",
      body: JSON.stringify(options),
    });
  },

  // Start boss battle
  startBossBattle(bossLevel = 1, userLevel = 1) {
    return request("/api/v1/quiz/boss-battle", {
      method: "POST",
      body: JSON.stringify({
        boss_level: bossLevel,
        user_level: userLevel,
      }),
    });
  },

  // Get stats
  getStats() {
    return request("/api/v1/quiz/stats");
  },

  // Get weak topics
  getWeakTopics(attempts = []) {
    const params = new URLSearchParams();
    params.set("attempted", JSON.stringify(attempts));
    return request(`/api/v1/quiz/weak-topics?${params.toString()}`);
  },

  // List questions
  listQuestions(filters = {}) {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([k, v]) => {
      if (v != null) params.set(k, v);
    });
    return request(`/api/v1/quiz/questions?${params.toString()}`);
  },

  // Get question detail
  getQuestionDetail(questionId) {
    return request(`/api/v1/quiz/questions/${questionId}`);
  },
};

export default quizApi;
