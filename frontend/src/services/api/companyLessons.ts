import { requestWithRetry as request } from "./request.ts";

export const companyLessonsApi = {
  listLessons() {
    return request<{ success: boolean; data: any[] }>("/api/v1/company-lessons");
  },

  getLesson(slug: string) {
    return request<{ success: boolean; data: any }>(`/api/v1/company-lessons/${encodeURIComponent(slug)}`);
  },

  complete(
    slug: string,
    payload: {
      answers: Record<string, number>;
      time_spent_seconds: number;
      track_id?: string;
      module_id?: string;
    },
  ) {
    return request<{ success: boolean; data: any }>(`/api/v1/company-lessons/${encodeURIComponent(slug)}/complete`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
