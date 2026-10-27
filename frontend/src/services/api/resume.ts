// @ts-nocheck
import {
  requestWithRetry as request,
  requestBlob,
} from "./request.ts";
import type { ResumeData, ResumeAnalysis, ATSScoreResponse } from "./types.ts";

export const resumeApi = {
  uploadResume(file: File): Promise<ResumeAnalysis> {
    const formData = new FormData();
    formData.append("file", file);

    // POSTs are never retried inside requestWithRetry, so the upload is safe there.
    return request("/api/v1/resume/upload", {
      method: "POST",
      body: formData,
    }) as Promise<ResumeAnalysis>;
  },

  generateResume(details: Record<string, unknown>): Promise<ResumeData> {
    return request("/api/v1/resume/generate", {
      method: "POST",
      body: JSON.stringify(details),
    });
  },

  optimizeResume(
    resumeId: string,
    jobDescription: string,
  ): Promise<ResumeData> {
    return request("/api/v1/resume/optimize", {
      method: "POST",
      body: JSON.stringify({
        resume_id: resumeId,
        job_description: jobDescription,
      }),
    });
  },

  exportResume(resumeId: string, format: "docx" | "pdf"): Promise<Blob> {
    return requestBlob(`/api/v1/resume/${resumeId}/export/${format}`);
  },

  getHistory(): Promise<ResumeData[]> {
    return request("/api/v1/resume/history");
  },

  semanticScore(
    resumeText: string,
    jobDescription = "",
  ): Promise<ATSScoreResponse> {
    return request("/api/v1/resume/semantic-score", {
      method: "POST",
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
      }),
    });
  },

  improveBullets(
    bullets: string[] | string,
    jobRole = "",
  ): Promise<{ improvements: Array<Record<string, unknown>> }> {
    const list = Array.isArray(bullets)
      ? bullets
      : String(bullets).split("\n").map((b) => b.trim()).filter(Boolean);
    return request("/api/v1/resume/improve-bullets", {
      method: "POST",
      body: JSON.stringify({ bullets: list, job_role: jobRole }),
    });
  },

  analyzeRuleBased(
    resumeText: string,
    jobDescription = "",
  ): Promise<Record<string, unknown>> {
    return request("/api/v1/resume/analyze-rulebased", {
      method: "POST",
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
      }),
    });
  },

  getResume(resumeId: string): Promise<ResumeData> {
    return request(`/api/v1/resume/${encodeURIComponent(resumeId)}`);
  },

  deleteResume(resumeId: string): Promise<{ deleted: boolean }> {
    return request(`/api/v1/resume/${encodeURIComponent(resumeId)}`, {
      method: "DELETE",
    });
  },
};
