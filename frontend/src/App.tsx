import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import { useEffect, Suspense, useState, useCallback, useRef } from "react";
import useAuthStore from "./store/authStore";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import ErrorBoundary from "./components/ErrorBoundary";
import ProtectedRoute from "./components/ProtectedRoute";
import OnboardingGuard from "./components/OnboardingGuard";
import AuthLayout from "./components/AuthLayout";
import Onboarding from "./components/Onboarding";
import { DashboardSkeleton } from "./components/ui/Skeleton";
import { SpaceBackground } from "./components/space";
import XPPopup from "./components/XPPopup";
import CelebrationOverlay from "./components/CelebrationOverlay";
import { ToastProvider } from "./components/Toast";
import BottomNav from "./components/BottomNav";
import { JuiceProvider, useJuice } from "./juice/JuiceProvider";
import SoundToggle from "./juice/SoundToggle";
import AudioInitButton from "./juice/AudioInitButton";

import {
  Landing,
  Login,
  Register,
  OnboardingQuest,
  Dashboard,
  Interview,
  InterviewSession,
   InterviewBooking,
   InterviewReplay,
  ResumeBuilder,
  ATSOptimizer,
  Pricing,
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
  AdminDashboard,
  Topics,
  TopicProblems,
  CardCollection,
  PersonalDashboard,
  AdaptivePath,
   LearningModules,
   ProjectGenerator,
   LanguageLearning,
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
  AchievementChains,
  CampusPulse,
  CareerRpg,
  ChallengePacks,
  Chat,
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
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/pricing" element={<Pricing />} />
      <Route path="/free-trial" element={<FreeTrial />} />
      <Route path="/onboarding" element={<ProtectedRoute><OnboardingQuest /></ProtectedRoute>} />

      <Route element={<ProtectedRoute><OnboardingGuard><AuthLayout /></OnboardingGuard></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/journey" element={<ProtectedRoute><Journey /></ProtectedRoute>} />
        <Route path="/hub" element={<CommandCenter />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/interview/:interviewId" element={<InterviewSession />} />
        <Route path="/interview-booking" element={<InterviewBooking />} />
        <Route path="/interview-replay/:interviewId" element={<InterviewReplay />} />
        <Route path="/referral" element={<Referral />} />
        <Route path="/resume" element={<ResumeBuilder />} />
        <Route path="/ats" element={<ATSOptimizer />} />
        <Route path="/aptitude" element={<AptitudeTest />} />
        <Route path="/mock-oa" element={<MockOA />} />
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
        <Route path="/battle-pass" element={<BattlePass />} />
        <Route path="/campus-connect" element={<CampusConnect />} />
        <Route path="/campus-wars" element={<CampusWars />} />
        <Route path="/journeys" element={<LearningJourneys />} />
        <Route path="/challenge-packs" element={<ChallengePacks />} />
        <Route path="/community" element={<Community />} />
        <Route path="/ai-mentor" element={<AIMentor />} />
        <Route path="/playground" element={<CodePlayground />} />
        <Route path="/daily-challenge" element={<DailyChallenge />} />
        <Route path="/daily-challenge/leaderboard" element={<DailyChallenge />} />
        <Route path="/learn/modules" element={<LearningModules />} />
        <Route path="/dsa-visualizer" element={<DSAVisualizer />} />
        <Route path="/visualize/compare" element={<CompareVisualizer />} />
        <Route path="/resume-ats" element={<ResumeATS />} />
        <Route path="/mock-oa" element={<MockOA />} />
        <Route path="/learn" element={<LearningHub />} />
        <Route path="/learn/:languageId" element={<LanguageJourney />} />
        <Route path="/learn/:languageId/:levelId/:lessonId" element={<LessonView />} />

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

        {/* Scrims — Scrimba-style screencasts */}
        <Route path="/scrims" element={<Scrims />} />
        <Route path="/scrims/:scrimId" element={<Scrims />} />

        {/* Project Showcase Gallery */}
        <Route path="/showcase" element={<Showcase />} />
        <Route path="/showcase/:projectId" element={<ShowcaseDetail />} />

        {/* PWA / Offline / Notifications */}
        <Route path="/pwa" element={<ProtectedRoute><PwaSetup /></ProtectedRoute>} />

        {/* Admin Content Management */}
        <Route path="/admin-content" element={<ProtectedRoute><AdminContent /></ProtectedRoute>} />

        {/* My Assignments */}
        <Route path="/my-assignments" element={<ProtectedRoute><MyAssignments /></ProtectedRoute>} />

        {/* Game Events — Daily Boss, Seasons, Combo */}
        <Route path="/game-events" element={<ProtectedRoute><GameEvents /></ProtectedRoute>} />

        {/* Campus Wars — College Leaderboard */}
        <Route path="/campus" element={<ProtectedRoute><CampusWars /></ProtectedRoute>} />

        {/* Placement Timeline — contribution graph + milestones */}
        <Route path="/timeline" element={<ProtectedRoute><Timeline /></ProtectedRoute>} />

        {/* World Map + Skill Tree */}
        <Route path="/world" element={<ProtectedRoute><WorldMap /></ProtectedRoute>} />

        {/* Mystery Merchant + Prestige */}
        <Route path="/merchant" element={<ProtectedRoute><Merchant /></ProtectedRoute>} />

        {/* Guilds + Dungeons */}
        <Route path="/guilds" element={<ProtectedRoute><Dungeons /></ProtectedRoute>} />
        <Route path="/dungeons" element={<ProtectedRoute><Dungeons /></ProtectedRoute>} />

        {/* Collection Book + Live Events */}
        <Route path="/collection" element={<ProtectedRoute><CollectionEvents /></ProtectedRoute>} />

        {/* Player Economy — Marketplace, Decks, Equipment, Crafting, Login */}
        <Route path="/economy" element={<ProtectedRoute><Economy /></ProtectedRoute>} />

        {/* Retention Analytics Admin */}
        <Route path="/retention" element={<ProtectedRoute><RetentionAdmin /></ProtectedRoute>} />
        {/* Career RPG — Role Ladder */}
        <Route path="/career" element={<ProtectedRoute><CareerRpg /></ProtectedRoute>} />
        {/* College Network — Campus Community */}
        <Route path="/college" element={<ProtectedRoute><CollegeNetwork /></ProtectedRoute>} />
        {/* Steam-Style Profile — Aggregate identity */}
        <Route path="/profile/steam" element={<ProtectedRoute><SteamProfile /></ProtectedRoute>} />
        {/* Placement Times — Daily Newspaper */}
        <Route path="/newspaper" element={<ProtectedRoute><Newspaper /></ProtectedRoute>} />
        {/* Real-time Chat */}
        <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
        {/* Daily Lucky Wheel */}
        <Route path="/wheel" element={<ProtectedRoute><LuckyWheel /></ProtectedRoute>} />
        {/* Guilds — Team-based social gamification */}
        <Route path="/guilds" element={<ProtectedRoute><Guilds /></ProtectedRoute>} />
        {/* Guild Castle — Shared defense rooms */}
        <Route path="/guilds/castle/:guildId" element={<ProtectedRoute><GuildCastle /></ProtectedRoute>} />
        {/* Shareable Achievements — Viral share cards */}
        <Route path="/share" element={<ProtectedRoute><ShareCard /></ProtectedRoute>} />
        {/* Campus Pulse — Campus vs campus battles */}
        <Route path="/campus-pulse" element={<ProtectedRoute><CampusPulse /></ProtectedRoute>} />
        {/* Trending Challenges — Viral challenge feed */}
        <Route path="/trending" element={<ProtectedRoute><TrendingChallenges /></ProtectedRoute>} />
        {/* Seasonal Events */}
        <Route path="/seasonal" element={<ProtectedRoute><SeasonalEvents /></ProtectedRoute>} />
        {/* Achievement Chains */}
        <Route path="/achievements" element={<ProtectedRoute><AchievementChains /></ProtectedRoute>} />
        {/* Tournaments — Competitive brackets */}
        <Route path="/tournaments" element={<ProtectedRoute><Tournaments /></ProtectedRoute>} />
        {/* Team Competitions — College/Company teams */}
        <Route path="/teams" element={<ProtectedRoute><TeamCompetitions /></ProtectedRoute>} />
        {/* Referral Gamification */}
        <Route path="/referrals" element={<ProtectedRoute><ReferralGamification /></ProtectedRoute>} />
        {/* Skill Trees — Visual progression paths */}
        <Route path="/skill-trees" element={<ProtectedRoute><SkillTrees /></ProtectedRoute>} />
        {/* Battles — 1v1 Coding Battles */}
        <Route path="/battles" element={<BattleArena />} />
        <Route path="/battles/:battleId" element={<BattleArena />} />

        {/* Rank — Honor & Kyu/Dan System */}
        <Route path="/rank" element={<RankProfile />} />

        {/* Personal Dashboard */}
        <Route path="/my-dashboard" element={<PersonalDashboard />} />

        {/* Adaptive Learning Path */}
        <Route path="/adaptive" element={<AdaptivePath />} />

         {/* AI Project Generator */}
         <Route path="/project-generator" element={<ProjectGenerator />} />

         {/* Language Learning Paths - 7 languages x 100 levels x 80 modules */}
         <Route path="/languages" element={<LanguageLearning />} />
         <Route path="/languages/:languageId" element={<LanguageLearning />} />

         {/* Admin */}
        <Route path="/admin" element={<AdminDashboard />} />
      </Route>

      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

function PageSuspense({ children }) {
  return (
    <Suspense fallback={<DashboardSkeleton />}>
      {children}
    </Suspense>
  );
}

function AppContent() {
  const { showXP, showLevelUp, showStreakCeremony, showBadgeUnlock, play } = useJuice();
  const [xpPopup, setXpPopup] = useState({ show: false, xp: 0, level: 0, streak: 0, badges: [] });
  const [celebration, setCelebration] = useState({ show: false, type: "confetti", title: "", subtitle: "", xp: 0 });
  const [searchOpen, setSearchOpen] = useState(false);
  const searchInputRef = useRef(null);

  // Global XP listener — components can dispatch "xp-gained" event
  useEffect(() => {
    const handler = (e) => {
      const { xp, level, streak, badges } = e.detail || {};
      if (xp) {
        setXpPopup({ show: true, xp, level: level || 0, streak: streak || 0, badges: badges || [] });
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
      if (type === 'levelup') {
        showLevelUp(title ? parseInt(title) : 1);
      }
      if (type === 'streak') {
        showStreakCeremony(parseInt(subtitle) || 1);
      }
      if (type === 'badge') {
        showBadgeUnlock({ name: title, emoji: '🏅' });
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
      <AudioInitButton />
      <div className="min-h-screen flex flex-col relative">
        <SpaceBackground />
        <div className="relative z-10 flex flex-col min-h-screen">
          <Navbar />
<main className="flex-1" id="main-content" role="main">
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
            title={celebration.title}
            subtitle={celebration.subtitle}
            xp={celebration.xp}
            onClose={() => setCelebration(prev => ({ ...prev, show: false }))}
          />
          <SoundToggle />
          <BottomNav />
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
      <JuiceProvider>
      <Router>
        <AppContent />
      </Router>
      </JuiceProvider>
      </ToastProvider>
    </ErrorBoundary>
  );
}