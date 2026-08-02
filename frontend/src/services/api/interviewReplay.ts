import { requestWithRetry } from "./request.ts";

export const interviewReplayApi = {
  getReplay(interviewId) {
    return requestWithRetry(`/api/v1/interview/${interviewId}/replay`);
  },

  getStats(interviewId) {
    return requestWithRetry(`/api/v1/interview/${interviewId}/replay/stats`);
  },
};
