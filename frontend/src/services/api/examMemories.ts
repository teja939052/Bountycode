import { requestWithRetry as request } from "./request.ts";

export interface ExamMemoryConfig {
  exams: { id: string; name: string }[];
  sections: string[];
  verify_threshold: number;
  daily_cap: number;
}

export interface ExamMemory {
  id: string;
  exam: string;
  exam_name: string;
  section: string;
  topic: string;
  question_text: string;
  format: "mcq" | "code" | "verbal";
  options: string[];
  known_answer: string;
  notes: string;
  status: "new" | "verified_crowd" | "approved" | "dismissed";
  report_count: number;
  created_at: string;
  updated_at: string;
  reporters?: string[];
  reviewed_by?: string;
  reviewed_at?: string;
}

export interface SubmitMemoryRequest {
  exam: string;
  section: string;
  topic?: string;
  question_text: string;
  format?: "mcq" | "code" | "verbal";
  options?: string[];
  known_answer?: string;
  notes?: string;
}

export interface ExamMemoryHeatmap {
  window_days: number;
  since: string;
  total_submissions: number;
  by_section: {
    exam: string;
    exam_name: string;
    section: string;
    submissions: number;
    reports: number;
    verified_crowd: number;
    approved: number;
  }[];
  by_exam: {
    exam: string;
    exam_name: string;
    submissions: number;
    reports: number;
    verified_crowd: number;
    approved: number;
  }[];
  hot_questions: {
    memory_id: string;
    exam: string;
    exam_name: string;
    section: string;
    topic: string;
    report_count: number;
    status: string;
    reviewed: boolean;
    question_text?: string;
  }[];
  verify_threshold: number;
}

export const examMemoriesApi = {
  async submit(req: SubmitMemoryRequest): Promise<ExamMemory & { duplicate: boolean; note: string }> {
    return request(`/api/v1/exam-memories`, {
      method: "POST",
      body: JSON.stringify(req),
    });
  },

  async mySubmissions(page = 1, limit = 20): Promise<{ memories: ExamMemory[]; total: number; page: number; pages: number }> {
    return request(`/api/v1/exam-memories/mine?page=${page}&limit=${limit}`);
  },

  async config(): Promise<ExamMemoryConfig> {
    return request(`/api/v1/exam-memories/config`);
  },

  async heatmap(days = 7): Promise<ExamMemoryHeatmap> {
    return request(`/api/v1/exam-memories/heatmap?days=${days}`);
  },

  async adminList(
    status?: string,
    exam?: string,
    page = 1,
    limit = 50
  ): Promise<{ memories: ExamMemory[]; total: number; page: number; pages: number; threshold: number }> {
    const params = new URLSearchParams({ page: String(page), limit: String(limit) });
    if (status) params.set("status", status);
    if (exam) params.set("exam", exam);
    return request(`/api/v1/exam-memories/admin/review?${params.toString()}`);
  },

  async promote(
    memoryId: string,
    body: { correct_index?: number; correct_answer?: string; reasoning?: string; type?: string; difficulty?: string; topic?: string }
  ): Promise<{ memory_id: string; status: string; promoted_question_id: string; added: number; note: string }> {
    return request(`/api/v1/exam-memories/admin/${encodeURIComponent(memoryId)}/promote`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  async dismiss(memoryId: string, reason: string): Promise<{ memory_id: string; status: string; reason: string }> {
    return request(`/api/v1/exam-memories/admin/${encodeURIComponent(memoryId)}/dismiss`, {
      method: "POST",
      body: JSON.stringify({ reason }),
    });
  },
};