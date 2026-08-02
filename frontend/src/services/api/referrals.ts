import { requestWithRetry as request } from "./request.ts";

export const referralApi = {
  getStatus() {
    return request("/api/v1/referrals/status");
  },

  refer(data) {
    return request("/api/v1/referrals/refer", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  claimBonus() {
    return request("/api/v1/referrals/claim-bonus", { method: "POST" });
  },
};