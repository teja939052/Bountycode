import { requestWithRetry } from "./request.ts";

export const campusApi = {
  setCollege(college) {
    return requestWithRetry("/api/v1/campus/profile", {
      method: "POST",
      body: JSON.stringify({ college }),
    });
  },

  getProfile() {
    return requestWithRetry("/api/v1/campus/profile");
  },

  addPoints(amount, reason = "activity") {
    return requestWithRetry("/api/v1/campus/points", {
      method: "POST",
      body: JSON.stringify({ amount, reason }),
    });
  },

  leaderboard() {
    return requestWithRetry("/api/v1/campus/leaderboard");
  },

  global() {
    return requestWithRetry("/api/v1/campus/global");
  },

  winners() {
    return requestWithRetry("/api/v1/campus/winners");
  },

  finalize() {
    return requestWithRetry("/api/v1/campus/finalize", {
      method: "POST",
    });
  },
};
