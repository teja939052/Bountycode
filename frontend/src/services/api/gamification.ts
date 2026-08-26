import {
  requestWithRetry as request,
  type ApiRequestOptions,
} from "./request.ts";
import type {
  StreakRepairResult,
  GamificationProfile,
  TowerData,
  LeaderboardEntry,
  SkillNode,
  StartupState,
  StreakStatus,
  Badge,
  PowerUp,
  Challenge,
} from "./types.ts";

export type { StreakRepairResult };

export const gamificationApi = {
  getProfile(): Promise<GamificationProfile> {
    return request("/api/v1/gamification/profile");
  },

  recordActivity(
    activityType: string,
    score = 0,
    category: string | null = null,
    skill: string | null = null,
    metadata: Record<string, unknown> | null = null,
  ): Promise<{ xp_earned: number; leveled_up?: boolean; new_level?: number }> {
    const params = new URLSearchParams({
      activity_type: activityType,
      score: score.toString(),
    });
    if (category) params.append("category", category);
    if (skill) params.append("skill", skill);
    const opts: ApiRequestOptions = { method: "POST" };
    if (metadata) opts.body = JSON.stringify(metadata);
    return request(`/api/v1/gamification/record?${params.toString()}`, opts);
  },

  getLeaderboard(
    limit = 10,
  ): Promise<{ entries: LeaderboardEntry[]; user_rank?: number }> {
    return request(`/api/v1/gamification/leaderboard?limit=${limit}`);
  },

  getAllBadges(): Promise<Badge[]> {
    return request("/api/v1/gamification/badges");
  },

  getSkillGraph(): Promise<{ skills: SkillNode[]; categories?: string[] }> {
    return request("/api/v1/gamification/skills");
  },

  getWeakAreas(topN = 5): Promise<SkillNode[]> {
    return request(`/api/v1/gamification/skills/weak?top_n=${topN}`);
  },

  getReadinessScore(
    company: string | null = null,
  ): Promise<{ score: number; breakdown?: Record<string, number> }> {
    const params = company ? `?company=${company}` : "";
    return request(`/api/v1/gamification/skills/readiness${params}`);
  },

  getTower(): Promise<TowerData> {
    return request("/api/v1/gamification/tower");
  },

  getForest(): Promise<Record<string, unknown>> {
    return request("/api/v1/gamification/forest");
  },

  getBoss(bossLevel: number): Promise<Record<string, unknown>> {
    return request(`/api/v1/gamification/tower/boss/${bossLevel}`);
  },

  defeatBoss(
    bossLevel: number,
    score: number,
  ): Promise<{ defeated?: boolean; reward?: Record<string, unknown> }> {
    return request(
      `/api/v1/gamification/tower/boss/${bossLevel}/defeat?score=${score}`,
      {
        method: "POST",
      },
    );
  },

  usePowerUp(
    powerUpId: string,
  ): Promise<{ used?: boolean; effect?: Record<string, unknown> }> {
    return request(
      `/api/v1/gamification/tower/powerup/use?power_up_id=${powerUpId}`,
      {
        method: "POST",
      },
    );
  },

  buyPowerUp(
    powerUpId: string,
  ): Promise<{ purchased?: boolean; cost?: number }> {
    return request(
      `/api/v1/gamification/tower/powerup/buy?power_up_id=${powerUpId}`,
      {
        method: "POST",
      },
    );
  },

  getPowerUps(): Promise<PowerUp[]> {
    return request("/api/v1/gamification/tower/powerups");
  },

  getChallenges(): Promise<{ challenges: Challenge[] }> {
    return request("/api/v1/gamification/tower/challenges");
  },

  claimChallenge(
    challengeType: string,
    challengeId: string,
  ): Promise<{ claimed?: boolean; reward?: Record<string, unknown> }> {
    return request(
      `/api/v1/gamification/tower/challenges/claim?challenge_type=${challengeType}&challenge_id=${challengeId}`,
      { method: "POST" },
    );
  },

  getStreakFreezeStatus(): Promise<Record<string, unknown>> {
    return request("/api/v1/gamification/tower/streak-freeze");
  },

  autoApplyStreakFreeze(): Promise<{ applied?: boolean }> {
    return request("/api/v1/gamification/tower/streak-freeze/auto-apply", {
      method: "POST",
    });
  },

  getStartupState(): Promise<StartupState> {
    return request("/api/v1/gamification/startup");
  },

  getLeague(): Promise<Record<string, unknown>> {
    return request("/api/v1/gamification/league");
  },

  buyStreakFreeze(): Promise<{ purchased?: boolean; cost?: number }> {
    return request("/api/v1/gamification/tower/streak-freeze/buy", {
      method: "POST",
    });
  },

  getStreakRepairStatus(): Promise<StreakRepairResult> {
    return request("/api/v1/gamification/tower/streak-repair");
  },

  buyStreakRepair(): Promise<StreakRepairResult> {
    return request<StreakRepairResult>(
      "/api/v1/gamification/tower/streak-repair/buy",
      { method: "POST" },
    );
  },

  getDailyGoal(): Promise<Record<string, unknown>> {
    return request("/api/v1/gamification/tower/daily-goal");
  },

  claimDailyBonus(): Promise<{
    claimed?: boolean;
    reward?: Record<string, unknown>;
  }> {
    return request("/api/v1/gamification/daily-bonus", { method: "POST" });
  },

  getDailyBonusHistory(limit = 30): Promise<Record<string, unknown>> {
    return request(`/api/v1/gamification/daily-bonus/history?limit=${limit}`);
  },

  getNearbyLeaderboard(
    radius = 5,
    limit = 10,
  ): Promise<{ entries: LeaderboardEntry[] }> {
    const params = new URLSearchParams({
      radius: String(radius),
      limit: String(limit),
    });
    return request(
      `/api/v1/gamification/leaderboard/nearby?${params.toString()}`,
    );
  },

  getStreakStatus(): Promise<StreakStatus> {
    return request("/api/v1/gamification/streak/status");
  },
};
