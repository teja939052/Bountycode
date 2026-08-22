import { requestWithRetry as request } from "./request.ts";
import type { InterviewResult } from "./types.ts";

export const interviewReplayApi = {
  getReplay(interviewId: string): Promise<InterviewResult> {
    return request(
      `/api/v1/interview/${encodeURIComponent(interviewId)}/replay`,
    );
  },

  getStats(interviewId: string): Promise<Record<string, unknown>> {
    return request(
      `/api/v1/interview/${encodeURIComponent(interviewId)}/replay/stats`,
    );
  },
};
