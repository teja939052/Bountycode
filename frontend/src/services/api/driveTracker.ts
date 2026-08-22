import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/drives/tracker";

export const driveApi = {
  stages() {
    return request(`${BASE}/stages`);
  },
  list() {
    return request(`${BASE}`);
  },
  create(payload: { company: string; role?: string; location?: string; package_lpa?: number | null; stage?: string; notes?: string }) {
    return request(`${BASE}`, { method: "POST", body: JSON.stringify(payload) });
  },
  update(id: string, payload: { stage?: string; status?: string; notes?: string; package_lpa?: number | null }) {
    return request(`${BASE}/${encodeURIComponent(id)}`, { method: "PUT", body: JSON.stringify(payload) });
  },
  remove(id: string) {
    return request(`${BASE}/${encodeURIComponent(id)}`, { method: "DELETE" });
  },
  stats() {
    return request(`${BASE}/stats`);
  },
};
