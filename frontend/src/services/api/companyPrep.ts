import { requestWithRetry as request } from "./request.ts";
export const companyPrepApi = {
  getCompanies() {
    return request("/api/v1/company/companies");
  },

  getBehavioralQuestion(company, role) {
    return request("/api/v1/company/behavioral", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    });
  },

  getInterviewTips(company, role, roundType) {
    return request("/api/v1/company/tips", {
      method: "POST",
      body: JSON.stringify({ company, role, round_type: roundType }),
    });
  },

  getGuide(company) {
    return request(`/api/v1/company/${company}/guide`);
  },
};

export const companyMocksApi = {
  getCompanies() {
    return request("/api/v1/company-mocks/companies");
  },

  getConfig(companyId) {
    return request(`/api/v1/company-mocks/${companyId}/config`);
  },

  start(companyId, roundName = null) {
    return request(`/api/v1/company-mocks/${companyId}/start`, {
      method: "POST",
      body: JSON.stringify({ round_name: roundName }),
    });
  },

  getStatus(sessionId) {
    return request(`/api/v1/company-mocks/${sessionId}/status`);
  },

  getResults(sessionId) {
    return request(`/api/v1/company-mocks/${sessionId}/results`);
  },
};