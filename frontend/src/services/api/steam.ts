import { requestWithRetry } from "./request.ts";

export const steamApi = {
  get() {
    return requestWithRetry("/api/v1/profile/steam");
  },

  getPublic(userId) {
    return requestWithRetry(`/api/v1/profile/steam/${encodeURIComponent(userId)}`);
  },
};
