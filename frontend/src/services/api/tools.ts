import { requestWithRetry as request } from "./request.ts";
export const toolsApi = {
  generateCoverLetter(resumeId, jobDescription, companyName = "") {
    return request("/api/v1/tools/cover-letter", {
      method: "POST",
      body: JSON.stringify({ resume_id: resumeId, job_description: jobDescription, company_name: companyName }),
    });
  },

  generateLinkedInAbout(resumeId, targetRole = "") {
    return request("/api/v1/tools/linkedin-about", {
      method: "POST",
      body: JSON.stringify({ resume_id: resumeId, target_role: targetRole }),
    });
  },

  getSalaryNegotiationTips(jobTitle, offeredSalary, location, yearsExperience = 0, companySize = "", benefits = []) {
    return request("/api/v1/tools/salary-negotiation", {
      method: "POST",
      body: JSON.stringify({
        job_title: jobTitle,
        offered_salary: offeredSalary,
        location,
        years_experience: yearsExperience,
        company_size: companySize,
        benefits,
      }),
    });
  },

  getCoverLetterHistory() {
    return request("/api/v1/tools/cover-letter/history");
  },
};

export const salaryApi = {
  getBenchmark(jobTitle, location, company = "", yearsExperience = 0, level = "") {
    return request("/api/v1/salary/benchmark", {
      method: "POST",
      body: JSON.stringify({ job_title: jobTitle, location, company, years_experience: yearsExperience, level }),
    });
  },

  compareOffers(offers) {
    return request("/api/v1/salary/compare", {
      method: "POST",
      body: JSON.stringify({ offers }),
    });
  },
};