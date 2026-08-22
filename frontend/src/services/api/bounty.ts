import { requestWithRetry } from "./request.ts";

export const bountyApi = {
  myCard() {
    return requestWithRetry("/api/v1/bounty/card");
  },
  userCard(userId: string) {
    return requestWithRetry(`/api/v1/bounty/card/${userId}`);
  },
  leaderboard(limit: number = 20) {
    return requestWithRetry(`/api/v1/bounty/leaderboard?limit=${limit}`);
  },
  tiers() {
    return requestWithRetry("/api/v1/bounty/tiers");
  },
};
