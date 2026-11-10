import { requestWithRetry as request } from "./request.ts";

/** Service-company OA mocks (TCS / Infosys / Wipro / Cognizant / Accenture). */
export const serviceOaApi = {
  listCompanies() {
    return request<{ data: Array<{ id: string; name: string; tracks: string[]; api_keys: string[] }> }>(
      "/api/v1/service-oa/companies",
    );
  },

  bankStats() {
    return request<{ data: { total: number; by_section: Record<string, number>; topics: string[] } }>(
      "/api/v1/service-oa/bank/stats",
    );
  },

  preview(company: string) {
    return request<{ data: { company_id: string; sample_quota_25: Record<string, number> } }>(
      `/api/v1/service-oa/mocks/preview?company=${encodeURIComponent(company)}`,
    );
  },

  startMock(body: {
    company: string;
    question_count?: number;
    seed?: number;
    sections?: string[];
  }) {
    return request<{ data: any }>("/api/v1/service-oa/mocks/start", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  gradeMock(body: {
    session_id: string;
    answers: Record<string, number>;
    time_spent_sec?: number;
  }) {
    return request<{ data: any }>("/api/v1/service-oa/mocks/grade", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },
};
