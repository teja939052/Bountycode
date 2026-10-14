import { lazy } from "react";

const routeImportFns = {
  Login: () => import("./Login"),
  Register: () => import("./Register"),
  Interview: () => import("./Interview"),
  InterviewSession: () => import("./InterviewSession"),
  ResumeBuilder: () => import("./ResumeBuilder"),
  ATSOptimizer: () => import("./ATSOptimizer"),
  AptitudeTest: () => import("./AptitudeTest"),
  CodingChallenge: () => import("./CodingChallenge"),
  Pricing: () => import("./Pricing"),
  NotFound: () => import("./NotFound"),
  Settings: () => import("./Settings"),
  QuestionBank: () => import("./QuestionBank"),
  Compiler: () => import("./Compiler"),
  SolveProblem: () => import("./SolveProblem"),
  ForgotPassword: () => import("./ForgotPassword"),
  ResetPassword: () => import("./ResetPassword"),
  MockOA: () => import("./MockOA"),
  AdminDashboard: () => import("./AdminDashboard"),
  DailyChallenge: () => import('./DailyChallenge'),
  Terms: () => import("./Terms"),
  Privacy: () => import("./Privacy"),
  FreeTrial: () => import("./FreeTrial"),
  Profile: () => import("./Profile"),
  OnboardingQuest: () => import('./OnboardingQuest'),
  PlacementCurriculum: () => import('./PlacementCurriculum'),
  PlacementCampaign: () => import('./PlacementCampaign'),
  PlacementDiagnostic: () => import('./PlacementDiagnostic'),
  MissionPlayer: () => import('./MissionPlayer'),
  HomeRedirect: () => import('./HomeRedirect'),
  CompanyBattlefield: () => import('./CompanyBattlefield'),
  PatternDrill: () => import('./PatternDrill'),
  RoundView: () => import('./RoundView'),
  LessonPlayer: () => import('./LessonPlayer'),
  PracticeMode: () => import('./PracticeMode'),
  UnifiedLessonPlayer: () => import('./UnifiedLessonPlayer'),
  MissionPackPlayer: () => import('./MissionPackPlayer'),
};

const preload: Record<string, () => void> = {};
const preloaded = new Set<string>();
for (const [name, importFn] of Object.entries(routeImportFns)) {
  preload[name] = () => {
    if (preloaded.has(name)) return;
    preloaded.add(name);
    importFn().catch(() => {});
  };
}

export { preload };

const IDLE_PRELOAD_ROUTES = [
  "Login",
  "Register",
  "Pricing",
  "Interview",
  "QuestionBank",
  "ResumeBuilder",
  "ATSOptimizer",
  "AptitudeTest",
  "CodingChallenge",
  "Compiler",
];

function scheduleIdlePreload() {
  const preloadAll = () => {
    IDLE_PRELOAD_ROUTES.forEach(name => preload[name]?.());
  };
  if (typeof window.requestIdleCallback === "function") {
    window.requestIdleCallback(preloadAll, { timeout: 4000 });
  } else {
    setTimeout(preloadAll, 2500);
  }
}

window.addEventListener("load", scheduleIdlePreload);

const Login = lazy(() => import("./Login"));
const Register = lazy(() => import("./Register"));
const Interview = lazy(() => import("./Interview"));
const InterviewSession = lazy(() => import("./InterviewSession"));
const ResumeBuilder = lazy(() => import("./ResumeBuilder"));
const ATSOptimizer = lazy(() => import("./ATSOptimizer"));
const AptitudeTest = lazy(() => import("./AptitudeTest"));
const CodingChallenge = lazy(() => import("./CodingChallenge"));
const Pricing = lazy(() => import("./Pricing"));
const NotFound = lazy(() => import("./NotFound"));
const Settings = lazy(() => import("./Settings"));
const QuestionBank = lazy(() => import("./QuestionBank"));
const Compiler = lazy(() => import("./Compiler"));
const SolveProblem = lazy(() => import("./SolveProblem"));
const ForgotPassword = lazy(() => import("./ForgotPassword"));
const ResetPassword = lazy(() => import("./ResetPassword"));
const VerifyEmail = lazy(() => import("./VerifyEmail"));
const MockOA = lazy(() => import("./MockOA"));
const AdminDashboard = lazy(() => import("./AdminDashboard"));
const DailyChallenge = lazy(() => import('./DailyChallenge'));
const Terms = lazy(() => import("./Terms"));
const Privacy = lazy(() => import("./Privacy"));
const FreeTrial = lazy(() => import("./FreeTrial"));
const Profile = lazy(() => import("./Profile"));
const OnboardingQuest = lazy(() => import('./OnboardingQuest'));
const PlacementCurriculum = lazy(() => import('./PlacementCurriculum'));
const PlacementCampaign = lazy(() => import('./PlacementCampaign'));
const PlacementDiagnostic = lazy(() => import('./PlacementDiagnostic'));
const MissionPlayer = lazy(() => import('./MissionPlayer'));
const HomeRedirect = lazy(() => import('./HomeRedirect'));
const CompanyBattlefield = lazy(() => import('./CompanyBattlefield'));
const PatternDrill = lazy(() => import('./PatternDrill'));
const RoundView = lazy(() => import('./RoundView'));
const LessonPlayer = lazy(() => import('./LessonPlayer'));
const PracticeMode = lazy(() => import('./PracticeMode'));
const UnifiedLessonPlayer = lazy(() => import('./UnifiedLessonPlayer'));
const MissionPackPlayer = lazy(() => import('./MissionPackPlayer'));
export {
  Login,
  Register,
  Interview,
  InterviewSession,
  ResumeBuilder,
  ATSOptimizer,
  AptitudeTest,
  CodingChallenge,
  Pricing,
  NotFound,
  Settings,
  QuestionBank,
  Compiler,
  SolveProblem,
  ForgotPassword,
  ResetPassword,
  VerifyEmail,
  MockOA,
  AdminDashboard,
  DailyChallenge,
  Terms,
  Privacy,
  FreeTrial,
  Profile,
  OnboardingQuest,
  PlacementCurriculum,
  PlacementCampaign,
  PlacementDiagnostic,
  MissionPlayer,
  UnifiedLessonPlayer,
  MissionPackPlayer,
  HomeRedirect,
  CompanyBattlefield,
  PatternDrill,
  RoundView,
  LessonPlayer,
  PracticeMode,
};
