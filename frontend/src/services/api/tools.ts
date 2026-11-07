import { requestWithRetry as request } from "./request.ts";
export const toolsApi = {
  generateLinkedInAbout(resumeId, targetRole = "") {
    return request("/api/v1/tools/linkedin-about", {
      method: "POST",
      body: JSON.stringify({ resume_id: resumeId, target_role: targetRole }),
    });
  },
};
