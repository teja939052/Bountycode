import { requestWithRetry } from "./request.ts";

const BASE = "/api/v1/castle";

export const guildCastleApi = {
  get: (guildId) => requestWithRetry(`${BASE}/${guildId}`),
  defend: (guildId, zone) =>
    requestWithRetry(`${BASE}/${guildId}/defend`, {
      method: "POST",
      body: JSON.stringify({ zone }),
    }),
  attack: (guildId, zone) =>
    requestWithRetry(`${BASE}/${guildId}/attack`, {
      method: "POST",
      body: JSON.stringify({ zone }),
    }),
  upgrade: (guildId, upgradeId) =>
    requestWithRetry(`${BASE}/${guildId}/upgrade`, {
      method: "POST",
      body: JSON.stringify({ upgrade_id: upgradeId }),
    }),
  dailyBonus: (guildId) =>
    requestWithRetry(`${BASE}/${guildId}/daily-bonus`, {
      method: "POST",
    }),
  leaderboard: (guildId, limit = 20) =>
    requestWithRetry(`${BASE}/${guildId}/leaderboard?limit=${limit}`),
};