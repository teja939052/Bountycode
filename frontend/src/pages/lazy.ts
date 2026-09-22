import { lazy } from "react";

const routeImportFns = {
  Login: () => import("./Login"),
  Register: () => import("./Register"),
  Interview: () => import("./Interview"),
  InterviewSession: () => import("./InterviewSession"),
  InterviewBooking: () => import("./InterviewBooking"),
  InterviewReplay: () => import("./InterviewReplay"),
  ResumeBuilder: () => import("./ResumeBuilder"),
  ResumeStudio: () => import("./ResumeStudio"),
  ATSOptimizer: () => import("./ATSOptimizer"),
  AptitudeTest: () => import("./AptitudeTest"),
  SystemDesign: () => import("./SystemDesign"),
  CodingChallenge: () => import("./CodingChallenge"),
  Pricing: () => import("./Pricing"),
  PlacementCalendar: () => import("./PlacementCalendar"),
  NotFound: () => import("./NotFound"),
  Settings: () => import("./Settings"),
  History: () => import("./History"),
  Leaderboard: () => import("./Leaderboard"),
  DailyDrill: () => import("./DailyDrill"),
  QuestionBank: () => import("./QuestionBank"),
  PracticeMode: () => import("./PracticeMode"),
  PatternPage: () => import("./PatternPage"),
  CompanyTrack: () => import("./CompanyTrack"),
  MyProgress: () => import("./MyProgress"),
  AlumniExperiences: () => import("./AlumniExperiences"),
  PlacementDrives: () => import("./PlacementDrives"),
  CareerProfile: () => import("./CareerProfile"),
  ApplicationTracker: () => import("./ApplicationTracker"),
  Enterprise: () => import("./Enterprise"),
  Compiler: () => import("./Compiler"),
  SolveProblem: () => import("./SolveProblem"),
  ForgotPassword: () => import("./ForgotPassword"),
  ResetPassword: () => import("./ResetPassword"),
  RoleSelect: () => import("./RoleSelect"),
  MonthlyContests: () => import("./MonthlyContests"),
  IndianPlacement: () => import("./IndianPlacement"),
  MockOA: () => import("./MockOA"),
  ResumeATS: () => import("./ResumeATS"),
  LearningHub: () => import("./LearningHub"),
  LessonPage: () => import("./LessonPage"),
  LessonPlayer: () => import("./LessonPlayer"),
  AdminDashboard: () => import("./AdminDashboard"),
  AdminContentCorpus: () => import("./AdminContentCorpus"),
  Topics: () => import("./Topics"),
  TopicProblems: () => import("./TopicProblems"),
  ProblemOfTheDay: () => import("./ProblemOfTheDay"),
  Tower: () => import("./Tower"),
  SkillGraph: () => import("./SkillGraph"),
  DailyChallenge: () => import("./DailyChallenge"),
  DSAVisualizer: () => import("./DSAVisualizer"),
  ChallengePacks: () => import("./ChallengePacks"),
  AIMentor: () => import("./AIMentor"),
  CodePlayground: () => import("./CodePlayground"),
  CompareVisualizer: () => import("./CompareVisualizer"),
  OnboardingQuest: () => import("./OnboardingQuest"),
  JourneyPage: () => import("./JourneyPage"),
  LevelMap: () => import("./LevelMap"),
  FreeTrial: () => import("./FreeTrial"),
  PwaSetup: () => import("./PwaSetup"),
  StudentDashboard: () => import("./StudentDashboard"),
  StudyTimer: () => import("./StudyTimer"),
  Terms: () => import("./Terms"),
  Privacy: () => import("./Privacy"),
  Practice: () => import("./Practice"),
  PrepHub: () => import("./PrepHub"),
  LearningPaths: () => import("./LearningPaths"),
  CompanyTracks: () => import("./CompanyTracks"),
  Concepts: () => import("./Concepts"),
  TcsNqtSimulation: () => import("./TcsNqtSimulation"),
  ExamMemorySubmission: () => import("./ExamMemorySubmission"),
  AdminExamReview: () => import("./AdminExamReview"),
  ReadinessHeatmap: () => import("./ReadinessHeatmap"),
  EvidenceDashboard: () => import("./EvidenceDashboard"),
  Target: () => import("./Target"),
  Skills: () => import("./Skills"),
  Profile: () => import("./Profile"),
  Mission: () => import("./Mission"),
  MissionResult: () => import("./MissionResult"),
  SlidingWindowMission: () => import("./SlidingWindowMission"),
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
  "SystemDesign",
  "CodingChallenge",
  "LearningPaths",
  "Compiler",
  "LevelMap",
  "Tower",
  "JourneyPage",
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
const ResumeStudio = lazy(() => import("./ResumeStudio"));
const ATSOptimizer = lazy(() => import("./ATSOptimizer"));
const AptitudeTest = lazy(() => import("./AptitudeTest"));
const SystemDesign = lazy(() => import("./SystemDesign"));
const CodingChallenge = lazy(() => import("./CodingChallenge"));
const Pricing = lazy(() => import("./Pricing"));
const PlacementCalendar = lazy(() => import("./PlacementCalendar"));
const NotFound = lazy(() => import("./NotFound"));
const Settings = lazy(() => import("./Settings"));
const History = lazy(() => import("./History"));
const Leaderboard = lazy(() => import("./Leaderboard"));
const DailyDrill = lazy(() => import("./DailyDrill"));
const QuestionBank = lazy(() => import("./QuestionBank"));
const PracticeMode = lazy(() => import("./PracticeMode"));
const PatternPage = lazy(() => import("./PatternPage"));
const CompanyTrack = lazy(() => import("./CompanyTrack"));
const MyProgress = lazy(() => import("./MyProgress"));
const AlumniExperiences = lazy(() => import("./AlumniExperiences"));
const PlacementDrives = lazy(() => import("./PlacementDrives"));
const CareerProfile = lazy(() => import("./CareerProfile"));
const ApplicationTracker = lazy(() => import("./ApplicationTracker"));
const Enterprise = lazy(() => import("./Enterprise"));
const Compiler = lazy(() => import("./Compiler"));
const SolveProblem = lazy(() => import("./SolveProblem"));
const ForgotPassword = lazy(() => import("./ForgotPassword"));
const ResetPassword = lazy(() => import("./ResetPassword"));
const RoleSelect = lazy(() => import("./RoleSelect"));
const MonthlyContests = lazy(() => import("./MonthlyContests"));
const IndianPlacement = lazy(() => import("./IndianPlacement"));
const MockOA = lazy(() => import("./MockOA"));
const ResumeATS = lazy(() => import("./ResumeATS"));
const LearningHub = lazy(() => import("./LearningHub"));
const LessonPage = lazy(() => import("./LessonPage"));
const LessonPlayer = lazy(() => import("./LessonPlayer"));
const AdminDashboard = lazy(() => import("./AdminDashboard"));
const AdminContentCorpus = lazy(() => import("./AdminContentCorpus"));
const Topics = lazy(() => import("./Topics"));
const TopicProblems = lazy(() => import("./TopicProblems"));
const ProblemOfTheDay = lazy(() => import('./ProblemOfTheDay'));
const Tower = lazy(() => import('./Tower'));
const SkillGraph = lazy(() => import('./SkillGraph'));
const DailyChallenge = lazy(() => import('./DailyChallenge'));
const DSAVisualizer = lazy(() => import('./DSAVisualizer'));
const ChallengePacks = lazy(() => import('./ChallengePacks'));
const AIMentor = lazy(() => import('./AIMentor'));
const CodePlayground = lazy(() => import('./CodePlayground'));
const CompareVisualizer = lazy(() => import('./CompareVisualizer'));
const OnboardingQuest = lazy(() => import('./OnboardingQuest'));
const InterviewBooking = lazy(() => import('./InterviewBooking'));
const InterviewReplay = lazy(() => import('./InterviewReplay'));
const JourneyPage = lazy(() => import('./JourneyPage'));
const LevelMap = lazy(() => import('./LevelMap'));
const FreeTrial = lazy(() => import('./FreeTrial'));
const PwaSetup = lazy(() => import('./PwaSetup'));
const StudentDashboard = lazy(() => import('./StudentDashboard'));
const StudyTimer = lazy(() => import('./StudyTimer'));
const Terms = lazy(() => import('./Terms'));
const Privacy = lazy(() => import('./Privacy'));
const Practice = lazy(() => import('./Practice'));
const PrepHub = lazy(() => import('./PrepHub'));
const LearningPaths = lazy(() => import('./LearningPaths'));
const CompanyTracks = lazy(() => import('./CompanyTracks'));
const Concepts = lazy(() => import('./Concepts'));
const TcsNqtSimulation = lazy(() => import('./TcsNqtSimulation'));
const ExamMemorySubmission = lazy(() => import('./ExamMemorySubmission'));
const AdminExamReview = lazy(() => import('./AdminExamReview'));
const ReadinessHeatmap = lazy(() => import('./ReadinessHeatmap'));
const EvidenceDashboard = lazy(() => import('./EvidenceDashboard'));
const Target = lazy(() => import('./Target'));
const Skills = lazy(() => import('./Skills'));
const Profile = lazy(() => import('./Profile'));
const Mission = lazy(() => import('./Mission'));
const MissionResult = lazy(() => import('./MissionResult'));
const SlidingWindowMission = lazy(() => import('./SlidingWindowMission'));
export {
  Login,
  Register,
  Interview,
  InterviewSession,
  ResumeBuilder,
  ResumeStudio,
  ATSOptimizer,
  AptitudeTest,
  SystemDesign,
  CodingChallenge,
  Pricing,
  PlacementCalendar,
  NotFound,
  Settings,
  History,
  Leaderboard,
  DailyDrill,
  QuestionBank,
  PracticeMode,
  PatternPage,
  CompanyTrack,
  MyProgress,
  AlumniExperiences,
  PlacementDrives,
  CareerProfile,
  ApplicationTracker,
  Enterprise,
  Compiler,
  SolveProblem,
  ForgotPassword,
  ResetPassword,
  RoleSelect,
  MonthlyContests,
  IndianPlacement,
  MockOA,
  ResumeATS,
  LearningHub,
  LessonPage,
  LessonPlayer,
  AdminDashboard,
  AdminContentCorpus,
  Topics,
  TopicProblems,
  ProblemOfTheDay,
  Tower,
  SkillGraph,
  DailyChallenge,
  DSAVisualizer,
  ChallengePacks,
  AIMentor,
  CodePlayground,
  CompareVisualizer,
  OnboardingQuest,
  InterviewBooking,
  InterviewReplay,
  JourneyPage,
  LevelMap,
  FreeTrial,
  PwaSetup,
  StudentDashboard,
  StudyTimer,
  Terms,
  Privacy,
  Practice,
  PrepHub,
  LearningPaths,
  CompanyTracks,
  Concepts,
  TcsNqtSimulation,
  ExamMemorySubmission,
  AdminExamReview,
  ReadinessHeatmap,
  EvidenceDashboard,
  Target,
  Skills,
  Profile,
  Mission,
  MissionResult,
  SlidingWindowMission,
};
