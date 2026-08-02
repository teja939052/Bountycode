import { requestWithRetry } from "./request.ts";

export const careerApi = {
  get() {
    return requestWithRetry("/api/v1/career");
  },

  refresh() {
    return requestWithRetry("/api/v1/career/refresh", { method: "POST" });
  },

  hall() {
    return requestWithRetry("/api/v1/career/hall");
  },
};
