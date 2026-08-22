import { requestWithRetry as request } from "./request.ts";

export const companyDirectoryApi = {
  getCompanies(params: Record<string, any> = {}) {
    const qs = new URLSearchParams(
      Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== "")
    ).toString();
    return request(`/api/v1/company-directory/companies${qs ? `?${qs}` : ""}`);
  },

  getCompany(id: string) {
    return request(`/api/v1/company-directory/companies/${id}`);
  },

  search(q: string) {
    return request(`/api/v1/company-directory/search?q=${encodeURIComponent(q)}`);
  },

  getCalendar() {
    return request(`/api/v1/company-directory/calendar`);
  },

  getFilters() {
    return request(`/api/v1/company-directory/filters`);
  },

  getProgress(companyId: string) {
    return request(`/api/v1/company-directory/companies/${companyId}/progress`);
  },

  saveProgress(companyId: string, completed: string[]) {
    return request(`/api/v1/company-directory/companies/${companyId}/progress`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed }),
    });
  },
};
