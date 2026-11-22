/**
 * Frontend Route Catalog — BountyCode
 *
 * Centralized, typed route registry. Every frontend route maps to:
 *
 *   • Stable route ID
 *   • URL path
 *   • Feature owner (hub)
 *   • Authentication requirement
 *   • Authorization requirement
 *   • Lazy page component
 *   • Error boundary
 *   • Data dependencies (backend APIs)
 *   • Loading state
 *   • Empty state
 *   • Unavailable state
 *   • Canonical navigation location
 *
 * This catalog is the single source of truth for route→API→engine dependencies.
 * No route should be defined outside this catalog. URL construction uses the
 * helpers in `helpers.ts` — never manual string concatenation.
 */
import { lazy } from "react";
import { Navigate } from "react-router-dom";
import ProtectedRoute from "../components/ProtectedRoute";
import FeatureErrorBoundary from "../components/FeatureErrorBoundary";
import RouteErrorBoundary from "../components/RouteErrorBoundary";

/**
 * Lazy page imports (all from pages/lazy.ts)
 */
const Landing = lazy(() => import("../pages/Landing"));
const Login = lazy(() => import("../pages/Login"));
const Register = lazy(() => import("../pages/Register"));
const ForgotPassword = lazy(() => import("../pages/ForgotPassword"));
const ResetPassword = lazy(() => import("../pages/ResetPassword"));
const Pricing = lazy(() => import("../pages/Pricing"));
const FreeTrial = lazy(() => import("../pages/FreeTrial"));
const Terms = lazy(() => import("../pages/Terms"));
const Privacy = lazy(() => import("../pages/Privacy"));
const Blogs = lazy(() => import("../pages/Blogs"));
const ArticlePage = lazy(() => import("../pages/ArticlePage"));
const PercentagesAcademy = lazy(() => import("../pages/PercentagesAcademy"));
const CodingAcademy = lazy(() => import("../pages/CodingAcademy"));
const TargetPage = lazy(() => import("../pages/TargetPage"));
const LoopsVertical = lazy(() => import("../pages/LoopsVertical"));
const GamificationDashboard = lazy(() =>
  import("../pages/GamificationDashboard")
);
const ContentBundles = lazy(() => import("../pages/ContentBundles"));

const Dashboard = lazy(() => import("../pages/Dashboard"));
const StudentDashboard = lazy(() => import("../pages/StudentDashboard"));
const PersonalDashboard = lazy(() => import("../pages/PersonalDashboard"));
const SkillMap = lazy(() => import("../pages/SkillMap"));
const MyProgress = lazy(() => import("../pages/MyProgress"));
const History = lazy(() => import("../pages/History"));
const Leaderboard = lazy(() => import("../pages/Leaderboard"));
const Home = lazy(() => import("../pages/Home"));
const Prepare = lazy(() => import("../pages/Prepare"));
const Practice = lazy(() => import("../pages/Practice"));
const Compete = lazy(() => import("../pages/Compete"));
const Career = lazy(() => import("../pages/Career"));
const Concepts = lazy(() => import("../pages/Concepts"));

const Interview = lazy(() => import("../pages/Interview"));
const InterviewSession = lazy(() => import("../pages/InterviewSession"));
const InterviewBooking = lazy(() => import("../pages/InterviewBooking"));
const InterviewReplay = lazy(() => import("../pages/InterviewReplay"));

const ResumeBuilder = lazy(() => import("../pages/ResumeBuilder"));
const ResumeStudio = lazy(() => import("../pages/ResumeStudio"));
const ATSOptimizer = lazy(() => import("../pages/ATSOptimizer"));
const CoverLetter = lazy(() => import("../pages/CoverLetter"));
const CareerProfile = lazy(() => import("../pages/CareerProfile"));
const ApplicationTracker = lazy(() => import("../pages/ApplicationTracker"));
const ResumeATS = lazy(() => import("../pages/ResumeATS"));

const AptitudeTest = lazy(() => import("../pages/AptitudeTest"));
const MockOA = lazy(() => import("../pages/MockOA"));
const CodingChallenge = lazy(() => import("../pages/CodingChallenge"));
const DailyDrill = lazy(() => import("../pages/DailyDrill"));
const DailyChallenge = lazy(() => import("../pages/DailyChallenge"));
const Predictor = lazy(() => import("../pages/Predictor"));
const SystemDesign = lazy(() => import("../pages/SystemDesign"));

const QuestionBank = lazy(() => import("../pages/QuestionBank"));
const PracticeMode = lazy(() => import("../pages/PracticeMode"));
const Topics = lazy(() => import("../pages/Topics"));
const TopicProblems = lazy(() => import("../pages/TopicProblems"));
const SolveProblem = lazy(() => import("../pages/SolveProblem"));
const ProblemOfTheDay = lazy(() => import("../pages/ProblemOfTheDay"));
const ChallengePacks = lazy(() => import("../pages/ChallengePacks"));
const DSAVisualizer = lazy(() => import("../pages/DSAVisualizer"));
const CompareVisualizer = lazy(() => import("../pages/CompareVisualizer"));
const Compiler = lazy(() => import("../pages/Compiler"));
const CodePlayground = lazy(() => import("../pages/CodePlayground"));

const TowerDashboard = lazy(() => import("../pages/TowerDashboard"));
const LearningHub = lazy(() => import("../pages/LearningHub"));
const LanguageJourney = lazy(() => import("../pages/LanguageJourney"));
const LessonView = lazy(() => import("../pages/LessonView"));
const LessonPlayer = lazy(() => import("../pages/LessonPlayer"));
const Lessons = lazy(() => import("../pages/Lessons"));
const StudyLibrary = lazy(() => import("../pages/StudyLibrary"));
const AdaptivePath = lazy(() => import("../pages/AdaptivePath"));
const LearningModules = lazy(() => import("../pages/LearningModules"));
const CurriculumHub = lazy(() => import("../pages/CurriculumHub"));
const LearnTrack = lazy(() => import("../pages/LearnTrack"));
const LearnLesson = lazy(() => import("../pages/LearnLesson"));

const OnboardingQuest = lazy(() => import("../pages/OnboardingQuest"));
const Onboarding = lazy(() => import("../components/Onboarding"));

const AdminDashboard = lazy(() => import("../pages/AdminDashboard"));
const AdminContent = lazy(() => import("../pages/AdminContent"));
const Analytics = lazy(() => import("../pages/Analytics"));
const Enterprise = lazy(() => import("../pages/Enterprise"));

const Community = lazy(() => import("../pages/Community"));
const AlumniExperiences = lazy(() => import("../pages/AlumniExperiences"));
const PlacementDrives = lazy(() => import("../pages/PlacementDrives"));
const PlacementCalendar = lazy(() => import("../pages/PlacementCalendar"));
const IndianPlacement = lazy(() => import("../pages/IndianPlacement"));

const AIMentor = lazy(() => import("../pages/AIMentor"));
const StudyTimer = lazy(() => import("../pages/StudyTimer"));
const StudyGoals = lazy(() => import("../pages/StudyGoals"));

const NotFound = lazy(() => import("../pages/NotFound"));

const Settings = lazy(() => import("../pages/Settings"));

/**
 * Route type definitions
 */
export type AuthLevel = "public" | "protected" | "admin";

export type ErrorBoundaryType =
  | "Interview"
  | "Resume"
  | "Career"
  | "Assessment"
  | "Question Bank"
  | "Compiler"
  | "Gamification"
  | "Learning"
  | "Study Tools"
  | "Placement"
  | "Community"
  | "default";

export interface RouteDefinition {
  /** Stable route ID (never changes) */
  id: string;
  /** URL path (may contain :params) */
  path: string;
  /** One of: dashboard, journey, practice, mock-oa, ai-interview, company-tracks, profile */
  hub: string;
  auth: AuthLevel;
  errorBoundary?: ErrorBoundaryType;
  component: React.ComponentType<any>;
  /** Backend APIs this route depends on (for data-fetching layer) */
  apis: string[];
  /** Loading / empty / unavailable states */
  loading: string;
  empty?: string;
  unavailable?: string;
  /** Canonical navigation location (where this route lives in the hub nav) */
  navLocation: string;
}

/**
 * Route catalog — single source of truth
 */
export const ROUTE_CATALOG: RouteDefinition[] = [
  // ═══ Public (no auth) ═══
  {
    id: "landing",
    path: "/",
    hub: "dashboard",
    auth: "public",
    component: Landing,
    apis: [],
    loading: "Landing page skeleton",
    navLocation: "root",
  },
  {
    id: "login",
    path: "/login",
    hub: "dashboard",
    auth: "public",
    component: Login,
    apis: ["/api/v1/auth/login"],
    loading: "Signing in…",
    navLocation: "auth",
  },
  {
    id: "register",
    path: "/register",
    hub: "dashboard",
    auth: "public",
    component: Register,
    apis: ["/api/v1/auth/register"],
    loading: "Creating account…",
    navLocation: "auth",
  },
  {
    id: "forgot-password",
    path: "/forgot-password",
    hub: "dashboard",
    auth: "public",
    component: ForgotPassword,
    apis: ["/api/v1/auth/forgot-password"],
    loading: "Sending reset link…",
    navLocation: "auth",
  },
  {
    id: "reset-password",
    path: "/reset-password",
    hub: "dashboard",
    auth: "public",
    component: ResetPassword,
    apis: ["/api/v1/auth/reset-password"],
    loading: "Resetting password…",
    navLocation: "auth",
  },
  {
    id: "pricing",
    path: "/pricing",
    hub: "dashboard",
    auth: "public",
    component: Pricing,
    apis: [],
    loading: "Loading plans…",
    navLocation: "root",
  },
  {
    id: "free-trial",
    path: "/free-trial",
    hub: "dashboard",
    auth: "public",
    component: FreeTrial,
    apis: ["/api/v1/free-trial"],
    loading: "Starting trial…",
    navLocation: "root",
  },
  {
    id: "terms",
    path: "/terms",
    hub: "dashboard",
    auth: "public",
    component: Terms,
    apis: [],
    loading: null,
    navLocation: "root",
  },
  {
    id: "privacy",
    path: "/privacy",
    hub: "dashboard",
    auth: "public",
    component: Privacy,
    apis: [],
    loading: null,
    navLocation: "root",
  },
  {
    id: "blogs",
    path: "/blogs",
    hub: "dashboard",
    auth: "public",
    component: Blogs,
    apis: [],
    loading: "Loading posts…",
    navLocation: "root",
  },
  {
    id: "article-page",
    path: "/blog/:slug",
    hub: "dashboard",
    auth: "public",
    component: ArticlePage,
    apis: [],
    loading: "Loading article…",
    navLocation: "root",
  },
  {
    id: "percentages-academy",
    path: "/percentages-academy",
    hub: "practice",
    auth: "public",
    component: PercentagesAcademy,
    apis: ["/api/v1/questions/browse"],
    loading: "Loading lesson…",
    navLocation: "practice",
  },
  {
    id: "coding-academy",
    path: "/coding-academy",
    hub: "practice",
    auth: "public",
    component: CodingAcademy,
    apis: ["/api/v1/questions/browse"],
    loading: "Loading lesson…",
    navLocation: "practice",
  },
  {
    id: "target",
    path: "/target",
    hub: "company-tracks",
    auth: "public",
    component: TargetPage,
    apis: ["/api/v1/target"],
    loading: "Selecting target…",
    navLocation: "company-tracks",
  },
  {
    id: "loops",
    path: "/loops",
    hub: "practice",
    auth: "public",
    component: LoopsVertical,
    apis: ["/api/v1/questions/browse"],
    loading: "Loading loops…",
    navLocation: "practice",
  },
  {
    id: "gamification-dashboard",
    path: "/gamification",
    hub: "dashboard",
    auth: "public",
    component: GamificationDashboard,
    apis: ["/api/v1/gamification/profile"],
    loading: "Loading stats…",
    navLocation: "dashboard",
  },
  {
    id: "content-bundles",
    path: "/content",
    hub: "practice",
    auth: "public",
    component: ContentBundles,
    apis: ["/api/v1/content"],
    loading: "Loading bundles…",
    navLocation: "practice",
  },

  // ═══ Protected (auth required) ═══
  {
    id: "onboarding",
    path: "/onboarding",
    hub: "dashboard",
    auth: "protected",
    component: OnboardingQuest,
    apis: [
      "/api/v1/auth/onboarding-status",
      "/api/v1/auth/onboarding-complete",
    ],
    loading: "Loading onboarding…",
    navLocation: "dashboard",
  },
  {
    id: "dashboard",
    path: "/dashboard",
    hub: "dashboard",
    auth: "protected",
    component: StudentDashboard,
    errorBoundary: "default",
    apis: [
      "/api/v1/dashboard",
      "/api/v1/gamification/profile",
      "/api/v1/study/today",
      "/api/v1/readiness",
    ],
    loading: "Loading dashboard…",
    empty: "No activity yet. Start your first lesson.",
    navLocation: "dashboard",
  },
  {
    id: "student-dashboard",
    path: "/student-dashboard",
    hub: "dashboard",
    auth: "protected",
    component: Navigate,
    apis: [],
    loading: null,
    navLocation: "dashboard",
  },
  {
    id: "my-dashboard",
    path: "/my-dashboard",
    hub: "dashboard",
    auth: "protected",
    component: Navigate,
    apis: [],
    loading: null,
    navLocation: "dashboard",
  },
  {
    id: "profile",
    path: "/profile",
    hub: "profile",
    auth: "protected",
    component: StudentDashboard,
    apis: [
      "/api/v1/profile/stats",
      "/api/v1/gamification/profile",
      "/api/v1/readiness",
      "/api/v1/evidence",
    ],
    loading: "Loading profile…",
    navLocation: "profile",
  },
  {
    id: "home",
    path: "/home",
    hub: "dashboard",
    auth: "protected",
    component: Home,
    apis: ["/api/v1/dashboard"],
    loading: "Loading home…",
    navLocation: "dashboard",
  },
  {
    id: "hub",
    path: "/hub",
    hub: "dashboard",
    auth: "protected",
    component: Home,
    apis: [],
    loading: null,
    navLocation: "dashboard",
  },
  {
    id: "prepare",
    path: "/prepare",
    hub: "practice",
    auth: "protected",
    component: Prepare,
    apis: ["/api/v1/target"],
    loading: "Loading prep…",
    navLocation: "practice",
  },
  {
    id: "practice",
    path: "/practice",
    hub: "practice",
    auth: "protected",
    component: Practice,
    apis: ["/api/v1/practice", "/api/v1/questions/browse"],
    loading: "Loading practice…",
    navLocation: "practice",
  },
  {
    id: "compete",
    path: "/compete",
    hub: "mock-oa",
    auth: "protected",
    component: Compete,
    apis: ["/api/v1/oa/companies"],
    loading: "Loading mocks…",
    navLocation: "mock-oa",
  },
  {
    id: "career",
    path: "/career",
    hub: "company-tracks",
    auth: "protected",
    component: Career,
    apis: ["/api/v1/company/companies"],
    loading: "Loading companies…",
    navLocation: "company-tracks",
  },
  {
    id: "lessons",
    path: "/lessons",
    hub: "journey",
    auth: "protected",
    component: Lessons,
    apis: ["/api/v1/lessons"],
    loading: "Loading lessons…",
    navLocation: "journey",
  },
  {
    id: "lesson-player",
    path: "/lessons/:lessonId",
    hub: "journey",
    auth: "protected",
    component: LessonPlayer,
    apis: ["/api/v1/lessons/:lessonId"],
    loading: "Loading lesson…",
    navLocation: "journey",
  },
  {
    id: "skills",
    path: "/skills",
    hub: "company-tracks",
    auth: "protected",
    component: SkillMap,
    apis: ["/api/v1/skills", "/api/v1/gamification/skills"],
    loading: "Loading skill map…",
    navLocation: "company-tracks",
  },
  {
    id: "concepts",
    path: "/concepts",
    hub: "journey",
    auth: "protected",
    component: Concepts,
    apis: ["/api/v1/concepts"],
    loading: "Loading concepts…",
    navLocation: "journey",
  },
  {
    id: "settings",
    path: "/settings",
    hub: "profile",
    auth: "protected",
    component: Settings,
    apis: ["/api/v1/auth/me"],
    loading: "Loading settings…",
    navLocation: "profile",
  },
  {
    id: "history",
    path: "/history",
    hub: "profile",
    auth: "protected",
    component: History,
    apis: ["/api/v1/questions/recent"],
    loading: "Loading history…",
    navLocation: "profile",
  },
  {
    id: "leaderboard",
    path: "/leaderboard",
    hub: "dashboard",
    auth: "protected",
    component: Leaderboard,
    apis: ["/api/v1/gamification/leaderboard"],
    loading: "Loading leaderboard…",
    navLocation: "dashboard",
  },
  {
    id: "contests",
    path: "/contests",
    hub: "mock-oa",
    auth: "protected",
    component: lazy(() => import("../pages/MonthlyContests")),
    apis: ["/api/v1/contests"],
    loading: "Loading contests…",
    navLocation: "mock-oa",
  },
  {
    id: "question-bank",
    path: "/question-bank",
    hub: "practice",
    auth: "protected",
    component: QuestionBank,
    errorBoundary: "Question Bank",
    apis: ["/api/v1/questions/browse", "/api/v1/questions/filters"],
    loading: "Loading questions…",
    navLocation: "practice",
  },
  {
    id: "question-bank-progress",
    path: "/question-bank/progress",
    hub: "practice",
    auth: "protected",
    component: MyProgress,
    errorBoundary: "Question Bank",
    apis: ["/api/v1/questions/stats"],
    loading: "Loading progress…",
    navLocation: "practice",
  },
  {
    id: "question-bank-detail",
    path: "/question-bank/:questionId",
    hub: "practice",
    auth: "protected",
    component: PracticeMode,
    errorBoundary: "Question Bank",
    apis: [
      "/api/v1/questions/:questionId",
      "/api/v1/questions/:questionId/solution",
    ],
    loading: "Loading problem…",
    navLocation: "practice",
  },
  {
    id: "problem-of-the-day",
    path: "/problem-of-the-day",
    hub: "practice",
    auth: "protected",
    component: ProblemOfTheDay,
    errorBoundary: "Question Bank",
    apis: ["/api/v1/daily-challenge"],
    loading: "Loading problem…",
    navLocation: "practice",
  },
  {
    id: "problems",
    path: "/problems",
    hub: "practice",
    auth: "protected",
    component: Topics,
    errorBoundary: "Question Bank",
    apis: ["/api/v1/questions/topics"],
    loading: "Loading topics…",
    navLocation: "practice",
  },
  {
    id: "topic-problems",
    path: "/problems/:topic",
    hub: "practice",
    auth: "protected",
    component: TopicProblems,
    errorBoundary: "Question Bank",
    apis: ["/api/v1/questions/browse?topic=:topic"],
    loading: "Loading problems…",
    navLocation: "practice",
  },
  {
    id: "solve",
    path: "/solve/:id",
    hub: "practice",
    auth: "protected",
    component: SolveProblem,
    errorBoundary: "Question Bank",
    apis: [
      "/api/v1/questions/:id/submit",
      "/api/v1/compiler/execute",
    ],
    loading: "Loading editor…",
    navLocation: "practice",
  },
  {
    id: "compiler",
    path: "/compiler",
    hub: "practice",
    auth: "protected",
    component: Compiler,
    errorBoundary: "Compiler",
    apis: [
      "/api/v1/compiler/languages",
      "/api/v1/compiler/execute",
    ],
    loading: "Loading compiler…",
    navLocation: "practice",
  },
  {
    id: "playground",
    path: "/playground",
    hub: "practice",
    auth: "protected",
    component: CodePlayground,
    errorBoundary: "Compiler",
    apis: ["/api/v1/compiler/execute"],
    loading: "Loading playground…",
    navLocation: "practice",
  },
  {
    id: "challenge-packs",
    path: "/challenge-packs",
    hub: "practice",
    auth: "protected",
    component: ChallengePacks,
    errorBoundary: "Question Bank",
    apis: ["/api/v1/questions/filters"],
    loading: "Loading packs…",
    navLocation: "practice",
  },
  {
    id: "dsa-visualizer",
    path: "/dsa-visualizer",
    hub: "practice",
    auth: "protected",
    component: DSAVisualizer,
    errorBoundary: "Question Bank",
    apis: [],
    loading: "Loading visualizer…",
    navLocation: "practice",
  },
  {
    id: "compare-visualizer",
    path: "/visualize/compare",
    hub: "practice",
    auth: "protected",
    component: CompareVisualizer,
    errorBoundary: "Question Bank",
    apis: [],
    loading: null,
    navLocation: "practice",
  },
  {
    id: "tower",
    path: "/tower",
    hub: "dashboard",
    auth: "protected",
    component: TowerDashboard,
    errorBoundary: "Gamification",
    apis: [
      "/api/v1/gamification/tower",
      "/api/v1/gamification/badges",
    ],
    loading: "Loading tower…",
    navLocation: "dashboard",
  },
  {
    id: "learn",
    path: "/learn",
    hub: "journey",
    auth: "protected",
    component: Navigate,
    apis: [],
    loading: null,
    navLocation: "journey",
  },
  {
    id: "learn-language",
    path: "/learn/:languageId",
    hub: "journey",
    auth: "protected",
    component: LearningHub,
    errorBoundary: "Learning",
    apis: ["/api/language-paths", "/api/learning/modules"],
    loading: "Loading language path…",
    navLocation: "journey",
  },
  {
    id: "learn-lesson",
    path: "/learn/:languageId/:levelId/:lessonId",
    hub: "journey",
    auth: "protected",
    component: LessonView,
    errorBoundary: "Learning",
    apis: ["/api/v1/lesson/:lessonId"],
    loading: "Loading lesson…",
    navLocation: "journey",
  },
  {
    id: "study-timer",
    path: "/study-timer",
    hub: "journey",
    auth: "protected",
    component: StudyTimer,
    errorBoundary: "Study Tools",
    apis: [],
    loading: null,
    navLocation: "journey",
  },
  {
    id: "study-goals",
    path: "/study-goals",
    hub: "journey",
    auth: "protected",
    component: StudyGoals,
    errorBoundary: "Study Tools",
    apis: ["/api/v1/study/today"],
    loading: "Loading goals…",
    navLocation: "journey",
  },
  {
    id: "ai-mentor",
    path: "/ai-mentor",
    hub: "ai-interview",
    auth: "protected",
    component: lazy(() => import("../pages/AIMentor")),
    errorBoundary: "Study Tools",
    apis: ["/api/v1/ai/tutor/explain"],
    loading: "Loading mentor…",
    navLocation: "ai-interview",
  },
  {
    id: "interview",
    path: "/interview",
    hub: "ai-interview",
    auth: "protected",
    component: Interview,
    errorBoundary: "Interview",
    apis: ["/api/v1/interview/start"],
    loading: "Starting interview…",
    navLocation: "ai-interview",
  },
  {
    id: "interview-session",
    path: "/interview/:interviewId",
    hub: "ai-interview",
    auth: "protected",
    component: InterviewSession,
    errorBoundary: "Interview",
    apis: [
      "/api/v1/interview/answer",
      "/api/v1/interview/:id/result",
    ],
    loading: "Loading session…",
    navLocation: "ai-interview",
  },
  {
    id: "interview-booking",
    path: "/interview-booking",
    hub: "ai-interview",
    auth: "protected",
    component: InterviewBooking,
    errorBoundary: "Interview",
    apis: ["/api/v1/interview/bookings"],
    loading: "Loading bookings…",
    navLocation: "ai-interview",
  },
  {
    id: "interview-replay",
    path: "/interview-replay/:interviewId",
    hub: "ai-interview",
    auth: "protected",
    component: InterviewReplay,
    errorBoundary: "Interview",
    apis: ["/api/v1/interview/:id/result"],
    loading: "Loading replay…",
    navLocation: "ai-interview",
  },
  {
    id: "mock-oa",
    path: "/mock-oa",
    hub: "mock-oa",
    auth: "protected",
    component: MockOA,
    errorBoundary: "Assessment",
    apis: ["/api/v1/oa/companies", "/api/v1/oa/start"],
    loading: "Loading mock OA…",
    navLocation: "mock-oa",
  },
  {
    id: "aptitude",
    path: "/aptitude",
    hub: "mock-oa",
    auth: "protected",
    component: AptitudeTest,
    errorBoundary: "Assessment",
    apis: [
      "/api/v1/aptitude/categories",
      "/api/v1/aptitude/start",
    ],
    loading: "Loading aptitude test…",
    navLocation: "mock-oa",
  },
  {
    id: "coding-challenge",
    path: "/coding",
    hub: "mock-oa",
    auth: "protected",
    component: CodingChallenge,
    errorBoundary: "Assessment",
    apis: ["/api/v1/coding/start", "/api/v1/coding/submit"],
    loading: "Loading challenge…",
    navLocation: "mock-oa",
  },
  {
    id: "daily-challenge",
    path: "/daily-challenge",
    hub: "mock-oa",
    auth: "protected",
    component: DailyChallenge,
    errorBoundary: "Assessment",
    apis: ["/api/v1/daily-challenge"],
    loading: "Loading daily challenge…",
    navLocation: "mock-oa",
  },
  {
    id: "system-design",
    path: "/system-design",
    hub: "mock-oa",
    auth: "protected",
    component: SystemDesign,
    errorBoundary: "Assessment",
    apis: ["/api/v1/system-design"],
    loading: "Loading system design…",
    navLocation: "mock-oa",
  },
  {
    id: "predictor",
    path: "/predictor",
    hub: "mock-oa",
    auth: "protected",
    component: Predictor,
    errorBoundary: "Assessment",
    apis: ["/api/v1/predictor"],
    loading: "Loading predictor…",
    navLocation: "mock-oa",
  },
  {
    id: "resume-builder",
    path: "/resume",
    hub: "company-tracks",
    auth: "protected",
    component: ResumeBuilder,
    errorBoundary: "Resume",
    apis: ["/api/v1/resume/upload", "/api/v1/resume/generate"],
    loading: "Loading resume builder…",
    navLocation: "company-tracks",
  },
  {
    id: "resume-studio",
    path: "/resume-studio",
    hub: "company-tracks",
    auth: "protected",
    component: ResumeStudio,
    errorBoundary: "Resume",
    apis: ["/api/v1/resume/generate"],
    loading: "Loading studio…",
    navLocation: "company-tracks",
  },
  {
    id: "ats-optimizer",
    path: "/ats",
    hub: "company-tracks",
    auth: "protected",
    component: ATSOptimizer,
    errorBoundary: "Resume",
    apis: [
      "/api/v1/resume/optimize",
      "/api/v1/resume/semantic-score",
    ],
    loading: "Loading ATS optimizer…",
    navLocation: "company-tracks",
  },
  {
    id: "cover-letter",
    path: "/cover-letter",
    hub: "company-tracks",
    auth: "protected",
    component: CoverLetter,
    errorBoundary: "Career",
    apis: ["/api/v1/cover-letter/generate"],
    loading: "Loading cover letter…",
    navLocation: "company-tracks",
  },
  {
    id: "career-profile",
    path: "/career-profile",
    hub: "profile",
    auth: "protected",
    component: CareerProfile,
    errorBoundary: "Career",
    apis: ["/api/v1/profile/integrations"],
    loading: "Loading career profile…",
    navLocation: "profile",
  },
  {
    id: "application-tracker",
    path: "/applications",
    hub: "profile",
    auth: "protected",
    component: ApplicationTracker,
    errorBoundary: "Career",
    apis: ["/api/v1/applications"],
    loading: "Loading applications…",
    navLocation: "profile",
  },
  {
    id: "resume-ats",
    path: "/resume-ats",
    hub: "company-tracks",
    auth: "protected",
    component: ResumeATS,
    errorBoundary: "Resume",
    apis: ["/api/v1/resume/semantic-score"],
    loading: "Loading ATS score…",
    navLocation: "company-tracks",
  },
  {
    id: "admin",
    path: "/admin",
    hub: "dashboard",
    auth: "admin",
    component: AdminDashboard,
    apis: ["/api/v1/analytics/admin"],
    loading: "Loading admin dashboard…",
    navLocation: "admin",
  },
  {
    id: "admin-content",
    path: "/admin-content",
    hub: "dashboard",
    auth: "admin",
    component: AdminContent,
    apis: ["/api/v1/admin/content"],
    loading: "Loading content…",
    navLocation: "admin",
  },
  {
    id: "analytics",
    path: "/analytics",
    hub: "dashboard",
    auth: "protected",
    component: Analytics,
    apis: ["/api/v1/analytics/admin"],
    loading: "Loading analytics…",
    navLocation: "dashboard",
  },
  {
    id: "enterprise",
    path: "/enterprise",
    hub: "dashboard",
    auth: "admin",
    component: Enterprise,
    apis: ["/api/v1/enterprise"],
    loading: "Loading enterprise…",
    navLocation: "admin",
  },
  {
    id: "community",
    path: "/community",
    hub: "profile",
    auth: "protected",
    component: Community,
    apis: ["/api/community/posts"],
    loading: "Loading community…",
    navLocation: "profile",
  },
  {
    id: "alumni-experiences",
    path: "/alumni-experiences",
    hub: "profile",
    auth: "protected",
    component: AlumniExperiences,
    apis: [],
    loading: "Loading alumni…",
    navLocation: "profile",
  },
  {
    id: "placement-drives",
    path: "/placement-drives",
    hub: "company-tracks",
    auth: "protected",
    component: PlacementDrives,
    apis: [],
    loading: "Loading drives…",
    navLocation: "company-tracks",
  },
  {
    id: "placement-calendar",
    path: "/placement-calendar",
    hub: "company-tracks",
    auth: "protected",
    component: PlacementCalendar,
    apis: [],
    loading: "Loading calendar…",
    navLocation: "company-tracks",
  },
  {
    id: "indian-placement",
    path: "/indian-placement",
    hub: "company-tracks",
    auth: "protected",
    component: IndianPlacement,
    apis: [],
    loading: "Loading prep…",
    navLocation: "company-tracks",
  },
  {
    id: "not-found",
    path: "*",
    hub: "dashboard",
    auth: "public",
    component: NotFound,
    apis: [],
    loading: null,
    navLocation: "root",
  },
];

/**
 * Lookup helpers
 */

export function getRouteById(id: string): RouteDefinition | undefined {
  return ROUTE_CATALOG.find((r) => r.id === id);
}

export function getRouteByPath(path: string): RouteDefinition | undefined {
  // Exact match first
  const exact = ROUTE_CATALOG.find((r) => r.path === path);
  if (exact) return exact;
  // Parametric match (/:param → matches any single segment)
  for (const route of ROUTE_CATALOG) {
    const routeSegments = route.path.split("/");
    const pathSegments = path.split("/");
    if (routeSegments.length !== pathSegments.length) continue;
    const matches = routeSegments.every((seg, i) =>
      seg.startsWith(":") || seg === pathSegments[i]
    );
    if (matches) return route;
  }
  return undefined;
}

export function getRoutesByHub(hub: string): RouteDefinition[] {
  return ROUTE_CATALOG.filter((r) => r.hub === hub);
}

export function isAuthRequired(path: string): boolean {
  const route = getRouteByPath(path);
  return route ? route.auth !== "public" : true;
}

export function isAdminRequired(path: string): boolean {
  const route = getRouteByPath(path);
  return route ? route.auth === "admin" : false;
}

export function requiresErrorBoundary(
  path: string
): ErrorBoundaryType | undefined {
  const route = getRouteByPath(path);
  return route?.errorBoundary;
}
