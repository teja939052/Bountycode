import { useRef, useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { lazy } from "react";
import Landing from "../pages/Landing";
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
  SystemDesign,
  CodingChallenge,
  Settings,
  History,
  Leaderboard,
  DailyDrill,
  QuestionBank,
  PracticeMode,
  MyProgress,
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
  ProblemOfTheDay,
  Tower,
  DailyChallenge,
  DSAVisualizer,
  ResumeATS,
  MockOA,
  LearningHub,
  RoleSelect,
  JourneyPage,
  LevelMap,
  AdminDashboard,
  AdminContentCorpus,
  Topics,
  TopicProblems,
  PatternPage,
  CompanyTrack,
  SkillGraph,
  AIMentor,
  ChallengePacks,
  Practice,
  Concepts,
  LessonPage,
  LessonPlayer,
  LearningPaths,
  CompanyTracks,
  PrepHub,
  Terms,
  Privacy,
  FreeTrial,
  PwaSetup,
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
} from "../pages/lazy";
import ProtectedRoute from "../components/ProtectedRoute";
import OnboardingGuard from "../components/OnboardingGuard";
import FeatureErrorBoundary from "../components/FeatureErrorBoundary";

const AuthLayout = lazy(() => import("../components/AuthLayout"));

function usePageTracking() {
  const lastTrackedPath = useRef<string | null>(null);
  useEffect(() => {
    const location = window.location;
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
  });
}

export function AnimatedRoutes() {
  usePageTracking();

  return (
    <Routes>
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
        <Route path="/dashboard" element={<Navigate to="/journey" replace />} />
        {/* V3 unified: Journey / Practice / Target / Skills / Profile */}
        <Route path="/target" element={<Target />} />
        <Route path="/skills" element={<Skills />} />
        <Route path="/profile" element={<Profile />} />
        {/* V4 internal wiring: universal Mission Shell (roads, not nav) */}
        <Route path="/mission/:missionId" element={<Mission />} />
        <Route path="/mission/:missionId/result" element={<MissionResult />} />
        {/* Flagship guided mission: Sliding Window (World 1) */}
        <Route path="/mission/sliding-window" element={<SlidingWindowMission />} />
        <Route path="/mission/sliding-window/result" element={<MissionResult />} />
        <Route path="/me" element={<Navigate to="/profile" replace />} />
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
          path="/learn/lesson/:slug"
          element={
            <FeatureErrorBoundary featureName="Lesson">
              <LessonPlayer />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/levels"
          element={
            <FeatureErrorBoundary featureName="Level Map">
              <LevelMap />
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
        <Route path="/student-dashboard" element={<Navigate to="/journey" replace />} />
        <Route path="/my-dashboard" element={<Navigate to="/journey" replace />} />
        <Route path="/home" element={<Navigate to="/journey" replace />} />
        <Route path="/hub" element={<Navigate to="/journey" replace />} />
        <Route path="/compete" element={<Navigate to="/mock-oa" replace />} />
        <Route path="/career" element={<Navigate to="/career-profile" replace />} />
        <Route path="/prepare" element={<Navigate to="/journey" replace />} />
        <Route path="/company-mocks" element={<Navigate to="/mock-oa" replace />} />
        <Route path="/company-mocks/:testId" element={<Navigate to="/mock-oa" replace />} />
        <Route path="/practice" element={<Practice />} />
        <Route path="/analytics" element={<Navigate to="/skills" replace />} />
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
          path="/tcs-nqt"
          element={
            <FeatureErrorBoundary featureName="Assessment">
              <TcsNqtSimulation />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/exam-memory/submit"
          element={
            <FeatureErrorBoundary featureName="Exam Memory">
              <ExamMemorySubmission />
            </FeatureErrorBoundary>
          }
        />
        <Route
          path="/admin/exam-review"
          element={
            <FeatureErrorBoundary featureName="Exam Memory Review">
              <AdminExamReview />
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
          path="/system-design"
          element={
            <FeatureErrorBoundary featureName="System Design">
              <SystemDesign />
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
          path="/readiness"
          element={
            <ProtectedRoute>
              <FeatureErrorBoundary featureName="Readiness">
                <ReadinessHeatmap />
              </FeatureErrorBoundary>
            </ProtectedRoute>
          }
        />
        <Route
          path="/evidence"
          element={
            <ProtectedRoute>
              <FeatureErrorBoundary featureName="Evidence Dashboard">
                <EvidenceDashboard />
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
        <Route path="/learn/modules" element={<Navigate to="/learn" replace />} />
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
        <Route path="/admin/corpus" element={
          <ProtectedRoute>
            <AdminContentCorpus />
          </ProtectedRoute>
        } />
        <Route
          path="/my-assignments"
          element={<Navigate to="/dashboard" replace />}
        />

      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
