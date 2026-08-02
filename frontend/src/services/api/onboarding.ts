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
};