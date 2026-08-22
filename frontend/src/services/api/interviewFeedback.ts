import { requestWithRetry as request } from "./request.ts";

export const interviewFeedbackApi = {
  submit(
    interviewId: string,
    scores: Record<string, number>,
    comment: string,
  ): Promise<{ submitted?: boolean; feedback?: string }> {
    return request("/api/v1/interview/feedback", {
      method: "POST",
      body: JSON.stringify({ interview_id: interviewId, scores, comment }),
    });
  },

  get(interviewId: string): Promise<Record<string, unknown>> {
    return request(
      `/api/v1/interview/feedback/${encodeURIComponent(interviewId)}`,
    );
  },

  stats(userId: string): Promise<Record<string, unknown>> {
    return request(`/api/v1/interview/stats/${encodeURIComponent(userId)}`);
  },
};

export const bookingApi = {
  stats(): Promise<Record<string, unknown>> {
    return request("/api/v1/interview-booking/stats");
  },
};
