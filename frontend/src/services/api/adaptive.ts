import { requestWithRetry as request } from "./request.ts";
export const adaptiveApi = {
  getSkillAssessment() {
    return request("/api/v1/adaptive/skills");
  },

  getWeakAreas() {
    return request("/api/v1/adaptive/weak-areas");
  },

  getDailyPlan(force = false) {
    const params = force ? "?force=true" : "";
    return request(`/api/v1/adaptive/daily-plan${params}`);
  },

  getRecommendations() {
    return request("/api/v1/adaptive/recommendations");
  },

  getLearningPath(company = null) {
    const params = company ? `?company=${encodeURIComponent(company)}` : "";
    return request(`/api/v1/adaptive/learning-path${params}`);
  },

  getReadinessScore(company = null) {
    const params = company ? `?company=${encodeURIComponent(company)}` : "";
    return request(`/api/v1/adaptive/readiness${params}`);
  },

  recordActivity(activity) {
    return request("/api/v1/adaptive/activity", {
      method: "POST",
      body: JSON.stringify(activity),
    });
  },
};

export const predictorApi = {
  predictOffer(company, role = "SDE") {
    return request("/api/v1/predictor/predict", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    });
  },

  predictOfferByCompany(company, role = "SDE") {
    return request(`/api/v1/predictor/predict/${company}?role=${role}`);
  },

  getHistory() {
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
};

export const readinessApi = {
  getCompanyReadiness(companyName) {
    return request(`/api/v1/readiness/company/${encodeURIComponent(companyName)}`);
  },
};