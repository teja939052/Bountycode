import { requestWithRetry } from "./request.ts";

export const merchantApi = {
  getShop() {
    return requestWithRetry("/api/v1/merchant");
  },

  buyItem(itemId) {
    return requestWithRetry("/api/v1/merchant/buy", {
      method: "POST",
      body: JSON.stringify({ item_id: itemId }),
    });
  },

  getPrestige() {
    return requestWithRetry("/api/v1/prestige");
  },

  prestige() {
    return requestWithRetry("/api/v1/prestige/reset", {
      method: "POST",
    });
  },
};
