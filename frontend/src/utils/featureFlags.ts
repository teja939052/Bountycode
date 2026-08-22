/**
 * Feature flags for managing 50+ features.
 *
 * Usage:
 *   import { features } from "@/utils/featureFlags";
 *   if (features.dsaVisualizer) { ... }
 */

export type FeatureFlag = {
  key: string;
  enabled: boolean;
  description: string;
  rolloutPercent?: number;
  allowedPlans?: ("free" | "pro" | "lifetime")[];
};

export const features: Record<string, FeatureFlag> = {
  // Core features (always on)
  interviews: { key: "interviews", enabled: true, description: "AI mock interviews" },
  resume: { key: "resume", enabled: true, description: "Resume builder and analyzer" },
  aptitude: { key: "aptitude", enabled: true, description: "Aptitude test practice" },
  coding: { key: "coding", enabled: true, description: "Coding challenges" },
  compiler: { key: "compiler", enabled: true, description: "LeetCode-style compiler" },
  questions: { key: "questions", enabled: true, description: "Question bank" },

  // AI features
  aiMentor: { key: "aiMentor", enabled: true, description: "AI mentor chat" },
  projectGenerator: { key: "projectGenerator", enabled: true, description: "AI project generator" },
  coverLetter: { key: "coverLetter", enabled: true, description: "Cover letter generator" },
  salaryNegotiation: { key: "salaryNegotiation", enabled: true, description: "Salary negotiation coach" },
  systemDesign: { key: "systemDesign", enabled: true, description: "System design practice" },
  companyPrep: { key: "companyPrep", enabled: true, description: "Company-specific prep" },
  aiDebugger: { key: "aiDebugger", enabled: true, description: "AI-powered debugger" },
  aiFeedback: { key: "aiFeedback", enabled: true, description: "Real-time AI feedback" },

  // Gamification
  gamification: { key: "gamification", enabled: true, description: "XP, levels, streaks, badges" },
  tower: { key: "tower", enabled: true, description: "Placement tower progression" },
  battlePass: { key: "battlePass", enabled: true, description: "Battle pass system" },
  dailyChallenges: { key: "dailyChallenges", enabled: true, description: "Daily adaptive challenges" },
  mysteryBoxes: { key: "mysteryBoxes", enabled: true, description: "Mystery box rewards" },
  powerUps: { key: "powerUps", enabled: true, description: "Power-up shop" },
  bossBattles: { key: "bossBattles", enabled: true, description: "Boss battles at levels 10,20..." },
  leaderboard: { key: "leaderboard", enabled: true, description: "Global leaderboard" },
  rank: { key: "rank", enabled: true, description: "Honor/Kyu-Dan rank system" },

  // Social/Community
  community: { key: "community", enabled: true, description: "Community discussions" },
  studyGroups: { key: "studyGroups", enabled: true, description: "Study groups" },
  battles: { key: "battles", enabled: true, description: "1v1 coding battles" },
  tournaments: { key: "tournaments", enabled: true, description: "Monthly contests" },
  scrims: { key: "scrims", enabled: true, description: "Scrimba-style screencasts" },
  chat: { key: "chat", enabled: true, description: "Real-time chat" },
  referrals: { key: "referrals", enabled: true, description: "Referral program" },

  // Learning
  learningHub: { key: "learningHub", enabled: true, description: "Learning hub" },
  languagePaths: { key: "languagePaths", enabled: true, description: "7 language learning paths" },
  learningModules: { key: "learningModules", enabled: true, description: "Duolingo-style lessons" },
  adaptivePath: { key: "adaptivePath", enabled: true, description: "AI-driven adaptive learning" },
  dsaFingerprint: { key: "dsaFingerprint", enabled: true, description: "DSA skill assessment" },
  dsaVisualizer: { key: "dsaVisualizer", enabled: true, description: "Algorithm visualizations" },
  concepts: { key: "concepts", enabled: true, description: "Concept explanations" },
  spacedRepetition: { key: "spacedRepetition", enabled: true, description: "SRS mastery system" },

  // Career tools
  atsOptimizer: { key: "atsOptimizer", enabled: true, description: "ATS score optimizer" },
  salaryBenchmark: { key: "salaryBenchmark", enabled: true, description: "Salary benchmark data" },
  applicationTracker: { key: "applicationTracker", enabled: true, description: "Job application tracker" },
  careerProfile: { key: "careerProfile", enabled: true, description: "Career profile" },
  interviewBooking: { key: "interviewBooking", enabled: true, description: "Interview booking system" },
  mockOA: { key: "mockOA", enabled: true, description: "Mock online assessments" },
  predictor: { key: "predictor", enabled: true, description: "Placement prediction engine" },
  readiness: { key: "readiness", enabled: true, description: "Interview readiness scoring" },

  // Indian market
  indianPlacement: { key: "indianPlacement", enabled: true, description: "Indian placement prep" },
  campusConnect: { key: "campusConnect", enabled: true, description: "Campus connect" },
  campusWars: { key: "campusWars", enabled: true, description: "Campus wars leaderboard" },
  placementDrives: { key: "placementDrives", enabled: true, description: "Placement drives" },
  alumniExperiences: { key: "alumniExperiences", enabled: true, description: "Alumni experiences" },

  // Advanced features
  worldMap: { key: "worldMap", enabled: true, description: "World map exploration" },
  skillTrees: { key: "skillTrees", enabled: true, description: "Visual skill trees" },
  dungeons: { key: "dungeons", enabled: true, description: "Dungeon challenges" },
  guilds: { key: "guilds", enabled: true, description: "Guild system" },
  economy: { key: "economy", enabled: true, description: "Player economy" },
  seasons: { key: "seasons", enabled: true, description: "Seasonal events" },
  gameEvents: { key: "gameEvents", enabled: true, description: "Game events" },
  cardCollection: { key: "cardCollection", enabled: true, description: "Card collection" },
  showcase: { key: "showcase", enabled: true, description: "Project showcase gallery" },
  timelines: { key: "timelines", enabled: true, description: "Placement timeline" },

  // Admin/Enterprise
  adminDashboard: { key: "adminDashboard", enabled: true, description: "Admin analytics dashboard", allowedPlans: ["pro", "lifetime"] },
  adminContent: { key: "adminContent", enabled: true, description: "Admin content management", allowedPlans: ["pro", "lifetime"] },
  enterprise: { key: "enterprise", enabled: true, description: "Enterprise plan features", allowedPlans: ["pro", "lifetime"] },
  billing: { key: "billing", enabled: true, description: "PayPal/Stripe billing" },

  // Experimental
  pwa: { key: "pwa", enabled: true, description: "Progressive Web App" },
  pushNotifications: { key: "pushNotifications", enabled: true, description: "Push notifications" },
  offlineMode: { key: "offlineMode", enabled: true, description: "Offline mode" },
  steamProfile: { key: "steamProfile", enabled: true, description: "Steam-style profile" },
  newspaper: { key: "newspaper", enabled: true, description: "Placement Times newspaper" },
  luckyWheel: { key: "luckyWheel", enabled: true, description: "Daily lucky wheel" },
  retentionAdmin: { key: "retentionAdmin", enabled: true, description: "Retention analytics admin", allowedPlans: ["pro", "lifetime"] },
};

export function isFeatureEnabled(flagKey: string, userPlan: string = "free"): boolean {
  const flag = features[flagKey];
  if (!flag) return false;
  if (!flag.enabled) return false;

  if (flag.allowedPlans && !flag.allowedPlans.includes(userPlan as "free" | "pro" | "lifetime")) {
    return false;
  }

  if (flag.rolloutPercent !== undefined) {
    return Math.random() * 100 < flag.rolloutPercent;
  }

  return true;
}

export function getEnabledFeatures(userPlan: string = "free"): string[] {
  return Object.entries(features)
    .filter(([key, _]) => isFeatureEnabled(key, userPlan))
    .map(([key]) => key);
}

export function setFeatureEnabled(key: string, enabled: boolean): void {
  if (features[key]) {
    features[key].enabled = enabled;
  }
}
