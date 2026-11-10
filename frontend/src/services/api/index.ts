import { authApi } from "./auth.ts";
import { interviewApi, bookingApi } from "./interview.ts";
import { resumeApi } from "./resume.ts";
import { billingApi } from "./billing.ts";
import { aptitudeApi } from "./aptitude.ts";
import { behavioralApi } from "./behavioral.ts";
import { hrApi } from "./hr.ts";

export {
  cloudinaryImage,
  cloudinaryVideo,
  optimizeImage,
} from "../cloudinary.ts";
import { codingApi, compilerApi } from "./coding.ts";
import { questionsApi } from "./questions.ts";
import { toolsApi } from "./tools.ts";
import { companyMocksApi } from "./companyPrep.ts";
import { gamificationApi } from "./gamification.ts";
import { rolesApi } from "./roles.ts";
import { oaApi } from "./oa.ts";
import { enhancedApi, freePracticeApi } from "./enhanced.ts";
import { studentApi } from "./student.ts";
import { placementApi, indianPlacementApi } from "./placement.ts";
import { systemDesignApi, systemDesignTestsApi } from "./systemDesign.ts";
import { dailyApi, learningApi, communityApi } from "./community.ts";
import { studyTimerApi } from "./studyTimer.ts";
import { companyDirectoryApi } from "./companyDirectory.ts";
import { adaptiveApi, predictorApi, readinessApi } from "./adaptive.ts";
import {
  personalDashboardApi,
  dsaFingerprintApi,
  playlistsApi,
  submissionsApi,
  featuresApi,
  visualizationsApi,
  distributionsApi,
  analyticsApi,
  aiDebuggerApi,
  conceptsApi,
  evidenceApi,
  progressApi,
} from "./misc.ts";
import { learningModulesApi } from "./learningModules.ts";
import { studyApi } from "./study.ts";
import { learningPathsApi, companyTracksApi } from "./learningPaths.ts";
import { freeTrialApi } from "./freeTrial.ts";
import { onboardingApi } from "./onboarding.ts";
import { lessonApi } from "./lesson.ts";
import { journeyApi } from "./journey.ts";
import { missionApi } from "./missions.ts";
import { mapApi } from "./map.ts";
import { adminContentApi, assignmentsApi } from "./adminContent.ts";
import { metricsApi } from "./metrics.ts";
import { tracksApi } from "./tracks.ts";
import { tcsNqtApi } from "./tcsNqt.ts";
import { companyLessonsApi } from "./companyLessons.ts";
import { academyApi } from "./academy.ts";
import { quizApi } from "./quiz.ts";
import { flatApi } from "./flat.ts";
import { flatOverrides } from "./flatOverrides.ts";
import { examMemoriesApi } from "./examMemories.ts";
import { sprintApi } from "./sprint.ts";
import { serviceOaApi } from "./serviceOa.ts";

const api = {
  auth: authApi,
  interview: interviewApi,
  booking: bookingApi,
  resume: resumeApi,
  billing: billingApi,
  aptitude: aptitudeApi,
  behavioral: behavioralApi,
  hr: hrApi,
  coding: codingApi,
  compiler: compilerApi,
  questions: questionsApi,
  tools: toolsApi,
  companyMocks: companyMocksApi,
  gamification: gamificationApi,
  roles: rolesApi,
  oa: oaApi,
  enhanced: enhancedApi,
  freePractice: freePracticeApi,
  student: studentApi,
  placement: placementApi,
  indianPlacement: indianPlacementApi,
  systemDesign: systemDesignApi,
  systemDesignTests: systemDesignTestsApi,
  daily: dailyApi,
  learning: learningApi,
  community: communityApi,
  studyTimer: studyTimerApi,
  companyDirectory: companyDirectoryApi,
  adaptive: adaptiveApi,
  predictor: predictorApi,
  readiness: readinessApi,
  personalDashboard: personalDashboardApi,
  dsaFingerprint: dsaFingerprintApi,
  playlists: playlistsApi,
  submissions: submissionsApi,
  features: featuresApi,
  visualizations: visualizationsApi,
  distributions: distributionsApi,
  analytics: analyticsApi,
  aiDebugger: aiDebuggerApi,
  concepts: conceptsApi,
  evidence: evidenceApi,
  progress: progressApi,
  learningModules: learningModulesApi,
  study: studyApi,
  learningPaths: learningPathsApi,
  companyTracks: companyTracksApi,
  freeTrial: freeTrialApi,
  onboarding: onboardingApi,
  lesson: lessonApi,
  journey: journeyApi,
  mission: missionApi,
  map: mapApi,
  adminContent: adminContentApi,
  assignments: assignmentsApi,
  metrics: metricsApi,
  tracks: tracksApi,
  tcsNqt: tcsNqtApi,
  companyLessons: companyLessonsApi,
  academy: academyApi,
  quiz: quizApi,
  examMemories: examMemoriesApi,
  sprint: sprintApi,
  serviceOa: serviceOaApi,
  login: (...args: Parameters<typeof authApi.login>) => authApi.login.apply(authApi, args),
  register: (...args: Parameters<typeof authApi.register>) => authApi.register.apply(authApi, args),
  logout: (...args: Parameters<typeof authApi.logout>) => authApi.logout.apply(authApi, args),
  updateProfile: (...args: Parameters<typeof authApi.updateProfile>) =>
    authApi.updateProfile.apply(authApi, args),
  changePassword: (...args: Parameters<typeof authApi.changePassword>) =>
    authApi.changePassword.apply(authApi, args),
  forgotPassword: (...args: Parameters<typeof authApi.forgotPassword>) =>
    authApi.forgotPassword.apply(authApi, args),
  resetPassword: (...args: Parameters<typeof authApi.resetPassword>) =>
    authApi.resetPassword.apply(authApi, args),
  onboardingStatus: (...args: Parameters<typeof authApi.onboardingStatus>) =>
    authApi.onboardingStatus.apply(authApi, args),
  onboardingComplete: (...args: Parameters<typeof authApi.onboardingComplete>) =>
    authApi.onboardingComplete.apply(authApi, args),
  ...flatApi,
  ...flatOverrides,
  rolesApi: rolesApi,
};

export default api;

export {
  authApi,
  interviewApi,
  bookingApi,
  resumeApi,
  billingApi,
  aptitudeApi,
  behavioralApi,
  hrApi,
  codingApi,
  compilerApi,
  questionsApi,
  toolsApi,
  companyMocksApi,
  gamificationApi,
  oaApi,
  enhancedApi,
  freePracticeApi,
  studentApi,
  placementApi,
  indianPlacementApi,
  systemDesignApi,
  systemDesignTestsApi,
  adaptiveApi,
  predictorApi,
  readinessApi,
  personalDashboardApi,
  dsaFingerprintApi,
  playlistsApi,
  submissionsApi,
  featuresApi,
  visualizationsApi,
  distributionsApi,
  analyticsApi,
  aiDebuggerApi,
  conceptsApi,
  learningModulesApi,
  studyApi,
  tracksApi,
  freeTrialApi,
  lessonApi,
  journeyApi,
  missionApi,
  mapApi,
  onboardingApi,
  examMemoriesApi,
  sprintApi,
  serviceOaApi,
  companyLessonsApi,
};
