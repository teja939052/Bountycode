// @ts-nocheck
import { useRef, useEffect } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { lazy } from "react";
import Landing from "../pages/Landing";
import {
  Login,
  Register,
  Interview,
  InterviewSession,
  ResumeBuilder,
  ATSOptimizer,
  Pricing,
  NotFound,
  AptitudeTest,
  CodingChallenge,
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
  PracticeMode,
  LessonPlayer,
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
} from "../pages/lazy";
import ProtectedRoute from "../components/ProtectedRoute";
import OnboardingGuard from "../components/OnboardingGuard";

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
      <Route path="/" element={<HomeRedirect />} />
      <Route path="/landing" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/verify-email" element={<VerifyEmail />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/free-trial" element={<FreeTrial />} />
      <Route path="/terms" element={<Terms />} />
      <Route path="/privacy" element={<Privacy />} />
      <Route path="/free-trial" element={<FreeTrial />} />

      <Route path="/onboarding" element={
        <ProtectedRoute>
          <OnboardingQuest />
        </ProtectedRoute>
      } />
      <Route
        path="/diagnostic"
        element={
          <ProtectedRoute>
            <PlacementDiagnostic />
          </ProtectedRoute>
        }
      />
      <Route
        path="/mission/:slug"
        element={
          <ProtectedRoute>
            <MissionPlayer />
          </ProtectedRoute>
        }
      />
      <Route
        path="/battlefield"
        element={
          <ProtectedRoute>
            <CompanyBattlefield />
          </ProtectedRoute>
        }
      />
      <Route
        path="/round/:roundId"
        element={
          <ProtectedRoute>
            <RoundView />
          </ProtectedRoute>
        }
      />
      <Route
        path="/pattern/:id"
        element={
          <ProtectedRoute>
            <PatternDrill />
          </ProtectedRoute>
        }
      />
      <Route
        path="/learn/:domain"
        element={
          <ProtectedRoute>
            <UnifiedLessonPlayer />
          </ProtectedRoute>
        }
      />

      {/* ============================================================
          CORE APP ROUTES
         ============================================================ */}
      <Route
        element={
          <ProtectedRoute>
            <OnboardingGuard>
              <AuthLayout />
            </OnboardingGuard>
          </ProtectedRoute>
        }
      >
        {/* SERVICE PLACEMENT CAMPAIGN */}
        <Route path="/placement" element={<PlacementCampaign />} />
        <Route path="/curriculum" element={<PlacementCurriculum />} />
        <Route
          path="/mission-pack/:packId"
          element={
            <ProtectedRoute>
              <MissionPackPlayer />
            </ProtectedRoute>
          }
        />

        {/* LEARN CODING */}
        <Route path="/lab/lesson/:lessonId" element={<LessonPlayer />} />

        {/* SERVICE-BASED PREP */}
        <Route path="/aptitude" element={<AptitudeTest />} />
        <Route path="/mock-oa" element={<MockOA />} />
        <Route path="/coding" element={<CodingChallenge />} />
        <Route path="/question-bank" element={<QuestionBank />} />
        <Route path="/question-bank/:questionId" element={<PracticeMode />} />
        <Route path="/compiler" element={<Compiler />} />
        <Route path="/solve/:id" element={<SolveProblem />} />

        {/* COMPANY / ROLE PREP */}
        <Route path="/interview" element={<Interview />} />
        <Route path="/interview/:interviewId" element={<InterviewSession />} />

        {/* CAREER / UTILITY */}
        <Route path="/resume" element={<ResumeBuilder />} />
        <Route path="/ats" element={<ATSOptimizer />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/daily-challenge" element={<DailyChallenge />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

