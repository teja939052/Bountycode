import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { useEffect, Suspense, useState, useCallback, useRef } from "react";
import { AnimatePresence } from "framer-motion";
import useAuthStore from "./store/authStore";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ErrorBoundary from "./components/ErrorBoundary";
import ProtectedRoute from "./components/ProtectedRoute";
import AuthLayout from "./components/AuthLayout";
import AnimatedPage from "./components/motion/AnimatedPage";
import Onboarding from "./components/Onboarding";
import { DashboardSkeleton } from "./components/ui/Skeleton";
import { SpaceBackground } from "./components/space";
import XPPopup from "./components/XPPopup";
import CelebrationOverlay from "./components/CelebrationOverlay";
import { ToastProvider } from "./components/Toast";

import {
  Landing,
  Login,
  Register,
  Dashboard,
  Interview,
  InterviewSession,
  ResumeBuilder,
  ATSOptimizer,
  Pricing,
  NotFound,
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
} from "./pages/lazy";
import Topics from "./pages/Topics";
import TopicProblems from "./pages/TopicProblems";
import CardCollection from "./pages/CardCollection";
import PersonalDashboard from "./pages/PersonalDashboard";

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password" element={<ResetPassword />} />
        <Route path="/pricing" element={<Pricing />} />

        <Route element={<ProtectedRoute><AuthLayout /></ProtectedRoute>}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/interview" element={<Interview />} />
          <Route path="/interview/:interviewId" element={<InterviewSession />} />
          <Route path="/resume" element={<ResumeBuilder />} />
          <Route path="/ats" element={<ATSOptimizer />} />
          <Route path="/aptitude" element={<AptitudeTest />} />
          <Route path="/cover-letter" element={<CoverLetter />} />
          <Route path="/salary-negotiation" element={<SalaryNegotiation />} />
          <Route path="/system-design" element={<SystemDesign />} />
          <Route path="/company-prep" element={<CompanyPrep />} />
          <Route path="/coding" element={<CodingChallenge />} />
          <Route path="/salary-benchmark" element={<SalaryBenchmark />} />

          <Route path="/settings" element={<Settings />} />
          <Route path="/history" element={<History />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/daily-drill" element={<DailyDrill />} />
          <Route path="/study-groups" element={<StudyGroups />} />
          <Route path="/contests" element={<MonthlyContests />} />
          <Route path="/predictor" element={<Predictor />} />

          <Route path="/question-bank" element={<QuestionBank />} />
          <Route path="/question-bank/progress" element={<MyProgress />} />
          <Route path="/question-bank/:questionId" element={<PracticeMode />} />
          <Route path="/fingerprint" element={<DSAFingerprint />} />
          <Route path="/tower" element={<TowerDashboard />} />

          <Route path="/company-mocks" element={<CompanyMocks />} />
          <Route path="/company-mocks/:testId" element={<CompanyMocks />} />
          <Route path="/alumni-experiences" element={<AlumniExperiences />} />
          <Route path="/placement-drives" element={<PlacementDrives />} />
          <Route path="/career-profile" element={<CareerProfile />} />
          <Route path="/applications" element={<ApplicationTracker />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/enterprise" element={<Enterprise />} />
          <Route path="/compiler" element={<Compiler />} />
          <Route path="/solve/:id" element={<SolveProblem />} />

          {/* DSA Practice Routes */}
          <Route path="/problems" element={<Topics />} />
          <Route path="/problems/:topic" element={<TopicProblems />} />

          {/* Card Collection */}
          <Route path="/cards" element={<CardCollection />} />

          {/* Indian Placement Prep */}
          <Route path="/indian-placement" element={<IndianPlacement />} />

          {/* Personal Dashboard */}
          <Route path="/my-dashboard" element={<PersonalDashboard />} />
        </Route>

        <Route path="*" element={<NotFound />} />
      </Routes>
    </AnimatePresence>
  );
}

function PageSuspense({ children }) {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      <AnimatedPage>
        {children}
      </AnimatedPage>
    </Suspense>
  );
}

export default function App() {
  const { loadUser } = useAuthStore();
  const [xpPopup, setXpPopup] = useState({ show: false, xp: 0, level: 0, streak: 0, badges: [] });
  const [celebration, setCelebration] = useState({ show: false, type: "confetti", message: "" });
  const [searchOpen, setSearchOpen] = useState(false);
  const searchInputRef = useRef(null);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  // Global XP listener — components can dispatch "xp-gained" event
  useEffect(() => {
    const handler = (e) => {
      const { xp, level, streak, badges } = e.detail || {};
      if (xp) {
        setXpPopup({ show: true, xp, level: level || 0, streak: streak || 0, badges: badges || [] });
      }
    };
    const celebrationHandler = (e) => {
      const { type, message } = e.detail || {};
      setCelebration({ show: true, type: type || "confetti", message: message || "Congratulations!" });
    };
    window.addEventListener("xp-gained", handler);
    window.addEventListener("celebrate", celebrationHandler);
    return () => {
      window.removeEventListener("xp-gained", handler);
      window.removeEventListener("celebrate", celebrationHandler);
    };
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeydown = (e) => {
      // Cmd+K or Ctrl+K to toggle search
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setSearchOpen((prev) => !prev);
      }
      // Escape to close search
      if (e.key === "Escape" && searchOpen) {
        setSearchOpen(false);
      }
    };
    window.addEventListener("keydown", handleKeydown);
    return () => window.removeEventListener("keydown", handleKeydown);
  }, [searchOpen]);

  return (
    <ErrorBoundary>
      <ToastProvider>
      <Router>
        <div className="min-h-screen flex flex-col relative">
          <SpaceBackground />
          <div className="relative z-10 flex flex-col min-h-screen">
            <Navbar />
            <main className="flex-1">
              <PageSuspense>
                <AnimatedRoutes />
              </PageSuspense>
            </main>
            <Footer />
            <Onboarding />
            <XPPopup
              show={xpPopup.show}
              xpGained={xpPopup.xp}
              level={xpPopup.level}
              streak={xpPopup.streak}
              newBadges={xpPopup.badges}
              onClose={() => setXpPopup(prev => ({ ...prev, show: false }))}
            />
            <CelebrationOverlay
              show={celebration.show}
              type={celebration.type}
              message={celebration.message}
              onClose={() => setCelebration(prev => ({ ...prev, show: false }))}
            />
          </div>
        </div>
      </Router>
      </ToastProvider>
    </ErrorBoundary>
  );
}
