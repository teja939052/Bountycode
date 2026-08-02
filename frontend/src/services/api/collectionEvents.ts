import { requestWithRetry } from "./request.ts";

export const collectionApi = {
  get() {
    return requestWithRetry("/api/v1/collection");
  },

  earn(companyId) {
    return requestWithRetry("/api/v1/collection/earn", {
      method: "POST",
      body: JSON.stringify({ company_id: companyId }),
    });
  },

  complete() {
    return requestWithRetry("/api/v1/collection/complete");
  },
};

export const eventsApi = {
  random() {
    return requestWithRetry("/api/v1/events/random");
  },

  research() {
    return requestWithRetry("/api/v1/events/research");
  },

  contribute(amount) {
    return requestWithRetry("/api/v1/events/research/contribute", {
      method: "POST",
      body: JSON.stringify({ amount }),
    });
  },

  festival() {
    return requestWithRetry("/api/v1/events/festival");
  },

  lucky(attempts) {
    return requestWithRetry("/api/v1/events/lucky", {
      method: "POST",
      body: JSON.stringify({ attempts }),
    });
  },
};
