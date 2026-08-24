import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
  Navigate,
} from "react-router-dom";
import {
  useEffect,
  Suspense,
  useState,
  useCallback,
  useRef,
  lazy,
} from "react";
import useAuthStore from "./store/authStore";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ErrorBoundary from "./components/ErrorBoundary";
import RouteErrorBoundary from "./components/RouteErrorBoundary";
import FeatureErrorBoundary from "./components/FeatureErrorBoundary";
import ProtectedRoute from "./components/ProtectedRoute";
import OnboardingGuard from "./components/OnboardingGuard";
import CustomCursor from "./components/CustomCursor";
import { DashboardSkeleton } from "./components/ui/Skeleton";
import { ToastProvider } from "./components/Toast";
import { ThemeProvider } from "./components/ThemeProvider";
import { JuiceProvider, useJuice } from "./juice/JuiceProvider";
import Landing from "./pages/Landing";

const AuthLayout = lazy(() => import("./components/AuthLayout"));
const Onboarding = lazy(() => import("./components/Onboarding"));
const XPPopup = lazy(() => import("./components/XPPopup"));
const CelebrationOverlay = lazy(
  () => import("./components/CelebrationOverlay"),
);
const BottomNav = lazy(() => import("./components/BottomNav"));

import {
  Login,
  Register,
  OnboardingQuest,
  Dashboard,
  Interview,
  InterviewSession,
  InterviewBooking,
  InterviewReplay,
  ResumeBuilder,
  ResumeStudio,
  ATSOptimizer,
  Pricing,
  RoleSelector,
  PlacementCalendar,
  NotFound,
  BattleArena,
  CodePlayground,
  CompareVisualizer,
  Journey,
  RankProfile,
  Scrims,
  AptitudeTest,
  CoverLetter,
  SalaryNegotiation,
  SystemDesign,
  CompanyPrep,
  CodingChallenge,
  SalaryBenchmark,
  Settings,
  History,
  Leaderboard,
  DailyDrill,
  StudyGroups,
  Predictor,
  QuestionBank,
  PracticeMode,
  MyProgress,
  CompanyMocks,
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
  DSAFingerprint,
  TowerDashboard,
  BattlePass,
  StudyTimer,
  StudyGoals,
  ThemesPage,
  CampusConnect,
  CampusWars,
  ProblemOfTheDay,
  DailyChallenge,
  DSAVisualizer,
  ResumeATS,
  MockOA,
  LearningHub,
  LanguageJourney,
  LessonView,
  StudyLibrary,
  AdminDashboard,
  Topics,
  TopicProblems,
  CardCollection,
  PersonalDashboard,
  StudentDashboard,
  AdaptivePath,
   LearningModules,
   LearningModule,
   ProjectGenerator,
  LanguageLearning,
  CurriculumHub,
  LearnTrack,
  LearnLesson,
  FreeTrial,
  Showcase,
  ShowcaseDetail,
  PwaSetup,
  AdminContent,
  MyAssignments,
  GameEvents,
  Timeline,
  WorldMap,
  AIMentor,
  HealthDashboard,
  AchievementChains,
  CampusPulse,
  CareerRpg,
  ChallengePacks,
  Home,
  Prepare,
  InterviewTerminal,
  MassRecruiterExam,
  Practice,
  Compete,
  Career,
  Chat,
  GDRoom,
  CGPASimulator,
  DriveTracker,
  PeerReview,
  StudySquads,
  PrepReportCard,
  CollectionEvents,
  CollegeNetwork,
  CommandCenter,
  Community,
  Dungeons,
  Economy,
  GuildCastle,
  Guilds,
  LearningJourneys,
  LuckyWheel,
  Merchant,
  Newspaper,
  Referral,
  ReferralGamification,
  RetentionAdmin,
  SeasonalEvents,
  ShareCard,
  SkillTrees,
  SteamProfile,
  TeamCompetitions,
  Tournaments,
  TrendingChallenges,
  BehavioralPractice,
  CompanyDirectory,
  Concepts,
  Quests,
  ReadinessScore,
  MysteryBoxPage,
  SkillMasteryPage,
  EnergyPage,
  FriendsPage,
  GoalsPage,
  DiscussionsPage,
  BossAssessment,
  MissionView,
  Mission,
  JourneyMapPage,
  BountyPage,
  JobReadiness,
  CapabilityWorlds,
  CapabilityMission,
} from "./pages/lazy";

function AnimatedRoutes() {
  const location = useLocation();
  const lastTrackedPath = useRef(null);

  // Track page views for analytics (throttled: once per path, StrictMode-safe)
  useEffect(() => {
    if (lastTrackedPath.current === location.pathname) return;
    lastTrackedPath.current = location.pathname;

    if (window.gtag) {
      window.gtag("event", "page_view", { page_path: location.pathname });
    }
    fetch("/api/v1/analytics/track", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ event: "page_view", path: location.pathname }),
    }).catch(() => {});
  }, [location.pathname]);

  return (
    <Routes location={location} key={location.pathname}>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/role-selector" element={<RoleSelector />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/free-trial" element={<FreeTrial />} />
      <Route
        path="/onboarding"
        element={
          <ProtectedRoute>
            <OnboardingQuest />
          </ProtectedRoute>
        }
      />

      <Route
        element={
          <ProtectedRoute>
            <OnboardingGuard>
              <AuthLayout />
            </OnboardingGuard>
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<StudentDashboard />} />
        <Route
          path="/student-dashboard"
          element={<Navigate to="/dashboard" replace />}
        />
        <Route
          path="/my-dashboard"
          element={<Navigate to="/dashboard" replace />}
        />
        <Route path="/home" element={<Home />} />
        <Route path="/hub" element={<Home />} />
        <Route path="/prepare" element={<Prepare />} />
        <Route path="/practice" element={<Practice />} />
        <Route path="/compete" element={<Compete />} />
        <Route path="/career" element={<Career />} />
        <Route
          path="/analytics"
          element={<Navigate to="/dashboard" replace />}
        />
        <Route path="/health" element={<Navigate to="/dashboard" replace />} />
        <Route path="/learning" element={<Navigate to="/learn" replace />} />
        <Route
          path="/campus"
          element={<Navigate to="/campus-wars" replace />}
        />
        <Route path="/journey" element={<CareerRpg />} />
        <Route path="/boss/:bossId" element={<BossAssessment />} />
        <Route path="/mission/:topic" element={<MissionView />} />
        <Route path="/mission/:worldId/:missionId" element={<Mission />} />
        <Route path="/journey-map/:worldId" element={<JourneyMapPage />} />
        <Route path="/world/:worldId" element={<JourneyMapPage />} />
        <Route path="/bounty" element={<BountyPage />} />
        <Route path="/job-readiness" element={<JobReadiness />} />
        <Route path="/capability-worlds" element={<CapabilityWorlds />} />
        <Route path="/capability-mission/:worldId/:competencyId" element={<CapabilityMission />} />
        <Route path="/behavioral-practice" element={<BehavioralPractice />} />
        <Route path="/company-directory" element={<CompanyDirectory />} />
        <Route path="/concepts" element={<Concepts />} />
        <Route path="/quests" element={<Quests />} />
        <Route path="/readiness" element={<ReadinessScore />} />
        <Route path="/mystery-box" element={<MysteryBoxPage />} />
        <Route path="/skill-mastery" element={<SkillMasteryPage />} />
        <Route path="/energy" element={<EnergyPage />} />
        <Route path="/friends" element={<FriendsPage />} />
        <Route path="/goals" element={<GoalsPage />} />
        <Route path="/discussions" element={<DiscussionsPage />} />

        {/* Interview Routes */}
        <Route
          path="/interview"
          element={
            <FeatureErrorBoundary featureName="Interview">
              <Interview />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/interview/:interviewId"
          element={
            <FeatureErrorBoundary featureName="Interview">
              <InterviewSession />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/interview-booking"
          element={
            <FeatureErrorBoundary featureName="Interview">
              <InterviewBooking />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/interview-terminal"
          element={
            <FeatureErrorBoundary featureName="Interview">
              <InterviewTerminal />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/mass-recruiter"
          element={
            <FeatureErrorBoundary featureName="MassRecruiterExam">
              <MassRecruiterExam />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/interview-replay/:interviewId"
          element={
            <FeatureErrorBoundary featureName="Interview">
              <InterviewReplay />
            </FeatureErrorBoundary>
          }
        />

        <Route path="/referral" element={<Referral />} />

        {/* Career Routes */}
        <Route
          path="/resume"
          element={
            <FeatureErrorBoundary featureName="Resume">
              <ResumeBuilder />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/resume-studio"
          element={
            <FeatureErrorBoundary featureName="Resume">
              <ResumeStudio />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/ats"
          element={
            <FeatureErrorBoundary featureName="Resume">
              <ATSOptimizer />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/cover-letter"
          element={
            <FeatureErrorBoundary featureName="Career">
              <CoverLetter />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/salary-negotiation"
          element={
            <FeatureErrorBoundary featureName="Career">
              <SalaryNegotiation />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/salary-benchmark"
          element={
            <FeatureErrorBoundary featureName="Career">
              <SalaryBenchmark />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/career-profile"
          element={
            <FeatureErrorBoundary featureName="Career">
              <CareerProfile />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/applications"
          element={
            <FeatureErrorBoundary featureName="Career">
              <ApplicationTracker />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/resume-ats"
          element={
            <FeatureErrorBoundary featureName="Resume">
              <ResumeATS />
            </FeatureErrorBoundary>
          }
        />

        {/* Assessment Routes */}
        <Route
          path="/aptitude"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <AptitudeTest />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/mock-oa"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <MockOA />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/coding"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <CodingChallenge />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/daily-drill"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <DailyDrill />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/daily-challenge"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <DailyChallenge />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/daily-challenge/leaderboard"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <DailyChallenge />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/company-mocks"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <CompanyMocks />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/company-mocks/:testId"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <CompanyMocks />
            </FeatureErrorBoundary>
          }
        />

        {/* System Design & Company Prep */}
        <Route
          path="/system-design"
          element={
            <FeatureErrorBoundary featureName="System Design">
              <SystemDesign />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/company-prep"
          element={
            <FeatureErrorBoundary featureName="Company Prep">
              <CompanyPrep />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/predictor"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <Predictor />
            </FeatureErrorBoundary>
          }
        />

        <Route path="/settings" element={<Settings />} />
        <Route path="/history" element={<History />} />
        <Route path="/leaderboard" element={<Leaderboard />} />
        <Route path="/contests" element={<MonthlyContests />} />

        {/* Question Bank Routes */}
        <Route
          path="/question-bank"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <QuestionBank />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/question-bank/progress"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <MyProgress />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/question-bank/:questionId"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <PracticeMode />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/problem-of-the-day"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <ProblemOfTheDay />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/problems"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <Topics />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/problems/:topic"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <TopicProblems />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/solve/:id"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <SolveProblem />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/compiler"
          element={
            <FeatureErrorBoundary featureName="Compiler">
              <Compiler />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/playground"
          element={
            <FeatureErrorBoundary featureName="Compiler">
              <CodePlayground />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/fingerprint"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <DSAFingerprint />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/challenge-packs"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <ChallengePacks />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/dsa-visualizer"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <DSAVisualizer />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/visualize/compare"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <CompareVisualizer />
            </FeatureErrorBoundary>
          }
        />

        {/* Gamification Routes */}
        <Route
          path="/tower"
          element={
            <FeatureErrorBoundary featureName="Gamification">
              <TowerDashboard />
            </FeatureErrorBoundary>
          }
        />
        <Route path="/battle-pass" element={<Navigate to="/tower" replace />} />
        <Route path="/cards" element={<Navigate to="/tower" replace />} />
        <Route path="/rank" element={<Navigate to="/tower" replace />} />
        <Route
          path="/achievements"
          element={<Navigate to="/tower" replace />}
        />
        <Route path="/skill-trees" element={<Navigate to="/tower" replace />} />
        <Route
          path="/battles"
          element={
            <FeatureErrorBoundary featureName="Gamification">
              <BattleArena />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/battles/:battleId"
          element={
            <FeatureErrorBoundary featureName="Gamification">
              <BattleArena />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/wheel"
          element={
            <FeatureErrorBoundary featureName="Gamification">
              <LuckyWheel />
            </FeatureErrorBoundary>
          }
        />

        {/* Learning Routes */}
        <Route
          path="/learn"
          element={
            <FeatureErrorBoundary featureName="Learning">
              <LearningHub />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/learn/modules"
          element={<Navigate to="/learn" replace />}
        />
        <Route
          path="/learn/:languageId"
          element={
            <FeatureErrorBoundary featureName="Learning">
              <LanguageLearning />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/learn/:languageId/:levelId/:lessonId"
          element={
            <FeatureErrorBoundary featureName="Learning">
              <LessonView />
            </FeatureErrorBoundary>
          }
        />
         <Route
          path="/modules"
          element={
            <FeatureErrorBoundary featureName="Learning">
              <LearningModules />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/modules/:moduleId"
          element={
            <FeatureErrorBoundary featureName="Learning">
              <LearningModule />
            </FeatureErrorBoundary>
          }
        />
        <Route path="/adaptive" element={<Navigate to="/learn" replace />} />
        <Route path="/languages" element={<Navigate to="/learn" replace />} />
        <Route
          path="/languages/:languageId"
          element={<Navigate to="/learn" replace />}
        />
        <Route path="/curriculum" element={<Navigate to="/learn" replace />} />
        <Route
          path="/curriculum/:trackId"
          element={<Navigate to="/learn" replace />}
        />
        <Route
          path="/curriculum/:trackId/:lessonId"
          element={<Navigate to="/learn" replace />}
        />
        <Route
          path="/scrims"
          element={
            <FeatureErrorBoundary featureName="Learning">
              <Scrims />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/scrims/:scrimId"
          element={
            <FeatureErrorBoundary featureName="Learning">
              <Scrims />
            </FeatureErrorBoundary>
          }
        />
        <Route path="/study" element={<Navigate to="/learn" replace />} />

        {/* Study Tools */}
        <Route
          path="/study-timer"
          element={
            <FeatureErrorBoundary featureName="Study Tools">
              <StudyTimer />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/study-goals"
          element={
            <FeatureErrorBoundary featureName="Study Tools">
              <StudyGoals />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/ai-mentor"
          element={
            <FeatureErrorBoundary featureName="Study Tools">
              <AIMentor />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/project-generator"
          element={
            <FeatureErrorBoundary featureName="Study Tools">
              <ProjectGenerator />
            </FeatureErrorBoundary>
          }
        />

        {/* Indian Placement Prep */}
        <Route
          path="/indian-placement"
          element={
            <FeatureErrorBoundary featureName="Placement">
              <IndianPlacement />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/alumni-experiences"
          element={
            <FeatureErrorBoundary featureName="Placement">
              <AlumniExperiences />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/placement-drives"
          element={
            <FeatureErrorBoundary featureName="Placement">
              <PlacementDrives />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/placement-calendar"
          element={
            <FeatureErrorBoundary featureName="Placement">
              <PlacementCalendar />
            </FeatureErrorBoundary>
          }
        />

        {/* Community Routes */}
        <Route
          path="/community"
          element={
            <FeatureErrorBoundary featureName="Community">
              <Community />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/campus-connect"
          element={<Navigate to="/community" replace />}
        />
        <Route
          path="/campus-wars"
          element={
            <FeatureErrorBoundary featureName="Community">
              <CampusWars />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/campus-pulse"
          element={<Navigate to="/community" replace />}
        />
        <Route path="/college" element={<Navigate to="/community" replace />} />
        <Route path="/chat" element={<Navigate to="/community" replace />} />
        <Route path="/gd" element={<Navigate to="/community" replace />} />
        <Route
          path="/gd/:roomId"
          element={<Navigate to="/community" replace />}
        />
        <Route
          path="/peer-review"
          element={<Navigate to="/community" replace />}
        />
        <Route
          path="/study-groups"
          element={<Navigate to="/community" replace />}
        />
        <Route
          path="/study-squads"
          element={<Navigate to="/community" replace />}
        />

        {/* Showcase */}
        <Route
          path="/showcase"
          element={
            <FeatureErrorBoundary featureName="Showcase">
              <Showcase />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/showcase/:projectId"
          element={
            <FeatureErrorBoundary featureName="Showcase">
              <ShowcaseDetail />
            </FeatureErrorBoundary>
          }
        />

        {/* PWA */}
        <Route
          path="/pwa"
          element={
            <ProtectedRoute>
              <PwaSetup />
            </ProtectedRoute>
          }
        />

        {/* Admin */}
        <Route path="/admin" element={<AdminDashboard />} />
        <Route
          path="/admin-content"
          element={<Navigate to="/admin" replace />}
        />
        <Route
          path="/my-assignments"
          element={<Navigate to="/dashboard" replace />}
        />
        <Route path="/retention" element={<Navigate to="/admin" replace />} />

        {/* Gamification Hub Redirects */}
        <Route path="/economy" element={<Navigate to="/tower" replace />} />
        <Route path="/merchant" element={<Navigate to="/tower" replace />} />
        <Route path="/game-events" element={<Navigate to="/tower" replace />} />
        <Route path="/world" element={<Navigate to="/tower" replace />} />
        <Route path="/guilds" element={<Navigate to="/tower" replace />} />
        <Route path="/dungeons" element={<Navigate to="/tower" replace />} />
        <Route path="/collection" element={<Navigate to="/tower" replace />} />
        <Route path="/timeline" element={<Navigate to="/tower" replace />} />
        <Route path="/newspaper" element={<Navigate to="/tower" replace />} />
        <Route path="/share" element={<Navigate to="/tower" replace />} />
        <Route path="/trending" element={<Navigate to="/tower" replace />} />
        <Route path="/seasonal" element={<Navigate to="/tower" replace />} />
        <Route
          path="/guilds/castle/:guildId"
          element={<Navigate to="/tower" replace />}
        />
        <Route path="/tournaments" element={<Navigate to="/tower" replace />} />
        <Route path="/teams" element={<Navigate to="/tower" replace />} />
        <Route path="/referrals" element={<Navigate to="/tower" replace />} />
        <Route path="/themes" element={<Navigate to="/tower" replace />} />
        <Route path="/daily-drill" element={<Navigate to="/tower" replace />} />
        <Route
          path="/profile/steam"
          element={<Navigate to="/dashboard" replace />}
        />

        {/* Utility */}
        <Route
          path="/cgpa-simulator"
          element={
            <ProtectedRoute>
              <CGPASimulator />
            </ProtectedRoute>
          }
        />
        <Route
          path="/drive-tracker"
          element={
            <ProtectedRoute>
              <DriveTracker />
            </ProtectedRoute>
          }
        />
        <Route
          path="/report-card"
          element={
            <ProtectedRoute>
              <PrepReportCard />
            </ProtectedRoute>
          }
        />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

function PageSuspense({ children }) {
  return <Suspense fallback={<DashboardSkeleton />}>{children}</Suspense>;
}

function AppContent() {
  const { showXP, showLevelUp, showStreakCeremony, showBadgeUnlock, play } =
    useJuice();
  const [xpPopup, setXpPopup] = useState({
    show: false,
    xp: 0,
    level: 0,
    streak: 0,
    badges: [],
  });
  const [celebration, setCelebration] = useState({
    show: false,
    type: "confetti",
    title: "",
    subtitle: "",
    xp: 0,
  });
  const [searchOpen, setSearchOpen] = useState(false);
  const searchInputRef = useRef(null);

  // Global XP listener — components can dispatch "xp-gained" event
  useEffect(() => {
    const handler = (e) => {
      const { xp, level, streak, badges } = e.detail || {};
      if (xp) {
        setXpPopup({
          show: true,
          xp,
          level: level || 0,
          streak: streak || 0,
          badges: badges || [],
        });
        showXP(xp, window.innerWidth / 2, window.innerHeight / 2);
        if (level) {
          setTimeout(() => showLevelUp(level), 300);
        }
        if (streak && (streak % 7 === 0 || streak === 1)) {
          setTimeout(() => showStreakCeremony(streak), 500);
        }
        if (badges && badges.length > 0) {
          badges.forEach((badge, i) => {
            setTimeout(() => showBadgeUnlock(badge), i * 800 + 500);
          });
        }
      }
    };
    const celebrationHandler = (e) => {
      const { type, title, subtitle, xp, message } = e.detail || {};
      setCelebration({
        show: true,
        type: type || "confetti",
        title: title || message || "",
        subtitle: subtitle || "",
        xp: xp || 0,
      });
      if (type === "levelup") {
        showLevelUp(title ? parseInt(title) : 1);
      }
      if (type === "streak") {
        showStreakCeremony(parseInt(subtitle) || 1);
      }
      if (type === "badge") {
        showBadgeUnlock({ name: title, emoji: "🏅" });
      }
      if (xp) {
        showXP(xp, window.innerWidth / 2, window.innerHeight / 2);
      }
    };
    window.addEventListener("xp-gained", handler);
    window.addEventListener("celebrate", celebrationHandler);
    return () => {
      window.removeEventListener("xp-gained", handler);
      window.removeEventListener("celebrate", celebrationHandler);
    };
  }, [showXP, showLevelUp, showStreakCeremony, showBadgeUnlock]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeydown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchOpen((prev) => !prev);
      }
      if (e.key === "Escape" && searchOpen) {
        setSearchOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeydown);
    return () => window.removeEventListener("keydown", handleKeydown);
  }, [searchOpen]);

  return (
    <>
      <div className="min-h-screen flex flex-col relative">
        <CustomCursor />
        <div className="relative z-10 flex flex-col min-h-screen">
          <Navbar />
          <main className="flex-1" id="main-content" role="main">
            <PageSuspense>
              <RouteErrorBoundary>
                <AnimatedRoutes />
              </RouteErrorBoundary>
            </PageSuspense>
          </main>
          <Footer />
          <Suspense fallback={null}>
            <Onboarding />
            <XPPopup
              show={xpPopup.show}
              xpGained={xpPopup.xp}
              level={xpPopup.level}
              streak={xpPopup.streak}
              newBadges={xpPopup.badges}
              onClose={() => setXpPopup((prev) => ({ ...prev, show: false }))}
            />
            <CelebrationOverlay
              show={celebration.show}
              type={celebration.type}
              title={celebration.title}
              subtitle={celebration.subtitle}
              xp={celebration.xp}
              onClose={() =>
                setCelebration((prev) => ({ ...prev, show: false }))
              }
            />
          </Suspense>
          <Suspense fallback={null}>
            <BottomNav />
          </Suspense>
        </div>
        <div className="h-16 md:hidden" />
      </div>
    </>
  );
}

export default function App() {
  const { loadUser } = useAuthStore();

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  return (
    <ErrorBoundary>
      <ToastProvider>
        <ThemeProvider>
          <JuiceProvider>
            <Router>
              <AppContent />
            </Router>
          </JuiceProvider>
        </ThemeProvider>
      </ToastProvider>
    </ErrorBoundary>
  );
}
