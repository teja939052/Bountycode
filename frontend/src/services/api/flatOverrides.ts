// Hand-mapped flat aliases for legacy `api.<name>(...)` calls whose target
// method name differs from its namespace method (or never existed). Kept
// separate from the auto-generated flat.js so it is auditable by hand.
import { requestWithRetry } from "./request.ts";
import { aptitudeApi } from "./aptitude.ts";
import { adaptiveApi } from "./adaptive.ts";
import { resumeApi } from "./resume.ts";
import { codingApi, compilerApi } from "./coding.ts";
import { questionsApi } from "./questions.ts";
import { gamificationApi } from "./gamification.ts";
import { communityApi, dailyApi } from "./community.ts";
import { companyPrepApi, companyMocksApi } from "./companyPrep.ts";
import { toolsApi, salaryApi } from "./tools.ts";
import {
  scrimsApi, rankApi, projectGeneratorApi, analyticsApi, aiDebuggerApi,
  featuresApi, submissionsApi, dsaFingerprintApi,
} from "./misc.ts";
import { journeyApi } from "./journey.ts";
import { systemDesignApi } from "./systemDesign.ts";
import { placementApi, indianPlacementApi } from "./placement.ts";
import { srsApi } from "./srs.ts";
import { billingApi } from "./billing.ts";
import { studentApi } from "./student.ts";
import { guildsApi } from "./guilds.ts";
import { enhancedApi } from "./enhanced.ts";
import { dungeonsApi } from "./dungeons.ts";

export const flatOverrides = {
  // ---- generic helper ----
  post: (endpoint, body) => requestWithRetry(endpoint, { method: "POST", body: JSON.stringify(body) }),

  // ---- gamification ----
  getGamificationProfile: (...a) => gamificationApi.getProfile.apply(gamificationApi, a),
  getReadinessScore: (...a) => gamificationApi.getReadinessScore.apply(gamificationApi, a),
  getSkillGraph: (...a) => gamificationApi.getSkillGraph.apply(gamificationApi, a),
  getWeakAreas: (...a) => gamificationApi.getWeakAreas.apply(gamificationApi, a),
  getDailyGoal: (...a) => gamificationApi.getDailyGoal.apply(gamificationApi, a),
  getStreakFreezeStatus: (...a) => gamificationApi.getStreakFreezeStatus.apply(gamificationApi, a),
  buyStreakFreeze: (...a) => gamificationApi.buyStreakFreeze.apply(gamificationApi, a),
  getAllBadges: (...a) => gamificationApi.getAllBadges.apply(gamificationApi, a),
  getTower: (...a) => gamificationApi.getTower.apply(gamificationApi, a),
  getChallenges: (...a) => gamificationApi.getChallenges.apply(gamificationApi, a),
  buyPowerUp: (...a) => gamificationApi.buyPowerUp.apply(gamificationApi, a),
  usePowerUp: (...a) => gamificationApi.usePowerUp.apply(gamificationApi, a),
  claimChallenge: (...a) => gamificationApi.claimChallenge.apply(gamificationApi, a),
  getCardCollection: (...a) => gamificationApi.getCardCollection.apply(gamificationApi, a),
  getCardStats: (...a) => gamificationApi.getCardStats.apply(gamificationApi, a),
  getDailyDraw: (...a) => gamificationApi.getDailyDraw.apply(gamificationApi, a),
  getLeaderboard: (...a) => gamificationApi.getLeaderboard.apply(gamificationApi, a),

  // ---- questions / problem bank ----
  browseQuestions: (...a) => questionsApi.browse.apply(questionsApi, a),
  getQuestionFull: (...a) => questionsApi.getFull.apply(questionsApi, a),
  isQuestionSolved: (...a) => questionsApi.isSolved.apply(questionsApi, a),
  getQuestionFilters: (...a) => questionsApi.getFilters.apply(questionsApi, a),
  submitNewQuestion: (...a) => questionsApi.submitQuestion.apply(questionsApi, a),
  upvoteQuestion: (...a) => questionsApi.upvote.apply(questionsApi, a),
  getQuestionStats: (...a) => questionsApi.getStats.apply(questionsApi, a),
  getRecentAnswers: (...a) => questionsApi.getRecent.apply(questionsApi, a),
  submitQuestionAnswer: (...a) => questionsApi.submitAnswer.apply(questionsApi, a),
  submitQuestionCode: (...a) => questionsApi.submitCode.apply(questionsApi, a),
  getTopicProblems: (topic) => questionsApi.browse({ topic, limit: 50 }),
  getAcceptanceRate: async (id) => {
    const d = await questionsApi.getFull(id);
    const anyD = d as Record<string, any>;
    return anyD.acceptance_rate ?? anyD.acceptanceRate ?? null;
  },
  getSimilarProblems: (...a) => featuresApi.getSimilarProblems.apply(featuresApi, a),
  getProblemSubmissions: (...a) => submissionsApi.getProblemSubmissions.apply(submissionsApi, a),

  // ---- coding + compiler ----
  getCodingTopics: (...a) => codingApi.getTopics.apply(codingApi, a),
  startCodingChallengeV2: (...a) => codingApi.startChallengeV2.apply(codingApi, a),
  submitCodingAnswer: (...a) => codingApi.submitAnswer.apply(codingApi, a),
  getCodingSolution: (...a) => codingApi.getSolution.apply(codingApi, a),
  getCodingHint: (...a) => codingApi.getHint.apply(codingApi, a),
  getInterviewerReview: (...a) => codingApi.getInterviewerReview.apply(codingApi, a),
  executeCompilerCode: (...a) => compilerApi.executeCode.apply(compilerApi, a),
  executeCompilerTestCases: (...a) => compilerApi.executeTestCases.apply(compilerApi, a),
  traceCompilerCode: (...a) => compilerApi.traceCode.apply(compilerApi, a),
  getCompilerBoilerplate: (...a) => compilerApi.getBoilerplate.apply(compilerApi, a),

  // ---- aptitude ----
  startAptitudeTest: (...a) => aptitudeApi.startTest.apply(aptitudeApi, a),
  submitAptitudeAnswer: (...a) => aptitudeApi.submitAnswer.apply(aptitudeApi, a),
  completeAptitudeTest: (...a) => aptitudeApi.completeTest.apply(aptitudeApi, a),

  // ---- resume ----
  uploadResume: (...a) => resumeApi.uploadResume.apply(resumeApi, a),
  generateResume: (...a) => resumeApi.generateResume.apply(resumeApi, a),
  optimizeResume: (...a) => resumeApi.optimizeResume.apply(resumeApi, a),
  exportResume: (...a) => resumeApi.exportResume.apply(resumeApi, a),
  getSemanticAtsScore: (...a) => resumeApi.semanticScore.apply(resumeApi, a),

  // ---- adaptive learning ----
  getSkillAssessment: (...a) => adaptiveApi.getSkillAssessment.apply(adaptiveApi, a),
  getWeakAreasAdaptive: (...a) => adaptiveApi.getWeakAreas.apply(adaptiveApi, a),
  getDailyPlan: (...a) => adaptiveApi.getDailyPlan.apply(adaptiveApi, a),
  getReadinessScoreAdaptive: (...a) => adaptiveApi.getReadinessScore.apply(adaptiveApi, a),
  getLearningPath: (...a) => adaptiveApi.getLearningPath.apply(adaptiveApi, a),
  recordAdaptiveActivity: (...a) => adaptiveApi.recordActivity.apply(adaptiveApi, a),

  // ---- analytics / admin ----
  getAnalyticsOverview: (...a) => analyticsApi.getOverview.apply(analyticsApi, a),
  getAnalyticsFunnel: (...a) => analyticsApi.getFunnel.apply(analyticsApi, a),
  getAnalyticsSkills: (...a) => analyticsApi.getSkills.apply(analyticsApi, a),
  getAnalyticsCompanies: (...a) => analyticsApi.getCompanies.apply(analyticsApi, a),
  getAnalyticsInsights: (...a) => analyticsApi.getInsights.apply(analyticsApi, a),
  getHealthStatus: () => requestWithRetry("/health"),

  // ---- progress / heatmap / streaks ----
  getProgressOverview: () => requestWithRetry("/api/v1/progress/overview"),
  getProblemProgress: () => requestWithRetry("/api/v1/progress/overview"),
  getHeatmap: () => requestWithRetry("/api/v1/progress/heatmap"),
  getStreak: () => requestWithRetry("/api/v1/progress/streak"),
  getTopicProgress: () => requestWithRetry("/api/v1/progress/topic-progress"),
  getWeeklyGoal: () => requestWithRetry("/api/v1/progress/weekly-goal"),

  // ---- community feed + study groups + discussions ----
  getFeedPosts: (page = 1, limit = 20) => requestWithRetry(`/api/v1/community/feed?page=${page}&limit=${limit}`),
  createFeedPost: (body) => requestWithRetry("/api/v1/community/feed", { method: "POST", body: JSON.stringify(body) }),
  likeFeedPost: (id) => requestWithRetry(`/api/v1/community/feed/${id}/like`, { method: "POST" }),
  deleteFeedPost: (id) => requestWithRetry(`/api/v1/community/feed/${id}`, { method: "DELETE" }),
  addFeedComment: (id, content) => requestWithRetry(`/api/v1/community/feed/${id}/comment`, { method: "POST", body: JSON.stringify({ content }) }),
  getDiscussions: (...a) => communityApi.getDiscussions.apply(communityApi, a),
  createDiscussion: (...a) => communityApi.createDiscussion.apply(communityApi, a),
  getStudyGroups: (...a) => communityApi.getStudyGroups.apply(communityApi, a),
  createStudyGroup: (...a) => communityApi.createStudyGroup.apply(communityApi, a),
  joinStudyGroup: (...a) => communityApi.joinStudyGroup.apply(communityApi, a),

  // ---- company prep / mocks ----
  getCompanies: (...a) => companyPrepApi.getCompanies.apply(companyPrepApi, a),
  getCompanyGuide: (...a) => companyPrepApi.getGuide.apply(companyPrepApi, a),
  getBehavioralQuestion: (...a) => companyPrepApi.getBehavioralQuestion.apply(companyPrepApi, a),
  getMockCompanies: (...a) => companyMocksApi.getCompanies.apply(companyMocksApi, a),
  getMockHistory: (...a) => questionsApi.getMockHistory.apply(questionsApi, a),
  startMockTest: (...a) => questionsApi.startMockTest.apply(questionsApi, a),
  completeMockTest: (...a) => questionsApi.completeMockTest.apply(questionsApi, a),

  // ---- 30-day daily challenge (separate router /api/v1/daily-challenge) ----
  getDailyChallenge: (...a) => dailyApi.getChallenge.apply(dailyApi, a),
  submitDailyChallenge: (...a) => dailyApi.submitChallenge.apply(dailyApi, a),
  getDailyChallengeToday: () => requestWithRetry("/api/v1/daily-challenge/today"),
  getDailyChallengeStatus: () => requestWithRetry("/api/v1/daily-challenge/status"),
  getDailyChallengeProgress: () => requestWithRetry("/api/v1/daily-challenge/progress"),
  getDailyChallengeLeaderboard: () => requestWithRetry("/api/v1/daily-challenge/leaderboard"),
  enrollDailyChallenge: (path) => requestWithRetry(`/api/v1/daily-challenge/enroll?path=${encodeURIComponent(path)}`, { method: "POST" }),
  completeDailyChallengeDay: (questIds) => requestWithRetry("/api/v1/daily-challenge/complete-day", { method: "POST", body: JSON.stringify({ quest_ids: questIds }) }),

  // ---- scrims ----
  createScrim: (...a) => scrimsApi.create.apply(scrimsApi, a),
  getScrims: (...a) => scrimsApi.get.apply(scrimsApi, a),
  getScrim: (...a) => scrimsApi.getById.apply(scrimsApi, a),
  likeScrim: (...a) => scrimsApi.like.apply(scrimsApi, a),

  // ---- system design ----
  startSystemDesign: (...a) => systemDesignApi.start.apply(systemDesignApi, a),
  submitSystemDesignAnswer: (...a) => systemDesignApi.submitAnswer.apply(systemDesignApi, a),
  getSystemDesignResult: (...a) => systemDesignApi.getResult.apply(systemDesignApi, a),

  // ---- rank ----
  getRankProfile: (...a) => rankApi.getProfile.apply(rankApi, a),
  getRankLeaderboard: (...a) => rankApi.get.apply(rankApi, a),

  // ---- career profile ----
  getCareerProfile: () => requestWithRetry("/api/v1/profile"),
  updateCareerProfile: (body) => requestWithRetry("/api/v1/profile", { method: "PUT", body: JSON.stringify(body) }),
  uploadResumeToProfile: (file) => {
    const formData = new FormData();
    formData.append("file", file);
    return fetch("/api/v1/profile/upload-resume", { method: "POST", credentials: "include", body: formData }).then((r) => r.json());
  },
  addProfileSectionItem: (section, item) => requestWithRetry(`/api/v1/profile/sections/${section}/items`, { method: "POST", body: JSON.stringify(item) }),
  removeProfileSectionItem: (section, index) => requestWithRetry(`/api/v1/profile/sections/${section}/items/${index}`, { method: "DELETE" }),
  getProfileStats: () => requestWithRetry("/api/v1/profile/stats"),

  // ---- application tracker (student) ----
  createApplication: (...a) => studentApi.createApplication.apply(studentApi, a),
  getApplicationPipeline: (...a) => studentApi.getApplicationPipeline.apply(studentApi, a),
  updateApplicationStage: (...a) => studentApi.updateApplicationStage.apply(studentApi, a),
  getApplicationStats: (...a) => studentApi.getApplicationStats.apply(studentApi, a),
  deleteApplication: (...a) => studentApi.deleteApplication.apply(studentApi, a),

  // ---- battles ----
  joinBattleQueue: (body) => requestWithRetry("/api/v1/battles/queue", { method: "POST", body: JSON.stringify(body || {}) }),
  getBattleQueueStatus: () => requestWithRetry("/api/v1/battles/queue/status"),
  getBattleState: (id) => requestWithRetry(`/api/v1/battles/${id}`),
  getBattleHistory: () => requestWithRetry("/api/v1/battles/history"),
  getBattleLeaderboard: () => requestWithRetry("/api/v1/battles/leaderboard"),
  submitBattleSolution: (id, body) => requestWithRetry(`/api/v1/battles/${id}/submit`, { method: "POST", body: JSON.stringify(body) }),
  surrenderBattle: (id) => requestWithRetry(`/api/v1/battles/${id}/surrender`, { method: "POST" }),

  // ---- practice sessions ----
  createPracticeSession: (body) => requestWithRetry("/api/v1/practice/session", { method: "POST", body: JSON.stringify(body || {}) }),

  // ---- enterprise ----
  getEnterpriseCohorts: () => requestWithRetry("/api/v1/enterprise/cohorts"),
  createEnterpriseCohort: (body) => requestWithRetry("/api/v1/enterprise/cohorts", { method: "POST", body: JSON.stringify(body) }),
  getCohortProgress: (id) => requestWithRetry(`/api/v1/enterprise/cohorts/${id}/progress`),

  // ---- project generator ----
  getProjectHistory: (...a) => projectGeneratorApi.getHistory.apply(projectGeneratorApi, a),
  generateProject: (...a) => projectGeneratorApi.generate.apply(projectGeneratorApi, a),
  reviewProject: (body) => requestWithRetry("/api/v1/projects/review", { method: "POST", body: JSON.stringify(body) }),
  improveCode: (body) => requestWithRetry("/api/v1/projects/improve", { method: "POST", body: JSON.stringify(body) }),
  saveProject: (body) => requestWithRetry("/api/v1/projects/save", { method: "POST", body: JSON.stringify(body) }),
  getProject: (id) => requestWithRetry(`/api/v1/projects/${id}`),

  // ---- billing / trial / discounts ----
  createCheckout: (...a) => billingApi.createCheckout.apply(billingApi, a),
  createLifetimeCheckout: (...a) => billingApi.createLifetimeCheckout.apply(billingApi, a),
  createYearlyCheckout: (...a) => billingApi.createYearlyCheckout.apply(billingApi, a),
  createTeamCheckout: (...a) => billingApi.createTeamCheckout.apply(billingApi, a),
  createEnterpriseCheckout: (...a) => billingApi.createEnterpriseCheckout.apply(billingApi, a),
  validateCoupon: (...a) => billingApi.validateCoupon.apply(billingApi, a),
  getUsageStats: (...a) => billingApi.getStatus.apply(billingApi, a),
  startTrial: (body) => requestWithRetry("/api/v1/trial/start", { method: "POST", body: JSON.stringify(body || {}) }),
  verifyStudentDiscount: (body) => requestWithRetry("/api/v1/discount/student/verify", { method: "POST", body: JSON.stringify(body) }),

  // ---- salary + cover letter ----
  generateCoverLetter: (...a) => toolsApi.generateCoverLetter.apply(toolsApi, a),
  generateLinkedInAbout: (...a) => toolsApi.generateLinkedInAbout.apply(toolsApi, a),
  getSalaryBenchmark: (...a) => salaryApi.getBenchmark.apply(salaryApi, a),
  getSalaryNegotiationTips: (...a) => toolsApi.getSalaryNegotiationTips.apply(toolsApi, a),

  // ---- placement ----
  getPlacementDrives: (...a) => placementApi.getPlacementDrives.apply(placementApi, a),
  getSupportedCompanies: (...a) => placementApi.getSupportedCompanies.apply(placementApi, a),
  getPredictionHistory: (...a) => placementApi.getPredictionHistory.apply(placementApi, a),
  predictOffer: (...a) => placementApi.predictOffer.apply(placementApi, a),
  getAlumniExperiences: (...a) => placementApi.getAlumniExperiences.apply(placementApi, a),
  getIndianCompanies: (...a) => indianPlacementApi.getCompanies.apply(indianPlacementApi, a),

  // ---- DSA fingerprint / skill profile ----
  getSkillProfile: (...a) => dsaFingerprintApi.getSkillProfile.apply(dsaFingerprintApi, a),
  getCompanyPredictions: (...a) => dsaFingerprintApi.getCompanyPredictions.apply(dsaFingerprintApi, a),
  getCompanyFingerprint: (...a) => dsaFingerprintApi.getCompanyFingerprint.apply(dsaFingerprintApi, a),

  // ---- journeys ----
  getLearningJourneys: (...a) => journeyApi.get.apply(journeyApi, a),
  getJourneyDetail: (...a) => journeyApi.get.apply(journeyApi, a),

  // ---- AI debugger ----
  analyzeCode: (...a) => aiDebuggerApi.analyzeCode.apply(aiDebuggerApi, a),
  creativeMind: (body) => requestWithRetry("/api/v1/enhanced/coding/creative-mind", { method: "POST", body: JSON.stringify(body) }),

  // ---- guilds ----
  getMyRank: (...a) => guildsApi.getRank.apply(guildsApi, a),

  // ---- spaced repetition ----
  initializeSRS: (body) => requestWithRetry("/api/v1/srs/initialize", { method: "POST", body: JSON.stringify(body || {}) }),
  reviewSRSConcept: (conceptId, grade) => requestWithRetry("/api/v1/srs/review", { method: "POST", body: JSON.stringify({ concept_id: conceptId, grade }) }),
  getDueSRSCards: (limit = 20) => requestWithRetry(`/api/v1/srs/due?limit=${limit}`),
  getSRSStats: () => requestWithRetry("/api/v1/srs/stats"),
  getSRSConcepts: () => requestWithRetry("/api/v1/srs/concepts"),
  getSRSForecast: (days = 30) => requestWithRetry(`/api/v1/srs/forecast?days=${days}`),

  // ---- contests ----
  getContests: () => communityApi.getActiveContests.apply(communityApi),
  joinContest: (contestId) => communityApi.enterContest.apply(communityApi, [contestId, 0]),

  // ---- dungeons ----
  getDungeons: () => dungeonsApi.list.apply(dungeonsApi),
  getDungeonDetail: (...a) => dungeonsApi.detail.apply(dungeonsApi, a),
  startDungeon: (...a) => dungeonsApi.start.apply(dungeonsApi, a),
  submitDungeonStage: (...a) => dungeonsApi.submit.apply(dungeonsApi, a),
  getDungeonLeaderboard: (...a) => dungeonsApi.leaderboard.apply(dungeonsApi, a),
  getDungeonHistory: (...a) => dungeonsApi.history.apply(dungeonsApi, a),
  getDungeonChests: (...a) => dungeonsApi.chests.apply(dungeonsApi, a),
  advanceDungeon: (dungeonId, stageIndex) => requestWithRetry(`/api/v1/dungeons/${dungeonId}/advance`, { method: "POST", body: JSON.stringify({ stage_index: stageIndex }) }),
};
