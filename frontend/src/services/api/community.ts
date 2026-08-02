import { requestWithRetry as request } from "./request.ts";
export const communityApi = {
  getDiscussions(questionId, sort = "best", page = 1) {
    return request(`/api/v1/discussions/${questionId}?sort=${sort}&page=${page}`);
  },

  createDiscussion(questionId, content, code = null, language = null, type = "solution") {
    return request(`/api/v1/discussions/${questionId}`, {
      method: "POST",
      body: JSON.stringify({ content, code, language, discussion_type: type }),
    });
  },

  upvoteDiscussion(discussionId) {
    return request(`/api/v1/discussions/${discussionId}/upvote`, { method: "POST" });
  },

  replyToDiscussion(discussionId, content) {
    return request(`/api/v1/discussions/${discussionId}/reply`, {
      method: "POST",
      body: JSON.stringify({ content }),
    });
  },

  getDiscussionSummary(questionId) {
    return request(`/api/v1/discussions/${questionId}/summary`);
  },

  getStudyGroups() {
    return request("/api/v1/hook/study-groups");
  },

  createStudyGroup(name, description = "") {
    return request("/api/v1/hook/study-groups/create", {
      method: "POST",
      body: JSON.stringify({ name, description }),
    });
  },

  joinStudyGroup(groupId) {
    return request(`/api/v1/hook/study-groups/${groupId}/join`, { method: "POST" });
  },

  getActiveContests() {
    return request("/api/v1/hook/contests");
  },

  enterContest(contestId, score) {
    return request(`/api/v1/hook/contests/${contestId}/enter?score=${score}`, {
      method: "POST",
    });
  },

  getContestLeaderboard(contestId) {
    return request(`/api/v1/hook/contests/${contestId}/leaderboard`);
  },
};

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