import { requestWithRetry as request } from "./request.ts";

export const dailyApi = {
  getChallenge() {
    return request("/api/v1/daily/challenge");
  },

  submitChallenge(problemId, code, language) {
    return request("/api/v1/daily/challenge/submit", {
      method: "POST",
      body: JSON.stringify({ problem_id: problemId, code, language }),
    });
  },

  getLeagues() {
    return request("/api/v1/daily/leagues");
  },

  getLeaderboard(timeframe = "daily") {
    return request(`/api/v1/daily/leaderboard?timeframe=${timeframe}`);
  },
};

export const learningApi = {
  getLanguages() {
    return request("/api/v1/learning/languages");
  },

  getLanguageLevels(languageId) {
    return request(`/api/v1/learning/${languageId}/levels`);
  },

  getLevelLessons(languageId, levelId) {
    return request(`/api/v1/learning/${languageId}/${levelId}/lessons`);
  },

  getLesson(languageId, levelId, lessonId) {
    return request(`/api/v1/learning/${languageId}/${levelId}/${lessonId}`);
  },

  completeLesson(languageId, levelId, lessonId) {
    return request(`/api/v1/learning/${languageId}/${levelId}/${lessonId}/complete`, {
      method: "POST",
    });
  },

  getProgress() {
    return request("/api/v1/learning/progress");
  },

  getLanguageStats(languageId) {
    return request(`/api/v1/learning/${languageId}/stats`);
  },

  getDailyGoal() {
    return request("/api/v1/learning/daily-goal");
  },

  getLeaderboard() {
    return request("/api/v1/learning/leaderboard");
  },

  getStreak() {
    return request("/api/v1/learning/streak");
  },
};