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
  useRef,
  lazy,
} from "react";
import useAuthStore from "./store/authStore";
import { useGamificationData } from "./hooks/useGamificationData";
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
import CookieBanner from "./components/CookieBanner";
import Landing from "./pages/Landing";
import ComboCounter from "./components/ComboCounter";
import ComboWarningOverlay from "./juice/ComboWarningOverlay";
import CriticalHitOverlay from "./juice/CriticalHitOverlay";

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
  Interview,
  InterviewSession,
  InterviewBooking,
  InterviewReplay,
  ResumeBuilder,
  ResumeStudio,
  ATSOptimizer,
  Pricing,
  PlacementCalendar,
  NotFound,
  CodePlayground,
  CompareVisualizer,
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
  Predictor,
  QuestionBank,
  PracticeMode,
  MyProgress,
  CompanyMocks,
  AlumniExperiences,
  PlacementDrives,
  CareerProfile,
  ApplicationTracker,
  Compiler,
  SolveProblem,
  ForgotPassword,
  ResetPassword,
  MonthlyContests,
  IndianPlacement,
  StudyTimer,
  StudyGoals,
  ProblemOfTheDay,
  Tower,
  DailyChallenge,
  DSAVisualizer,
  ResumeATS,
  MockOA,
  LearningHub,
  RoleSelect,
  JourneyPage,
  AdminDashboard,
  Topics,
  TopicProblems,
  PatternPage,
  CompanyTrack,
  DuolingoPage,
  SkillGraph,
  AIMentor,
  ChallengePacks,
  Home,
  Prepare,
  Practice,
  Compete,
  Career,
  Community,
  Concepts,
  LessonPage,
  LearningPaths,
  CompanyTracks,
  PrepHub,
  Terms,
  Privacy,
  FreeTrial,
  StudentDashboard,
  LanguageLearning,
  PwaSetup,
} from "./pages/lazy";

function AnimatedRoutes() {
  const location = useLocation();
  const lastTrackedPath = useRef<string | null>(null);

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
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />
<Route path="/pricing" element={<Pricing />} />
<Route path="/free-trial" element={<FreeTrial />} />
<Route path="/terms" element={<Terms />} />
<Route path="/privacy" element={<Privacy />} />
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
          path="/journey"
          element={
            <FeatureErrorBoundary featureName="Journey">
              <JourneyPage />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/lesson/:slug"
          element={
            <FeatureErrorBoundary featureName="Lesson">
              <LessonPage />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/role-select"
          element={
            <FeatureErrorBoundary featureName="Role Select">
              <RoleSelect />
            </FeatureErrorBoundary>
          }
        />
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
        <Route path="/learning" element={<Navigate to="/learn" replace />} />
        <Route path="/learning-paths" element={<LearningPaths />} />
        <Route path="/company-tracks" element={<CompanyTracks />} />
        <Route path="/prep-hub" element={<PrepHub />} />
        <Route path="/concepts" element={<Concepts />} />

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
          path="/interview-replay/:interviewId"
          element={
            <FeatureErrorBoundary featureName="Interview">
              <InterviewReplay />
            </FeatureErrorBoundary>
          }
        />

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
          path="/tower"
          element={
            <ProtectedRoute>
              <FeatureErrorBoundary featureName="Gamification">
                <Tower />
              </FeatureErrorBoundary>
            </ProtectedRoute>
          }
        />
        <Route
          path="/skill-graph"
          element={
            <ProtectedRoute>
              <FeatureErrorBoundary featureName="Skill Graph">
                <SkillGraph />
              </FeatureErrorBoundary>
            </ProtectedRoute>
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
          path="/pattern/:patternId"
          element={
            <FeatureErrorBoundary featureName="Question Bank">
              <PatternPage />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/tracks/:company"
          element={
            <FeatureErrorBoundary featureName="Company Prep">
              <CompanyTrack />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/language-loop"
          element={
            <FeatureErrorBoundary featureName="Learning">
              <DuolingoPage />
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
        <Route path="/admin" element={
          <ProtectedRoute>
            <AdminDashboard />
          </ProtectedRoute>
        } />
        <Route
          path="/admin-content"
          element={<Navigate to="/admin" replace />}
        />
        <Route
          path="/my-assignments"
          element={<Navigate to="/dashboard" replace />}
        />

      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

function PageSuspense({ children }: { children: React.ReactNode }) {
  return <Suspense fallback={<DashboardSkeleton />}>{children}</Suspense>;
}

function AppContent() {
  const { showXP, showLevelUp, showStreakCeremony, showBadgeUnlock, showBossDefeat, showDailyLogin, showAchievement, showCriticalHit, screenShake } =
    useJuice();
  const [xpPopup, setXpPopup] = useState({
    show: false,
    xp: 0,
    level: 0,
    streak: 0,
    badges: [] as string[],
    critical: false,
    criticalBonus: 0,
  });
  const [celebration, setCelebration] = useState({
    show: false,
    type: "confetti",
    title: "",
    subtitle: "",
    xp: 0,
  });
  const [searchOpen, setSearchOpen] = useState(false);

  const { combo } = useGamificationData();
  const currentCombo = (combo?.current_combo as number | undefined) ?? 0;
  const comboMultiplier = (combo?.multiplier as number | undefined) ?? 1;

  // Global XP listener — components can dispatch "xp-gained" event
  useEffect(() => {
    const handler = (e: Event) => {
      const detail = (e as CustomEvent).detail || {};
      const { xp, level, streak, badges, critical, boss, dailyLogin, achievement } = detail;
      if (xp) {
        const isBig = (xp || 0) >= 100;
        setXpPopup({
          show: true,
          xp,
          level: level || 0,
          streak: streak || 0,
          badges: (badges as string[]) || [],
          critical: critical || false,
          criticalBonus: (critical as { bonus?: number } | undefined)?.bonus || 0,
        });
        showXP(xp, window.innerWidth / 2, window.innerHeight / 2, isBig);
        if (critical) {
          showCriticalHit('CRITICAL HIT!', `+${Math.round(((critical as { bonus?: number } | undefined)?.bonus || 0) * 100)}% Bonus`);
        }
        if (level) {
          setTimeout(() => showLevelUp(level), 300);
        }
        if (streak && (streak % 7 === 0 || streak === 1)) {
          setTimeout(() => showStreakCeremony(streak), 500);
        }
        if (badges && (badges as string[])?.length > 0) {
          (badges as string[]).forEach((badge, i) => {
            setTimeout(() => showBadgeUnlock(badge), i * 800 + 500);
          });
        }
        if (boss) {
          setTimeout(() => showBossDefeat(boss), 400);
          screenShake(10, 600);
        }
        if (dailyLogin) {
          setTimeout(() => showDailyLogin(dailyLogin.reward, dailyLogin.streak), 200);
        }
        if (achievement) {
          setTimeout(() => showAchievement(achievement), 300);
        }
      }
    };
    const celebrationHandler = (e: Event) => {
      const { type, title, subtitle, xp, message } = (e as CustomEvent).detail || {};
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
  }, [showXP, showLevelUp, showStreakCeremony, showBadgeUnlock, showBossDefeat, showDailyLogin, showAchievement, showCriticalHit, screenShake]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeydown = (e: KeyboardEvent) => {
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
          <CookieBanner />
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
            <ComboCounter
              combo={currentCombo}
              multiplier={comboMultiplier}
              visible={currentCombo >= 2}
            />
            <ComboWarningOverlay
              seconds={(combo?.combo_decay_seconds as number | undefined) ?? 0}
              visible={currentCombo >= 3}
            />
            <CriticalHitOverlay
              visible={celebration?.type === 'critical'}
              text={celebration?.title}
              subtext={celebration?.subtitle}
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
