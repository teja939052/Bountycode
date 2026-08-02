import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/chat";

function wsUrl(roomType, roomId) {
  const proto = window.location.protocol === "https:" ? "wss:" : "ws:";
  const host = window.location.host;
  const params = new URLSearchParams({ room_type: roomType });
  if (roomId) params.set("room_id", roomId);
  return `${proto}//${host}${BASE}/ws?${params.toString()}`;
}

export const chatApi = {
  wsUrl,

  send(payload) {
    return request(`${BASE}/send`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  messages(roomType, roomId, limit = 50, afterId = null) {
    const q = new URLSearchParams({
      room_type: roomType,
      limit: String(limit),
      ts: String(Date.now()),
    });
    if (roomId) q.set("room_id", roomId);
    if (afterId) q.set("after_id", afterId);
    return request(`${BASE}/messages?${q.toString()}`);
  },

  recent() {
    return request(`${BASE}/recent?ts=${Date.now()}`);
  },

  emotes() {
    return request(`${BASE}/emotes`);
  },

  search(roomType, roomId, query, limit = 20) {
    const q = new URLSearchParams({
      room_type: roomType,
      q: query,
      limit: String(limit),
      ts: String(Date.now()),
    });
    if (roomId) q.set("room_id", roomId);
    return request(`${BASE}/search?${q.toString()}`);
  },

  reactions(messageId, emoji) {
    return request(`${BASE}/messages/${messageId}/reactions`, {
      method: "POST",
      body: JSON.stringify({ emoji }),
    });
  },

  markRead(roomType, roomId) {
    return request(`${BASE}/mark-read`, {
      method: "POST",
      body: JSON.stringify({ room_type: roomType, room_id: roomId }),
    });
  },

  typing(roomType, roomId) {
    return request(`${BASE}/typing`, {
      method: "POST",
      body: JSON.stringify({ room_type: roomType, room_id: roomId }),
    });
  },

  unreadCount() {
    return request(`${BASE}/unread?ts=${Date.now()}`);
  },

  createRoom(roomType, roomId, name) {
    return request(`${BASE}/rooms`, {
      method: "POST",
      body: JSON.stringify({ room_type: roomType, room_id: roomId, name }),
    });
  },

  leaveRoom(roomType, roomId) {
    return request(`${BASE}/rooms/leave`, {
      method: "POST",
      body: JSON.stringify({ room_type: roomType, room_id: roomId }),
    });
  },

  roomMembers(roomType, roomId) {
    return request(`${BASE}/rooms/${roomType}/${roomId}/members`);
  },

  messageStats(roomType, roomId) {
    return request(`${BASE}/stats?room_type=${roomType}&room_id=${roomId || ""}`);
  },
};