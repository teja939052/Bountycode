import { requestWithRetry as request } from "./request.ts";

export const companyMocksApi = {
  getCompanies(): Promise<{ companies: string[] }> {
    return request("/api/v1/company-mocks/companies");
  },

  getConfig(companyId: string): Promise<Record<string, unknown>> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(companyId)}/config`,
    );
  },

  start(
    companyId: string,
    roundName: string | null = null,
  ): Promise<{ session_id: string; questions?: unknown[] }> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(companyId)}/start`,
      {
        method: "POST",
        body: JSON.stringify({ round_name: roundName }),
      },
    );
  },

  getStatus(
    sessionId: string,
  ): Promise<{ status: string; completed?: boolean; current_round?: string }> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(sessionId)}/status`,
    );
  },

  getResults(sessionId: string): Promise<Record<string, unknown>> {
    return request(
      `/api/v1/company-mocks/${encodeURIComponent(sessionId)}/results`,
    );
  },
};
