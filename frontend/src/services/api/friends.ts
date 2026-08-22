import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/friends";

export const friendsApi = {
  uid() {
    return request(`${BASE}/uid`);
  },

  overview() {
    return request(`${BASE}/overview`);
  },

  request(uid: string) {
    return request(`${BASE}/request`, { method: "POST", body: JSON.stringify({ uid }) });
  },

  lookup(uid: string) {
    return request(`${BASE}/lookup`, { method: "POST", body: JSON.stringify({ uid }) });
  },

  accept(requestId: string) {
    return request(`${BASE}/requests/${encodeURIComponent(requestId)}/accept`, { method: "POST" });
  },

  decline(requestId: string) {
    return request(`${BASE}/requests/${encodeURIComponent(requestId)}/decline`, { method: "POST" });
  },

  cancel(requestId: string) {
    return request(`${BASE}/requests/${encodeURIComponent(requestId)}/cancel`, { method: "POST" });
  },

  remove(friendId: string) {
    return request(`${BASE}/${encodeURIComponent(friendId)}`, { method: "DELETE" });
  },

  suggestions(q?: string, limit = 10) {
    const params: string[] = [];
    if (q && q.trim()) params.push(`q=${encodeURIComponent(q.trim())}`);
    params.push(`limit=${limit}`);
    return request(`${BASE}/suggestions?${params.join("&")}`);
  },
};