import { requestWithRetry } from "./request.ts";

export const battlePassApi = {
  track() {
    return requestWithRetry("/api/v1/pass/track");
  },

  claim(tier = null) {
    const body = tier !== null ? JSON.stringify({ tier }) : undefined;
    return requestWithRetry("/api/v1/pass/claim", {
      method: "POST",
      body,
    });
  },

  shop() {
    return requestWithRetry("/api/v1/pass/shop");
  },

  purchase(itemId) {
    return requestWithRetry("/api/v1/pass/purchase", {
      method: "POST",
      body: JSON.stringify({ item_id: itemId }),
    });
  },

  dailyLogin() {
    return requestWithRetry("/api/v1/pass/daily-login", { method: "POST" });
  },

  activatePremium() {
    return requestWithRetry("/api/v1/pass/premium", { method: "POST" });
  },

  leaderboard() {
    return requestWithRetry("/api/v1/pass/leaderboard");
  },
};
