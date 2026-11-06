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

  answerStep(slug: string, stepIndex: number, answerIndex: number) {
    return request<{ success: boolean; data: { correct: boolean; selected_index: number; correct_index: number; explanation: string } }>(
      `/api/v1/company-lessons/${encodeURIComponent(slug)}/steps/${stepIndex}/answer`,
      {
        method: "POST",
        body: JSON.stringify({ answer_index: answerIndex }),
      },
    );
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
