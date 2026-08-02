import { requestWithRetry as request } from "./request.ts";
export const studentApi = {
  getCheatSheet(company, topic) {
    return request("/api/v1/student/cheatsheet", {
      method: "POST",
      body: JSON.stringify({ company, topic }),
    });
  },

  getCheatSheetTemplates() {
    return request("/api/v1/student/cheatsheet/templates");
  },

  humanizeBullet(bullet) {
    return request("/api/v1/student/humanize/bullet", {
      method: "POST",
      body: JSON.stringify({ bullet }),
    });
  },

  humanizeResume(resumeText) {
    return request("/api/v1/student/humanize/resume", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText }),
    });
  },

  createApplication(company, role, jobUrl = "", notes = "") {
    return request("/api/v1/student/applications", {
      method: "POST",
      body: JSON.stringify({ company, role, job_url: jobUrl, notes }),
    });
  },

  getApplicationPipeline() {
    return request("/api/v1/student/applications/pipeline");
  },

  updateApplicationStage(applicationId, newStage) {
    return request("/api/v1/student/applications/stage", {
      method: "PUT",
      body: JSON.stringify({ application_id: applicationId, new_stage: newStage }),
    });
  },

  getApplicationStats() {
    return request("/api/v1/student/applications/stats");
  },

  deleteApplication(applicationId) {
    return request(`/api/v1/student/applications/${applicationId}`, {
      method: "DELETE",
    });
  },

  getPipelineStages() {
    return request("/api/v1/student/applications/stages");
  },

  getDailyDrill() {
    return request("/api/v1/student/drill/daily", { method: "POST" });
  },

  submitDrill(drillId, answers) {
    return request("/api/v1/student/drill/submit", {
      method: "POST",
      body: JSON.stringify({ drill_id: drillId, answers }),
    });
  },

  syncGitHub(githubUrl) {
    return request("/api/v1/student/sync/github", {
      method: "POST",
      body: JSON.stringify({ github_url: githubUrl }),
    });
  },

  generateBulletsFromProjects(projects, role = "Software Engineer") {
    return request("/api/v1/student/sync/generate-bullets", {
      method: "POST",
      body: JSON.stringify({ projects, role }),
    });
  },
};