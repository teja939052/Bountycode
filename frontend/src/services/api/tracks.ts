import { requestWithRetry as request } from "./request.ts";

export interface TrackBrief {
  id: string;
  title: string;
  difficulty: string;
  status: string;
  best_score: number | null;
  topic: string;
  companies: string[];
  provenance: string;
  statement: string;
  approach: string;
  complexity: { time?: string; space?: string };
  testcase_count: number;
}

export interface TrackSection {
  section: string;
  title: string;
  topics: { topic: string; count: number }[];
  practice_count: number;
  practice: TrackBrief[];
}

export interface TrackReadiness {
  foundation: { solved: number; total: number };
  coding: { solved: number; total: number };
  overall_percent: number;
  sections: { section: string; title: string; solved: number; total: number; percent: number }[];
  next_up_id: string | null;
  weakest_section: string | null;
  weakest_title: string | null;
}

export interface TrackOverview {
  company: string;
  structure: {
    title: string;
    duration_minutes: number;
    stages: { id: string; title: string; sections: string[]; note?: string }[];
    provenance?: string;
  } | null;
  track: string;
  verified_only: boolean;
  provenance_note: string;
  foundation: { sections: TrackSection[] };
  advanced_coding: {
    total: number;
    solved: number;
    problems: TrackBrief[];
  };
  readiness: TrackReadiness;
}

export const tracksApi = {
  overview(company: string): Promise<TrackOverview> {
    return request(`/api/v1/tracks/${encodeURIComponent(company)}/overview`);
  },
};