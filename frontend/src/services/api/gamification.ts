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
  ): Promise<{
    xp_earned: number;
    leveled_up?: boolean;
    new_level?: number;
    coins_earned?: number;
    stars_earned?: number;
    new_streak?: number;
    new_badges?: unknown[];
    combo?: { current: number; max: number; multiplier: number };
    critical_hit?: boolean;
    critical_bonus?: number;
    streak_multiplier?: number;
    streak_frozen?: boolean;
    streak_freezes_remaining?: number;
    daily_goal_count?: number;
    daily_goal_target?: number;
    milestone?: Record<string, unknown>;
    boss_level?: number | null;
    base_xp?: number;
    multipliers?: {
      streak: number;
      combo: number;
      first_of_day: boolean;
      critical: number;
      double_xp: boolean;
    };
  }> {
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
    timeframe: "all" | "weekly" | "monthly" = "all",
    levelMin?: number,
    levelMax?: number,
  ): Promise<LeaderboardEntry[]> {
    const params = new URLSearchParams({ limit: String(limit), timeframe });
    if (levelMin != null) params.append("level_min", String(levelMin));
    if (levelMax != null) params.append("level_max", String(levelMax));
    return request(`/api/v1/gamification/leaderboard?${params.toString()}`);
  },

  getMyRank(
    timeframe: "all" | "weekly" | "monthly" = "weekly",
  ): Promise<{
    timeframe: string; rank: number; of: number; period_xp: number;
    next_up: { xp_gap: number; target_xp: number } | null;
  }> {
    return request(`/api/v1/gamification/leaderboard/me?timeframe=${timeframe}`);
  },

  getLeagueLeaderboard(timeframe: "all" | "weekly" | "monthly" = "weekly"): Promise<{
    entries: LeaderboardEntry[];
    user_index?: number | null;
    user_rank?: number | null;
    band_start: number;
    band_end: number;
    timeframe: string;
    total: number;
  }> {
    const params = new URLSearchParams({ timeframe });
    return request(`/api/v1/gamification/leaderboard/league?${params.toString()}`);
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

  getComboStatus(): Promise<Record<string, unknown>> {
    return request("/api/v1/gamification/combo");
  },

  getDailyLoginCalendar(days = 7): Promise<Record<string, unknown>> {
    return request(`/api/v1/gamification/daily-login?days=${days}`);
  },

  claimDailyLogin(): Promise<Record<string, unknown>> {
    return request("/api/v1/gamification/daily-login/claim", { method: "POST" });
  },

  getAchievementChains(): Promise<Record<string, unknown>> {
    return request("/api/v1/gamification/achievement-chains");
  },

  setTargetCompany(company: string): Promise<{ success: boolean; target_company: string }> {
    return request("/api/v1/gamification/profile/target-company", {
      method: "POST",
      body: JSON.stringify({ company }),
    });
  },

  getTitleProgression(): Promise<Record<string, unknown>> {
    return request("/api/v1/gamification/profile/title-progression");
  },

  getReadinessScore(company?: string): Promise<{
    overall_readiness: number;
    domain_scores: Record<string, number>;
    per_company_scores: Record<string, unknown>;
    target_company?: string;
    blockers: string[];
    next_focus: string;
    readiness_level: string;
  }> {
    const params = company ? `?company=${encodeURIComponent(company)}` : "";
    return request(`/api/v1/gamification/readiness${params}`);
  },
};
