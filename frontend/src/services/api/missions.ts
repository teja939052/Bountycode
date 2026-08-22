import { requestWithRetry } from "./request.ts";

export const missionApi = {
  interactionTypes() {
    return requestWithRetry("/api/v1/missions/interaction-types");
  },
  masteryDimensions() {
    return requestWithRetry("/api/v1/missions/mastery-dimensions");
  },
  skillRanks() {
    return requestWithRetry("/api/v1/missions/skill-ranks");
  },
  topics() {
    return requestWithRetry("/api/v1/missions/topics");
  },
  topicMastery(topic: string) {
    return requestWithRetry(`/api/v1/missions/mastery/${topic}`);
  },
  allMastery() {
    return requestWithRetry("/api/v1/missions/mastery");
  },
  stats() {
    return requestWithRetry("/api/v1/missions/stats");
  },
  submitInteraction(data: {
    topic: string;
    interaction_type: string;
    score: number;
    is_correct: boolean;
    time_taken?: number;
    answer?: string;
  }) {
    return requestWithRetry("/api/v1/missions/interact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  },
  requestHint(data: {
    topic: string;
    interaction_type: string;
    hint_level: number;
    context?: any;
  }) {
    return requestWithRetry("/api/v1/missions/hint", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  },
  topicRank(topic: string) {
    return requestWithRetry(`/api/v1/missions/rank/${topic}`);
  },
  domainProgress(domain: string) {
    return requestWithRetry(`/api/v1/missions/domain/${domain}`);
  },
  missionContent(topic: string) {
    return requestWithRetry(`/api/v1/missions/content/${topic}`);
  },
  allMissionContent() {
    return requestWithRetry("/api/v1/missions/content");
  },
};
