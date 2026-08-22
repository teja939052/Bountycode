import { requestWithRetry as request } from "./request.ts";
import type { CompanyProfile } from "./types.ts";

export const companyPrepApi = {
  getCompanies(): Promise<{ companies: string[] }> {
    return request("/api/v1/company/companies");
  },

  getBehavioralQuestion(
    company: string,
    role: string,
  ): Promise<{ question: string; category?: string; follow_ups?: string[] }> {
    return request("/api/v1/company/behavioral", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    });
  },

  getInterviewTips(
    company: string,
    role: string,
    roundType: string,
  ): Promise<{
    tips: string[];
    faqs?: Array<{ question: string; answer: string }>;
  }> {
    return request("/api/v1/company/tips", {
      method: "POST",
      body: JSON.stringify({ company, role, round_type: roundType }),
    });
  },

  getGuide(company: string): Promise<CompanyProfile> {
    return request(`/api/v1/company/${encodeURIComponent(company)}/guide`);
  },
};

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
