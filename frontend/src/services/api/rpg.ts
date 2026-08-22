import { requestWithRetry } from "./request.ts";

export const rpgApi = {
  profile() {
    return requestWithRetry("/api/v1/rpg/profile");
  },
  ranks() {
    return requestWithRetry("/api/v1/rpg/ranks");
  },
  rank(level: number) {
    return requestWithRetry(`/api/v1/rpg/rank/${level}`);
  },
  skillTree() {
    return requestWithRetry("/api/v1/rpg/skill-tree");
  },
  quests() {
    return requestWithRetry("/api/v1/rpg/quests");
  },
  completeQuestStep(questId: string, stepId: string) {
    return requestWithRetry("/api/v1/rpg/quests/complete-step", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quest_id: questId, step_id: stepId }),
    });
  },
  bosses() {
    return requestWithRetry("/api/v1/rpg/bosses");
  },
  bossDetail(bossId: string) {
    return requestWithRetry(`/api/v1/rpg/boss/${bossId}`);
  },
  challengeBoss(bossId: string, score: number) {
    return requestWithRetry("/api/v1/rpg/boss/challenge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ boss_id: bossId, score }),
    });
  },
  dungeons() {
    return requestWithRetry("/api/v1/rpg/dungeons");
  },
  dungeonDetail(dungeonId: string) {
    return requestWithRetry(`/api/v1/rpg/dungeon/${dungeonId}`);
  },
  completeDungeonGate(dungeonId: string, gateId: string, score: number) {
    return requestWithRetry("/api/v1/rpg/dungeon/gate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dungeon_id: dungeonId, gate_id: gateId, score }),
    });
  },
  collections() {
    return requestWithRetry("/api/v1/rpg/collections");
  },
};
