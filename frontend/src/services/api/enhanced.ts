import { requestWithRetry as request } from "./request.ts";
export const enhancedApi = {
  improveBullet(bullet, jobRole = "") {
    return request("/api/v1/enhanced/resume/improve-bullet", {
      method: "POST",
      body: JSON.stringify({ bullet, job_role: jobRole }),
    });
  },

  improveBullets(bullets, jobRole = "") {
    return request("/api/v1/enhanced/resume/improve-bullets", {
      method: "POST",
      body: JSON.stringify({ bullets, job_role: jobRole }),
    });
  },

  getATSChecklist(resumeText) {
    return request("/api/v1/enhanced/resume/ats-checklist", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText }),
    });
  },

  tailorResume(resumeText, jobDescription, jobRole = "") {
    return request("/api/v1/enhanced/resume/tailor", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription, job_role: jobRole }),
    });
  },

  getCompanyChallenge(company, role = "SDE", difficulty = null) {
    return request("/api/v1/enhanced/coding/company-challenge", {
      method: "POST",
      body: JSON.stringify({ company, role, difficulty }),
    });
  },

  getCodeReviewerFeedback(code, language, problemDescription) {
    return request("/api/v1/enhanced/coding/interviewer-feedback", {
      method: "POST",
      body: JSON.stringify({ code, language, problem_description: problemDescription }),
    });
  },

  explainConcept(concept, level = "intermediate") {
    return request("/api/v1/enhanced/coding/explain", {
      method: "POST",
      body: JSON.stringify({ concept, level }),
    });
  },

  getHint(problemDescription, currentCode = "", hintLevel = 1) {
    return request("/api/v1/enhanced/coding/hint", {
      method: "POST",
      body: JSON.stringify({ problem_description: problemDescription, current_code: currentCode, hint_level: hintLevel }),
    });
  },

  evaluateSTAR(question, answer, company = "", leadershipPrinciples = []) {
    return request("/api/v1/enhanced/behavioral/evaluate-star", {
      method: "POST",
      body: JSON.stringify({ question, answer, company, leadership_principles: leadershipPrinciples }),
    });
  },

  getSTAR模板(question, company = "", role = "") {
    return request("/api/v1/enhanced/behavioral/star-template", {
      method: "POST",
      body: JSON.stringify({ question, company, role }),
    });
  },

  getBehavioralQuestions(company, role, count = 5) {
    return request("/api/v1/enhanced/behavioral/practice-questions", {
      method: "POST",
      body: JSON.stringify({ company, role, count }),
    });
  },

  getSemanticATS(resumeText, jobDescription = "") {
    return request("/api/v1/enhanced/ats/semantic", {
      method: "POST",
      body: JSON.stringify({ resume_text: resumeText, job_description: jobDescription }),
    });
  },
};

export const freePracticeApi = {
  quickInterview(jobRole = "Software Engineer") {
    return request("/api/v1/free/quick-interview", {
      method: "POST",
      body: JSON.stringify({ job_role: jobRole }),
    });
  },

  quickEvaluate(question, answer, jobRole = "Software Engineer") {
    return request("/api/v1/free/quick-evaluate", {
      method: "POST",
      body: JSON.stringify({ question, answer, job_role: jobRole }),
    });
  },
};