import { requestWithRetry as request } from "./request.ts";

export const companyLessonsApi = {
  listLessons() {
    return request<{ success: boolean; data: any[] }>("/api/v1/company-lessons");
  },

  getLesson(slug: string) {
    return request<{ success: boolean; data: any }>(`/api/v1/company-lessons/${encodeURIComponent(slug)}`);
  },

  complete(slug: string, payload: { score: number; time_spent_seconds: number }) {
    return request<{ success: boolean; data: any }>(`/api/v1/company-lessons/${encodeURIComponent(slug)}/complete`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
