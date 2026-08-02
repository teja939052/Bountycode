import { requestWithRetry } from "./request.ts";

export const timelineApi = {
  get() {
    return requestWithRetry("/api/v1/timeline");
  },

  activity(days = 180) {
    return requestWithRetry(`/api/v1/timeline/activity?days=${days}`);
  },

  getPublic(userId) {
    return requestWithRetry(`/api/v1/timeline/${userId}`);
  },
};
