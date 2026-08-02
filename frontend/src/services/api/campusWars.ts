import { requestWithRetry } from "./request.ts";

export const campusWarsApi = {
  dailyQuests() {
    return requestWithRetry("/api/v1/campus/daily-quests");
  },

  weeklyChallenges() {
    return requestWithRetry("/api/v1/campus/weekly-challenges");
  },

  weeklyClaim(tier) {
    return requestWithRetry("/api/v1/campus/weekly-claim", {
      method: "POST",
      body: JSON.stringify({ tier }),
    });
  },

  // Alias for backward compatibility
  claimWeeklyReward(tier) {
    return this.weeklyClaim(tier);
  },

  claimDailyQuest(questId) {
    return requestWithRetry("/api/v1/campus/daily-quests", {
      method: "POST",
      body: JSON.stringify({ quest_id: questId }),
    });
  },

  streakBonus() {
    return requestWithRetry("/api/v1/campus/streak", { method: "POST" });
  },

  badges() {
    return requestWithRetry("/api/v1/campus/badges");
  },

  ranks() {
    return requestWithRetry("/api/v1/campus/ranks");
  },

  startDuel(college) {
    return requestWithRetry("/api/v1/campus/duel", {
      method: "POST",
      body: JSON.stringify({ college }),
    });
  },

  joinDuel(duelId) {
    return requestWithRetry(`/api/v1/campus/duel/${duelId}/join`, {
      method: "POST",
    });
  },

  collegeLeaderboard(college) {
    return requestWithRetry(`/api/v1/campus/leaderboard/${college}`);
  },
};