// @ts-nocheck
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

  getDiagnosticStatus() {
    return requestWithRetry("/api/v1/onboarding/diagnostic/status");
  },

  startDiagnostic(role) {
    return requestWithRetry(`/api/v1/onboarding/diagnostic/start?role=${role}`);
  },

  completeDiagnostic(data) {
    return requestWithRetry("/api/v1/onboarding/diagnostic/complete", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};