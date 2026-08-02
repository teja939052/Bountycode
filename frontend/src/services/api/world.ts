import { requestWithRetry } from "./request.ts";

export const worldApi = {
  getMap() {
    return requestWithRetry("/api/v1/world/map");
  },

  advance() {
    return requestWithRetry("/api/v1/world/advance", {
      method: "POST",
    });
  },

  getTree() {
    return requestWithRetry("/api/v1/world/skill/tree");
  },

  unlockNode(nodeId) {
    return requestWithRetry("/api/v1/world/skill/unlock", {
      method: "POST",
      body: JSON.stringify({ node_id: nodeId }),
    });
  },
};
