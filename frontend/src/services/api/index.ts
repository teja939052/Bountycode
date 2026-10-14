import { authApi } from "./auth.ts";
import { interviewApi, bookingApi } from "./interview.ts";
import { resumeApi } from "./resume.ts";
import { billingApi } from "./billing.ts";
import { aptitudeApi } from "./aptitude.ts";
import { codingApi, compilerApi } from "./coding.ts";
import { questionsApi } from "./questions.ts";
import { toolsApi } from "./tools.ts";
import { companyMocksApi } from "./companyPrep.ts";
import { gamificationApi } from "./gamification.ts";
import { oaApi } from "./oa.ts";
import { systemDesignApi } from "./systemDesign.ts";
import { learningEventsApi } from "./learningEvents.ts";
import { analyticsApi } from "./analytics.ts";
import { adminContentApi, assignmentsApi } from "./adminContent.ts";
import { onboardingApi } from "./onboarding.ts";
import { lessonApi, unifiedLearningApi } from "./lesson.ts";
import { learningModulesApi } from "./learningModules.ts";
import { studyApi } from "./study.ts";
import { tcsNqtApi } from "./tcsNqt.ts";
import { indianPlacementApi } from "./placement.ts";
import { metricsApi } from "./metrics.ts";
import { missionApi } from "./missions.ts";
import { csFundamentalsApi } from "./csFundamentals.ts";
import { learnerApi } from "./learner.ts";
import { opportunityApi } from "./opportunity.ts";
import { searchApi } from "./search.ts";
import campaignApi from "./campaign.ts";
import { trialApi } from "./trial.ts";
import { aiDebuggerApi } from "./aiDebugger.ts";
import { accountApi } from "./account.ts";
import { requestWithRetry } from "./request.ts";
import type { ApiRequestOptions } from "./request.ts";

export {
  cloudinaryImage,
  cloudinaryVideo,
  optimizeImage,
} from "../cloudinary.ts";

export { missionApi, csFundamentalsApi, learnerApi, opportunityApi };
export * from "./types.ts";
export * from "./curriculum.ts";

const api = {
  // Flat compatibility surface: pages historically call api.<method>() directly
  // (e.g. api.startAptitudeTest). Every sub-API is spread here so those calls
  // resolve; namespaced access (api.billing.*) keeps working alongside.
  // Four names collide across modules (submitAnswer, getState, getToday,
  // recordActivity) — no page calls them via the flat surface, and the
  // namespaced objects remain the source of truth for those.
  ...authApi,
  ...interviewApi,
  ...bookingApi,
  ...resumeApi,
  ...billingApi,
  ...aptitudeApi,
  ...codingApi,
  ...compilerApi,
  ...questionsApi,
  ...toolsApi,
  ...companyMocksApi,
  ...gamificationApi,
  ...oaApi,
  ...systemDesignApi,
  ...learningEventsApi,
  ...analyticsApi,
  ...adminContentApi,
  ...assignmentsApi,
  ...onboardingApi,
  ...lessonApi,
  ...unifiedLearningApi,
  ...learningModulesApi,
  ...studyApi,
  ...tcsNqtApi,
  ...indianPlacementApi,
  ...metricsApi,
  ...missionApi,
  ...csFundamentalsApi,
  ...learnerApi,
  ...opportunityApi,
  ...searchApi,
  ...(campaignApi as Record<string, unknown>),
  ...trialApi,
  ...aiDebuggerApi,
  ...accountApi,

  // Legacy long-name aliases: pages call these names, modules define the
  // short names. Signatures match positionally — keep both in sync.
  startAptitudeTest: aptitudeApi.startTest,
  submitAptitudeAnswer: aptitudeApi.submitAnswer,
  completeAptitudeTest: aptitudeApi.completeTest,
  getCodingTopics: codingApi.getTopics,
  startCodingChallengeV2: codingApi.startChallengeV2,
  submitCodingAnswer: codingApi.submitAnswer,
  getCodingSolution: codingApi.getSolution,
  getCodingHint: codingApi.getHint,
  executeCompilerCode: compilerApi.executeCode,
  executeCompilerTestCases: compilerApi.executeTestCases,
  getCompilerBoilerplate: compilerApi.getBoilerplate,
  traceCompilerCode: compilerApi.traceCode,
  getQuestionFull: questionsApi.getFull,
  submitQuestionAnswer: questionsApi.submitAnswer,
  submitQuestionCode: questionsApi.submitCode,
  submitNewQuestion: questionsApi.submitQuestion,
  upvoteQuestion: questionsApi.upvote,
  getSemanticATS: resumeApi.semanticScore,
  getSemanticAtsScore: resumeApi.semanticScore,
  improveBullets: resumeApi.improveBullets,
  getRepairRetest: missionApi.getRetest,
  submitRepairRetest: missionApi.submitRetest,
  getHealthStatus: () => requestWithRetry("/api/v1/health/status"),

  // Raw HTTP verbs for hooks/pages that call endpoints directly
  // (api.get("/api/v1/...")). Declared last so they win over the three
  // domain-specific `get`s (adminContent/learningModules) for flat callers;
  // those remain reachable via their namespaces.
  get: (endpoint: string, options?: ApiRequestOptions) =>
    requestWithRetry(endpoint, { ...options, method: "GET" }),
  post: (endpoint: string, body?: unknown, options?: ApiRequestOptions) =>
    requestWithRetry(endpoint, {
      ...options,
      method: "POST",
      body: body === undefined ? undefined : JSON.stringify(body),
      headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    }),
  put: (endpoint: string, body?: unknown, options?: ApiRequestOptions) =>
    requestWithRetry(endpoint, {
      ...options,
      method: "PUT",
      body: body === undefined ? undefined : JSON.stringify(body),
      headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    }),
  patch: (endpoint: string, body?: unknown, options?: ApiRequestOptions) =>
    requestWithRetry(endpoint, {
      ...options,
      method: "PATCH",
      body: body === undefined ? undefined : JSON.stringify(body),
      headers: { "Content-Type": "application/json", ...(options?.headers || {}) },
    }),
  delete: (endpoint: string, options?: ApiRequestOptions) =>
    requestWithRetry(endpoint, { ...options, method: "DELETE" }),

  auth: authApi,
  interview: interviewApi,
  booking: bookingApi,
  resume: resumeApi,
  billing: billingApi,
  aptitude: aptitudeApi,
  coding: codingApi,
  compiler: compilerApi,
  questions: questionsApi,
  tools: toolsApi,
  companyMocks: companyMocksApi,
  gamification: gamificationApi,
  oa: oaApi,
  systemDesign: systemDesignApi,
  learningEvents: learningEventsApi,
  analytics: analyticsApi,
  adminContent: adminContentApi,
  assignments: assignmentsApi,
  onboarding: onboardingApi,
  lesson: lessonApi,
  unifiedLearning: unifiedLearningApi,
  learningModules: learningModulesApi,
  study: studyApi,
  tcsNqt: tcsNqtApi,
  indianPlacement: indianPlacementApi,
  metrics: metricsApi,
  missions: missionApi,
  csFundamentals: csFundamentalsApi,
  learner: learnerApi,
  opportunity: opportunityApi,
  search: searchApi,
  campaign: campaignApi,
  trial: trialApi,
  aiDebugger: aiDebuggerApi,
  account: accountApi,
};

export default api;
