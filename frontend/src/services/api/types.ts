export interface ApiErrorResponse {
  detail?: string;
  error_explanation?: string | null;
  [key: string]: unknown;
}

export interface AuthUser {
  id: string;
  email: string;
  name: string;
  plan: "free" | "pro" | "lifetime" | string;
  email_verified?: boolean;
  is_admin?: boolean;
  role?: string;
  onboarding?: Record<string, unknown>;
  usage?: UsageStats;
  xp?: number;
  level?: number;
  streak?: number;
  college?: string;
  league?: string;
  gamification?: Record<string, unknown>;
}

export interface UsageStats {
  plan?: string;
  interviews_used?: number;
  interviews_limit?: number | string;
  resumes_used?: number;
  resumes_limit?: number | string;
  aptitude_used?: number;
  aptitude_limit?: number | string;
  cover_letters_used?: number;
  cover_letters_limit?: number | string;
  company_mocks_used?: number;
  company_mocks_limit?: number | string;
  predictions_used?: number;
  predictions_limit?: number | string;
  question_bank_used?: number;
  question_bank_limit?: number | string;
  features?: Record<
    string,
    { monthly_limit: number | string; monthly_used: number }
  >;
}

export interface LoginResponse {
  token: string;
  user: AuthUser;
}

export interface RegisterResponse {
  token: string;
  user: AuthUser;
}

export interface Interview {
  id: string;
  question: string;
  question_type?: string;
  difficulty?: string;
  company?: string;
  job_role?: string;
  tips?: string;
  questions_asked?: string[];
  follow_up?: boolean;
}

export interface InterviewStartResponse {
  interview_id: string;
  question: string;
  question_type?: string;
  difficulty?: string;
  company?: string;
  company_style?: string;
  tips?: string;
  total_questions?: number;
  [key: string]: unknown;
}

export interface InterviewResult {
  interview_id: string;
  job_role?: string;
  company?: string;
  overall_score?: number;
  score_breakdown?: Record<string, number>;
  questions?: Array<{
    question: string;
    answer: string;
    score: number;
    difficulty?: string;
    is_follow_up?: boolean;
    feedback?: {
      strengths?: string[];
      improvements?: string[];
      better_answer?: string;
      reaction?: string;
      breakdown?: Record<string, number>;
    };
  }>;
  total_score?: number;
  max_score?: number;
  feedback?: string;
  strengths?: string[];
  weaknesses?: string[];
  improvement_tips?: string[];
  difficulty_progression?: string[];
  strength_areas?: string[];
  improvement_areas?: string[];
  readiness_score?: number;
  communication_score?: number;
  total_questions?: number;
  xp_earned?: number;
  level_up?: boolean;
  [key: string]: unknown;
}

export interface InterviewHistoryItem {
  id: string;
  interview_id?: string;
  job_role?: string;
  company?: string;
  interview_type?: string;
  overall_score?: number;
  score?: number;
  max_score?: number;
  feedback?: string;
  created_at?: string;
  date?: string;
  [key: string]: unknown;
}

export interface QuestionFilters {
  companies: string[];
  roles: string[];
  topics: string[];
  sub_topics: string[];
  types: string[];
  difficulties: string[];
  patterns: string[];
  sources: string[];
}

export interface QuestionItem {
  id: string;
  question?: string;
  question_title?: string;
  difficulty?: string;
  topic?: string;
  sub_topic?: string;
  company?: string | string[];
  type?: string;
  upvotes?: number;
  acceptance_rate?: number;
  description?: string;
  examples?: Array<{ input: string; output: string; explanation?: string }>;
  constraints?: string[];
  [key: string]: unknown;
}

export interface QuestionDetail {
  id: string;
  question: string;
  question_title?: string;
  difficulty?: string;
  topic?: string;
  sub_topic?: string;
  company?: string | string[];
  description?: string;
  examples?: Array<{ input: string; output: string; explanation?: string }>;
  constraints?: string[];
  starter_code?: string;
  solution?: string;
  time_complexity?: string;
  space_complexity?: string;
  [key: string]: unknown;
}

export interface BrowseResult {
  questions: QuestionItem[];
  total: number;
  pages: number;
}

export interface QuestionStats {
  total_solved?: number;
  easy_solved?: number;
  medium_solved?: number;
  hard_solved?: number;
  expert_solved?: number;
  acceptance_rate?: number;
  by_difficulty?: {
    easy: number;
    medium: number;
    hard: number;
    expert: number;
  };
  [key: string]: unknown;
}

export interface SolutionHint {
  hint: string;
  hint_level: number;
  solution?: string;
  explanation?: string;
}

export interface SubmitResult {
  passed: boolean;
  score: number;
  feedback: string;
  runtime?: number;
  memory?: number;
  all_passed?: boolean;
  test_results?: Array<{ name: string; passed: boolean; output?: string }>;
}

export interface LanguageInfo {
  language: string;
  version: string;
  aliases?: string[];
}

export interface ExecutionResult {
  success: boolean;
  output: string;
  error?: string;
  execution_time_ms?: number;
  memory_bytes?: number;
}

export interface TestCaseResult {
  name: string;
  passed: boolean;
  expected: string;
  actual: string;
  output?: string;
}

export interface ResumeData {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  summary?: string;
  experience?: Array<ExperienceEntry>;
  education?: Array<EducationEntry>;
  skills?: string[];
  projects?: Array<ProjectEntry>;
  ats_score?: number;
  ats_keywords?: Array<{ keyword: string; matched: boolean }>;
  missing_keywords?: string[];
  created_at?: string;
}

export interface ExperienceEntry {
  company: string;
  title: string;
  start_date?: string;
  end_date?: string;
  location?: string;
  bullets?: string[];
}

export interface EducationEntry {
  institution: string;
  degree?: string;
  field?: string;
  start_date?: string;
  end_date?: string;
  gpa?: string;
}

export interface ProjectEntry {
  name: string;
  description?: string;
  tech_stack?: string[];
  live_url?: string;
  repo_url?: string;
  bullets?: string[];
}

export interface ResumeAnalysis {
  ats_score: number;
  keyword_match: number;
  missing_keywords: string[];
  suggestions: Array<{
    type: string;
    text: string;
    severity?: "high" | "medium" | "low";
  }>;
  readability_score?: number;
}

export interface ATSScoreResponse {
  ats_score: number;
  match_ratio: number;
  keyword_analysis: Array<{
    keyword: string;
    found: boolean;
    frequency?: number;
  }>;
  missing_keywords: string[];
  suggestions?: Array<{
    type: string;
    text: string;
  }>;
}

export interface AptitudeCategory {
  id: string;
  name: string;
  description?: string;
  question_count?: number;
}

export interface AptitudeQuestion {
  id: string;
  question: string;
  options: string[];
  correct_answer: number;
  explanation?: string;
  difficulty?: string;
  category?: string;
}

export interface TestSession {
  test_id: string;
  category: string;
  difficulty: string;
  questions: AptitudeQuestion[];
  start_time: string;
  end_time?: string;
  time_limit?: number;
}

export interface TestResult {
  test_id: string;
  score: number;
  total: number;
  percentage: number;
  correct_answers: number;
  wrong_answers: number;
  time_taken?: number;
  category?: string;
  questions_review?: Array<{
    question: string;
    selected_answer: number;
    correct_answer: number;
    correct: boolean;
    explanation?: string;
  }>;
}

export interface BillingStatus {
  plan: "free" | "pro" | "lifetime";
  status: "active" | "canceled" | "past_due" | "incomplete";
  current_period_end?: string;
  cancel_at_period_end?: boolean;
  usage?: UsageStats;
}

export interface CheckoutResponse {
  approval_url?: string;
  order_id?: string;
  status?: string;
  client_secret?: string;
  session_id?: string;
}

export interface PlanInfo {
  id: string;
  name: string;
  description?: string;
  price: number;
  currency?: string;
  interval?: string;
  features: string[];
  is_popular?: boolean;
}

export interface CouponValidation {
  valid: boolean;
  discount: number;
  plan_restriction?: string[];
  expires_at?: string;
  message?: string;
}

export interface GamificationProfile {
  xp?: number;
  level?: number;
  streak?: number;
  longest_streak?: number;
  xp_to_next?: number;
  xp_for_current?: number;
  today_xp?: number;
  total_solved?: number;
  ranking?: number;
  badges?: Badge[];
  streak_freezes?: number;
  coins?: number;
  title?: string;
  title_emoji?: string;
  wizard_outfit?: string;
  [key: string]: unknown;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  emoji?: string;
  rarity?: "common" | "rare" | "epic" | "legendary";
  earned_at?: string;
  earned?: boolean;
}

export interface TowerData {
  level: number;
  xp: number;
  xp_to_next: number;
  tower_level: number;
  bosses_beaten: number;
  power_ups: PowerUp[];
  challenges: Challenge[];
  streak_freezes?: number;
  coins?: number;
}

export interface PowerUp {
  id: string;
  name: string;
  description: string;
  cost: number;
  icon: string;
  owned?: boolean;
  active?: boolean;
}

export interface Challenge {
  id: string;
  type: string;
  title: string;
  description: string;
  reward_xp?: number;
  reward_coins?: number;
  completed?: boolean;
  progress?: number;
  target?: number;
}

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  name?: string;
  xp?: number;
  level?: number;
  streak?: number;
  avatar?: string;
}

export interface SkillNode {
  id: string;
  name: string;
  description?: string;
  level: number;
  max_level: number;
  xp: number;
  xp_to_next?: number;
  prerequisites?: string[];
  category?: string;
}

export interface StartupState {
  level: number;
  xp: number;
  streak: number;
  streak_freezes: number;
  streak_protected: boolean;
  streak_protect_message: string;
  streak_protect?: boolean;
  league?: LeagueInfo;
  tier?: string;
  rank?: number;
  of?: number;
  weekly_xp?: number;
  promoted_next_week?: boolean;
  relegated_next_week?: boolean;
  [key: string]: unknown;
}

export interface LeagueInfo {
  tier: string;
  name: string;
  color?: string;
  icon?: string;
  rank?: number;
  of?: number;
  weekly_xp?: number;
  promoted_next_week?: boolean;
  relegated_next_week?: boolean;
}

export interface StreakStatus {
  streak?: number;
  streak_protected?: boolean;
  streak_protect_message?: string;
  streak_freezes?: number;
  last_active?: string;
  next_reset?: string;
  streak_in_danger?: boolean;
  daily_bonus_claimed_today?: boolean;
  [key: string]: unknown;
}

export interface CompanyProfile {
  id: string;
  name: string;
  description?: string;
  industry?: string;
  size?: string;
  location?: string;
  interview_difficulty?: string;
  acceptance_rate?: number;
  questions?: QuestionItem[];
  behavioral_questions?: Array<{
    question: string;
    category?: string;
    answer_tips?: string[];
  }>;
  faqs?: Array<{ question: string; answer: string }>;
  interview_tips?: string[];
}

export interface BookingConfig {
  company: string;
  interview_type: string;
  role?: string;
  difficulty?: string;
  scheduled_at?: string;
}

export interface BookingSlot {
  date: string;
  slots: Array<{
    time: string;
    available: boolean;
    slot_id?: string;
  }>;
}

export interface BookingDetail {
  id: string;
  company: string;
  role: string;
  interview_type: string;
  scheduled_at: string;
  status: string;
  interviewer?: string;
  meeting_link?: string;
  reminders?: string[];
}

export interface LearningModule {
  id: string;
  title: string;
  description?: string;
  lessons: Lesson[];
  progress?: number;
  xp_reward?: number;
  completed?: boolean;
}

export interface Lesson {
  id: string;
  title: string;
  content: string;
  order: number;
  duration?: number;
  completed?: boolean;
}

export interface Scrim {
  id: string;
  title: string;
  description?: string;
  duration?: number;
  instructor?: string;
  video_url?: string;
  transcript?: string;
  questions?: Array<{ id: string; question: string; answer: string }>;
  completed?: boolean;
}

export interface DailyChallengeData {
  id: string;
  title: string;
  description?: string;
  difficulty?: string;
  category?: string;
  rewards?: Array<{ type: string; amount: number }>;
  expires_at?: string;
  solved?: boolean;
}

export interface UserProfileStats {
  id: string;
  name: string;
  email?: string;
  level?: number;
  xp?: number;
  streak?: number;
  total_solved?: number;
  plan?: string;
  achievements?: Badge[];
  integrations?: Record<string, string>;
  [key: string]: unknown;
}

export interface OnboardingStatus {
  completed: boolean;
  step?: string;
  progress?: number;
}

export interface OnboardingData {
  name?: string;
  email?: string;
  college?: string;
  year?: string;
  branch?: string;
  skills?: string[];
  goals?: string[];
  experience?: string;
}

export interface StreakRepairResult {
  success: boolean;
  message: string;
  cost?: number;
  upgrade_required?: boolean;
}
