import { requestWithRetry as request } from "./request.ts";
import type { ResumeAnalysis } from "./types.ts";

export const studentApi = {
  getCheatSheet(company: string, topic: string): Promise<ResumeAnalysis> {
    return request("/api/v1/student/cheatsheet", {
      method: "POST",
      body: JSON.stringify({ company, topic }),
    });
  },

  getCheatSheetTemplates(): Promise<{ templates: string[] }> {
    return request("/api/v1/student/cheatsheet/templates");
  },

  humanizeBullet(bullet: string): Promise<{ humanized: string }> {
    return request("/api/v1/student/humanize/bullet", {
      method: "POST",
      body: JSON.stringify({ bullet }),
    });
  },

  humanizeResume(resumeText: string): Promise<{ humanized: string }> {
    return request("/api/v1/student/humanize/resume", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText }),
    });
  },

  createApplication(
    company: string,
    role: string,
    jobUrl = "",
    notes = "",
  ): Promise<{ id: string; status: string }> {
    return request("/api/v1/student/applications", {
      method: "POST",
      body: JSON.stringify({ company, role, job_url: jobUrl, notes }),
    });
  },

  getApplicationPipeline(): Promise<{
    applications: Record<string, unknown>[];
  }> {
    return request("/api/v1/student/applications/pipeline");
  },

  updateApplicationStage(
    applicationId: string,
    newStage: string,
  ): Promise<{ updated?: boolean }> {
    return request("/api/v1/student/applications/stage", {
      method: "PUT",
      body: JSON.stringify({
        application_id: applicationId,
        new_stage: newStage,
      }),
    });
  },

  getApplicationStats(): Promise<Record<string, unknown>> {
    return request("/api/v1/student/applications/stats");
  },

  deleteApplication(applicationId: string): Promise<{ deleted?: boolean }> {
    return request(
      `/api/v1/student/applications/${encodeURIComponent(applicationId)}`,
      {
        method: "DELETE",
      },
    );
  },

  getPipelineStages(): Promise<{ stages: string[] }> {
    return request("/api/v1/student/applications/stages");
  },

  getDailyDrill(): Promise<Record<string, unknown>> {
    return request("/api/v1/student/drill/daily", { method: "POST" });
  },

  submitDrill(
    drillId: string,
    answers: Record<string, unknown>,
  ): Promise<{ score?: number; results?: Record<string, unknown> }> {
    return request("/api/v1/student/drill/submit", {
      method: "POST",
      body: JSON.stringify({ drill_id: drillId, answers }),
    });
  },

  syncGitHub(
    githubUrl: string,
  ): Promise<{ synced?: boolean; profile?: Record<string, unknown> }> {
    return request("/api/v1/student/sync/github", {
      method: "POST",
      body: JSON.stringify({ github_url: githubUrl }),
    });
  },

  generateBulletsFromProjects(
    projects: Record<string, unknown>[],
    role = "Software Engineer",
  ): Promise<{ bullets: string[] }> {
    return request("/api/v1/student/sync/generate-bullets", {
      method: "POST",
      body: JSON.stringify({ projects, role }),
    });
  },
};
