import { requestWithRetry as request } from "./request.ts";

export type AcademyLearnerProfile = {
  target_role: string;
  target_companies: string[];
  experience_level: string;
  preferred_language: string;
  daily_minutes: number;
  placement_date: string | null;
  learning_preference: string;
  timezone: string;
};

export const academyApi = {
  getProfile() {
    return request<{ success: boolean; data: { profile: AcademyLearnerProfile | null; onboarding_complete: boolean } }>(
      "/api/v1/academy/profile",
    );
  },
  saveProfile(profile: AcademyLearnerProfile) {
    return request<{ success: boolean; data: { profile: AcademyLearnerProfile; onboarding_complete: boolean } }>(
      "/api/v1/academy/profile",
      { method: "PUT", body: JSON.stringify(profile) },
    );
  },
  getPlan() {
    return request<{ success: boolean; plan: any }>("/api/v1/academy/plan");
  },
  getLatestDiagnostic() {
    return request<{ success: boolean; result: any }>("/api/v1/academy/diagnostic/latest");
  },
  startDiagnostic(questionsPerDomain = 4) {
    return request<{ success: boolean; diagnostic: any }>("/api/v1/academy/diagnostic/start", {
      method: "POST",
      body: JSON.stringify({ questions_per_domain: questionsPerDomain }),
    });
  },
  answerDiagnostic(diagnosticId: string, questionId: string, answer: string) {
    return request(
      `/api/v1/academy/diagnostic/${encodeURIComponent(diagnosticId)}/answer`,
      { method: "POST", body: JSON.stringify({ question_id: questionId, answer }) },
    );
  },
  completeDiagnostic(diagnosticId: string) {
    return request(
      `/api/v1/academy/diagnostic/${encodeURIComponent(diagnosticId)}/complete`,
      { method: "POST" },
    );
  },
};
