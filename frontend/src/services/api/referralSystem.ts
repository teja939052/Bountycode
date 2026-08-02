import { requestWithRetry } from "./request.ts";

export const referralSystemApi = {
  generateCode() {
    return requestWithRetry("/api/v1/referral/generate-code");
  },

  registerWithReferral(code) {
    return requestWithRetry("/api/v1/referral/register-with-referral", {
      method: "POST",
      body: JSON.stringify({ referral_code: code }),
    });
  },

  myReferrals() {
    return requestWithRetry("/api/v1/referral/my-referrals");
  },

  leaderboard(limit = 20) {
    return requestWithRetry(`/api/v1/referral/leaderboard?limit=${limit}`);
  },
};
