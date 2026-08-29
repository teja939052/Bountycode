import { requestWithRetry as request } from "./request.ts";

export const curriculumApi = {
  // Meta & Stats
  getMeta() {
    return request("/api/v1/curriculum/meta");
  },

  getStats() {
    return request("/api/v1/curriculum/stats");
  },

  // Phases
  listPhases() {
    return request("/api/v1/curriculum/phases");
  },

  // Roles
  listRoles() {
    return request("/api/v1/curriculum/roles");
  },

  getRoleDetail(roleId) {
    return request(`/api/v1/curriculum/roles/${roleId}`);
  },

  getRoleSkill(roleId, skillId) {
    return request(`/api/v1/curriculum/roles/${roleId}/skill/${skillId}`);
  },

  getRolePhase(roleId, phaseId) {
    return request(`/api/v1/curriculum/roles/${roleId}/phase/${phaseId}`);
  },

  // Learning Modules
  listModules(params = {}) {
    const searchParams = new URLSearchParams();
    if (params.phase) searchParams.set("phase", params.phase);
    if (params.topic) searchParams.set("topic", params.topic);
    if (params.difficulty) searchParams.set("difficulty", params.difficulty);
    const qs = searchParams.toString();
    return request(`/api/v1/curriculum/modules${qs ? `?${qs}` : ""}`);
  },

  getModuleDetail(moduleId) {
    return request(`/api/v1/curriculum/modules/${moduleId}`);
  },

  // Companies
  listCompanies() {
    return request("/api/v1/curriculum/companies");
  },

  getCompanyDetail(companyId) {
    return request(`/api/v1/curriculum/companies/${companyId}`);
  },

  // Personalized Path
  getCurriculumPath(roleId, company = null) {
    const params = new URLSearchParams();
    params.set("role_id", roleId);
    if (company) params.set("company", company);
    return request(`/api/v1/curriculum/path?${params.toString()}`);
  },
};

export default curriculumApi;
