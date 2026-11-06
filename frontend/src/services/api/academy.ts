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
  getPlan() {\n    return request<{ success: boolean; plan: any }>("/api/v1/academy/plan");\n  },\n  getLatestDiagnostic() {\n    return request<{ success: boolean; result: any }>("/api/v1/academy/diagnostic/latest");\n  },\n  startDiagnostic(questionsPerDomain = 4) {\n    return request<{ success: boolean; diagnostic: any }>("/api/v1/academy/diagnostic/start", {\n      method: "POST", body: JSON.stringify({ questions_per_domain: questionsPerDomain }),\n    });\n  },\n  answerDiagnostic(diagnosticId: string, questionId: string, answer: string) {\n    return request(`/api/v1/academy/diagnostic/${encodeURIComponent(diagnosticId)}/answer`, {\n      method: "POST", body: JSON.stringify({ question_id: questionId, answer }),\n    });\n  },\n  completeDiagnostic(diagnosticId: string) {\n    return request(`/api/v1/academy/diagnostic/${encodeURIComponent(diagnosticId)}/complete`, { method: "POST" });\n  },\n  saveProfile(profile: AcademyLearnerProfile) {
    return request<{ success: boolean; data: { profile: AcademyLearnerProfile; onboarding_complete: boolean } }>(
      "/api/v1/academy/profile",
      { method: "PUT", body: JSON.stringify(profile) },
    );
  },
};
