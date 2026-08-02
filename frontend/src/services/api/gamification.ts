import { requestWithRetry as request } from "./request.ts";
export const gamificationApi = {
  getProfile() {
    return request("/api/v1/gamification/profile");
  },

  recordActivity(activityType, score = 0, category = null, skill = null) {
    const params = new URLSearchParams({ activity_type: activityType, score: score.toString() });
    if (category) params.append("category", category);
    if (skill) params.append("skill", skill);
    return request(`/api/v1/gamification/record?${params.toString()}`, {
      method: "POST",
    });
  },

  getLeaderboard(limit = 10) {
    return request(`/api/v1/gamification/leaderboard?limit=${limit}`);
  },

  getAllBadges() {
    return request("/api/v1/gamification/badges");
  },

  getSkillGraph() {
    return request("/api/v1/gamification/skills");
  },

  getWeakAreas(topN = 5) {
    return request(`/api/v1/gamification/skills/weak?top_n=${topN}`);
  },

  getReadinessScore(company = null) {
    const params = company ? `?company=${company}` : "";
    return request(`/api/v1/gamification/skills/readiness${params}`);
  },

  getTower() {
    return request("/api/v1/gamification/tower");
  },

  getBoss(bossLevel) {
    return request(`/api/v1/gamification/tower/boss/${bossLevel}`);
  },

  defeatBoss(bossLevel, score) {
    return request(`/api/v1/gamification/tower/boss/${bossLevel}/defeat?score=${score}`, {
      method: "POST",
    });
  },

  usePowerUp(powerUpId) {
    return request(`/api/v1/gamification/tower/powerup/use?power_up_id=${powerUpId}`, {
      method: "POST",
    });
  },

  buyPowerUp(powerUpId) {
    return request(`/api/v1/gamification/tower/powerup/buy?power_up_id=${powerUpId}`, {
      method: "POST",
    });
  },

  getPowerUps() {
    return request("/api/v1/gamification/tower/powerups");
  },

  getChallenges() {
    return request("/api/v1/gamification/tower/challenges");
  },

  claimChallenge(challengeType, challengeId) {
    return request(
      `/api/v1/gamification/tower/challenges/claim?challenge_type=${challengeType}&challenge_id=${challengeId}`,
      { method: "POST" }
    );
  },

  getStreakFreezeStatus() {
    return request("/api/v1/gamification/tower/streak-freeze");
  },

  buyStreakFreeze() {
    return request("/api/v1/gamification/tower/streak-freeze/buy", { method: "POST" });
  },

  getDailyGoal() {
    return request("/api/v1/gamification/tower/daily-goal");
  },

  getCardCollection(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, v);
    });
    return request(`/api/v1/cards/collection?${query.toString()}`);
  },

  getDailyDraw() {
    return request("/api/v1/cards/daily-draw");
  },

  fuseCards(cardIds) {
    return request("/api/v1/cards/fuse", cardIds);
  },

  toggleCardFavorite(cardId) {
    return request(`/api/v1/cards/favorite/${cardId}`, { method: "POST" });
  },

  getCardStats() {
    return request("/api/v1/cards/stats");
  },

  getMissingCards() {
    return request("/api/v1/cards/missing");
  },

  getWizardProfile() {
    return request("/api/v1/wizard/profile");
  },

  customizeWizard(updates) {
    return request("/api/v1/wizard/customize", {
      method: "PUT",
      body: JSON.stringify(updates),
    });
  },

  getWizardDialogue(situation) {
    return request(`/api/v1/wizard/dialogue/${situation}`);
  },

  getWizardLevels() {
    return request("/api/v1/wizard/levels");
  },
};