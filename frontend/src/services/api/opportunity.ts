// @ts-nocheck
import { requestWithRetry } from "./request.ts";

export const opportunityApi = {
  getOpportunity(companyId: string, _variant?: string) {
    const safeCompany = encodeURIComponent(companyId || "");
    return requestWithRetry(`/api/v1/opportunity/company/${safeCompany}`, {
      skipAuthRefresh: false,
    }).catch(() => ({
      company: companyId,
      assessment_variant: _variant || "generic",
      version: "0.1.0",
      effective_date: new Date().toISOString().slice(0, 10),
      interview_rounds: [],
      min_skills: {},
      min_solved: 0,
      typical_timeline_weeks: null,
    }));
  },

  getOpportunityFit(companyId: string, _variant?: string) {
    const safeCompany = encodeURIComponent(companyId || "");
    return requestWithRetry(`/api/v1/opportunity/company/${safeCompany}/fit?role=${encodeURIComponent(_variant || "")}`, {
      skipAuthRefresh: false,
    }).catch(() => ({
      company: companyId,
      role: _variant || null,
      fit_score: 0,
      matched: [],
      gaps: [],
    }));
  },

  getCapabilityGaps(companyId: string, _variant?: string) {
    const safeCompany = encodeURIComponent(companyId || "");
    return requestWithRetry(`/api/v1/opportunity/company/${safeCompany}/gaps?role=${encodeURIComponent(_variant || "")}`, {
      skipAuthRefresh: false,
    }).catch(() => ({
      company: companyId,
      role: _variant || null,
      gaps: [],
    }));
  },

  getAdaptivePlan(_companyId: string | null, _variant?: string) {
    return requestWithRetry(`/api/v1/opportunity/adaptive-plan?company=${encodeURIComponent(_companyId || "")}&role=${encodeURIComponent(_variant || "")}`, {
      skipAuthRefresh: false,
    }).catch(() => ({
      plan: [],
      focus_areas: [],
      weekly_targets: {},
    }));
  },
};
