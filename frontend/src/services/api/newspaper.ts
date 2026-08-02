import { requestWithRetry } from "./request.ts";

export const newspaperApi = {
  today() {
    return requestWithRetry("/api/v1/newspaper/today");
  },

  daily() {
    return requestWithRetry("/api/v1/newspaper/daily");
  },
};
