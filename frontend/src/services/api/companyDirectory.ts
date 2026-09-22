import { requestWithRetry as request } from "./request.ts";

export const companyDirectoryApi = {
  getCompanies(params: { q?: string; type?: string; tier?: string; month?: string } = {}): Promise<{
    companies: any[];
    total?: number;
  }> {
    const qp = new URLSearchParams();
    if (params.q) qp.set("q", params.q);
    if (params.type) qp.set("type", params.type);
    if (params.tier) qp.set("tier", params.tier);
    if (params.month) qp.set("month", params.month);
    const qs = qp.toString();
    return request(`/api/v1/company-directory/companies${qs ? `?${qs}` : ""}`);
  },

  getCompany(idOrName: string): Promise<any> {
    return request(`/api/v1/company-directory/companies/${encodeURIComponent(idOrName)}`);
  },

  search(q: string): Promise<{ companies: any[]; count?: number }> {
    return request(`/api/v1/company-directory/search?q=${encodeURIComponent(q)}`);
  },

  getCalendar(): Promise<{ calendar: any }> {
    return request("/api/v1/company-directory/calendar");
  },

  getFilters(): Promise<{ types: string[]; tiers: string[]; months: string[] }> {
    return request("/api/v1/company-directory/filters");
  },

  getProgress(companyId: string): Promise<{ company_id: string; completed: string[] }> {
    return request(`/api/v1/company-directory/companies/${encodeURIComponent(companyId)}/progress`);
  },

  saveProgress(companyId: string, completed: string[]): Promise<any> {
    return request(`/api/v1/company-directory/companies/${encodeURIComponent(companyId)}/progress`, {
      method: "POST",
      body: JSON.stringify({ completed }),
    });
  },
};