import { requestWithRetry as request } from "./request.ts";

export const companyLessonsApi = {
  listLessons() {
    return request<{ success: boolean; data: any[] }>("/api/v1/company-lessons");
  },

  getLesson(slug: string) {
    return request<{ success: boolean; data: any }>(`/api/v1/company-lessons/${encodeURIComponent(slug)}`);
  },

  getProgress(slug: string) {
    return request<{ success: boolean; data: { current_step: number; step_count: number; has_progress: boolean } }>(
      `/api/v1/company-lessons/${encodeURIComponent(slug)}/progress`,
    );
  },

  saveProgress(slug: string, currentStep: number) {
    return request<{ success: boolean; data: { current_step: number } }>(
      `/api/v1/company-lessons/${encodeURIComponent(slug)}/progress`,
      {
        method: "PUT",
        body: JSON.stringify({ current_step: currentStep }),
      },
    );
  },

  answerStep(slug: string, stepIndex: number, answer: number | string | number[]) {
    const payload = Array.isArray(answer)
      ? { answer_order: answer }
      : typeof answer === "number"
        ? { answer_index: answer }
        : { answer_text: answer };
    return request<{ success: boolean; data: { correct: boolean; selected_index: number | null; correct_index: number | null; correct_answer: string; correct_order?: number[]; explanation: string } }>(
      `/api/v1/company-lessons/${encodeURIComponent(slug)}/steps/${stepIndex}/answer`,
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );
  },

  /** Progressive server-side hint. Never awards mastery. */
  getHint(slug: string, stepIndex: number, hintsUsed = 0) {
    return request<{
      success: boolean;
      hint: string | null;
      hints_remaining?: number;
      exhausted?: boolean;
      awards_mastery?: boolean;
    }>(`/api/v1/sprint/lessons/${encodeURIComponent(slug)}/hint`, {
      method: "POST",
      body: JSON.stringify({ step_index: stepIndex, hints_used: hintsUsed }),
    });
  },

  complete(
    slug: string,
    payload: {
      answers: Record<string, number>;
      time_spent_seconds: number;
      track_id?: string;
      module_id?: string;
      topic_id?: string;
    },
  ) {
    return request<{ success: boolean; data: any }>(`/api/v1/company-lessons/${encodeURIComponent(slug)}/complete`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
