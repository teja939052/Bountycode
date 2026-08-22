import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/gd";

function wsUrl(roomId: string) {
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${proto}//${window.location.host}${BASE}/rooms/${encodeURIComponent(roomId)}/ws`;
}

export const gdApi = {
  wsUrl,

  topics() {
    return request(`${BASE}/topics`);
  },

  createRoom(payload: { topic?: string; duration_minutes?: number; max_participants?: number }) {
    return request(`${BASE}/rooms`, {
      method: "POST",
      body: JSON.stringify(payload || {}),
    });
  },

  listRooms(status?: string) {
    const q = status ? `?status=${encodeURIComponent(status)}` : "";
    return request(`${BASE}/rooms${q}`);
  },

  getRoom(roomId: string) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}`);
  },

  joinByCode(joinCode: string) {
    return request(`${BASE}/rooms/join-by-code?join_code=${encodeURIComponent(joinCode.toUpperCase())}`, { method: "POST" });
  },

  join(roomId: string) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}/join`, { method: "POST" });
  },

  leave(roomId: string) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}/leave`, { method: "POST" });
  },

  start(roomId: string) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}/start`, { method: "POST" });
  },

  end(roomId: string) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}/end`, { method: "POST" });
  },

  setTimer(roomId: string, seconds: number) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}/timer?seconds=${seconds}`, { method: "POST" });
  },

  rate(roomId: string, payload: { target_user_id: string; clarity: number; listening: number; initiative: number; comment?: string }) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}/rate`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  myFeedback(roomId: string) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}/feedback`);
  },

  roomScores(roomId: string) {
    return request(`${BASE}/rooms/${encodeURIComponent(roomId)}/scores`);
  },
};
