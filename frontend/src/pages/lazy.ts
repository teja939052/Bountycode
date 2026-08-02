import { lazy } from "react";

const routeImportFns = {
  Landing: () => import("./Landing"),
  Login: () => import("./Login"),
  Register: () => import("./Register"),
  Dashboard: () => import("./Dashboard"),
  Interview: () => import("./Interview"),
  InterviewSession: () => import("./InterviewSession"),
  ResumeBuilder: () => import("./ResumeBuilder"),
  ATSOptimizer: () => import("./ATSOptimizer"),
  AptitudeTest: () => import("./AptitudeTest"),
  CoverLetter: () => import("./CoverLetter"),
  SalaryNegotiation: () => import("./SalaryNegotiation"),
  SystemDesign: () => import("./SystemDesign"),
  CompanyPrep: () => import("./CompanyPrep"),
  CodingChallenge: () => import("./CodingChallenge"),
  SalaryBenchmark: () => import("./SalaryBenchmark"),
  Pricing: () => import("./Pricing"),
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
  AdminDashboard: () => import("./AdminDashboard"),
  Topics: () => import("./Topics"),
  TopicProblems: () => import("./TopicProblems"),
  CardCollection: () => import("./CardCollection"),
  PersonalDashboard: () => import("./PersonalDashboard"),
  AdaptivePath: () => import("./AdaptivePath"),
  LearningModules: () => import("./LearningModules"),
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
  SteamProfile: () => import("./SteamProfile"),
   LuckyWheel: () => import("./LuckyWheel"),
   Chat: () => import("./Chat"),
  BattlePass: () => import("./BattlePass"),
   Guilds: () => import("./Guilds"),
  GuildCastle: () => import("./GuildCastle"),
  ShareCard: () => import("./ShareCard"),
  CampusPulse: () => import("./CampusPulse"),
  TrendingChallenges: () => import("./TrendingChallenges"),
   SeasonalEvents: () => import("./SeasonalEvents"),
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

window.addEventListener("load", () => {
  const idleRoutes = ["Dashboard", "LearningHub", "TowerDashboard", "QuestionBank"];
  idleRoutes.forEach(name => preload[name]?.());
});

const Landing = lazy(() => import("./Landing"));
const Login = lazy(() => import("./Login"));
const Register = lazy(() => import("./Register"));
const Dashboard = lazy(() => import("./Dashboard"));
const Interview = lazy(() => import("./Interview"));
const InterviewSession = lazy(() => import("./InterviewSession"));
const ResumeBuilder = lazy(() => import("./ResumeBuilder"));
const ATSOptimizer = lazy(() => import("./ATSOptimizer"));
const AptitudeTest = lazy(() => import("./AptitudeTest"));
const CoverLetter = lazy(() => import("./CoverLetter"));
const SalaryNegotiation = lazy(() => import("./SalaryNegotiation"));
const SystemDesign = lazy(() => import("./SystemDesign"));
const CompanyPrep = lazy(() => import("./CompanyPrep"));
const CodingChallenge = lazy(() => import("./CodingChallenge"));
const SalaryBenchmark = lazy(() => import("./SalaryBenchmark"));
const Pricing = lazy(() => import("./Pricing"));
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
const AdminDashboard = lazy(() => import("./AdminDashboard"));
const Topics = lazy(() => import("./Topics"));
const TopicProblems = lazy(() => import("./TopicProblems"));
const CardCollection = lazy(() => import("./CardCollection"));
const PersonalDashboard = lazy(() => import("./PersonalDashboard"));
const AdaptivePath = lazy(() => import("./AdaptivePath"));
const LearningModules = lazy(() => import("./LearningModules"));
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
const ProjectGenerator = lazy(() => import('./ProjectGenerator'));
const LanguageLearning = lazy(() => import('./LanguageLearning'));
const OnboardingQuest = lazy(() => import('./OnboardingQuest'));
const InterviewBooking = lazy(() => import('./InterviewBooking'));
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
const CollegeNetwork = lazy(() => import('./CollegeNetwork'));
const Newspaper = lazy(() => import('./Newspaper'));
const SteamProfile = lazy(() => import('./SteamProfile'));
const Chat = lazy(() => import('./Chat'));
const Guilds = lazy(() => import('./Guilds'));
const GuildCastle = lazy(() => import('./GuildCastle'));
const ShareCard = lazy(() => import('./ShareCard'));
const CampusPulse = lazy(() => import('./CampusPulse'));
const TrendingChallenges = lazy(() => import('./TrendingChallenges'));
const LuckyWheel = lazy(() => import('./LuckyWheel'));
const BattlePass = lazy(() => import('./BattlePass'));
const CampusConnect = lazy(() => import('./CampusConnect'));
const AchievementChains = lazy(() => import('./AchievementChains'));
const ReferralGamification = lazy(() => import('./ReferralGamification'));
const SeasonalEvents = lazy(() => import('./SeasonalEvents'));
const SkillTrees = lazy(() => import('./SkillTrees'));
const TeamCompetitions = lazy(() => import('./TeamCompetitions'));
const Tournaments = lazy(() => import('./Tournaments'));
export {
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
  Landing,
  Login,
  Register,
  Dashboard,
  Interview,
  InterviewSession,
  ResumeBuilder,
  ATSOptimizer,
  AptitudeTest,
  CoverLetter,
  SalaryNegotiation,
  SystemDesign,
  CompanyPrep,
  CodingChallenge,
  SalaryBenchmark,
  Pricing,
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
  AdminDashboard,
  Topics,
  TopicProblems,
  CardCollection,
  PersonalDashboard,
  AdaptivePath,
  LearningModules,
  CodePlayground,
  CommandCenter,
   Scrims,
   ProjectGenerator,
   LanguageLearning,
  OnboardingQuest,
  InterviewBooking,
  Referral,
  InterviewReplay,
  FreeTrial,
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
   CampusConnect,
   Chat,
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
};