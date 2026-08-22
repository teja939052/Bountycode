import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/study-squads";

export const studySquadsApi = {
  goals() {
    return request(`${BASE}/goals`);
  },
  profile(payload: { goals?: string[]; topics?: string[]; languages?: string[]; availability?: string; bio?: string }) {
    return request(`${BASE}/profile`, { method: "POST", body: JSON.stringify(payload) });
  },
  me() {
    return request(`${BASE}/me`);
  },
  match(limit?: number) {
    return request(`${BASE}/match${limit ? `?limit=${limit}` : ""}`);
  },
  invite(userId: string) {
    return request(`${BASE}/invite`, { method: "POST", body: JSON.stringify({ user_id: userId }) });
  },
  invites() {
    return request(`${BASE}/invites`);
  },
  acceptInvite(inviteId: string) {
    return request(`${BASE}/invites/${encodeURIComponent(inviteId)}/accept`, { method: "POST" });
  },
  declineInvite(inviteId: string) {
    return request(`${BASE}/invites/${encodeURIComponent(inviteId)}/decline`, { method: "POST" });
  },
  squads() {
    return request(`${BASE}/squads`);
  },
  postMessage(squadId: string, text: string) {
    return request(`${BASE}/${encodeURIComponent(squadId)}/message`, { method: "POST", body: JSON.stringify({ text }) });
  },
  messages(squadId: string) {
    return request(`${BASE}/${encodeURIComponent(squadId)}/messages`);
  },
};
