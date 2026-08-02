import { requestWithRetry as request } from "./request.ts";
export const mockInterviewApi = {
  start(config: Record<string, any> = {}) {
    return request("/api/v1/mock-interview/start", {
      method: "POST",
      body: JSON.stringify(config),
    });
  },

  submitAnswer(sessionId, questionIndex, code, language) {
    return request(`/api/v1/mock-interview/${sessionId}/submit`, {
      method: "POST",
      body: JSON.stringify({ question_index: questionIndex, code, language }),
    });
  },

  getStatus(sessionId) {
    return request(`/api/v1/mock-interview/${sessionId}/status`);
  },

  getHistory() {
    return request("/api/v1/mock-interview/history");
  },
};

export const personalDashboardApi = {
  get() {
    return request("/api/v1/dashboard/personal");
  },

  getRecommendations() {
    return request("/api/v1/dashboard/recommendations");
  },
};

export const dsaFingerprintApi = {
  getSkillProfile() {
    return request("/api/v1/fingerprint/skill-profile");
  },

  getCompanyPredictions() {
    return request("/api/v1/fingerprint/company-predictions");
  },

  getCompanyFingerprint(companyId) {
    return request(`/api/v1/fingerprint/company/${companyId}`);
  },
};

export const battlesApi = {
  get() {
    return request("/api/v1/battles");
  },

  getById(battleId) {
    return request(`/api/v1/battles/${battleId}`);
  },
};

export const scrimsApi = {
  get(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, v);
    });
    return request(`/api/v1/scrims?${query.toString()}`);
  },

  getById(scrimId) {
    return request(`/api/v1/scrims/${scrimId}`);
  },

  create(payload) {
    return request("/api/v1/scrims", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  like(scrimId) {
    return request(`/api/v1/scrims/${scrimId}/like`, { method: "POST" });
  },
};

export const rankApi = {
  get() {
    return request("/api/v1/rank");
  },

  getProfile() {
    return request("/api/v1/rank/profile");
  },
};

export const projectGeneratorApi = {
  generate(payload) {
    return request("/api/v1/project-generator/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  getHistory() {
    return request("/api/v1/project-generator/history");
  },
};

export const mysteryBoxApi = {
  open() {
    return request("/api/v1/hook/mystery-box", { method: "POST" });
  },

  checkDoubleXP(activityType, score) {
    return request("/api/v1/hook/double-xp-check", {
      method: "POST",
      body: JSON.stringify({ activity_type: activityType, score }),
    });
  },

  getSavageFeedback(score) {
    return request(`/api/v1/hook/savage-feedback?score=${score}`);
  },

  useStreakFreeze() {
    return request("/api/v1/hook/streak-freeze", { method: "POST" });
  },

  getDailyBonus() {
    return request("/api/v1/hook/daily-bonus");
  },
};

export const energyApi = {
  get() {
    return request("/api/v1/energy");
  },
};

export const playlistsApi = {
  get(difficulty = null, company = null) {
    const params = new URLSearchParams();
    if (difficulty) params.append("difficulty", difficulty);
    if (company) params.append("company", company);
    return request(`/api/v1/playlists?${params.toString()}`);
  },

  getById(playlistId) {
    return request(`/api/v1/playlists/${playlistId}`);
  },

  getNext(playlistId) {
    return request(`/api/v1/playlists/${playlistId}/next`);
  },

  createCustom(title, description, problemIds) {
    return request("/api/v1/playlists/custom", {
      method: "POST",
      body: JSON.stringify({ title, description, problem_ids: problemIds }),
    });
  },

  getMyCustom() {
    return request("/api/v1/playlists/my/custom");
  },
};

export const discussionsApi = {
  get(questionId, sort = "best", page = 1) {
    return request(`/api/v1/discussions/${questionId}?sort=${sort}&page=${page}`);
  },

  create(questionId, content, code = null, language = null, type = "solution") {
    return request(`/api/v1/discussions/${questionId}`, {
      method: "POST",
      body: JSON.stringify({ content, code, language, discussion_type: type }),
    });
  },

  upvote(discussionId) {
    return request(`/api/v1/discussions/${discussionId}/upvote`, { method: "POST" });
  },

  reply(discussionId, content) {
    return request(`/api/v1/discussions/${discussionId}/reply`, {
      method: "POST",
      body: JSON.stringify({ content }),
    });
  },

  getSummary(questionId) {
    return request(`/api/v1/discussions/${questionId}/summary`);
  },
};

export const submissionsApi = {
  submit(questionId, code, language) {
    return request(`/api/v1/submissions/${questionId}/submit`, {
      method: "POST",
      body: JSON.stringify({ code, language }),
    });
  },

  getHistory(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, v);
    });
    return request(`/api/v1/submissions/history?${query.toString()}`);
  },

  getProblemSubmissions(questionId, limit = 10) {
    return request(`/api/v1/submissions/problem/${questionId}?limit=${limit}`);
  },

  getSolvedStatus(questionId) {
    return request(`/api/v1/submissions/status/${questionId}`);
  },

  getSolvedProblems(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, v);
    });
    return request(`/api/v1/submissions/solved?${query.toString()}`);
  },

  getStats() {
    return request("/api/v1/submissions/stats");
  },
};

export const featuresApi = {
  getRandomProblem(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, v);
    });
    return request(`/api/v1/features/random?${query.toString()}`);
  },

  toggleBookmark(questionId) {
    return request(`/api/v1/features/bookmarks/${questionId}`, { method: "POST" });
  },

  getBookmarks(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, v);
    });
    return request(`/api/v1/features/bookmarks?${query.toString()}`);
  },

  saveNote(questionId, content) {
    return request(`/api/v1/features/notes/${questionId}`, {
      method: "POST",
      body: JSON.stringify({ content }),
    });
  },

  getNote(questionId) {
    return request(`/api/v1/features/notes/${questionId}`);
  },

  getAllNotes() {
    return request("/api/v1/features/notes");
  },

  getEnhancedProblemDetail(questionId) {
    return request(`/api/v1/features/problem/${questionId}/enhanced`);
  },

  getSimilarProblems(questionId, limit = 5) {
    return request(`/api/v1/features/problem/${questionId}/similar?limit=${limit}`);
  },
};

export const visualizationsApi = {
  getComparisons() {
    return request("/api/v1/visualizations/compare");
  },

  getComparison(comparisonId) {
    return request(`/api/v1/visualizations/compare/${comparisonId}`);
  },
};

export const distributionsApi = {
  get() {
    return request("/api/v1/distributions");
  },
};

export const analyticsApi = {
  getOverview() {
    return request("/api/v1/analytics/overview");
  },

  getFunnel() {
    return request("/api/v1/analytics/funnel");
  },

  getSkills() {
    return request("/api/v1/analytics/skills");
  },

  getCompanies() {
    return request("/api/v1/analytics/companies");
  },

  getInsights() {
    return request("/api/v1/analytics/insights");
  },
};

export const aiDebuggerApi = {
  analyzeCode({ code, language = "python", context = "chat" }) {
    return request("/api/v1/ai-debugger/analyze", {
      method: "POST",
      body: JSON.stringify({ code, language, context }),
    });
  },

  getStepByStep(questionId, code, language) {
    return request("/api/v1/ai-debugger/step-by-step", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, code, language }),
    });
  },

  suggestFix(code, language, error) {
    return request("/api/v1/ai-debugger/suggest-fix", {
      method: "POST",
      body: JSON.stringify({ code, language, error }),
    });
  },

  rubberDuck(question, code, language) {
    return request("/api/v1/ai-debugger/rubber-duck", {
      method: "POST",
      body: JSON.stringify({ question, code, language }),
    });
  },

  analyzeFailedSubmission(questionId, code, language, failedTestCase = null) {
    return request("/api/v1/ai-debugger/analyze", {
      method: "POST",
      body: JSON.stringify({
        question_id: questionId,
        code,
        language,
        failed_test_case: failedTestCase,
      }),
    });
  },

  getProgressiveHint(questionId, hintLevel = 1, code = null) {
    return request("/api/v1/ai-debugger/hint", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, hint_level: hintLevel, code }),
    });
  },

  explainError(errorMessage, code, language) {
    return request("/api/v1/ai-debugger/explain-error", {
      method: "POST",
      body: JSON.stringify({ error_message: errorMessage, code, language }),
    });
  },
};

export const conceptsApi = {
  get(topic) {
    return request(`/api/v1/concepts/${encodeURIComponent(topic)}`);
  },

  getAll() {
    return request("/api/v1/concepts");
  },
};