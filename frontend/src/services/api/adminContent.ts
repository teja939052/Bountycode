import { requestWithRetry } from "./request.ts";

export const adminContentApi = {
  list(params: Record<string, any> = {}) {
    const qs = new URLSearchParams();
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") qs.set(k, v);
    });
    const query = qs.toString();
    return requestWithRetry(`/api/v1/admin/content${query ? `?${query}` : ""}`);
  },

  get(contentId) {
    return requestWithRetry(`/api/v1/admin/content/${contentId}`);
  },

  create(payload) {
    return requestWithRetry("/api/v1/admin/content", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  update(contentId, payload) {
    return requestWithRetry(`/api/v1/admin/content/${contentId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  },

  remove(contentId) {
    return requestWithRetry(`/api/v1/admin/content/${contentId}`, { method: "DELETE" });
  },
};

export const assignmentsApi = {
  list() {
    return requestWithRetry("/api/v1/assignments");
  },

  listAdmin() {
    return requestWithRetry("/api/v1/assignments/admin");
  },

  create(payload) {
    return requestWithRetry("/api/v1/assignments", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  submit(assignmentId, answerText) {
    return requestWithRetry(`/api/v1/assignments/${assignmentId}/submit`, {
      method: "POST",
      body: JSON.stringify({ answer_text: answerText }),
    });
  },

  review(assignmentId, userId, score, feedback) {
    return requestWithRetry(`/api/v1/assignments/${assignmentId}/review`, {
      method: "POST",
      body: JSON.stringify({ user_id: userId, score, feedback }),
    });
  },

  submissions(assignmentId = null) {
    const qs = assignmentId ? `?assignment_id=${assignmentId}` : "";
    return requestWithRetry(`/api/v1/assignments/submissions${qs}`);
  },
};
