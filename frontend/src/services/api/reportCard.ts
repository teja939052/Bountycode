import { requestWithRetry as request } from "./request.ts";

const BASE = "/api/v1/report-card";

export const reportCardApi = {
  get() {
    return request(`${BASE}`);
  },
  exportUrl(fmt: "docx" | "pdf" | "txt") {
    return `${BASE}/export/${fmt}`;
  },
};
