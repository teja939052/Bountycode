import { requestWithRetry as request } from "./request.ts";

export const guildsApi = {
  getPresets() {
    return request("/api/v1/guilds/presets");
  },

  create(data) {
    return request("/api/v1/guilds/create", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  // Alias for backward compatibility
  my() {
    return this.getMyGuild();
  },

  getMyGuild() {
    return request("/api/v1/guilds/my-guild");
  },

  join(data) {
    return request("/api/v1/guilds/join", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  leave() {
    return request("/api/v1/guilds/leave", { method: "POST" });
  },

  // Alias for backward compatibility
  leaderboard(limit = 20) {
    return this.getLeaderboard(limit);
  },

  getLeaderboard(limit = 20) {
    return request(`/api/v1/guilds/leaderboard?limit=${limit}`);
  },

  getMembers(guildId) {
    return request(`/api/v1/guilds/members/${guildId}`);
  },

  // Alias for backward compatibility
  contribute(amount, reason) {
    return this.contributeXP({ xp: amount, reason });
  },

  contributeXP(data) {
    return request("/api/v1/guilds/contribute-xp", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  getRank(guildId) {
    return request(`/api/v1/guilds/rank/${guildId}`);
  },

  // Guild war endpoints (may not exist in backend yet)
  activeWar() {
    return request("/api/v1/guilds/active-war");
  },

  challenge(guildId) {
    return request("/api/v1/guilds/challenge", {
      method: "POST",
      body: JSON.stringify({ guild_id: guildId }),
    });
  },

  warScore(warId, guildId, amount) {
    return request("/api/v1/guilds/war-score", {
      method: "POST",
      body: JSON.stringify({ war_id: warId, guild_id: guildId, amount }),
    });
  },

  resolveWar(warId) {
    return request("/api/v1/guilds/resolve-war", {
      method: "POST",
      body: JSON.stringify({ war_id: warId }),
    });
  },
};