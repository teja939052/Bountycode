import { requestWithRetry as request } from "./request.ts";

export const sprintApi = {
  /** Ordered daily focus from the service-company sprint engine. */
  getToday() {
    return request<{ success: boolean; data: any; skills_summary?: any }>("/api/v1/sprint/today");
  },

  getCurriculum() {
    return request<{ success: boolean; curriculum: any; ordered_lessons: string[] }>(
      "/api/v1/sprint/curriculum",
    );
  },

  /** Progressive hint for a lesson step. Never awards mastery. */
  getHint(slug: string, stepIndex: number, hintsUsed = 0) {
    return request<{
      success: boolean;
      hint: string | null;
      hint_index?: number;
      hints_remaining?: number;
      exhausted?: boolean;
      awards_mastery?: boolean;
      policy?: string;
    }>(`/api/v1/sprint/lessons/${encodeURIComponent(slug)}/hint`, {
      method: "POST",
      body: JSON.stringify({ step_index: stepIndex, hints_used: hintsUsed }),
    });
  },
};

export default sprintApi;
