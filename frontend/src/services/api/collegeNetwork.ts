import { requestWithRetry } from "./request.ts";

export const collegeNetworkApi = {
  join(payload) {
    return requestWithRetry("/api/v1/college/join", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  profile() {
    return requestWithRetry("/api/v1/college/profile");
  },

  leaderboard(college) {
    const q = college ? `?college=${encodeURIComponent(college)}` : "";
    return requestWithRetry(`/api/v1/college/leaderboard${q}`);
  },

  feed(college, limit = 20) {
    const q = college ? `?college=${encodeURIComponent(college)}&limit=${limit}` : `?limit=${limit}`;
    return requestWithRetry(`/api/v1/college/feed${q}`);
  },

  sameBatch(branch?, year?) {
    const q = [];
    if (branch) q.push(`branch=${encodeURIComponent(branch)}`);
    if (year) q.push(`year=${encodeURIComponent(year)}`);
    return requestWithRetry(`/api/v1/college/same-batch?${q.join("&")}`);
  },

  cell() {
    return requestWithRetry("/api/v1/college/cell");
  },

  colleges() {
    return requestWithRetry("/api/v1/college/colleges");
  },

  startDuel(data) {
    return requestWithRetry("/api/v1/college/duel/start", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
};