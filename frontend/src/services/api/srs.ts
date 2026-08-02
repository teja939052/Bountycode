import { requestWithRetry as request } from "./request.ts";

export const srsApi = {
  initialize(body = {}) {
    return request("/api/v1/srs/initialize", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  review(conceptId, grade) {
    return request("/api/v1/srs/review", {
      method: "POST",
      body: JSON.stringify({ concept_id: conceptId, grade }),
    });
  },

  bulkReview(reviews) {
    return request("/api/v1/srs/review/bulk", {
      method: "POST",
      body: JSON.stringify({ reviews }),
    });
  },

  getDue(limit = 20) {
    return request(`/api/v1/srs/due?limit=${limit}`);
  },

  getStats() {
    return request("/api/v1/srs/stats");
  },

  getConcepts() {
    return request("/api/v1/srs/concepts");
  },

  getForecast(days = 30) {
    return request(`/api/v1/srs/forecast?days=${days}`);
  },
};