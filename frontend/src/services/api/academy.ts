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
};
