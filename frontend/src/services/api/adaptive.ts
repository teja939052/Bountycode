import { requestWithRetry as request } from "./request.ts";
import type { StartupState } from "./types.ts";

export const adaptiveApi = {
  getSkillAssessment(): Promise<Record<string, unknown>> {
    return request("/api/v1/adaptive/skills");
  },

  getWeakAreas(): Promise<Record<string, unknown>> {
    return request("/api/v1/adaptive/weak-areas");
  },

  getDailyPlan(force = false): Promise<Record<string, unknown>> {
    const params = force ? "?force=true" : "";
    return request(`/api/v1/adaptive/daily-plan${params}`);
  },

  getRecommendations(): Promise<Record<string, unknown>> {
    return request("/api/v1/adaptive/recommendations");
  },

  getLearningPath(
    company: string | null = null,
  ): Promise<Record<string, unknown>> {
    const params = company ? `?company=${encodeURIComponent(company)}` : "";
    return request(`/api/v1/adaptive/learning-path${params}`);
  },

  getReadinessScore(company: string | null = null): Promise<{ score: number }> {
    const params = company ? `?company=${encodeURIComponent(company)}` : "";
    return request(`/api/v1/adaptive/readiness${params}`);
  },

  recordActivity(
    activity: Record<string, unknown>,
  ): Promise<{ xp_earned?: number }> {
    return request("/api/v1/adaptive/activity", {
      method: "POST",
      body: JSON.stringify(activity),
    });
  },
};

export const predictorApi = {
  predictOffer(
    company: string,
    role = "SDE",
  ): Promise<Record<string, unknown>> {
    return request("/api/v1/predictor/predict", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    });
  },

  predictOfferByCompany(
    company: string,
    role = "SDE",
  ): Promise<Record<string, unknown>> {
    return request(
      `/api/v1/predictor/predict/${encodeURIComponent(company)}?role=${encodeURIComponent(role)}`,
    );
  },

  getHistory(): Promise<Record<string, unknown>[]> {
    return request("/api/v1/predictor/history");
  },

  getSupportedCompanies(): Promise<{ companies: string[] }> {
    return request("/api/v1/predictor/companies");
  },

  getCompaniesByTier(tier: string): Promise<Record<string, unknown>> {
    return request(`/api/v1/predictor/companies/${encodeURIComponent(tier)}`);
  },

  getTierWeights(): Promise<Record<string, unknown>> {
    return request("/api/v1/predictor/tiers");
  },

  getSubSkills(): Promise<Record<string, unknown>> {
    return request("/api/v1/predictor/sub-skills");
  },

  recordOutcome(
    payload: Record<string, unknown>,
  ): Promise<{ recorded?: boolean }> {
    return request("/api/v1/predictor/outcome", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },

  getOutcomes(): Promise<Record<string, unknown>[]> {
    return request("/api/v1/predictor/outcomes");
  },

  deleteOutcome(outcomeId: string): Promise<{ deleted?: boolean }> {
    return request(
      `/api/v1/predictor/outcome/${encodeURIComponent(outcomeId)}`,
      {
        method: "DELETE",
      },
    );
  },

  getOutcomeStats(): Promise<Record<string, unknown>> {
    return request("/api/v1/predictor/outcome-stats");
  },

  timeToOffer(company: string, role = "SDE"): Promise<Record<string, unknown>> {
    return request("/api/v1/predictor/time-to-offer", {
      method: "POST",
      body: JSON.stringify({ company, role }),
    });
  },
};

export const readinessApi = {
  getCompanyReadiness(companyName: string): Promise<StartupState> {
    return request(
      `/api/v1/readiness/company/${encodeURIComponent(companyName)}`,
    );
  },
};
