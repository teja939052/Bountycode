import { requestWithRetry as request, API_BASE, requestBlob } from "./request.ts";
export const resumeApi = {
  uploadResume(file) {
    const formData = new FormData();
    formData.append("file", file);

    return fetch(`${API_BASE}/api/resume/upload`, {
      method: "POST",
      credentials: "include",
      body: formData,
    }).then((r) => {
      if (r.status === 401) throw new Error("Session expired");
      if (!r.ok) throw new Error("Upload failed");
      return r.json();
    });
  },

  generateResume(details) {
    return request("/api/v1/resume/generate", {
      method: "POST",
      body: JSON.stringify(details),
    });
  },

  optimizeResume(resumeId, jobDescription) {
    return request("/api/v1/resume/optimize", {
      method: "POST",
      body: JSON.stringify({ resume_id: resumeId, job_description: jobDescription }),
    });
  },

  exportResume(resumeId, format) {
    return requestBlob(`/api/v1/resume/${resumeId}/export/${format}`);
  },

  getHistory() {
    return request("/api/v1/resume/history");
  },

  semanticScore(resumeText, jobDescription = "") {
    return request("/api/v1/resume/semantic-score", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
    });
  },
};