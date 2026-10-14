// @ts-nocheck
import { requestWithRetry as request } from "./request.ts";

export const trialApi = {
  startTrial(_opts: Record<string, unknown> = {}): Promise<{
    status: string;
    plan: string;
    trial_end: string;
    days: number;
  }> {
    return request("/api/v1/trial/start", { method: "POST" });
  },

  getTrialStatus(): Promise<Record<string, unknown>> {
    return request("/api/v1/trial/status");
  },

  verifyStudentDiscount(email: string): Promise<Record<string, unknown>> {
    return request("/api/v1/discount/verify-student", {
      method: "POST",
      body: JSON.stringify({ email }),
    });
  },
};
