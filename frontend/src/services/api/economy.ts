import { requestWithRetry as request } from "./request.ts";

export const economyApi = {
  getBalance() {
    return request("/api/v1/economy/balance");
  },

  earn(data) {
    return request("/api/v1/economy/earn", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  dailyBonus() {
    return request("/api/v1/economy/daily-bonus", { method: "POST" });
  },

  getShop() {
    return request("/api/v1/economy/shop");
  },

  buy(data) {
    return request("/api/v1/economy/buy", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  sell(data) {
    return request("/api/v1/economy/sell", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getTransactions() {
    return request("/api/v1/economy/transactions");
  },
};