import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/peer-review";

export const peerReviewApi = {
  submit(payload: { title: string; language: string; code: string; description?: string }) {
    return request(`${BASE}/submit`, { method: "POST", body: JSON.stringify(payload) });
  },
  my() {
    return request(`${BASE}/my`);
  },
  queue(limit?: number) {
    return request(`${BASE}/queue${limit ? `?limit=${limit}` : ""}`);
  },
  claim(itemId: string) {
    return request(`${BASE}/${encodeURIComponent(itemId)}/claim`, { method: "POST" });
  },
  review(itemId: string, payload: { comments: string; rating: number; strengths?: string; improvements?: string }) {
    return request(`${BASE}/${encodeURIComponent(itemId)}/review`, { method: "POST", body: JSON.stringify(payload) });
  },
  itemReviews(itemId: string) {
    return request(`${BASE}/${encodeURIComponent(itemId)}/reviews`);
  },
};
