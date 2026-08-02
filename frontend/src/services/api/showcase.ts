import { requestWithRetry } from "./request.ts";

export const showcaseApi = {
  browse(params: Record<string, any> = {}) {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v) query.set(k, v);
    });
    return requestWithRetry(`/api/v1/showcase?${query.toString()}`);
  },

  getById(projectId) {
    return requestWithRetry(`/api/v1/showcase/${projectId}`);
  },

  publish(payload) {
    return requestWithRetry("/api/v1/showcase", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  like(projectId) {
    return requestWithRetry(`/api/v1/showcase/${projectId}/like`, {
      method: "POST",
    });
  },

  addReview(projectId, comment, rating) {
    return requestWithRetry(`/api/v1/showcase/${projectId}/reviews`, {
      method: "POST",
      body: JSON.stringify({ comment, rating }),
    });
  },

  remove(projectId) {
    return requestWithRetry(`/api/v1/showcase/${projectId}`, {
      method: "DELETE",
    });
  },

  getTags() {
    return requestWithRetry("/api/v1/showcase/tags");
  },
};
