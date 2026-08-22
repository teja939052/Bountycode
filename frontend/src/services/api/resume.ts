import {
  requestWithRetry as request,
  requestBlob,
  API_BASE,
} from "./request.ts";
import type { ResumeData, ResumeAnalysis, ATSScoreResponse } from "./types.ts";

export const resumeApi = {
  uploadResume(file: File): Promise<ResumeAnalysis> {
    const formData = new FormData();
    formData.append("file", file);

    return fetch(`${API_BASE}/api/v1/resume/upload`, {
      method: "POST",
      credentials: "include",
      body: formData,
    }).then((r) => {
      if (r.status === 401) throw new Error("Session expired");
      if (!r.ok) throw new Error("Upload failed");
      return r.json();
    });
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

  getResume(resumeId: string): Promise<ResumeData> {
    return request(`/api/v1/resume/${encodeURIComponent(resumeId)}`);
  },

  deleteResume(resumeId: string): Promise<{ deleted: boolean }> {
    return request(`/api/v1/resume/${encodeURIComponent(resumeId)}`, {
      method: "DELETE",
    });
  },
};
