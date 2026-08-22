import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/cgpa";

export const cgpaApi = {
  gradeScale() {
    return request(`${BASE}/grade-scale`);
  },
  calculate(payload: { semesters: Array<{ name: string; subjects: Array<{ name: string; credits: number; grade_point: number }> }>; max_scale?: number }) {
    return request(`${BASE}/calculate`, { method: "POST", body: JSON.stringify(payload) });
  },
  target(payload: { current_cgpa: number; credits_completed: number; target_cgpa: number; credits_remaining: number; max_scale?: number }) {
    return request(`${BASE}/target`, { method: "POST", body: JSON.stringify(payload) });
  },
  save(payload: { title: string; kind: string; result: unknown }) {
    return request(`${BASE}/save`, { method: "POST", body: JSON.stringify(payload) });
  },
  history() {
    return request(`${BASE}/history`);
  },
};
