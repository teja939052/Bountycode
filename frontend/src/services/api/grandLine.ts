import { requestWithRetry as request } from "./request.ts";

export interface GapItem {
  label: string;
  score: number;
  est_hours: number;
  key?: string;
  missing_points?: number;
}

export interface FleetEntry {
  company: string;
  display_name: string;
  overall_score: number;
  company_score: number;
  match_label: string;
  weeks_remaining?: number | null;
  estimated_date?: string | null;
  confidence?: string | null;
  requirements: {
    min_problems?: number | null;
    interview_rounds?: number | null;
    typical_timeline_weeks?: number | null;
  };
  top_gaps: GapItem[];
  verdict: string;
}

export interface GrandLineAssessment {
  general: {
    overall: number;
    categories: Record<string, { score: number; weight: number }>;
    prediction: Record<string, unknown>;
  };
  fleet: FleetEntry[];
  target: FleetEntry | null;
  voyage_plan: GapItem[];
  summary: string;
  your_stats: {
    total_problems: number;
    medium: number;
    hard: number;
    aptitude_tests: number;
    interviews_completed: number;
  };
}

export const grandLineApi = {
  assess(target?: string): Promise<GrandLineAssessment> {
    const q = target ? `?target=${encodeURIComponent(target)}` : "";
    return request(`/api/v1/grand-line/assess${q}`);
  },

  listTargets(): Promise<{
    targets: {
      key: string;
      name: string;
      focus_topics: string[];
      typical_timeline_weeks?: number;
    }[];
  }> {
    return request("/api/v1/grand-line/companies");
  },
};
