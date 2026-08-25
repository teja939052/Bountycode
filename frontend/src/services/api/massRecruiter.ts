import { requestWithRetry as request } from "./request.ts";

export interface ExamBlueprint {
  exam_id: string;
  name: string;
  description: string;
  total_questions: number;
  total_minutes: number;
  sections: { name: string; questions: number; minutes: number }[];
  negative_marks: number;
  cutoff_pct: number;
  locked?: boolean;
}

export interface ExamQuestion {
  id: string;
  question: string;
  options: string[];
  category: string;
  sub_category: string;
  difficulty: string;
  special?: "email" | "coding" | null;
}

export interface ExamSectionWindow {
  name: string;
  special?: string | null;
  part?: string;
  start_index: number;
  end_index: number;
  count: number;
  minutes: number;
}

export interface ExamStart {
  test_id: string;
  exam_id: string;
  exam_name: string;
  locked?: boolean;
  sections: ExamSectionWindow[];
  questions: ExamQuestion[];
  total_questions: number;
  total_minutes: number;
  negative_marks: number;
  ends_at: string;
}

export interface ExamResult {
  test_id: string;
  exam_name: string;
  score: number;
  net_score: number;
  passed_cutoff: boolean;
  cutoff_pct: number;
  correct_answers: number;
  wrong_answers: number;
  skipped_answers: number;
  negative_marks: number;
  total_questions: number;
  xp_earned: number;
  section_stats: Record<string, { correct: number; wrong: number; skipped: number; total: number }>;
  subjective?: Record<string, { avg_score: number; items: { label: string; score: number; feedback: string }[] }>;
  weak_areas: { category: string; accuracy: number; solved: number; total: number }[];
  message: string;
}

export const massRecruiterApi = {
  listExams(): Promise<{ exams: ExamBlueprint[] }> {
    return request("/api/v1/mass-recruiter/exams");
  },

  start(examId: string): Promise<ExamStart> {
    return request("/api/v1/mass-recruiter/start", {
      method: "POST",
      body: JSON.stringify({ exam_id: examId }),
    });
  },

  saveAnswer(
    testId: string,
    questionIndex: number,
    answer: string | null,
    marked = false,
  ): Promise<{ recorded: boolean }> {
    const params = new URLSearchParams({
      question_index: String(questionIndex),
      marked: String(marked),
    });
    if (answer !== null) params.set("answer", answer);
    return request(`/api/v1/mass-recruiter/${testId}/answer?${params.toString()}`, {
      method: "POST",
    });
  },

  complete(testId: string): Promise<ExamResult> {
    return request(`/api/v1/mass-recruiter/${testId}/complete`, { method: "POST" });
  },

  history(): Promise<{ exams: Record<string, unknown>[]; total: number }> {
    return request("/api/v1/mass-recruiter/history");
  },
};
