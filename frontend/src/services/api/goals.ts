import { requestWithRetry as request } from "./request.ts";

export interface Goal {
  id: string;
  title: string;
  metric: string;
  target: number;
  progress: number;
  progress_pct: number;
  deadline: string | null;
  streak: number;
  completed: boolean;
  created_at: string;
}

export const goalsApi = {
  list() {
    return request("/api/v1/goals/") as Promise<{ goals: Goal[] }>;
  },

  create(title: string, target: number, metric: string, deadline: string | null = null) {
    return request("/api/v1/goals/create", {
      method: "POST",
      body: JSON.stringify({ title, target, metric, deadline }),
    }) as Promise<{ goal: Goal; created: boolean }>;
  },

  track(goalId: string, amount = 1) {
    return request(`/api/v1/goals/${goalId}/track`, {
      method: "POST",
      body: JSON.stringify({ amount }),
    }) as Promise<{
      goal_id: string;
      progress: number;
      target: number;
      completed: boolean;
      streak: number;
      bonus_xp: number;
    }>;
  },

  delete(goalId: string) {
    return request(`/api/v1/goals/${goalId}`, { method: "DELETE" }) as Promise<{ deleted: boolean }>;
  },
};
