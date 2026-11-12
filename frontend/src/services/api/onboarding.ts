import { requestWithRetry } from "./request.ts";

export const onboardingApi = {
  getQuest() {
    return requestWithRetry("/api/v1/onboarding/quest");
  },

  completeStep(data) {
    return requestWithRetry("/api/v1/onboarding/complete", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getStatus() {
    return requestWithRetry("/api/v1/onboarding/status");
  },

  getPreferences() {
    return requestWithRetry("/api/v1/onboarding/preferences");
  },

  savePreferences(data: { career_goals: string[]; tech_interests: string[] }) {
    return requestWithRetry("/api/v1/onboarding/preferences", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  restart() {
    return requestWithRetry("/api/v1/onboarding/restart", {
      method: "POST",
    });
  },
};
