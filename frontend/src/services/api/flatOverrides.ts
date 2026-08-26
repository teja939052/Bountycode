// Legacy flat aliases for backward-compatible `api.<name>(...)` calls.
// New code should use the namespace-based API: `api.namespace.method(...)`.
import { requestWithRetry } from "./request.ts";
import type { PlanInfo } from "./types.ts";

export const flatOverrides = {
  // ---- generic helper ----
  get: (endpoint: string) => requestWithRetry(endpoint),
  post: (endpoint: string, body: Record<string, unknown>) =>
    requestWithRetry(endpoint, { method: "POST", body: JSON.stringify(body) }),

  // ---- questions / problem bank (convenience aliases) ----
  browseQuestions: (params: Record<string, unknown> = {}) =>
    requestWithRetry(
      `/api/v1/questions/browse?${new URLSearchParams(params as Record<string, string>).toString()}`,
    ),
  getQuestionFull: (questionId: string) =>
    requestWithRetry(`/api/v1/questions/${encodeURIComponent(questionId)}`),
  isQuestionSolved: (questionId: string) =>
    requestWithRetry(
      `/api/v1/questions/${encodeURIComponent(questionId)}/solved`,
    ),
  getQuestionFilters: () => requestWithRetry("/api/v1/questions/filters"),
  submitQuestionAnswer: (
    questionId: string,
    answer: string,
    timeTaken: number | null = null,
  ) =>
    requestWithRetry("/api/v1/questions/answer", {
      method: "POST",
      body: JSON.stringify({
        question_id: questionId,
        answer,
        time_taken: timeTaken,
      }),
    }),
  submitQuestionCode: (questionId: string, payload: Record<string, unknown>) =>
    requestWithRetry(
      `/api/v1/questions/${encodeURIComponent(questionId)}/submit`,
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    ),
  getTopicProblems: (topic: string) =>
    requestWithRetry(
      `/api/v1/questions/browse?${new URLSearchParams({ topic, limit: "100" }).toString()}`,
    ),

  // ---- coding + compiler (convenience aliases) ----
  getCodingTopics: () => requestWithRetry("/api/v1/coding/topics"),
  startCodingChallengeV2: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/coding/start", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  submitCodingAnswer: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/coding/submit", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getCodingSolution: (challengeId: string) =>
    requestWithRetry(
      `/api/v1/coding/${encodeURIComponent(challengeId)}/solution`,
    ),
  getCodingHint: (challengeId: string, hintLevel = 1) =>
    requestWithRetry("/api/v1/coding/hint", {
      method: "POST",
      body: JSON.stringify({
        challenge_id: challengeId,
        hint_level: hintLevel,
      }),
    }),
  getInterviewerReview: (challengeId: string, code: string, language: string) =>
    requestWithRetry("/api/v1/coding/interviewer-review", {
      method: "POST",
      body: JSON.stringify({ challenge_id: challengeId, code, language }),
    }),
  executeCompilerCode: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/compiler/execute", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  executeCompilerTestCases: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/compiler/execute-test-cases", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  traceCompilerCode: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/compiler/trace", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getCompilerBoilerplate: (language: string, topics: string[] = []) =>
    requestWithRetry("/api/v1/compiler/boilerplate", {
      method: "POST",
      body: JSON.stringify({ language, topics }),
    }),

  // ---- aptitude (convenience aliases) ----
  startAptitudeTest: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/aptitude/start", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  submitAptitudeAnswer: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/aptitude/answer", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  completeAptitudeTest: (testId: string) =>
    requestWithRetry(
      `/api/v1/aptitude/${encodeURIComponent(testId)}/complete`,
      {
        method: "POST",
      },
    ),

  // ---- resume (convenience aliases) ----
  uploadResume: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return fetch("/api/v1/resume/upload", {
      method: "POST",
      credentials: "include",
      body: formData,
    }).then((r) => r.json());
  },
  generateResume: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/resume/generate", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  optimizeResume: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/resume/optimize", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  exportResume: (resumeId: string) =>
    requestWithRetry(
      `/api/v1/resume/${encodeURIComponent(resumeId)}/export/docx`,
    ),
  getSemanticAtsScore: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/resume/semantic-score", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  improveBullets: (bullets: string[], jobRole = "") =>
    requestWithRetry("/api/v1/enhanced/resume/improve-bullets", {
      method: "POST",
      body: JSON.stringify({ bullets, job_role: jobRole }),
    }),

  // ---- adaptive learning (convenience aliases) ----
  getSkillAssessment: () => requestWithRetry("/api/v1/adaptive/skills"),
  getWeakAreasAdaptive: () => requestWithRetry("/api/v1/adaptive/weak-areas"),
  getDailyPlan: () => requestWithRetry("/api/v1/adaptive/daily-plan"),
  getReadinessScoreAdaptive: () =>
    requestWithRetry("/api/v1/adaptive/readiness"),
  getLearningPath: () => requestWithRetry("/api/v1/adaptive/learning-path"),
  recordAdaptiveActivity: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/adaptive/activity", {
      method: "POST",
      body: JSON.stringify(payload),
    }),

  // ---- analytics / admin ----
  getAnalyticsOverview: () => requestWithRetry("/api/v1/analytics/overview"),
  getAnalyticsFunnel: () => requestWithRetry("/api/v1/analytics/funnel"),
  getAnalyticsSkills: () => requestWithRetry("/api/v1/analytics/skills"),
  getAnalyticsCompanies: () => requestWithRetry("/api/v1/analytics/companies"),
  getAnalyticsInsights: () => requestWithRetry("/api/v1/analytics/insights"),
  getHealthStatus: () => requestWithRetry("/health"),

  // ---- progress / heatmap / streaks ----
  getProgressOverview: () => requestWithRetry("/api/v1/progress/overview"),
  getProblemProgress: () => requestWithRetry("/api/v1/progress/overview"),
  getHeatmap: () => requestWithRetry("/api/v1/progress/heatmap"),
  getStreak: () => requestWithRetry("/api/v1/progress/streak"),
  getTopicProgress: () => requestWithRetry("/api/v1/progress/topic-progress"),
  getWeeklyGoal: () => requestWithRetry("/api/v1/progress/weekly-goal"),

  // ---- community feed + study groups + discussions ----
  getFeedPosts: (page = 1, limit = 20) =>
    requestWithRetry(`/api/v1/community/feed?page=${page}&limit=${limit}`),
  createFeedPost: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/community/feed", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  likeFeedPost: (id: string) =>
    requestWithRetry(`/api/v1/community/feed/${encodeURIComponent(id)}/like`, {
      method: "POST",
    }),
  deleteFeedPost: (id: string) =>
    requestWithRetry(`/api/v1/community/feed/${encodeURIComponent(id)}`, {
      method: "DELETE",
    }),
  addFeedComment: (id: string, content: string) =>
    requestWithRetry(
      `/api/v1/community/feed/${encodeURIComponent(id)}/comment`,
      {
        method: "POST",
        body: JSON.stringify({ content }),
      },
    ),
  getDiscussions: (params: Record<string, string> = {}) =>
    requestWithRetry(
      `/api/v1/discussions${Object.keys(params).length ? `?${new URLSearchParams(params).toString()}` : ""}`,
    ),
  createDiscussion: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/discussions", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  getStudyGroups: () => requestWithRetry("/api/v1/hook/study-groups"),
  createStudyGroup: (body: { name: string; description?: string }) =>
    requestWithRetry("/api/v1/hook/study-groups/create", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  joinStudyGroup: (groupId: string) =>
    requestWithRetry(
      `/api/v1/hook/study-groups/${encodeURIComponent(groupId)}/join`,
      {
        method: "POST",
      },
    ),

  // ---- company prep / mocks ----
  getCompanies: () => requestWithRetry("/api/v1/company/companies"),
  getCompanyGuide: (companyId: string) =>
    requestWithRetry(`/api/v1/company/${encodeURIComponent(companyId)}/guide`),
  getBehavioralQuestion: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/company/behavioral", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getCompanyQuestions: (company: string) =>
    requestWithRetry(
      `/api/v1/questions/company/${encodeURIComponent(company)}`,
    ),
  getCompanyQuestionList: (
    company: string,
    category = "",
    page: number = 1,
    limit: number = 20,
  ) =>
    requestWithRetry(
      `/api/v1/questions/company/${encodeURIComponent(company)}/questions?category=${encodeURIComponent(
        category,
      )}&page=${page}&limit=${limit}`,
    ),
  getMockCompanies: () => requestWithRetry("/api/v1/company-mocks/companies"),
  getMockHistory: () => requestWithRetry("/api/v1/mock-interview/history"),
  startMockTest: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/mock-interview/start", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  completeMockTest: (sessionId: string) =>
    requestWithRetry(
      `/api/v1/mock-interview/${encodeURIComponent(sessionId)}/complete`,
      {
        method: "POST",
      },
    ),

  // ---- 30-day daily challenge (separate router) ----
  getDailyChallenge: () => requestWithRetry("/api/v1/daily/challenge"),
  submitDailyChallenge: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/daily/challenge/submit", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getDailyChallengeToday: () => requestWithRetry("/api/v1/daily/challenge"),
  getDailyChallengeStatus: () =>
    requestWithRetry("/api/v1/daily/challenge/status"),
  getDailyChallengeProgress: () =>
    requestWithRetry("/api/v1/daily/challenge/progress"),
  getDailyChallengeLeaderboard: () =>
    requestWithRetry("/api/v1/daily/challenge/leaderboard"),
  enrollDailyChallenge: (path: string) =>
    requestWithRetry(
      `/api/v1/daily/challenge/enroll?path=${encodeURIComponent(path)}`,
      { method: "POST" },
    ),
  completeDailyChallengeDay: (questIds: string[]) =>
    requestWithRetry("/api/v1/daily/challenge/complete-day", {
      method: "POST",
      body: JSON.stringify({ quest_ids: questIds }),
    }),

  // ---- system design ----
  startSystemDesign: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/system-design/start", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  submitSystemDesignAnswer: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/system-design/answer", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getSystemDesignResult: (sessionId: string) =>
    requestWithRetry(
      `/api/v1/system-design/${encodeURIComponent(sessionId)}/result`,
    ),

  // ---- rank ----
  getRankProfile: () => requestWithRetry("/api/v1/rank/profile"),
  getRankLeaderboard: () => requestWithRetry("/api/v1/rank/leaderboard"),

  // ---- career profile ----
  getCareerProfile: () => requestWithRetry("/api/v1/profile"),
  updateCareerProfile: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/profile", {
      method: "PUT",
      body: JSON.stringify(body),
    }),
  uploadResumeToProfile: (file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    return fetch("/api/v1/profile/upload-resume", {
      method: "POST",
      credentials: "include",
      body: formData,
    }).then((r) => r.json());
  },
  addProfileSectionItem: (section: string, item: Record<string, unknown>) =>
    requestWithRetry(
      `/api/v1/profile/sections/${encodeURIComponent(section)}/items`,
      {
        method: "POST",
        body: JSON.stringify(item),
      },
    ),
  removeProfileSectionItem: (section: string, index: number) =>
    requestWithRetry(
      `/api/v1/profile/sections/${encodeURIComponent(section)}/items/${index}`,
      { method: "DELETE" },
    ),
  getProfileStats: () =>
    requestWithRetry("/api/v1/profile/stats") as Promise<{
      level?: number;
      xp?: number;
      streak?: number;
      total_solved?: number;
      easy?: number;
      medium?: number;
      hard?: number;
      [key: string]: unknown;
    }>,

  // ---- application tracker (student) ----
  createApplication: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/applications", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  getApplicationPipeline: () =>
    requestWithRetry("/api/v1/applications/pipeline"),
  updateApplicationStage: (
    applicationId: string,
    stage: Record<string, unknown>,
  ) =>
    requestWithRetry(
      `/api/v1/applications/${encodeURIComponent(applicationId)}/stage`,
      {
        method: "PUT",
        body: JSON.stringify(stage),
      },
    ),
  getApplicationStats: () => requestWithRetry("/api/v1/applications/stats"),
  deleteApplication: (applicationId: string) =>
    requestWithRetry(
      `/api/v1/applications/${encodeURIComponent(applicationId)}`,
      {
        method: "DELETE",
      },
    ),

  // ---- battles ----
  joinBattleQueue: (body: Record<string, unknown> = {}) =>
    requestWithRetry("/api/v1/battles/queue", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  getBattleQueueStatus: () => requestWithRetry("/api/v1/battles/queue/status"),
  getBattleState: (id: string) =>
    requestWithRetry(`/api/v1/battles/${encodeURIComponent(id)}`),
  getBattleHistory: () => requestWithRetry("/api/v1/battles/history"),
  getBattleLeaderboard: () => requestWithRetry("/api/v1/battles/leaderboard"),
  submitBattleSolution: (id: string, body: Record<string, unknown>) =>
    requestWithRetry(`/api/v1/battles/${encodeURIComponent(id)}/submit`, {
      method: "POST",
      body: JSON.stringify(body),
    }),
  surrenderBattle: (id: string) =>
    requestWithRetry(`/api/v1/battles/${encodeURIComponent(id)}/surrender`, {
      method: "POST",
    }),

  // ---- practice sessions ----
  createPracticeSession: (body: Record<string, unknown> = {}) =>
    requestWithRetry("/api/v1/practice/session", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  // ---- enterprise ----
  getEnterpriseCohorts: () => requestWithRetry("/api/v1/enterprise/cohorts"),
  createEnterpriseCohort: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/enterprise/cohorts", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  getCohortProgress: (id: string) =>
    requestWithRetry(
      `/api/v1/enterprise/cohorts/${encodeURIComponent(id)}/progress`,
    ),

  // ---- project generator ----
  getProjectHistory: () => requestWithRetry("/api/v1/projects/history"),
  generateProject: (
    description: string,
    language?: string,
    framework?: string,
  ) =>
    requestWithRetry("/api/v1/projects/generate", {
      method: "POST",
      body: JSON.stringify({ description, language, framework }),
    }),
  reviewProject: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/projects/review", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  improveCode: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/projects/improve", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  saveProject: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/projects/save", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  getProject: (id: string) =>
    requestWithRetry(`/api/v1/projects/${encodeURIComponent(id)}`),

  // ---- billing / trial / discounts ----
  createCheckout: (country = "US", couponCode = "", seats = 1) =>
    requestWithRetry("/api/v1/billing/checkout", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode, seats }),
    }),
  createLifetimeCheckout: (country = "US", couponCode = "") =>
    requestWithRetry("/api/v1/billing/checkout/lifetime", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode }),
    }),
  createYearlyCheckout: (country = "US", couponCode = "") =>
    requestWithRetry("/api/v1/billing/checkout/yearly", {
      method: "POST",
      body: JSON.stringify({ country, coupon_code: couponCode }),
    }),
  createTeamCheckout: (country = "US", seats = 5, couponCode = "") =>
    requestWithRetry("/api/v1/billing/checkout/team", {
      method: "POST",
      body: JSON.stringify({ country, seats, coupon_code: couponCode }),
    }),
  createEnterpriseCheckout: (country = "US", seats = 10, couponCode = "") =>
    requestWithRetry("/api/v1/billing/checkout/enterprise", {
      method: "POST",
      body: JSON.stringify({ country, seats, coupon_code: couponCode }),
    }),
  getPlans: () =>
    requestWithRetry("/api/v1/billing/plans") as Promise<PlanInfo[]>,
  validateCoupon: (code = "") =>
    requestWithRetry("/api/v1/billing/coupon/validate", {
      method: "POST",
      body: JSON.stringify({ code }),
    }),
  getUsageStats: () =>
    requestWithRetry("/api/v1/billing/status") as Promise<{
      plan?: string;
      features?: Record<
        string,
        { monthly_limit: number | string; monthly_used: number }
      >;
      [key: string]: unknown;
    }>,
  startTrial: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/trial/start", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  verifyStudentDiscount: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/discount/student/verify", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  // ---- salary + cover letter ----
  generateCoverLetter: (
    resumeId: string,
    jobDescription: string,
    companyName: string,
  ) =>
    requestWithRetry("/api/v1/tools/cover-letter", {
      method: "POST",
      body: JSON.stringify({
        resume_id: resumeId,
        job_description: jobDescription,
        company_name: companyName,
      }),
    }),
  generateLinkedInAbout: (resumeId: string, targetRole: string) =>
    requestWithRetry("/api/v1/tools/linkedin-about", {
      method: "POST",
      body: JSON.stringify({ resume_id: resumeId, target_role: targetRole }),
    }),
  getSalaryBenchmark: (
    jobTitle: string,
    location: string,
    company = "",
    yearsExperience = 0,
    level = "",
  ) =>
    requestWithRetry("/api/v1/salary/benchmark", {
      method: "POST",
      body: JSON.stringify({
        job_title: jobTitle,
        location,
        company,
        years_experience: yearsExperience,
        level,
      }),
    }),
  getSalaryNegotiationTips: (
    jobTitle: string,
    offeredSalary: number,
    location: string,
    yearsExperience = 0,
    companySize = "",
    benefits: string[] = [],
  ) =>
    requestWithRetry("/api/v1/tools/salary-negotiation", {
      method: "POST",
      body: JSON.stringify({
        job_title: jobTitle,
        offered_salary: offeredSalary,
        location,
        years_experience: yearsExperience,
        company_size: companySize,
        benefits,
      }),
    }),

  // ---- placement ----
  getPlacementDrives: () => requestWithRetry("/api/v1/placement/drives"),
  getSupportedCompanies: () => requestWithRetry("/api/v1/predictor/companies"),
  getPredictionHistory: () => requestWithRetry("/api/v1/predictor/history"),
  predictOffer: (company: string, role = "SDE") =>
    requestWithRetry("/api/v1/predictor/predict", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    }),
  recordOutcome: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/predictor/outcome", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getOutcomes: () => requestWithRetry("/api/v1/predictor/outcomes"),
  deleteOutcome: (id: string) =>
    requestWithRetry(`/api/v1/predictor/outcome/${encodeURIComponent(id)}`, {
      method: "DELETE",
    }),
  getOutcomeStats: () => requestWithRetry("/api/v1/predictor/outcome-stats"),
  timeToOffer: (company: string, role = "SDE") =>
    requestWithRetry("/api/v1/predictor/time-to-offer", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    }),
  getAlumniExperiences: () => requestWithRetry("/api/v1/placement/alumni"),
  getIndianCompanies: () =>
    requestWithRetry("/api/v1/indian-placement/companies"),

  // ---- DSA fingerprint / skill profile ----
  getSkillProfile: () => requestWithRetry("/api/v1/fingerprint/skill-profile"),
  getCompanyPredictions: () =>
    requestWithRetry("/api/v1/fingerprint/company-predictions"),
  getCompanyFingerprint: (companyId: string) =>
    requestWithRetry(
      `/api/v1/fingerprint/company/${encodeURIComponent(companyId)}`,
    ),

  // ---- journeys ----
  getLearningJourneys: () => requestWithRetry("/api/v1/learning/journeys"),
  getJourneyDetail: (journeyId: string) =>
    requestWithRetry(
      `/api/v1/learning/journeys/${encodeURIComponent(journeyId)}`,
    ),

  // ---- AI debugger ----
  analyzeCode: (payload: Record<string, unknown>) =>
    requestWithRetry("/api/v1/ai-debugger/analyze", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  creativeMind: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/enhanced/coding/creative-mind", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  // ---- spaced repetition ----
  initializeSRS: (body: Record<string, unknown> = {}) =>
    requestWithRetry("/api/v1/srs/initialize", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  reviewSRSConcept: (conceptId: string, grade: number) =>
    requestWithRetry("/api/v1/srs/review", {
      method: "POST",
      body: JSON.stringify({ concept_id: conceptId, grade }),
    }),
  getDueSRSCards: (limit = 20) =>
    requestWithRetry(`/api/v1/srs/due?limit=${limit}`),
  getSRSStats: () => requestWithRetry("/api/v1/srs/stats"),
  getSRSConcepts: () => requestWithRetry("/api/v1/srs/concepts"),
  getSRSForecast: (days = 30) =>
    requestWithRetry(`/api/v1/srs/forecast?days=${days}`),

  // ---- contests ----
  getContests: () => requestWithRetry("/api/v1/hook/contests"),
  joinContest: (contestId: string) =>
    requestWithRetry(
      `/api/v1/hook/contests/${encodeURIComponent(contestId)}/enter`,
      {
        method: "POST",
      },
    ),

  getGamificationProfile: () =>
    requestWithRetry("/api/v1/gamification/profile"),

  // ---- question bank extras (missing legacy aliases) ----
  getQuestionStats: () => requestWithRetry("/api/v1/questions/stats"),
  submitNewQuestion: (body: Record<string, unknown>) =>
    requestWithRetry("/api/v1/questions/submit", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  upvoteQuestion: (questionId: string, vote = 1) =>
    requestWithRetry("/api/v1/questions/upvote", {
      method: "POST",
      body: JSON.stringify({ question_id: questionId, vote }),
    }),
  getRecentAnswers: (limit = 20) =>
    requestWithRetry(`/api/v1/questions/recent?limit=${limit}`),
  getRandomProblem: (params: Record<string, string> = {}) =>
    requestWithRetry(
      `/api/v1/features/random?${new URLSearchParams(params).toString()}`,
    ),
  getAcceptanceRate: (questionId: string) =>
    requestWithRetry(
      `/api/v1/features/problem/${encodeURIComponent(questionId)}/acceptance`,
    ),
  getSimilarProblems: (questionId: string, limit = 5) =>
    requestWithRetry(
      `/api/v1/features/problem/${encodeURIComponent(questionId)}/similar?limit=${limit}`,
    ),

  // ---- gamification extras (skill graph / streak freeze / daily goal) ----
  getSkillGraph: () => requestWithRetry("/api/v1/gamification/skills"),
  getWeakAreas: (topN = 5) =>
    requestWithRetry(`/api/v1/gamification/skills/weak?top_n=${topN}`),
  getReadinessScore: (company: string | null = null) =>
    requestWithRetry(
      `/api/v1/gamification/skills/readiness${company ? `?company=${company}` : ""}`,
    ),
  getStreakFreezeStatus: () =>
    requestWithRetry("/api/v1/gamification/tower/streak-freeze"),
  buyStreakFreeze: () =>
    requestWithRetry("/api/v1/gamification/tower/streak-freeze/buy", {
      method: "POST",
    }),
  getDailyGoal: () => requestWithRetry("/api/v1/gamification/tower/daily-goal"),
  getAllBadges: () => requestWithRetry("/api/v1/gamification/badges"),
  getHealth: () => requestWithRetry("/health"),

  // ---- Friends ----
  getMyUid: () => requestWithRetry("/api/v1/friends/uid"),
  getFriendsOverview: () => requestWithRetry("/api/v1/friends/overview"),
  sendFriendRequest: (uid: string) =>
    requestWithRetry("/api/v1/friends/request", {
      method: "POST",
      body: JSON.stringify({ uid }),
    }),
  acceptFriendRequest: (id: string) =>
    requestWithRetry(
      `/api/v1/friends/requests/${encodeURIComponent(id)}/accept`,
      { method: "POST" },
    ),
  declineFriendRequest: (id: string) =>
    requestWithRetry(
      `/api/v1/friends/requests/${encodeURIComponent(id)}/decline`,
      { method: "POST" },
    ),
  cancelFriendRequest: (id: string) =>
    requestWithRetry(
      `/api/v1/friends/requests/${encodeURIComponent(id)}/cancel`,
      { method: "POST" },
    ),
  removeFriend: (friendId: string) =>
    requestWithRetry(`/api/v1/friends/${encodeURIComponent(friendId)}`, {
      method: "DELETE",
    }),
  getFriendSuggestions: (q?: string, limit = 10) =>
    requestWithRetry(
      `/api/v1/friends/suggestions?${q ? `q=${encodeURIComponent(q)}&` : ""}limit=${limit}`,
    ),

  // ---- Battle challenges ----
  createBattleChallenge: (mode: string, difficulty: string, language: string) =>
    requestWithRetry("/api/v1/battles/challenge", {
      method: "POST",
      body: JSON.stringify({ mode, difficulty, language }),
    }),
  getBattleChallenge: (token: string) =>
    requestWithRetry(`/api/v1/battles/challenge/${encodeURIComponent(token)}`),
  acceptBattleChallenge: (token: string) =>
    requestWithRetry(
      `/api/v1/battles/challenge/${encodeURIComponent(token)}/accept`,
      { method: "POST" },
    ),

  // ---- Squad join codes ----
  getSquadJoinCode: (squadId: string) =>
    requestWithRetry(
      `/api/v1/study-squads/${encodeURIComponent(squadId)}/join-code`,
      { method: "POST" },
    ),
  joinSquadByCode: (code: string) =>
    requestWithRetry("/api/v1/study-squads/join-by-code", {
      method: "POST",
      body: JSON.stringify({ code }),
    }),
};
