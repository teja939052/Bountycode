import { requestWithRetry } from "./request.ts";

export const campusWarsApi = {
  dailyQuests() {
    return requestWithRetry("/api/v1/campus-wars/daily-quests");
  },

  weeklyChallenges() {
    return requestWithRetry("/api/v1/campus-wars/weekly-challenges");
  },

  weeklyClaim(tier) {
    return requestWithRetry("/api/v1/campus-wars/weekly-claim", {
      method: "POST",
      body: JSON.stringify({ tier }),
    });
  },

  // Alias for backward compatibility
  claimWeeklyReward(tier) {
    return this.weeklyClaim(tier);
  },

  claimDailyQuest(questId) {
    return requestWithRetry("/api/v1/campus-wars/daily-quests", {
      method: "POST",
      body: JSON.stringify({ quest_id: questId }),
    });
  },

  streakBonus() {
    return requestWithRetry("/api/v1/campus-wars/streak", { method: "POST" });
  },

  badges() {
    return requestWithRetry("/api/v1/campus-wars/badges");
  },

  ranks() {
    return requestWithRetry("/api/v1/campus-wars/ranks");
  },

  startDuel(college) {
    return requestWithRetry("/api/v1/campus-wars/duel", {
      method: "POST",
      body: JSON.stringify({ college }),
    });
  },

  joinDuel(duelId) {
    return requestWithRetry(`/api/v1/campus-wars/duel/${duelId}/join`, {
      method: "POST",
    });
  },

  collegeLeaderboard(college) {
    return requestWithRetry(`/api/v1/campus-wars/leaderboard/${college}`);
  },
};