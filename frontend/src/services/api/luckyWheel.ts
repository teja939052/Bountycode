import { requestWithRetry } from "./request.ts";

export const luckyWheelApi = {
  state() {
    return requestWithRetry("/api/v1/wheel/state");
  },

  spin() {
    return requestWithRetry("/api/v1/wheel/spin", { method: "POST" });
  },

  stats() {
    return requestWithRetry("/api/v1/wheel/stats");
  },
};
