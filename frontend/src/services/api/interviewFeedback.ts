import { requestWithRetry } from "./request.ts";

export const interviewFeedbackApi = {
  submit(interviewId, scores, comment) {
    return requestWithRetry("/api/v1/interview/feedback", {
      method: "POST",
      body: JSON.stringify({ interview_id: interviewId, scores, comment }),
    });
  },

  get(interviewId) {
    return requestWithRetry(`/api/v1/interview/feedback/${interviewId}`);
  },

  stats(userId) {
    return requestWithRetry(`/api/v1/interview/stats/${userId}`);
  },
};

export const bookingApi = {
  stats() {
    return requestWithRetry("/api/v1/interview-booking/stats");
  },
};
