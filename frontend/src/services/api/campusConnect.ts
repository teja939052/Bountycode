import { requestWithRetry } from "./request.ts";

export const campusConnectApi = {
  generateInvite(college) {
    return requestWithRetry("/api/v1/connect/invite", {
      method: "POST",
      body: JSON.stringify({ college }),
    });
  },

  joinInvite(token) {
    return requestWithRetry(`/api/v1/connect/${token}`);
  },

  startReferralDuel(college) {
    return requestWithRetry("/api/v1/connect/referral-duel", {
      method: "POST",
      body: JSON.stringify({ college }),
    });
  },

  // Alias for backward compatibility
  startDuel(college) {
    return this.startReferralDuel(college);
  },

  joinDuel(duelId) {
    return requestWithRetry(`/api/v1/connect/referral-duel/${duelId}`, {
      method: "POST",
    });
  },

  submitDuelSolution(duelId, problemId, code, language) {
    return requestWithRetry(`/api/v1/connect/referral-duel/${duelId}/solve`, {
      method: "POST",
      body: JSON.stringify({ problem_id: problemId, code, language }),
    });
  },

  getDuelResult(duelId) {
    return requestWithRetry(`/api/v1/connect/referral-duel/${duelId}/result`);
  },

  getTournaments() {
    return requestWithRetry("/api/v1/connect/tournaments");
  },

  getCollegeLeaderboard(college) {
    return requestWithRetry(`/api/v1/connect/leaderboard/${college || ""}`);
  },

  colleges() {
    return requestWithRetry("/api/v1/connect/colleges");
  },
};