import { requestWithRetry as request, requestBlob } from "./request.ts";

export type OAMode = "calm" | "pressure" | "boss";

export interface StartOARequest {
  company: string;
  role?: string;
  total_questions?: number;
  duration_minutes?: number;
  mode?: OAMode;
  integrity?: boolean;
  verified_only?: boolean;
}

export interface SubmitOAItem {
  question_uid: string;
  answer: unknown;
  language?: string;
  time_taken?: number;
  test_cases?: unknown[];
}

export interface SubmitOABatch {
  session_id: string;
  items: SubmitOAItem[];
}

export interface OASession {
  session_id: string;
  company: string;
  mode: string;
  blueprint: Record<string, number>;
  marking_scheme?: unknown;
  stage_budgets?: unknown[];
  exam_structure?: unknown;
  duration_minutes: number;
  ends_at: string;
  integrity_enabled: boolean;
  total_questions: number;
  questions: Record<string, unknown>[];
  sections?: Record<string, unknown>[];
  negative_marking?: boolean;
  back_navigation?: boolean;
  section_switching?: boolean;
}

export interface OAResult {
  session_id: string;
  score: number;
  total_questions: number;
  correct_count: number;
  incorrect_count: number;
  unattempted_count: number;
  percentage: number;
  passed: boolean;
  time_taken: number;
  breakdown: Record<string, unknown>;
  skill_diagnostics: Record<string, unknown>;
  readiness_after: number;
  next_missions: unknown[];
}

export const oaApi = {
  async start(req: StartOARequest): Promise<OASession> {
    return request(`/api/v1/oa/${encodeURIComponent(req.company)}/start`, {
      method: "POST",
      body: JSON.stringify({
        role: req.role || "swe",
        total_questions: req.total_questions ?? 20,
        duration_minutes: req.duration_minutes ?? 90,
        mode: req.mode || "calm",
        integrity: req.integrity ?? false,
        verified_only: req.verified_only ?? true,
      }),
    });
  },

  async submitAnswer(sessionId: string, items: SubmitOAItem[]): Promise<unknown> {
    return request(`/api/v1/oa/answer`, {
      method: "POST",
      body: JSON.stringify({ session_id: sessionId, items }),
    });
  },

  async complete(sessionId: string): Promise<OAResult> {
    return request(`/api/v1/oa/${encodeURIComponent(sessionId)}/complete`, {
      method: "POST",
    });
  },

  async getResult(sessionId: string): Promise<OAResult> {
    return request(`/api/v1/oa/${encodeURIComponent(sessionId)}/result`);
  },

  async getHistory(): Promise<unknown[]> {
    return request(`/api/v1/oa/history`);
  },

  async getBlueprints(): Promise<unknown> {
    return request(`/api/v1/oa/blueprints`);
  },

  async recordIntegrity(
    sessionId: string,
    event: string,
    detail?: string,
  ): Promise<unknown> {
    return request(`/api/v1/oa/integrity`, {
      method: "POST",
      body: JSON.stringify({
        session_id: sessionId,
        event,
        detail: detail || "",
        at: Date.now() / 1000,
      }),
    });
  },

  async downloadReadinessReport(sessionId: string): Promise<Blob> {
    return requestBlob(`/api/v1/oa/${encodeURIComponent(sessionId)}/readiness-report`);
  },
};
