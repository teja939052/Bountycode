import { lazy } from "react";

const routeImportFns = {
  CurriculumHub: () => import("./CurriculumHub"),
  LearnTrack: () => import("./LearnTrack"),
  LearnLesson: () => import("./LearnLesson"),
  Login: () => import("./Login"),
  Register: () => import("./Register"),
  Dashboard: () => import("./Dashboard"),
  Interview: () => import("./Interview"),
  InterviewSession: () => import("./InterviewSession"),
  ResumeBuilder: () => import("./ResumeBuilder"),
  ResumeStudio: () => import("./ResumeStudio"),
  ATSOptimizer: () => import("./ATSOptimizer"),
  AptitudeTest: () => import("./AptitudeTest"),
  CoverLetter: () => import("./CoverLetter"),
  SystemDesign: () => import("./SystemDesign"),
  CodingChallenge: () => import("./CodingChallenge"),
  Pricing: () => import("./Pricing"),
  PlacementCalendar: () => import("./PlacementCalendar"),
  NotFound: () => import("./NotFound"),
  Settings: () => import("./Settings"),
  History: () => import("./History"),
  Leaderboard: () => import("./Leaderboard"),
  DailyDrill: () => import("./DailyDrill"),
  StudyGroups: () => import("./StudyGroups"),
  Predictor: () => import("./Predictor"),
  QuestionBank: () => import("./QuestionBank"),
  PracticeMode: () => import("./PracticeMode"),
  MyProgress: () => import("./MyProgress"),
  AlumniExperiences: () => import("./AlumniExperiences"),
  PlacementDrives: () => import("./PlacementDrives"),
  CareerProfile: () => import("./CareerProfile"),
  ApplicationTracker: () => import("./ApplicationTracker"),
  Analytics: () => import("./Analytics"),
  Enterprise: () => import("./Enterprise"),
  Compiler: () => import("./Compiler"),
  SolveProblem: () => import("./SolveProblem"),
  ForgotPassword: () => import("./ForgotPassword"),
  ResetPassword: () => import("./ResetPassword"),
  MonthlyContests: () => import("./MonthlyContests"),
  IndianPlacement: () => import("./IndianPlacement"),
  TowerDashboard: () => import("./TowerDashboard"),
  MockOA: () => import("./MockOA"),
  ResumeATS: () => import("./ResumeATS"),
  LearningHub: () => import("./LearningHub"),
  LanguageJourney: () => import("./LanguageJourney"),
  LessonView: () => import("./LessonView"),
  StudyLibrary: () => import("./StudyLibrary"),
  AdminDashboard: () => import("./AdminDashboard"),
  Topics: () => import("./Topics"),
  TopicProblems: () => import("./TopicProblems"),
  PersonalDashboard: () => import("./PersonalDashboard"),
  AdaptivePath: () => import("./AdaptivePath"),
   LearningModules: () => import("./LearningModules"),
   ProblemOfTheDay: () => import("./ProblemOfTheDay"),
  DailyChallenge: () => import("./DailyChallenge"),
  DSAVisualizer: () => import("./DSAVisualizer"),
  ChallengePacks: () => import("./ChallengePacks"),
  AIMentor: () => import("./AIMentor"),
  CodePlayground: () => import("./CodePlayground"),
  CompareVisualizer: () => import("./CompareVisualizer"),
  Community: () => import("./Community"),

  LanguageLearning: () => import("./LanguageLearning"),
  OnboardingQuest: () => import("./OnboardingQuest"),
  InterviewBooking: () => import("./InterviewBooking"),

  InterviewReplay: () => import("./InterviewReplay"),
  FreeTrial: () => import("./FreeTrial"),
  PwaSetup: () => import("./PwaSetup"),
  AdminContent: () => import("./AdminContent"),
  MyAssignments: () => import("./MyAssignments"),

  StudentDashboard: () => import("./StudentDashboard"),

  StudyTimer: () => import("./StudyTimer"),

  Terms: () => import("./Terms"),
  Privacy: () => import("./Privacy"),
  Blogs: () => import("./Blogs"),
  ArticlePage: () => import("./ArticlePage"),
  PercentagesAcademy: () => import("./PercentagesAcademy"),
  CodingAcademy: () => import("./CodingAcademy"),
  TargetPage: () => import("./TargetPage"),
  LoopsVertical: () => import("./LoopsVertical"),
  GamificationDashboard: () => import("./GamificationDashboard"),
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
  "Dashboard",
  "Login",
  "Register",
  "Pricing",
  "Interview",
  "QuestionBank",
  "ResumeBuilder",
  "ATSOptimizer",
  "AptitudeTest",
  "SystemDesign",
  "CodingChallenge",
  "TowerDashboard",
  "LearningHub",
  "Compiler",
  "Community",
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
const CurriculumHub = lazy(() => import("./CurriculumHub"));
const LearnTrack = lazy(() => import("./LearnTrack"));
const LearnLesson = lazy(() => import("./LearnLesson"));
const Register = lazy(() => import("./Register"));
const Dashboard = lazy(() => import("./Dashboard"));
const Interview = lazy(() => import("./Interview"));
const InterviewSession = lazy(() => import("./InterviewSession"));
const ResumeBuilder = lazy(() => import("./ResumeBuilder"));
const ResumeStudio = lazy(() => import("./ResumeStudio"));
const ATSOptimizer = lazy(() => import("./ATSOptimizer"));
const AptitudeTest = lazy(() => import("./AptitudeTest"));
const CoverLetter = lazy(() => import("./CoverLetter"));
const SystemDesign = lazy(() => import("./SystemDesign"));
const CodingChallenge = lazy(() => import("./CodingChallenge"));
const Pricing = lazy(() => import("./Pricing"));
const PlacementCalendar = lazy(() => import("./PlacementCalendar"));
const NotFound = lazy(() => import("./NotFound"));
const Settings = lazy(() => import("./Settings"));
const History = lazy(() => import("./History"));
const Leaderboard = lazy(() => import("./Leaderboard"));
const DailyDrill = lazy(() => import("./DailyDrill"));
const StudyGroups = lazy(() => import("./StudyGroups"));
const Predictor = lazy(() => import("./Predictor"));
const QuestionBank = lazy(() => import("./QuestionBank"));
const PracticeMode = lazy(() => import("./PracticeMode"));
const MyProgress = lazy(() => import("./MyProgress"));
const AlumniExperiences = lazy(() => import("./AlumniExperiences"));
const PlacementDrives = lazy(() => import("./PlacementDrives"));
const CareerProfile = lazy(() => import("./CareerProfile"));
const ApplicationTracker = lazy(() => import("./ApplicationTracker"));
const Analytics = lazy(() => import("./Analytics"));
const Enterprise = lazy(() => import("./Enterprise"));
const Compiler = lazy(() => import("./Compiler"));
const SolveProblem = lazy(() => import("./SolveProblem"));
const ForgotPassword = lazy(() => import("./ForgotPassword"));
const ResetPassword = lazy(() => import("./ResetPassword"));
const MonthlyContests = lazy(() => import("./MonthlyContests"));
const IndianPlacement = lazy(() => import("./IndianPlacement"));
const TowerDashboard = lazy(() => import("./TowerDashboard"));
const MockOA = lazy(() => import("./MockOA"));
const ResumeATS = lazy(() => import("./ResumeATS"));
const LearningHub = lazy(() => import("./LearningHub"));
const LanguageJourney = lazy(() => import("./LanguageJourney"));
const LessonView = lazy(() => import("./LessonView"));
const LessonPlayer = lazy(() => import("./LessonPlayer"));
const Lessons = lazy(() => import("./Lessons"));
const StudyLibrary = lazy(() => import("./StudyLibrary"));
const AdminDashboard = lazy(() => import("./AdminDashboard"));
const Topics = lazy(() => import("./Topics"));
const TopicProblems = lazy(() => import("./TopicProblems"));
const PersonalDashboard = lazy(() => import("./PersonalDashboard"));
const StudentDashboard = lazy(() => import("./StudentDashboard"));
const AdaptivePath = lazy(() => import("./AdaptivePath"));
const LearningModules = lazy(() => import("./LearningModules"));
const ProblemOfTheDay = lazy(() => import('./ProblemOfTheDay'));
const DailyChallenge = lazy(() => import('./DailyChallenge'));
const DSAVisualizer = lazy(() => import('./DSAVisualizer'));
const ChallengePacks = lazy(() => import('./ChallengePacks'));
const AIMentor = lazy(() => import('./AIMentor'));
const CodePlayground = lazy(() => import('./CodePlayground'));
const CompareVisualizer = lazy(() => import('./CompareVisualizer'));
const Community = lazy(() => import('./Community'));
const LanguageLearning = lazy(() => import('./LanguageLearning'));
const OnboardingQuest = lazy(() => import('./OnboardingQuest'));
const InterviewBooking = lazy(() => import('./InterviewBooking'));
const InterviewReplay = lazy(() => import('./InterviewReplay'));
const FreeTrial = lazy(() => import('./FreeTrial'));
const PwaSetup = lazy(() => import('./PwaSetup'));
const AdminContent = lazy(() => import('./AdminContent'));
const MyAssignments = lazy(() => import('./MyAssignments'));
const Concepts = lazy(() => import('./Concepts'));
const StudyTimer = lazy(() => import('./StudyTimer'));
const StudyGoals = lazy(() => import('./StudyGoals'));
const Home = lazy(() => import('./Home'));
const Prepare = lazy(() => import('./Prepare'));
const Practice = lazy(() => import('./Practice'));
const Compete = lazy(() => import('./Compete'));
const Career = lazy(() => import('./Career'));
const Terms = lazy(() => import('./Terms'));
const Privacy = lazy(() => import('./Privacy'));
const Blogs = lazy(() => import('./Blogs'));
const ArticlePage = lazy(() => import('./ArticlePage'));
const PercentagesAcademy = lazy(() => import('./PercentagesAcademy'));
const CodingAcademy = lazy(() => import('./CodingAcademy'));
const TargetPage = lazy(() => import('./TargetPage'));
const LoopsVertical = lazy(() => import('./LoopsVertical'));
const GamificationDashboard = lazy(() => import('./GamificationDashboard'));
const ContentBundles = lazy(() => import('./ContentBundles'));
const SkillMap = lazy(() => import('./SkillMap'));
export {
  CurriculumHub,
  LearnTrack,
  LearnLesson,
  CompareVisualizer,
  Community,
  ProblemOfTheDay,
  DailyChallenge,
  DSAVisualizer,
  ChallengePacks,
  AIMentor,
  Login,
  Register,
  Dashboard,
  Interview,
  InterviewSession,
  ResumeBuilder,
  ResumeStudio,
  ATSOptimizer,
  AptitudeTest,
  CoverLetter,
  SystemDesign,
  CodingChallenge,
  Pricing,  PlacementCalendar,
  NotFound,
  Settings,
  History,
  Leaderboard,
  DailyDrill,
  StudyGroups,
  Predictor,
  QuestionBank,
  PracticeMode,
  MyProgress,
  AlumniExperiences,
  PlacementDrives,
  CareerProfile,
  ApplicationTracker,
  Analytics,
  Enterprise,
  Compiler,
  SolveProblem,
  ForgotPassword,
  ResetPassword,
  MonthlyContests,
  IndianPlacement,
  TowerDashboard,
  MockOA,
  ResumeATS,
  LearningHub,
  LanguageJourney,
  LessonView,
  LessonPlayer,
  Lessons,
  StudyLibrary,
  AdminDashboard,
  Topics,
  TopicProblems,
  PersonalDashboard,
  StudentDashboard,
  AdaptivePath,
  LearningModules,
  CodePlayground,
  LanguageLearning,
  OnboardingQuest,
  InterviewBooking,
  InterviewReplay,
  FreeTrial,
  PwaSetup,
  AdminContent,
  MyAssignments,
  StudyTimer,
  StudyGoals,
  Home,
  Prepare,
  Practice,
  Compete,
  Career,
  Concepts,
  Terms,
  Privacy,
  Blogs,
  ArticlePage,
  PercentagesAcademy,
  CodingAcademy,
  TargetPage,
  LoopsVertical,
  GamificationDashboard,
  ContentBundles,
  SkillMap,
};
