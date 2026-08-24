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
  SalaryNegotiation: () => import("./SalaryNegotiation"),
  SystemDesign: () => import("./SystemDesign"),
  CompanyPrep: () => import("./CompanyPrep"),
  CodingChallenge: () => import("./CodingChallenge"),
  SalaryBenchmark: () => import("./SalaryBenchmark"),
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
  CompanyMocks: () => import("./CompanyMocks"),
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
  DSAFingerprint: () => import("./DSAFingerprint"),
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
  CardCollection: () => import("./CardCollection"),
  PersonalDashboard: () => import("./PersonalDashboard"),
  AdaptivePath: () => import("./AdaptivePath"),
   LearningModules: () => import("./LearningModules"),
   LearningModule: () => import("./LearningModule"),
  ProblemOfTheDay: () => import("./ProblemOfTheDay"),
  DailyChallenge: () => import("./DailyChallenge"),
  DSAVisualizer: () => import("./DSAVisualizer"),
  LearningJourneys: () => import("./LearningJourneys"),
  ChallengePacks: () => import("./ChallengePacks"),
  AIMentor: () => import("./AIMentor"),
  CodePlayground: () => import("./CodePlayground"),
  CommandCenter: () => import("./CommandCenter"),
  CompareVisualizer: () => import("./CompareVisualizer"),
  Community: () => import("./Community"),
   Scrims: () => import("./Scrims"),
   BattleArena: () => import("./BattleArena"),
   RankProfile: () => import("./RankProfile"),
   RoleSelector: () => import("./RoleSelector"),
  ProjectGenerator: () => import("./ProjectGenerator"),
  LanguageLearning: () => import("./LanguageLearning"),
  OnboardingQuest: () => import("./OnboardingQuest"),
  InterviewBooking: () => import("./InterviewBooking"),
  Referral: () => import("./Referral"),
  InterviewReplay: () => import("./InterviewReplay"),
  FreeTrial: () => import("./FreeTrial"),
  Showcase: () => import("./Showcase"),
  ShowcaseDetail: () => import("./ShowcaseDetail"),
  PwaSetup: () => import("./PwaSetup"),
  AdminContent: () => import("./AdminContent"),
  MyAssignments: () => import("./MyAssignments"),
   GameEvents: () => import("./GameEvents"),
   Timeline: () => import("./Timeline"),
  WorldMap: () => import("./WorldMap"),
  Merchant: () => import("./Merchant"),
  Dungeons: () => import("./Dungeons"),
  CollectionEvents: () => import("./CollectionEvents"),
  Journey: () => import("./Journey"),
  Economy: () => import("./Economy"),
  RetentionAdmin: () => import("./RetentionAdmin"),
  CareerRpg: () => import("./CareerRpg"),
  CollegeNetwork: () => import("./CollegeNetwork"),
  CampusConnect: () => import("./CampusConnect"),
  CampusWars: () => import("./CampusWars"),
  Newspaper: () => import("./Newspaper"),
  StudentDashboard: () => import("./StudentDashboard"),
  SteamProfile: () => import("./SteamProfile"),
   LuckyWheel: () => import("./LuckyWheel"),
   Chat: () => import("./Chat"),
   GDRoom: () => import("./GDRoom"),
   CGPASimulator: () => import("./CGPASimulator"),
   DriveTracker: () => import("./DriveTracker"),
   PeerReview: () => import("./PeerReview"),
   StudySquads: () => import("./StudySquads"),
   PrepReportCard: () => import("./PrepReportCard"),
  BattlePass: () => import("./BattlePass"),
  StudyTimer: () => import("./StudyTimer"),
  Guilds: () => import("./Guilds"),
  GuildCastle: () => import("./GuildCastle"),
  ShareCard: () => import("./ShareCard"),
  CampusPulse: () => import("./CampusPulse"),
  TrendingChallenges: () => import("./TrendingChallenges"),
    SeasonalEvents: () => import("./SeasonalEvents"),
    BossAssessment: () => import("./BossAssessment"),
    MissionView: () => import("./MissionView"),
    BountyPage: () => import("./BountyPage"),
    JobReadiness: () => import("./JobReadiness"),
    CapabilityWorlds: () => import("./CapabilityWorlds"),
    CapabilityMission: () => import("./CapabilityMission"),
};

const preload = {};
const preloaded = new Set();
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
  "CompanyPrep",
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
const SalaryNegotiation = lazy(() => import("./SalaryNegotiation"));
const SystemDesign = lazy(() => import("./SystemDesign"));
const CompanyPrep = lazy(() => import("./CompanyPrep"));
const CodingChallenge = lazy(() => import("./CodingChallenge"));
const SalaryBenchmark = lazy(() => import("./SalaryBenchmark"));
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
const CompanyMocks = lazy(() => import("./CompanyMocks"));
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
const DSAFingerprint = lazy(() => import("./DSAFingerprint"));
const TowerDashboard = lazy(() => import("./TowerDashboard"));
const MockOA = lazy(() => import("./MockOA"));
const ResumeATS = lazy(() => import("./ResumeATS"));
const LearningHub = lazy(() => import("./LearningHub"));
const LanguageJourney = lazy(() => import("./LanguageJourney"));
const LessonView = lazy(() => import("./LessonView"));
const StudyLibrary = lazy(() => import("./StudyLibrary"));
const AdminDashboard = lazy(() => import("./AdminDashboard"));
const Topics = lazy(() => import("./Topics"));
const TopicProblems = lazy(() => import("./TopicProblems"));
const CardCollection = lazy(() => import("./CardCollection"));
const PersonalDashboard = lazy(() => import("./PersonalDashboard"));
const StudentDashboard = lazy(() => import("./StudentDashboard"));
const AdaptivePath = lazy(() => import("./AdaptivePath"));
const LearningModules = lazy(() => import("./LearningModules"));
const LearningModule = lazy(() => import("./LearningModule"));
const ProblemOfTheDay = lazy(() => import('./ProblemOfTheDay'));
const DailyChallenge = lazy(() => import('./DailyChallenge'));
const DSAVisualizer = lazy(() => import('./DSAVisualizer'));
const LearningJourneys = lazy(() => import('./LearningJourneys'));
const ChallengePacks = lazy(() => import('./ChallengePacks'));
const AIMentor = lazy(() => import('./AIMentor'));
const CodePlayground = lazy(() => import('./CodePlayground'));
const CommandCenter = lazy(() => import('./CommandCenter'));
const CompareVisualizer = lazy(() => import('./CompareVisualizer'));
const Community = lazy(() => import('./Community'));
const Scrims = lazy(() => import('./Scrims'));
const BattleArena = lazy(() => import('./BattleArena'));
const RankProfile = lazy(() => import('./RankProfile'));
const RoleSelector = lazy(() => import('./RoleSelector'));
const ProjectGenerator = lazy(() => import('./ProjectGenerator'));
const LanguageLearning = lazy(() => import('./LanguageLearning'));
const OnboardingQuest = lazy(() => import('./OnboardingQuest'));
const InterviewBooking = lazy(() => import('./InterviewBooking'));
const InterviewTerminal = lazy(() => import("./InterviewTerminal"));
const MassRecruiterExam = lazy(() => import("./MassRecruiterExam"));
const Referral = lazy(() => import('./Referral'));
const InterviewReplay = lazy(() => import('./InterviewReplay'));
const FreeTrial = lazy(() => import('./FreeTrial'));
const Showcase = lazy(() => import('./Showcase'));
const ShowcaseDetail = lazy(() => import('./ShowcaseDetail'));
const PwaSetup = lazy(() => import('./PwaSetup'));
const AdminContent = lazy(() => import('./AdminContent'));
const MyAssignments = lazy(() => import('./MyAssignments'));
const GameEvents = lazy(() => import('./GameEvents'));
const CampusWars = lazy(() => import('./CampusWars'));
const Timeline = lazy(() => import('./Timeline'));
const WorldMap = lazy(() => import('./WorldMap'));
const Merchant = lazy(() => import('./Merchant'));
const Dungeons = lazy(() => import('./Dungeons'));
const CollectionEvents = lazy(() => import('./CollectionEvents'));
const Journey = lazy(() => import('./Journey'));
const Economy = lazy(() => import('./Economy'));
const RetentionAdmin = lazy(() => import('./RetentionAdmin'));
const CareerRpg = lazy(() => import('./CareerRpg'));
const BehavioralPractice = lazy(() => import('./BehavioralPractice'));
const CompanyDirectory = lazy(() => import('./CompanyDirectory'));
const Concepts = lazy(() => import('./Concepts'));
const Quests = lazy(() => import('./Quests'));
const ReadinessScore = lazy(() => import('./ReadinessScore'));
const MysteryBoxPage = lazy(() => import('./MysteryBoxPage'));
const SkillMasteryPage = lazy(() => import('./SkillMasteryPage'));
const EnergyPage = lazy(() => import('./EnergyPage'));
const FriendsPage = lazy(() => import('./FriendsPage'));
const GoalsPage = lazy(() => import('./GoalsPage'));
const DiscussionsPage = lazy(() => import('./DiscussionsPage'));
const CollegeNetwork = lazy(() => import('./CollegeNetwork'));
const Newspaper = lazy(() => import('./Newspaper'));
const SteamProfile = lazy(() => import('./SteamProfile'));
const Chat = lazy(() => import('./Chat'));
const GDRoom = lazy(() => import('./GDRoom'));
const CGPASimulator = lazy(() => import('./CGPASimulator'));
const DriveTracker = lazy(() => import('./DriveTracker'));
const PeerReview = lazy(() => import('./PeerReview'));
const StudySquads = lazy(() => import('./StudySquads'));
const PrepReportCard = lazy(() => import('./PrepReportCard'));
const Guilds = lazy(() => import('./Guilds'));
const GuildCastle = lazy(() => import('./GuildCastle'));
const ShareCard = lazy(() => import('./ShareCard'));
const CampusPulse = lazy(() => import('./CampusPulse'));
const TrendingChallenges = lazy(() => import('./TrendingChallenges'));
const LuckyWheel = lazy(() => import('./LuckyWheel'));
const BattlePass = lazy(() => import('./BattlePass'));
const StudyTimer = lazy(() => import('./StudyTimer'));
const StudyGoals = lazy(() => import('./StudyGoals'));
const Home = lazy(() => import('./Home'));
const Prepare = lazy(() => import('./Prepare'));
const Practice = lazy(() => import('./Practice'));
const Compete = lazy(() => import('./Compete'));
const Career = lazy(() => import('./Career'));
const ThemesPage = lazy(() => import('./CustomThemes'));
const CampusConnect = lazy(() => import('./CampusConnect'));
const AchievementChains = lazy(() => import('./AchievementChains'));
const HealthDashboard = lazy(() => import('./HealthDashboard'));
const ReferralGamification = lazy(() => import('./ReferralGamification'));
const SeasonalEvents = lazy(() => import('./SeasonalEvents'));
const SkillTrees = lazy(() => import('./SkillTrees'));
const TeamCompetitions = lazy(() => import('./TeamCompetitions'));
const Tournaments = lazy(() => import('./Tournaments'));
const BossAssessment = lazy(() => import('./BossAssessment'));
const MissionView = lazy(() => import('./MissionView'));
const Mission = lazy(() => import('./Mission'));
const JourneyMapPage = lazy(() => import('./JourneyMapPage'));
const BountyPage = lazy(() => import('./BountyPage'));
const JobReadiness = lazy(() => import('./JobReadiness'));
const CapabilityWorlds = lazy(() => import('./CapabilityWorlds'));
const CapabilityMission = lazy(() => import('./CapabilityMission'));
export {
  CurriculumHub,
  LearnTrack,
  LearnLesson,
  CompareVisualizer,
  Community,
  ProblemOfTheDay,
  DailyChallenge,
  DSAVisualizer,
  LearningJourneys,
  ChallengePacks,
  AIMentor,
  BattleArena,
  RankProfile,
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
  SalaryNegotiation,
  SystemDesign,
  CompanyPrep,
  CodingChallenge,
  SalaryBenchmark,
  Pricing,
  PlacementCalendar,
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
  MockOA,
  ResumeATS,
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
  CodePlayground,
  CommandCenter,
    Scrims,
    ProjectGenerator,
    LanguageLearning,
    OnboardingQuest,
    InterviewBooking,
    InterviewTerminal,
    MassRecruiterExam,
    Referral,
    InterviewReplay,
    FreeTrial,
    RoleSelector,
  Showcase,
  ShowcaseDetail,
  PwaSetup,
  AdminContent,
  MyAssignments,
  GameEvents,
  CampusWars,
  Timeline,
  WorldMap,
  Merchant,
  Dungeons,
  CollectionEvents,
  Journey,
  Economy,
  RetentionAdmin,
   CareerRpg,
   CollegeNetwork,
   Newspaper,
   SteamProfile,
   LuckyWheel,
   BattlePass,
   StudyTimer,
   StudyGoals,
   ThemesPage,
   CampusConnect,
   Chat,
   GDRoom,
   CGPASimulator,
   DriveTracker,
   PeerReview,
   StudySquads,
   PrepReportCard,
   Guilds,
  GuildCastle,
  ShareCard,
  CampusPulse,
  TrendingChallenges,
   SeasonalEvents,
    AchievementChains,
     Tournaments,
     TeamCompetitions,
     ReferralGamification,
     SkillTrees,
      HealthDashboard,
BossAssessment,
       MissionView,
         Mission,
         JourneyMapPage,
         BountyPage,
        JobReadiness,
        CapabilityWorlds,
        CapabilityMission,
        Home,
     Prepare,
     Practice,
     Compete,
      Career,
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
};