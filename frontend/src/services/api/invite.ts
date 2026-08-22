import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/invite";

export const inviteApi = {
  generate(kind: "friend" | "study_squad" | "campus_connect", targetUserId?: string, college?: string) {
    return request(`${BASE}/generate`, {
      method: "POST",
      body: JSON.stringify({ kind, target_user_id: targetUserId, college }),
    });
  },

  inbox() {
    return request(`${BASE}/inbox`);
  },

  outbox() {
    return request(`${BASE}/outbox`);
  },

  accept(inviteId: string) {
    return request(`${BASE}/${encodeURIComponent(inviteId)}/accept`, { method: "POST" });
  },

  decline(inviteId: string) {
    return request(`${BASE}/${encodeURIComponent(inviteId)}/decline`, { method: "POST" });
  },
};