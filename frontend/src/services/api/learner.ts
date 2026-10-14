// @ts-nocheck
import { requestWithRetry } from "./request.ts";

export const learnerApi = {
  getState() {
    return requestWithRetry("/api/v1/learner/state", {
      skipAuthRefresh: false,
    });
  },

  getNextMission(params: {
    company?: string;
    role?: string;
    session_minutes?: number;
  } = {}) {
    const qs = new URLSearchParams();
    if (params.company) qs.set("company", params.company);
    if (params.role) qs.set("role", params.role);
    if (params.session_minutes) qs.set("session_minutes", String(params.session_minutes));
    const suffix = qs.toString() ? `?${qs.toString()}` : "";
    return requestWithRetry(`/api/v1/learner/next-mission${suffix}`, {
      skipAuthRefresh: false,
    });
  },
};
