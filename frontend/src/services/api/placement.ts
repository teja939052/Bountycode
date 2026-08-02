import { requestWithRetry as request } from "./request.ts";
export const placementApi = {
  predictOffer(company, role = "SDE") {
    return request("/api/v1/predictor/predict", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    });
  },

  predictOfferByCompany(company, role = "SDE") {
    return request(`/api/v1/predictor/predict/${company}?role=${role}`);
  },

  getPredictionHistory() {
    return request("/api/v1/predictor/history");
  },

  getSupportedCompanies() {
    return request("/api/v1/predictor/companies");
  },

  getCompaniesByTier(tier) {
    return request(`/api/v1/predictor/companies/${tier}`);
  },

  getTierWeights() {
    return request("/api/v1/predictor/tiers");
  },

  getSubSkills() {
    return request("/api/v1/predictor/sub-skills");
  },

  getGapAnalysis(company, targetProbability = 75) {
    return request("/api/v1/placement/gap-analysis", {
      method: "POST",
      body: JSON.stringify({ company, target_probability: targetProbability }),
    });
  },

  getCompanyProbability(company, target = 75) {
    return request(`/api/v1/placement/probability/${encodeURIComponent(company)}?target=${target}`);
  },

  getDashboardInsights() {
    return request("/api/v1/placement/dashboard-insights");
  },

  getAlumniExperiences(company = null, role = null, limit = 20) {
    const params = new URLSearchParams();
    if (company) params.set("company", company);
    if (role) params.set("role", role);
    params.set("limit", limit.toString());
    return request(`/api/v1/placement/alumni?${params.toString()}`);
  },

  getPlacementDrives(limit = 10) {
    return request(`/api/v1/placement/drives?limit=${limit}`);
  },
};

export const indianPlacementApi = {
  getCompanies() {
    return request("/api/v1/indian-placement/companies");
  },

  getCompanyDetail(companyId) {
    return request(`/api/v1/indian-placement/${companyId}`);
  },

  getMockConfig(companyId) {
    return request(`/api/v1/indian-placement/${companyId}/mock-config`);
  },

  getHRQuestions(companyId) {
    return request(`/api/v1/indian-placement/${companyId}/hr-questions`);
  },

  getCodingPatterns(companyId) {
    return request(`/api/v1/indian-placement/${companyId}/coding-patterns`);
  },

  startMock(companyId, sectionName = null) {
    return request("/api/v1/indian-placement/start-mock", {
      method: "POST",
      body: JSON.stringify({ company_id: companyId, section_name: sectionName }),
    });
  },
};