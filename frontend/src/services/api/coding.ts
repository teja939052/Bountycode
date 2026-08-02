import { requestWithRetry as request } from "./request.ts";
export const codingApi = {
  getTopics() {
    return request("/api/v1/coding/topics");
  },

  startChallenge(difficulty = "medium", topic = "arrays", language = "python") {
    return request("/api/v1/coding/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic, language }),
    });
  },

  startChallengeV2(difficulty = "medium", topic = "arrays", language = "python", company = "", role = "SDE") {
    return request("/api/v1/coding/start", {
      method: "POST",
      body: JSON.stringify({ difficulty, topic, language, company, role }),
    });
  },

  getHint(challengeId, hintLevel = 1) {
    return request("/api/v1/coding/hint", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, hint_level: hintLevel }),
    });
  },

  getInterviewerReview(challengeId, code, language = "python") {
    return request("/api/v1/coding/interviewer-review", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, code, language }),
    });
  },

  submitAnswer(challengeId, code, timeTaken = 0) {
    return request("/api/v1/coding/submit", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, code, time_taken: timeTaken }),
    });
  },

  getSolution(challengeId) {
    return request(`/api/v1/coding/${challengeId}/solution`);
  },

  getHistory() {
    return request("/api/v1/coding/history");
  },
};

export const compilerApi = {
  executeCode({ code, language, stdin = "", timeout = 5 }) {
    return request("/api/v1/compiler/execute", {
      method: "POST",
      body: JSON.stringify({ code, language, stdin, timeout }),
    });
  },

  executeTestCases({ code, language, test_cases, timeout = 5 }) {
    return request("/api/v1/compiler/execute-test-cases", {
      method: "POST",
      body: JSON.stringify({ code, language, test_cases, timeout }),
    });
  },

  getLanguages() {
    return request("/api/v1/compiler/languages");
  },

  getBoilerplate(language, topics = []) {
    return request("/api/v1/compiler/boilerplate", {
      method: "POST",
      body: JSON.stringify({ language, topics }),
    });
  },

  traceCode({ code, language, stdin = "" }) {
    return request("/api/v1/compiler/trace", {
      method: "POST",
      body: JSON.stringify({ code, language, stdin }),
    });
  },
};