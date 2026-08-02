import { requestWithRetry } from "./request.ts";

export const metricsApi = {
  track(feature, event, value) {
    return requestWithRetry("/api/v1/metrics/event", {
      method: "POST",
      body: JSON.stringify({ feature, event, value }),
    }).catch(() => null);
  },

  retention() {
    return requestWithRetry("/api/v1/metrics/retention");
  },

  features() {
    return requestWithRetry("/api/v1/metrics/features");
  },
};
