import { requestWithRetry } from "./request.ts";

export const freeTrialApi = {
  getLessons() {
    return requestWithRetry("/api/v1/free-trial/lessons");
  },

  complete() {
    return requestWithRetry("/api/v1/free-trial/complete", { method: "POST" });
  },

  getConversionPrompt() {
    return requestWithRetry("/api/v1/free-trial/conversion-prompt");
  },

  trackTrial(data) {
    return requestWithRetry("/api/v1/free-trial/track-trial", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};