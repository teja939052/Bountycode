import { requestWithRetry as request } from "./request.ts";

export interface CompanyMockQuestion {
  id: string;
  question: string;
  title?: string;
  difficulty?: string;
  topic?: string;
  round?: string;
  description?: string;
  examples?: Array<{ input?: string; output?: string }>;
  constraints?: string[] | string;
  starter_code?: Record<string, string> | string;
  function_name?: string;
  time_limit_seconds?: number;
  memory_limit_mb?: number;
}

export interface CompanyMockRound {
  name: string;
  type: string;
  questions: number;
  time_minutes: number;
  difficulty: string;
  focus: string[];
  format?: string;
}

export interface CompanyMockCompany {
  id: string;
  name: string;
  description: string;
  total_time_minutes: number;
  rounds_count: number;
  passing_score: number;
}

export interface CompanyMockStartResponse {
  session_id: string;
  company: string;
  config: Record<string, unknown>;
  rounds: CompanyMockRound[];
  unsupported_rounds: string[];
  questions: CompanyMockQuestion[];
  ends_at: string;
}

export interface CompanyMockStatus {
  session_id: string;
  status: "in_progress" | "completed" | string;
  time_remaining_seconds: number;
  current_round: number;
  questions_answered: number;
  total_questions: number;
  company?: string;
  ends_at?: string | null;
  started_at?: string | null;
  unsupported_rounds?: string[];
  answers?: Array<{
    question_id: string;
    code: string;
    language: string;
    is_correct: boolean;
    passed_count: number;
    total_count: number;
    score: number;
    summary: string;
  }>;
  questions?: CompanyMockQuestion[];
}

export interface CompanyMockAnswerResponse {
  success: boolean;
  question_id: string;
  is_correct: boolean;
  passed_count: number;
  total_count: number;
  score: number;
  summary: string;
}

export interface CompanyMockResults {
  session_id: string;
  company: string;
  total_score: number;
  passing_score: number;
  passed: boolean;
  round_scores: Record<string, { total: number; score: number; count: number }>;
  completed_at: string;
  interview_tips: string[];
}

export const companyMocksApi = {
  getCompanies(): Promise<{ companies: CompanyMockCompany[] }> {
    return request("/api/v1/company-mocks/companies");
  },

  getConfig(companyId: string): Promise<Record<string, unknown>> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(companyId)}/config`,
    );
  },

  start(
    companyId: string,
    roundName: string | null = null,
  ): Promise<CompanyMockStartResponse> {
    const query = roundName
      ? `?round_name=${encodeURIComponent(roundName)}`
      : "";
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(companyId)}/start${query}`,
      { method: "POST" },
    );
  },

  submitAnswer(
    sessionId: string,
    payload: { question_id: string; code: string; language: string; time_spent_seconds?: number },
  ): Promise<CompanyMockAnswerResponse> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(sessionId)}/answer`,
      { method: "POST", body: JSON.stringify(payload) },
    );
  },

  complete(sessionId: string): Promise<CompanyMockResults> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(sessionId)}/complete`,
      { method: "POST" },
    );
  },

  getStatus(sessionId: string): Promise<CompanyMockStatus> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(sessionId)}/status`,
    );
  },

  getResults(sessionId: string): Promise<CompanyMockResults> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(sessionId)}/results`,
    );
  },
};
