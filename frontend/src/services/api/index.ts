import { authApi } from "./auth.ts";
import { interviewApi, mockInterviewApi, bookingApi } from "./interview.ts";
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
import { toolsApi, salaryApi } from "./tools.ts";
import { companyPrepApi, companyMocksApi } from "./companyPrep.ts";
import { gamificationApi } from "./gamification.ts";
import { enhancedApi, freePracticeApi } from "./enhanced.ts";
import { studentApi } from "./student.ts";
import { placementApi, indianPlacementApi } from "./placement.ts";
import { systemDesignApi, systemDesignTestsApi } from "./systemDesign.ts";
import { communityApi, dailyApi, learningApi } from "./community.ts";
import { adaptiveApi, predictorApi, readinessApi } from "./adaptive.ts";
import {
  mockInterviewApi as mockIntApi,
  personalDashboardApi,
  dsaFingerprintApi,
  battlesApi,
  scrimsApi,
  rankApi,
  projectGeneratorApi,
  mysteryBoxApi,
  energyApi,
  playlistsApi,
  discussionsApi,
  submissionsApi,
  featuresApi,
  visualizationsApi,
  distributionsApi,
  analyticsApi,
  aiDebuggerApi,
  conceptsApi,
} from "./misc.ts";
import { learningModulesApi } from "./learningModules.ts";
import { studyApi } from "./study.ts";
import { languagePathsApi } from "./languagePathsApi.ts";
import { freeTrialApi } from "./freeTrial.ts";
import { onboardingApi } from "./onboarding.ts";
import { showcaseApi } from "./showcase.ts";
import { adminContentApi, assignmentsApi } from "./adminContent.ts";
import { gameEventsApi } from "./gameEvents.ts";
import { campusApi } from "./campus.ts";
import { companyDirectoryApi } from "./companyDirectory.ts";
import { worldApi } from "./world.ts";
import { merchantApi } from "./merchant.ts";
import { guildsApi } from "./guilds.ts";
import { dungeonsApi } from "./dungeons.ts";
import { collectionApi, eventsApi } from "./collectionEvents.ts";
import { metricsApi } from "./metrics.ts";
import { economyApi } from "./economy.ts";
import { journeyApi } from "./journey.ts";
import { careerApi } from "./career.ts";
import { timelineApi } from "./timeline.ts";
import { collegeNetworkApi } from "./collegeNetwork.ts";
import { newspaperApi } from "./newspaper.ts";
import { steamApi } from "./steam.ts";
import { luckyWheelApi } from "./luckyWheel.ts";
import { battlePassApi } from "./battlePass.ts";
import { referralSystemApi } from "./referralSystem.ts";
import { guildCastleApi } from "./guildCastle.ts";
import { chatApi } from "./chat.ts";
import { gdApi } from "./gdRooms.ts";
import { cgpaApi } from "./cgpa.ts";
import { driveApi } from "./driveTracker.ts";
import { peerReviewApi } from "./peerReview.ts";
import { studySquadsApi } from "./studySquads.ts";
import { reportCardApi } from "./reportCard.ts";
import { seasonsApi } from "./seasons.ts";
import { achievementsApi } from "./achievements.ts";
import { tournamentsApi } from "./tournaments.ts";
import { teamsApi } from "./teams.ts";
import { referralApi } from "./referrals.ts";
import { skillTreesApi } from "./skillTrees.ts";
import { shareableAchievementsApi } from "./shareableAchievements.ts";
import { campusPulseApi } from "./campusPulse.ts";
import { trendingChallengesApi } from "./trendingChallenges.ts";
import { flatApi } from "./flat.ts";
import { flatOverrides } from "./flatOverrides.ts";
import { friendsApi } from "./friends.ts";
import { studyTimerApi } from "./studyTimer.ts";
import { goalsApi } from "./goals.ts";
import { themesApi } from "./themes.ts";
import { bountyApi } from "./bounty.ts";
import { interviewChatApi } from "./interviewChat.ts";
import { massRecruiterApi } from "./massRecruiter.ts";

const api = {
  auth: authApi,
  interview: interviewApi,
  interviewChat: interviewChatApi,
  mockInterview: mockInterviewApi,
  booking: bookingApi,
  resume: resumeApi,
  billing: billingApi,
  aptitude: aptitudeApi,
  massRecruiter: massRecruiterApi,
  behavioral: behavioralApi,
  hr: hrApi,
  coding: codingApi,
  compiler: compilerApi,
  questions: questionsApi,
  tools: toolsApi,
  salary: salaryApi,
  companyPrep: companyPrepApi,
  companyMocks: companyMocksApi,
  gamification: gamificationApi,
  battlePass: battlePassApi,
  referral: referralSystemApi,
  guildCastle: guildCastleApi,
  enhanced: enhancedApi,
  freePractice: freePracticeApi,
  student: studentApi,
  placement: placementApi,
  indianPlacement: indianPlacementApi,
  systemDesign: systemDesignApi,
  systemDesignTests: systemDesignTestsApi,
  community: communityApi,
  daily: dailyApi,
  learning: learningApi,
  adaptive: adaptiveApi,
  predictor: predictorApi,
  readiness: readinessApi,
  personalDashboard: personalDashboardApi,
  dsaFingerprint: dsaFingerprintApi,
  battles: battlesApi,
  scrims: scrimsApi,
  rank: rankApi,
  projectGenerator: projectGeneratorApi,
  mysteryBox: mysteryBoxApi,
  energy: energyApi,
  playlists: playlistsApi,
  discussions: discussionsApi,
  submissions: submissionsApi,
  features: featuresApi,
  visualizations: visualizationsApi,
  distributions: distributionsApi,
  analytics: analyticsApi,
  aiDebugger: aiDebuggerApi,
  concepts: conceptsApi,
  learningModules: learningModulesApi,
  study: studyApi,
  languagePaths: languagePathsApi,
  freeTrial: freeTrialApi,
  onboarding: onboardingApi,
  showcase: showcaseApi,
  adminContent: adminContentApi,
  assignments: assignmentsApi,
  gameEvents: gameEventsApi,
  campus: campusApi,
  companyDirectory: companyDirectoryApi,
  world: worldApi,
  merchant: merchantApi,
  guilds: guildsApi,
  dungeons: dungeonsApi,
  collection: collectionApi,
  events: eventsApi,
  metrics: metricsApi,
  economy: economyApi,
  seasons: seasonsApi,
  journey: journeyApi,
  career: careerApi,
  timeline: timelineApi,
  college: collegeNetworkApi,
  newspaper: newspaperApi,
  steam: steamApi,
  chat: chatApi,
  gd: gdApi,
  cgpa: cgpaApi,
  driveTracker: driveApi,
  peerReview: peerReviewApi,
  studySquads: studySquadsApi,
  reportCard: reportCardApi,
  wheel: luckyWheelApi,
  pass: battlePassApi,
  achievements: achievementsApi,
  tournaments: tournamentsApi,
  teams: teamsApi,
  referrals: referralApi,
  skillTrees: skillTreesApi,
  shareableAchievements: shareableAchievementsApi,
  campusPulse: campusPulseApi,
  trendingChallenges: trendingChallengesApi,
  getMe: () => authApi.getMe(),
  register: (...args: Parameters<typeof authApi.register>) =>
    authApi.register.apply(authApi, args),
  login: (...args: Parameters<typeof authApi.login>) =>
    authApi.login.apply(authApi, args),
  logout: (...args: Parameters<typeof authApi.logout>) =>
    authApi.logout.apply(authApi, args),
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
  onboardingComplete: (
    ...args: Parameters<typeof authApi.onboardingComplete>
  ) => authApi.onboardingComplete.apply(authApi, args),
  ...flatApi,
  ...flatOverrides,
  friends: friendsApi,
  studyTimer: studyTimerApi,
  goals: goalsApi,
  themes: themesApi,
  bounty: bountyApi,
};

export default api;
export {
  authApi,
  interviewApi,
  interviewChatApi,
  mockInterviewApi,
  bookingApi,
  resumeApi,
  billingApi,
  aptitudeApi,
  massRecruiterApi,  codingApi,
  behavioralApi,
  hrApi,
  compilerApi,
  questionsApi,
  toolsApi,
  salaryApi,
  companyPrepApi,
  companyMocksApi,
  gamificationApi,
  enhancedApi,
  freePracticeApi,
  studentApi,
  placementApi,
  indianPlacementApi,
  systemDesignApi,
  systemDesignTestsApi,
  communityApi,
  dailyApi,
  learningApi,
  adaptiveApi,
  predictorApi,
  readinessApi,
  mockIntApi,
  personalDashboardApi,
  dsaFingerprintApi,
  battlesApi,
  scrimsApi,
  rankApi,
  projectGeneratorApi,
  mysteryBoxApi,
  energyApi,
  playlistsApi,
  discussionsApi,
  submissionsApi,
  featuresApi,
  visualizationsApi,
  distributionsApi,
  analyticsApi,
  aiDebuggerApi,
  conceptsApi,
  learningModulesApi,
  studyApi,
  languagePathsApi,
  freeTrialApi,
  onboardingApi,
  timelineApi,
  chatApi,
  peerReviewApi,
  studySquadsApi,
  friendsApi,
  reportCardApi,
  studyTimerApi,
  goalsApi,
  themesApi,
  bountyApi,
};
