import { requestWithRetry as request } from "./request.ts";

export type TcsNqtPattern = {
  pattern: string;
  count: number;
  domains: string[];
  skills: string[];
};

export type TcsNqtQuestion = {
  id: string;
  pattern: string;
  skill: string;
  domain: string;
  difficulty: string;
  trust_status: string;
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
  hints: string[];
  common_mistakes: string[];
  time_estimate_sec: number;
  company_relevance: Record<string, number>;
};

export type TcsNqtAssessResult = {
  pattern: string;
  score: number;
  correct: number;
  total: number;
  passed: boolean;
  mastery_threshold: number;
  results: Array<{
    id: string;
    correct: boolean;
    your_answer: string;
    correct_answer: string;
    explanation: string;
    common_mistakes: string[];
  }>;
  message: string;
};

export const tcsNqtApi = {
  getPatterns(): Promise<{ patterns: TcsNqtPattern[]; total_patterns: number }> {
    return request("/api/v1/tcs-nqt/patterns");
  },

  getPatternQuestions(
    pattern: string,
    params?: { limit?: number; difficulty?: string },
  ): Promise<{
    pattern: string;
    questions: TcsNqtQuestion[];
    total: number;
    returned: number;
  }> {
    const query = new URLSearchParams();
    if (params?.limit) query.set("limit", String(params.limit));
    if (params?.difficulty) query.set("difficulty", params.difficulty);
    const qs = query.toString();
    return request(`/api/v1/tcs-nqt/patterns/${encodeURIComponent(pattern)}${qs ? `?${qs}` : ""}`);
  },

  assessPattern(
    pattern: string,
    answers: Record<string, string>,
    timeSpentSeconds = 0,
  ): Promise<TcsNqtAssessResult> {
    return request(`/api/v1/tcs-nqt/patterns/${encodeURIComponent(pattern)}/assess`, {
      method: "POST",
      body: JSON.stringify({ answers, time_spent_seconds: timeSpentSeconds }),
    });
  },

  getProgress(): Promise<{
    progress: Array<{
      pattern: string;
      total_questions: number;
      verified_questions: number;
      domains: string[];
    }>;
    total_patterns: number;
    total_questions: number;
    total_verified: number;
  }> {
    return request("/api/v1/tcs-nqt/progress");
  },
};
