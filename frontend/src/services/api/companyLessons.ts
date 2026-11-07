import { requestWithRetry as request } from "./request.ts";

export const companyLessonsApi = {
  listLessons() {
    return request<{ success: boolean; data: any[] }>("/api/v1/company-lessons");
  },

  getLesson(slug: string) {
    return request<{ success: boolean; data: any }>(`/api/v1/company-lessons/${encodeURIComponent(slug)}`);
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
