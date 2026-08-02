import { requestWithRetry } from "./request.ts";

export const journeyApi = {
  get() {
    return requestWithRetry("/api/v1/journey");
  },

  move(regionId) {
    return requestWithRetry("/api/v1/journey/move", {
      method: "POST",
      body: JSON.stringify({ region_id: regionId }),
    });
  },

  completeQuest(regionId, questIndex) {
    return requestWithRetry("/api/v1/journey/quest/complete", {
      method: "POST",
      body: JSON.stringify({ region_id: regionId, quest_index: questIndex }),
    });
  },
};
