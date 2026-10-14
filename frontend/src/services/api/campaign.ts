// @ts-nocheck
import { requestWithRetry } from "./request";

export interface CampaignState {
  company: string;
  role: string;
  assessment_date: string;
}

export interface PatternMastery {
  id: string;
  name: string;
  emoji: string;
  mastery: number;
  attempts: number;
  accuracy: number | null;
  diagnosis: string[];
  last_practiced: string | null;
  question_count: number;
  is_weak: boolean;
  is_lowest: boolean;
  status: string;
}

export interface Round {
  id: string;
  name: string;
  icon: string;
  description: string;
  patterns: PatternMastery[];
}

export interface Battlefield {
  company: string;
  rounds: Round[];
  biggest_weakness: PatternMastery | null;
  total_patterns: number;
  mastered_patterns: number;
  weak_patterns: number;
}

export interface TodayRecommendation {
  id: string;
  type: string;
  priority: number;
  title: string;
  subtitle: string;
  emoji: string;
  estimated_minutes: number;
  pattern_id: string | null;
  round_id: string | null;
  reason: string;
  action: string;
}

export interface TodayPlan {
  company: string;
  role: string;
  assessment_date: string;
  days_remaining: number | null;
  streak: number;
  level: number;
  overall_score: number;
  overall_mastery: string;
  overall_mastery_label: string;
  recommendations: TodayRecommendation[];
  totals: { estimated_minutes: number; task_count: number };
  biggest_weakness: PatternMastery | null;
  battlefield_summary: {
    total_patterns: number;
    mastered_patterns: number;
    weak_patterns: number;
  };
}

export interface PatternDetail extends PatternMastery {
  round_id: string;
  round_name: string;
  mission_slug: string;
  why: string;
}

const campaignApi = {
  getState: () =>
    requestWithRetry<CampaignState>("/api/v1/campaign/state"),

  selectCampaign: (payload: { company: string; role?: string; assessment_date?: string }) =>
    requestWithRetry<{ success: boolean; campaign: CampaignState }>(
      "/api/v1/campaign/select",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    ),

  getBattlefield: (company?: string) =>
    requestWithRetry<Battlefield>(
      `/api/v1/campaign/battlefield${company ? `?company=${encodeURIComponent(company)}` : ""}`,
    ),

  getToday: (company?: string) =>
    requestWithRetry<TodayPlan>(
      `/api/v1/campaign/today${company ? `?company=${encodeURIComponent(company)}` : ""}`,
    ),

  getPattern: (patternId: string, company?: string) =>
    requestWithRetry<PatternDetail>(
      `/api/v1/campaign/patterns/${encodeURIComponent(patternId)}${company ? `?company=${encodeURIComponent(company)}` : ""}`,
    ),

  submitEvidence: (payload: { pattern_id: string; evidence: object }) =>
    requestWithRetry<{ success: boolean; pattern_id: string; stage_score: number; final_passed: boolean; mastery_update: number }>(
      "/api/v1/campaign/missions/evidence",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    ),

  getPlan: (company?: string) =>
    requestWithRetry<any>(
      `/api/v1/campaign/plan${company ? `?company=${encodeURIComponent(company)}` : ""}`,
    ),

  getBlueprint: (company: string) =>
    requestWithRetry<any>(
      `/api/v1/campaign/blueprint/${encodeURIComponent(company)}`,
    ),
};

export default campaignApi;
